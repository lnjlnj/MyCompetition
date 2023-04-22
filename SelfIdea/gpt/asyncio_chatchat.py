import asyncio
import aiohttp
import json
import pandas as pd
import os
import csv
import tqdm

headers = {
    'accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
    'authorization': 'LYW666666',
    'Connection': 'keep-alive',
    'content-Type': 'application/json',
    'origin': 'http://xvx.ink',
    'referer': 'http://xvx.ink/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

async def chatchat_response(input:str):
    url = 'https://express-aqde-43397-8-1317793992.sh.run.tcloudbase.com/api/chat-process'
    data = {
      "prompt": input,
      "options": {}
    }
    n = 0
    while True:
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=100)) as session:
                async with session.post(url, json=data, headers=headers) as resp:
                    reward = await resp.text()
            break # 如果请求成功，跳出 while 循环
        except Exception as e:
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
    print(reward_dict['text'])
    return reward_dict['text']

async def main(input_list:list):
    # input_list = ['hello', 'how are you?', 'what is your name?']
    tasks = [chatchat_response(input_str) for input_str in input_list]
    results = await asyncio.gather(*tasks)

if __name__ == '__main__':

    args = {
        'save_path': './data/keyword.csv',
        'csv_headers': ['video_id', 'question', 'keyword', 'subtitle']
    }

    with open('./data/question_and_subtitles.json', 'r') as f:
        data = json.load(f)

    if os.path.exists(args['save_path']) is False:
        with open(args['save_path'], 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(args['csv_headers'])
        row_count = 0
    else:
        df = pd.read_csv(args['save_path'])
        row_count = len(df.index)

    new_data = []
    input_list = []
    for n in data:
        new_n = n
        text = ''
        for t in n['subtitle']:
            text += f',{t["text"]}'
        text = text[1:]
        prompt = '提取下面这段字幕内容的关键内容，要求以分号分开各部分且尽可能全面与详细:'
        question = prompt + text
        input_list.append(question)
        new_n['gpt_input'] = question
        new_data.append(new_n)

    new_input_list = input_list[:1]

    asyncio.run(main(new_input_list))