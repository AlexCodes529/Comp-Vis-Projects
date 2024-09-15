import streamlit as st

if "wordSelect" not in st.session_state:
    st.session_state.wordSelect = "blank"


def wordSelect(word):
    st.session_state.wordSelect = word

st.markdown("""

    Welcome to OpenASL's word library!
            
    This page allows you to search up any word from a catalogue of over 20,000 videos hosted on the
    signASL.org webpage which has conveniently collected these videos.
            
    If a word isn't currently supported by our model, you'll see a small "Not Currently Supported"
    tag right beneath the page that pops up when you search a word.
            
    You can use this page to initially learn new words.
            
            
    Hope you enjoy!

""")

wordQuery = st.text_input("Word search")

st.components.v1.iframe(f"https://www.signasl.org/sign/{wordQuery}", height=600, scrolling=True)