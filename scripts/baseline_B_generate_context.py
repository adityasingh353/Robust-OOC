import os
import sys
from PIL import Image

# Add the root directory to the python path to allow imports from models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.baseline_B_vlm import BaselineBVLM

def test_vlm():
    print("Initializing Baseline B VLM (MOCK mode for fast testing)...")
    vlm = BaselineBVLM(mock=True)
    
    # Create a dummy image for testing
    dummy_image = Image.new('RGB', (224, 224), color = 'red')
    caption = "A red square representing a generic placeholder."
    
    print(f"\nInput Caption: {caption}")
    print("Generating context...")
    
    context = vlm.generate_context(dummy_image, caption)
    
    print(f"\nGenerated Context:\n{context}")
    print("\nMilestone 2 Test Complete.")

if __name__ == "__main__":
    test_vlm()
