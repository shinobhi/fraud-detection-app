from workers import Response, WorkerEntrypoint
from urllib.parse import urlparse
import json

MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = urlparse(request.url)

        if request.method == "POST" and url.path == "/analyze":
            try:
                event = await request.json()
            except Exception:
                return Response.json(
                    {"error": "Request body must be valid JSON"},
                    status=400,
                )

            result = await self.env.AI.run(
                MODEL,
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a fraud investigation assistant. "
                                "Analyze account and payment events for suspicious signals. "
                                "Do not claim fraud has definitely occurred. "
                                "Explain your reasoning concisely and suggest investigation steps."
                            ),
                        },
                        {
                            "role": "user",
                            "content": (
                                "Analyze this event:\n\n"
                                + json.dumps(event, indent=2)
                            ),
                        },
                    ],
                    "max_tokens": 500,
                    "temperature": 0.2,
                },
            )

            return Response.json(result)

        return Response.json(
            {"error": "Not found"},
            status=404,
        )
