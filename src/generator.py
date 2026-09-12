import os
from openai import OpenAI


def generate_reply(email_text, examples):
    """
    Generate a suggested email reply using an LLM,
    grounded in similar historical email/reply examples.
    """

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    examples_text = "\n\n".join(
        [
            f"Example email:\n{item['email']}\n"
            f"Example reply:\n{item['reply']}"
            for item in examples
        ]
    )

    prompt = f"""
You are an AI email assistant.

Write a professional, concise, helpful reply to the incoming email.

Use the historical examples as guidance for tone and response style.
Do not copy an example blindly. Adapt the response to the new email.

Historical examples:
{examples_text}

Incoming email:
{email_text}

Return only the suggested reply.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful professional email assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()
