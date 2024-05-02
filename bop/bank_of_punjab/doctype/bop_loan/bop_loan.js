// Copyright (c) 2024, Pukat Digital and contributors
// For license information, please see license.txt

frappe.ui.form.on('BOP Loan', {
    loan_amount: function(frm) {
		frm.set_value('total_principal_amount', frm.doc.loan_amount);
		frm.set_value('principal_balance',frm.doc.loan_amount);
    },
    
    before_submit: function(frm) {
      
      frappe.call({
          doc : frm.doc,
          method: "check_salary_structure_assignment",
          args: {
              doc_name: frm.doc.name
          },
          callback: function(r) {
            if (r.message && r.message.error) {
                frappe.msgprint(r.message.error);
                frappe.validated = false; // Prevent submission
            }
        }
      });
  }
});
