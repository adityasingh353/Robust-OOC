# RobustOOC Project Structure

## Phase 1, Task 1: Fixed COSMOS Test Dataset — ✅ COMPLETE

### Summary
- **File created**: `data/cosmos_test_fixed.csv`
- **Total samples**: 10 (sample/mock data for development)
- **Label distribution**: 5 OOC (50%), 5 NOOC (50%)
- **Columns**: `image_id`, `image_path_or_url`, `caption1`, `caption2`, `label`

### Current Status
✅ **Sample dataset ready** — 10 mock COSMOS examples with realistic caption pairs and OOC/NOOC labels
- This dataset is **fixed and permanent** for testing
- Same structure will be used for real COSMOS data (1000 samples)
- All evaluation methods will use exactly this file

### How to Replace with Real COSMOS Dataset

**Step 1: Get the real COSMOS data**
1. Visit: https://github.com/shivangi-aneja/COSMOS
2. Fill out the dataset request form: https://docs.google.com/forms/d/13kJQ2wlv7sxyXoaM1Ddon6Nq7dUJY_oftl-6xzwTGow
3. Download the provided dataset files

**Step 2: Prepare the JSON**
The COSMOS test.json should have this structure:
```json
[
  {
    "image_id": 0,
    "img_local_path": "path/to/image.jpg",
    "caption1": "Caption text for image",
    "caption2": "Different caption for same image",
    "label": 1,  // 1 = OOC, 0 = NOOC
    "maskrcnn_bboxes": [[x1, y1, x2, y2], ...]
  },
  ...
]
```

**Step 3: Place files**
- Copy `test.json` → `temp_cosmos/test.json`
- Copy image folder → `temp_cosmos/images/`

**Step 4: Regenerate CSV**
```bash
python prepare_cosmos_test.py
```

This will create `data/cosmos_test_fixed.csv` with real data, reporting:
- Total samples (should be 1000 for full COSMOS)
- Label distribution
- Image availability statistics
- 5 sample rows

---

## Project Directory Structure

```
RobustOOC/
├── data/
│   ├── cosmos_test_fixed.csv          ← FIXED test set (DO NOT MODIFY)
│   └── README.md
├── models/                             ← Baseline method implementations
├── eval/                               ← Evaluation scripts
├── results/                            ← Results & outputs
├── notebooks/                          ← Jupyter notebooks for analysis
├── temp_cosmos/                        ← COSMOS repo code (reference)
│   ├── test.json                       ← Test data (replace with real)
│   ├── images/                         ← Test images (to be populated)
│   └── ...
├── prepare_cosmos_test.py              ← Data preparation script
├── create_sample_data.py               ← Generate sample data
└── README.md                           ← This file
```

---

## Sample Dataset Preview

| image_id | caption1 | caption2 | label |
|----------|----------|----------|-------|
| cosmos_test_0000 | A young child holding a birthday cake with lit candles | The president announcing new climate policies during a press conference | OOC |
| cosmos_test_0001 | A doctor performing surgery in a hospital operating room | A doctor examining a patient during a routine checkup | NOOC |
| cosmos_test_0002 | Athletes running in a marathon race on a city street | A famous actor walking the red carpet at a movie premiere | OOC |
| cosmos_test_0003 | A family enjoying breakfast together at their kitchen table | Children having fun at a birthday party with cake and decorations | NOOC |
| cosmos_test_0004 | The Eiffel Tower during sunset with tourists on the grounds | A military tank rolling through a city street during conflict | OOC |

---

## Next Steps (Phase 1, Task 2)
1. Implement 2-4 lightweight baseline OOC detection methods
2. Evaluate all on `cosmos_test_fixed.csv`
3. Create fair comparison table

## Constraints Enforced
✅ Simple, incremental workflow  
✅ Fixed test set (no moving targets)  
✅ Small sample (10) for testing → scales to 1000  
✅ Clean repository structure  
✅ Ready for git commit  
