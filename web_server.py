from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from core.interpreter import run
import io
import sys
import signal
from contextlib import contextmanager
import threading


class CodeRequest(BaseModel):
    code: str


app = FastAPI(title="Hausalang Interpreter API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from web/ directory
app.mount("/static", StaticFiles(directory="web"), name="static")


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException("Code execution timed out")


@app.post("/api/execute")
async def execute_code(request: CodeRequest):
    """Execute Hausalang code and return output"""
    code = request.code.strip()
    
    if not code:
        return {"success": False, "error": "No code provided"}
    
    # Capture stdout
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    
    try:
        # Set a timeout (5 seconds)
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(5)
        
        run(code)
        
        signal.alarm(0)  # Cancel the alarm
        output = buf.getvalue()
        
        return {
            "success": True,
            "output": output if output else "(no output)",
            "error": None
        }
    
    except TimeoutException:
        signal.alarm(0)
        return {
            "success": False,
            "output": buf.getvalue(),
            "error": "Code execution timed out (5 second limit)"
        }
    
    except Exception as e:
        signal.alarm(0)
        return {
            "success": False,
            "output": buf.getvalue(),
            "error": str(e)
        }
    
    finally:
        sys.stdout = old_stdout


@app.get("/api/examples")
async def get_examples():
    """Return built-in examples for the playground"""
    return {
        "examples": [
            {
                "name": "Hello World",
                "code": 'rubuta "Sannu Duniya"'
            },
            {
                "name": "Variables",
                "code": 'suna = "Nura"\nrubuta "Sannu " + suna'
            },
            {
                "name": "If Statement",
                "code": 'x = 15\nidan x > 10:\n    rubuta "x is greater than 10"\nin ba haka ba:\n    rubuta "x is 10 or less"'
            },
            {
                "name": "Function",
                "code": 'aiki add(a, b):\n    mayar a + b\n\nresult = add(5, 3)\nrubuta result'
            },
            {
                "name": "Arithmetic",
                "code": 'rubuta 2 + 3 * 4\nrubuta (2 + 3) * 4\nrubuta 20 / 4'
            }
        ]
    }


@app.get("/")
async def root():
    """Redirect to playground"""
    return {"message": "Hausalang Interpreter API. Visit /static/ for the playground."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
