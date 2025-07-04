import google.generativeai as genai

def stream_response(model, user_input: str) -> str:
    response = model.generate_content(user_input, stream=True)
    full_response = ""
    for chunk in response:
        full_response += chunk.text
    return full_response