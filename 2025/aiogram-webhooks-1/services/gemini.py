import logging

from google import genai


class GeminiService:
    def __init__(self, api_key: str, model: str) -> None:
        # google-genai exposes async methods via client.aio
        self._client = genai.Client(api_key=api_key)
        self._async_client = self._client.aio
        self._model = model

    async def ask(self, prompt: str) -> str:
        try:
            response = await self._async_client.models.generate_content(
                model=self._model,
                contents=prompt,
            )
        except Exception:
            logging.exception("Gemini request failed")
            return "I had trouble reaching Gemini right now. Please try again."

        text = response.text or ""
        clean = text.strip()
        if not clean:
            return "Gemini did not return any text this time."
        return clean

    async def aclose(self) -> None:
        close = getattr(self._async_client, "aclose", None)
        if close is not None:
            await close()
