week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
days = len(week_days)

def display_message(message, indent=""):
	print(indent + "┌" + ("─" * (len(message) + 2)) + "┐")
	print(indent + "│", message, "│")
	print(indent + "└" + ("─" * (len(message) + 2)) + "┘")
