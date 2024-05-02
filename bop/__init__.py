from __future__ import unicode_literals
import frappe
from frappe.utils import now, get_first_day, get_last_day, nowdate
from datetime import datetime, timedelta

__version__ = '0.0.1'


@frappe.whitelist()
def update_daily_markup():
	loan_records = frappe.db.get_list('Loan',
	filters={
		'docstatus': 1
	},
	fields=['name','loan_application','mark_up_rate','remaining_principal_amount']
	)

	# Get current date
	current_date = now()

	# Get current month's start and end dates
	current_month_start_date = get_first_day(current_date)
	current_month_end_date = get_last_day(current_date)

	# Get current month name
	current_month_name = current_month_start_date.strftime('%B')

	# Get today date
	current_datetime = datetime.now()
	one_day = timedelta(days=1)
	new_datetime = current_datetime + one_day

	# print(f"Current Month: {current_month_name}")
	# print(f"Current Month Start Date: {current_month_start_date}")
	# print(f"Current Month End Date: {current_month_end_date}")
	# print(f"Today's Date: {current_date}")
	# print(f"Today's Date: {new_datetime}")
	# print(f"loan records: {loan_records}")

	for i in loan_records:
		if frappe.db.exists("Markup Amount On Daily Basis", {"against_loan": i.name, "month": current_month_name}):
			day_markup_amount = i.remaining_principal_amount * (i.mark_up_rate/100) / 365
			#print(f"day_markup: {day_markup_amount} {i.remaining_principal_amount} {i.mark_up_rate}")

			# Fetch the document using Frappe's get_doc function
			day_mk_doc = frappe.get_doc("Markup Amount On Daily Basis", {"against_loan": i.name, "month": current_month_name})
			mr_child = frappe.new_doc("Daily Basis Markup Item")
			mr_child.date = new_datetime
			mr_child.markup_rate = i.mark_up_rate
			mr_child.remaining_principal_amount = i.remaining_principal_amount
			mr_child.day_markup_amt = day_markup_amount
			day_mk_doc.append("day_wise_markup_details", mr_child)
			day_mk_doc.save(ignore_permissions=True)
			#print(f"recods: {day_mk_doc}")
		else:
			day_markup_amount = i.remaining_principal_amount * (i.mark_up_rate/100) / 365
			daily_markup_doc = frappe.get_doc({
							"doctype": "Markup Amount On Daily Basis",
							"against_loan": i.name,
							"loan_application": i.loan_application,
							"posting_date": current_date,
							"month": current_month_name,
							"month_start_date": current_month_start_date,
							"month_end_date": current_month_end_date
						})
			daily_markup_doc.save(ignore_permissions=True)
			if daily_markup_doc.name:
				mr_child = frappe.new_doc("Daily Basis Markup Item")
				mr_child.date = new_datetime
				mr_child.markup_rate = i.mark_up_rate
				mr_child.remaining_principal_amount = i.remaining_principal_amount
				mr_child.day_markup_amt = day_markup_amount
				daily_markup_doc.append("day_wise_markup_details", mr_child)
				daily_markup_doc.save(ignore_permissions=True)	


@frappe.whitelist()
def fetch_deduction_details(deduction_type):
    deduction_doc = frappe.get_doc('Deduction Type', deduction_type)
    return {
        'principal_amount': deduction_doc.principal,
        'markup_amount': deduction_doc.markup
    }
