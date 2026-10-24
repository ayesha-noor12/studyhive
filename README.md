# 🐝 StudyHive

Paste your notes or upload a PDF, get them explained section by section, take a quiz when you're ready, and get every mistake re-explained from your own material.

Built for the Devpost **Build With AI: Basics** hackathon.

## Who it's for

University students who study from lecture notes or textbook chapters and want quick, grounded explanations plus self-testing, instead of rereading passively.

## What it does

1. **Input:** paste text or upload a text-based PDF (up to ~20 pages).
2. **Explain:** the Explainer agent walks through the material one section at a time, in plain language, using only your text.
3. **Quiz:** click "I'm ready" and the Quizzer agent writes 5 multiple-choice questions from your material.
4. **Review:** you get a score, and the Tutor agent re-explains each question you got wrong and points to the section it came from.

## How it works (three agents)

| Agent | Job |
|-------|-----|
| Explainer | Turns one section into a clear explanation |
| Quizzer | Writes 5 MCQs as validated JSON (retries once if the output is malformed) |
| Tutor | Explains why the correct answer is right and the chosen one is wrong |

The UI shows which agent is working at each step.

## Run it

You need Python 3.10+ and a free API key from [console.groq.com](https://console.groq.com).

```bash
git clone <your-repo-url>
cd studyhive
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # then add your GROQ_API_KEY
streamlit run app.py
```

Optional: set `GROQ_MODEL` in `.env` (for example `openai/gpt-oss-20b`). If it's unset, the app picks a model your key can use.

## Project files

```
app.py           Streamlit UI and flow
agents.py        Explainer, Quizzer and Tutor agents
pdf_utils.py     PDF extraction and text splitting
models.py        Quiz validation (pydantic)
scope.md         What's in and out of scope
prd.md           Product requirements
spec.md          Technical spec and build order
```

## Built with the Devpost Learn Skill Pack

The project was planned with the skills in `.agents/skills`, and the planning documents `scope.md`, `prd.md` and `spec.md` are in the repo root.

## Limits

- Scanned (image-only) PDFs aren't supported; paste the text instead.
- No accounts or saved history.
- Quiz quality depends on the model and on how much text you provide.

## What I learned

Things that I learned from this is that how to use LLM to make your work easy as well as planning scope before coding, how to validate LLM JSON output, how to split work across agents.
