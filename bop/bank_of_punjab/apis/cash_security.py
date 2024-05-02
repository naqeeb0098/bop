import frappe
from frappe import utils
from datetime import datetime, timedelta
import traceback

@frappe.whitelist(allow_guest=True)
def calculate_daily_markup_for_cash_security():
    error_logs = []

    try:
        cash_security_records = frappe.get_all("Cash Security", filters={"docstatus": 1}, fields=["name", "employee", "security_amount", "profit_rate", "cs_balance"])

        for cash_security in cash_security_records:
            try:
                employee_record = frappe.get_doc("Employee", cash_security.employee)
                if employee_record.status == "Active":
                    security_amount = cash_security.security_amount
                    profit_rate = cash_security.profit_rate
                    daily_markup_for_cash_security = (security_amount * profit_rate / 100) / 365
                    existing_markup_amount = cash_security.cs_balance or 0
                    total_markup_amount = existing_markup_amount + daily_markup_for_cash_security
                    frappe.db.set_value("Cash Security", cash_security.name, "cs_balance", total_markup_amount)
                    frappe.db.commit()
                else:
                    error_logs.append(f"Employee {cash_security.employee} associated with Cash Security {cash_security.name} is not active.")
            except Exception as e:
                error_logs.append(f"Error processing Cash Security {cash_security.name}: {str(e)}\n{traceback.format_exc()}")

        return "Daily markup for cash security updated successfully!" if not error_logs else "\n".join(error_logs)
    except Exception as ex:
        error_logs.append(f"Exception occurred: {str(ex)}\n{traceback.format_exc()}")
        return f"An unexpected error occurred: {str(ex)}\n{traceback.format_exc()}"


