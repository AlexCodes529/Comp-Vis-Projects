import streamlit as st

st.set_page_config(
    page_title="Help"
)


LinkedIn = "https://www.linkedin.com/in/alexandermallet529/"
Gmail = "alexander.foli.mallet@gmail.com"
Instagram = "https://www.instagram.com/alexander_mallet123/"

st.markdown("""
    If you have any questions, complaints, or business inquries please do not
    hesitate to reach out to me!
     
    **Links:**               """)
            
st.write(":point_right: LinkedIn: [https://www.linkedin.com/in/alexandermallet529/](%s)" % LinkedIn)   
st.write(":point_right: Gmail: [alexander.foli.mallet@gmail.com](%s)" % Gmail)   
st.write(":point_right: Instagram: [https://www.instagram.com/alexander_mallet123/](%s)" % Instagram)          