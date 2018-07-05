import math
from collections import defaultdict

class CustomLanguageModel:
  # Trigram Model

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.total = 0
    self.trigramCounts = defaultdict(lambda:0)

    # We need to also calculate the count of bigram of first two words in trigram
    self.bigramCounts = defaultdict(lambda:0)
    self.unigramCounts = defaultdict(lambda:0)

    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    for sentence in corpus.corpus:
      # @NaW: not a word
      token1 = '@NaW'
      token2 = '<s>'

      self.unigramCounts[token2] += 1
      self.total += 1
      
      for datum in sentence.data:
        token3 = datum.word
        self.total += 1
        # Calculate bigram history to support trigram model
        self.unigramCounts[token3] += 1
        self.bigramCounts[(token2, token3)] += 1

        if token1 != '@NaW':
          self.trigramCounts[(token1, token2, token3)] += 1

        token1 = token2
        token2 = token3

      token3 = '</s>'
      self.total += 1

      self.unigramCounts[token3] += 1
      self.bigramCounts[(token2, token3)] += 1

      self.trigramCounts[(token1, token2, token3)] += 1  



  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0

    token1 = '@NaW'
    token2 = '<s>'

    #count1 = self.unigramCounts[token2]
    for word in sentence:
      token3 = word
      count2 = self.bigramCounts[(token2, token3)]
      count3 = self.trigramCounts[(token1, token2, token3)]

      # Stupid backoff seems to perform worse (0.191083 to 0.197452)
      # -> Remove alpha constant
      if count3 > 0:
        # Trigram
        score += math.log(float(count3)/(self.bigramCounts[(token1, token2)]))
      elif count2 > 0:
        # Bigram
        score += math.log(float(count2)/(self.unigramCounts[token2]))
      else:
        # Addone Smoothing Unigram
        score += math.log(float(self.unigramCounts[token3]+1)/ (len(self.unigramCounts) + self.total))

      token1 = token2
      token2 = token3

    token3 = '</s>'
    count2 = self.bigramCounts[(token2, token3)]
    count3 = self.trigramCounts[(token1, token2, token3)]

    if count3 > 0:
      # Trigram
      score += math.log(float(count3)/(self.bigramCounts[(token1, token2)]))
    elif count2 > 0:
      # Bigram
      score += math.log(float(count2)/(self.unigramCounts[token2]))
    else:
      # Addone Smoothing Laplace Unigram
      score += math.log(float(self.unigramCounts[token3]+1)/ (len(self.unigramCounts) + self.total))


    return score
