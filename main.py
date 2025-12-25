import sys
from core.interpreter import interpret_program
from core.errors import ContextualError, SourceLocation
from core.formatters import ErrorFormatter


def main():
    """Main entry point for Hausalang interpreter.

    Reads a .ha file, interprets it, and handles any errors that occur.
    Errors are formatted using ErrorFormatter for better readability.

    Exit codes:
      0: Success
      1: User error (syntax, runtime, file not found, etc.)
      2: Internal/system error
    """
    if len(sys.argv) < 2:
        print("Kuskure: Babu fayil da aka bayar")
        return 1

    filename = sys.argv[1]

    if not filename.endswith(".ha"):
        print("Kuskure: Fayil dole ya kasance .ha")
        return 1

    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()
            interpret_program(code)
        return 0  # Success

    except ContextualError as e:
        """Handle ContextualError with path resolution and pretty formatting."""
        # Resolve file path in error location (from "<input>" to actual filename)
        if e.location.file_path == "<input>":
            # Create new location with resolved filename
            resolved_location = SourceLocation(
                file_path=filename,
                line=e.location.line,
                column=e.location.column,
                end_line=e.location.end_line,
                end_column=e.location.end_column,
            )

            # Create new error with updated location (immutable pattern)
            resolved_error = ContextualError(
                kind=e.kind,
                message=e.message,
                location=resolved_location,
                source=e.source,
                context_frames=e.context_frames,
                tags=e.tags,
                help=e.help,
                timestamp=e.timestamp,
                error_id=e.error_id,
            )
        else:
            # Path already resolved (shouldn't happen, but handle gracefully)
            resolved_error = e

        # Format and print error to stderr
        formatter = ErrorFormatter(use_colors=True)
        error_output = formatter.pretty(resolved_error)
        print(error_output, file=sys.stderr)
        return 1

    except FileNotFoundError:
        print("Kuskure: Ba a samu fayil ba", file=sys.stderr)
        return 1

    except Exception as e:
        # Unexpected error type (shouldn't happen with new error system)
        print(f"Kuskure: Internal error: {type(e).__name__}: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
