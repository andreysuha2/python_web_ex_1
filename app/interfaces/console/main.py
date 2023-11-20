from app.interfaces.InterfaceABC import InterfaceHandlerABC, IntrfaceABC
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from app.comands import CLOSE_COMANDS, HANDLERS
from app.interfaces.console.CommandsList import CommandsList
from app.interfaces.console import Commands as commands
from app.interfaces.console.CommandABC import CommandABC
from typing import Tuple
import re

class ConsoleInterface(IntrfaceABC):
    def __init__(self) -> None:
        super().__init__()
        self.completer = NestedCompleter.from_nested_dict({ k: None for k in  [ *HANDLERS.keys(), *CLOSE_COMANDS ] })
        
    def input(self, input_text=">>> "):
        return (prompt(input_text, completer=self.completer)).strip()
    
    def output(self, *args):
        return print(*args)
    
class ConsoleHandler(InterfaceHandlerABC):
    def __init__(self, interface: IntrfaceABC):
        super().__init__(interface)
        self.commands_list = CommandsList()
        self.__init_commands()

    def __init_commands(self):
        self.commands_list.add_command(pseudos=('help',), command=commands.HelpCommand(commands_list=self.commands_list))
        self.commands_list.add_command(pseudos=('close', 'exit', 'good bye', 'bye'), command=commands.CloseCommand())
        self.commands_list.add_command(pseudos=('search',), command=commands.SearchCommand())
        self.commands_list.add_command(pseudos=('add contact',), command=commands.AddContactCommand())
        self.commands_list.add_command(pseudos=('add phone', 'add phones'), command=commands.AddPhonesCommand())
        self.commands_list.add_command(pseudos=('add birthday', ), command=commands.AddBirthdayCommand())
        self.commands_list.add_command(pseudos=('add address', ), command=commands.AddAddress())
        self.commands_list.add_command(pseudos=('add mail', ), command=commands.AddMail())
        self.commands_list.add_command(pseudos=('remove contact', ), command=commands.RemoveContactCommand())
        self.commands_list.add_command(pseudos=('show contact', ), command=commands.ShowContactCommand())
        self.commands_list.add_command(pseudos=('change phone', ), command=commands.ChangePhoneCommand())
        self.commands_list.add_command(pseudos=('remove phone', ), command=commands.RemovePhoneCommand())
        self.commands_list.add_command(pseudos=('days to birthday',), command=commands.DaysToBirthday())
        self.commands_list.add_command(pseudos=('birthdays range',), command=commands.BirthdaysRange())
        self.commands_list.add_command(pseudos=('show all', ), command=commands.ShowAllContacts())
        self.commands_list.add_command(pseudos=('add note',), command=commands.AddNoteCommand())
        self.commands_list.add_command(pseudos=('update note',), command=commands.UpdateNoteCommand())
        self.commands_list.add_command(pseudos=('delete note',), command=commands.DeleteNoteCommand())
        self.commands_list.add_command(pseudos=('searh note',), command=commands.SearchNoteCommand())
        self.commands_list.add_command(pseudos=('sort file',), command=commands.SortFilesCommand())
        
    def __parse_input(self, input_string) -> Tuple[CommandABC, list]:
        searching_pseudo = next((pseudo for pseudo in self.commands_list.pseudos_list if re.search(f"^({pseudo}(\s|$))", input_string)), None)
        if not searching_pseudo:
            raise UndefinedCommandException
        command = self.commands_list.get_command(searching_pseudo)
        args = input_string[len(searching_pseudo) + 1:].split(' ')
        return (command, list(filter(lambda arg: arg, args)))
    
    def __execute_comand(self, command: CommandABC, args: list = []):
        output = command.execute(args)
        if output:
            self.interface.output(output)
        
    
    def run(self):
        print(f'Hello!!! \r\nYoy can use "help" comand ')
        while True:
            try:
                input_string = self.interface.input()
                command, args = self.__parse_input(input_string)
                self.__execute_comand(command, args)
                if not command.next:
                    break
            except KeyboardInterrupt:
                command = self.commands_list.get_command('close')
                self.__execute_comand(command, [])
                break
            except UndedinedCommandException:
                print("We can't find this command, please try again or use help command.")

class UndefinedCommandException(Exception):
    pass