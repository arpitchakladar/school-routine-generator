import mysql.connector as msc
from utils import *
from table import *


# Establishing connection to the database
_db_connection = msc.connect(
	host="localhost",
	user="root",
	database="SchoolRoutine",
)
_db_cursor = _db_connection.cursor()


def get_routine_table_name(class_name):
	return f"Routine_{class_name.upper().replace(" ", "_")}"


def _create_routine_table(class_name):
	try:
		table_name = get_routine_table_name(class_name)
		_db_cursor.execute(f"""
			CREATE TABLE {table_name} (
				{" VARCHAR(100) NOT NULL, ".join(week_days)} VARCHAR(100) NOT NULL,
				PRIMARY KEY ({", ".join(week_days)})
			);
		""")
		return True
	except msc.Error as error:
		if error.errno == msc.errorcode.ER_TABLE_EXISTS_ERROR:
			return False


def close_database():
	_db_cursor.close()
	_db_connection.close()


def delete_class_routine(class_name):
	try:
		table_name = get_routine_table_name(class_name)
		_db_cursor.execute(f"DROP TABLE {table_name};")
		return True

	except msc.Error as error:
		if error.errno == msc.errorcode.ER_BAD_TABLE_ERROR:
			return False


def insert_class_routine(class_name, routine):
	if not _create_routine_table(class_name):
		return False

	table_name = get_routine_table_name(class_name)
	for row_index in range(len(routine[0])):
		routine_row = f'"{routine[0][row_index]}"'
		for day_index in range(1, len(week_days)):
			routine_row += f', "{routine[day_index][row_index]}"'
		_db_cursor.execute(f"""
			INSERT INTO {table_name} (
				{", ".join(week_days)}
			) VALUES ({routine_row});
		""")
	_db_connection.commit()
	return True


def get_class_names():
	_db_cursor.execute("SHOW TABLES;")
	class_names = []
	for table in _db_cursor.fetchall():
		class_names.append(table[0][8:].replace("_", " "))
	return class_names


def get_routine(class_name):
	try:
		_db_cursor.execute(f"""
			SELECT {", ".join(week_days)}
			FROM {get_routine_table_name(class_name)};
		""")
		return _db_cursor.fetchall()

	except msc.Error as error:
		if error.errno == msc.errorcode.ER_NO_SUCH_TABLE:
			return False
