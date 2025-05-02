import streamlit as st
import requests
import re

API_URL = "http://localhost:3000/"  # Replace with your actual API endpoint

st.title("Cuss Word Detector")

# Input text
user_input = st.text_area("Enter text to check for cuss words:")

if st.button("Detect"):
    if not user_input.strip():
        st.warning("Please enter some text.")
    else:
        # Send request to API
        response = requests.post(API_URL, json={"text": user_input})

        if response.status_code == 201:
            result = response.json()

            if result['cuss_words_detected'] == True:
                st.subheader("Original Text")
                highlighted_text = user_input
                for entry in sorted(result["cuss_words"], key=lambda x: -x["start_index"]):
                    word = entry["word"]
                    start, end = entry["start_index"], entry["end_index"] + 1
                    highlighted_text = (
                        highlighted_text[:start]
                        + f":red[{highlighted_text[start:end]}]"
                        + highlighted_text[end:]
                    )

                st.markdown(highlighted_text)

                st.subheader("Detection Result")
                st.write("Cuss words detected:", result["cuss_words_detected"])
                st.write("Cuss words list:", [entry["word"] for entry in result["cuss_words"]])

        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
