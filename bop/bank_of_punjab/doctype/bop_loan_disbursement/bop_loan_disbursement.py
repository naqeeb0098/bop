# Copyright (c) 2024, Pukat Digital and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BOPLoanDisbursement(Document):
    @frappe.whitelist()
    def update_loan_status(self):
        disb_loan_name =self.against_loan
        date = self.disbursement_date
        frappe.db.sql(f"""UPDATE `tabBOP Loan` set status = 'Disbursed', disbursement_date = '{date}' where name = '{disb_loan_name}'""",as_dict = True)
        frappe.db.commit()     
        
    @frappe.whitelist()
    def reverse_loan_status(loan_disbursement):
        disbursement = frappe.get_doc("BOP Loan Disbursement", loan_disbursement)
        loan = frappe.get_doc("BOP Loan", disbursement.bop_loan)
        loan.status = "Sanctioned" 
        loan.save()
		