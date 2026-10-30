# DATASET SPLIT FREEZE REPORT

## 1. Current Dataset Identified
- **Path:** `data/cosmos_test_fixed.csv`
- **Total Rows:** 1000
- **Sample ID Column:** `image_id`
- **Label Distribution:** {'OOC': 513, 'NOOC': 487}

## 2. Existing 900 IDs Verification
- **Baseline A 900 IDs verified?** Yes
- **Baseline B evaluated all 900 IDs?** Yes
- **Are Baseline A IDs exactly the last 900 of the full dataset?** Yes
- **Duplicate IDs in Baseline A predictions?** None
- **Duplicate IDs in Baseline B subset?** None
- **Baseline A and Baseline B ID match:** Exactly 900 overlapping IDs confirmed.

## 3. Files Created
The following files were successfully created in `data/COSMOS-FIXED-v1/`:
1. `cosmos_dev_100.csv` (100 tuning samples)
2. `cosmos_test_900.csv` (900 held-out samples)
3. `split_manifest.json` (Contains dataset hashes and exact ID arrays)
4. `SPLIT_DEFINITION.md` (Usage rules)

No existing results or history files were overwritten.
