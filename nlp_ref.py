import operator
import re

from collections import defaultdict
from sklearn.cluster import KMeans


def LoadProblemsWithoutChoices(filename):
  # Returns a list for strings represents the problem without the
  # choices.
  problems = ['']
  problem_id = 1
  with open(filename, 'r') as f:
    for line in f.readlines():
      line = line.strip()
      if not line:
        continue

      if line.startswith('$\\text') or line.startswith('$\\mathrm'):
        problem_id += 1
        problems.append('')
      else:
        problems[problem_id - 1] += line
  return problems


def ValidToken(token):
  # Returns True if token is not empty and all characters in token are
  # alphabet.
  return token and all([c.isalpha() for c in token])


def Tokenization(text):
  # Returns a list of string in lower case.
  tokens = list(set(re.split('[^a-zA-Z]', text)))
  return [t.lower() for t in tokens if t != '' and ValidToken(t)]


def BuildVocabuaryList(problems, min_freq, min_word_len):
  # Returns a dictionary mapping string to tuple of (word_idx, word_freq).
  # Word shorter than min_word_len or has less frequent of min_freq is skipped.
  voc = defaultdict(int)
  for problem in problems:
    for token in list(set(problem)):
      voc[token] += 1

  words = {}
  for word, count in sorted(voc.items(), key=operator.itemgetter(1)):
    if count < min_freq or len(word) < min_word_len:
      continue
    words[word] = (len(words), count)
  return words


def BuildFeatures(tokenized_problem, voc):
  features = []
  for problem in tokenized_problem:
    feature = [0] * len(voc)
    for token in problem:
      if token not in voc:
        continue
      feature[voc[token][0]] = 1.0
    features.append(feature)
  return features


def LoadData(filename):
  # Load problems and do tokenization.
  problems = LoadProblemsWithoutChoices(filename)
  tokenized_problem = [Tokenization(problem) for problem in problems]

  # Build vocabulary(min_word_len = 2, min_word_freq=2) and conver the problem
  # to one hot features.
  voc = BuildVocabuaryList(tokenized_problem, 2, 2)
  features = BuildFeatures(tokenized_problem, voc)
  return (problems, features, voc)


def Classification(features, num_clusters):
  kmeans = KMeans(n_clusters=num_clusters, n_init=100, n_jobs=4)
  kmeans.fit(features)
  return kmeans.predict(features)


def OutputClassifiedProblem(filename, classified_problem):
  with open('data/amc8_1999_to_2018_classified.html', 'w') as out:
    out.write('<html><head>')
    out.write('''<script type="text/x-mathjax-config">
        MathJax.Hub.Config({tex2jax: {inlineMath: [["$","$"],
                                                   ["\\(","\\)"]]}});
        </script>''')
    out.write('''<script type="text/javascript" async
        src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML">
        </script>''')
    out.write('</head><body>')
    for a in classified_problem:
      out.write('<div style="margin: 20"><div style="margin-bottom: 10">')
      out.write(str(a[0]))
      out.write('</div><div>')
      out.write(a[1])
      out.write('</div></div>')
    out.write('</body></html>')


if __name__ == '__main__':
  problems, features, voc = LoadData('data/amc8_1999_to_2018.txt')
  classified_problem = sorted(zip(Classification(features, 40), problems),
                              key=lambda x: x[0])
  OutputClassifiedProblem('data/amc8_1999_to_2018_classified.html',
                          classified_problem)
