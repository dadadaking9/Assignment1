# Brandon Chan
# chanbz@uci.edu
# 12383908

import pathlib
from pathlib import Path

def input_terminal(): 
        '''Takes user-input and delegates it accordingly'''
        user_input = input()

        # If the user types in 'Q', quit the program
        while user_input != "Q":
                is_valid = cmd_checker(user_input)
                if is_valid:
                        cmd_processor(user_input)
                        user_input = input()
                else:
                        error()
                        user_input = input()
                        
def cmd_checker(user_input)-> bool:
        '''Checks whether the user-entered command is one that the program can process'''
        commands = ['L ', 'C ', 'D ', 'R '] # Q, rather than a command, is set up as a program quitter.
        user_cmd = user_input[0:2]
        cmd_exists = user_cmd in commands
        valid_extension = True

        if len(user_input) < 1: # Empty Input
                return False
        if user_cmd == 'L ':
                l_valid_extensions = [' -r', ' -f']
                l_additional_input = [' -s', ' -e'] 
                l_user_extensions = []
                l_path_exists = True
                counter = 0
                # Process the string 2 characters at a time. After processing the 2 characters, forget about those 2 characters in the string.
                for character in user_input: 
                        remaining_input = user_input[counter:]
                        # if there's a ' -', recognize it as an attempted extension.
                        if (character == '-') and (user_input[counter - 1] == ' '): 
                                l_user_extensions.append(' ' + remaining_input[0:2])
                        counter += 1

                # For every extension detected in the user-input, check if it's an extension that the program supports        
                for extension in l_user_extensions:
                        if not ((extension in l_valid_extensions) or (extension in l_additional_input)):
                                valid_extension = False
                        if extension in l_additional_input:
                                try:
                                        if len(user_input[(user_input.index(extension) + 4):]) < 1: # both -s and -e require additional input. If none, invalid command. Try/except catches index out of bounds.
                                                valid_extension = False
                                except:
                                        valid_extension = False
                if len(l_user_extensions) < 1:
                        p = pathlib.Path(user_input[2:])
                        l_path_exists = p.exists()
                else:
                        p = pathlib.Path(user_input[2:(user_input.find(l_user_extensions[0]))])
                        l_path_exists = p.exists()
                return cmd_exists and valid_extension and l_path_exists
        elif cmd_exists: # C, D, and R all have built-in error checking so doing it here is unneccessary
                return True
        else:
                return False

def cmd_processor(command):
        '''Processess the given command by delegating the request to the respective method'''
        primary_command = command[0:1] 
        if primary_command == 'L':
                if '-r' in command:
                        list_recursive(command)
                else:
                        list_iterative(command)
        elif primary_command == 'C':
                create_cmd(command)
        elif primary_command == 'D':
                delete_cmd(command)
        elif primary_command == 'R':
                read_cmd(command)
                
def list_iterative(command):
        '''Runs the list command along with user-specifications iteratively'''
        file_l = []
        directory_l = []
        path_input = ''

        possible_extensions = [' -f',' -s',' -e']
        has_extension = False
        the_extension = ''
        
        for extension in possible_extensions:
                if extension in command:
                        the_extension = extension
                        has_extension = True
        
        if has_extension:
                path_input = command[2:command.index(the_extension)]
        else:
                path_input = command[2:]

        data_folder = pathlib.Path(path_input)

        for file_obj in data_folder.iterdir():
                if file_obj.is_file():
                        file_l.append(file_obj)
                elif file_obj.is_dir():
                        directory_l.append(file_obj)

        for file in file_l:
                if the_extension == '' or the_extension == ' -f':
                        print(file)
                elif the_extension == ' -s':
                        if str(file.name) == command[command.index(' -s ') + 4:]:
                                print(file)
                elif the_extension == ' -e':
                        if file.suffix == '.' + str(command[command.index(' -e ' + 4):]):
                                print(file)

        for directory in directory_l:
                if not (the_extension == ' -f'):
                        if not (the_extension == ' -s'):
                                print(directory)
                        else:
                                if directory.name == command[command.index(' -s ') + 4:]:
                                        print(directory)



def list_recursive(command):
        '''Runs the list command along with user-specifications recursively. Looks into directories in the specified path for more
        files if they exist.'''
        starting_location = pathlib.Path(command[2:command.index(' -r')])
        list_recursive_helper(command, starting_location)
        
                        
def list_recursive_helper(command, location): 
        '''Helper method for list_recursive.'''
        file_l = []
        directory_l = []

        for item in location.iterdir():
                if item.is_file():
                        file_l.append(item)
                elif item.is_dir():
                        directory_l.append(item)

        for f in file_l:
                if ' -s ' in command: 
                        if command[(command.index(' -s ') + 4):] == f.name:
                                print(f)
                elif ' -e ' in command:
                        if command[(command.index(' -e ') + 4):] == f.suffix[1:]: #[1:] is to skip the . in the file's suffix
                                print(f)
                else:
                        print(f)
                                
        for directory in directory_l:
                if not ((' -f' in command) or (' -s' in command) or (' -e' in command)):
                        print(directory)
                elif ' -s ' in command:
                        if command[(command.index(' -s ') + 4):] == directory.name:
                                print(directory)
                list_recursive_helper(command, directory)
                        

def create_cmd(command):
        '''Create a new user-named file in a user-specified directory'''
        try:
                name_index = command.index(' -n ')
                file_name = command[name_index + 4:]
                specified_dir = command[2:name_index]
                item = pathlib.Path(specified_dir)
                new_item = file_name + '.dsu'
                item.joinpath(new_item).touch(exist_ok = False)
                print(item.joinpath(new_item))
        except:
                error()

def delete_cmd(command):
        '''Deletes a specified DSU file. Errors if file specified is
        not a DSU file.'''
        try:
                del_item = pathlib.Path(command[2:])
                if del_item.suffix == '.dsu':
                        del_item.unlink(missing_ok = False)
                        print (str(del_item) + ' DELETED')
                else:
                        error()
        except:
                error()

def read_cmd(command):
        '''Attempts to read the user-specified file. If empty, prints "EMPTY". '''
        try:
                read_item = pathlib.Path(command[2:])
                if read_item.suffix == '.dsu':
                        if read_item.stat().st_size == 0:
                                print('EMPTY') 
                        else:
                                try:
                                        read_item.open('r')
                                        print(read_item.read_text(),end='')
                                except:
                                        error()
                else:
                        error()
        except:
                error()


def error():
        '''Prints 'ERROR'''
        print('ERROR')
        
def main():
        input_terminal()


if __name__ == "__main__":
        main()
