from workers import Response, WorkerEntrypoint
from urllib.parse import urlparse

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = urlparse(request.url)

        if request.method == "POST" and url.path == "/analyze":
            try:
                body = await request.json()
            except Exception:
                return Response.json(
                    {"error": "Request body must be valid JSON"},
                    status=400,
                )

            return Response.json(
                {
                    "message": "Fraud event received",
                    "event": body,
                }
            )

        return Response.json(
            {"error": "Not found"},
            status=404,
        )
