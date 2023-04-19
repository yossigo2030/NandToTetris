"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re


class Parser:
    """Encapsulates access to the input code. Reads and assembly language
    command, parses it, and provides convenient access to the commands
    components (fields and symbols). In addition, removes all white space and
    comments.
    """
    type = None
    currentLine = -1
    endLines = 0
    currentCommend = None
    listOfCommend = []
    new_list_of_commend = []
    symbol_counter = 0
    first_pass = True

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
        input_file (typing.TextIO): input file.
        """
        input_lines = input_file.read().splitlines()
        self.listOfCommend = input_lines
        self.endLines = len(input_lines)

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
        bool: True if there are more commands, False otherwise.
        """
        self.currentLine += 1
        if self.currentLine == self.endLines:
            return False
        return True

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        if self.first_pass:
            self.currentCommend = self.listOfCommend[self.currentLine]
        else:
            self.currentCommend = self.new_list_of_commend[self.currentLine]

    def command_type(self) -> str:
        """
        Returns:
        str: the type of the current command:
        "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
        "C_COMMAND" for dest=comp;jump
        "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if self.currentCommend.startswith("@"):
            return "A_COMMAND"
        if self.currentCommend.startswith("("):
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
        str: the symbol or decimal Xxx of the current command @Xxx or
        (Xxx). Should be called only when command_type() is "A_COMMAND" or
        "L_COMMAND".
        """
        if self.type == "A_COMMAND":
            return self.currentCommend[1:]
        else:
            return self.currentCommend[1:-1]

    def dest(self) -> str:
        """
        Returns:
        str: the dest mnemonic in the current C-command. Should be called
        only when commandType() is "C_COMMAND".
        """
        dest = re.search("^.*=", self.currentCommend)
        if dest is None:
            return "null"
        self.currentCommend = re.sub("^.*=", "", self.currentCommend)
        dest = dest.group(0)
        dest = dest[:-1]
        return dest

    def comp(self) -> str:
        """
        Returns:
        str: the comp mnemonic in the current C-command. Should be called
        only when commandType() is "C_COMMAND".
        """
        comp = re.search("^.*;", self.currentCommend)
        if comp is None:
            comp = self.currentCommend
            self.currentCommend = ""
            return comp
        comp = comp.group(0)
        comp = comp[:-1]
        self.currentCommend = re.sub("^.*;", "", self.currentCommend)
        return comp

    def jump(self) -> str:
        """
        Returns:
        str: the jump mnemonic in the current C-command. Should be called
        only when commandType() is "C_COMMAND".
        """
        if self.currentCommend == "":
            return "null"
        return self.currentCommend

