import json
import logging
from urllib.parse import urlparse

from workers import Response, WorkerEntrypoint

from fraud_rules import derive_signals

MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
logger = logging.getLogger(__name__)

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

            event_details = event.get("event", event)
            local_signals = derive_signals(event_details)

            try:
                result = await self.env.AI.run(
                    MODEL,
                    {
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "You are a fraud investigation assistant. "
                                    "The application has already computed deterministic fraud signals. "
                                    "Use those signals as evidence when explaining risk and include "
                                    "each one verbatim in the response's signals array. "
                                    "Do not invent additional factual signals that are not supported by the event. "
                                    "You may identify patterns worth investigating, but clearly distinguish them "
                                    "from signals already detected by the system. "
                                    "Do not state that fraud has definitely occurred."
                                ),
                            },
                            {
                                "role": "user",
                                "content": (
                                    "Analyze this event:\n\n"
                                    + json.dumps(event, indent=2)
                                    + "\n\nDeterministic fraud signals:\n"
                                    + json.dumps(local_signals, indent=2)
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
            except Exception:
                logger.exception("Workers AI fraud analysis failed")
                return Response.json(
                    {
                        "error": (
                            "Fraud analysis is temporarily unavailable. "
                            "Please try again shortly."
                        ),
                        "code": "analysis_unavailable",
                    },
                    status=503,
                )

        return Response.json(
            {"error": "Not found"},
            status=404,
        )
