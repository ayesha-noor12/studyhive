# PRD: StudyHive

## Problem
Students reread notes passively and never test themselves. Chat tools explain but don't check understanding or tie answers to the source material.

## Users
University students studying from PDFs (lecture slides, notes, textbook chapters).

## User flow
1. Upload PDF
2. App shows explanation, one section at a time (Next / Previous)
3. Student clicks "I'm ready" to start the quiz
4. Student answers 5 MCQs
5. App shows score and, for each wrong answer, a short explanation referencing the section
6. Option to retry with new questions

## Requirements
| ID | Requirement | Priority |
|----|-------------|----------|
| R1 | Accept PDF up to ~20 pages | Must |
| R2 | Explain each section in plain language, using only PDF content | Must |
| R3 | Quiz generated only from PDF content, 5 MCQs, 4 options each | Must |
| R4 | Score shown after submission | Must |
| R5 | Wrong answers re-explained with section reference | Must |
| R6 | UI shows which agent is working (Explainer, Quizzer, Tutor) | Should |
| R7 | Retry with fresh questions | Could |

## Agents (multi-agent angle)
- **Explainer**: turns a section into a clear explanation
- **Quizzer**: produces MCQs as validated JSON
- **Tutor**: re-explains a missed question using the relevant section

## Non-goals
Accounts, persistence, scanned documents, mobile app, personalization.

## Risks
- Scanned/image PDFs have no text: show a clear error
- LLM returns malformed quiz JSON: validate and retry once
- Hallucinated answers: prompt to use only supplied text, cite section number
