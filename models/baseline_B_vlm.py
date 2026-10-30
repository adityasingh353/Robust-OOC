import torch
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class BaselineBVLM:
    """
    Vision-Language Model wrapper for Baseline B.
    Replaces LLaMa-Adapter V2 with LLaVA-1.5 7B (or a mock implementation for fast testing).
    Generates a contextual description given an image and a caption.
    """
    def __init__(self, model_name="llava-hf/llava-1.5-7b-hf", device=None, mock=True):
        self.mock = mock
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        if self.mock:
            logger.info("Initializing VLM in MOCK mode. No heavy weights will be loaded.")
        else:
            logger.info(f"Loading VLM {model_name} onto {self.device}...")
            from transformers import AutoProcessor, LlavaForConditionalGeneration
            self.processor = AutoProcessor.from_pretrained(model_name)
            # Use 4-bit or 8-bit quantization if possible to save memory, else load normally
            try:
                self.model = LlavaForConditionalGeneration.from_pretrained(
                    model_name, 
                    device_map="auto", 
                    load_in_4bit=True
                )
            except Exception as e:
                logger.warning(f"Could not load in 4-bit: {e}. Loading normally...")
                self.model = LlavaForConditionalGeneration.from_pretrained(model_name).to(self.device)
            self.model.eval()
            
    def generate_context(self, image: Image.Image, caption: str) -> str:
        """
        Generates a contextual paragraph describing the image and the given caption.
        """
        if self.mock:
            # Return a generic dummy context for testing the pipeline
            return f"In the image, we see a scene related to the text '{caption}'. The scene appears to depict related entities and actions."
            
        # LLaVA specific prompt format
        prompt = f"USER: <image>\nHere is a caption for this image: '{caption}'. Describe the context of this image and caption in detail.\nASSISTANT:"
        
        inputs = self.processor(text=prompt, images=image, return_tensors="pt")
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            output_ids = self.model.generate(**inputs, max_new_tokens=150)
            
        # Decode and strip the prompt part
        output_text = self.processor.decode(output_ids[0], skip_special_tokens=True)
        # Extract everything after "ASSISTANT: "
        if "ASSISTANT:" in output_text:
            context = output_text.split("ASSISTANT:")[1].strip()
        else:
            context = output_text.strip()
            
        return context

