import requests
import json
import pandas as pd
import os
import csv
from tqdm import tqdm
from collections import OrderedDict
from transformers import AutoTokenizer

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
    'Authorization': 'LYW666666',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    # 'Host': '124.71.219.136:3002',
    'Origin': 'http://xvx.ink',
    'Referer': 'http://xvx.ink/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

tokenizer = AutoTokenizer.from_pretrained('IDEA-CCNL/Erlangshen-DeBERTa-v2-320M-Chinese')

def chatchat_respone(input:str):
    url = 'https://express-aqde-43397-8-1317793992.sh.run.tcloudbase.com/api/chat-process'
    data = {
      "prompt": input,
      "options": {}
    }
    n = 0
    while True:
        try:
            reward = requests.post(url, json=data, headers=headers, timeout=100).text
            break  # 如果请求成功，跳出 while 循环
        except:
            n += 1
            print(f"request time out, {n}th retry")
            continue
    s = ''
    record = []
    for n in reward:
        s += n
        if n == '\n':
            record.append(s)
            s = ''
    reward_dict = json.loads(record[-1])
    return reward_dict['text']


if __name__ == '__main__':

    args = {
        'save_path':'./data/keyword.csv',
        'csv_headers':['video_id', 'keyword']
    }

    with open('/home/ubuntu/sda_8T/codespace/new_lei/MyCompetition/task23/NLPCC_2023_CMIVQA_TRAIN_DEV/subtitle.json', 'r') as f:
        data = json.load(f)

    if os.path.exists(args['save_path']) is False:
        with open(args['save_path'], 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(args['csv_headers'])
        row_count = 0
    else:
        df = pd.read_csv(args['save_path'])
        row_count = len(df.index)

    index = 1
    data = OrderedDict(data)
    data = list(data.items())

    for n in tqdm(data):
        if index <= row_count:
            index += 1
            continue
        else:
            new_n = {'video_id':'', 'keyword':''}
            new_n['video_id'] = n[0]
            text = ''
            for t in n[1]:
                text += f',{t["text"]}'
            text = text[1:]
            prompt = '提取下面这段字幕内容的关键词，要求以分号分开各部分且尽可能全面与详细:'
            question = prompt + text
            token_nums = len(tokenizer(question).input_ids)
            if token_nums > 2200:
                new_n['keyword'] = 'too many tokens'
                new_df = pd.DataFrame(new_n, index=[0])
                new_df.to_csv(args['save_path'], mode='a', index=False, header=False)
            else:
                keyword = chatchat_respone(question)
                new_n['keyword'] = keyword
                new_df = pd.DataFrame(new_n, index=[0])
                new_df.to_csv(args['save_path'], mode='a', index=False, header=False)


