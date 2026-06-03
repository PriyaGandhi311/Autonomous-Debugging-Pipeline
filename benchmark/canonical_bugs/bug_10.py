# Bug type: exception_handling
# Description: Exception is caught but original error information is lost

def read_file(filepath):
    try:
        with open(filepath, "r") as f:
            return f.read()
    except Exception:
        raise Exception("File error")