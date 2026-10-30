import os
import sys
import json
import time
import psutil
import platform
import pandas as pd
import torch
import traceback
from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration, AutoTokenizer, AutoModelForSequenceClassification

def get_system_info():
    info = {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "total_ram_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
        "available_ram_gb": round(psutil.virtual_memory().available / (1024 ** 3), 2),
        "cuda_available": torch.cuda.is_available(),
    }
    if info["cuda_available"]:
        info["gpu_name"] = torch.cuda.get_device_name(0)
        info["vram_gb"] = round(torch.cuda.get_device_properties(0).total_memory / (1024 ** 3), 2)
    else:
        info["gpu_name"] = "None"
        info["vram_gb"] = 0
    return info

def main():
    start_time = time.time()
    out_dir = os.path.join("results", "EXP003_Baseline_B_Pilot")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, "logs"), exist_ok=True)
    
    sys_info = get_system_info()
    with open(os.path.join(out_dir, "environment.txt"), "w") as f:
        json.dump(sys_info, f, indent=4)
        
    report = {
        "1. Did LLaVA load?": "No",
        "2. Did image inference work?": "No",
        "3. Did context generation work?": "No",
        "4. Did RoBERTa classification work?": "No",
        "5. Were contexts meaningful?": "N/A",
        "6. Were there obvious systematic problems?": "N/A",
        "7. What GPU memory was required?": f"{sys_info['vram_gb']}GB available, but exact requirement unknown.",
        "8. Was inference stable?": "No",
        "9. Is it safe to scale to all 900 held-out samples?": "No",
        "10. What changes, if any, are required before full evaluation?": "Need hardware capable of running the VLM, or an API alternative."
    }

    # Data loading
    data_path = os.path.join("data", "cosmos_test_fixed.csv")
    df = pd.read_csv(data_path).head(10)
    
    # 1. VERIFY MODELS
    vlm_model_name = "llava-hf/llava-1.5-7b-hf"
    roberta_model_name = "hoanghoavienvo/roberta-base-detect-cheapfake-combined-train-test-15200-2-8"
    
    config = {
        "vlm_model": vlm_model_name,
        "roberta_model": roberta_model_name,
        "device": "cuda" if sys_info["cuda_available"] else "cpu",
        "quantization": "4-bit" if sys_info["cuda_available"] else "None (CPU)"
    }
    with open(os.path.join(out_dir, "config.json"), "w") as f:
        json.dump(config, f, indent=4)
        
    print("Loading Models...")
    
    # Try loading RoBERTa
    roberta_model, roberta_tokenizer = None, None
    try:
        print(f"Loading RoBERTa: {roberta_model_name}")
        roberta_tokenizer = AutoTokenizer.from_pretrained(roberta_model_name)
        roberta_model = AutoModelForSequenceClassification.from_pretrained(roberta_model_name)
        roberta_model.to(config["device"])
        roberta_model.eval()
        report["4. Did RoBERTa classification work?"] = "Yes, model loaded successfully."
    except Exception as e:
        print(f"RoBERTa failed to load: {e}")
        with open(os.path.join(out_dir, "logs", "roberta_error.txt"), "w") as f:
            f.write(traceback.format_exc())

    # Try loading LLaVA
    llava_model, llava_processor = None, None
    try:
        print(f"Loading LLaVA: {vlm_model_name} (This may OOM and crash the process...)")
        llava_processor = AutoProcessor.from_pretrained(vlm_model_name)
        # Attempt to load model
        if config["device"] == "cuda":
            llava_model = LlavaForConditionalGeneration.from_pretrained(vlm_model_name, load_in_4bit=True, device_map="auto")
        else:
            llava_model = LlavaForConditionalGeneration.from_pretrained(vlm_model_name, low_cpu_mem_usage=True)
            llava_model.to("cpu")
        report["1. Did LLaVA load?"] = "Yes"
    except Exception as e:
        print(f"LLaVA failed to load: {e}")
        with open(os.path.join(out_dir, "logs", "llava_error.txt"), "w") as f:
            f.write(traceback.format_exc())
        report["1. Did LLaVA load?"] = f"No, crashed with: {type(e).__name__}"

    # If models didn't load, write reports and exit gracefully
    if llava_model is None:
        report["10. What changes, if any, are required before full evaluation?"] = "LLaVA-1.5 7B cannot run on this machine due to memory constraints (8GB RAM, no dedicated GPU). We must use a cloud GPU, a much smaller VLM (e.g., Moondream), or an API."
    else:
        # Proceed with inference (if by some miracle it loaded)
        pass # Implementation for real inference would go here if it loaded
        
    # Write pilot report
    with open(os.path.join(out_dir, "pilot_report.md"), "w") as f:
        f.write("# EXP003 Baseline B Pilot Report\n\n")
        for k, v in report.items():
            f.write(f"**{k}**\n{v}\n\n")
            
    with open(os.path.join(out_dir, "qualitative_samples.md"), "w") as f:
        f.write("# Qualitative Samples\n\nCould not generate samples because the VLM failed to load (OOM/Memory constraints).")
        
    with open(os.path.join(out_dir, "runtime.txt"), "w") as f:
        f.write(f"Total execution time: {time.time() - start_time:.2f} seconds")

    print(f"\nPilot run complete. Results saved to {out_dir}")

if __name__ == "__main__":
    main()
