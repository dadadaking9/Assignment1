# a1.py

# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Brandon Chan
# chanbz@uci.edu
# 12383908

import pathlib
from pathlib import Path

def valid_input_check(user_input)->bool:
	'''Check if the user's input is a valid command'''
	valid_commands = ['Q','L','C','D','R']
	user_info = user_input.split()
	# TODO: user_info[1] will not work if the path has spaces
	# Edge Cases

	# Empty Input
	if len(user_info) < 1:
		return False

	# Quitting the Program
	if user_info[0] == 'Q':
		return True

	# No additional info added asides from command
	if len(user_info) < 2:
		return False

	
	p = Path(user_info[1])

	# Delete Edge Case
	if user_info[0] == 'D':
		p = Path(user_input[2:])
		return p.exists()

	# Read Edge Case
	if user_info[0] == 'R':
		p = Path(user_input[2:])
		return p.exists()

	#print (user_info[0] in valid_commands, p.exists()) #Delete
	return (user_info[0] in valid_commands) and (p.exists())

def list_cmd(recursive, path_input, file_only, name_only, name, suffix_only, the_suffix):
	data_folder = pathlib.Path(path_input)
	file_l = []
	directory_l = []
	if not recursive: # Runs Iteratively
		# Sorts files and directories into seperate lists
		for file_obj in data_folder.iterdir():
			if file_obj.is_file():
				file_l.append(file_obj)
			elif file_obj.is_dir():
				directory_l.append(file_obj)

		# Prints sorted files first and then sorted directories
		for file in file_l:
			print(file)
		for directory in directory_l:
			if not file_only:
				print(directory)	

	else: # Runs Recursively
		#print('Entered Recursive List Run') #Delete
		if data_folder.is_file():
			if not (suffix_only) and not (name_only):
				print(data_folder)
			elif suffix_only: # If the user specifies a suffix
				if str(data_folder.suffix) == '.' + the_suffix:
					print(data_folder)
			elif name_only: # If the user is searching for a specific name
				if data_folder.name == name:
					print(data_folder)
		elif data_folder.is_dir():
			#print('recognizes as directory') #Delete
			if not file_only:
				#print('thinks name_only is ' + str(name_only)) #Delete
				if not (name_only) and not (suffix_only):
					print(data_folder)
				elif name_only:
					if name == str(data_folder.name):
						print(data_folder)
				elif suffix_only:
					if str(data_folder.suffix) == the_suffix:
						print(data_folder)

			#print('Made it to before the for loop') #Delete
			for objs in data_folder.iterdir():
				list_cmd(recursive, str(objs), file_only, name_only, name, suffix_only, the_suffix)



def create_cmd(specified_dir, file_name):
	'''Create a new user-named file in a user-specified directory'''
	item = pathlib.Path(specified_dir)
	item.joinpath(file_name + '.dsu').touch(exist_ok = True)

def delete_cmd(del_path):
	'''Deletes a specified DSU file. Errors if file specified is
	not a DSU file.'''
	try:
		del_item = pathlib.Path(del_path)
		if del_item.suffix == '.dsu':
			del_item.unlink(missing_ok=True)
			print (str(del_item) + ' DELETED')
	except:
		print('ERROR')

def read_cmd(specified_file):
	'''Attempts to read the user-specified file. If empty, prints "EMPTY". '''
	try:
		read_item = pathlib.Path(specified_file)
		if read_item.suffix == '.dsu':
			if read_item.stat().st_size == 0:
				print('EMPTY')
			else:
				try:
					read_item.open('r')
					read_item.readlines()
				except:
					print('ERROR')
		else:
			print("ERROR")
	except:
		print('ERROR')

def main():																										
	no_error = False
	while not no_error: # While there's an error
		user_in = input()
		no_error = valid_input_check(user_in) # Check if the input is valid
		if not no_error: # If it isn't

			print('ERROR')
		else: # If is valid
			cmd_input = user_in.split()
			if cmd_input[0] == 'Q':
				break
			elif cmd_input[0] == 'L':
				#print('Made it into "L"') #Delete
				if '-r' in cmd_input:
					#print('Made it into -r if loop') #Delete
					if '-f' in user_in: # Print Only Files
						#print('recognizes the f') #Delete
						list_cmd(True, cmd_input[1], True, False, '', False, '')
					elif '-s' in user_in: # Print files with given name
						list_cmd(True, cmd_input[1], False, True, user_in[(user_in.index(' -s ') + 4):], False, '')
					elif '-e' in user_in: # Print only files with given suffix
						list_cmd(True, cmd_input[1], False, False, '', True, cmd_input[4])
					else:
						list_cmd(True, cmd_input[1], False, False, '', False, '')
				# Edge Case, -f opperates iteratively
				elif '-f' in cmd_input:
					list_cmd(False, cmd_input[1], True, False, '', False, '')
				else:
					list_cmd(False, cmd_input[1], False, False, '', False, '')
#def list_cmd(recursive, path_input, file_only, name_only, name, suffix_only, the_suffix):

			elif cmd_input[0] == 'C': 
				try:
					name_index = user_in.index(' -n ')
					create_cmd(cmd_input[1], user_in[name_index + 4:])
				except:
					print("ERROR")				

			elif cmd_input[0] == 'D':
				delete_cmd(user_in[2:])

			elif cmd_input[0] == 'R':
				read_cmd(user_in[2:])
			no_error = False # Reset loop	


if __name__ == "__main__":
	main()
