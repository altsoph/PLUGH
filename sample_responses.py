import json
import argparse
from typing import Dict, List, Optional, Tuple

from openai import OpenAI
import anthropic

client = OpenAI()


prompt_parts = {
    'task1.system': 'You will be provided with a short fiction text. Your task is to extract mentioned locations and compile a description of locations graph in a graphviz format, undirected, without nodes description, only with edges without labels for directly connected nodes.',
    'task2a.system': 'You will be provided with a short fiction text and a list of location names. Your task is to extract the main character\'s path as a sequence of visited locations, one by one, each on a new line.',
    'task2b.system': "You will be provided with a short fiction text and a list of location names. Your task is to extract the main character\'s path as a sequence of visited locations in reverse order, one by one, each on a new line.",
    'task3.system': 'You will be provided with a short fiction text and a list of location names. Your task is to extract the shortest path between two given locations (source and target) as a sequence of visited locations starting from the source and ending with the target location, one by one, each on a new line.',
    'task4.system': 'You will be provided with a short fiction text and a list of location names. Your task is to extract the shortest path between two given locations (source and target) as a sequence of visited locations starting from the source and ending with the target location, one by one, each on a new line.',
    'text_prefix': "# Input text\n\n",
    'locations_prefix': "\n\n# Locations\n\n",
    'markers_prefix': "\n\n# Source and target\n\n",
    'response_prefix': "# Response\n\n",
}

def prepare_chat_prompt(task_data, task_type, examples=0):
    messages = []
    messages.append( {"role": "system", "content": prompt_parts[f"{task_type}.system"]} )
    task_num = task_type[:-1] if task_type[-1] in "ab" else task_type
    for example in task_data[task_num]['few_shots'][:examples]:
        if task_num == 'task1':
            messages.append( {"role": "user", "content": f"{prompt_parts['text_prefix']}{example[0]}"} )
        elif task_num == 'task2':
            locations = "\n".join(example[1])
            messages.append( {"role": "user", "content": f"{prompt_parts['text_prefix']}{example[0]}{prompt_parts['locations_prefix']}{locations}"} )
        else:
            locations = "\n".join(example[1])
            endpoints = f"{example[2][0]}\n{example[2][-1]}"
            messages.append( {"role": "user", "content": f"{prompt_parts['text_prefix']}{example[0]}{prompt_parts['locations_prefix']}{locations}{prompt_parts['markers_prefix']}{endpoints}"} )
            
        if task_type in ('task2a', 'task3', 'task4'):
            messages.append( {"role": "assistant", "content": "\n".join(example[-1])} )
        elif task_type=='task1':
            messages.append( {"role": "assistant", "content": example[-1]} )
        elif task_type=='task2b':
            messages.append( {"role": "assistant", "content": "\n".join(example[-1][::-1])} )
        
    if task_num == 'task1':
        messages.append( {"role": "user", "content": f"{prompt_parts['text_prefix']}{task_data['text']}"} )
    elif task_num == 'task2':
        locations = "\n".join(task_data['locations'])
        messages.append( {"role": "user", "content": f"{prompt_parts['text_prefix']}{task_data['text']}{prompt_parts['locations_prefix']}{locations}"} )
    elif task_num == 'task3':
        locations = "\n".join(task_data['locations'])
        endpoints = f"{task_data[task_num]['from']}\n{task_data[task_num]['to']}"
        messages.append( {"role": "user", "content": f"{prompt_parts['text_prefix']}{task_data['text']}{prompt_parts['locations_prefix']}{locations}{prompt_parts['markers_prefix']}{endpoints}"} )
    elif task_num == 'task4':
        locations = "\n".join(task_data['locations'])
        endpoints = f"{task_data[task_num]['from_marker']}\n{task_data[task_num]['to_marker']}"
        messages.append( {"role": "user", "content": f"{prompt_parts['text_prefix']}{task_data['text']}{prompt_parts['locations_prefix']}{locations}{prompt_parts['markers_prefix']}{endpoints}"} )
    return messages

