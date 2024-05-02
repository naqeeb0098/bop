// Copyright (c) 2024, Pukat Digital and contributors
// For license information, please see license.txt

frappe.ui.form.on('Provident Fund Investment', {
	before_submit: function (frm){
		if (frm.doc.amount_invested && frm.doc.pf_balance) {
			if (frm.doc.amount_invested > frm.doc.pf_balance) {
				frappe.throw("Invested Amount should not be greater than PF Balance");
				return;
			}
		} 
	},
	on_submit : function(frm) {     
		frappe.call({
			doc : frm.doc,
			method: "validate_and_add_deatils_to_provident_fund",
			// args: {
			// 	doc_name: frm.doc.name
			// },
			callback: function(r) {
			  if (r.message && r.message.error) {
				  frappe.msgprint(r.message.error);
				  frappe.validated = false;
			  }
		  }
		});
	},
	before_cancel : function (frm){
		frappe.call({
			doc: frm.doc,
			method: "validater"
		})
	}
});
