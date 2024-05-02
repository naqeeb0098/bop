// Copyright (c) 2024, Pukat Digital and contributors
// For license information, please see license.txt

frappe.ui.form.on('Provident Fund', {
	investment_amount: function(frm) {
		frm.set_value('pf_balance', frm.doc.investment_amount);
	  },
});
