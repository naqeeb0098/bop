// Copyright (c) 2024, Pukat Digital and contributors
// For license information, please see license.txt

frappe.ui.form.on('BOP Loan Deduction', {
    testing: function(frm) {
        // Check if the loan type field value has changed
        // if (frm.doc.__islocal || frm.doc.__unsaved || frm.doc.__unedited) {
        //     // If the document is new or unsaved, do nothing
        //     return;
        // }

        // Display a message indicating that the loan type has changed
        frappe.msgprint("Loan type has been changed: " + frm.doc.testing);
    },
	on_submit : function (frm) {
		frappe.call({
            method: "bop.bank_of_punjab.apis.loan.additional_salery",
			args: {
				parent_name : frm.doc.name
			}

		}),
			frappe.call({
			// doc : frm.doc,
			method : "bop.bank_of_punjab.apis.loan.update_balances_in_bop_loan"
		})
	},
	after_cancel: function (frm) {
        frappe.call({
            method: "bop.bank_of_punjab.apis.loan.delete_additional_salaries",
            args: {
                parent_name: frm.doc.name
            },
            callback: function (r) {
                if (r.message) {
                    frappe.msgprint(r.message);
                }
        }
        }),
		frappe.call({
            method: "bop.bank_of_punjab.apis.loan.update_balances_in_bop_loan_after_cancelation",
            args: {
                parent_name: frm.doc.name
            },
            // callback: function (r) {
            //     if (r.message) {
            //         frappe.msgprint(r.message);
            //     }
            // }
        })
    },
	date: function(frm) {
		frm.clear_table('loan_deduction_details');
        frm.refresh_field('loan_type');
		if (!frm.doc.date) {
            frappe.throw("Please select a date first.");
            return;
        }
        // console.log("Loan Type:", frm.doc.loan_type);
        frappe.call({
			doc : frm.doc,
            method: "insert_records_into_child_table",
			args: {
                date: frm.doc.date,
                loan_type: frm.doc.loan_type

            },
			callback: function(r) {
                frm.refresh_field('loan_deduction_details');
            }
        });
    },
    loan_type: function (frm) {
        frm.clear_table('loan_deduction_details');
        frappe.call({
			doc : frm.doc,
            method: "insert_records_into_child_table",
			args: {
                date: frm.doc.date,
                loan_type: frm.doc.loan_type
            },
			callback: function(r) {
                frm.refresh_field('loan_deduction_details');
            }
        });
    }
    
});
