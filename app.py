import streamlit as st
from google import genai
from google.genai import types

client = genai.Client(api_key=st.secrets["gemini_api_key"])


@st.cache_data
def get_gemini_response(text):
    api_response = client.models.generate_content(
        model="gemini-2.5-pro",
        config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION),
        contents=text,
    )
    parts = api_response.candidates[0].content.parts
    response = "".join(part.text for part in parts)
    return response


st.title("संस्कृत-शोधकः")
st.markdown(
    """
    **Note**: Generating the response *will* be slow. Please be patient!
    
    Please also note that this demo supports a limited number of requests and 
    may be unavailable if too many people use the service. 
    Thank you for your understanding.
    
    ---
    Enter your sentence in the input box at the bottom of this screen
    to receive feedback from an AI engine. Input in Devanagari may be preferable 
    (you can use [Aksharamukha](https://www.aksharamukha.com) to transliterate),
    but the AI might be able to handle transliterated text as well.
    If you don't know the Sanskrit word for something, feel free to use
    some other language. The AI will try to correct it.
    
    **Examples** - Try entering one of these
      - maam सह आगच्चसि to the shop?
      - train kadaa leave?
      - pustakam kutra keep?
"""
)

SYSTEM_INSTRUCTION = """Help me with my Sanskrit progress. I will provide some sentences.
        * Always check the grammar/spelling of everything. Also, briefly comment on the idiomatic aspect.
        * If the sentences have both Sanskrit and English versions separated by an `=` or a `\n`, check whether the sentences align in sentiment/meaning and provide a critique
        * If I only provide one sentence, give me a translation along with the critique
        * If the input contains words in a language different from Sanskrit, provide an appropriate translation and incorporate it into the sentence
        * If the input contains non-Devanagari characters, try to do a phonetic transliteration and then correct the word
        BE AS BRIEF AND CONCISE AS POSSIBLE
    """

# Collapsible prompt section
with st.expander("View Prompt (Non-editable)"):
    st.markdown(
        "Feel free to copy the prompt and experiment with it at "
        "[Google AI studio](https://aistudio.google.com/prompts/new_chat):"
    )
    st.markdown(SYSTEM_INSTRUCTION)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("संस्कृतवाक्यम् (e.g. try - maam सह आगच्चसि to the shop?)"):
    if not prompt.strip():
        st.error("Please enter some text.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Generating response ... Please wait."):
            response = get_gemini_response(prompt)

        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
