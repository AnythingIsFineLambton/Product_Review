import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from datetime import datetime
import db

st.title("Product Review Analysis")
st.sidebar.title("Select Your Choices")
st.set_option('deprecation.showPyplotGlobalUse', False)

data_path = ("Yelp.csv")

def load_data():
    data = pd.read_csv(data_path)
    data['date'] = pd.to_datetime(data['date'])
    return data

data = load_data()

st.markdown("")
see_data = st.expander('Click here to see the dataset')
with see_data:
        st.dataframe(data.reset_index(drop=True))
st.text('')

st.sidebar.subheader("Random Reviews")
random_tweet = st.sidebar.radio('Select the Sentiment',('positive','negative','neutral'))
if st.sidebar.checkbox("Show", False, key="1"):
    st.subheader("Here are some of random reviews according to your choice!")
    for i in range(len(data['date'])):
        if i ==5:
            break
        else:
            st.markdown(str(i+1) +"." + data.query("sentiments == @random_tweet")[['text']].sample(n=1).iat[0,0])

st.sidebar.markdown("### Visualization of Reviews")
select = st.sidebar.selectbox('Select type of visualization',['Histogram','PieChart'])

sentiment_count = data['sentiments'].value_counts()
sentiment_count = pd.DataFrame({'Sentiments':sentiment_count.index,'Reviews':sentiment_count.values})

if st.sidebar.checkbox('Show',False,key='0'):
    st.markdown("### No. of reviews by sentiments ")
    if select=='Histogram':
        fig = px.bar(sentiment_count,x='Sentiments',y='Reviews',color='Reviews',height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count,values='Reviews',names='Sentiments')
        st.plotly_chart(fig)

st.sidebar.subheader("Breakdown Sentiments by city")
choice = st.sidebar.multiselect("Pick City", tuple(pd.unique(data["city"])))
if st.sidebar.checkbox("Show", False, key="5"):
    if len(choice) > 0:
        chosen_data = data[data["city"].isin(choice)]
        fig = px.histogram(chosen_data, x="city", y="sentiments",
                                histfunc="count", color="sentiments",
                                facet_col="sentiments", labels={"sentiments": "sentiment"})
        st.plotly_chart(fig)

# Word cloud
st.sidebar.subheader("Word Cloud")
word_sentiment = st.sidebar.radio("Which Sentiment to Display?", tuple(pd.unique(data["sentiments"])))
if st.sidebar.checkbox("Show", False, key="6"):
    st.subheader(f"Word Cloud for {word_sentiment.capitalize()} Sentiment")
    df = data[data["sentiments"]==word_sentiment]
    words = " ".join(df["text"])
    #processed_words = " ".join([word for word in words.split() if "http" not in word and not word.startswith() and word != "RT"])
    processed_words = " ".join([word for word in words.split()])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color="white", width=600, height=500).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()