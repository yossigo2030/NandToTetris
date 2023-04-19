"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code
import re


def assemble_file(
    input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
    input_file (typing.TextIO): the file to assemble.
    output_file (typing.TextIO): writes all output to this file.
    """

    symbol_table = SymbolTable()
    parser = Parser(input_file)
    first_pass(parser, symbol_table)
    second_pass(parser, symbol_table)
    for element in parser.new_list_of_commend:
        output_file.write(element + "\n")


def first_pass(parser, symbol_table):
    """
    Args:
    parser: parser object that parse the file
    symbol_table: table of symbols of the program
    and make the first pass of file and translate the () symbols
    Returns:
    """
    while parser.has_more_commands():
        parser.advance()
        stirped_command = parser.currentCommend.replace(" ", "")
        if stirped_command.startswith("//") or stirped_command == "":
            continue
        dest = re.search("(?:(?!/).)*", stirped_command)
        dest = dest.group(0)
        parser.type = parser.command_type()
        if parser.type == "L_COMMAND":
            symbol = parser.symbol()
            symbol_table.add_entry(symbol, parser.symbol_counter)
        else:
            Parser.new_list_of_commend.append(dest)
            parser.symbol_counter += 1


def second_pass(parser, symbol_table):
    """
    Args:
    parser: parser object that parse the file
    symbol_table: table of symbols of the program
    and make the second pass of file
    Returns:
    """
    num_of_symbols = 16
    parser.first_pass = False
    parser.currentLine = -1
    parser.endLines = len(parser.new_list_of_commend)
    while parser.has_more_commands():
        parser.advance()
        parser.type = parser.command_type()
        if parser.type == "L_COMMAND" or parser.type == "A_COMMAND":
            symbol = parser.symbol()
            if symbol.isdigit():
                num = int(symbol)
                make_a_code(parser, num)
            else:
                exist = symbol_table.contains(symbol)
                if not exist:
                    symbol_table.add_entry(symbol, num_of_symbols)
                    num_of_symbols += 1
                make_a_code(parser, symbol_table.get_address(symbol))
        else:
            make_c_code(parser)


def make_a_code(parser, symbol):
    """
    Args:
    parser: parser object that parse the file
    symbol: symbol of type a that need to translate to code
    Returns:
    """
    binary = bin(symbol)[2:].zfill(16)
    parser.new_list_of_commend[parser.currentLine] = binary


def make_c_code(parser):
    """
    Args:
    parser: parser object that parse the file
    translate the c type orders to code
    Returns:
    """
    shift_list = {'D<<', 'A<<', 'M<<', 'D>>', 'A>>', 'M>>'}
    code = Code()
    base = "111"
    dest = code.dest(parser.dest())
    comp_ee = parser.comp()
    comp = code.comp(comp_ee)
    jump = code.jump(parser.jump())
    for item in shift_list:
        if comp_ee == item:
            base = "101"
    new_code = base + comp + dest + jump
    parser.new_list_of_commend[parser.currentLine] = new_code


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
