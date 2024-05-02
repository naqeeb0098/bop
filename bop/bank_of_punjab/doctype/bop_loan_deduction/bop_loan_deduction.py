# Copyright (c) 2024, Pukat Digital and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document

# class BOPLoanDeduction(Document):
# 	pass

import frappe
from frappe import utils
from frappe.model.document import Document
class BOPLoanDeduction(Document): 
	@frappe.whitelist()
	def insert_records_into_child_table(doc,date,loan_type = None):
		filters = {
			"docstatus": 1,
			"status": "Disbursed",
			"disbursement_date": ["<=", date]
		}

		if loan_type:
			filters["loan_type"] = loan_type
		date = frappe.form_dict.get('date')	
		parent_doc = frappe.get_doc(doc)
		bop_loans = frappe.get_all("BOP Loan", filters=filters, fields=["*"])
		# bop_loans = frappe.get_all("BOP Loan", filters={"docstatus": 1, "status": "Disbursed","disbursement_date": ["<=", date]}, fields=["*"])	
		if not bop_loans:
			frappe.msgprint(f"Record not Found !")
		for loan in bop_loans:
			if loan.principal_balance <= 0 and loan.balance_markup_amount <= 0:
				frappe.db.set_value("BOP Loan", loan.name, "status", "Closed")
				frappe.db.commit()

			elif loan.markup == 0: 
				principal_percentage_amount = loan.monthly_repayment_amount
				deducted_principal_amount = min(principal_percentage_amount, loan.principal_balance)

				if loan.monthly_repayment_amount > loan.principal_balance:
					deducted_markup_amount = min(loan.monthly_repayment_amount - deducted_principal_amount, loan.balance_markup_amount)
				else:
					deducted_markup_amount = 0

				loan_data = {
					"loan_id": loan.name,
					"loan_type": loan.loan_type,
					"employee_id": loan.employee_id,
					"employee_name": loan.employee_name,
					"branch": loan.custom_branch,
					"loan_amount": loan.loan_amount,
					"balance_principal_amt": loan.principal_balance,
					"markup_amount": loan.total_markup_amount,
					"markup_paid": loan.total_markup_paid,
					"balance_markup": loan.balance_markup_amount,
					"loan_installment": loan.monthly_repayment_amount,
					"principal_percentage": loan.principal,
					"markup_percentage": loan.markup,
					"deducted_principal_amount": deducted_principal_amount,
					"deducted_markup_amount": max(0, deducted_markup_amount)
				}
				parent_doc.append("loan_deduction_details", loan_data)

			else:
				markup_percentage_amount = loan.monthly_repayment_amount * (loan.markup / 100)
				principal_percentage_amount = loan.monthly_repayment_amount * (loan.principal / 100)
					
				deducted_principal_amount = min(principal_percentage_amount, loan.principal_balance)
				deducted_markup_amount = min(markup_percentage_amount, loan.balance_markup_amount)

				if loan.principal_balance > 0 and loan.principal_balance < principal_percentage_amount:
					deducted_principal_amount = loan.principal_balance
				else:
					remaining_markup_deduction = markup_percentage_amount - deducted_markup_amount
					deducted_principal_amount += max(min(remaining_markup_deduction, loan.principal_balance), 0)

				if loan.balance_markup_amount > 0 and loan.balance_markup_amount < markup_percentage_amount:
					deducted_markup_amount = loan.balance_markup_amount
				else:
					remaining_principal_deduction = principal_percentage_amount - deducted_principal_amount
					deducted_markup_amount += max(min(remaining_principal_deduction, loan.balance_markup_amount), 0)

				loan_data = {
					"loan_id": loan.name,
					"loan_type": loan.loan_type,
					"employee_id": loan.employee_id,
					"employee_name": loan.employee_name,
					"branch": loan.custom_branch,
					"loan_amount": loan.loan_amount,
					"balance_principal_amt": loan.principal_balance,
					"markup_amount": loan.total_markup_amount,
					"markup_paid": loan.total_markup_paid,
					"balance_markup": loan.balance_markup_amount,
					"loan_installment": loan.monthly_repayment_amount,
					"principal_percentage": loan.principal,
					"markup_percentage": loan.markup,
					"deducted_principal_amount": deducted_principal_amount,
					"deducted_markup_amount": max(0, deducted_markup_amount)
				}
				parent_doc.append("loan_deduction_details", loan_data)
    
    
    
	@frappe.whitelist()
	def additional_salery(doc,name):
		name = frappe.form_dict.get('name')		
		data = frappe.db.sql(f"""select * from `tabBOP Loan Details` where parent ='{name}'""", as_dict = True)
		return data