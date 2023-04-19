"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """
    token_list = []
    split_token_list = []
    current_token = 0
    end_lines = 0
    tab = ""
    output = None

    def __init__(self, tokens, output_stream: typing.TextIO) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param tokens: list of tokens.
        :param output_stream: The output stream.
        """
        self.token_list = tokens
        self.split_token_list = []
        for token in self.token_list:
            self.split_token_list.append(token.split(" "))
        self.current_token = 0
        self.end_lines = len(tokens)
        self.output = output_stream

        self.compile_class()

    def get_next_token(self):
        """

        """
        self.current_token += 1

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.output.write("<class>" + "\n")
        # print("<class>")
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # class
        # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # class name
        # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # {
        # print(self.tab + self.token_list[self.current_token])
        while True:
            # print(self.split_token_list[self.current_token + 1][1])
            if self.split_token_list[self.current_token + 1][1] == "}":
                break
            if self.split_token_list[self.current_token + 1][1] == "field" or \
                    self.split_token_list[self.current_token + 1][1] == "static":
                self.compile_class_var_dec()
            elif self.split_token_list[self.current_token + 1][1] == "function" or \
                    self.split_token_list[self.current_token + 1][1] == "method" or \
                    self.split_token_list[self.current_token + 1][1] == "constructor":
                self.compile_subroutine()
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # }
        # print(self.tab + self.token_list[self.current_token])
        self.output.write("</class>" + "\n")
        # print("</class>")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.output.write("<classVarDec>" + "\n")
        # print("<classVarDec>")
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # static
        # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # int | class name
        # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # var name
        # print(self.tab + self.token_list[self.current_token])
        while True:
            if self.split_token_list[self.current_token + 1][1] == ";":
                break
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # ,
            # print(self.tab + self.token_list[self.current_token])
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # var name
            # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # ;
        # print(self.tab + self.token_list[self.current_token])
        self.output.write("</classVarDec>" + "\n")
        # print("</classVarDec>")

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        self.output.write("<subroutineDec>" + "\n")
        # print("<subroutineDec>")
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # constructor | method
        # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # void | type
        # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # subroutine name
        # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # (
        # print(self.tab + self.token_list[self.current_token])
        self.compile_parameter_list() # parameter list
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # )
        # print(self.tab + self.token_list[self.current_token])
        self.output.write("<subroutineBody>" + "\n")
        # print("<subroutineBody>")
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # {
        # print(self.tab + self.token_list[self.current_token])
        if self.split_token_list[self.current_token + 1][1] != "}":
            while True:
                if self.split_token_list[self.current_token + 1][1] == "var":
                    self.compile_var_dec() # varDec
                    continue
                break
            while True:
                if self.split_token_list[self.current_token + 1][1] != "}":
                    self.compile_statements() # statements
                break
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # }
        # print(self.tab + self.token_list[self.current_token])
        self.output.write("</subroutineBody>" + "\n")
        # print("</subroutineBody>")
        self.output.write("</subroutineDec>" + "\n")
        # print("</subroutineDec>")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        self.output.write("<parameterList>" + "\n")
        # print("<parameterList>")
        while True:
            # print(self.split_token_list[self.current_token + 1][1])
            if self.split_token_list[self.current_token + 1][1] == ")":
                break
            if self.split_token_list[self.current_token + 1][1] == ",":
                self.get_next_token()
                self.output.write(self.tab + self.token_list[self.current_token] + "\n") # ,
                # print(self.tab + self.token_list[self.current_token])
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # type
            # print(self.tab + self.token_list[self.current_token])
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # var name
            # print(self.tab + self.token_list[self.current_token])
        self.output.write("</parameterList>" + "\n")
        # print("</parameterList>")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.output.write("<varDec>" + "\n")
        # print("<varDec>")
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # var
        # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # type
        # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # var name
        # print(self.tab + self.token_list[self.current_token])
        while True:
            if self.split_token_list[self.current_token + 1][1] == ";":
                break
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # ,
            # print(self.tab + self.token_list[self.current_token])
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # var name
            # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # ;
        # print(self.tab + self.token_list[self.current_token])
        self.output.write("</varDec>" + "\n")
        # print("</varDec>")


    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        self.output.write("<statements>" + "\n")
        # print("<statements>")
        while True:
            if self.split_token_list[self.current_token + 1][1] == "}":
                break
            if self.split_token_list[self.current_token + 1][1] == "let":
                self.compile_let()
            elif self.split_token_list[self.current_token + 1][1] == "if":
                self.compile_if()
            elif self.split_token_list[self.current_token + 1][1] == "while":
                self.compile_while()
            elif self.split_token_list[self.current_token + 1][1] == "do":
                self.compile_do()
            elif self.split_token_list[self.current_token + 1][1] == "return":
                self.compile_return()
        self.output.write("</statements>" + "\n")
        # print("</statements>")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.output.write("<letStatement>" + "\n")
        # print("<letStatement>")
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # let
        # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # var name
        # print(self.tab + self.token_list[self.current_token])
        if self.split_token_list[self.current_token + 1][1] == "[":
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # [
            # print(self.tab + self.token_list[self.current_token])
            self.compile_expression() # expression
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # ]
            # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # =
        # print(self.tab + self.token_list[self.current_token])
        self.compile_expression()
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # ;
        # print(self.tab + self.token_list[self.current_token])
        self.output.write("</letStatement>" + "\n")
        # print("</letStatement>")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.output.write("<ifStatement>" + "\n")
        # print("<ifStatement>")
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # if
        # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # (
        # print(self.tab + self.token_list[self.current_token])
        self.compile_expression() # expression
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # )
        # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # {
        # print(self.tab + self.token_list[self.current_token])
        self.compile_statements() # statements
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # }
        # print(self.tab + self.token_list[self.current_token])
        if self.split_token_list[self.current_token + 1][1] == "else":
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # else
            # print(self.tab + self.token_list[self.current_token])
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # {
            # print(self.tab + self.token_list[self.current_token])
            self.compile_statements() # statements
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # }
            # print(self.tab + self.token_list[self.current_token])
        self.output.write("</ifStatement>" + "\n")
        # print("</ifStatement>")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.output.write("<whileStatement>" + "\n")
        # print("<whileStatement>")
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # while
        # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # (
        # print(self.tab + self.token_list[self.current_token])
        self.compile_expression() # expression
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # )
        # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # {
        # print(self.tab + self.token_list[self.current_token])
        self.compile_statements() # statements
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # }
        # print(self.tab + self.token_list[self.current_token])
        self.output.write("</whileStatement>" + "\n")
        # print("</whileStatement>")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.output.write("<doStatement>" + "\n")
        # print("<doStatement>")
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # do
        # print(self.tab + self.token_list[self.current_token])
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # name
        # print(self.tab + self.token_list[self.current_token])
        if self.split_token_list[self.current_token + 1][1] == "(":
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # (
            # print(self.tab + self.token_list[self.current_token])
            self.compile_expression_list()
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # )
            # print(self.tab + self.token_list[self.current_token])
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # ;
            # print(self.tab + self.token_list[self.current_token])
            self.output.write("</doStatement>" + "\n")
            # print("</doStatement>")
            return
        if self.split_token_list[self.current_token + 1][1] == ".":
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # .
            # print(self.tab + self.token_list[self.current_token])
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # subroutine name
            # print(self.tab + self.token_list[self.current_token])
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # (
            # print(self.tab + self.token_list[self.current_token])
            self.compile_expression_list()
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # )
            # print(self.tab + self.token_list[self.current_token])
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # ;
            # print(self.tab + self.token_list[self.current_token])
            self.output.write("</doStatement>" + "\n")
            # print("</doStatement>")
            return

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.output.write("<returnStatement>" + "\n")
        # print("<returnStatement>")
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # return
        # print(self.tab + self.token_list[self.current_token])
        if self.split_token_list[self.current_token + 1][1] != ";":
            self.compile_expression()
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # ;
        # print(self.tab + self.token_list[self.current_token])
        self.output.write("</returnStatement>" + "\n")
        # print("</returnStatement>")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.output.write("<expression>" + "\n")
        # print("<expression>")
        self.compile_term() # term
        while True:
            if self.split_token_list[self.current_token + 1][1] != "+" and \
                    self.split_token_list[self.current_token + 1][1] != "-" and \
                    self.split_token_list[self.current_token + 1][1] != "*" and \
                    self.split_token_list[self.current_token + 1][1] != "/" and \
                    self.split_token_list[self.current_token + 1][1] != "&amp;" and \
                    self.split_token_list[self.current_token + 1][1] != "|" and \
                    self.split_token_list[self.current_token + 1][1] != "&lt;" and \
                    self.split_token_list[self.current_token + 1][1] != "&gt;" and \
                    self.split_token_list[self.current_token + 1][1] != "=":
                break
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # op
            # print(self.tab + self.token_list[self.current_token])
            self.compile_term() # term
        self.output.write("</expression>" + "\n")
        # print("</expression>")

    def compile_term(self) -> None:
        """Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        self.output.write("<term>" + "\n")
        # print("<term>")
        self.get_next_token()
        self.output.write(self.tab + self.token_list[self.current_token] + "\n") # var name
        # print(self.tab + self.token_list[self.current_token])
        if self.split_token_list[self.current_token][1] == "(": # ( expression )
            self.compile_expression() # expression
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # )
            # print(self.tab + self.token_list[self.current_token])
            self.output.write("</term>" + "\n")
            # print("</term>")
            return
        if self.split_token_list[self.current_token + 1][1] == "[":
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # [
            # print(self.tab + self.token_list[self.current_token])
            self.compile_expression() # expression
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # ]
            # print(self.tab + self.token_list[self.current_token])
            self.output.write("</term>" + "\n")
            # print("</term>")
            return
        if self.split_token_list[self.current_token][1] == "-" or \
                self.split_token_list[self.current_token][1] == "~" or \
                self.split_token_list[self.current_token][1] == "^" or \
                self.split_token_list[self.current_token][1] == "#":
            # unaryOp
            self.compile_term() # term
            self.output.write("</term>" + "\n")
            # print("</term>")
            return
        if self.split_token_list[self.current_token + 1][1] == "(": # subroutine call (
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # (
            # print(self.tab + self.token_list[self.current_token])
            self.compile_expression_list()
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # )
            # print(self.tab + self.token_list[self.current_token])
        if self.split_token_list[self.current_token + 1][1] == ".": # subroutine call .
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # .
            # print(self.tab + self.token_list[self.current_token])
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # subroutine name
            # print(self.tab + self.token_list[self.current_token])
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # (
            # print(self.tab + self.token_list[self.current_token])
            self.compile_expression_list()
            self.get_next_token()
            self.output.write(self.tab + self.token_list[self.current_token] + "\n") # )
            # print(self.tab + self.token_list[self.current_token])
        self.output.write("</term>" + "\n")
        # print("</term>")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.output.write("<expressionList>" + "\n")
        # print("<expressionList>")
        if self.split_token_list[self.current_token + 1][1] != ")":
            self.compile_expression() # expression
            while True:
                if self.split_token_list[self.current_token + 1][1] != ",":
                    break
                self.get_next_token()
                self.output.write(self.tab + self.token_list[self.current_token] + "\n") # ,
                self.compile_expression()
        self.output.write("</expressionList>" + "\n")
