# Copyright (c) 2026, pavithran and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_hours, now_datetime

from college_custom.gateflow.doctype.gate_pass.gate_pass import (
	approve_gate_pass,
	record_entry,
	record_exit,
	verify_pass_token,
)
from college_custom.setup import setup_default_gate_pass_types


class TestGatePass(FrappeTestCase):
	def setUp(self):
		setup_default_gate_pass_types()

	def test_create_and_process_gate_pass(self):
		valid_from = now_datetime()
		valid_upto = add_hours(valid_from, 4)

		doc = frappe.get_doc({
			"doctype": "Gate Pass",
			"pass_type": "Student Outpass",
			"pass_category": "Student",
			"movement_type": "Two-Way",
			"applicant_name": "Test Student",
			"valid_from": valid_from,
			"valid_upto": valid_upto,
			"purpose": "Personal work"
		})
		doc.insert()
		self.assertIsNotNone(doc.verification_token)

		# Submit doc
		doc.submit()
		self.assertIn(doc.status, ["Pending Approval", "Approved"])

		# Approve pass
		approve_res = approve_gate_pass(doc.name, "Approved for testing")
		self.assertEqual(approve_res["status"], "Approved")

		# Check token verification
		token_res = verify_pass_token(doc.verification_token)
		self.assertTrue(token_res["valid"])
		self.assertEqual(token_res["gate_pass"], doc.name)

		# Record exit
		exit_res = record_exit(doc.name, "North Gate")
		self.assertEqual(exit_res["status"], "Out/Active")

		# Record entry
		entry_res = record_entry(doc.name, "North Gate")
		self.assertEqual(entry_res["status"], "Completed")
