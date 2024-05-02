// Copyright (c) 2024, Pukat Digital and contributors
// For license information, please see license.txt

frappe.ui.form.on('BOP Loan Disbursement', {
    
    on_submit: function(frm) {
        frappe.call({
			doc : frm.doc,
            method: "update_loan_status"
        });
    }
});
