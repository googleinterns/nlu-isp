import os
import sys
import pathlib
from collections import defaultdict, OrderedDict, Counter

project_root = pathlib.Path(__file__).parents[0]
from src.logging_util import ColoredLog

import torch
import numpy as np
from sklearn.metrics import f1_score
from scipy.interpolate import interp1d
from matplotlib import rcParams
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
rcParams["figure.figsize"] = [9.0, 6.0]


class Evaluator(object):

    """Incremental Test Outcome Object."""

    def __init__(self, pred_out, name, exclude_other=False):
        """Initialization.

        :pred_out: prediction outcome from the model
        :name: experiment name
        :exclude_other: whether to exclude `O` tags when calculating slot f1 scores
        """

        self.logger = ColoredLog(__name__)
        self.name = name
        self.exclude_other = exclude_other
        self.test_set = {}
        self.error = defaultdict(list)
        self.count = defaultdict(int)
        self.length_map = defaultdict(list)
        for i in range(len(pred_out["sorted_ids"])):
            sent_id = pred_out["sorted_ids"][i][:10]
            sub_id = pred_out["sorted_ids"][i][11:]
            if sent_id not in self.test_set:
                self.test_set[sent_id] = defaultdict(dict)
            if sub_id != "full":
                sub_id = int(sub_id)
                self.test_set[sent_id][sub_id]["gold_int"] = pred_out["golden"][i]
                self.test_set[sent_id][sub_id]["pred_int"] = pred_out["pred"][i]
                if pred_out["golden"][i] != pred_out["pred"][i]:
                    self.error["intent"].append((sent_id, sub_id))
                self.test_set[sent_id][sub_id]["gold_slot"] = pred_out["golden_slot"][i]
                self.test_set[sent_id][sub_id]["pred_slot"] = pred_out["pred_slot"][i]
                if not (np.array(pred_out["golden_slot"][i]) == np.array(pred_out["pred_slot"][i])).all():
                    self.error["slot"].append((sent_id, sub_id))
                self.test_set[sent_id][sub_id]["text"] = pred_out["text"][i]
            else:
                length = len(pred_out["golden_slot"][i]) - 2
                self.count[length] += 1
                self.length_map[length].append(sent_id)

        self.intent_set = self.generate_intent_map(pred_out["golden"])
        self.slot_set = self.generate_slot_map(pred_out["golden_slot"])
        self.ave_score = {}

    def convert_intent(self, intent, label_set):
        """ Convert intent to 0-1 vector.
        :intent: intent in string format
        :label_set: an ordered set of intents
        """
        vec = np.zeros(len(label_set), dtype=int)
        for i in intent.split("#"):
            vec[label_set[i]] = 1
        return list(vec)

    def convert_slot(self, slot, label_set):
        """ Convert slot to 0-1 vector.
        :slot: slot in string format
        :label_set: an ordered set of slots
        """
        vec = np.zeros(len(label_set), dtype=int)
        vec[label_set[slot]] = 1
        return list(vec)

    def generate_intent_map(self, intent_list):
        """ Generate an ordered map for all intents. """
        intent_set = set()
        for i in intent_list:
            intent_set.update(set(i.split("#")))

        intent_set = {i:j for j, i in enumerate(intent_set)}
        return intent_set

    def generate_slot_map(self, slot_list):
        """ Generate an ordered map for all slots. """
        slot_set = set()
        for s in slot_list:
            slot_set.update(set(s))

        if self.exclude_other:
            slot_set.remove("O")
        slot_set = {s:i for i, s in enumerate(slot_set)}
        return slot_set

    def generate_summary(self):
        """ Organize pred_out by query length. """
        # summary_intent is a dictionary with query-length as keys
        # for each query length, it contains prediction result at each incremental step
        # each element in the list corresponds to a (golden, pred) pair 
        self.summary_intent = defaultdict(lambda: defaultdict(lambda: [[], []]))
        self.summary_slot = defaultdict(lambda: defaultdict(lambda: [[], []]))
        self.seq = defaultdict(lambda: defaultdict(list)) 

        t_b = 0
        t_a = 0
        for sent_id, rec in self.test_set.items():
            query_len = max(rec.keys())

            for num_token in rec:
                y_true = self.convert_intent(rec[num_token]["gold_int"], self.intent_set)
                y_pred = self.convert_intent(rec[num_token]["pred_int"], self.intent_set)
                self.summary_intent[query_len][num_token][0].append(y_true)
                self.summary_intent[query_len][num_token][1].append(y_pred)

                slots = np.array(rec[num_token]["gold_slot"][1:])
                filter_o = np.where(slots != "O")[0]
                filtered_slots = slots[filter_o]
                t_b += len(slots)
                t_a += len(filtered_slots)
                s_true = [self.convert_slot(s, self.slot_set) for s in filtered_slots]
                s_pred = [self.convert_slot(s, self.slot_set) for s in filtered_slots]
                self.summary_slot[query_len][num_token][0].extend(s_true)
                self.summary_slot[query_len][num_token][1].extend(s_pred)

                self.seq[query_len][num_token].extend([sent_id] * len(filtered_slots))

        self.summary = {"intent": self.summary_intent, "slot": self.summary_slot}
        print(t_b, t_a)

    def calculate_slot_f1(self, granularity=0.05):
        self.slot_f1_scores = OrderedDict()
        self.slot_f1_dict = defaultdict(lambda: defaultdict(dict))
        for k in self.count.keys():
            x = [0]
            y = [0]
            for i in range(1, len(self.summary["slot"][k]) + 1):
                y_true = np.array(self.summary["slot"][k][i][0])
                y_pred = np.array(self.summary["slot"][k][i][1])
                score = f1_score(y_true, y_pred, average="weighted")
                self.slot_f1_dict[k][i]["f1"] = score
                self.slot_f1_dict[k][i]["size"] = len(y_true)
                x.append(float(i)/k)
                y.append(score)

            f = interp1d(x,y)
            interp_score = f(np.arange(0, (1 + granularity), granularity))
            self.slot_f1_scores[k] = interp_score

        self.ave_score["slot"] = np.average(list(self.slot_f1_scores.values()), axis=0, weights=list(self.count.values()))
        return self.ave_score["slot"]

    def calculate_intent_f1(self, granularity=0.05):
        self.granularity = granularity
        self.intent_f1_scores = OrderedDict()
        for k in self.count.keys():
            x = [0]
            y = [0]
            for i in range(1, len(self.summary["intent"][k]) + 1):
                y_true = np.array(self.summary["intent"][k][i][0])
                y_pred = np.array(self.summary["intent"][k][i][1])
                score = f1_score(y_true, y_pred, average="weighted")
                x.append(float(i)/k)
                y.append(score)

            f = interp1d(x,y)
            interp_score = f(np.arange(0, (1 + granularity), granularity))
            self.intent_f1_scores[k] = interp_score

        self.ave_score["intent"] = np.average(list(self.intent_f1_scores.values()), axis=0, weights=list(self.count.values()))
        return self.ave_score["intent"]

    def plot(self, task, color="b"):
        """ Plot average f1 score and dashed lines for each query length.

        :task: intent or slot
        :color: what color to use for the average score
        """

        if task == "intent":
            src = self.intent_f1_scores
        else:
            src = self.slot_f1_scores

        sorted_keys = sorted(self.summary[task].keys())

        fig, ax = plt.subplots()
        for j in range(len(src)):
            ql = sorted_keys[j]
            if ql in src:
                ax.plot(np.arange(0, (1 + self.granularity), self.granularity), src[ql], "--", lw=1, label=f"{ql} ({self.count[ql]})")
        ax.plot(np.arange(0, (1 + self.granularity), self.granularity), self.ave_score[task], c=color, lw=2, label="Average", alpha=0.85)
        ax.set_title(f"Experiment: {self.name} [{task}]")
        ax.set_xlabel("Received Query Fraction")
        ax.set_ylabel("F1 Score")
        ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))
        ax.legend(loc="right", bbox_to_anchor=(1.4, 0.5), ncol=2, title="Query Length (Count)")
        plt.show()

    def pprint(self, sent_id):
        out = []
        query = self.test_set[sent_id]
        max_len = max(query.keys())

        for i in range(1, max_len + 1):
            out.append([sent_id, "-", query[i]["gold_int"], query[i]["pred_int"], "-", "-"])
            for k in range(1, i+1):
                out.append([k, query[i]["text"][k], "-", "-", query[i]["gold_slot"][k], query[i]["pred_slot"][k]])
            out.append(["==="] * 6)
        self.logger.critical(out, header=["len", "text", "gold_int", "pred_int", "gold_slot", "pred_slot"])

