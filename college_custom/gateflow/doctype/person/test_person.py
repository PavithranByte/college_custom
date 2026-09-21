# Copyright (c) 2026, pavithran and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestPerson(FrappeTestCase):
	def tearDown(self):
		frappe.db.rollback()

	def test_create_person_for_all_major_types(self):
		person_types = ["Student", "Employee", "Faculty", "Staff", "Visitor", "Contractor", "Vendor", "Other"]

		for p_type in person_types:
			pid = f"TEST-{p_type.upper()}-001"
			if frappe.db.exists("Person", pid):
				frappe.delete_doc("Person", pid, force=True)

			doc = frappe.get_doc({
				"doctype": "Person",
				"person_id": pid,
				"full_name": f"Test {p_type} Person",
				"person_type": p_type,
				"status": "Active",
				"email": f"test.{p_type.lower()}@example.com",
				"phone": "9876543210",
				"department": "Computer Science" if p_type in ["Student", "Faculty", "Staff"] else "",
				"organization": "Partner Acme Corp" if p_type in ["Visitor", "Contractor", "Vendor"] else "College"
			})
			doc.insert(ignore_permissions=True)

			self.assertEqual(doc.person_id, pid)
			self.assertEqual(doc.status, "Active")
			self.assertEqual(doc.person_type, p_type)

	def test_duplicate_person_id_handling(self):
		pid = "TEST-DUP-001"
		if frappe.db.exists("Person", pid):
			frappe.delete_doc("Person", pid, force=True)

		doc1 = frappe.get_doc({
			"doctype": "Person",
			"person_id": pid,
			"full_name": "Original Person",
			"person_type": "Student",
			"status": "Active"
		})
		doc1.insert(ignore_permissions=True)

		# Attempt duplicate insert
		doc2 = frappe.get_doc({
			"doctype": "Person",
			"person_id": pid,
			"full_name": "Duplicate Person",
			"person_type": "Visitor",
			"status": "Active"
		})
		self.assertRaises(frappe.ValidationError, doc2.insert)

	def test_invalid_email_validation(self):
		doc = frappe.get_doc({
			"doctype": "Person",
			"person_id": "TEST-EMAIL-ERR",
			"full_name": "Bad Email Person",
			"person_type": "Student",
			"email": "invalid-email-address",
			"status": "Active"
		})
		self.assertRaises(frappe.InvalidEmailAddressError, doc.insert)

	def test_status_states(self):
		pid = "TEST-STATUS-001"
		if frappe.db.exists("Person", pid):
			frappe.delete_doc("Person", pid, force=True)

		doc = frappe.get_doc({
			"doctype": "Person",
			"person_id": pid,
			"full_name": "Status Test Person",
			"person_type": "Employee",
			"status": "Active"
		})
		doc.insert(ignore_permissions=True)

		# Change to Inactive
		doc.status = "Inactive"
		doc.save()
		self.assertEqual(frappe.db.get_value("Person", pid, "status"), "Inactive")

		# Change to Blocked
		doc.status = "Blocked"
		doc.notes = "Security violation on gate exit"
		doc.save()
		self.assertEqual(frappe.db.get_value("Person", pid, "status"), "Blocked")
