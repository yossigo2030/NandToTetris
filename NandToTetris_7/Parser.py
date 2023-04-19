"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient
    access to their components.
    In addition, it removes all white space and comments.
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
        """Gets ready to parse the input file.

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
        """Reads the next command from the input and makes it the current
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        self.currentCommend = self.listOfCommend[self.currentLine]

    def command_type(self) -> str:
        """
        Returns:
        str: the type of the current VM command.
        "C_ARITHMETIC" is returned for all arithmetic commands.
        For other commands, can return:

        "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
        "C_RETURN", "C_CALL".
        """
        if self.currentCommend.startswith("add") or self.currentCommend.startswith("sub")\
                or self.currentCommend.startswith("eq") or self.currentCommend.startswith("gt") or\
                self.currentCommend.startswith("lt") or self.currentCommend.startswith("and") or\
                self.currentCommend.startswith("or") or self.currentCommend.startswith("neg") or\
                self.currentCommend.startswith("not"):
            return "C_ARITHMETIC"
        if self.currentCommend.startswith("push"):
            return "C_PUSH"
        if self.currentCommend.startswith("pop"):
            return "C_POP"
        else:
            return "EX8"

    def arg1(self) -> str:
        """
        Returns:
        str: the first argument of the current command. In case of
        "C_ARITHMETIC", the command itself (add, sub, etc.) is returned.
        Should not be called if the current command is "C_RETURN".
        """
        if self.type == "C_ARITHMETIC":
            return self.currentCommend
        else:
            return self.currentCommend

    def arg2(self) -> int:
        """
        Returns:
        int: the second argument of the current command. Should be
        called only if the current command is "C_PUSH", "C_POP",
        "C_FUNCTION" or "C_CALL".
        """
        # Your code goes here!
        pass
