import traceback
import frappe

@frappe.whitelist(allow_guest=True)
def calculate_daily_provident_fund():
    error_logs = []
    try:
        pf_record = frappe.get_all("Provident Fund", filters={"docstatus": 1}, fields=["name", "pf_balance", "rate_of_int", "investment_amount"])
        for record in pf_record:
            try:
                pf_balance = record.pf_balance
                rate_of_int = record.rate_of_int
                daily_pf_markup = (pf_balance * rate_of_int / 100) / 365
                pf_balance = record.pf_balance or 0
                total_markup_amount = pf_balance + daily_pf_markup
                frappe.db.set_value("Provident Fund", record.name, "pf_balance", total_markup_amount)
                frappe.db.commit()
            except Exception as e:
                error_logs.append(f"Error processing Cash Security {record.name}: {str(e)}\n{traceback.format_exc()}")
        return "Daily markup for provident fund updated successfully!" if not error_logs else "\n".join(error_logs)
    except Exception as ex:
        error_logs.append(f"Exception occurred: {str(ex)}\n{traceback.format_exc()}")
        return f"An unexpected error occurred: {str(ex)}\n{traceback.format_exc()}"
    
#======================update pf balance in provident fun on the basisis of graduatiy or pension==============
@frappe.whitelist(allow_guest=True)
def provident_fund_balance_updation_on_basis_of_salary_slip(doc_name):
    try:
        salary_slip = frappe.get_doc("Salary Slip", doc_name)
        total_pf_deduction = 0
        for component in salary_slip.get("deductions"):
            if component.salary_component == "P.F. @ 10% of Current B.Pay (Gratuity)":
                total_pf_deduction += 2 * component.amount
            elif component.salary_component == "P.F. @ 10% of Current B.Pay (Pension)":
                total_pf_deduction += component.amount

        pf_record = frappe.get_doc("Provident Fund", {"employee": salary_slip.employee})
        name = pf_record.name
        pf_balance = pf_record.pf_balance + total_pf_deduction
        frappe.db.sql(f"""update `tabProvident Fund` SET pf_balance = '{pf_balance}' where name = '{name}'""")
        frappe.db.commit()
        return {"success": True}  # Indicate success to the client-side script
    except Exception as e:
        frappe.log_error(f"Error updating Provident Fund balance: {e}")
        return {"error": "An error occurred while updating Provident Fund balance. Please try again later."}
#======================update pf balance in provident fun on the basisis of graduatiy or pension on cancel ==============
@frappe.whitelist(allow_guest=True)
def provident_fund_balance_updation_on_basis_of_salary_slip_cancel(doc_name):
    try:
        salary_slip = frappe.get_doc("Salary Slip", doc_name)
        total_pf_deduction = 0
        for component in salary_slip.get("deductions"):
            if component.salary_component == "P.F. @ 10% of Current B.Pay (Gratuity)":
                total_pf_deduction += 2 * component.amount
            elif component.salary_component == "P.F. @ 10% of Current B.Pay (Pension)":
                total_pf_deduction += component.amount

        pf_record = frappe.get_doc("Provident Fund", {"employee": salary_slip.employee})
        name = pf_record.name
        pf_balance = pf_record.pf_balance - total_pf_deduction
        frappe.db.sql(f"""update `tabProvident Fund` SET pf_balance = '{pf_balance}' where name = '{name}'""")
        frappe.db.commit()
        return {"success": True}  # Indicate success to the client-side script
    except Exception as e:
        frappe.log_error(f"Error updating Provident Fund balance: {e}")
        return {"error": "An error occurred while updating Provident Fund balance. Please try again later."}



