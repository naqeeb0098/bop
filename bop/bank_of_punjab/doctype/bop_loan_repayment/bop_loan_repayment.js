// Copyright (c) 2024, Pukat Digital and contributors
// For license information, please see license.txt

frappe.ui.form.on('BOP Loan Repayment', {
    // validate: function(frm) {
    //     // Round amount_paid and total_balance_amount to two decimal places
    //     let amount_paid = parseFloat(frm.doc.amount_paid).toFixed(2);
    //     let total_balance_amount = parseFloat(frm.doc.total_balance_amount).toFixed(2);

    //     // Check if amount_paid is greater than total_balance_amount
    //     if (amount_paid > total_balance_amount) {
    //         frappe.msgprint(__('Amount paid is greater than total balance amount'));
    //         frappe.validated = false;  // Prevent form submission
    //     }
    // },

	before_submit : function (frm){
		frappe.call({
			doc : frm.doc,
            method: "update_bop_loan",
			args: {
                name: frm.doc.against_laon,
                amount_paid: frm.doc.amount_paid
            }
        });

	},
	before_cancel: function (frm){
		frappe.call({
			doc : frm.doc,
            method: "revert_bop_loan_update",
			args: {
                name: frm.doc.against_laon
            }
        });

	},
	onload: function(frm) {
            calculate_total_balance(frm);
        },
        principal_balance: function(frm) {
            calculate_total_balance(frm);
        },
        balance_markup_amount: function(frm) {
            calculate_total_balance(frm);
        }
});

	function calculate_total_balance(frm) {
    		// Get the values of the two fields
	    let principal_balance = frm.doc.principal_balance || 0;
	    let balance_markup_amount = frm.doc.balance_markup_amount || 0;
	    let total_balance = principal_balance + balance_markup_amount;
   	 frm.set_value('total_balance_amount', total_balance);
}
