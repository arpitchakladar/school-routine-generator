week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
days_per_week = len(week_days)

menu_prompt_message = """
┌─────────────────────────┐
│ Options                 │
├─────────────────────────┤
│ 1  Create new routine   │
│ 2  Show routine         │
│ 3  Show all classes     │
│ 4  Recreate routine     │
│ 5  Delete routine       │
│ 6  Stop                 │
│ !  Cancel any operation │
├─────────────────────────┘
└ Enter your choice: """


def display_message(message, indent=""):
	dash_border = "─" * (len(message) + 2)
	print(indent + "┌" + dash_border + "┐")
	print(indent + f"│ {message} │")
	print(indent + "└" + dash_border + "┘")


def c_input(prompt):
	value = input(prompt)
	if value.strip() == "!":
		raise ValueError("Operation cancelled.")
	else:
		return value
