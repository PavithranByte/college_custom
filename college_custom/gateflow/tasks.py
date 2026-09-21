# Copyright (c) 2026, pavithran and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import now_datetime, get_datetime


def check_expired_passes():
	settings = frappe.get_single("Gate Pass Settings")
	now = get_datetime(now_datetime())

	# Expire passes where valid_upto < now and status is still Approved or Pending Approval
	overdue_passes = frappe.get_all(
		"Gate Pass",
		filters={
			"docstatus": 1,
			"status": ["in", ["Pending Approval", "Approved"]],
			"valid_upto": ["<", now]
		},
		fields=["name", "status"]
	)

	for p in overdue_passes:
		doc = frappe.get_doc("Gate Pass", p.name)
		doc.db_set("status", "Expired")
		frappe.get_doc({
			"doctype": "Gate Pass Log",
			"gate_pass": doc.name,
			"action": "Expiration",
			"log_datetime": now_datetime(),
			"gate_name": "System Task",
			"user": "Administrator",
			"remarks": "Pass auto-expired by background task."
		}).insert(ignore_permissions=True)
