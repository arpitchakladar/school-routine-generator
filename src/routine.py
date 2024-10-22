from random import randint

from utils import *
from table import *
from db import *

def _generate_routine(subjects, periods, max_classes):
	used = {}
	for name, _, n in subjects:
		used[name] = n
		if n > max_classes * days:
			return []
	routine = []

	for d in range(days):
		l = []
		if d == 4:
			for u in used.values():
				if u > max_classes:
					return _generate_routine(subjects, periods, max_classes)

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
	return routine

def generate_routine():
	subjects = []
	total_classes = 0
	class_name = input("\t└ Enter class : ")
	periods = int(input("\t└ Enter number of periods in a day : "))
	max_classes = int(input("\t└ Enter maximum number of classes in a day per subject : "))
	total_possible_classes = periods * days

	while True:
		subject = input("\t└ Enter subject : ")
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
				display_message("Too many classes for a single subject in a week.", "\t\t")
			elif classes + total_classes > total_possible_classes:
				display_message(f"Only {total_possible_classes - total_classes} classes are left for the week.", "\t\t")
			else:
				break

		total_classes += classes
		subjects.append([subject.upper().strip(), teachers, classes])

		if total_possible_classes == total_classes:
			break
		else:
			display_message(f"{total_possible_classes - total_classes} classes left for the week.", "\t")

	routine = _generate_routine(subjects, periods, max_classes)
	create_routine(class_name, routine)
	display_routine(class_name)
