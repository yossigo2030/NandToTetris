"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""
    output_file = None
    current_line = -1

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
        output_stream (typing.TextIO): output stream.
        """
        self.output_file = output_stream

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.

        Args:
        filename (str): The name of the VM file.
        """
        # Your code goes here!
        pass

    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given
        arithmetic command.

        Args:
        command (str): an arithmetic command.
        """
        if command == "add":
            self.add_sub("D=M+D")
        if command == "sub":
            self.add_sub("D=M-D")
        if command == "neg":
            self.output_file.write("@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1\n")
        if command == "eq":
            self.compare("D;JNE")
        if command == "gt":
            self.compare("D;JLE")
        if command == "lt":
            self.compare("D;JGE")
        if command == "and":
            self.and_or("D=D&M")
        if command == "or":
            self.and_or("D=D|M")
        if command == "not":
            self.output_file.write("@SP\nM=M-1\nA=M\nM=!M\n@SP\nM=M+1\n")
        if command == "shiftLeft":
            self.shift("M<<")
        if command == "shiftRight":
            self.shift("M>>")

    def compare(self, command) -> None:
        self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@FALSE."
                               + str(self.current_line) + "\n" + command + "\n@SP\nA=M\nM=-1\n@CONTINUE."
                               + str(self.current_line) + "\n0;JMP\n(FALSE." + str(self.current_line)
                               + ")\n@SP\nA=M\nM=0\n(CONTINUE." + str(self.current_line) + ")\n@SP\nM=M+1\n")

    def add_sub(self, command) -> None:
        self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\n" + command + "\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def and_or(self, command):
        self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\n" + command + "\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.current_line += 1

    def shift(self, command) -> None:
        self.output_file.write("SP\nM=M-1\nA=M\n" + command + "\n@SP\nM=M+1\n")

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes the assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
        command (str): "C_PUSH" or "C_POP".
        segment (str): the memory segment to operate on.
        index (int): the index in the memory segment.
        """
        str_index = str(index)
        if command == "push":
            if segment == "constant":
                self.output_file.write("@" + str_index + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            if segment == "local":
                self.push_standard(str_index, "LCL")
            if segment == "argument":
                self.push_standard(str_index, "ARG")
            if segment == "this":
                self.push_standard(str_index, "THIS")
            if segment == "that":
                self.push_standard(str_index, "THAT")
            if segment == "temp":
                self.output_file.write("@" + str_index + "\nD=A\n@R5\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            if segment == "pointer":
                if index == 0:
                    self.push_pointer("THIS")
                else:
                    self.push_pointer("THAT")
            if segment == "static":
                self.output_file.write("@Foo." + str_index + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        else:
            if segment == "local":
                self.pop_standard(str_index, "LCL")
            if segment == "argument":
                self.pop_standard(str_index, "ARG")
            if segment == "this":
                self.pop_standard(str_index, "THIS")
            if segment == "that":
                self.pop_standard(str_index, "THAT")
            if segment == "temp":
                self.output_file.write("@" + str_index + "\nD=A\n@R5\nD=D+A\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n"
                                                         "@R13\nA=M\nM=D\n")
            if segment == "pointer":
                if index == 0:
                    self.pop_pointer("THIS")
                else:
                    self.pop_pointer("THAT")
            if segment == "static":
                self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@Foo." + str_index + "\nM=D\n")

    def push_pointer(self, command):
        self.output_file.write("@" + command + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def close(self) -> None:
        """Closes the output file."""
        self.output_file.close()

    def push_standard(self, str_index, segment):
        self.output_file.write("@" + str_index + "\nD=A\n@" + segment +
                               "\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def pop_standard(self, str_index, segment):
        self.output_file.write("@" + str_index + "\nD=A\n@" + segment +
                               "\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n")

    def pop_pointer(self, command):
        self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@" + command + "\nM=D\n")
