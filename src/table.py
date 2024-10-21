def _display_table_bar(start, end, column_widths, sep):
	print(start, end="")
	for w in column_widths[:-1]:
		print("─" * (w + 2), end=sep)
	print("─" * (column_widths[-1] + 2) + end)

def display_table(headings, data):
	column_names = []
	for i in range(len(headings)):
		column_names.append(str(headings[i]))

	column_widths = []
	for i in range(len(column_names)):
		m = len(column_names[i])
		for j in range(len(data)):
			m1 = len(str(data[j][i]))
			if m1 > m:
				m = m1
		column_widths.append(m)

	_display_table_bar("┌", "┐", column_widths, "┬")
	print("│ ", end="")
	for i in range(len(column_names)):
		column = column_names[i]
		print(column, " " * (column_widths[i] - len(column)), end="│ ")
	print("")

	_display_table_bar("├", "┤", column_widths, "┼")

	for row in data:
		print("│ ", end="")
		for i in range(len(row)):
			x = str(row[i])
			print(x, " " * (column_widths[i] - len(x)), end="│ ")
		print()
	_display_table_bar("└", "┘", column_widths, "┴")
