# Spec: StudyHive

## Stack
Python 3.11, Streamlit, pypdf, Groq or OpenAI API, pydantic for validation. API key in `.env`.

## Structure
```
studyhive/
  app.py            # Streamlit UI and state
  pdf_utils.py      # extract text, split into sections
  agents.py         # Explainer, Quizzer, Tutor
  models.py         # Quiz / Question pydantic models
  prompts.py        # prompt templates
  .env.example
  scope.md prd.md spec.md README.md
```

## Modules
- `pdf_utils.extract_sections(file) -> list[Section]`: read pages with pypdf, join text, split into chunks of ~800 words, number them. Raise `NoTextError` if no text found.
- `agents.explain(section) -> str`: prompt "Explain this for a student using only this text."
- `agents.make_quiz(sections, n=5) -> Quiz`: ask for JSON `{questions:[{q, options[4], answer_index, section_id}]}`; validate with pydantic; retry once on failure.
- `agents.tutor(question, chosen, section) -> str`: explain why the answer is correct and why the chosen one is wrong, referencing the section.

## State (st.session_state)
`sections`, `current_idx`, `stage` (upload | explain | quiz | results), `quiz`, `answers`.

## Screens
1. Upload
2. Explain (section n of N, Next/Previous, "I'm ready" button)
3. Quiz (radio buttons per question, Submit)
4. Results (score, per-wrong-answer Tutor explanation, Retry)

## Build order
1. pdf_utils + test on one PDF
2. explain() and Explain screen
3. make_quiz() with validation
4. Quiz and Results screens
5. tutor() for wrong answers
6. Agent status line, README, demo recording

## Done when
A PDF can be uploaded, explained, quizzed, scored and re-explained without errors on a real 10-page document.
