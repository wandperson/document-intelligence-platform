# Backend
import httpx

# Custom
from app.core.config import get_settings

LLM_MODEL = "qwen3-vl:8b"

LLM_INSTRUCTION = """
You are an expert document parsing assistant.
Your task is to extract all text directly from the provided image and format it with maximum structure.

Guidelines:
1. Accuracy: Extract all text verbatim. Do not summarize or skip sections.
2. Output: Provide ONLY the clean, structured text. Do not include any introductory or concluding conversational text.
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
                f"{get_settings().ollama_url}/api/generate",
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
