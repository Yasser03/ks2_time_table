# Kumon-Style Math Learning App - Addition & Multiplication
# Yasser Mustafa WE. 13/11/2019
# Enhanced with Kumon methodology: progressive levels, worksheets, mastery tracking

from random import randint, shuffle
import streamlit as st

st.set_page_config(
    page_title="Kumon Math Learning",
    page_icon="🧮",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------
DEFAULTS = {
    "subject": "Addition",
    "level": 1,
    "correct": 0,
    "total": 0,
    "streak": 0,
    "best_streak": 0,
    # Worksheet mode
    "worksheet_active": False,
    "worksheet_problems": [],
    "worksheet_answers": [],
    "worksheet_index": 0,
    # Single-problem mode
    "current_x": None,
    "current_y": None,
    "show_result": False,
    "last_correct": None,
}

for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ---------------------------------------------------------------------------
# Level definitions
# ---------------------------------------------------------------------------
# Kumon philosophy: start very easy, increase difficulty in tiny steps.
# Each level is (min_a, max_a, min_b, max_b).

ADDITION_LEVELS = {
    1:  {"label": "+1 facts",            "range": (1, 5, 1, 1),   "desc": "Adding 1 to small numbers"},
    2:  {"label": "+2 facts",            "range": (1, 8, 2, 2),   "desc": "Adding 2 to numbers up to 8"},
    3:  {"label": "+3 facts",            "range": (1, 10, 3, 3),  "desc": "Adding 3 to numbers up to 10"},
    4:  {"label": "Small sums (≤10)",    "range": (1, 5, 1, 5),   "desc": "Both numbers 1-5"},
    5:  {"label": "Sums to 10",          "range": (1, 9, 1, 9),   "desc": "Any single digits, sum ≤ 18"},
    6:  {"label": "+10s",                "range": (10, 90, 10, 90), "desc": "Adding multiples of 10"},
    7:  {"label": "2-digit + 1-digit",   "range": (10, 50, 1, 9),  "desc": "Two-digit plus one-digit"},
    8:  {"label": "2-digit + 2-digit (no carry)", "range": (10, 44, 11, 44), "desc": "Two-digit addition, no carrying"},
    9:  {"label": "2-digit + 2-digit",   "range": (10, 99, 10, 99), "desc": "Any two-digit addition"},
    10: {"label": "3-digit + 2-digit",   "range": (100, 500, 10, 99), "desc": "Three-digit plus two-digit"},
}

MULTIPLICATION_LEVELS = {
    1:  {"label": "×1 facts",    "range": (1, 10, 1, 1),  "desc": "Multiplying by 1"},
    2:  {"label": "×2 facts",    "range": (1, 10, 2, 2),  "desc": "Multiplying by 2"},
    3:  {"label": "×3 facts",    "range": (1, 10, 3, 3),  "desc": "Times-3 table"},
    4:  {"label": "×4 facts",    "range": (1, 10, 4, 4),  "desc": "Times-4 table"},
    5:  {"label": "×5 facts",    "range": (1, 10, 5, 5),  "desc": "Times-5 table"},
    6:  {"label": "×6 facts",    "range": (1, 10, 6, 6),  "desc": "Times-6 table"},
    7:  {"label": "×7 facts",    "range": (1, 10, 7, 7),  "desc": "Times-7 table"},
    8:  {"label": "×8 & ×9",     "range": (1, 10, 8, 9),  "desc": "Times-8 and times-9 tables"},
    9:  {"label": "Mixed facts",  "range": (2, 10, 2, 10), "desc": "All times tables mixed"},
    10: {"label": "Extended",     "range": (2, 12, 2, 12), "desc": "Up to 12×12"},
}

LEVEL_DEFS = {
    "Addition": ADDITION_LEVELS,
    "Multiplication": MULTIPLICATION_LEVELS,
}

OPERATORS = {
    "Addition": ("+", lambda a, b: a + b),
    "Multiplication": ("×", lambda a, b: a * b),
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def generate_problem(subject, level):
    """Return (a, b) for the given subject and level."""
    info = LEVEL_DEFS[subject][level]
    min_a, max_a, min_b, max_b = info["range"]
    return randint(min_a, max_a), randint(min_b, max_b)


def generate_worksheet(subject, level, count=10):
    """Generate a list of (a, b) problems for a worksheet."""
    return [generate_problem(subject, level) for _ in range(count)]


def compute_answer(subject, a, b):
    _, fn = OPERATORS[subject]
    return fn(a, b)


def mastery_reached():
    """Kumon advances when accuracy ≥ 90% over at least 10 problems."""
    if st.session_state.total < 10:
        return False
    return (st.session_state.correct / st.session_state.total) >= 0.90


def reset_stats():
    st.session_state.correct = 0
    st.session_state.total = 0
    st.session_state.streak = 0
    st.session_state.best_streak = 0
    st.session_state.show_result = False
    st.session_state.last_correct = None
    clear_worksheet()


def clear_worksheet():
    st.session_state.worksheet_active = False
    st.session_state.worksheet_problems = []
    st.session_state.worksheet_answers = []
    st.session_state.worksheet_index = 0


def new_single_problem():
    x, y = generate_problem(st.session_state.subject, st.session_state.level)
    st.session_state.current_x = x
    st.session_state.current_y = y
    st.session_state.show_result = False
    st.session_state.last_correct = None

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Kumon Math")

    new_subject = st.radio("Subject", ["Addition", "Multiplication"], index=0 if st.session_state.subject == "Addition" else 1)
    if new_subject != st.session_state.subject:
        st.session_state.subject = new_subject
        reset_stats()
        st.rerun()

    levels = LEVEL_DEFS[st.session_state.subject]
    level_options = [f"Level {k}: {v['label']}" for k, v in levels.items()]
    selected_idx = st.selectbox(
        "Level",
        range(len(level_options)),
        format_func=lambda i: level_options[i],
        index=st.session_state.level - 1,
    )
    new_level = selected_idx + 1
    if new_level != st.session_state.level:
        st.session_state.level = new_level
        reset_stats()
        st.rerun()

    st.divider()
    st.subheader("Progress")
    if st.session_state.total > 0:
        accuracy = st.session_state.correct / st.session_state.total * 100
        st.metric("Accuracy", f"{accuracy:.0f}%")
        st.metric("Solved", st.session_state.total)
        st.metric("Best streak", st.session_state.best_streak)
        st.progress(min(accuracy / 100, 1.0))

        if mastery_reached():
            st.success("Level mastered! Ready to advance.")
    else:
        st.caption("Solve problems to see your progress.")

    st.divider()
    if st.button("Reset progress"):
        reset_stats()
        st.rerun()

# ---------------------------------------------------------------------------
# Main area – title & level info
# ---------------------------------------------------------------------------
subject = st.session_state.subject
level = st.session_state.level
level_info = LEVEL_DEFS[subject][level]
op_symbol, op_fn = OPERATORS[subject]

st.title(f"Kumon {subject}")
st.markdown(f"**Level {level} — {level_info['label']}**: {level_info['desc']}")
st.divider()

# ---------------------------------------------------------------------------
# Mode tabs: Practice (one at a time) | Worksheet (batch of 10)
# ---------------------------------------------------------------------------
tab_practice, tab_worksheet = st.tabs(["Practice", "Worksheet"])

# ---- Practice mode --------------------------------------------------------
with tab_practice:
    # Generate a problem if we don't have one
    if st.session_state.current_x is None:
        new_single_problem()

    x = st.session_state.current_x
    y = st.session_state.current_y
    correct_answer = compute_answer(subject, x, y)

    # Display problem
    st.markdown("### Solve:")
    cols = st.columns([1, 0.5, 1, 0.5, 2])
    cols[0].markdown(f"## {x}")
    cols[1].markdown(f"## {op_symbol}")
    cols[2].markdown(f"## {y}")
    cols[3].markdown("## =")

    answer = cols[4].number_input("Your answer", value=None, step=1, key="practice_answer", label_visibility="collapsed", placeholder="?")

    col_submit, col_next = st.columns(2)

    if col_submit.button("Submit", type="primary", use_container_width=True, disabled=st.session_state.show_result):
        if answer is not None:
            st.session_state.total += 1
            if int(answer) == correct_answer:
                st.session_state.correct += 1
                st.session_state.streak += 1
                st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.streak)
                st.session_state.last_correct = True
            else:
                st.session_state.streak = 0
                st.session_state.last_correct = False
            st.session_state.show_result = True
            st.rerun()

    if col_next.button("Next problem", use_container_width=True):
        new_single_problem()
        st.rerun()

    # Feedback
    if st.session_state.show_result:
        if st.session_state.last_correct:
            st.success(f"Correct! {x} {op_symbol} {y} = {correct_answer}")
            if st.session_state.streak >= 3:
                st.info(f"Streak: {st.session_state.streak} in a row!")
        else:
            st.error(f"Not quite. {x} {op_symbol} {y} = {correct_answer}")
            st.caption("Mistakes help you learn — try the next one!")

# ---- Worksheet mode -------------------------------------------------------
with tab_worksheet:
    st.markdown(
        "A Kumon worksheet gives you **10 problems** to solve in order. "
        "Try to get them all correct before moving on!"
    )

    if not st.session_state.worksheet_active:
        ws_col1, ws_col2 = st.columns(2)
        size = ws_col1.selectbox("Problems per worksheet", [5, 10, 15, 20], index=1)
        if ws_col2.button("Start worksheet", type="primary", use_container_width=True):
            st.session_state.worksheet_problems = generate_worksheet(subject, level, size)
            st.session_state.worksheet_answers = [None] * size
            st.session_state.worksheet_active = True
            st.session_state.worksheet_index = 0
            st.rerun()
    else:
        problems = st.session_state.worksheet_problems
        answers = st.session_state.worksheet_answers
        total = len(problems)
        idx = st.session_state.worksheet_index

        st.progress((idx) / total, text=f"Problem {idx + 1} of {total}")

        if idx < total:
            a, b = problems[idx]
            correct_ans = compute_answer(subject, a, b)

            st.markdown(f"### Problem {idx + 1}")
            pcols = st.columns([1, 0.5, 1, 0.5, 2])
            pcols[0].markdown(f"## {a}")
            pcols[1].markdown(f"## {op_symbol}")
            pcols[2].markdown(f"## {b}")
            pcols[3].markdown("## =")
            ws_answer = pcols[4].number_input(
                "Answer", value=None, step=1, key=f"ws_ans_{idx}",
                label_visibility="collapsed", placeholder="?"
            )

            if st.button("Submit answer", type="primary", key="ws_submit"):
                if ws_answer is not None:
                    answers[idx] = int(ws_answer)
                    st.session_state.worksheet_answers = answers
                    # Update overall stats
                    st.session_state.total += 1
                    if int(ws_answer) == correct_ans:
                        st.session_state.correct += 1
                        st.session_state.streak += 1
                        st.session_state.best_streak = max(st.session_state.best_streak, st.session_state.streak)
                    else:
                        st.session_state.streak = 0
                    st.session_state.worksheet_index = idx + 1
                    st.rerun()

        # Worksheet complete — show results
        if idx >= total:
            st.markdown("### Worksheet complete!")
            ws_correct = 0
            for i, (a, b) in enumerate(problems):
                expected = compute_answer(subject, a, b)
                got = answers[i]
                is_right = (got == expected)
                if is_right:
                    ws_correct += 1
                icon = "+" if is_right else "-"
                st.markdown(
                    f"`{icon}` {a} {op_symbol} {b} = **{got}** "
                    + ("" if is_right else f"(correct: {expected})")
                )

            pct = ws_correct / total * 100
            st.divider()
            m1, m2 = st.columns(2)
            m1.metric("Score", f"{ws_correct}/{total}")
            m2.metric("Accuracy", f"{pct:.0f}%")

            if pct == 100:
                st.balloons()
                st.success("Perfect score! Outstanding work!")
            elif pct >= 90:
                st.success("Level mastered! You can move to the next level.")
            elif pct >= 70:
                st.info("Good effort! A bit more practice and you'll master this level.")
            else:
                st.warning("Keep practising this level. Accuracy comes before speed!")

            if st.button("New worksheet"):
                clear_worksheet()
                st.rerun()

# ---------------------------------------------------------------------------
# Kumon tips
# ---------------------------------------------------------------------------
st.divider()
with st.expander("Kumon tips for success"):
    st.markdown("""
- **Practice daily** — even 15-20 minutes builds strong foundations.
- **Accuracy first** — speed comes naturally once the facts are solid.
- **Master each level** — aim for 90%+ accuracy before advancing.
- **Review earlier levels** — revisit them regularly to keep skills sharp.
- **Learn from mistakes** — understand *why* an answer is wrong, not just what the right answer is.
""")

st.caption("Keep practising! Every problem makes your mental maths stronger.")
