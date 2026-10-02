from workers import Response, WorkerEntrypoint
from urllib.parse import urlparse
import json

MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"

FRAUD_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "risk": {
            "type": "string",
            "enum": ["low", "medium", "high"],
            "description": "The assessed fraud risk level.",
        },
        "summary": {
            "type": "string",
            "description": "A concise summary of the incident and assessment.",
        },
        "signals": {
            "type": "array",
            "items": {"type": "string"},
            "description": "The suspicious signals that informed the assessment.",
        },
        "recommended_actions": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Actions recommended to investigate or mitigate the incident.",
        },
    },
    "required": ["risk", "summary", "signals", "recommended_actions"],
    "additionalProperties": False,
}

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
                                "Base the risk rating only on evidence in the supplied event. "
                                "Return every field required by the response schema. "
                                "Keep the summary concise, list each signal separately, and "
                                "recommend concrete investigation or mitigation actions."
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
                    "response_format": {
                        "type": "json_schema",
                        "json_schema": FRAUD_RESPONSE_SCHEMA,
                    },
                    "max_tokens": 500,
                    "temperature": 0.2,
                },
            )

            return Response.json(result.response)

        return Response.json(
            {"error": "Not found"},
            status=404,
        )
