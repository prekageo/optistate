import qm
import qm_orig
import itertools
import sys

def t(x,n):
  x = x[1]
  if x == '1':
    return ['X'*n]
  if x == '0':
    return ['X'*n]

  result = []
  for a,b in x:
    tmp = []
    for i in xrange(n):
      if a & 1:
        tmp.append('1')
      elif b & 1:
        tmp.append('X')
      else:
        tmp.append('0')
      a >>= 1
      b >>= 1
    tmp.reverse()
    result.append(''.join(tmp))
  return result

def eq(check, correct, dc):
  def update_v(s, v, bit_pos):
    for term_pos in xrange(len(s)):
      if s[term_pos][bit_pos] == '1' and not bit:
        v[term_pos] = False
      elif s[term_pos][bit_pos] == '0' and bit:
        v[term_pos] = False
  if len(correct) == 0:
    return False
  n = len(correct[0])
  check = t(check, n)
  if len(check) != len(correct):
    return False
  for state in xrange(1<<n):
    if state in dc:
      continue
    check_v = [True] * len(check)
    correct_v = [True] * len(correct)
    for bit_pos in xrange(n):
      bit = state & 1<<bit_pos
      update_v(check, check_v, n-bit_pos-1)
      update_v(correct, correct_v, n-bit_pos-1)
    #print state,check_v,correct_v
    check_v = any(check_v)
    correct_v = any(correct_v)
    if check_v != correct_v:
      return False
  return True

def main():
  n = 3
  qm1 = qm.QM([chr(code) for code in xrange(ord('A'),ord('A')+n)])

  for minterms in itertools.chain(*(itertools.combinations(range(1<<n),i) for i in xrange(1,1<<n+1))):
    minterms = set(minterms)
    if max(minterms) == 0:
      continue
    for dc in itertools.chain(*(itertools.combinations(minterms,i) for i in xrange(0,len(minterms)+1))):
      dc = list(dc)
      ones = list(minterms - set(dc))
      check = qm1.solve(ones,dc)
      correct = qm_orig.qm(ones=ones,dc=dc)
      if not eq(check, correct, dc):
        print 'ERROR',ones,dc,t(check, n),qm1.get_function(check[1]),correct,check
      #else:
      #  print '   OK',ones,dc,qm1.get_function(check[1]),correct

if __name__ == '__main__':
  main()
