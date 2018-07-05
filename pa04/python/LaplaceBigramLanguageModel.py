import math
from collections import defaultdict

class LaplaceBigramLanguageModel:
  # Bigram model w/ addone smoothing

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here

    # Keep track of occurences
    self.bigramCounts = defaultdict(lambda:0)

    # Keep track of number of unigramCounts
    self.unigramCounts = defaultdict(lambda:0)
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any bigramCounts or other corpus statistics in this function.
    """  
    # TODO your code here
    for sentence in corpus.corpus:
      token1 = '<s>'
      self.unigramCounts[token1] += 1
      
      for datum in sentence.data:
        token2 = datum.word
        # Number of "token1 token2" == C(w(n-1).w(n))
        # number of times that token2 follows token1 in corpus
        self.bigramCounts[(token1, token2)] += 1
        self.unigramCounts[token2] += 1
        self.total += 1
        # Set value for next iteration
        token1 = datum.word
      # Last word of a transformed sentence
      token2 = '</s>'
      self.bigramCounts[(token1, token2)] += 1
      self.unigramCounts[token2] += 1


  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0

    token1 = '<s>'

    # For normal unigramCounts
    for word in sentence:
      token2 = word
      count = self.bigramCounts[(token1, token2)]
      score += math.log(float(count+1)/(self.unigramCounts[token1] + self.total))
      token1 = word

    # For end sentence symnbol
    token2 = '</s>'
    count = self.bigramCounts[(token1, token2)]
    score += math.log(float(count+1)/(self.unigramCounts[token1] + self.total))

    return score
