import streamlit as st
from feedback_database import insert_data


def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key


def sidebar_login(db):
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"
            "2. Type the symptoms of your cat\n"
            "3. Enjoy the rest Meow!"
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",
            value=st.session_state.get("OPENAI_API_KEY", ""),
        )
        if api_key_input:
            set_openai_api_key(api_key_input)
        st.write("")
        with st.expander("Give us Feedbacks!", expanded=True):
            username = st.text_input("Username", placeholder="Your Name")
            rating = st.slider("Rating", 0, 5, 5)
            feedback = st.text_input(
                "Write your reviews!", placeholder="Feel free to write anything!"
            )
            review_button = st.button("Thanks!")
            if review_button:
                insert_data(db=db, username=username, rating=rating, feedback=feedback)
                st.markdown(f"**Thanks for submitting the feedback!**")
