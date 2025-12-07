# Utility functions
from fastapi.responses import JSONResponse
from rich.pretty import pprint


def response(data, message: str, success: bool = True):
    return {"data": data, "message": message, "success": success}


def error_response(message: str, status_code: int = 400):
    return JSONResponse(content={"message": message}, status_code=status_code)


def dd(args):
    pprint(args)  # Pretty print with color
