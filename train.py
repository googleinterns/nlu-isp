"""
Copyright 2020 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import os
import pathlib
import json
import random
import argparse
from collections import defaultdict, Counter
project_root = pathlib.Path(__file__).parents[1]

from utils.module import ModelManager
from utils.loader import DatasetManager
from utils.process import Processor
from utils.fscore import FScore
from utils.logging_utils import ColoredLog

import torch
import numpy as np

parser = argparse.ArgumentParser()

# Training parameters.
parser.add_argument('--continue_training', default=True)
parser.add_argument('--data_name', type=str, default='atis')
parser.add_argument('--save_base', '-sd', type=str, default='save')
parser.add_argument('--mtype', type=str, default="reg")
#  type = ["base", "reg", "ub"]
parser.add_argument('--anticipation_size', "-as", type=int, default=2)

parser.add_argument("--random_state", '-rs', type=int, default=0)
parser.add_argument('--num_epoch', '-ne', type=int, default=1)
parser.add_argument('--batch_size', '-bs', type=int, default=16)
parser.add_argument('--l2_penalty', '-lp', type=float, default=1e-6)
parser.add_argument("--learning_rate", '-lr', type=float, default=0.001)
parser.add_argument('--dropout_rate', '-dr', type=float, default=0.4)
parser.add_argument('--intent_forcing_rate', '-ifr', type=float, default=0.9)
parser.add_argument("--differentiable", "-d", action="store_true", default=False)
parser.add_argument('--slot_forcing_rate', '-sfr', type=float, default=0.9)

# model parameters.
parser.add_argument('--word_embedding_dim', '-wed', type=int, default=64)
parser.add_argument('--encoder_hidden_dim', '-ehd', type=int, default=256)
parser.add_argument('--intent_embedding_dim', '-ied', type=int, default=8)
parser.add_argument('--slot_embedding_dim', '-sed', type=int, default=32)
parser.add_argument('--slot_decoder_hidden_dim', '-sdhd', type=int, default=64)
parser.add_argument('--intent_decoder_hidden_dim', '-idhd', type=int, default=64)
parser.add_argument('--attention_hidden_dim', '-ahd', type=int, default=1024)
parser.add_argument('--attention_output_dim', '-aod', type=int, default=128)

if __name__ == "__main__":
    args = parser.parse_args()
    args.data_dir = os.path.join(project_root, "data", args.data_name)
    args.save_dir = os.path.join(args.data_dir, f"{args.save_base}-{args.mtype}")

    # Save training and model parameters.
    if not os.path.exists(args.save_dir):
        os.system("mkdir -p " + args.save_dir)

    log_path = os.path.join(args.save_dir, "param.json")
    with open(log_path, "w") as fw:
        fw.write(json.dumps(args.__dict__, indent=True))

    # Fix the random seed of package random.
    random.seed(args.random_state)
    np.random.seed(args.random_state)

    # Fix the random seed of Pytorch when using GPU.
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.random_state)
        torch.cuda.manual_seed(args.random_state)

    # Fix the random seed of Pytorch when using CPU.
    torch.manual_seed(args.random_state)
    torch.random.manual_seed(args.random_state)

    # Instantiate a dataset object.
    dataset = DatasetManager(args)
    dataset.quick_build()
    dataset.show_summary()

    # Instantiate a network model object.
    if args.continue_training and os.path.exists(os.path.join(args.save_dir, "model/model.pkl")):
        print(f"continue from existing model at {os.path.join(args.save_dir, 'model/model.pkl')}")
        model = torch.load(os.path.join(args.save_dir, "model/model.pkl"))
    else:
        model = ModelManager(
            args, len(dataset.word_alphabet),
            len(dataset.slot_alphabet),
            len(dataset.intent_alphabet))

    model.show_summary()

    # To train and evaluate the models.
    process = Processor(dataset, model, args.batch_size)
    process.train()

    res, pred = Processor.validate(os.path.join(args.save_dir, "model/model.pkl"), os.path.join(args.save_dir, "model/dataset.pkl"), args.batch_size)
