import frappe

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_active_batches(doctype, txt, searchfield, start, page_len, filters):

	item_group = frappe.db.get_single_value("SS Settings", "seed_item_group")
	# disabled = filters.get('disabled')
	values = { 'item_group': item_group, 'txt': '%'+txt+'%' }
	return frappe.db.sql("""
		SELECT 
			sle.batch_no,
			i.item_group,
			sle.item_code,
			SUM(sle.actual_qty) qty
		FROM `tabStock Ledger Entry` sle
		LEFT JOIN `tabItem` i ON sle.item_code = i.name
		WHERE
			i.item_group = %(item_group)s
			AND sle.docstatus = 1
			AND sle.is_cancelled=0
		GROUP BY sle.batch_no
		HAVING qty > 0
	""", values=values, as_dict=0)
