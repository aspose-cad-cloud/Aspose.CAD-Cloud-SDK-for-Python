# form_param_json_serializer.py

import io
import json
from typing import Any, List, Tuple, Union, Optional

# Type alias for form parameters to improve code readability.
# It represents a tuple compatible with 'requests' library 'files' argument:
# (form_param_file_name: str, fileobj: IO[bytes], content_type: str)
FormFileTuple = Tuple[str, io.BytesIO, str]
FormParam = Tuple[str, Union[str, FormFileTuple]]

class FormParamJsonSerializer:
    """
    Utility class to transform string-based form params data into file-like objects.
    """
    
    @classmethod
    def prepare_form_param(cls, form_param: Optional[Any], 
                               form_param_field_name: str, 
                               form_param_file_name: str) -> List[FormParam]:
        """
        Prepares the form parameter for a multipart request.
        
        If form_param is None, returns an empty list.
        If provided, serializes the data to JSON, encodes it to UTF-8 bytes,
        wraps it in a BytesIO stream, and returns a list containing a single tuple.
        
        Args:
            form_param: The data to be sent. Can be a dict, list, or a pre-serialized JSON string.
            form_param_field_name: The name of the form field (e.g., "exportOptions").
            form_param_file_name: The form_param_file_name that the server will receive (e.g., "exportOptions.json").
            
        Returns:
            A list of tuples. Empty if input is None, otherwise containing the file tuple.
            Compatible with 'files' argument in 'requests' or 'httpx' libraries.
        """
        if form_param is None:
            return []

        # If the input is already a string, assume it is a pre-serialized JSON.
        # Otherwise, serialize the Python object (dict/list) into a JSON string.
        if isinstance(form_param, str):
            json_string = form_param
        else:
            # separators remove unnecessary whitespace to minimize payload size.
            json_string = json.dumps(form_param, separators=(',', ':'))
        
        # Encode the JSON string into UTF-8 bytes 
        json_bytes = json_string.encode('utf-8')
        
        # Create an in-memory binary stream 
        memory_stream = io.BytesIO(json_bytes)
        
        try:
            # Reset stream position to the beginning to ensure the entire content is read during transmission.
            memory_stream.seek(0)
            
            # Read the content from the stream to pass as bytes, 
            # matching the pattern used for regular files (filename, filedata, mimetype). 
            file_data = memory_stream.read()
            
            # Construct the tuple. 
            # 'application/json' explicitly defines the MIME type for the file part.
            file_tuple: FormFileTuple = (form_param_file_name, file_data, 'application/json')
        
            # Return a list with the field name (lowercased) and the file tuple.
            # This structure matches how 'requests' expects multipart data.
            return tuple([form_param_field_name, tuple([form_param_field_name, file_data, 'application/json'])]) 
        finally:
            # Explicitly closing the stream to free up resources.
            memory_stream.close()
