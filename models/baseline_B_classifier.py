import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import logging

logger = logging.getLogger(__name__)

class BaselineBClassifier:
    """
    Wrapper for the fine-tuned RoBERTa model used in Baseline B:
    'Detecting Out-of-Context Media with LLaMa-Adapter V2 and RoBERTa'
    """
    def __init__(self, model_name="hoanghoavienvo/roberta-base-detect-cheapfake-combined-train-test-15200-2-8", device=None):
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        logger.info(f"Loading tokenizer and model {model_name} onto {self.device}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()
        
    def predict(self, context1: str, context2: str) -> int:
        """
        Predicts if the contexts represent an Out-of-Context (OOC) or Not-Out-of-Context (NOOC) pair.
        The paper concatenates Context1 and Context2 into a single 'context combined' paragraph.
        
        Returns:
            1 if OOC (Out-of-Context)
            0 if NOOC (Not-Out-of-Context)
        """
        combined_context = f"{context1} {context2}"
        
        inputs = self.tokenizer(combined_context, return_tensors="pt", truncation=True, padding=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            predicted_class_id = logits.argmax().item()
            
        return predicted_class_id

    def predict_batch(self, contexts1: list[str], contexts2: list[str]) -> list[int]:
        """
        Batch prediction for efficiency.
        """
        assert len(contexts1) == len(contexts2), "Context lists must be of the same length"
        combined_contexts = [f"{c1} {c2}" for c1, c2 in zip(contexts1, contexts2)]
        
        inputs = self.tokenizer(combined_contexts, return_tensors="pt", truncation=True, padding=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            predicted_class_ids = logits.argmax(dim=-1).tolist()
            
        return predicted_class_ids
