import streamlit as st
from OpenASLfuncs import *
import time

if "confirm" not in st.session_state:
    st.session_state.confirm = False

if "practice" not in st.session_state:
    st.session_state.practice = False

if "train" not in st.session_state:
    st.session_state.train = False

if "record" not in st.session_state:
    st.session_state.record = False

if "accuracyY" not in st.session_state:
    st.session_state.accuracyY = False

if "accuracyN" not in st.session_state:
    st.session_state.accuracyN = False

if "reset" not in st.session_state:
    st.session_state.reset = False

if "choice1" not in st.session_state:
    st.session_state.choice1 = False

if "choice2" not in st.session_state:
    st.session_state.choice2 = False

if "RUNSTATUSTRANSLATE" not in st.session_state:
    st.session_state.RUNSTATUSTRANSLATE = 0

if "RUNSTATUSRECORDNCACHE" not in st.session_state:
    st.session_state.RUNSTATUSRECORDNCACHE = 0

if "nameSubmitted" not in st.session_state:
    st.session_state.nameSubmitted = False

if "wordSubmitted" not in st.session_state:
    st.session_state.wordSubmitted = False

def changeRecord():
    st.session_state.record = True

def changeChoice1():
    st.session_state.choice1 = True

def changeChoice2():
    st.session_state.choice2 = True

def nameSubmitted():
    st.session_state.nameSubmitted = True

def wordSubmitted():
    st.session_state.wordSubmitted = True

def changeSelect():
    st.session_state.confirm = True
    if multiSelect == "Practice":
        st.session_state.train = False
        st.session_state.reset = False
        st.session_state.practice = True
    if multiSelect == "Train":
        st.session_state.practice = False
        st.session_state.reset = False
        st.session_state.train = True
    if multiSelect == "Reset":
        st.session_state.practice = False
        st.session_state.train = False
        st.session_state.reset = True
    
def Reset():
    st.session_state.confirm = False
    st.session_state.practice = False
    st.session_state.train = False
    st.session_state.record = False
    st.session_state.accuracyY = False
    st.session_state.accuracyN = False
    st.session_state.choice1 = False
    st.session_state.choice2 = False
    st.session_state.RUNSTATUSTRANSLATE = 0
    st.session_state.RUNSTATUSRECORDNCACHE = 0
    st.session_state.nameSubmitted = False
    st.session_state.wordSubmitted = False

    st.write(st.session_state)

def ResetChoices(choice):
    st.session_state.confirm = True
    if choice == "Practice":
        st.session_state.practice = True
    if choice == "Train":
        st.session_state.train = True
    
st.title("Train and Practice")
st.write("This is an open source application where you can practice and learn ASL with AI-driven tools")

if st.session_state.confirm == False:
    st.markdown(
        """
        Welcome to the train and practice section of OpenASL! :hand:

        Here you can both practice your ASL and contribute to the training of our model.

        Here's the basics:

        :one: Select a mode. You can either choose "Train" or "Practice"

        :two: Follow the instructions that pop up on this specific page.

                """)


st.subheader("Select mode")
multiSelect = st.selectbox("Mode selection:", ("Practice", "Train", "Reset"))

confirm = st.button("Confirm choice", on_click=changeSelect)


if st.session_state.confirm == True:

    if st.session_state.practice == True:
        st.write("Welcome to OpenASL's practice mode! Follow these steps to practice!")
        st.write(":one: Record and submit video of yourself signing. Press 's' to begin, and 'q' to end the video.")
        st.write(":two: Get real-time predictions on the clarity of your signing.")
        st.write(":three: Get accurate translations of your signing with our constantly evolving model. Press 't' to receive your translation.")
        st.write(":four: Enjoy!")
        record = st.button("Begin recording", on_click=changeRecord)

        if st.session_state.record:
            if st.session_state.RUNSTATUSTRANSLATE < 1:
                TRANSLATE()
                haltButton = st.button("Restart", on_click=Reset)
                st.session_state.RUNSTATUSTRANSLATE += 1


            feedback1 = st.text_input("Was this translation correct?", on_change=changeChoice1)
            if st.session_state.choice1 and feedback1.lower() == "yes":
                st.write("Perfect!")
            

            if st.session_state.choice1 and feedback1.lower() == "no":
                st.write("We apologise for the incorrect translation. Would you wish to submit the correct translation?")
                feedback2 = st.text_input("Submit translation?", on_change=changeChoice2)
                if st.session_state.choice2 and feedback2.lower() == "yes":
                    
                    translation = st.text_input("Correct translation: ")
                    st.session_state.RUNSTATUSRECORDNCACHE = 0
                    if st.session_state.RUNSTATUSRECORDNCACHE < 1:
                        RECORDNCACHE(translation.lower())
                        st.session_state.RUNSTATUSRECORDNCACHE += 1

                    if translation:
                        st.write("Thank you for improving our model! Taking you back to the main page")
                        time.sleep(2.5)
                        Reset()
                        ResetChoices(multiSelect)
                        st.rerun()  

            reloadTrain = st.button("Reload and practice again")
            if reloadTrain:
                Reset()
                ResetChoices(multiSelect)
                st.rerun() 

    if st.session_state.train == True:
        st.write(":one: Enter a word which you will be signing.")
        st.write(":two: Perform this sign on camera as it records. Press 's' to start, and 'q' to end.")
        st.write(":three: Submit video by ending the video.")
        st.write(":four: Sit back and let us do the rest!")
        text = st.text_input("Word: ", on_change=wordSubmitted)
        if st.session_state.wordSubmitted and text != "":
            if st.session_state.RUNSTATUSRECORDNCACHE < 1:
                RECORDNCACHE(text.lower())
                st.session_state.RUNSTATUSRECORDNCACHE += 1

            st.write("Video submitted for training. Thank you for contributing! Would you care to submit your name to be added to our contributor list?")
            option = st.button("Become a contributor", on_click=nameSubmitted)
            if st.session_state.nameSubmitted:
                name = st.text_input("Name: ", )
                with open(r"C:\Users\Alex_\Desktop\Contributor List.txt", "a") as handler:
                    handler.write(name+"\n")
                    handler.close()
                if name:
                    st.write(f"Thanks {name}! :heart:")

            
                reloadTrain = st.button("Reload and train again")
                if reloadTrain:
                    Reset()
                    ResetChoices(multiSelect)
                    st.rerun()

    if st.session_state.reset == True:
        Reset()