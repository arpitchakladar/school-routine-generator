import mysql.connector
from const import week_days
from table import display_table

cnx = mysql.connector.connect(
	host="localhost",
	user="root",
	database="SchoolRoutine",
)

cur = cnx.cursor()

def create_table(class_name):
	cur.execute(f"""
		CREATE TABLE IF NOT EXISTS Routine{class_name} (
			{" VARCHAR(100) NOT NULL, ".join(week_days)} VARCHAR(100) NOT NULL,
			PRIMARY KEY ({", ".join(week_days)})
		);
	""")

def close_db():
	cur.close()
	cnx.close()

def create_routine(class_name, routine):
	create_table(class_name)
	for i in range(len(routine[0])):
		s = f"\"{routine[0][i]}\""
		for j in range(1, len(week_days)):
			s += f", \"{routine[j][i]}\""
		cur.execute(f"""
			INSERT INTO Routine{class_name} (
				{", ".join(week_days)}
			) VALUES ({s});
		""");
	cnx.commit()

# Format of subjects is (subject name, number of classes in a week)
def display_routine(class_name):
	cur.execute(f"""
		SELECT {", ".join(week_days)}
		FROM Routine{class_name};
	""");
	l = cur.fetchall()
	x = []
	for i in range(len(l[0])):
		k = []
		for j in range(len(l)):
			l.append(l[j][i])
		x.append(k)

	print(x)

	for i in range(len(week_days)):
		x[i] = [week_days[i]] + x[i]
	headings = ["Days"]
	for i in range(1, periods + 1):
		headings.append("Period " + str(i))
	display_table(headings, x)
