import pandas as pd
import json
from transformers import AutoTokenizer

json_path = '/home/ubuntu/sda_8T/codespace/new_lei/MyCompetition/task23/NLPCC_2023_CMIVQA_TRAIN_DEV/subtitle.json'
train_path = '/home/ubuntu/sda_8T/codespace/new_lei/MyCompetition/task23/NLPCC_2023_CMIVQA_TRAIN_DEV/CMIVQA_Train_Dev.json'
# train_path = '/home/ubuntu/sda_8T/codespace/new_lei/MyCompetition/task23/NLPCC_2023_CMIVQA_TESTA/dataset_testA_for_track23.json'
with open(json_path, 'r') as f:
    subtitle = json.load(f)

with open(train_path, 'r') as f:
    question = json.load(f)

data = []
for n in question:
    try:
        data.append({'video_id':n['video_id'], 'question':n['question'], 'subtitle':subtitle[n['video_id']]})
    except:
        continue


with open('./question_and_subtitles.json', 'w') as f:
    json.dump(data, f)

# len(tokenizer(''.join(n['text'] for n in i['video_sub_title'])).input_ids)

print()