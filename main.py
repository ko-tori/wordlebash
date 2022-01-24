from words import *

def check(word, solution, d=None):
  if d is None:
    d = {}
    for i in solution:
      if i not in d:
        d[i] = 0
      d[i] += 1

  result = []
  for i, j in zip(word, solution):
    if i == j:
      result.append(2)
    elif i in d:
      result.append(1)
      d[i] -= 1
      if d[i] <= 0:
        del d[i]
    else:
      result.append(0)

  return result

def match(word, tested, result, d=None):
  if d is None:
    d = {}
    for i in word:
      if i not in d:
        d[i] = 0
      d[i] += 1

  for i, (n, c) in enumerate(zip(result, tested)):
    if n == 2 and word[i] != c:
      return False
    elif n == 1:
      if word[i] == c:
        return False
      if c in d:
        d[c] -= 1
      else:
        return False
      if d[c] <= 0:
        del d[c]
    elif n == 0:
      if word[i] == c or c in d:
        return False

  return True

def perf(word, solution, lex=SOLUTIONS):
  return len(skim(word, solution, lex)) / len(lex)

def skim(word, solution, valid):
  return set(filter(lambda w: match(w, word, check(word, solution)), valid))

def bash(solution, lex=ALL, depth=1, n=10, cutoff=float('inf')):
  results = []
  for word in lex:
    result = check(word, solution)
    result = set(filter(lambda w: match(w, word, result), lex))
    word2 = []
    if depth > 1:
      b = bash(solution, result, depth - 1, n, cutoff)
      if len(b):
        word2, result = b[0]
    if len(result) < cutoff:
      results.append(([word]+word2, result))
      if depth == 2:
        print(results[-1])

  results.sort(key=lambda x: -len(x[1]))
  return results[-n:]

def pprint(result):
  for i, j in result:
    print(i, j)

#result = bash('proxy', SOLUTIONS_SORTED, 2, 10)
#pprint(result)

def score(guess, lex=SOLUTIONS_SORTED):
  return 1 - sum(perf(guess, solution) for solution in lex) / len(lex)

def score_all(i, hi, lo):
  print('starting from', ALL_SORTED[i], 'current high:', hi, 'current low:', lo)
  with open('out.txt', 'a') as f:
    for guess in ALL_SORTED[i:]:
      s = score(guess)
      if s > hi[1]:
        hi[0] = guess
        hi[1] = s
        print('new high:', hi)
      if s < lo[1]:
        lo[0] = guess
        lo[1] = s
        print('new low:', lo)
      f.write(guess + ' ' + str(s) + '\n')
      print(guess, s)

def resume_scoring(fn='out.txt'):
  (hi, hic), (lo, loc) = hilo(parse_file(fn))
  i = ALL_SORTED.index(p[-1].split()[0]) + 1
  score_all(i, hi=[hi, hic], lo=[lo, loc])

def hilo(p, n=1):
  p.sort(key=lambda x: x[1])
  if n == 1:
    return [p[-1], p[0]]
  else:
    return [p[-n:], p[:n]]

def parse_file(fn='out.txt'):
  p = []
  with open('out.txt', 'r') as f:
    for line in f.readlines():
      w, n = line.strip().split()
      n = float(n)
      p.append([w, n])
  return p