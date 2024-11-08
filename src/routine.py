from random import randint
from utils import *
from table import *
from db import *


def _generate_class_routine(subjects, periods_per_day, max_subject_periods):
	subject_periods_left = {}
	for name, _, period_count in subjects:
		subject_periods_left[name] = period_count
	
	for subject_name, _, period_count in subjects:
		if period_count > max_subject_periods * days_per_week:
			return []
	
	routine = []

	for day in range(days_per_week):
		daily_schedule = []

		if day == 4:
			for periods_left in subject_periods_left.values():
				if periods_left > max_subject_periods:
					return _generate_class_routine(subjects, periods_per_day, max_subject_periods)

		for period in range(periods_per_day):
			subject = None
			while True:
				subject_index = randint(0, len(subjects) - 1)
				subject = subjects[subject_index]
				subject_name = subject[0]
				
				if subject_periods_left[subject_name] > 0:
					period_count = 0
					for scheduled_class in daily_schedule:
						if scheduled_class.startswith(subject_name):
							period_count += 1
					if period_count < max_subject_periods:
						break

			teacher_list = subject[1]
			teacher = teacher_list[randint(0, len(teacher_list) - 1)]
			daily_schedule.append(f"{subject_name} ({teacher})")
			subject_periods_left[subject_name] -= 1

		routine.append(daily_schedule)
	return routine


def generate_routine():
	subjects = []
	total_periods_scheduled = 0
	class_name = c_input("\t└ Enter class name: ")
	periods_per_day = int(c_input("\t└ Enter number of periods per day: "))
	max_subject_periods = int(c_input("\t└ Enter maximum periods per subject per day: "))
	total_weekly_periods = periods_per_day * days_per_week
	while True:
		subject_name = c_input("\t└ Enter subject name: ").upper().strip()
		if not subject_name:
			continue
		teachers = []
		while True:
			teacher_name = c_input("\t\t└ Enter teacher name (leave empty to finish): ").upper().strip()
			if not teacher_name:
				break
			teachers.append(teacher_name)
		while True:
			weekly_class_periods = int(c_input("\t\t└ Enter number of periods per week: "))
			if weekly_class_periods > max_subject_periods * days_per_week:
				display_message("Too many periods for a subject in a week.", "\t\t")
			elif weekly_class_periods + total_periods_scheduled > total_weekly_periods:
				display_message(
					f"Only {total_weekly_periods - total_periods_scheduled} periods left for the week.",
					"\t\t",
				)
			else:
				break
		total_periods_scheduled += weekly_class_periods
		subjects.append([subject_name, teachers, weekly_class_periods])
		if total_weekly_periods == total_periods_scheduled:
			break
		else:
			display_message(
				f"{total_weekly_periods - total_periods_scheduled} periods left for the week.",
				"\t",
			)
	routine = _generate_class_routine(subjects, periods_per_day, max_subject_periods)
	if insert_class_routine(class_name, routine):
		display_routine(class_name)
	else:
		display_message(
			f"Routine for class {class_name} already exists.",
			"\t",
		)


def display_routine(class_name):
	routine = get_routine(class_name)
	if routine == False:
		display_message(
			f"Routine for class {class_name} not found.",
			"\t",
		)
		return
	formatted_routine = []
	for i in range(len(week_days)):
		routine_period = [week_days[i]]
		for day_schedule in routine:
			routine_period.append(day_schedule[i])
		formatted_routine.append(routine_period)
	headers = ["Days"]
	for i in range(1, len(routine) + 1):
		headers.append(f"Period {i}")
	display_table(headers, formatted_routine, "Routine of " + class_name.upper())


def list_classes():
	class_names = get_class_names()
	if len(class_names) == 0:
		class_names = ["No classes"]
	display_single_row_table("Classes", class_names)
