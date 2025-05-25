import logging
from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration,
    GPT2Tokenizer,
    GPT2LMHeadModel
)
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load BLIP model and processor
logger.info("Loading BLIP model and processor...")
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load smaller GPT-2 model (distilgpt2) with fast tokenizer
logger.info("Loading distilgpt2 tokenizer and model (use_fast=True)...")
gpt2_tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2", use_fast=True)
gpt2_model = GPT2LMHeadModel.from_pretrained("distilgpt2")

# Setup device - use GPU if available, else CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
blip_model.to(device)
gpt2_model.to(device)

def generate_story(image):
    """
    Generate a short 3-4 line story based on the uploaded image.

    Args:
        image (PIL.Image): Input image.

    Returns:
        str: Generated story.
    """
    try:
        logger.info("Generating caption from image...")
        inputs = blip_processor(image, return_tensors="pt").to(device)
        caption_ids = blip_model.generate(**inputs, max_length=50)
        caption = blip_processor.decode(caption_ids[0], skip_special_tokens=True)
        logger.info(f"Caption: {caption}")

        # Prepare prompt for story generation
        prompt = (
            f"Write a creative 3-4 line story based on this caption:\n"
            f"{caption}\n\nStory:"
        )

        input_ids = gpt2_tokenizer.encode(prompt, return_tensors="pt").to(device)
        output = gpt2_model.generate(
            input_ids,
            max_length=160,
            num_beams=5,
            no_repeat_ngram_size=2,
            early_stopping=True
        )

        generated_text = gpt2_tokenizer.decode(output[0], skip_special_tokens=True)
        story = generated_text.replace(prompt, "").strip()

        logger.info("Story generation completed successfully.")
        return story

    except Exception as e:
        logger.error(f"Error generating story: {e}")
        return "Sorry, an error occurred while generating the story."
