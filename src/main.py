from random import randint
from table import display_table
from db import create_tables, close_db, create_routine, create_period

week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

routine = [[]]
subject = []
max_classes = 0
periods = 0
days = len(week_days)

create_tables()

def generate_routine():
	used = {}
	for name, _, n in subjects:
		used[name] = n
		if n > max_classes * days:
			return False
	global routine
	routine = []

	for d in range(days):
		l = []
		if d == 4:
			for u in used.values():
				if u > max_classes:
					return generate_routine()

		for p in range(periods):
			sub = None
			while True:
				x = randint(0, len(subjects) - 1)
				sub = subjects[x]
				if used[sub[0]] > 0:
					c = 0
					for clas in l:
						p = clas.rfind("(")
						subject = clas[:p-1]
						if subject == sub[0]:
							c += 1
					if c < max_classes:
						break
			teachers = sub[1]
			teacher = teachers[randint(0, len(teachers) - 1)]
			l.append(sub[0] + " (" + teacher + ")")
			used[sub[0]] -= 1
		routine.append(l)
	return True

def substitution(day, teacher):
	for i in range(periods):
		clas = routine[day][i]
		x = clas.rfind("(")
		subject_teacher = clas[x + 1:-1]
		subject = clas[:x - 1]
		if teacher == subject_teacher:
			s = None
			for sub in subjects:
				if sub[0] == subject:
					s = sub
					break
			if len(s[1]) <= 1:
				j = 0
				k = 0
				while True:
					j = randint(0, days - 1)
					k = randint(0, periods - 1)
					new_subject = routine[j][k]
					y = new_subject.rfind("(")
					new_subject_name = new_subject[:y-1]
					if new_subject_name != subject and j != day:
						break
				routine[j][k], routine[day][i] = clas, routine[j][k]
			else:
				new_teacher = ""
				for t in s[1]:
					if t != teacher:
						new_teacher = t
						break
				routine[day][i] = subject + " (" + new_teacher + ")"

def swap_classes(day1, period1, day2, period2):
	try:
		d1 = week_days.index(day1.capitalize())
		d2 = week_days.index(day2.capitalize())
		routine[d1][period1], routine[d2][period2] = routine[d2][period2], routine[d1][period1]
	except ValueError:
		pass

def change_class(day, period, subject, teacher):
	try:
		d = week_days.index(day.capitalize())
		clas = routine[d][period]
		s = clas[:clas.rfind("(") - 1]
		already_filled = False
		for i in range(len(subjects)):
			if subjects[i][0] == s:
				subjects[i][2] -= 1
			if subjects[i][0] == subject:
				subjects[i][2] += 1
				if teacher not in subjects[i][1]:
					subjects[i][1].append(teacher)
				already_filled = True
		routine[d][period] = subject + " (" + teacher + ")"
		if not already_filled:
			subjects.append([subject, (teacher,), 1])
	except ValueError:
		pass

# Format of subjects is (subject name, number of classes in a week)
def display_routine():
	x = list(routine)
	for i in range(days):
		x[i] = [week_days[i]] + x[i]
	headings = ["Days"]
	for i in range(1, periods + 1):
		headings.append("Period " + str(i))
	display_table(headings, x)

