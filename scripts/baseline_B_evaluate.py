import os
import sys

# Add the root directory to the python path to allow imports from models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.baseline_B_classifier import BaselineBClassifier

def test_classifier():
    print("Initializing Baseline B Classifier...")
    # Explicitly use CPU for testing to avoid GPU memory issues if user has limited VRAM
    classifier = BaselineBClassifier(device="cpu")
    
    print("Testing with dummy contexts...")
    
    # Test case 1: Very different contexts (Likely OOC)
    ctx1_ooc = "The president is giving a speech on the economy in Washington D.C."
    ctx2_ooc = "An actor is filming a movie scene about a politician in Hollywood."
    
    # Test case 2: Very similar contexts (Likely NOOC)
    ctx1_nooc = "A golden retriever is playing fetch in the park."
    ctx2_nooc = "A golden retriever dog is catching a ball outdoors in a grassy park."
    
    print(f"\nEvaluating OOC-like dummy data:")
    print(f"Context 1: {ctx1_ooc}")
    print(f"Context 2: {ctx2_ooc}")
    pred_ooc = classifier.predict(ctx1_ooc, ctx2_ooc)
    print(f"Prediction: {pred_ooc} (1 = OOC, 0 = NOOC)")
    
    print(f"\nEvaluating NOOC-like dummy data:")
    print(f"Context 1: {ctx1_nooc}")
    print(f"Context 2: {ctx2_nooc}")
    pred_nooc = classifier.predict(ctx1_nooc, ctx2_nooc)
    print(f"Prediction: {pred_nooc} (1 = OOC, 0 = NOOC)")
    
    print("\nBatch prediction test...")
    batch_preds = classifier.predict_batch([ctx1_ooc, ctx1_nooc], [ctx2_ooc, ctx2_nooc])
    print(f"Batch predictions: {batch_preds}")
    
    print("\nMilestone 1 Test Complete.")

if __name__ == "__main__":
    test_classifier()
