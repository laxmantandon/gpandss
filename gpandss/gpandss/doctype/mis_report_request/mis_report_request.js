// Copyright (c) 2024, laxman and contributors
// For license information, please see license.txt

frappe.ui.form.on('MIS Report Request', {
	refresh(frm) {
		// abcd
		if (frm.is_new()) {
			
			let records = [
				"MIS Balance Sheet",
				"MIS Profit and Loss Statement",
				"MIS Trial Balance",
				"Indirect Cash Flow",
				"Cashflow Statement Projection Monthwise"
			]
			frm.clear_table("items")
			records.forEach(rec => {
				var row = cur_frm.fields_dict['items'].grid.add_new_row();
				frappe.model.set_value(row.doctype, row.name, "report_name", rec);
			});
		}
	 },

	onload: function(frm) {
        let tables = ["items"]
        tables.forEach(function(table) {
            if(frm.fields_dict[table]) {
                frm.get_field(table).grid.cannot_add_rows = true;
                frm.set_df_property(table, 'cannot_add_rows', true);
                frm.get_field(table).grid.refresh();
                frm.get_field(table).grid.cannot_delete_rows = true;
            }
        });
        
    },

});
