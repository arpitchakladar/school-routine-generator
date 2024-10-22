from table import *
from db import *
from utils import *
from routine import *

while True:
	try:
		option = int(input("""
┌─────────────────────────┐
│ Options                 │
├─────────────────────────┤
│ 1. Create New routine   │
│ 2. Show routine         │
│ 3. Show all classes     │
│ 4. Recreate routine     │
│ 5. Delete routine       │
│ 6. Stop                 │
└─────────────────────────┘
Enter your choice : """))
		print("")
		if option == 1:
			display_message("Creating routine.")
			generate_routine()

		elif option == 2:
			class_name = input("\t└ Enter class : ")
			display_routine(class_name)

		elif option == 3:
			list_classes()

		elif option == 4:
			class_name = input("\t└ Enter existing class : ")
			delete_routine(class_name)
			display_message(f"Recreating routine for {class_name}.", "\t")
			generate_routine()

		elif option == 5:
			class_name = input("\t└ Enter class : ")
			delete_routine(class_name)
			display_message("Routine deleted.")

		elif option == 6:
			break

		else:
			raise Exception()

	except Exception as e:
		print(e)
		display_message("Invalid Option")

close_db()
