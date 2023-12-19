def read_file(file_path):
    """
    Read the content of a file and return it as a string.

    Parameters:
        file_path (str): The path to the file.

    Returns:
        str: The content of the file.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError: # Handle the exception
        print(f"Error: File not found at path {file_path}")
        return None
    except Exception as e: # Handle the exception
        print(f"Error: {e}") # Print an error message with the details of the exception
        return None # Return None to indicate an error