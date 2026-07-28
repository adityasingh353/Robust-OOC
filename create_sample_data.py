"""
Create a sample/mock COSMOS test dataset for development and testing.
This allows us to develop and test the pipeline before real COSMOS data is available.
"""

import json
import os
from pathlib import Path

# Sample COSMOS test data structure
SAMPLE_TEST_DATA = [
    {
        "image_id": 0,
        "img_local_path": "images/sample_001.jpg",
        "caption1": "A young child holding a birthday cake with lit candles",
        "caption2": "The president announcing new climate policies during a press conference",
        "label": 1,  # OOC: completely different context
        "maskrcnn_bboxes": [[10, 10, 100, 100], [50, 50, 150, 150]]
    },
    {
        "image_id": 1,
        "img_local_path": "images/sample_002.jpg",
        "caption1": "A doctor performing surgery in a hospital operating room",
        "caption2": "A doctor examining a patient during a routine checkup",
        "label": 0,  # NOOC: both captions match the medical context
        "maskrcnn_bboxes": [[20, 20, 200, 200]]
    },
    {
        "image_id": 2,
        "img_local_path": "images/sample_003.jpg",
        "caption1": "Athletes running in a marathon race on a city street",
        "caption2": "A famous actor walking the red carpet at a movie premiere",
        "label": 1,  # OOC: sports vs entertainment
        "maskrcnn_bboxes": [[30, 30, 300, 300], [100, 100, 250, 250]]
    },
    {
        "image_id": 3,
        "img_local_path": "images/sample_004.jpg",
        "caption1": "A family enjoying breakfast together at their kitchen table",
        "caption2": "Children having fun at a birthday party with cake and decorations",
        "label": 0,  # NOOC: both are family gathering contexts
        "maskrcnn_bboxes": [[40, 40, 350, 350]]
    },
    {
        "image_id": 4,
        "img_local_path": "images/sample_005.jpg",
        "caption1": "The Eiffel Tower during sunset with tourists on the grounds",
        "caption2": "A military tank rolling through a city street during conflict",
        "label": 1,  # OOC: tourism vs war
        "maskrcnn_bboxes": [[0, 0, 500, 500]]
    },
    {
        "image_id": 5,
        "img_local_path": "images/sample_006.jpg",
        "caption1": "A wedding couple cutting their wedding cake during the reception",
        "caption2": "Newlyweds dancing together at their wedding reception",
        "label": 0,  # NOOC: both are wedding scenes
        "maskrcnn_bboxes": [[50, 50, 400, 400], [150, 150, 450, 450]]
    },
    {
        "image_id": 6,
        "img_local_path": "images/sample_007.jpg",
        "caption1": "A wild tiger walking through the jungle",
        "caption2": "A tiger in the zoo behind a protective barrier",
        "label": 0,  # NOOC: both are tiger images (different context but both valid)
        "maskrcnn_bboxes": [[10, 10, 480, 480]]
    },
    {
        "image_id": 7,
        "img_local_path": "images/sample_008.jpg",
        "caption1": "A nurse comforting a patient in a hospital bed",
        "caption2": "A rocket launching into space during a space mission",
        "label": 1,  # OOC: healthcare vs space
        "maskrcnn_bboxes": [[20, 20, 350, 350]]
    },
    {
        "image_id": 8,
        "img_local_path": "images/sample_009.jpg",
        "caption1": "Students studying together in a university library",
        "caption2": "Students sitting in a classroom listening to a lecture",
        "label": 0,  # NOOC: both are education contexts
        "maskrcnn_bboxes": [[30, 30, 400, 400], [80, 80, 350, 350]]
    },
    {
        "image_id": 9,
        "img_local_path": "images/sample_010.jpg",
        "caption1": "A beautiful sunset over the ocean horizon",
        "caption2": "A tornado destroying buildings in a rural area",
        "label": 1,  # OOC: nature beauty vs disaster
        "maskrcnn_bboxes": [[0, 0, 512, 512]]
    },
]

def create_sample_cosmos_test():
    """Create sample COSMOS test data."""
    project_root = Path(__file__).parent
    
    # Save as test.json in temp_cosmos
    temp_cosmos_dir = project_root / "temp_cosmos"
    temp_cosmos_dir.mkdir(exist_ok=True)
    
    test_json_path = temp_cosmos_dir / "test.json"
    
    # Write sample data
    with open(str(test_json_path), 'w') as f:
        json.dump(SAMPLE_TEST_DATA, f, indent=2)
    
    print(f"✓ Sample COSMOS test.json created: {test_json_path}")
    print(f"  - {len(SAMPLE_TEST_DATA)} sample records")
    print(f"  - Format: COSMOS test set with caption pairs and OOC/NOOC labels")
    
    # Create images directory (even though images won't exist yet)
    images_dir = temp_cosmos_dir / "images"
    images_dir.mkdir(exist_ok=True)
    print(f"✓ Images directory created: {images_dir}")
    
    return test_json_path

if __name__ == "__main__":
    create_sample_cosmos_test()
