import frappe

def process_attendance_log():

	attendance_logs = frappe.db.sql(
		"""
		SELECT 
			*
		FROM
			bio_attendance_log b
		WHERE is_processed is null or is_processed = 'N'
		ORDER by employee_id, punch_date, punch_time
		LIMIT 1000
	""", as_dict=True)

	for log in attendance_logs:

		try:
			employee = frappe.db.exists("Employee", {"attendance_device_id": log.employee_id})

			if not employee:
				sql = f"UPDATE bio_attendance_log set is_processed = 'E', message = 'Employee ID Does not exists' where name = '{log.name}'"
				frappe.db.sql(sql)
			else:
				log_type = ""
				time = f"{log.punch_date_time}"

				if log.punch_direction == "Check In":
					log_type = "IN"
				else:
					log_type = "OUT"

				# if log.punch_direction == "Check In":
				# 	log_type = "OUT"

				checkin = frappe.get_doc({
					"doctype": "Employee Checkin",
					"employee": employee,
					"log_type": log_type,
					"time": time,
					"device_id": log.terminal_id,
					"custom_bio_log_id": log.name
				})

				checkin.save()
				print(checkin.name)
				sql = f"UPDATE bio_attendance_log set is_processed = 'Y', message = '{checkin.name}' where name = '{log.name}'"
				frappe.db.sql(sql)

		except Exception as e:
			frappe.log_error('bio_attendance_exception')
			sql = f"UPDATE bio_attendance_log set is_processed = 'E', message = '{str(e)}' where name = '{log.name}'"
			frappe.db.sql(sql)


@frappe.whitelist()
def reset_attendance_log(bio_id):
	frappe.db.sql(
		f"""
		UPDATE
			bio_attendance_log
			set is_processed = 'N', message = null
		WHERE 
			name = '{bio_id}'
	""", as_dict=True)

	bio = frappe.db.sql("SELECT * from bio_attendance_log where name = %s", bio_id)
	if bio:
		check_ins = frappe.db.get_all("Employee Checkin", filters={"custom_bio_log_id":  bio_id})
		for check_in in check_ins:
			frappe.delete_doc("Employee Checkin", check_in.get("name"))

	frappe.db.commit()
