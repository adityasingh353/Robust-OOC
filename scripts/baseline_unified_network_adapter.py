import pandas as pd
import json

df = pd.read_csv('results/EXP005_UnifiedNetwork_Pilot/pilot_10_samples.csv')
output = []
for index, row in df.iterrows():
    # The inference script expects img_local_path, caption1, caption2, context_label
    d = {
        'img_local_path': row['image_path_or_url'],
        'caption1': row['caption1'],
        'caption2': row['caption2'],
        'context_label': row['label']
    }
    output.append(json.dumps(d))

with open('results/EXP005_UnifiedNetwork_Pilot/pilot_10_samples.jsonl', 'w') as f:
    f.write('\n'.join(output))

print("Created pilot_10_samples.jsonl")
