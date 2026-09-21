# Copyright (c) 2026, pavithran and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import validate_email_address


class Person(Document):
	def autoname(self):
		if self.person_id:
			self.person_id = self.person_id.strip()
			self.name = self.person_id
		else:
			prefix_map = {
				"Student": "STU-",
				"Employee": "EMP-",
				"Faculty": "FAC-",
				"Staff": "STF-",
				"Visitor": "VIS-",
				"Contractor": "CON-",
				"Vendor": "VEN-",
				"Other": "PER-"
			}
			prefix = prefix_map.get(self.person_type, "PER-")
			self.name = frappe.model.naming.make_autoname(f"{prefix}.#####")
			self.person_id = self.name

	def validate(self):
		self.clean_fields()
		self.validate_person_id_uniqueness()
		self.validate_email()
		self.validate_status_notes()

	def clean_fields(self):
		if self.person_id:
			self.person_id = self.person_id.strip()
		if self.full_name:
			self.full_name = self.full_name.strip()
		if self.email:
			self.email = self.email.strip()
		if self.phone:
			self.phone = self.phone.strip()

	def validate_person_id_uniqueness(self):
		if not self.person_id:
			frappe.throw(_("Person ID is mandatory."))

		existing = frappe.db.get_value("Person", {"person_id": self.person_id, "name": ["!=", self.name]}, "name")
		if existing:
			frappe.throw(_("Person ID {0} is already registered to person {1}.").format(self.person_id, existing))

	def validate_email(self):
		if self.email:
			validate_email_address(self.email, throw=True)

	def validate_status_notes(self):
		if self.status == "Blocked" and not self.notes:
			frappe.msgprint(_("Warning: Adding a note/reason when blocking a person is strongly recommended."), alert=True)
