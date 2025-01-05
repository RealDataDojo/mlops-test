from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
from openai import OpenAI
import re
import streamlit as st


load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
llm_model = 'gpt-4o-mini'
system_prompt = 'You are a tweet writer. Create a viral tweet based on the text: ' 


def generate_summary(input_text):
    client = OpenAI(api_key=openai_api_key)

    chat_completion = client.chat.completions.create(
        model=llm_model,
        messages=[{"role": "system", "content": system_prompt}] + [{"role": "user", "content": input_text}]
    )
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    st.title("Viral Tweets")
    st.subheader("Make your blog post into viral tweets instantly")
    input_text = st.text_input("Enter text")
    button = st.button("Get viral tweets")
    if button:
        with st.spinner("Generating tweets... Please wait"):
            res = generate_summary(input_text)
        st.text(res)

