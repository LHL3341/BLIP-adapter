# based on: https://github.com/haltakov/natural-language-image-search
from tqdm import tqdm
import json
from collections import defaultdict
from glob import glob
import os
import numpy as np
import torch
from PIL import Image
from pathlib import Path
import argparse


def find_best_matches(text_features, photo_features):
    similarities = (photo_features @ text_features.T).squeeze(1)
    best_photo_idx = (-similarities).argsort()
    similarities = -similarities
    unsorted_sims = np.copy(similarities)
    similarities.sort()
    return best_photo_idx, similarities, unsorted_sims

parser = argparse.ArgumentParser()
parser.add_argument('--descr_path', type=str, default='../data/valid_data.json')
parser.add_argument('--imgs_path', type=str, default='../data/image-set/')
args = parser.parse_args()
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f'USING DEVICE: {device}')

correct = 0
total = 0
vid_correct = 0
vid_total = 0
img_correct = 0
img_total = 0

img_dirs = args.imgs_path
descriptions = json.load(open(args.descr_path, 'r'))
results = defaultdict(dict)
for img_dir, data in tqdm(descriptions.items()):
    for img_idx, text in data.items():
        img_files = list((Path(img_dirs) / img_dir).glob("*.jpg"))
        img_files = sorted(img_files, key=lambda x: int(str(x).split('/')[-1].split('.')[0][3:]))
        ranked_idx, sim, unsorted_sims = find_best_matches(text_emb, img_embs)
        ranked_files = [str(img_files[rank]).split('/')[-1][:-4] for rank in ranked_idx]
        target = str(img_files[int(img_idx)]).split('/')[-1][:-4]
        total += 1
        results[img_dir].update({f'raw_preds_{img_idx}': unsorted_sims.tolist(), f'clip_pred_{img_idx}': int(ranked_idx[0]) ,f'correct_{img_idx}': 1 if ranked_files[0] == target else 0})
        if ranked_files[0] == target:
            correct += 1
        if 'open-images' in img_dir:
            img_total += 1
            if ranked_files[0] == target:
                img_correct += 1
        else:
            vid_total += 1
            if ranked_files[0] == target:
                vid_correct += 1        


print('OVERALL ACC: ' + str(round(correct/total,4)))
print('VIDEO ACC: ' + str(round(vid_correct/vid_total,4)))
print('IMG ACC: ' + str(round(img_correct/img_total,4)))
json.dump(results, open(f'results/zero_test.json', 'w'), indent=2)