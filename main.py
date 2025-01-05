from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os
from openai import OpenAI
import re
import streamlit as st


load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
llm_model = 'gpt-4o-mini'
system_prompt = 'You are a youtube summarizer. Create a short, informative summary of the main points of the transcript text here: ' 


def extract_transcript(url):
    res = ''
    video_id = re.split(r'&|=', url)[1]
    transcripts = YouTubeTranscriptApi.get_transcript(video_id)

    for transcript in transcripts:
        res += ' ' + transcript['text']
    return res


def generate_summary(res):
    client = OpenAI(api_key=openai_api_key)

    chat_completion = client.chat.completions.create(
        model=llm_model,
        messages=[{"role": "system", "content": system_prompt}] + [{"role": "user", "content": res}]
    )
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    st.title("Youtube Summarizer")
    st.subheader("Get notes from videos ASAP")
    input_url = st.text_input("Enter your url")
    button = st.button("Generate video summary")
    if button:
        with st.spinner("Generating summary... Please wait"):
            res = extract_transcript(input_url)
            summary = generate_summary(res)
        st.text(summary)

