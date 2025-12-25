"""
Recursive-Descent Parser for Hausalang

This module implements a formal recursive-descent parser that consumes tokens
from the lexer and produces an Abstract Syntax Tree (AST).

Key Design Principles:
- Each parsing function handles one grammatical construct
- Token consumption is explicit and safe (check before advancing)
- Error messages include line and column numbers
- AST nodes are immutable NamedTuples for clarity
"""

from typing import List, Optional, Union
from dataclasses import dataclass

from core.lexer import Token


# ============================================================================
# AST Node Definitions
# ============================================================================


@dataclass(frozen=True)
class ASTNode:
    """Base class for all AST nodes."""

    line: int
    column: int


@dataclass(frozen=True)
class Program(ASTNode):
    """Root node: represents the entire program."""

    statements: List["Statement"]


# Expressions (produce values)
@dataclass(frozen=True)
class Number(ASTNode):
    """Numeric literal: 42, 3.14"""

    value: Union[int, float]


@dataclass(frozen=True)
class String(ASTNode):
    """String literal: "hello" """

    value: str


@dataclass(frozen=True)
class Identifier(ASTNode):
    """Variable or function name: x, suna, greet"""

    name: str


@dataclass(frozen=True)
class BinaryOp(ASTNode):
    """Binary operation: x + y, x > 5, "a" + "b" """

    left: "Expression"
    operator: str  # "+", "-", "*", "/", "==", "!=", ">", "<", ">=", "<="
    right: "Expression"


@dataclass(frozen=True)
class FunctionCall(ASTNode):
    """Function call: greet("name"), add(1, 2)"""

    name: str
    arguments: List["Expression"]


# Statements (do not produce values; cause side effects)
@dataclass(frozen=True)
class Assignment(ASTNode):
    """Variable assignment: x = 5 + 3"""

    name: str
    value: "Expression"


@dataclass(frozen=True)
class Print(ASTNode):
    """Print statement: rubuta x + 1"""

    expression: "Expression"


@dataclass(frozen=True)
class Return(ASTNode):
    """Return statement: mayar x + 10"""

    expression: "Expression"


@dataclass(frozen=True)
class If(ASTNode):
    """If/else block.

    idan x > 5:
        rubuta "big"
    in ba haka ba:
        rubuta "small"
    """

    condition: "Expression"
    then_body: List["Statement"]
    else_body: Optional[List["Statement"]] = None


@dataclass(frozen=True)
class While(ASTNode):
    """While loop.

    kadai x < 10:
        rubuta x
        x = x + 1
    """

    condition: "Expression"
    body: List["Statement"]


@dataclass(frozen=True)
class For(ASTNode):
    """For loop (will be rewritten to while loop + assignment).

    don i = 0 zuwa 10 ta 2:
        rubuta i

    Internal representation:
      var: variable name
      start: starting value expression
      end: ending value expression
      direction: "ascending" (zuwa) or "descending" (ba)
      step: optional step value expression (default: None → 1)
      body: list of statements to execute
    """

    var: str  # Loop variable
    start: "Expression"  # Start value
    end: "Expression"  # End value
    direction: str  # "ascending" or "descending"
    body: List["Statement"]  # Loop body
    step: Optional["Expression"] = None  # Optional step (default: 1)


@dataclass(frozen=True)
class Function(ASTNode):
    """Function definition.

    aiki greet(name):
        rubuta "hi " + name
        mayar 0
    """

    name: str
    parameters: List[str]
    body: List["Statement"]


@dataclass(frozen=True)
class ExpressionStatement(ASTNode):
    """Expression used as a statement (e.g., function call).

    Examples:
        greet("Ali")
        x + y  # expression with side effects
    """

    expression: "Expression"


# Type aliases for clarity
Expression = Union[Number, String, Identifier, BinaryOp, FunctionCall]
Statement = Union[
    Assignment, Print, Return, If, While, For, Function, ExpressionStatement
]


# ============================================================================
# Parser Implementation
# ============================================================================


