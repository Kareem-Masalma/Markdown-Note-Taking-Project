from google import genai
from google.genai import types


async def send_to_gemini(prompt: str):
    """
    This method is used to call gemini api with a certain prompt.

    :param prompt: The text sent to api.
    :return: The response of the api.
    """
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=1)
        ),
    )


    return response
