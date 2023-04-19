"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from Parser import Parser
from CodeWriter import CodeWriter
import re

flag = True


def translate_file(
    input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Translates a single file.
    Args:
    input_file (typing.TextIO): the file to translate.
    output_file (typing.TextIO): writes all output to this file.
    """

    parser = Parser(input_file)
    code_writer = CodeWriter(output_file)
    global flag
    if flag:
        code_writer.write_int()
    flag = False
    while parser.has_more_commands():
        parser.advance()
        stirped_command = parser.currentCommend.strip(" ")
        if stirped_command.startswith("//") or stirped_command == "":
            continue
        command = re.search("(?:(?!/).)*", stirped_command)
        command = command.group(0)
        parser.type = parser.command_type()
        code_writer.output_file.write("// " + command + "\n")
        split_command = command.split(" ")
        if parser.type == "C_ARITHMETIC":
            code_writer.current_line += 1
            code_writer.write_arithmetic(split_command[0])
            continue
        if parser.type == "LABEL":
            code_writer.write_label(split_command[1])
            continue
        if parser.type == "IF":
            code_writer.write_if(split_command[1])
            continue
        if parser.type == "GOTO":
            code_writer.write_goto(split_command[1])
            continue
        if parser.type == "FUNCTION":
            code_writer.write_function(split_command[1], int(split_command[2]))
            continue
        if parser.type == "RETURN":
            code_writer.write_return()
            continue
        if parser.type == "CALL":
            code_writer.write_call(split_command[1], split_command[2])
            continue
        else:
            code_writer.write_push_pop(split_command[0], split_command[1], int(split_command[2]))


if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file)
                