while True:
	try:
		option = int(input("""
┌────────────────────────────┐
│Options                     │
├────────────────────────────┤
│1. Generate New routine     │
│2. Show routine             │
│3. Show subjects details    │
│4. Add substitution         │
│5. Swap classes             │
│6. Change class             │
│7. Regenerate routine       │
│8. Stop                     │
└────────────────────────────┘
Enter your choice : """))
		print("")
		if option == 1:
			print("┌───────────────────┐")
			print("│ Creating routine  │")
			print("└───────────────────┘")
			subjects = []
			total_classes = 0
			class_name = input("\t└ Enter class : ")
			periods = int(input("\t└ Enter number of periods in a day : "))
			max_classes = int(input("\t└ Enter maximum number of classes in a day per subject : "))
			create_routine(class_name, max_classes)
			while True:
				subject = input("\t└ Enter subject (leave empty to finish) : ")
				if not subject:
					break
				teachers = []
				while True:
					teacher = input("\t\t└ Enter teacher (leave empty to finish) : ")
					if not teacher:
						break
					teachers.append(teacher.upper().strip())
				classes = 0
				while True:
					classes = int(input("\t\t└ Enter number of classes in a week  : "))
					if classes > max_classes * days:
						print("\t\t┌────────────────────┐")
						print("\t\t│ Too many classes.  │")
						print("\t\t└────────────────────┘")
					else:
						break
				total_classes += classes
				subjects.append([subject.upper().strip(), teachers, classes])
			if periods * days != total_classes:
				print("\t┌─────────────────────────────────────────────────────────────────────────────────────────────┐")
				print("\t│ Total number of classes and total number of classes assigned to each subject are not equal. │")
				print("\t└─────────────────────────────────────────────────────────────────────────────────────────────┘")
				continue
			generate_routine()
			display_routine()
			i = 0
			for i in range(len(routine)):
				d = routine[i]
				for j in range(len(d)):
					create_period(week_days[i], j + 1, class_name, d[j])

		elif option == 2:
			if routine[0]:
				display_routine()
			else:
				print("")
				print("┌─────────────┐")
				print("│ No routine  │")
				print("└─────────────┘")

		elif option == 3:
			headings = ("Subjects",)
			l = 0
			for subject in subjects:
				headings += (subject[0] + " (" + str(subject[2]) + " Classes)",)
				l = max(l, len(subject[1]))
			k = len(subjects)
			teachers = []
			for i in range(l):
				row = [""]
				if i == (l - 1) // 2:
					row = ["Teachers"]
				for j in range(k):
					subject_teachers = subjects[j][1]
					if i < len(subject_teachers):
						row.append(subject_teachers[i])
					else:
						row.append("")
				teachers.append(row)
			display_table(headings, teachers)

		elif option == 4:
			print("┌─────────────────────┐")
			print("│ Adding Substitution │")
			print("└─────────────────────┘")
			day = input("\t└ Enter day to substitute : ").strip().upper()
			d = 0
			for i in range(len(week_days)):
				if day == week_days[i].upper():
					d = i
			teacher = input("\t└ Enter name of teacher to substitute : ").upper().strip()
			substitution(d, teacher)
			display_routine()

		elif option == 5:
			print("┌─────────────────────┐")
			print("│ Swap classes        │")
			print("└─────────────────────┘")
			day1, period1 = input("\t└ Enter class to swap (format day,period): ").replace(" ", "").split(",")
			day2, period2 = input("\t└ Enter class to swap with (format day,period): ").replace(" ", "").split(",")
			swap_classes(day1, int(period1) - 1, day2, int(period2) - 1)
			display_routine()

		elif option == 6:
			print("┌─────────────────────┐")
			print("│ Change Class        │")
			print("└─────────────────────┘")
			day, period = input("\t└ Enter class to change (format day,period): ").replace(" ", "").split(",")
			subject = input("\t└ Enter subject: ")
			teacher = input("\t└ Enter teacher: ")
			change_class(day, int(period) - 1, subject.upper().strip(), teacher.upper().strip())
			display_routine()

		elif option == 7:
			if generate_routine():
				display_routine()
			else:
				print("┌───────────────────────────────────────────────────────────────────────────────┐")
				print("│ There are too many classes to maintain the maximum number of classes in a day │")
				print("└───────────────────────────────────────────────────────────────────────────────┘")

		elif option == 8:
			break

		else:
			raise Exception()

	except Exception as e:
		print(e)
		print("┌────────────────┐")
		print("│ Invalid Option │")
		print("└────────────────┘")

close_db()
