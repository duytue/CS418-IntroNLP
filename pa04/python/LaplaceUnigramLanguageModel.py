import math
from collections import defaultdict

class LaplaceUnigramLanguageModel:
  # a unigram model with add-one smoothing. 
  # Treat out-of-vocabulary items as a word which was seen zero times in training.

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    # Collection = Dictionary
    # Key value storage

    # Default value for element not in Collection is 0
    # == Treat new word as seen 0 time
    self.unigramCounts = defaultdict(lambda:0)

    # Total number of training words
    self.total = 0

    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any unigramCounts or other corpus statistics in this function.
    """  
    # TODO your code here
    #pass
    for sentence in corpus.corpus:
      for datum in sentence.data:
        # token acts as a key in collection
        token = datum.word
        # number of occurences is value of collection[token]
        self.unigramCounts[token] += 1

        self.total += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0
    for token in sentence:
      # count = 0 for 'outofvocabulary' word
      count = self.unigramCounts[token]

      # Return log probability of token with added 1 smoothing
      score += math.log(float(count+1)/(self.total + len(self.unigramCounts)))

    return score