class Parser:
    """Recursive-descent parser for Hausalang.

    This parser consumes a list of tokens and produces an AST.
    Each method corresponds to a grammatical rule.
    """

    def __init__(self, tokens: List[Token]):
        """Initialize parser with a token stream.

        Args:
            tokens: List of Token objects from the lexer.
        """
        self.tokens = tokens
        self.current = 0  # Index of current token

    # ========================================================================
    # Token Management
    # ========================================================================

    def peek(self) -> Optional[Token]:
        """Return the current token without advancing."""
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None

    def advance(self) -> Token:
        """Consume and return the current token."""
        token = self.peek()
        if token:
            self.current += 1
        return token

    def expect(self, token_type: str, message: str = "") -> Token:
        """Assert the current token is of the given type, then consume it.

        Raises:
            SyntaxError: If the token type doesn't match.
        """
        token = self.peek()
        if not token or token.type != token_type:
            tok_str = f"{token.type}({token.value})" if token else "EOF"
            error_msg = message or f"Expected {token_type}, got {tok_str}"
            self._error(error_msg, token)
        return self.advance()

    def match(self, *token_types: str) -> bool:
        """Check if current token matches any of the given types."""
        token = self.peek()
        return token is not None and token.type in token_types

    def consume_newlines(self) -> None:
        """Skip any NEWLINE tokens."""
        while self.match("NEWLINE"):
            self.advance()

    def _error(self, message: str, token: Optional[Token] = None) -> None:
        """Raise a SyntaxError with location info."""
        if token:
            raise SyntaxError(f"Line {token.line}, Column {token.column}: {message}")
        else:
            raise SyntaxError(message)

    # ========================================================================
    # Main Entry Point
    # ========================================================================

    def parse(self) -> Program:
        """Parse a complete program.

        Grammar:
            program = statement*

        Returns:
            A Program node containing all statements.
        """
        statements = []
        self.consume_newlines()

        while not self.match("EOF"):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.consume_newlines()

        return Program(
            statements=statements,
            line=self.tokens[0].line if self.tokens else 1,
            column=0,
        )

    # ========================================================================
    # Statement Parsing
    # ========================================================================

    def parse_statement(self) -> Optional[Statement]:
        """Parse a single statement.

        Grammar:
            statement = assignment
                      | print_stmt
                      | return_stmt
                      | if_stmt
                      | while_stmt
                      | for_stmt
                      | function_def
                      | expression_stmt (function call)

        Returns:
            A Statement node, or None if no valid statement found.
        """
        token = self.peek()
        if not token:
            return None

        # Function definition: aiki name(params):
        if token.type == "KEYWORD_FUNCTION":
            return self.parse_function()

        # If statement: idan condition:
        if token.type == "KEYWORD_IF":
            return self.parse_if()

        # While loop: kadai condition:
        if token.type == "KEYWORD_WHILE":
            return self.parse_while()

        # For loop: don var = start direction end:
        if token.type == "KEYWORD_FOR":
            return self.parse_for()

        # Return statement: mayar expr
        if token.type == "KEYWORD_RETURN":
            return self.parse_return()

        # Print statement: rubuta expr
        if token.type == "KEYWORD_PRINT":
            return self.parse_print()

        # Assignment or function call: name = expr OR name(args)
        if token.type == "IDENTIFIER":
            # Lookahead: is there an = operator?
            if (
                self.current + 1 < len(self.tokens)
                and self.tokens[self.current + 1].type == "OPERATOR"
                and self.tokens[self.current + 1].value == "="
            ):
                return self.parse_assignment()

            # Otherwise, parse as an expression statement (e.g., function call)
            # This allows statements like: greet(name)
            expr = self.parse_expression()
            return ExpressionStatement(
                expression=expr, line=token.line, column=token.column
            )

        # If none matched, error
        self._error(f"Unexpected token: {token.type}({token.value})", token)

    def parse_assignment(self) -> Assignment:
        """Parse a variable assignment.

        Grammar:
            assignment = IDENTIFIER "=" expression

        Example:
            x = 5 + 3
        """
        name_token = self.expect("IDENTIFIER")
        name = name_token.value

        # Expect = operator
        equals_token = self.peek()
        if (
            not equals_token
            or equals_token.type != "OPERATOR"
            or equals_token.value != "="
        ):
            self._error('Expected "=" in assignment', equals_token)
        self.advance()

        expr = self.parse_expression()

        return Assignment(
            name=name, value=expr, line=name_token.line, column=name_token.column
        )

    def parse_print(self) -> Print:
        """Parse a print statement.

        Grammar:
            print = "rubuta" expression

        Example:
            rubuta x + 1
            rubuta "hello"
        """
        token = self.expect("KEYWORD_PRINT", 'Expected "rubuta"')
        expr = self.parse_expression()

        return Print(expression=expr, line=token.line, column=token.column)

    def parse_return(self) -> Return:
        """Parse a return statement.

        Grammar:
            return = "mayar" expression

        Example:
            mayar 42
            mayar x + y
        """
        token = self.expect("KEYWORD_RETURN", 'Expected "mayar"')
        expr = self.parse_expression()

        return Return(expression=expr, line=token.line, column=token.column)

    def parse_if(self) -> If:
        """Parse an if/else statement.

        Grammar:
            if = "idan" expression ":" INDENT statement* DEDENT
                 ["in ba haka ba" ":" INDENT statement* DEDENT]

        Design Note:
            In Hausalang, blocks are denoted by indentation (INDENT/DEDENT tokens).
            The lexer produces these tokens to track scope.
        """
        if_token = self.expect("KEYWORD_IF", 'Expected "idan"')

        # Parse condition (comparison expression)
        condition = self.parse_expression()

        # Expect colon
        colon_token = self.peek()
        if (
            not colon_token
            or colon_token.type != "OPERATOR"
            or colon_token.value != ":"
        ):
            self._error('Expected ":" after if condition', colon_token)
        self.advance()

        # Expect NEWLINE and INDENT
        self.consume_newlines()
        self.expect("INDENT", "Expected INDENT after if block")

        # Parse then-body (statements until DEDENT)
        then_body = self.parse_block()

        # Expect DEDENT
        self.expect("DEDENT", "Expected DEDENT after if block")

        # Check for else clause
        else_body = None
        if self.match("KEYWORD_ELSE"):
            # "in ba haka ba" is tokenized as 4 separate KEYWORD_ELSE tokens
            # Consume them: in, ba, haka, ba
            for _ in range(4):
                if self.match("KEYWORD_ELSE"):
                    self.advance()
                else:
                    break

            # Expect colon
            colon_token = self.peek()
            if (
                not colon_token
                or colon_token.type != "OPERATOR"
                or colon_token.value != ":"
            ):
                self._error('Expected ":" after else', colon_token)
            self.advance()

            # Expect NEWLINE and INDENT
            self.consume_newlines()
            self.expect("INDENT", "Expected INDENT after else block")

            # Parse else-body
            else_body = self.parse_block()

            # Expect DEDENT
            self.expect("DEDENT", "Expected DEDENT after else block")

        return If(
            condition=condition,
            then_body=then_body,
            else_body=else_body,
            line=if_token.line,
            column=if_token.column,
        )

    def parse_while(self) -> While:
        """Parse a while loop.

        Grammar:
            while = "kadai" expression ":" INDENT statement* DEDENT

        Design Note:
            While loops follow the same indentation-based block syntax as if statements.
            The condition is re-evaluated on each iteration.
        """
        while_token = self.expect("KEYWORD_WHILE", 'Expected "kadai"')

        # Parse condition (comparison expression)
        condition = self.parse_expression()

        # Expect colon
        colon_token = self.peek()
        if (
            not colon_token
            or colon_token.type != "OPERATOR"
            or colon_token.value != ":"
        ):
            self._error('Expected ":" after while condition', colon_token)
        self.advance()

        # Expect NEWLINE and INDENT
        self.consume_newlines()
        self.expect("INDENT", "Expected INDENT after while block")

        # Parse loop body (statements until DEDENT)
        body = self.parse_block()

        # Expect DEDENT
        self.expect("DEDENT", "Expected DEDENT after while block")

        return While(
            condition=condition,
            body=body,
            line=while_token.line,
            column=while_token.column,
        )

    def parse_for(self) -> For:
        """Parse a for loop.

        Grammar:
            for = "don" IDENTIFIER "=" expression ("zuwa"|"ba") expression
                  ["ta" expression] ":" INDENT statement* DEDENT

        Examples:
            don i = 0 zuwa 10:              (ascending 0 to <10)
            don i = 0 zuwa 10 ta 2:         (ascending 0 to <10, step 2)
            don i = 10 ba 0:                (descending 10 to >0)

        Design Note:
            For loops are internally rewritten to assignment + while loop.
            The interpreter converts this to:
                var = start
                kadai (condition based on direction):
                    body
                    var = var (+/- step)
        """
        for_token = self.expect("KEYWORD_FOR", 'Expected "don"')

        # Parse loop variable name
        var_token = self.expect("IDENTIFIER", "Expected variable name after don")
        var_name = var_token.value

        # Expect = operator
        equals_token = self.peek()
        if (
            not equals_token
            or equals_token.type != "OPERATOR"
            or equals_token.value != "="
        ):
            self._error('Expected "=" after variable name', equals_token)
        self.advance()

        # Parse start value (expression)
        start_expr = self.parse_expression()

        # Check direction: zuwa (ascending) or ba (descending)
        direction_token = self.peek()
        if not direction_token:
            self._error("Expected direction (zuwa or ba) in for loop", direction_token)

        if direction_token.type == "KEYWORD_TO":  # zuwa - ascending
            direction = "ascending"
            self.advance()
        elif direction_token.type == "KEYWORD_ELSE" and direction_token.value == "ba":
            # ba context-sensitive: else clause vs descending
            # In for loop context, it's descending
            direction = "descending"
            self.advance()
        else:
            self._error('Expected "zuwa" or "ba" in for loop', direction_token)

        # Parse end value (expression)
        end_expr = self.parse_expression()

        # Check for optional step
        step_expr = None
        if self.match("KEYWORD_STEP"):  # ta - step
            self.advance()
            step_expr = self.parse_expression()

        # Expect colon
        colon_token = self.peek()
        if (
            not colon_token
            or colon_token.type != "OPERATOR"
            or colon_token.value != ":"
        ):
            self._error('Expected ":" after for declaration', colon_token)
        self.advance()

        # Expect NEWLINE and INDENT
        self.consume_newlines()
        self.expect("INDENT", "Expected INDENT after for block")

        # Parse loop body (statements until DEDENT)
        body = self.parse_block()

        # Expect DEDENT
        self.expect("DEDENT", "Expected DEDENT after for block")

        return For(
            var=var_name,
            start=start_expr,
            end=end_expr,
            direction=direction,
            body=body,
            step=step_expr,
            line=for_token.line,
            column=for_token.column,
        )

    def parse_function(self) -> Function:
        """Parse a function definition.

        Grammar:
            function = "aiki" IDENTIFIER "(" params ")" ":" INDENT statement* DEDENT

        Example:
            aiki greet(name):
                rubuta "hi " + name
                mayar 0
        """
        func_token = self.expect("KEYWORD_FUNCTION", 'Expected "aiki"')

        # Function name
        name_token = self.expect("IDENTIFIER", "Expected function name")
        name = name_token.value

        # Opening paren
        paren_token = self.peek()
        if (
            not paren_token
            or paren_token.type != "OPERATOR"
            or paren_token.value != "("
        ):
            self._error("Expected '(' after function name", paren_token)
        self.advance()

        # Parameters (comma-separated identifiers)
        parameters = []
        if not self.match("OPERATOR") or self.peek().value != ")":
            while True:
                param_token = self.expect("IDENTIFIER", "Expected parameter name")
                parameters.append(param_token.value)

                # Check for comma (another parameter) or )
                if self.match("OPERATOR"):
                    if self.peek().value == ",":
                        self.advance()  # consume comma
                        continue
                    elif self.peek().value == ")":
                        break
                self._error("Expected ',' or ')' in parameter list")

        # Closing paren
        close_paren_token = self.peek()
        if (
            not close_paren_token
            or close_paren_token.type != "OPERATOR"
            or close_paren_token.value != ")"
        ):
            self._error("Expected ')' after parameters", close_paren_token)
        self.advance()

        # Colon
        colon_token = self.peek()
        if (
            not colon_token
            or colon_token.type != "OPERATOR"
            or colon_token.value != ":"
        ):
            self._error('Expected ":" after function signature', colon_token)
        self.advance()

        # NEWLINE and INDENT
        self.consume_newlines()
        self.expect("INDENT", "Expected INDENT after function definition")

        # Function body
        body = self.parse_block()

        # DEDENT
        self.expect("DEDENT", "Expected DEDENT after function body")

        return Function(
            name=name,
            parameters=parameters,
            body=body,
            line=func_token.line,
            column=func_token.column,
        )

    def parse_block(self) -> List[Statement]:
        """Parse a block of statements (until DEDENT).

        Used for: function bodies, if/else bodies.

        Returns:
            A list of Statement nodes.
        """
        statements = []
        self.consume_newlines()

        # Continue parsing until we hit DEDENT or EOF
        while self.peek() and self.peek().type != "DEDENT":
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.consume_newlines()

        return statements

    # ========================================================================
    # Expression Parsing
    # ========================================================================

    def parse_expression(self) -> Expression:
        """Parse an expression (handles operator precedence).

        Grammar:
            expression = comparison

        This delegates to comparison, which handles lower-precedence ops.
        Precedence (low to high):
            1. Comparison: ==, !=, >, <, >=, <=
            2. Additive: +, -
            3. Multiplicative: *, /
            4. Primary: literals, identifiers, parenthesized expressions
        """
        return self.parse_comparison()

    def parse_comparison(self) -> Expression:
        """Parse comparison operators (==, !=, >, <, >=, <=).

        Grammar:
            comparison = additive ((==|!=|>|<|>=|<=) additive)*

        Example:
            x > 5
            a == b
        """
        left = self.parse_additive()

        while self.match("OPERATOR"):
            op_token = self.peek()
            if op_token.value in ("==", "!=", ">", "<", ">=", "<="):
                op = op_token.value
                self.advance()
                right = self.parse_additive()
                left = BinaryOp(
                    left=left,
                    operator=op,
                    right=right,
                    line=op_token.line,
                    column=op_token.column,
                )
            else:
                break

        return left

    def parse_additive(self) -> Expression:
        """Parse addition and subtraction.

        Grammar:
            additive = multiplicative ((+|-) multiplicative)*

        Example:
            x + 5
            a - b + c
        """
        left = self.parse_multiplicative()

        while self.match("OPERATOR"):
            op_token = self.peek()
            if op_token.value in ("+", "-"):
                op = op_token.value
                self.advance()
                right = self.parse_multiplicative()
                left = BinaryOp(
                    left=left,
                    operator=op,
                    right=right,
                    line=op_token.line,
                    column=op_token.column,
                )
            else:
                break

        return left

    def parse_multiplicative(self) -> Expression:
        """Parse multiplication and division.

        Grammar:
            multiplicative = primary ((*|/) primary)*

        Example:
            x * 2
            a / b * c
        """
        left = self.parse_primary()

        while self.match("OPERATOR"):
            op_token = self.peek()
            if op_token.value in ("*", "/"):
                op = op_token.value
                self.advance()
                right = self.parse_primary()
                left = BinaryOp(
                    left=left,
                    operator=op,
                    right=right,
                    line=op_token.line,
                    column=op_token.column,
                )
            else:
                break

        return left

    def parse_primary(self) -> Expression:
        """Parse primary expressions (lowest precedence, highest binding).

        Grammar:
            primary = NUMBER
                    | STRING
                    | IDENTIFIER [ "(" arguments ")" ]
                    | "(" expression ")"

        Examples:
            42
            "hello"
            x
            greet("name")
            (x + y)
        """
        token = self.peek()

        if not token:
            self._error("Unexpected end of input")

        # Number literal
        if token.type == "NUMBER":
            self.advance()
            # Parse as int or float
            if "." in token.value:
                value = float(token.value)
            else:
                value = int(token.value)
            return Number(value=value, line=token.line, column=token.column)

        # String literal
        if token.type == "STRING":
            self.advance()
            # Remove surrounding quotes
            value = token.value[1:-1]
            return String(value=value, line=token.line, column=token.column)

        # Identifier or function call
        if token.type == "IDENTIFIER":
            name = token.value
            self.advance()

            # Check for function call: name(args)
            if self.match("OPERATOR"):
                next_tok = self.peek()
                if next_tok.value == "(":
                    self.advance()  # consume (

                    # Parse arguments
                    arguments = []
                    if not (self.match("OPERATOR") and self.peek().value == ")"):
                        while True:
                            arg = self.parse_expression()
                            arguments.append(arg)

                            # Check for comma or )
                            if self.match("OPERATOR"):
                                if self.peek().value == ",":
                                    self.advance()
                                    continue
                                elif self.peek().value == ")":
                                    break
                            else:
                                self._error("Expected ',' or ')' in function call")

                    # Closing paren
                    close_paren = self.expect(
                        "OPERATOR", "Expected ')' after function arguments"
                    )
                    if close_paren.value != ")":
                        self._error("Expected ')'")

                    return FunctionCall(
                        name=name,
                        arguments=arguments,
                        line=token.line,
                        column=token.column,
                    )

            # Just an identifier
            return Identifier(name=name, line=token.line, column=token.column)

        # Parenthesized expression
        if token.type == "OPERATOR" and token.value == "(":
            self.advance()  # consume (
            expr = self.parse_expression()
            close_paren = self.peek()
            if not close_paren or close_paren.value != ")":
                self._error("Expected ')' after expression", close_paren)
            self.advance()  # consume )
            return expr

        # Unknown token
        self._error(f"Unexpected token: {token.type}({token.value})", token)


# ============================================================================
# Public API
# ============================================================================


def parse(tokens: List[Token]) -> Program:
    """Parse a list of tokens and produce an AST.

    Args:
        tokens: A list of Token objects from the lexer.

    Returns:
        A Program node (the root of the AST).

    Raises:
        SyntaxError: If the tokens do not form a valid program.
    """
    parser = Parser(tokens)
    return parser.parse()
