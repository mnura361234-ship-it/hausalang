#!/usr/bin/env python3
"""Clean interpreter.py - keep only the new AST-based content"""

new_content = '''"""
AST Interpreter for Hausalang

This module implements an interpreter that walks the Abstract Syntax Tree (AST)
produced by the parser and executes the program.

Key Design:
- Environment class manages variable scope and function definitions
- Interpreter class walks AST nodes recursively
- No raw token or line-based execution; pure AST-driven
"""

from typing import Any, Dict, List, Optional

from core import parser
from core.lexer import tokenize_program


class ReturnValue(Exception):
    """Exception used to implement return statements.

    When a return statement is executed, we raise this exception to unwind
    the call stack back to the function call site.
    """
    def __init__(self, value: Any):
        self.value = value
        super().__init__()


class Environment:
    """Manages variable scope and function definitions.

    An environment maps variable names to values and function names to
    function definitions (AST nodes). When entering a new scope (function call),
    we create a new Environment with a parent reference.
    """

    def __init__(self, parent: Optional['Environment'] = None):
        """Initialize an environment.

        Args:
            parent: The parent environment (for scope chain). None for global scope.
        """
        self.parent = parent
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, parser.Function] = {}

    def define_variable(self, name: str, value: Any) -> None:
        """Define a variable in this environment."""
        self.variables[name] = value

    def get_variable(self, name: str) -> Any:
        """Get a variable, searching parent scopes if necessary."""
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get_variable(name)
        raise NameError(f"Undefined variable: {name}")

    def define_function(self, name: str, func: parser.Function) -> None:
        """Define a function in this environment."""
        self.functions[name] = func

    def get_function(self, name: str) -> parser.Function:
        """Get a function, searching parent scopes if necessary."""
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_function(name)
        raise NameError(f"Undefined function: {name}")

    def function_exists(self, name: str) -> bool:
        """Check if a function is defined."""
        if name in self.functions:
            return True
        if self.parent:
            return self.parent.function_exists(name)
        return False


class Interpreter:
    """AST Interpreter for Hausalang.

    Walks the AST and executes each node by dispatching to specialized methods.
    """

    def __init__(self):
        """Initialize the interpreter with a global environment."""
        self.global_env = Environment()

    # ========================================================================
    # Program Execution
    # ========================================================================

    def interpret(self, program: parser.Program) -> None:
        """Execute a program (AST).

        Args:
            program: The Program node from the parser.
        """
        self.execute_program(program, self.global_env)

    def execute_program(self, program: parser.Program, env: Environment) -> None:
        """Execute all statements in a program.

        Args:
            program: The Program node.
            env: The environment for execution.
        """
        for statement in program.statements:
            self.execute_statement(statement, env)

    # ========================================================================
    # Statement Execution
    # ========================================================================

    def execute_statement(self, stmt: parser.Statement, env: Environment) -> None:
        """Execute a statement.

        Dispatches to the appropriate handler based on statement type.

        Args:
            stmt: The statement to execute.
            env: The environment for execution.
        """
        if isinstance(stmt, parser.Assignment):
            self.execute_assignment(stmt, env)

        elif isinstance(stmt, parser.Print):
            self.execute_print(stmt, env)

        elif isinstance(stmt, parser.Return):
            self.execute_return(stmt, env)

        elif isinstance(stmt, parser.If):
            self.execute_if(stmt, env)

        elif isinstance(stmt, parser.Function):
            self.execute_function_def(stmt, env)

        elif isinstance(stmt, parser.ExpressionStatement):
            # Expression statements (like function calls) are evaluated for
            # side effects but their return value is discarded
            self.eval_expression(stmt.expression, env)

        else:
            raise RuntimeError(f"Unknown statement type: {type(stmt)}")

    def execute_assignment(self, stmt: parser.Assignment, env: Environment) -> None:
        """Execute an assignment statement.

        Evaluates the expression and stores the result in the variable.

        Args:
            stmt: The Assignment statement.
            env: The environment for execution.
        """
        value = self.eval_expression(stmt.value, env)
        env.define_variable(stmt.name, value)

    def execute_print(self, stmt: parser.Print, env: Environment) -> None:
        """Execute a print statement.

        Evaluates the expression and prints the result to stdout.

        Args:
            stmt: The Print statement.
            env: The environment for execution.
        """
        value = self.eval_expression(stmt.expression, env)
        print(value, end='')

    def execute_return(self, stmt: parser.Return, env: Environment) -> None:
        """Execute a return statement.

        Raises a ReturnValue exception to unwind back to the function call.

        Args:
            stmt: The Return statement.
            env: The environment for execution.

        Raises:
            ReturnValue: Always (this is the mechanism for return).
        """
        value = self.eval_expression(stmt.expression, env)
        raise ReturnValue(value)

    def execute_if(self, stmt: parser.If, env: Environment) -> None:
        """Execute an if/else statement.

        Evaluates the condition, then executes either the then_body or else_body.

        Args:
            stmt: The If statement.
            env: The environment for execution.
        """
        condition = self.eval_expression(stmt.condition, env)

        if self.is_truthy(condition):
            # Execute then-body
            for then_stmt in stmt.then_body:
                self.execute_statement(then_stmt, env)
        elif stmt.else_body:
            # Execute else-body (if it exists)
            for else_stmt in stmt.else_body:
                self.execute_statement(else_stmt, env)

    def execute_function_def(self, stmt: parser.Function, env: Environment) -> None:
        """Execute a function definition.

        Stores the function in the environment so it can be called later.

        Args:
            stmt: The Function statement.
            env: The environment for execution.
        """
        env.define_function(stmt.name, stmt)

    # ========================================================================
    # Expression Evaluation
    # ========================================================================

    def eval_expression(self, expr: parser.Expression, env: Environment) -> Any:
        """Evaluate an expression to a value.

        Args:
            expr: The expression to evaluate.
            env: The environment for execution.

        Returns:
            The result of evaluating the expression.
        """
        if isinstance(expr, parser.Number):
            return expr.value

        elif isinstance(expr, parser.String):
            return expr.value

        elif isinstance(expr, parser.Identifier):
            return env.get_variable(expr.name)

        elif isinstance(expr, parser.BinaryOp):
            return self.eval_binary_op(expr, env)

        elif isinstance(expr, parser.FunctionCall):
            return self.eval_function_call(expr, env)

        else:
            raise RuntimeError(f"Unknown expression type: {type(expr)}")

    def eval_binary_op(self, expr: parser.BinaryOp, env: Environment) -> Any:
        """Evaluate a binary operation.

        Args:
            expr: The BinaryOp expression.
            env: The environment for execution.

        Returns:
            The result of the operation.
        """
        left = self.eval_expression(expr.left, env)
        right = self.eval_expression(expr.right, env)

        op = expr.operator

        # Arithmetic operators
        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            # Integer division if both operands are integers
            if isinstance(left, int) and isinstance(right, int):
                return left // right
            return left / right

        # Comparison operators
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        elif op == ">":
            return left > right
        elif op == "<":
            return left < right
        elif op == ">=":
            return left >= right
        elif op == "<=":
            return left <= right

        else:
            raise RuntimeError(f"Unknown operator: {op}")

    def eval_function_call(self, expr: parser.FunctionCall, env: Environment) -> Any:
        """Evaluate a function call.

        Looks up the function, evaluates the arguments, creates a new environment
        for the function, executes the function body, and returns the result.

        Args:
            expr: The FunctionCall expression.
            env: The environment for execution.

        Returns:
            The return value of the function (or None if no return statement).
        """
        # Evaluate arguments
        arg_values = [self.eval_expression(arg, env) for arg in expr.arguments]

        # Look up the function
        func = env.get_function(expr.name)

        # Check argument count
        if len(arg_values) != len(func.parameters):
            raise ValueError(
                f"Function {expr.name} expects {len(func.parameters)} arguments, "
                f"got {len(arg_values)}"
            )

        # Create a new environment for the function with current environment as parent
        func_env = Environment(parent=env)

        # Bind parameters to argument values
        for param_name, arg_value in zip(func.parameters, arg_values):
            func_env.define_variable(param_name, arg_value)

        # Execute the function body
        try:
            for stmt in func.body:
                self.execute_statement(stmt, func_env)
        except ReturnValue as ret:
            # Function returned a value
            return ret.value

        # If no return statement, return None
        return None

    # ========================================================================
    # Utilities
    # ========================================================================

    def is_truthy(self, value: Any) -> bool:
        """Determine if a value is truthy in Hausalang.

        In Hausalang:
        - False, 0, "", and None are falsy
        - Everything else is truthy

        Args:
            value: The value to test.

        Returns:
            True if the value is truthy, False otherwise.
        """
        if value is False or value is None:
            return False
        if value == 0 or value == "":
            return False
        return True


# ============================================================================
# Public API
# ============================================================================

def interpret_program(source_code: str) -> None:
    """Parse and interpret a Hausalang program.

    This is the main entry point: takes source code, lexes it, parses it to
    produce an AST, then interprets the AST.

    Args:
        source_code: The Hausalang source code as a string.

    Raises:
        SyntaxError: If the code has a syntax error.
        NameError: If a variable or function is undefined.
        ValueError: If a function is called with wrong number of arguments.
        RuntimeError: For other runtime errors.
    """
    # Lex the source code
    tokens = tokenize_program(source_code)

    # Parse tokens to produce AST
    program = parser.parse(tokens)

    # Interpret the AST
    interpreter = Interpreter()
    interpreter.interpret(program)
'''

with open("core/interpreter.py", "w") as f:
    f.write(new_content)

print("✅ Cleaned interpreter.py")
