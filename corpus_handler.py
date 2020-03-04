# Copyright 2019 Sebastian Kahl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Provide Corpus data from Drawing Corpus.
Created on 16.05.2018

@author: skahl
"""

# Imports from __future__ in case we're running Python 2
from __future__ import division, print_function
from __future__ import absolute_import, unicode_literals


import os
import sys
from copy import copy
from collections import deque
from random import random, choice, shuffle
import simplejson as json


class Drawing(object):

    def __init__(self, drawing, number, user=0):
        if len(drawing) > 0:
            self.drawing = deque(drawing)
            self.number = number
            self.user = user
        else:
            print("\nNo trajectory in drawing!\n")
            self.drawing = None


    def __repr__(self):
        return str(self.drawing)


    def __len__(self):
        if self.drawing is not None:
            return len(self.drawing)
        else:
            return None


    def get_next_coordinate(self):
        if self.drawing is None:
            return None
        else:
            try:
                return self.drawing.popleft()
            except IndexError as error:
                return "done"




class DrawingCorpus(object):

    def __init__(self, corpus_filename, only_user=None, only_number=None, randomize=False):
        self.corpus_filename = corpus_filename
        self.corpus_data = None
        self.prepared_corpus = {}
        self.randomized = randomize

        self.current_userid = None
        self.current_numberid = None
        self.current_trajectoryid = None
        self.empty_numbers = []

        # try to open it
        try:
            corpus = None
            with open(self.corpus_filename, 'r') as corpus_file:
                corpus_json = corpus_file.read()
                corpus = json.loads(corpus_json)
                self.corpus_data = corpus
            corpus_file.close()

            if self.corpus_data is not None:
                print("Successfully read corpus", self.corpus_filename, "from file!")

            # prepare corpus for output
            self.prepare(only_user=only_user, only_number=only_number)

        except Exception as error:
            print(error)
            sys.exit(1)


    def prepare(self, only_user=None, only_number=None):
        # prepare corpus
        corpus_keys = self.corpus_data.keys() if only_number is None else only_number

        try:
            for numberid in corpus_keys:
                user_keys = self.corpus_data[numberid].keys() if only_user is None else only_user
                for userid in user_keys:
                    user_trajectories = self.corpus_data[numberid][userid]

                    trajectories = deque(user_trajectories.keys())
                    
                    # shuffle if needed
                    if self.randomized:
                        shuffle(trajectories)

                    # prepare corpus
                    num_all = len(trajectories)
                    for num in range(num_all):
                        # popleft keys from deque and add trajectory until test set size is reached
                        traj_id = trajectories.popleft()
                        # test set won't have any more trajectory or user ids
                        if numberid not in self.prepared_corpus:
                            self.prepared_corpus[numberid] = deque()
                        self.prepared_corpus[numberid].append({'user': userid, 'trajectory': user_trajectories[traj_id]})

        except Exception as er:
            print("An error occured preparing the corpus: \n", er)


    def get_corpus(self):
        """ Return a copy of the prepared corpus.
        """
        return copy(self.prepared_corpus)


    def pop_next_corpus_drawing(self):
        """ From given corpus, return a random drawing will be returned.

        """
        left_numbers = []

        if self.prepared_corpus is not None and self.prepared_corpus is not {}:
            left_numbers = list(set(self.prepared_corpus.keys()) - set(self.empty_numbers))

            if left_numbers == []:
                print("corpus out of trajectories")
                return None

            # return drawing from random number index corpus
            self.current_numberid = choice(left_numbers)

            trajectories = self.prepared_corpus[self.current_numberid]
            # shuffle(trajectories)

            trajectory = trajectories.popleft()
            userid = trajectory['user']
            print("\nReturning Drawing of number:", self.current_numberid, "(", len(trajectory['trajectory']), " coordinates), with drawings left:", len(trajectories))

            if len(trajectories) < 1:
                self.empty_numbers.append(self.current_numberid)

            accessible_drawing = Drawing(trajectory['trajectory'], number=self.current_numberid, user=userid)
            return accessible_drawing
        print("Corpus is None!")
        return None
