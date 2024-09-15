import streamlit as st

st.set_page_config(
    page_title="OpenASL",
    page_icon=":ear: :hand:"
)

st.sidebar.success("Select a page")

st.write("# Welcome to OpenASL! :hand:")

st.header("Why OpenASL?")
st.markdown(
    """
    OpenASL is a project started by me, Alexander Mallet, after seeing some of the challenges faced 
    by the American Sign Language society at my school. The main issues they faced were:

    :one: Lack of a wider audience with which they could practice.

    :two: Differing online resources making learning the "right" signing difficult.

    :three: Very few members interested in ASL in the surrounding community. 

    OpenASL seeks to solve all 3 of these issues by providing a free, open-source, and globally accessible
    platform for those passionate about sign language and providing acessibility to the audibly impaired.

    To accomplish this goal, OpenASL provides a comprehensive library of american sign language signs through our **"Search+Learn"**
    section. You can then practice this new knowledge on our pre-trained model which recognizes and automatically translates
    using an LSTM architecture in the **"Train+Practice"** section

    To make it even better, you can become a contributor yourself by training the model. Simply input the word(s) you wish to
    train it on, perform these signs, and our model will update on a daily basis to become even more comprehensive and accurate!

    (Plus you get your name added to our contributor list. I think that's pretty cool...)

    In the future, I hope to grow this web app to reflect the different sign language forms around the world, create a global community
    connected via signing, and add even more advanced functionalities.

    And with that, I bid you adieu :hand:, and I hope you enjoy! :heart:

    -Alexander Mallet
    """
)
