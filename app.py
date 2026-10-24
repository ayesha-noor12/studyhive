import streamlit as st

import agents
from pdf_utils import NoTextError, extract_sections, split_text

st.set_page_config(page_title="StudyHive", page_icon="🐝")
st.title("🐝 StudyHive")
st.caption("Paste text or upload a PDF → get it explained → take a quiz → review your mistakes")

S = st.session_state
defaults = {"stage": "upload", "sections": [], "idx": 0,
            "explanations": {}, "quiz": None, "answers": {}}
for k, v in defaults.items():
    S.setdefault(k, v)


def clear_quiz_state():
    for k in list(S.keys()):
        if k.startswith("tutor") or (k.startswith("q") and k[1:].isdigit()):
            del S[k]
    S.answers = {}


def build_quiz():
    try:
        with st.spinner("Quizzer agent is writing questions..."):
            S.quiz = agents.make_quiz(S.sections)
    except Exception as e:
        st.error(f"Quiz generation failed: {e}")
        return False
    clear_quiz_state()
    S.stage = "quiz"
    return True


# ---------- Upload / Paste ----------
if S.stage == "upload":
    tab_paste, tab_pdf = st.tabs(["Paste text", "Upload PDF"])

    with tab_paste:
        pasted = st.text_area("Paste your notes or chapter text here", height=300)
        if st.button("Start with pasted text", type="primary"):
            try:
                S.sections = split_text(pasted)
                S.idx, S.explanations, S.stage = 0, {}, "explain"
                st.rerun()
            except NoTextError as e:
                st.error(str(e))

    with tab_pdf:
        f = st.file_uploader("Upload a text-based PDF (up to ~20 pages)", type="pdf")
        if f and st.button("Start with PDF", type="primary"):
            try:
                S.sections = extract_sections(f)
                S.idx, S.explanations, S.stage = 0, {}, "explain"
                st.rerun()
            except NoTextError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Could not read this PDF: {e}")

# ---------- Explain ----------
elif S.stage == "explain":
    n, i = len(S.sections), S.idx
    st.caption("🤖 Agent: Explainer")
    st.subheader(f"Section {i + 1} of {n}")
    if i not in S.explanations:
        try:
            with st.spinner("Explainer agent is reading..."):
                S.explanations[i] = agents.explain(S.sections[i])
        except Exception as e:
            st.error(f"Explanation failed: {e}")
            st.stop()
    st.write(S.explanations[i])
    with st.expander("Original text"):
        st.write(S.sections[i])

    c1, c2, c3 = st.columns(3)
    if c1.button("← Previous", disabled=(i == 0)):
        S.idx -= 1
        st.rerun()
    if c2.button("Next →", disabled=(i == n - 1)):
        S.idx += 1
        st.rerun()
    if c3.button("I'm ready, quiz me", type="primary"):
        if build_quiz():
            st.rerun()

# ---------- Quiz ----------
elif S.stage == "quiz":
    st.caption("🤖 Agent: Quizzer")
    with st.form("quiz_form"):
        picks = []
        for qi, q in enumerate(S.quiz.questions):
            picks.append(st.radio(f"{qi + 1}. {q.question}", q.options,
                                  index=None, key=f"q{qi}"))
        submitted = st.form_submit_button("Submit answers", type="primary")
    if submitted:
        if None in picks:
            st.warning("Please answer every question.")
        else:
            S.answers = {qi: S.quiz.questions[qi].options.index(p)
                         for qi, p in enumerate(picks)}
            S.stage = "results"
            st.rerun()

# ---------- Results ----------
else:
    quiz = S.quiz
    wrong = [qi for qi, q in enumerate(quiz.questions)
             if S.answers.get(qi) != q.answer_index]
    score = len(quiz.questions) - len(wrong)
    st.header(f"Score: {score}/{len(quiz.questions)}")
    if not wrong:
        st.success("Perfect! Nothing to review.")
    else:
        st.caption("🤖 Agent: Tutor")
    for qi in wrong:
        q = quiz.questions[qi]
        chosen, correct = q.options[S.answers[qi]], q.options[q.answer_index]
        st.markdown(f"**{qi + 1}. {q.question}**")
        st.write(f"❌ Your answer: {chosen}")
        st.write(f"✅ Correct: {correct}")
        key = f"tutor{qi}"
        if key not in S:
            sec = min(max(q.section, 1), len(S.sections)) - 1
            try:
                with st.spinner("Tutor agent is explaining..."):
                    S[key] = agents.tutor(q.question, chosen, correct, S.sections[sec])
            except Exception as e:
                S[key] = f"Tutor failed: {e}"
        st.info(f"{S[key]}\n\n_Source: section {min(max(q.section, 1), len(S.sections))}_")
        st.divider()

    c1, c2 = st.columns(2)
    if c1.button("New quiz on same PDF"):
        if build_quiz():
            st.rerun()
    if c2.button("Start over"):
        for k in list(S.keys()):
            del S[k]
        st.rerun()
