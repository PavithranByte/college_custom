// Copyright (c) 2026, pavithran and contributors
// For license information, please see license.txt

frappe.ui.form.on("Gate Pass", {
	person(frm) {
		if (frm.doc.person) {
			frappe.db.get_doc("Person", frm.doc.person).then(person => {
				frm.set_value("applicant_name", person.full_name);
				frm.set_value("phone", person.phone);
				frm.set_value("email", person.email);
				frm.set_value("applicant_user", person.user_id);
				frm.set_value("visitor_company", person.organization);
				frm.set_value("id_proof_type", person.id_proof_type);
				frm.set_value("id_proof_number", person.id_proof_number);
				frm.set_value("visitor_photo", person.photo);

				if (["Student"].includes(person.person_type)) {
					frm.set_value("pass_category", "Student");
				} else if (["Employee", "Faculty", "Staff"].includes(person.person_type)) {
					frm.set_value("pass_category", "Employee");
				} else if (["Visitor"].includes(person.person_type)) {
					frm.set_value("pass_category", "Visitor");
				} else {
					frm.set_value("pass_category", "Material/Vendor");
				}
			});
		}
	},

	refresh(frm) {
		if (frm.doc.docstatus === 1) {
			if (frm.doc.status === "Pending Approval") {
				frm.add_custom_button(__("Approve"), () => {
					frappe.call({
						method: "college_custom.gateflow.doctype.gate_pass.gate_pass.approve_gate_pass",
						args: { gate_pass_name: frm.doc.name },
						callback(r) {
							if (!r.exc) {
								frappe.msgprint(r.message);
								frm.reload_doc();
							}
						}
					});
				}, __("Gate Actions")).addClass("btn-success");

				frm.add_custom_button(__("Reject"), () => {
					frappe.prompt([
						{ fieldname: "reason", fieldtype: "Small Text", label: __("Reason for Rejection"), reqd: 1 }
					], (values) => {
						frappe.call({
							method: "college_custom.gateflow.doctype.gate_pass.gate_pass.reject_gate_pass",
							args: { gate_pass_name: frm.doc.name, reason: values.reason },
							callback(r) {
								if (!r.exc) {
									frappe.msgprint(r.message);
									frm.reload_doc();
								}
							}
						});
					}, __("Reject Gate Pass"), __("Submit"));
				}, __("Gate Actions")).addClass("btn-danger");
			}

			if (frm.doc.status === "Approved") {
				frm.add_custom_button(__("Record Exit (Check-Out)"), () => {
					frappe.call({
						method: "college_custom.gateflow.doctype.gate_pass.gate_pass.record_exit",
						args: { gate_pass_name: frm.doc.name },
						callback(r) {
							if (!r.exc) {
								frappe.msgprint(r.message);
								frm.reload_doc();
							}
						}
					});
				}, __("Gatekeeper Actions")).addClass("btn-primary");
			}

			if (frm.doc.status === "Out/Active") {
				frm.add_custom_button(__("Record Entry (Check-In)"), () => {
					frappe.call({
						method: "college_custom.gateflow.doctype.gate_pass.gate_pass.record_entry",
						args: { gate_pass_name: frm.doc.name },
						callback(r) {
							if (!r.exc) {
								frappe.msgprint(r.message);
								frm.reload_doc();
							}
						}
					});
				}, __("Gatekeeper Actions")).addClass("btn-success");
			}
		}
	}
});
