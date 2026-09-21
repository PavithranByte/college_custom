// Copyright (c) 2026, pavithran and contributors
// For license information, please see license.txt

frappe.listview_settings["Person"] = {
	add_fields: ["status", "person_type", "full_name", "phone", "email"],
	get_indicator(doc) {
		if (doc.status === "Active") {
			return [__("Active"), "green", "status,=,Active"];
		} else if (doc.status === "Inactive") {
			return [__("Inactive"), "gray", "status,=,Inactive"];
		} else if (doc.status === "Blocked") {
			return [__("Blocked"), "red", "status,=,Blocked"];
		}
	}
};
