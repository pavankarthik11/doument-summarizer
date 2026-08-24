"""
summarizer.py — AI Summary Generation Module
Uses Google Gemini 3.6 Flash to generate structured summaries.
"""

import google.generativeai as genai
from typing import TypedDict


class SummaryResult(TypedDict):
    summary: str
    key_points: list[str]
    improvement_suggestions: list[str]


LENGTH_INSTRUCTIONS = {
    "short": "Write a concise summary in 2-3 sentences (50-80 words max).",
    "medium": "Write a balanced summary in 1-2 paragraphs (150-200 words).",
    "long": "Write a comprehensive, detailed summary in 3-4 paragraphs (300-400 words).",
}


def configure_gemini(api_key: str) -> None:
    """Configure the Gemini API client with the provided key."""
    genai.configure(api_key=api_key)


def generate_summary(text: str, length: str, api_key: str) -> SummaryResult:
    """
    Generate a structured summary from extracted document text.

    Args:
        text: The extracted document text.
        length: One of 'short', 'medium', 'long'.
        api_key: Google Gemini API key.

    Returns:
        SummaryResult with summary, key_points, and improvement_suggestions.
    """
    configure_gemini(api_key)

    length_instruction = LENGTH_INSTRUCTIONS.get(length, LENGTH_INSTRUCTIONS["medium"])

    prompt = f"""You are an expert document analyst. Analyze the following document text and provide a structured response.

TASK:
1. Summary: {length_instruction}
2. Key Points: Extract exactly 5 of the most important key points or main ideas as bullet points.
3. Improvement Suggestions: Provide 3 suggestions on how the document could be improved (clarity, structure, completeness, etc.).

DOCUMENT TEXT:
---
{text[:12000]}
---

Respond ONLY in this exact JSON format (no markdown, no code blocks):
{{
  "summary": "Your summary here",
  "key_points": [
    "Key point 1",
    "Key point 2",
    "Key point 3",
    "Key point 4",
    "Key point 5"
  ],
  "improvement_suggestions": [
    "Suggestion 1",
    "Suggestion 2",
    "Suggestion 3"
  ]
}}"""

    model = genai.GenerativeModel("gemini-3.6-flash")
    response = model.generate_content(prompt)
    response_text = response.text.strip()

    # Remove markdown code fences if present
    if response_text.startswith("```"):
        lines = response_text.split("\n")
        response_text = "\n".join(lines[1:-1])

    import json
    result = json.loads(response_text)

    return SummaryResult(
        summary=result.get("summary", ""),
        key_points=result.get("key_points", []),
        improvement_suggestions=result.get("improvement_suggestions", []),
    )
