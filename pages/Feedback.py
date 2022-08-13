import streamlit as st
from datetime import datetime
from win32com.client import Dispatch
import db


def speak(str):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(str)
    
COMMENT_TEMPLATE_MD = """{} - {}
> {}"""

# Reviews part
conn = db.connect()
comments = db.collect(conn)

#with st.expander("💬 Review our project"):

# Show comments
        
st.title("💬 Review our project")

st.markdown('#')


# Insert comment
#st.write("**Add your own comment:**")
form = st.form("comment", clear_on_submit=True)
name = form.text_input("Name")
comment = form.text_area("Comment")
submit = form.form_submit_button("Submit")

if submit:
    st.success("Your comment was successfully posted.")
    speak("Your comment was successfully posted") 
    
for index, entry in enumerate(comments.itertuples()):
    st.markdown(COMMENT_TEMPLATE_MD.format(entry.name, entry.date, entry.comment))
    is_last = index == len(comments) - 1
    is_new = "just_posted" in st.session_state and is_last
    #if is_new:
         
             
if submit:
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    db.insert(conn, [[name, comment, date]])
    if "just_posted" not in st.session_state:
        st.session_state["just_posted"] = True
    st.experimental_rerun()
