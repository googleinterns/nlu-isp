import os
import sys
import pathlib
import argparse
import collections
from collections import OrderedDict, defaultdict
from typing import List, Tuple, Iterable, Union

from ordered_set import OrderedSet
from logging_util import ColoredLog

project_root = pathlib.Path(__file__).parents[1]

class Vocabulary(object):
    """
    A vocabulary instance, for tokens, intents, and slots.
    """

    def __init__(self, name: str, speical_tokens: List=None):
        """Initialization.

        :name: name of the vocabulary
        :speical_tokens: speical tokens to be added to vocabulary

        """

        self.name = name
        self.speical_tokens = speical_tokens
        self.counter = defaultdict(int)

        self.instance_set = OrderedSet()
        self.instance_map = OrderedDict()
        if speical_tokens:
            self.add_instance(speical_tokens)

    def add_instance(self, instance: Union[str, Iterable[str]]) -> None:
        """ Add instances to the vocabulary.

        :instance: can be either one instance or an iterable that contains multiple instances

        """

        if isinstance(instance, collections.abc.Iterable) and not isinstance(instance, str):
            for item in instance:
                self.add_instance(item)
            return

        self.counter[instance] += 1
        if instance not in self.instance_map:
            self.instance_set.append(instance)
            self.instance_map[instance] = len(self.instance_map)

    def encode(self, instance: Union[str, Iterable[str]]) -> Union[int, List[int]]:
        """ Encode instance to index.

        :instance: string or list of strings
        """

        if isinstance(instance, collections.abc.Iterable) and not isinstance(instance, str):
            return [self.encode(item) for item in instance]

        if instance in self.instance_map:
            return self.instance_map[instance]
        else:
            return self.instance_map["[UNK]"]

    def decode(self, index: Union[int, Iterable[int]]) -> Union[str, List[str]]:
        """ Decode from index to instance.

        :index: one index or list of indices
        """

        if isinstance(index, collections.abc.Iterable) and not isinstance(index, str):
            return [self.decode(elem) for elem in index]

        return self.instance_set[index]

    def save(self, dir_path: str) -> None:
        """ Save vocabulary.

        :dir_path: directory to save the object

        """

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        save_path = os.path.join(dir_path, self.name + "_vocab.txt")
        with open(save_path, 'w') as f:
            for instance, index in self.instance_map.items():
                f.write(f"{instance}\t{index}\n")

    def __len__(self) -> int:
        return len(self.instance_set)

    def __str__(self) -> str:
        return f"Vocabulary size: {len(self)}\nSpecial tokens: {self.speical_tokens}"
