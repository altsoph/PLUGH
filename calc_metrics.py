import re
import json
import argparse
from collections import defaultdict

from tabulate import tabulate
import numpy as np
from Levenshtein import distance as ldist

def normalized_distance(p1, p2):
    return ldist(p1, p2)/max(len(p1), len(p2))

def normalize(n):
    n = n.lower()
    n = n.replace('_', ' ').replace("'", ' ')
    n = f" {n} ".replace(" the ", " ").replace(" a ", " ")
    n = n.strip().strip(';').strip('"').strip()
    n = re.sub(r"\[[^\]]+\]", ' ', n).strip()
    return n

def clean_path(p):
    r = []
    for l in p.split('\n'):
        if l.startswith('#'):
            continue
        if '*' in l:
            continue
        if not l.strip():
            continue
        l = re.sub(r'^\d+\.', '', l)
        l = l.lower().strip()
        r.append( l )
    return "\n".join(r)            

def extract_graph(raw):
    if raw is None:
        return [],[]
    if 'assistant\n\n' in raw:
        raw = raw.split('assistant\n\n',1)[0]
    # print([raw,])
    if '{' in raw:
        _, d = raw.split('{',1)
    else:
        d = raw
    if '}' in d:
        d = d.split('}')[-2]
    edges = []
    nodes = set()
    for l in d.split('\n'):
        l = l.replace(' -- ', ' -> ')
        if ' -> ' in l:
            n1, n2 = l.split(' -> ',1)
            n1 = normalize(n1)
            n2 = normalize(n2)
            if (n1, n2) not in edges and (n2, n1) not in edges:
                edges.append( (n1, n2) )
                nodes.add( n1 )
                nodes.add( n2 )
    return list(sorted(edges)), list(nodes)

def match_nodes(n1, n2):
    if n1 and n2 and (not (set(n1.split())-set(n2.split())) 
                      or not (set(n2.split())-set(n1.split()))):
        return True
    return False

def fuzzy_intersect_nodes(gt_n, pr_n):
    intersection = 0
    seen = set()
    for n1 in gt_n:
        for n2 in pr_n:
            if n2 not in seen and match_nodes(n1, n2):
                intersection += 1
                seen.add(n2)
                break
    return min(intersection, len(gt_n), len(pr_n))

def fuzzy_intersect_edges(gt_e, pr_e):
    intersection = 0
    seen = set()
    for e1 in gt_e:
        for e2 in pr_e:
            if e2 not in seen and fuzzy_intersect_nodes(e1, e2)==2:
                intersection += 1
                seen.add(e2)
                break
    return min(intersection, len(gt_e), len(pr_e))

def calc_task1_metric(ground_truth, predicted, entity='nodes', metric='f1', strict=True):
    intersection = 0
    pred_len = 0
    gt_len = 0
    if entity=='nodes':
        gt_n = set([normalize(n) for n,_ in ground_truth] + [normalize(n) for _,n in ground_truth])
        pr_n = set([normalize(n) for n,_ in predicted] + [normalize(n) for _,n in predicted])
        pred_len = len(pr_n)
        gt_len = len(gt_n)
        if strict:
            intersection = len(gt_n&pr_n)
        else:
            intersection = fuzzy_intersect_nodes(gt_n, pr_n)
    elif entity=='edges':
        gt_e = set( [frozenset([normalize(n) for n in e]) for e in ground_truth] )
        pr_e = set( [frozenset([normalize(n) for n in e]) for e in predicted] )
        pred_len = len(pr_e)
        gt_len = len(gt_e)
        if strict:
            intersection = len(gt_e&pr_e)
        else:
            intersection = fuzzy_intersect_edges(gt_e, pr_e)

    if not pred_len:
        return 0.
    prec = intersection/pred_len
    rec = intersection/gt_len
    if prec+rec:
        f1 = 2*prec*rec/(prec+rec)
    else:
        f1 = 0
    metrics = {'prec':prec, 'rec':rec, 'f1':f1}

    return metrics.get(metric, 0)

def calc_task2_metric(ground_truth, predicted, strict=True):
    if predicted is None:
        return 1.
    if strict:
        return normalized_distance(ground_truth, predicted.split('\n'))
    return normalized_distance(ground_truth, clean_path(predicted).split('\n'))

def calc_task3_metric(ground_truth, predicted, strict=True):
    return min(map(lambda x:calc_task2_metric( x, predicted, strict=strict), ground_truth)) 

def calc_task4_metric(ground_truth, predicted, strict=True):
    return min(map(lambda x:calc_task2_metric( x, predicted, strict=strict), ground_truth)) 


