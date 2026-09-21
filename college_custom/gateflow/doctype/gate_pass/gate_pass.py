# Copyright (c) 2026, pavithran and contributors
# For license information, please see license.txt

import secrets
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_datetime, now_datetime, get_url


class GatePass(Document):
	def validate(self):
		self.set_title()
		self.validate_dates()
		self.validate_type_requirements()
		self.ensure_verification_token()

	def set_title(self):
		self.title = f"{self.pass_type or 'Pass'} - {self.applicant_name or 'Applicant'}"

	def validate_dates(self):
		if self.valid_from and self.valid_upto:
			v_from = get_datetime(self.valid_from)
			v_upto = get_datetime(self.valid_upto)
			if v_upto <= v_from:
				frappe.throw(_("Valid Upto datetime must be after Valid From datetime."))

	def validate_type_requirements(self):
		if not self.pass_type:
			return

		pass_type_doc = frappe.get_doc("Gate Pass Type", self.pass_type)
		if pass_type_doc.require_vehicle_info and not self.vehicle_number:
			frappe.throw(_("Vehicle Number is mandatory for pass type {0}").format(self.pass_type))

		if pass_type_doc.require_items_table and not self.items:
			frappe.throw(_("At least one Item must be listed for pass type {0}").format(self.pass_type))

		settings = frappe.get_single("Gate Pass Settings")
		if self.pass_category == "Visitor" and settings.require_id_proof_for_visitors:
			if not self.id_proof_type or not self.id_proof_number:
				frappe.throw(_("ID Proof details are required for Visitor Gate Passes."))

	def ensure_verification_token(self):
		if not self.verification_token:
			self.verification_token = secrets.token_urlsafe(16)
		qr_data = f"GP_TOKEN:{self.name}:{self.verification_token}"
		self.qr_code_svg = qr_data

	def on_submit(self):
		if not self.pass_type:
			return

		pass_type_doc = frappe.get_doc("Gate Pass Type", self.pass_type)
		settings = frappe.get_single("Gate Pass Settings")

		if not pass_type_doc.requires_approval or settings.auto_approve_outpass:
			self.db_set("status", "Approved")
			self.db_set("approval_datetime", now_datetime())
			self.db_set("approver", frappe.session.user)
			create_log(self.name, "Approval", "Auto Approved upon Submission")
		else:
			self.db_set("status", "Pending Approval")
			create_log(self.name, "Approval", "Submitted and Pending Approval")


def create_log(gate_pass_name, action, remarks=None, gate_name="Main Gate"):
	log = frappe.get_doc({
		"doctype": "Gate Pass Log",
		"gate_pass": gate_pass_name,
		"action": action,
		"log_datetime": now_datetime(),
		"gate_name": gate_name,
		"user": frappe.session.user or "Administrator",
		"remarks": remarks or ""
	})
	log.insert(ignore_permissions=True)
	return log


@frappe.whitelist()
def approve_gate_pass(gate_pass_name, remarks=None):
	doc = frappe.get_doc("Gate Pass", gate_pass_name)
	if doc.docstatus != 1:
		frappe.throw(_("Pass must be submitted before approval."))

	doc.db_set("status", "Approved")
	doc.db_set("approval_datetime", now_datetime())
	doc.db_set("approver", frappe.session.user)
	create_log(doc.name, "Approval", remarks or "Approved by Approver")
	return {"status": "Approved", "message": _("Gate Pass approved successfully.")}


@frappe.whitelist()
def reject_gate_pass(gate_pass_name, reason):
	doc = frappe.get_doc("Gate Pass", gate_pass_name)
	doc.db_set("status", "Rejected")
	doc.db_set("rejection_reason", reason)
	create_log(doc.name, "Rejection", f"Reason: {reason}")
	return {"status": "Rejected", "message": _("Gate Pass rejected.")}


@frappe.whitelist()
def record_exit(gate_pass_name, gate_name="Main Gate"):
	doc = frappe.get_doc("Gate Pass", gate_pass_name)
	if doc.docstatus != 1:
		frappe.throw(_("Gate Pass is not submitted."))

	if doc.status not in ["Approved", "Pending Approval"]:
		settings = frappe.get_single("Gate Pass Settings")
		if not settings.allow_gatekeeper_overrides:
			frappe.throw(_("Cannot record exit for a pass with status: {0}").format(doc.status))

	doc.db_set("status", "Out/Active")
	doc.db_set("actual_exit_datetime", now_datetime())
	doc.db_set("exit_gatekeeper", frappe.session.user)
	create_log(doc.name, "Check Out", f"Exit recorded at {gate_name}", gate_name)

	if doc.movement_type == "Outward Only":
		doc.db_set("status", "Completed")

	return {"status": doc.status, "message": _("Check Out recorded successfully.")}


@frappe.whitelist()
def record_entry(gate_pass_name, gate_name="Main Gate"):
	doc = frappe.get_doc("Gate Pass", gate_pass_name)
	if doc.docstatus != 1:
		frappe.throw(_("Gate Pass is not submitted."))

	if doc.movement_type == "Outward Only":
		frappe.throw(_("This pass is registered for Outward Movement Only."))

	doc.db_set("status", "Returned")
	doc.db_set("actual_entry_datetime", now_datetime())
	doc.db_set("entry_gatekeeper", frappe.session.user)
	create_log(doc.name, "Check In", f"Entry recorded at {gate_name}", gate_name)
	doc.db_set("status", "Completed")

	return {"status": "Completed", "message": _("Check In recorded and Pass completed.")}


@frappe.whitelist()
def verify_pass_token(token):
	passes = frappe.get_all("Gate Pass", filters={"verification_token": token}, fields=["name", "status", "applicant_name", "pass_type", "valid_from", "valid_upto"])
	if not passes:
		return {"valid": False, "message": _("Invalid or non-existent token.")}

	p = passes[0]
	now = get_datetime(now_datetime())
	v_upto = get_datetime(p.valid_upto)

	is_expired = now > v_upto
	return {
		"valid": True,
		"gate_pass": p.name,
		"status": p.status,
		"applicant_name": p.applicant_name,
		"pass_type": p.pass_type,
		"is_expired": is_expired,
		"message": _("Pass token verified.")
	}
