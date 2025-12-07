# Utility functions 

async def response(data, message: str, success: bool = True):
    return {"data": data, "message": message, "success": success}