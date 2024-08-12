# PLUGH
This is a supplementary code for the paper "[PLUGH: A Benchmark for Spatial Understanding and Reasoning in Large Language Models](https://arxiv.org/abs/2408.04648)," accepted for Wordplay Workshop at ACL 2024.

## Abstract

We present PLUGH[\*](https://www.urbandictionary.com/define.php?term=plugh), a modern benchmark that currently consists of 5 tasks, each with 125 input texts extracted from 48 different games and representing 61 different (non-isomorphic) spatial graphs to assess the abilities of Large Language Models (LLMs) for spatial understanding and reasoning. Our evaluation of API-based and open-sourced LLMs shows that while some commercial LLMs exhibit strong reasoning abilities, open-sourced competitors can demonstrate almost the same level of quality; however, all models still have significant room for improvement. We identify typical reasons for LLM failures and discuss possible ways to deal with them. Datasets and evaluation code are released.

## Content
* `plugh.json` -- the benchmark data.
* `sample_responses.py` -- use this script to query models via OpenAI API or to generate the prompts, so you can use them to query any custom model.
* `plugh.responses.json` -- already sampled responses for several models mentioned in the paper.
* `calc_metrics.py` -- use this script to process responses, parse them, and calculate the benchmark metrics.


## Results
The run of `python calc_metrics.py -i plugh.json -r plugh.responses.json` should produce the following report:
```
# task1

## task1_strict_nodes_f1
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  55.2%     66.6%     70.7%     73.5%
openai:gpt-4-turbo-2024-04-09         113  73.2%     76.5%     76.4%     77.1%
anthropic:claude-3-opus-20240229      113  70.0%     77.5%     78.9%     81.4%
local:llama3_8b                       113  64.8%     60.1%     65.4%     67.1%
local:mixtral_8x7b                    113  25.2%     67.2%     69.0%     69.0%
local:llama3_70b                      113  68.0%     73.7%     74.0%     74.2%
local:mixtral_8x22b                   113  67.7%     75.3%     76.6%     75.4%
openai:gpt-4o-2024-05-13              113  71.7%     73.4%     74.7%     75.8%

## task1_strict_edges_f1
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  30.6%     42.0%     46.0%     49.5%
openai:gpt-4-turbo-2024-04-09         113  53.1%     56.4%     56.4%     57.4%
anthropic:claude-3-opus-20240229      113  50.7%     59.0%     60.4%     62.9%
local:llama3_8b                       113  41.1%     36.8%     40.3%     40.9%
local:mixtral_8x7b                    113  12.6%     41.4%     42.4%     44.6%
local:llama3_70b                      113  46.5%     53.1%     53.6%     54.2%
local:mixtral_8x22b                   113  45.8%     54.1%     56.2%     55.4%
openai:gpt-4o-2024-05-13              113  52.2%     53.7%     56.1%     57.4%

## task1_fuzzy_nodes_f1
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  64.6%     75.8%     81.3%     82.8%
openai:gpt-4-turbo-2024-04-09         113  82.9%     86.4%     86.3%     86.8%
anthropic:claude-3-opus-20240229      113  80.3%     87.1%     88.3%     90.7%
local:llama3_8b                       113  77.5%     70.3%     76.2%     78.6%
local:mixtral_8x7b                    113  29.2%     76.7%     79.1%     79.3%
local:llama3_70b                      113  78.9%     84.0%     85.4%     84.9%
local:mixtral_8x22b                   113  78.9%     85.2%     86.5%     84.7%
openai:gpt-4o-2024-05-13              113  82.0%     83.3%     84.3%     85.5%

## task1_fuzzy_edges_f1
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  41.4%     54.3%     60.4%     62.3%
openai:gpt-4-turbo-2024-04-09         113  67.1%     71.1%     71.3%     71.8%
anthropic:claude-3-opus-20240229      113  64.4%     74.3%     76.2%     79.0%
local:llama3_8b                       113  55.7%     50.9%     53.9%     57.2%
local:mixtral_8x7b                    113  17.0%     53.0%     55.6%     58.4%
local:llama3_70b                      113  61.6%     68.0%     70.1%     70.5%
local:mixtral_8x22b                   113  60.1%     68.5%     70.6%     68.8%
openai:gpt-4o-2024-05-13              113  66.8%     67.8%     70.8%     72.3%

## task1_strict_nodes_rec
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  73.7%     77.3%     76.8%     77.2%
openai:gpt-4-turbo-2024-04-09         113  76.5%     76.8%     75.6%     76.5%
anthropic:claude-3-opus-20240229      113  79.9%     81.4%     80.2%     81.1%
local:llama3_8b                       113  68.6%     70.1%     70.6%     70.7%
local:mixtral_8x7b                    113  30.5%     73.6%     73.0%     71.8%
local:llama3_70b                      113  75.6%     77.3%     76.4%     75.9%
local:mixtral_8x22b                   113  73.9%     77.1%     76.3%     74.2%
openai:gpt-4o-2024-05-13              113  78.8%     78.8%     78.7%     78.9%

## task1_strict_edges_rec
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  44.2%     52.5%     52.9%     54.8%
openai:gpt-4-turbo-2024-04-09         113  57.0%     56.7%     55.7%     56.9%
anthropic:claude-3-opus-20240229      113  58.0%     61.9%     61.1%     62.2%
local:llama3_8b                       113  48.2%     45.8%     45.9%     45.5%
local:mixtral_8x7b                    113  15.2%     46.9%     45.9%     48.2%
local:llama3_70b                      113  54.5%     57.9%     57.2%     56.5%
local:mixtral_8x22b                   113  51.1%     56.4%     56.0%     54.2%
openai:gpt-4o-2024-05-13              113  58.4%     58.2%     59.5%     60.0%

## task1_fuzzy_nodes_rec
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  87.6%     88.5%     88.7%     87.4%
openai:gpt-4-turbo-2024-04-09         113  86.7%     87.0%     85.4%     86.1%
anthropic:claude-3-opus-20240229      113  91.8%     91.5%     89.6%     90.6%
local:llama3_8b                       113  82.3%     82.0%     82.2%     83.1%
local:mixtral_8x7b                    113  35.3%     84.0%     83.7%     82.3%
local:llama3_70b                      113  88.2%     88.3%     88.3%     87.1%
local:mixtral_8x22b                   113  86.6%     87.4%     86.2%     83.5%
openai:gpt-4o-2024-05-13              113  90.4%     89.7%     88.8%     89.2%

## task1_fuzzy_edges_rec
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  62.2%     68.5%     70.5%     69.9%
openai:gpt-4-turbo-2024-04-09         113  71.9%     71.9%     70.4%     71.2%
anthropic:claude-3-opus-20240229      113  73.8%     78.0%     76.9%     78.2%
local:llama3_8b                       113  65.3%     64.1%     61.1%     63.6%
local:mixtral_8x7b                    113  21.2%     60.7%     60.6%     62.6%
local:llama3_70b                      113  72.5%     74.3%     74.7%     73.6%
local:mixtral_8x22b                   113  67.7%     71.6%     70.6%     67.5%
openai:gpt-4o-2024-05-13              113  75.1%     74.0%     75.1%     76.0%

## task1_strict_nodes_prec
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  50.0%     62.5%     68.5%     72.3%
openai:gpt-4-turbo-2024-04-09         113  72.4%     77.8%     78.7%     78.9%
anthropic:claude-3-opus-20240229      113  64.7%     75.6%     78.8%     82.6%
local:llama3_8b                       113  63.4%     55.6%     64.4%     66.5%
local:mixtral_8x7b                    113  23.0%     64.9%     67.9%     68.6%
local:llama3_70b                      113  63.8%     72.1%     73.1%     74.0%
local:mixtral_8x22b                   113  65.2%     75.1%     78.3%     78.2%
openai:gpt-4o-2024-05-13              113  67.6%     70.4%     72.7%     74.3%

## task1_strict_edges_prec
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  26.0%     37.1%     42.5%     46.6%
openai:gpt-4-turbo-2024-04-09         113  51.7%     57.3%     58.6%     59.2%
anthropic:claude-3-opus-20240229      113  47.0%     57.9%     60.9%     65.1%
local:llama3_8b                       113  37.1%     32.6%     38.0%     38.8%
local:mixtral_8x7b                    113  11.4%     39.0%     41.0%     43.0%
local:llama3_70b                      113  41.9%     50.5%     51.7%     53.1%
local:mixtral_8x22b                   113  43.4%     53.4%     57.8%     58.3%
openai:gpt-4o-2024-05-13              113  48.8%     51.6%     54.7%     56.6%

## task1_fuzzy_nodes_prec
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  58.1%     71.0%     78.4%     81.2%
openai:gpt-4-turbo-2024-04-09         113  81.9%     87.6%     88.9%     88.9%
anthropic:claude-3-opus-20240229      113  74.1%     84.9%     88.2%     92.1%
local:llama3_8b                       113  75.9%     65.0%     75.0%     77.6%
local:mixtral_8x7b                    113  26.7%     74.1%     77.7%     79.1%
local:llama3_70b                      113  73.9%     82.1%     84.4%     84.6%
local:mixtral_8x22b                   113  75.8%     84.9%     88.3%     87.6%
openai:gpt-4o-2024-05-13              113  77.1%     79.6%     82.0%     83.7%

## task1_fuzzy_edges_prec
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  34.7%     48.2%     55.6%     58.5%
openai:gpt-4-turbo-2024-04-09         113  65.4%     72.0%     74.1%     74.0%
anthropic:claude-3-opus-20240229      113  59.6%     73.0%     77.0%     81.5%
local:llama3_8b                       113  50.8%     44.8%     51.1%     54.2%
local:mixtral_8x7b                    113  15.3%     49.7%     53.7%     56.8%
local:llama3_70b                      113  55.6%     64.7%     67.8%     69.1%
local:mixtral_8x22b                   113  56.8%     67.6%     72.6%     72.1%
openai:gpt-4o-2024-05-13              113  62.4%     64.7%     69.1%     71.0%


# task2a

## task2a_strict_distance
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  38.0%     31.6%     29.7%     28.3%
openai:gpt-4-turbo-2024-04-09         113  26.1%     12.8%     12.2%     11.7%
anthropic:claude-3-opus-20240229      113  34.6%     11.2%     10.5%     10.0%
local:llama3_8b                       113  80.6%     65.8%     53.7%     54.0%
local:mixtral_8x7b                    113  61.4%     46.6%     47.7%     46.3%
local:llama3_70b                      113  58.7%     15.1%     14.5%     15.9%
local:mixtral_8x22b                   113  34.7%     19.7%     16.9%     18.1%
openai:gpt-4o-2024-05-13              113  21.5%     10.5%     10.0%     9.5%

## task2a_fuzzy_distance
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  33.6%     30.5%     28.5%     28.2%
openai:gpt-4-turbo-2024-04-09         113  16.2%     12.8%     11.9%     11.7%
anthropic:claude-3-opus-20240229      113  19.2%     11.1%     10.5%     10.0%
local:llama3_8b                       113  38.7%     51.3%     44.1%     46.4%
local:mixtral_8x7b                    113  35.9%     36.6%     38.2%     37.6%
local:llama3_70b                      113  23.4%     14.9%     14.4%     15.8%
local:mixtral_8x22b                   113  18.7%     17.7%     16.4%     17.6%
openai:gpt-4o-2024-05-13              113  12.7%     9.5%      9.3%      9.3%


# task2b

## task2b_strict_distance
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  64.5%     61.0%     58.8%     59.6%
openai:gpt-4-turbo-2024-04-09         113  22.8%     18.2%     15.2%     15.5%
anthropic:claude-3-opus-20240229      113  31.1%     23.6%     21.1%     21.0%
local:llama3_8b                       113  90.7%     69.6%     67.1%     66.1%
local:mixtral_8x7b                    113  83.7%     60.7%     63.2%     60.6%
local:llama3_70b                      113  59.9%     32.2%     30.3%     32.9%
local:mixtral_8x22b                   113  63.0%     40.9%     39.8%     39.0%
openai:gpt-4o-2024-05-13              113  21.8%     13.0%     11.7%     12.4%

## task2b_fuzzy_distance
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  64.5%     60.2%     58.4%     59.5%
openai:gpt-4-turbo-2024-04-09         113  21.7%     18.2%     15.2%     15.5%
anthropic:claude-3-opus-20240229      113  25.7%     23.6%     21.1%     21.0%
local:llama3_8b                       113  65.0%     63.6%     62.2%     61.7%
local:mixtral_8x7b                    113  60.8%     54.4%     57.2%     53.4%
local:llama3_70b                      113  37.2%     32.1%     30.2%     32.8%
local:mixtral_8x22b                   113  46.1%     40.8%     39.8%     38.8%
openai:gpt-4o-2024-05-13              113  19.4%     13.0%     11.7%     12.4%


# task3

## task3_strict_distance
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  31.0%     21.6%     21.2%     20.6%
openai:gpt-4-turbo-2024-04-09         113  18.6%     13.1%     12.4%     11.8%
anthropic:claude-3-opus-20240229      113  49.3%     23.4%     20.3%     17.4%
local:llama3_8b                       113  75.3%     52.1%     58.0%     73.8%
local:mixtral_8x7b                    113  64.7%     60.1%     51.5%     50.0%
local:llama3_70b                      113  56.3%     15.4%     16.2%     14.1%
local:mixtral_8x22b                   113  36.8%     18.1%     16.8%     14.4%
openai:gpt-4o-2024-05-13              113  45.9%     15.9%     13.2%     13.0%

## task3_fuzzy_distance
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  30.4%     21.6%     21.2%     20.6%
openai:gpt-4-turbo-2024-04-09         113  18.6%     13.1%     12.4%     11.8%
anthropic:claude-3-opus-20240229      113  37.7%     23.0%     20.2%     17.4%
local:llama3_8b                       113  53.4%     43.3%     51.9%     69.7%
local:mixtral_8x7b                    113  37.4%     34.1%     21.5%     18.2%
local:llama3_70b                      113  38.3%     15.3%     16.2%     14.1%
local:mixtral_8x22b                   113  33.2%     17.2%     15.9%     13.5%
openai:gpt-4o-2024-05-13              113  26.2%     15.9%     13.2%     13.0%


# task4

## task4_strict_distance
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  67.3%     62.2%     52.2%     53.5%
openai:gpt-4-turbo-2024-04-09         113  42.0%     17.9%     20.0%     20.7%
anthropic:claude-3-opus-20240229      113  49.0%     30.2%     25.7%     21.6%
local:llama3_8b                       113  91.8%     74.4%     83.4%     89.4%
local:mixtral_8x7b                    113  74.8%     75.9%     75.5%     74.8%
local:llama3_70b                      113  73.1%     31.4%     30.6%     31.0%
local:mixtral_8x22b                   113  55.9%     35.0%     33.0%     29.5%
openai:gpt-4o-2024-05-13              113  59.8%     15.9%     14.8%     14.7%

## task4_fuzzy_distance
model                               items  0-shot    1-shot    2-shot    3-shot
--------------------------------  -------  --------  --------  --------  --------
openai:gpt-3-5-turbo                  113  66.6%     60.3%     51.9%     53.1%
openai:gpt-4-turbo-2024-04-09         113  30.2%     17.9%     20.0%     20.7%
anthropic:claude-3-opus-20240229      113  38.7%     30.2%     25.7%     21.6%
local:llama3_8b                       113  70.6%     67.8%     79.7%     87.2%
local:mixtral_8x7b                    113  64.5%     62.8%     60.9%     59.5%
local:llama3_70b                      113  44.8%     31.4%     30.4%     31.0%
local:mixtral_8x22b                   113  46.3%     34.8%     32.6%     28.9%
openai:gpt-4o-2024-05-13              113  24.4%     15.9%     14.8%     14.7%
```
