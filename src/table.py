def _display_table_border(start_char, end_char, column_widths, separator):
	print(start_char, end="")
	for width in column_widths[:-1]:
		print("─" * (width + 2), end=separator)
	print("─" * (column_widths[-1] + 2) + end_char)


def display_table(headers, rows):
	header_names = [str(header) for header in headers]

	column_widths = []
	for col_index in range(len(header_names)):
		max_width = len(header_names[col_index])
		for row in rows:
			cell_width = len(str(row[col_index]))
			if cell_width > max_width:
				max_width = cell_width
		column_widths.append(max_width)

	_display_table_border("┌", "┐", column_widths, "┬")
	print("│ ", end="")
	for col_index, header in enumerate(header_names):
		print(header, " " * (column_widths[col_index] - len(header)), end="│ ")
	print()

	_display_table_border("├", "┤", column_widths, "┼")

	for row in rows:
		print("│ ", end="")
		for col_index, cell in enumerate(row):
			cell_str = str(cell)
			print(cell_str, " " * (column_widths[col_index] - len(cell_str)), end="│ ")
		print()

	_display_table_border("└", "┘", column_widths, "┴")
