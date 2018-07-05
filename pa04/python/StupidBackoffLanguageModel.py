import collections, math

class StupidBackoffLanguageModel:
  # Use an unsmoothed bigram model
  # If no such bigram exists in corpus, backoff to unigram with addone smoothed unigram model
  # Multiply by alpha(0.4) when backoff happens.


  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.unigramCounts = collections.defaultdict(lambda:0)
    self.bigramCounts = collections.defaultdict(lambda:0)
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    for sentence in corpus.corpus:
      # Compute counts for unigram and bigram models

      token1 = '<s>'
      self.unigramCounts[token1] += 1
      self.total += 1

      for datum in sentence.data:
        token2 = datum.word
        self.total += 1
        self.bigramCounts[(token1, token2)] += 1
        self.unigramCounts[token2] += 1
        token1 = datum.word

      token2 = '</s>'
      self.total += 1
      self.unigramCounts[token2] += 1
      self.bigramCounts[(token1, token2)] += 1


  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0

    token1 = '<s>'
    for word in sentence:
      token2 = word
      # Get bigram count
      count = self.bigramCounts[(token1, token2)]

      if count > 0:
        # If there exists a bigram for current word (token2)
        # We calculate using bigram model
        score += math.log(float(count)/(self.unigramCounts[token1]))
      else:
        # No bigram for token2
        # We backoff to Unigram with addone smoohting
        # Multiply Unigram score with backoff factor(0.4)
        score += math.log(float(0.4 * (self.unigramCounts[token2] + 1)) / (self.total + len(self.unigramCounts)))

      token1 = word
    
    token2 = '</s>'
    count = self.bigramCounts[(token1, token2)]
    if count > 0:
      # If there exists a bigram for current word (token2)
      # We calculate using bigram model
      score += math.log(float(count)/(self.unigramCounts[token1]))
    else:
      # No bigram for token2
      # We backoff to Unigram with addone smoohting
      # Multiply Unigram score with backoff factor(0.4)
      score += math.log(float(0.4 * (self.unigramCounts[token2] + 1)) / (self.total + len(self.unigramCounts)))

    return score
