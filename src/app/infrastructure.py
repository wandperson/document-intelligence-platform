# Backend
import httpx


LLM_MODEL = "qwen3-vl:8b"

LLM_INSTRUCTION = """
    Extract all visible text from the image exactly as it appears.

    Rules:
    - Do not add any information that is not explicitly visible.
    - Preserve structure (lines, paragraphs, tables if possible).

    Then provide a short neutral description of the image content.

    Output format:
    [FILE]
    {{verbatim extracted text}}

    [Description]
    {{your short description of image}}
"""


async def get_text_from_image(b64_image: str | list[str]) -> str:
    images = [b64_image] if isinstance(b64_image, str) else b64_image

    try:
        # TODO: It's better not to create it every time
        # and pass it to a function or keep it as a singleton
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(300.0, connect=10.0)
        ) as client:
            response = await client.post(
                # Ollama API endpoints docs
                # https://docs.ollama.com/api/generate
                "http://localhost:11434/api/generate",
                json={
                    "model": LLM_MODEL,
                    "prompt": LLM_INSTRUCTION,
                    "images": images,
                    "stream": False,
                    "think": False,
                },
            )

            response.raise_for_status()
    except httpx.RequestError as error:
        raise RuntimeError(f"Failed to get text from image: {error}")

    try:
        response_json = response.json()
    except ValueError:
        raise RuntimeError("Invalid JSON response")

    if "response" not in response_json:
        raise RuntimeError(f"Unexpected response: {response_json}")

    return response_json["response"]
