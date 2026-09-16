import os

import pytest
import requests


def test_local_api_smoke():
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "qwen3.5")
    url = f"{base_url.rstrip('/')}/api/generate"

    try:
        response = requests.post(
            url,
            json={
                "model": model,
                "prompt": "Say only the word Hello.",
                "stream": False,
            },
            timeout=10,
        )
    except requests.RequestException as exc:
        pytest.skip(f"Local API not available at {url}: {exc}")

    if response.status_code != 200:
        pytest.skip(
            f"Local API responded with status {response.status_code} at {url}: "
            f"{response.text[:200]}"
        )

    payload = response.json()
    assert "response" in payload
    assert str(payload["response"]).strip()