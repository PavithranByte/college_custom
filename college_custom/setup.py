# Copyright (c) 2026, pavithran and contributors
# For license information, please see license.txt

import frappe


def after_install():
	setup_default_gate_pass_types()
	setup_default_gate_pass_settings()


def after_migrate():
	setup_default_gate_pass_types()
	setup_default_gate_pass_settings()


def setup_default_gate_pass_types():
	if not frappe.db.exists("DocType", "Gate Pass Type"):
		return

	default_types = [
		{
			"pass_type_name": "Student Outpass",
			"pass_category": "Student",
			"requires_approval": 1,
			"allowed_movement_type": "Both",
			"max_duration_hours": 12,
			"description": "Standard movement outpass for campus students."
		},
		{
			"pass_type_name": "Employee Duty Pass",
			"pass_category": "Employee",
			"requires_approval": 1,
			"allowed_movement_type": "Both",
			"max_duration_hours": 8,
			"description": "Official duty pass for staff & faculty members."
		},
		{
			"pass_type_name": "Visitor Entry Pass",
			"pass_category": "Visitor",
			"requires_approval": 0,
			"allowed_movement_type": "Both",
			"max_duration_hours": 4,
			"description": "Visitor & parent entry pass."
		},
		{
			"pass_type_name": "Material Outward (Returnable)",
			"pass_category": "Material/Vendor",
			"requires_approval": 1,
			"allowed_movement_type": "Both",
			"require_items_table": 1,
			"description": "Returnable equipment / material movement pass."
		},
		{
			"pass_type_name": "Material Outward (Non-Returnable)",
			"pass_category": "Material/Vendor",
			"requires_approval": 1,
			"allowed_movement_type": "Outward Only",
			"require_items_table": 1,
			"description": "Non-returnable material outward pass."
		}
	]

	for data in default_types:
		if not frappe.db.exists("Gate Pass Type", data["pass_type_name"]):
			doc = frappe.get_doc({
				"doctype": "Gate Pass Type",
				**data
			})
			doc.insert(ignore_permissions=True)


def setup_default_gate_pass_settings():
	if frappe.db.exists("DocType", "Gate Pass Settings"):
		settings = frappe.get_single("Gate Pass Settings")
		if not settings.naming_series:
			settings.naming_series = "GP-.YYYY.-.#####."
			settings.save(ignore_permissions=True)
