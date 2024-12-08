from table import *
from db import *
from utils import *
from routine import *

while True:
	try:
		user_choice = int(c_input(menu_prompt_message))

		if user_choice == 1:
			display_message("Creating new routine.")
			generate_routine()

		elif user_choice == 2:
			class_name = c_input("\t└ Enter class name: ")
			display_routine(class_name)

		elif user_choice == 3:
			list_classes()

		elif user_choice == 4:
			class_name = c_input("\t└ Enter existing class name: ")
			if delete_class_routine(class_name):
				display_message(
					f"Recreating routine for {class_name}.",
					"\t",
				)
				generate_routine()
			else:
				display_message(f"No routine found for class {class_name}.")

		elif user_choice == 5:
			class_name = c_input("\t└ Enter class name: ")
			if delete_class_routine(class_name):
				display_message("Routine successfully deleted.")
			else:
				display_message(f"No routine found for class {class_name}.")

		elif user_choice == 6:
			break

		else:
			raise ValueError("Invalid menu option selected.")

	except ValueError as e:
		display_message(str(e))

	except Exception as e:
		display_message("Failed to process request.")


close_database()
