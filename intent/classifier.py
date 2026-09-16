import json
import re

from ai import ask_ai


SYSTEM_PROMPT = """
You are Jarvis's Intent Classifier.

Never answer the user.

Return ONLY valid JSON.

Available intents:

time
weather
vision
apps
browser
system
memory
chat
exit

------------------------
Vision
------------------------

{
    "intent":"vision",
    "action":"analyze",
    "mode":"describe"
}

Modes:

describe
code
error
website
document
chart
ocr

------------------------
Apps
------------------------

{
    "intent":"apps",
    "action":"open",
    "target":"chrome"
}

------------------------
Browser
------------------------

{
    "intent":"browser",
    "action":"search",
    "query":"python decorators"
}

------------------------
Weather
------------------------

{
    "intent":"weather",
    "action":"current"
}

------------------------
Time
------------------------

{
    "intent":"time",
    "action":"current"
}

------------------------
System
------------------------

Shutdown

{
    "intent":"system",
    "action":"shutdown"
}

Restart

{
    "intent":"system",
    "action":"restart"
}

Lock

{
    "intent":"system",
    "action":"lock"
}

Screenshot

{
    "intent":"system",
    "action":"screenshot"
}

Battery

{
    "intent":"system",
    "action":"battery"
}

------------------------
Memory
------------------------

Remember:

{
    "intent":"memory",
    "action":"remember",
    "key":"favorite color",
    "value":"blue"
}

Recall:

{
    "intent":"memory",
    "action":"recall",
    "key":"favorite color"
}

------------------------
Exit
------------------------

{
    "intent":"exit"
}

------------------------
Anything else
------------------------

{
    "intent":"chat"
}

Return JSON only.
"""


def classify(command):

    prompt = f"""
{SYSTEM_PROMPT}

User:

{command}
"""

    reply = ask_ai(prompt)

    try:

        match = re.search(r"\{.*\}", reply, re.DOTALL)

        if match:

            return json.loads(match.group())

    except Exception:
        pass

    return {
        "intent": "chat"
    }