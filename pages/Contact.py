import streamlit as st
from datetime import datetime
import db
#from win32com.client import Dispatch

#def speak(str):
    #speak=Dispatch(("SAPI.SpVoice"))
    #speak.Speak(str)

st.title("Get In Touch!")
st.caption("### We're here to help")
COMMENT_TEMPLATE_MD = """{} - {}
> {}"""

# Reviews part
conn = db.connect()
comments = db.collect_contact(conn)

for index, entry in enumerate(comments.itertuples()):
    #st.markdown(COMMENT_TEMPLATE_MD.format(entry.name, entry.date, entry.comment))
    is_last = index == len(comments) - 1
    is_new = "just_posted" in st.session_state and is_last

# Insert comment
#st.write("**Add your own comment:**")
form = st.form("comment", clear_on_submit=True)
name = form.text_input("Name", help="Enter Your Name")
email=form.text_input("Email", help="Enter Your Email ID")
phone=form.text_input("Phone", help="Enter Your Phone Number")
comment = form.text_area("Comment", help="Add Your Comment")
submit = form.form_submit_button("Submit")

if submit:
    st.success("Successfully Submitted.")
    #speak("Successfully Submitted")

if submit:
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    db.insert_contact(conn, [[name, email, phone, comment, date]])
    if "just_posted" not in st.session_state:
        st.session_state["just_posted"] = True
    st.experimental_rerun()

        
