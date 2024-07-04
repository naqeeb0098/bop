import frappe
from frappe import utils
from datetime import datetime, timedelta

def insert_single_additional_salary(row, parent_name, date):
    try:
        amount = float(row.get("deducted_principal_amount")) + float(row.get("deducted_markup_amount"))
        additional_salary = frappe.new_doc("Additional Salary")
        additional_salary.update({
            "employee": row.get("employee_id"),
            "employee_name": row.get("employee_name"),
            "company": "PPCBL",
            "payroll_date": date,
            "salary_component": row.get("loan_type"),
            "type": "Deduction",
            "amount": amount,
            "reason": "BOP Loan Deduction",
            "against_bop_loan_deduction": parent_name
        })
        additional_salary.insert(ignore_permissions=True)
        additional_salary.submit()
        frappe.db.commit()
    except Exception as e:
        error_message = f"Error in inserting additional salary for employee {row.get('employee_id')} on {date}: {str(e)}"
        frappe.log_error(message=error_message, title="Error in inserting additional salary")
        
def insert_additional_salary(parent_name):
    custom_date = frappe.get_doc("BOP Loan Deduction", parent_name)
    date = custom_date.get("custom_date")
    data = frappe.db.sql(f"""SELECT * FROM `tabBOP Loan Details` WHERE parent = '{parent_name}'""", as_dict=True)
    for row in data:
        frappe.enqueue('bop.bank_of_punjab.apis.loan.insert_single_additional_salary',
                       queue="long", row=row, parent_name=parent_name, date=date)
    return "All records have been queued for insertion."

@frappe.whitelist(allow_guest=True)
def additional_salery(parent_name):
    frappe.enqueue('bop.bank_of_punjab.apis.loan.insert_additional_salary', queue="long", parent_name=parent_name)
    return "Job queued for inserting data successfully."
# ===================================================================================================================

@frappe.whitelist(allow_guest=True)
def delete_additional_salaries(parent_name):
    frappe.db.sql(f"""DELETE FROM `tabAdditional Salary` WHERE against_bop_loan_deduction = '{parent_name}'""")
    frappe.db.commit()
    return "Additional salaries also deleted"

# ============================jobs for markup claucuulation Start==============================================

# @frappe.whitelist(allow_guest=True)
# def calculate_daily_markup():
#     bop_loans = frappe.get_all("BOP Loan", filters={"docstatus": 1, "status": "Disbursed"})
#     for loan in bop_loans:
#         loan_doc = frappe.get_doc("BOP Loan", loan.name)
#         daily_markup_amount = loan_doc.principal_balance * (loan_doc.markup_rate / 100) / 365
#         existing_total_markup_amount = frappe.db.get_value("BOP Loan", loan.name, "total_markup_amount")
#         if existing_total_markup_amount is None:
#             existing_total_markup_amount = 0
#         total_markup_amount = existing_total_markup_amount + daily_markup_amount
#         markup_paid = loan.total_markup_paid
#         if markup_paid is None:
#             markup_paid = 0
#             balance_markup = total_markup_amount + loan_doc.opening_balance - markup_paid
#         frappe.db.set_value("BOP Loan", loan.name, {"total_markup_amount":total_markup_amount,"balance_markup_amount":balance_markup})
#         frappe.db.commit()
        
#     return "Daily markup calculated and updated successfully!"

# ============================calaculate markup for specific timeperiod=================
from datetime import datetime, time

@frappe.whitelist(allow_guest=True)
def calculate_daily_markup_for_loans(loan_ids=None, from_date=None, to_date=None):
    if not loan_ids:
        return "Please provide the list of loan IDs."
    if not from_date or not to_date:
        return "Please provide both from date and to date."

    # Convert date strings to datetime objects
    from_date = datetime.combine(datetime.strptime(from_date, "%Y-%m-%d"), time.min)
    to_date = datetime.combine(datetime.strptime(to_date, "%Y-%m-%d"), time.max)
    
    num_days = (to_date - from_date).days + 1

    for loan_id in loan_ids:
        loan_doc = frappe.get_doc("BOP Loan", loan_id)
        if loan_doc.docstatus != 1 or loan_doc.status != "Disbursed" or not loan_doc.disbursement_date:
            continue
        daily_markup_amount = loan_doc.principal_balance * (loan_doc.markup_rate / 100) / 366
        existing_total_markup_amount = frappe.db.get_value("BOP Loan", loan_id, "total_markup_amount") or 0
        total_markup_amount = existing_total_markup_amount + daily_markup_amount * num_days
        markup_paid = loan_doc.total_markup_paid or 0
        balance_markup = total_markup_amount + loan_doc.opening_balance - markup_paid

        # Update loan document fields
        frappe.db.set_value("BOP Loan", loan_id, {
            "total_markup_amount": total_markup_amount,
            "balance_markup_amount": balance_markup
        })
        frappe.db.commit()

    return "Daily markup calculated and updated successfully!"



