"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

num = 0


class CodeWriter:
    """Translates VMtranslator commands into Hack assembly code."""
    output_file = None
    current_line = -1

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
        output_stream (typing.TextIO): output stream.
        """
        self.output_file = output_stream
        global num

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VMtranslator file is
        started.

        Args:
        filename (str): The name of the VMtranslator file.
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
            self.neg_not("M=-M")
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
            self.neg_not("M=!M")
        if command == "shiftLeft":
            self.shift("M<<")
        if command == "shiftRight":
            self.shift("M>>")

    def compare(self, command) -> None:
        self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@FALSE."
                               + str(self.current_line) + "\n" + command + "\n@SP\nA=M\nM=-1\n@CONTINUE."
                               + str(self.current_line) + "\n0;JMP\n(FALSE." + str(self.current_line)
                               + ")\n@SP\nA=M\nM=0\n(CONTINUE." + str(self.current_line) + ")\n@SP\nM=M+1\n")

    def neg_not(self, command) -> None:
        self.output_file.write("@SP\nM=M-1\nA=M\n" + command + "\n@SP\nM=M+1\n")

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

    def write_int(self):
        self.output_file.write("@256\nD=A\n@SP\nM=D\n")
        self.write_call("Sys.init", 0)

    def write_label(self, label):
        self.output_file.write("(" + label + ")\n")

    def write_goto(self, label):
        self.output_file.write("@" + label + "\n0;JMP\n")

    def write_if(self, label):
        self.output_file.write("@SP\nAM=M-1\nD=M\nA=A-1\n@" + label + "\nD;JNE\n")
        # self.output_file.write("@SP\nM=M-1\nA=M\nD=M\n@" + label + "\nD;JNE\n")

    def write_function(self, function_name, num_vars):
        self.output_file.write("(" + function_name + ")\n")
        for i in range(0, num_vars):
            self.write_push_pop("push", "constant", 0)
        # i = 0
        # while i < num_vars:
        # self.write_push_pop("push", "constant", 0)
        # i += 1

    def write_call(self, function_name, num_args):
        global num
        self.saved_parameters()
        self.output_file.write("@SP\nD=M\n@5\nD=D-A\n@" + str(num_args) + "\nD=D-A\n@ARG\nM=D\n")
        self.output_file.write("@SP\nD=M\n@LCL\nM=D\n")
        self.output_file.write("@" + function_name + "\n0;JMP\n(returnAddress" + str(num) + ")\n")
        num += 1

    def write_return(self):
        self.output_file.write("@LCL\nD=M\n@R11\nM=D\n@5\nA=D-A\nD=M\n@R12\nM=D\n")
        self.output_file.write("@ARG\nD=M\n@0\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.output_file.write("@ARG\nD=M\n@SP\nM=D+1\n")
        param = self.return_helper_2("THAT") + self.return_helper_2("THIS") + self.return_helper_2("ARG") + \
                self.return_helper_2("LCL")
        self.output_file.write(param + "@R12\nA=M\n0;JMP\n")

    def return_helper_2(self, segment):
        return "@R11\nD=M-1\nAM=D\nD=M\n@" + segment + "\nM=D\n"

    def saved_parameters(self):
        global num
        saved = self.saved_parameters_helper("LCL") + self.saved_parameters_helper("ARG") + \
                self.saved_parameters_helper("THIS") + self.saved_parameters_helper("THAT")
        self.output_file.write("@returnAddress" + str(num) + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" + saved)

    def saved_parameters_helper(self, segment) -> str:
        return "@" + segment + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
