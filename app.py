import streamlit as st
from PIL import Image
from story_generator import generate_story

st.set_page_config(page_title="AI Image Story Generator", layout="centered")
st.title("🖼️ AI Image to Story Generator")
st.markdown("Upload an image and let AI generate a beautiful story about it.")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Generate Story"):
        with st.spinner("Generating story..."):
            try:
                story = generate_story(image)
                st.markdown(
                    f"""
                    <div style='padding: 15px; border-radius: 10px; background-color: #f9f9f9;
                         border-left: 5px solid #4CAF50; margin-top: 20px'>
                        <p style='font-size: 18px; line-height: 1.6'>{story}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.download_button("📄 Download Story", story, file_name="story.txt")
            except Exception as e:
                st.error("Failed to generate story. Please try again.")
                st.code(str(e))
