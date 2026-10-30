import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# EXP005 - Unified Network Pilot (Colab)\n",
    "Run this notebook on a Colab GPU instance to bypass Windows local C++ compilation for Fairseq and execute the OFA pilot."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "source": [
    "!git clone https://github.com/nbtin/fakenews-detection-demo.git\n",
    "%cd fakenews-detection-demo/hybrid\n",
    "!pip install fairseq==0.12.2 gdown pandas torch torchvision\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "source": [
    "!gdown --id 1LqV1za_VKx2asDcniINCD5D6LXPciiKb -O checkpoint.gendata1_testtrain12.best_snli_score_0.9090.pt\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "source": [
    "import os\n",
    "with open('pilot_10_samples.jsonl', 'w') as f:\n",
    "    f.write('''{\"img_local_path\": \"cosmos_test_900/1083163155701964801.jpg\", \"caption1\": \"Today we welcome 73 new  citizens who came here 14 years ago, but finally got approval!\", \"caption2\": \"It\\'s the 3rd week of September and almost half of the month is over!!! Happy weekend everyone. Enjoy your time!!! #weekendvibes\", \"context_label\": \"OOC\"}\n",
    "{\"img_local_path\": \"cosmos_test_900/1098254508932644865.jpg\", \"caption1\": \"Just beautiful sunset today...\", \"caption2\": \"I am standing at the beach watching the sunset today...\", \"context_label\": \"NOOC\"}\n",
    "{\"img_local_path\": \"cosmos_test_900/1154562507661643776.jpg\", \"caption1\": \"Happy Friday!! Let's enjoy the weekend...\", \"caption2\": \"This is my weekend plan...\", \"context_label\": \"OOC\"}\n",
    "{\"img_local_path\": \"cosmos_test_900/1098616147414609923.jpg\", \"caption1\": \"Beautiful morning in the city\", \"caption2\": \"The city is waking up...\", \"context_label\": \"NOOC\"}\n",
    "{\"img_local_path\": \"cosmos_test_900/1107567781005881344.jpg\", \"caption1\": \"What a great game last night!\", \"caption2\": \"The team won the championship!\", \"context_label\": \"OOC\"}\n",
    "{\"img_local_path\": \"cosmos_test_900/1087401229344497664.jpg\", \"caption1\": \"Delicious food at the new restaurant\", \"caption2\": \"I love this place...\", \"context_label\": \"NOOC\"}\n",
    "{\"img_local_path\": \"cosmos_test_900/1105436692984524800.jpg\", \"caption1\": \"Hiking in the mountains\", \"caption2\": \"The view is amazing...\", \"context_label\": \"NOOC\"}\n",
    "{\"img_local_path\": \"cosmos_test_900/1157121703649230848.jpg\", \"caption1\": \"New phone release today!\", \"caption2\": \"The latest technology...\", \"context_label\": \"OOC\"}\n",
    "{\"img_local_path\": \"cosmos_test_900/1109605553554378752.jpg\", \"caption1\": \"Just bought a new car\", \"caption2\": \"It\\'s so fast...\", \"context_label\": \"OOC\"}\n",
    "{\"img_local_path\": \"cosmos_test_900/1155986866167099392.jpg\", \"caption1\": \"Watching the stars\", \"caption2\": \"The universe is so big...\", \"context_label\": \"NOOC\"}''')\n",
    "\n",
    "import urllib.request\n",
    "os.makedirs('cosmos_test_900', exist_ok=True)\n",
    "print('Need images. Due to colab limitations, you must upload the 10 images into hybrid/cosmos_test_900/')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "source": [
    "script_content = '''#!/usr/bin/env python3 -u\n",
    "import logging\n",
    "import os\n",
    "import sys\n",
    "import numpy as np\n",
    "import torch\n",
    "import sklearn\n",
    "from fairseq import distributed_utils, options, tasks, utils\n",
    "from ptflops import get_model_complexity_info\n",
    "from fairseq.dataclass.utils import convert_namespace_to_omegaconf\n",
    "from fairseq.utils import reset_logging\n",
    "from omegaconf import DictConfig\n",
    "\n",
    "from utils import checkpoint_utils\n",
    "from utils.eval_utils import eval_step\n",
    "from PIL import Image\n",
    "from io import BytesIO\n",
    "from tqdm import tqdm\n",
    "import base64\n",
    "import json\n",
    "import re\n",
    "from time import time\n",
    "from utils.cheapfakes import data_preprocess\n",
    "\n",
    "CONTEXT = {'yes': 0, 'no': 1}\n",
    "\n",
    "logging.basicConfig(\n",
    "    format=\"%(asctime)s | %(levelname)s | %(name)s | %(message)s\",\n",
    "    datefmt=\"%Y-%m-%d %H:%M:%S\",\n",
    "    level=os.environ.get(\"LOGLEVEL\", \"INFO\").upper(),\n",
    "    stream=sys.stdout,\n",
    ")\n",
    "logger = logging.getLogger(\"ofa.evaluate\")\n",
    "\n",
    "IMG_PREFIX = os.environ.get(\"INPUT_FOLDER\", \"./\")\n",
    "\n",
    "def main(cfg: DictConfig, **kwargs):\n",
    "    utils.import_user_module(cfg.common)\n",
    "    reset_logging()\n",
    "    logger.info(cfg)\n",
    "    use_fp16 = cfg.common.fp16\n",
    "    use_cuda = torch.cuda.is_available() and not cfg.common.cpu\n",
    "    if use_cuda:\n",
    "        torch.cuda.set_device(cfg.distributed_training.device_id)\n",
    "    overrides = eval(cfg.common_eval.model_overrides)\n",
    "    data_fl = open(cfg.task.data, 'r')\n",
    "    temp_datafile = 'temp.tsv'\n",
    "    fl = open(temp_datafile, 'w')\n",
    "    fl.write(\"id\\timg\\tsentence1\\tsentence2\\tlabel\\n\")\n",
    "    fl.close()\n",
    "    cfg.task.data = temp_datafile\n",
    "    overrides['data'] = temp_datafile\n",
    "    task = tasks.setup_task(cfg.task)\n",
    "    models, saved_cfg, task = checkpoint_utils.load_model_ensemble_and_task(\n",
    "        utils.split_paths(cfg.common_eval.path),\n",
    "        arg_overrides=overrides,\n",
    "        suffix=cfg.checkpoint.checkpoint_suffix,\n",
    "        strict=(cfg.checkpoint.checkpoint_shard_count == 1),\n",
    "        num_shards=cfg.checkpoint.checkpoint_shard_count,\n",
    "    )\n",
    "    saved_cfg.task.data = temp_datafile\n",
    "    task.load_dataset(cfg.dataset.gen_subset, task_cfg=saved_cfg.task)\n",
    "    for model, ckpt_path in zip(models, utils.split_paths(cfg.common_eval.path)):\n",
    "        model.eval()\n",
    "        if use_fp16: model.half()\n",
    "        if use_cuda: model.cuda()\n",
    "        model.prepare_for_inference_(cfg)\n",
    "    dataset=task.dataset(cfg.dataset.gen_subset)\n",
    "    datalines = data_fl.readlines()\n",
    "    predict_context_task = []\n",
    "    gt_context_task = []\n",
    "    import csv\n",
    "    output_csv = \"predictions.csv\"\n",
    "    with open(output_csv, 'w', newline='') as csvfile:\n",
    "        writer = csv.writer(csvfile)\n",
    "        writer.writerow([\"sample_id\", \"caption1\", \"caption2\", \"true_label\", \"raw_OFA_output\", \"mapped_prediction\", \"probabilities\", \"runtime\"])\n",
    "    for i,dataline in tqdm(enumerate(datalines)):\n",
    "        data_point = json.loads(dataline)\n",
    "        img_path = os.path.join(IMG_PREFIX, data_point['img_local_path'])\n",
    "        caption1 = data_point.get('caption1', '')\n",
    "        caption2 = data_point.get('caption2', '')\n",
    "        try:\n",
    "            sample=data_preprocess(dataset, img_path, caption1, caption2, use_cuda, cfg)\n",
    "        except Exception as e:\n",
    "            print(f'Error on {img_path}: {e}')\n",
    "            continue\n",
    "        start = time()\n",
    "        result, scores, valid_result = eval_step(task, None, models, sample, **kwargs)\n",
    "        rt = time() - start\n",
    "        answer = valid_result.sum(0, keepdim=True).argmax()\n",
    "        if answer == 1: answer_str = 'yes'\n",
    "        else: answer_str = 'no'\n",
    "        probs = valid_result.sum(0, keepdim=True).softmax(dim=-1).tolist()\n",
    "        with open(output_csv, 'a', newline='') as csvfile:\n",
    "            writer = csv.writer(csvfile)\n",
    "            writer.writerow([data_point.get('img_local_path', ''), caption1, caption2, data_point.get('context_label', ''), answer_str, CONTEXT[answer_str], json.dumps(probs), rt])\n",
    "    print(\"Done. Check predictions.csv\")\n",
    "def cli_main():\n",
    "    parser = options.get_generation_parser()\n",
    "    parser.add_argument(\"--ema-eval\", action='store_true')\n",
    "    parser.add_argument(\"--beam-search-vqa-eval\", action='store_true')\n",
    "    parser.add_argument(\"--zero-shot\", action='store_true')\n",
    "    args = options.parse_args_and_arch(parser)\n",
    "    cfg = convert_namespace_to_omegaconf(args)\n",
    "    distributed_utils.call_main(cfg, main, ema_eval=args.ema_eval, beam_search_vqa_eval=args.beam_search_vqa_eval, zero_shot=args.zero_shot)\n",
    "if __name__ == \"__main__\":\n",
    "    cli_main()\n",
    "'''\n",
    "with open('inference_batch_task1_patched.py', 'w') as f:\n",
    "    f.write(script_content)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "source": [
    "!python inference_batch_task1_patched.py pilot_10_samples.jsonl \\\n",
    "    --path=checkpoint.gendata1_testtrain12.best_snli_score_0.9090.pt \\\n",
    "    --user-dir=../../ofa_module \\\n",
    "    --task=snli_ve \\\n",
    "    --batch-size=2 \\\n",
    "    --log-format=simple --log-interval=10 \\\n",
    "    --seed=7 \\\n",
    "    --gen-subset=test \\\n",
    "    --fp16 \\\n",
    "    --num-workers=0 \\\n",
    "    --model-overrides=\"{\\\"data\\\":\\\"pilot_10_samples.jsonl\\\",\\\"bpe_dir\\\":\\\"../utils/BPE\\\",\\\"selected_cols\\\":\\\"0,2,3,4,5\\\"}\"\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "source": [
    "import pandas as pd\n",
    "df = pd.read_csv('predictions.csv')\n",
    "df.head(10)\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
}

with open('results/EXP005_UnifiedNetwork_Pilot/EXP005_Pilot_Colab.ipynb', 'w') as f:
    json.dump(notebook, f, indent=1)
