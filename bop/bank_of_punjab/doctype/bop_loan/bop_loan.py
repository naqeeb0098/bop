# Copyright (c) 2024, Pukat Digital and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BOPLoan(Document):
    @staticmethod
    @frappe.whitelist(allow_guest=True)
    def check_salary_structure_assignment(doc_name):
        bop_loan = frappe.get_doc("BOP Loan", doc_name)
        employee_id = bop_loan.employee_id
        if not frappe.db.exists("Salary Structure Assignment", {"employee": employee_id, "docstatus": 1}):
            return {"error": f"Salary structure is not assigned for employee: {employee_id}"}
        else:
            return {"success": True}