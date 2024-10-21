import mysql.connector

cnx = mysql.connector.connect(
	host="localhost",
	user="root",
	database="SchoolRoutine",
)

cur = cnx.cursor()

def create_tables():
	cur.execute("""
		CREATE TABLE IF NOT EXISTS ClassRoutine (
			class VARCHAR(100) NOT NULL PRIMARY KEY,
			maximum INT DEFAULT(2),
			periods INT DEFAULT(4)
		);
	""")

	cur.execute(f"""
		CREATE TABLE IF NOT EXISTS Period (
			day VARCHAR(100) NOT NULL,
			period INT NOT NULL,
			class VARCHAR(100) NOT NULL REFERENCES ClassRoutine,
			teacher VARCHAR(100) NOT NULL,
			PRIMARY KEY(day, period, class)
		);
	""")

def close_db():
	cur.close()
	cnx.close()

def create_routine(class_name, maximum):
	cur.execute(f"""
		INSERT INTO ClassRoutine(class, maximum)
		VALUES ("{class_name}", {maximum});
	""")
	cnx.commit()

def create_period(day, period, class_name, teacher):
	cur.execute(f"""
		INSERT INTO Period(day, period, class, teacher)
		VALUES ("{day}", {period}, "{class_name}", "{teacher}");
	""")
	cnx.commit()
