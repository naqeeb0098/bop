# Copyright (c) 2024, Pukat Digital and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BOPLoanDisbursement(Document):
    def on_submit(self):
        frappe.log_error(f"on_submit called for {self.name}", "BOP Loan Disbursement Submission")
        self.update_loan_status()

    @frappe.whitelist()
    def update_loan_status(self):
        disb_loan_name = self.against_loan
        date = self.disbursement_date
        try:
            frappe.log_error(f"Updating loan {disb_loan_name} status to Disbursed", "BOP Loan Update")
            frappe.db.sql("""
                UPDATE `tabBOP Loan`
                SET status = 'Disbursed', disbursement_date = %s
                WHERE name = %s
            """, (date, disb_loan_name))
            frappe.db.commit()
            frappe.log_error(f"Loan {disb_loan_name} status updated to Disbursed successfully", "BOP Loan Update Success")
        except Exception as e:
            frappe.log_error(f"Error updating loan {disb_loan_name}: {str(e)}", "BOP Loan Update Failure")
            frappe.db.rollback()
            frappe.throw(f"Error updating loan {disb_loan_name}: {str(e)}")

    def on_cancel(self):
        frappe.log_error(f"on_cancel called for {self.name}", "BOP Loan Disbursement Cancelation")
        self.reverse_loan_status()

    @frappe.whitelist()
    def reverse_loan_status(self):
        disb_loan_name = self.against_loan
        # date = self.disbursement_date
        try:
            frappe.log_error(f"Updating loan {disb_loan_name} status to Sanctioned", "BOP Loan Update")
            frappe.db.sql("""
                UPDATE `tabBOP Loan`
                SET status = 'Sanctioned'
                WHERE name = %s
            """, (disb_loan_name))
            frappe.db.commit()
            frappe.log_error(f"Loan {disb_loan_name} status updated to Sanctioned successfully", "BOP Loan Update Success")
        except Exception as e:
            frappe.log_error(f"Error updating loan {disb_loan_name}: {str(e)}", "BOP Loan Update Failure")
            frappe.db.rollback()
            frappe.throw(f"Error updating loan {disb_loan_name}: {str(e)}")



# class BOPLoanDisbursement(Document):
#     @frappe.whitelist()
#     def update_loan_status(self):
#         disb_loan_name =self.against_loan
#         date = self.disbursement_date
#         frappe.db.sql(f"""UPDATE `tabBOP Loan` set status = 'Disbursed', disbursement_date = '{date}' where name = '{disb_loan_name}'""",as_dict = True)
#         frappe.db.commit()     
        
#     @frappe.whitelist()
#     def reverse_loan_status(self):
#         disb_loan_name =self.against_loan
#         frappe.db.sql(f"""UPDATE `tabBOP Loan` set status = 'Sanctioned' where name = '{disb_loan_name}'""",as_dict = True)
#         frappe.db.commit() 
		