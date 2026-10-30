# COSMOS-FIXED-v1 Dataset Split Definition

**100 samples (`cosmos_dev_100.csv`):**
Development/tuning only. These samples were used to establish the logical rules and thresholds for Baseline A.

**900 samples (`cosmos_test_900.csv`):**
Final held-out evaluation only. These are the exact 900 samples used for evaluating Baseline A and Baseline B.

**FREEZE NOTICE:**
The 900-sample held-out set is permanently frozen and must never be changed based on model results. All future baselines and methods must be evaluated against this exact set to ensure fair and scientifically valid comparability.