def prepare_text_prompt(task_data, task_type, examples=0):
    messages = []
    messages.append( prompt_parts[f"{task_type}.system"] )
    task_num = task_type[:-1] if task_type[-1] in "ab" else task_type
    for example in task_data[task_num]['few_shots'][:examples]:
        if task_num == 'task1':
            messages.append( f"{prompt_parts['text_prefix']}{example[0]}" )
        elif task_num == 'task2':
            locations = "\n".join(example[1])
            messages.append( f"{prompt_parts['text_prefix']}{example[0]}{prompt_parts['locations_prefix']}{locations}" )
        else:
            locations = "\n".join(example[1])
            endpoints = f"{example[2][0]}\n{example[2][-1]}"
            messages.append( f"{prompt_parts['text_prefix']}{example[0]}{prompt_parts['locations_prefix']}{locations}{prompt_parts['markers_prefix']}{endpoints}" )
            
        if task_type in ('task2a', 'task3', 'task4'):
            messages.append( prompt_parts['response_prefix']+"\n".join(example[-1]) )
        elif task_type=='task1':
            messages.append( prompt_parts['response_prefix']+example[-1] )
        elif task_type=='task2b':
            messages.append( prompt_parts['response_prefix']+"\n".join(example[-1][::-1]) )

    if task_num == 'task1':
        messages.append( f"{prompt_parts['text_prefix']}{task_data['text']}" )
    elif task_num == 'task2':
        locations = "\n".join(task_data['locations'])
        messages.append( f"{prompt_parts['text_prefix']}{task_data['text']}{prompt_parts['locations_prefix']}{locations}" )
    elif task_num == 'task3':
        locations = "\n".join(task_data['locations'])
        endpoints = f"{task_data[task_num]['from']}\n{task_data[task_num]['to']}"
        messages.append( f"{prompt_parts['text_prefix']}{task_data['text']}{prompt_parts['locations_prefix']}{locations}{prompt_parts['markers_prefix']}{endpoints}" )
    elif task_num == 'task4':
        locations = "\n".join(task_data['locations'])
        endpoints = f"{task_data[task_num]['from_marker']}\n{task_data[task_num]['to_marker']}"
        messages.append( f"{prompt_parts['text_prefix']}{task_data['text']}{prompt_parts['locations_prefix']}{locations}{prompt_parts['markers_prefix']}{endpoints}" )
    messages.append( prompt_parts['response_prefix'] )
    return "\n\n".join(messages)

def query_model(api, model_id, prompt):
    if api=='openai':
        completion = client.chat.completions.create(
            model=model_id,
            messages=prompt,
            temperature=.01,
            max_tokens=4090,
        )
        return completion.choices[0].message.content
    elif api=="anthropic":
        completion = anthropic.Anthropic().messages.create(
            model=model_id,
            max_tokens=4090,
            system=prompt[0]['content'],
            temperature= 0.01,
            messages=prompt[1:],
        )
        return completion.content[0].text
    return None

def process_task(task_data, task_type, model='prompt:chat', examples=0):
    if model.startswith('openai:') or model.startswith('anthropic:') or model=='prompt:chat':
        prompt = prepare_chat_prompt(task_data, task_type, examples)
    else:
        prompt = prepare_text_prompt(task_data, task_type, examples)
    if model.startswith('prompt:'):
        return prompt
    api, model_id = model.split(':',1)
    return query_model(api, model_id, prompt)


def main(args):
    with open(args.input_file, encoding='utf-8') as fh:
        input_data = json.loads(fh.read())

    res = []
    for task in ('task1', 'task2a', 'task2b', 'task3', 'task4'):
        print('Processing task:', task)
        for shots in range(4):
            for idx, it in enumerate(input_data):
                if it['split'] == 'dev':
                    continue
                try:
                    response = process_task(it, task, args.model, examples=shots)
                    res.append( tuple((it['id'], task, args.model, shots, response)) )
                except:
                    print('ERR', idx, args.model, task, shots)
                    time.sleep(1)
            print(f'{shots}-shots done')

    with open(args.output_file, 'w', encoding='utf-8') as fh:
        json.dump(res, fh, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', type=str, 
                        default=None, required=True, 
                        help='Path to the file with benchmark data')
    parser.add_argument('-m', '--model', type=str, 
                        default=None, required=True, 
                        help='Name of the OpenAI model to query')
    parser.add_argument('-o', '--output-file', type=str, 
                        default=None, required=True, 
                        help='Path to the output json file')
    args = parser.parse_args()
    main(args)


