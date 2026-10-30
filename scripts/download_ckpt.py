import gdown
import os

output_path = 'results/EXP005_UnifiedNetwork/fakenews-detection-demo/checkpoint.gendata1_testtrain12.best_snli_score_0.9090.pt'
if not os.path.exists(output_path):
    print("Downloading checkpoint...")
    gdown.download(id='1LqV1za_VKx2asDcniINCD5D6LXPciiKb', output=output_path, quiet=False)
    print("Download finished.")
else:
    print("Checkpoint already exists.")
