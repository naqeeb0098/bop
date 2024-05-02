// Copyright (c) 2024, Pukat Digital and contributors
// For license information, please see license.txt

frappe.ui.form.on('BOP Loan Repayment', {
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
});
