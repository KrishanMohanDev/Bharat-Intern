import streamlit as st
import pickle
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()


tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

# text preprocessing
def transform_text(text):
    #     Lower case
    text = text.lower()

#     Tokenization
    text = nltk.word_tokenize(text)

#     Remove Special Character
    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]  # cloning the list
    y.clear()

#     Remove stop words and punctuation
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

#     Stemming
    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


# website building
st.title("Email/SMS Spam Classifier")

input_sms = st.text_area("Enter the message")

if st.button("Predict"):
    # 1. Preprocess
    transformed_sms = transform_text(input_sms)
    # 2. Vectorize
    vector_input = tfidf.transform([transformed_sms])
    # 3. Predict
    result = model.predict(vector_input)[0]
    # 4. Display
    if result == 1:
        st.header("Spam")
    else:
        st.header("Not Spam")