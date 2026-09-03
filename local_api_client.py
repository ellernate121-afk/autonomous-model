#!/usr/bin/env python3
"""
Simple local API client for GPT4All-style OpenAI-compatible server.
Saves as local_api_client.py in your repo and run with: python local_api_client.py
"""

import os
import sys
import json
import argparse
import requests

# Defaults
DEFAULT_HOST = "http://localhost"
DEFAULT_PORT = int(os.environ.get("LOCAL_API_PORT", 4891))
DEFAULT_MODEL = os.environ.get("LOCAL_MODEL", "YourModelName")
DEFAULT_TIMEOUT = 30

def build_url(host: str, port: int, path: str) -> str:
    return f"{host}:{port}{path}"

def chat_completion(host: str, port: int, model: str, messages: list, timeout: int = DEFAULT_TIMEOUT):
    url = build_url(host, port, "/v1/chat/completions")
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 512
    }
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}", file=sys.stderr)
        return None

def list_models(host: str, port: int, timeout: int = DEFAULT_TIMEOUT):
    url = build_url(host, port, "/v1/models")
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="Local API client for OpenAI-compatible local server")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Host (default http://localhost)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port (default {DEFAULT_PORT})")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model id to use")
    parser.add_argument("--list", action="store_true", help="List available models")
    parser.add_argument("--message", "-m", help="Single user message to send to the model")
    args = parser.parse_args()

    if args.list:
        models = list_models(args.host, args.port)
        if models is None:
            sys.exit(1)
        print(json.dumps(models, indent=2))
        return

    if not args.message:
        print("No message provided. Use --message 'hello' or --list to see models.", file=sys.stderr)
        sys.exit(1)

    messages = [{"role": "user", "content": args.message}]
    result = chat_completion(args.host, args.port, args.model, messages)
    if result is None:
        sys.exit(1)

    # Try to print assistant text in a friendly way
    try:
        # OpenAI-style response parsing
        choices = result.get("choices")
        if choices and isinstance(choices, list):
            for i, c in enumerate(choices):
                content = c.get("message", {}).get("content") or c.get("text")
                print(f"--- Choice {i} ---")
                print(content)
        else:
            # Fallback: print full JSON
            print(json.dumps(result, indent=2))
    except Exception as e:
        print("Failed to parse response:", e, file=sys.stderr)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
