# 🖼️ Image to Story Generator

This Streamlit app uses AI to generate a beautiful 3–4 line story from any image.

## ✨ Features

- Upload an image
- Generates a caption using BLIP (by Salesforce)
- Uses GPT-2 to expand that into a story
- Easy download of the generated story

## 🧠 Models Used

- **BLIP (Salesforce)**: For image captioning
- **GPT-2 (OpenAI)**: For story generation

## 🚀 How to Run

```bash
git clone https://github.com/AshwiniGidaveer82/ImageToStoryGenerate
cd ImageToStoryGenerate
pip install -r requirements.txt
streamlit run app.py
