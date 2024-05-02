# Copyright (c) 2024, Pukat Digital and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProvidentFundInvestment(Document):
	@frappe.whitelist()
	def validate_and_add_deatils_to_provident_fund(doc, method):
		if doc.type == "ADD":
			pf_balance = doc.pf_balance + doc.amount_invested
		if doc.type == "SUBTRACT":
			pf_balance = doc.pf_balance - doc.amount_invested
		if pf_balance < 0:
			frappe.throw(f"""PF_blance {pf_balance} is lesser than zero """)
		else:	
			doc.db_set('pf_balance', pf_balance)
			frappe.db.set_value("Provident Fund", doc.against_provident_fund, "pf_balance",pf_balance)
			child_table = frappe.get_doc("Provident Fund", doc.against_provident_fund)
			child_row = child_table.append("investments", {})
			child_row.remarks = doc.remarks
			child_row.invested_amount = doc.amount_invested
			child_row.pf_investment = doc.name
			child_table.save()
			frappe.db.commit()
   
	@frappe.whitelist(allow_guest=True)
	def validater(doc,method):
		if doc.type == "ADD":
			pf_balance = doc.pf_balance - doc.amount_invested
		if doc.type == "SUBTRACT":
			pf_balance = doc.pf_balance + doc.amount_invested
		if pf_balance < 0:
			frappe.throw(f"""PF_blance {pf_balance} is lesser than zero """)
		else:	
			doc.db_set('pf_balance', pf_balance)
			frappe.db.set_value("Provident Fund", doc.against_provident_fund, "pf_balance",pf_balance)
			doc_name = doc.name
			frappe.db.sql(f"DELETE FROM `tabPF Investment Details` WHERE pf_investment ='{doc_name}'")
			frappe.db.commit()