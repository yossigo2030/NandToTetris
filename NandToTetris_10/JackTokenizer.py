"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import re
import typing

class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    """
    input = []
    end_lines = 0
    token_list = []
    current_line = -1
    current_token = None

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.
        Args:
        input_stream (typing.TextIO): input stream.
        """
        self.input = input_stream.read().splitlines()
        self.end_lines = len(self.input)
        self.token_list = []
        self.current_line = -1
        self.token_list.append("<tokens>")

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?
        Returns:
        bool: True if there are more tokens, False otherwise.
        """
        if self.current_line + 1 == self.end_lines:
            return False
        return True

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token.
        This method should be called if has_more_tokens() is true.
        Initially there is no current token.
        """
        self.current_line += 1
        self.current_token = self.input[self.current_line]

    def advance_helper(self, token):
        result = re.search("^[^\"]*", token)
        rest = token[result.end():]
        if rest == "":
            replace = token.replace("\t", " ")
            split_line = replace.split(" ")
            for item in split_line:
                if item == " ":
                    continue
                self.token_type(item)
            return
        strip = result.group(0).strip()
        split_line = strip.split(" ")
        for item in split_line:
            if item == " ":
                continue
            self.token_type(item)
        self.token_type(rest)

    def token_type(self, item):
        """
        Returns:
        str: the type of the current token, can be
        "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        result = re.search("^\"[^\"]*\"", item)
        if result is not None:
            self.string_val(result.group(0)[1:-1])
            rest = item[result.end():]
            if rest == "":
                return
            return self.token_type(rest)
        result = re.search("^[0-9]+", item)
        if result is not None and 0 <= result.group(0).isnumeric() <= 32767:
            self.int_val(int(result.group(0)))
            rest = item[result.end():]
            if rest == "":
                return
            return self.token_type(rest)
        result = re.search("^(/|{|}|\.|\^|,|#|;|\+|-|\*|&|\||<|>|=|~|\(|\)|\[|\])", item)
        if result is not None:
            rest = item[result.end():]
            result = result.group(0)
            if result == "<":
                result = "&lt;"
            if result == ">":
                result = "&gt;"
            if result == "\"":
                result = "&quot;"
            if result == "&":
                result = "&amp;"
            self.symbol(result)
            if rest == "":
                return
            return self.token_type(rest)
        result = re.search("^(class|method|function|constructor|int|boolean|char|void|var|static|field|let|do)", item)
        if result is not None:
            rest = item[result.end():]
            if rest == "":
                self.keyword(result.group(0))
                return
        result = re.search("^(if|else|while|return|true|false|null|this)", item)
        if result is not None:
            rest = item[result.end():]
            if rest == "":
                self.keyword(result.group(0))
                return
            res = re.search("^[a-zA-Z_]+", rest)
            if res is None:
                self.keyword(result.group(0))
                return self.token_type(rest)
        result = re.search("^[a-zA-Z_][a-zA-Z_0-9]*", item)
        if result is not None:
            self.identifier(result.group(0))
            rest = item[result.end():]
            if rest == "":
                return
            return self.token_type(rest)

    def keyword(self, string):
        """
        Returns:
        str: the keyword which is the current token.
        Should be called only when token_type() is "KEYWORD".
        Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT",
        "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO",
        "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        self.token_list.append("<keyword> " + string + " </keyword>")

    def symbol(self, string) -> None:
        """
        Returns:
        str: the character which is the current token.
        Should be called only when token_type() is "SYMBOL".
        """
        self.token_list.append("<symbol> " + string + " </symbol>")

    def identifier(self, string) -> None:
        """
        Returns:
        str: the identifier which is the current token.
        Should be called only when token_type() is "IDENTIFIER".
        """
        self.token_list.append("<identifier> " + string + " </identifier>")

    def int_val(self, num) -> None:
        """
        Returns:
        str: the integer value of the current token.
        Should be called only when token_type() is "INT_CONST".
        """
        self.token_list.append("<integerConstant> " + str(num) + " </integerConstant>")

    def string_val(self, string) -> None:
        """
        Returns:
        str: the string value of the current token, without the double
        quotes. Should be called only when token_type() is "STRING_CONST".
        """
        self.token_list.append("<stringConstant> " + string + " </stringConstant>")
