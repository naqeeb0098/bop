// Copyright (c) 2024, Pukat Digital and contributors
// For license information, please see license.txt

frappe.ui.form.on('BOP Loan Disbursement', {
    on_submit: function(frm) {
        frm.call({
            method: "update_loan_status",
            doc: frm.doc
        });
    },
    before_cancel: function(frm) {
        frm.call({
            method: "reverse_loan_status",
            doc: frm.doc
        });
    },
    onload: function(frm) {
        frm.set_query('against_loan', function() {
            return {
                filters: {
                    'status': 'Sanctioned'
                }
            };
        });
    },
    refresh: function(frm) {
        frm.trigger('onload');  // Apply the filter when the form is refreshed
    }
});