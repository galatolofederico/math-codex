import sys
import ast
import signal
import io

def execute_program(program):
    lines = program.split("\n")
    lines[-1] = "output = "+lines[-1]+"\nprint(output)"
    program = "\n".join(lines)

    program_output = io.StringIO()
    valid_program = True
    program_halts = False
    program_error = False

    try:
        code = ast.parse(program, mode="exec")
    except:
        valid_program = False
    
    if valid_program:
        def signal_handler(signum, frame):
            raise Exception("Timed out")
        
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(1)
        old_stdout = sys.stdout 
        try:
            sys.stdout = program_output
            exec(compile(code, "", mode="exec"))
        except Exception as e:
            if str(e) == "Timed out":
                program_halts = True
            else:
                program_error = True
        finally:
            sys.stdout = old_stdout
        signal.alarm(0)

    return dict(
        valid=valid_program,
        halts=program_halts,
        error=program_error,
        output=program_output.getvalue().strip()
    )