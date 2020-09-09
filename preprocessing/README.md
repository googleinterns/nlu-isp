# Data Preprocessing

## Data Sources
We use the following four different public datasets for semantic parsing:
* [`Microsoft ATIS`](https://www.kaggle.com/siddhadev/atis-dataset-clean-re-split-kernel#The-ATIS-Dataset)
* [`Facebook TOP`](http://fb.me/semanticparsingdialog)
* [`SNIPS`](https://github.com/snipsco/nlu-benchmark.git)
* [`Facebook Multilingual (EN)`](https://fb.me/multilingual_task_oriented_data)

Run the `processing.py` script to process raw data files and create consistent format for all four data sources, consisted of incrementalized queries. Specifically, the output format is:

```
    type-sent_id-sub_id
    token1 tag1
    token2 tag2
    token3 tag3
    ...
    intents
```

where type is either `train`, `dev`, or `test`. An example for the identifier at the beginning of an data instance is `train-00001-1`. For each `sent_id` with `n` tokens in the full query, there will be `n` data entries in the processed data files, starting from `type-sent_id-1` to `type-sent_id-full`, with `full` indicating this instance corresponds to a full query.

Processed data files are saved to `data` folder; each data source contains a `train.txt`, `dev.txt`, and `test.txt`.
