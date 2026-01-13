# ui/app.py
import streamlit as st

# =========================
# MUST BE FIRST STREAMLIT CALL
# =========================
st.set_page_config(
    page_title="Real Estate AI Valuation System",
    layout="wide",
)

# =========================
# PATH BOOTSTRAP
# =========================
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# =========================
# IMPORTS
# =========================
from ui.shared.state.session_state import (
    initialize_session_state,
    get_session_state,
)
from ui.shared.auth.login import render_login
from ui.navigation import render_navigation


def main():
    # =========================
    # INIT SESSION STATE (FIRST)
    # =========================
    initialize_session_state()
    state = get_session_state()

    # =========================
    # AUTH GATE
    # =========================
    if not state.user:
        render_login()
        st.stop()

    # =========================
    # DEBUG (OPTIONAL)
    # =========================
    st.sidebar.markdown("### Session Debug")
    st.sidebar.write("USER:", state.user)
    st.sidebar.write("ROLE:", state.role)

    # =========================
    # MAIN UI
    # =========================
    render_navigation()
    st.title("📊 Hệ thống định giá – Tổng quan")


if __name__ == "__main__":
    main()