metrics_wrappers = {
    'task1': {
        'task1_strict_nodes_f1': lambda item,response: calc_task1_metric(item['task1']['target'], extract_graph(response)[0], entity='nodes', strict=True, metric='f1'),
        'task1_strict_edges_f1': lambda item,response: calc_task1_metric(item['task1']['target'], extract_graph(response)[0], entity='edges', strict=True, metric='f1'),
        'task1_fuzzy_nodes_f1':  lambda item,response: calc_task1_metric(item['task1']['target'], extract_graph(response)[0], entity='nodes', strict=False, metric='f1'),
        'task1_fuzzy_edges_f1':  lambda item,response: calc_task1_metric(item['task1']['target'], extract_graph(response)[0], entity='edges', strict=False, metric='f1'),

        'task1_strict_nodes_rec': lambda item,response: calc_task1_metric(item['task1']['target'], extract_graph(response)[0], entity='nodes', strict=True, metric='rec'),
        'task1_strict_edges_rec': lambda item,response: calc_task1_metric(item['task1']['target'], extract_graph(response)[0], entity='edges', strict=True, metric='rec'),
        'task1_fuzzy_nodes_rec':  lambda item,response: calc_task1_metric(item['task1']['target'], extract_graph(response)[0], entity='nodes', strict=False, metric='rec'),
        'task1_fuzzy_edges_rec':  lambda item,response: calc_task1_metric(item['task1']['target'], extract_graph(response)[0], entity='edges', strict=False, metric='rec'),

        'task1_strict_nodes_prec': lambda item,response: calc_task1_metric(item['task1']['target'], extract_graph(response)[0], entity='nodes', strict=True, metric='prec'),
        'task1_strict_edges_prec': lambda item,response: calc_task1_metric(item['task1']['target'], extract_graph(response)[0], entity='edges', strict=True, metric='prec'),
        'task1_fuzzy_nodes_prec':  lambda item,response: calc_task1_metric(item['task1']['target'], extract_graph(response)[0], entity='nodes', strict=False, metric='prec'),
        'task1_fuzzy_edges_prec':  lambda item,response: calc_task1_metric(item['task1']['target'], extract_graph(response)[0], entity='edges', strict=False, metric='prec'),
    },
    'task2a': {
        'task2a_strict_distance': lambda item,response: calc_task2_metric(item['task2']['target'], response, strict=True),
        'task2a_fuzzy_distance':  lambda item,response: calc_task2_metric(item['task2']['target'], response, strict=False),
    },
    'task2b': {
        'task2b_strict_distance': lambda item,response: calc_task2_metric(item['task2']['target'][::-1], response, strict=True),
        'task2b_fuzzy_distance':  lambda item,response: calc_task2_metric(item['task2']['target'][::-1], response, strict=False),
    },
    'task3': {
        'task3_strict_distance': lambda item,response: calc_task3_metric(item['task3']['target'], response, strict=True),
        'task3_fuzzy_distance':  lambda item,response: calc_task3_metric(item['task3']['target'], response, strict=False),
    },
    'task4': {
        'task4_strict_distance': lambda item,response: calc_task4_metric(item['task4']['target'], response, strict=True),
        'task4_fuzzy_distance':  lambda item,response: calc_task4_metric(item['task4']['target'], response, strict=False),
    },
}

def main(args):
    with open(args.input_file, encoding='utf-8') as fh:
        input_data = json.loads(fh.read())

    with open(args.response_file, encoding='utf-8') as fh:
        response_data = json.loads(fh.read())

    stats = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:defaultdict(list))))
    for idx, task, model, shots, response in response_data:
        if task not in metrics_wrappers:
            continue
        for metric in metrics_wrappers[task]:
            value = metrics_wrappers[task][metric]( input_data[idx], response )
            stats[task][metric][model][shots].append( value )

    for task in stats:
        print(f'\n\n# {task}')
        for metric in stats[task]:
            print(f'\n## {metric}')
            table = []
            for model in stats[task][metric]:
                row = [model, len(stats[task][metric][model][0])]
                for shots in stats[task][metric][model]:
                    row.append( f'{np.mean(stats[task][metric][model][shots]):0.1%}' )
                table.append( row )
            print (tabulate(table, headers=["model", "items"] + [f'{s}-shot' for s in stats[task][metric][model]]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', type=str, 
                        default=None, required=True, 
                        help='Path to the file with benchmark data')
    parser.add_argument('-r', '--response-file', type=str, 
                        default=None, required=True, 
                        help='Path to the file with model\'s responses')
    args = parser.parse_args()
    main(args)