# ============================jobs for markup claucuulation end==============================================





# @frappe.whitelist(allow_guest=True)
# def calculate_daily_markup():
#     today = datetime.now().date()
#     bop_loans = frappe.get_all("BOP Loan", filters={"docstatus": 1, "status": "Disbursed"})
#     for loan in bop_loans:
#         loan_doc = frappe.get_doc("BOP Loan", loan.name)
#         disbursement_date = loan_doc.disbursement_date
#         days_since_disbursement = ((today - disbursement_date).days + 1)
        
#         if days_since_disbursement <= 0:
#             continue  
        
#         daily_markup_rate = loan_doc.markup_rate / 100 / 365
#         daily_markup_amount = loan_doc.principal_balance * daily_markup_rate
        
#         existing_total_markup_amount = frappe.db.get_value("BOP Loan", loan.name, "total_markup_amount")
#         if existing_total_markup_amount is None:
#             existing_total_markup_amount = 0
        
#         total_markup_amount = daily_markup_amount * days_since_disbursement
        
#         markup_paid = loan_doc.total_markup_paid or 0
#         balance_markup = total_markup_amount - markup_paid
        
#         frappe.db.set_value("BOP Loan", loan.name, {"total_markup_amount": total_markup_amount, "balance_markup_amount": balance_markup})
#         frappe.db.commit()
        
#     return "Daily markup calculated and updated successfully!"


@frappe.whitelist(allow_guest=True)
def update_balances_in_bop_loan():
    data = frappe.db.sql("""
        SELECT 
            loan_id,
            SUM(deducted_principal_amount) AS total_deducted_principal_amount,
            SUM(deducted_markup_amount) AS total_deducted_markup_amount
        FROM 
            `tabBOP Loan Details`
        GROUP BY 
            loan_id;
    """, as_dict=True)
    
    for entry in data:
        loan_id = entry.get("loan_id")
        total_deducted_principal = entry.get("total_deducted_principal_amount", 0)
        total_deducted_markup = entry.get("total_deducted_markup_amount", 0)
        
        values = {
            "total_principal_paid": total_deducted_principal,
            "total_markup_paid": total_deducted_markup
        }
        frappe.db.set_value("BOP Loan", loan_id, values)
    
    bop_loans = frappe.get_all("BOP Loan",filters={"docstatus": 1})
    for loan in bop_loans:
        loan_doc = frappe.get_doc("BOP Loan", loan.name)
        balance_amount = loan_doc.total_principal_amount - loan_doc.total_principal_paid
        total_markup_amount = loan_doc.total_markup_amount + loan_doc.opening_balance - loan_doc.total_markup_paid
        values = {
            "principal_balance": balance_amount,
            "balance_markup_amount": total_markup_amount
        }   
        frappe.db.set_value("BOP Loan", loan.name, values)
        frappe.db.commit()
    
    frappe.db.commit()

    return "Balances adjusted successfully"

@frappe.whitelist(allow_guest=True)
def update_balances_in_bop_loan_after_cancelation(parent_name):
    data = frappe.db.sql(f"""
        SELECT 
            loan_id,
            SUM(deducted_principal_amount) AS total_deducted_principal_amount,
            SUM(deducted_markup_amount) AS total_deducted_markup_amount
        FROM 
            `tabBOP Loan Details`
        WHERE 
            parent != '{parent_name}'
        GROUP BY 
            loan_id;
    """, as_dict=True)
    
    for entry in data:
        loan_id = entry.get("loan_id")
        total_deducted_principal = entry.get("total_deducted_principal_amount", 0)
        total_deducted_markup = entry.get("total_deducted_markup_amount", 0)
        
        values = {
            "total_principal_paid": total_deducted_principal,
            "total_markup_paid": total_deducted_markup
        }
        frappe.db.set_value("BOP Loan", loan_id, values)
    
    bop_loans = frappe.get_all("BOP Loan",filters={"docstatus": 1})
    for loan in bop_loans:
        loan_doc = frappe.get_doc("BOP Loan", loan.name)
        balance_amount = loan_doc.total_principal_amount - loan_doc.total_principal_paid
        total_markup_amount = loan_doc.total_markup_amount + loan_doc.opening_balance - loan_doc.total_markup_paid
        values = {
            "principal_balance": balance_amount,
            "balance_markup_amount": total_markup_amount
        }   
        frappe.db.set_value("BOP Loan", loan.name, values)
        frappe.db.commit()
    
    frappe.db.commit()

    return "Balances adjusted successfully"


