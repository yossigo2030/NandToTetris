"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import re
import sys
import typing
from CompilationEngine import CompilationEngine
from JackTokenizer import JackTokenizer


def analyze_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Analyzes a single file.
    Args:
        input_file (typing.TextIO): the file to analyze.
        output_file (typing.TextIO): writes all output to this file.
    """
    jack_tokenizer = JackTokenizer(input_file)
    flag = False
    while jack_tokenizer.has_more_tokens():
        jack_tokenizer.advance()
        stirped_token = jack_tokenizer.current_token.strip()
        if flag:
            res = re.search("(?:(?!\*/).)*\*/", stirped_token)
            if res == None:
                continue
            stirped_token = stirped_token[res.end():]
            flag = False
        if stirped_token.startswith("//") or stirped_token == "" or stirped_token.startswith("/**")\
                or stirped_token.startswith("*") or (stirped_token.startswith("/*") and stirped_token.endswith("*/")):
            continue
        token = stirped_token
        rr = ""
        while True:
            temp = re.search("(?:(?!//).)*", token)
            rest1 = token[temp.end():]
            qqqqq = re.search("(?:(?!\").)*", token)
            if qqqqq != None:
                rest2 = token[qqqqq.end():]
                if len(rest2) > len(rest1):
                    string_qout = re.search("^\"[^\"]*\"", rest2)
                    final_rest = rest2[string_qout.end():]
                    rr = rr + qqqqq.group(0) + string_qout.group(0)
                    token = final_rest
                    continue
            if rr != "":
                token = rr + temp.group(0)
                break
            token = temp.group(0)
            break
        token = token.strip()
        # print(token)
        line = token
        fff = ""
        while True:
            result = re.search("^[^/*]*", line)
            rest = line[result.end():]
            if rest != "":
                aaaa = re.search("^[^\"]*", line)
                if aaaa != None:
                    qout = line[aaaa.end():]
                    if len(qout) > len(rest):
                        xxxx = re.search("^[^\"]*\"[^\"]*\"", line)
                        fff = fff + xxxx.group(0)
                        line = line[xxxx.end():]
                        continue
                res1 = re.search("^/\*{1,2}", rest)
                if res1 == None:
                    symbol = ""
                    if rest[0] == "/":
                        symbol = re.search("^/", rest)
                    else:
                        symbol = re.search("^\*", rest)
                    rest = rest[symbol.end():]
                    begin = result.group(0) + symbol.group(0)
                    fff = begin
                    line = rest
                    continue
                res = re.search("^/\*{1,2}[^*/]*\*/", rest)
                if res != None:
                    end = rest[res.end():]
                    if fff == "":
                        line = result.group(0) + " " + end
                        continue
                    line = fff + result.group(0) + " " + end
                    continue
                flag = True
                line = re.search("^[^*]*", line).group(0)
                line = line[:-1]
            if fff == "":
                break
            line = fff + result.group(0)
            break
        # print(line)
        jack_tokenizer.advance_helper(line)
    jack_tokenizer.token_list.append("</tokens>")
    # for item in jack_tokenizer.token_list:
    # print(item)
    CompilationEngine(jack_tokenizer.token_list, output_file)


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: JackAnalyzer <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".jack":
            continue
        output_path = filename + ".xml"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            analyze_file(input_file, output_file)
