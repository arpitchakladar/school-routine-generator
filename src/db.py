import mysql.connector

from utils import *
from table import *

cnx = mysql.connector.connect(
	host="localhost",
	user="root",
	database="SchoolRoutine",
)

cur = cnx.cursor()

def _get_class_name_routine_table(class_name):
	return f"Routine{class_name.upper()}"

def create_table(class_name):
	cur.execute(f"""
		CREATE TABLE IF NOT EXISTS {_get_class_name_routine_table(class_name)} (
			{" VARCHAR(100) NOT NULL, ".join(week_days)} VARCHAR(100) NOT NULL,
			PRIMARY KEY ({", ".join(week_days)})
		);
	""")

def close_db():
	cur.close()
	cnx.close()

def delete_routine(class_name):
	cur.execute(f"""
		DROP TABLE {_get_class_name_routine_table(class_name)};
	""");

def create_routine(class_name, routine):
	create_table(class_name)
	for i in range(len(routine[0])):
		s = f"\"{routine[0][i]}\""
		for j in range(1, len(week_days)):
			s += f", \"{routine[j][i]}\""

		cur.execute(f"""
			INSERT INTO {_get_class_name_routine_table(class_name)} (
				{", ".join(week_days)}
			) VALUES ({s});
		""");

	cnx.commit()

# Format of subjects is (subject name, number of classes in a week)
def display_routine(class_name):
	cur.execute(f"""
		SELECT {", ".join(week_days)}
		FROM {_get_class_name_routine_table(class_name)};
	""");
	l = list(cur.fetchall())
	x = []

	for i in range(len(l[0])):
		k = []
		for j in range(len(l)):
			k.append(l[j][i])
		x.append(k)

	periods = len(l)
	for i in range(len(week_days)):
		x[i] = [week_days[i]] + x[i]
	headings = ["Days"]

	for i in range(1, periods + 1):
		headings.append(f"Period {i}")

	display_table(headings, x)

def list_classes():
	cur.execute("SHOW TABLES;");

	l = []
	for e in cur.fetchall():
		l.append((e[0][7:],))

	display_table(["Classes"], l)
