from openai import OpenAI



def is_valid_key(api_key):
    client = OpenAI(api_key=api_key)
    try:
        # Make a simple call to test the key, for example, list the engines
        # TODO: The resource 'Engine' has been deprecated
        # Replace the deprecated call with a valid one, for example:
        client.completions.create(model="gpt-3.5-turbo", prompt="Hello")

        # If the above call succeeds, the key is valid
        return True, "API key is valid."
    except Exception as e:
        # It's generally a good idea not to expose exception details in production
        # Here we return the exception message to be displayed in the Streamlit app
        return False, str(e)