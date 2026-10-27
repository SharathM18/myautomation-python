from typing import Any

import httpx
from httpx_retry import RetryPolicy, RetryTransport


class APIClient:
    def __init__(self, base_url: str):
        """
        Initializes the API client.
        """
        # 1. Defines the headers
        headers = {"X-Api-Key": "..."}

        # 2. Define Exponential Backoff Policies
        retry_policy = (
            RetryPolicy()
            .with_max_retries(3)  # Try 3 times before giving up
            .with_min_delay(1.0)  # Wait 1 second on first failure
            .with_multiplier(2)  # Double the wait time (1s -> 2s -> 4s)
            .with_retry_on(
                lambda status: status >= 500 or status == 429
            )  # Retry on Server Errors or Rate Limits
        )
        # 3. Attach Retry Policy into HTTPX Transport layer
        transport = RetryTransport(policy=retry_policy)

        # 4. Initialize client session
        self.client = httpx.Client(
            base_url=base_url, headers=headers, transport=transport, timeout=30.0
        )

    def get(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Performs a strict GET request with automatic background exponential retrieval."""
        try:
            response = self.client.get(endpoint, params=params)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "error": f"HTTP {e.response.status_code}",
                "detail": e.response.text,
            }
        except httpx.RequestError as e:
            return {"success": False, "error": f"Network Connection Failed: {str(e)}"}

    def close(self):
        """Closes the underlying network session cleanly."""
        self.client.close()


# Example Usage
# Initialize the client linked to your background proxy
# api = APIClient(base_url="https://api.example.com")

# result = api.get("/addresses")
# print(result)


# Always close the client when done
# api.close()
