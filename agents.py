import json
import os

from dotenv import load_dotenv
from groq import Groq
from pydantic import ValidationError

from models import Quiz

load_dotenv()
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


def _chat(system, user, json_mode=False):
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to your .env file.")
    kwargs = {"response_format": {"type": "json_object"}} if json_mode else {}
    resp = Groq(api_key=key).chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.3,
        **kwargs,
    )
    return resp.choices[0].message.content


def explain(section_text):
    """Explainer agent: plain-language explanation of one section."""
    system = (
        "You are a patient tutor. Explain the text to a university student in "
        "clear, simple language using ONLY the provided text. Use short "
        "paragraphs and a few bullet points for key ideas. Do not add facts "
        "that are not in the text."
    )
    return _chat(system, section_text)


def make_quiz(sections, n=5):
    """Quizzer agent: n multiple-choice questions grounded in the PDF, as validated JSON."""
    context = "\n\n".join(f"[Section {i + 1}]\n{s}" for i, s in enumerate(sections))
    context = context[:20000]
    system = (
        "You write quiz questions strictly from the provided text. "
        "Return ONLY JSON in this shape: "
        '{"questions":[{"question":"...","options":["A","B","C","D"],'
        '"answer_index":0,"section":1}]} '
        "Rules: exactly 4 options, answer_index is 0-3, 'section' is the "
        "section number the answer comes from, wrong options must be plausible, "
        "vary the position of the correct answer."
    )
    user = f"Write {n} multiple-choice questions from this text.\n\n{context}"
    last_error = None
    for _ in range(2):  # retry once on malformed output
        try:
            raw = _chat(system, user, json_mode=True)
            quiz = Quiz(**json.loads(raw))
            if quiz.questions:
                return quiz
        except (json.JSONDecodeError, ValidationError, TypeError) as e:
            last_error = e
    raise RuntimeError(f"Could not generate a valid quiz: {last_error}")


def tutor(question, chosen, correct, section_text):
    """Tutor agent: re-explain a missed question using the relevant section."""
    system = (
        "You are a supportive tutor. The student answered a quiz question "
        "wrongly. In 3-5 sentences: say why the correct answer is right, why "
        "their choice is wrong, and point to the idea in the text. Use ONLY "
        "the provided text."
    )
    user = (
        f"Question: {question}\nStudent chose: {chosen}\n"
        f"Correct answer: {correct}\n\nRelevant text:\n{section_text}"
    )
    return _chat(system, user)
