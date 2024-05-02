# Copyright (c) 2024, Pukat Digital and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BOPLoanRepayment(Document):
	@frappe.whitelist()
	def update_bop_loan(name, amount_paid):
		loan = frappe.get_doc("BOP Loan", name.against_loan)
		amount = loan.principal_balance + loan.balance_markup_amount
		if float(amount_paid) > float(amount):
			frappe.throw("Amount_paid is grater than sum of principal balance and marup balance")
		else:
			markup_percentage_amount = amount_paid * (loan.markup / 100)
			principal_percentage_amount = amount_paid * (loan.principal / 100)
				
			deducted_principal_amount = min(principal_percentage_amount, loan.principal_balance)
			deducted_markup_amount = min(markup_percentage_amount, loan.balance_markup_amount)

			if 0 < loan.principal_balance < principal_percentage_amount:
				deducted_principal_amount = loan.principal_balance
			else:
				remaining_markup_deduction = markup_percentage_amount - deducted_markup_amount
				deducted_principal_amount += max(min(remaining_markup_deduction, loan.principal_balance), 0)

			if 0 < loan.balance_markup_amount < markup_percentage_amount:
				deducted_markup_amount = loan.balance_markup_amount
			else:
				remaining_principal_deduction = principal_percentage_amount - deducted_principal_amount
				deducted_markup_amount += max(min(remaining_principal_deduction, loan.balance_markup_amount), 0)

			blnc_principal = loan.principal_balance - deducted_principal_amount
			blnc_markup = loan.balance_markup_amount - deducted_markup_amount
			paid_princiapl = loan.total_principal_amount - blnc_principal
			paid_markup = loan.total_markup_amount - blnc_markup
   
			name.deducted_amount_from_principal = deducted_principal_amount
			name.deducted_amount_from_markup = deducted_markup_amount
			name.principal_balance = blnc_principal
			name.total_principal_paid = paid_princiapl
			name.balance_markup_amount = blnc_markup
			name.total_markup_paid = paid_markup	
			frappe.db.sql(f"""UPDATE `tabBOP Loan` SET total_principal_paid = {paid_princiapl}, principal_balance = {blnc_principal}, balance_markup_amount = {blnc_markup}, total_markup_paid = {paid_markup}""",as_dict=True)
			frappe.db.commit()
			return "BOP Loan updated successfully."
	@frappe.whitelist()
	def revert_bop_loan_update(name):
		loan = frappe.get_doc("BOP Loan", name.against_loan)
		name.deducted_amount_from_principal 
		name.deducted_amount_from_markup 
		blnc_principal = loan.principal_balance + name.deducted_amount_from_principal
		blnc_markup = loan.balance_markup_amount + name.deducted_amount_from_markup
		paid_princiapl = loan.total_principal_amount - blnc_principal
		paid_markup = loan.total_markup_amount - blnc_markup
		frappe.db.sql(f"""UPDATE `tabBOP Loan` SET total_principal_paid = {paid_princiapl}, principal_balance = {blnc_principal}, balance_markup_amount = {blnc_markup}, total_markup_paid = {paid_markup}""",as_dict=True)
		frappe.db.commit()
		return "BOP Loan updated successfully."
