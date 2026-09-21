// Copyright (c) 2026, pavithran and contributors
// For license information, please see license.txt

frappe.ui.form.on("Person", {
	refresh(frm) {
		frm.trigger("set_status_indicator");

		if (!frm.is_new()) {
			// Action button to quickly issue Gate Pass for this person
			frm.add_custom_button(__("Create Gate Pass"), () => {
				frappe.model.with_doctype("Gate Pass", () => {
					let pass_doc = frappe.model.get_new_doc("Gate Pass");
					pass_doc.applicant_name = frm.doc.full_name;
					pass_doc.phone = frm.doc.phone;
					pass_doc.email = frm.doc.email;
					pass_doc.applicant_user = frm.doc.user_id;
					pass_doc.visitor_company = frm.doc.organization;
					pass_doc.id_proof_type = frm.doc.id_proof_type;
					pass_doc.id_proof_number = frm.doc.id_proof_number;
					pass_doc.visitor_photo = frm.doc.photo;

					// Map person category
					if (["Student"].includes(frm.doc.person_type)) {
						pass_doc.pass_category = "Student";
					} else if (["Employee", "Faculty", "Staff"].includes(frm.doc.person_type)) {
						pass_doc.pass_category = "Employee";
					} else if (["Visitor"].includes(frm.doc.person_type)) {
						pass_doc.pass_category = "Visitor";
					} else {
						pass_doc.pass_category = "Material/Vendor";
					}

					frappe.set_route("Form", "Gate Pass", pass_doc.name);
				});
			}, __("Actions")).addClass("btn-primary");
		}
	},

	person_type(frm) {
		frm.trigger("toggle_fields_by_type");
	},

	status(frm) {
		frm.trigger("set_status_indicator");
	},

	set_status_indicator(frm) {
		if (frm.doc.status === "Active") {
			frm.page.set_indicator(__("Active"), "green");
		} else if (frm.doc.status === "Inactive") {
			frm.page.set_indicator(__("Inactive"), "gray");
		} else if (frm.doc.status === "Blocked") {
			frm.page.set_indicator(__("Blocked"), "red");
		}
	},

	toggle_fields_by_type(frm) {
		let is_external = ["Visitor", "Contractor", "Vendor", "Other"].includes(frm.doc.person_type);
		frm.set_df_property("organization", "reqd", is_external ? 1 : 0);
	}
});
