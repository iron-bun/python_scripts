#!/usr/bin/env python3

class solver:
  def __init__(self, width):
    self.width = width
    self.ans = []
    self.query_rows = []
    
  def append_query_row(self, query):
    self.query_rows.append(query)
    self.ans.append(self.query_probabilities(query))
  
  def query_probabilities(self, query):
    ans = [0]*self.width
    count = 0
    for i in solver.permute_query(query, self.width):
      tmp = []
      count += 1
      print(i)
      for j,k in zip(ans, i):
        tmp.append(j+k)
      ans = tmp
    return map(lambda x: x/count, ans)

  def permute_query(query, length):
    if len(query) == 1:
      value = query[0]
      for i in range(length - value + 1):
        yield [0]*i + [1]*value + [0]*(length-value-i)
    else:
        value = query.pop(0)
        for i in range(length):
            tmp = [0]*i + [1]*value + [0]
            for j in solver.permute_query(query, length - i - value - 1):
                yield tmp + j
        
  def print(self):
    for i in self.ans:
      print(list(i))

if __name__ == '__main__':
  #solve https://www.nonograms.org/nonograms/i/46955
  s = solver(10)
  s.append_query_row([4])
  s.append_query_row([7])
  s.append_query_row([2,5])
  s.append_query_row([3,2])
  s.append_query_row([1,3,1])
  s.append_query_row([1,5])
  s.append_query_row([1,2,3,1])
  s.append_query_row([2,1])
  s.append_query_row([2,1,2])
  s.append_query_row([7])
  s.append_query_row([2,2])
  s.append_query_row([5])
  s.append_query_row([3])
  s.print()
                
