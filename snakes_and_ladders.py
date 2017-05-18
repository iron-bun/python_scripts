#!/usr/bin/env python3
import random

ans = 0
for i in range(1000):
    j = 1
    while j < 99:
        tmp = random.randint(1, 6)
        j += tmp
        ans += 1

print(ans / 1000)

import numpy as p

states = [[0 for _ in range(99)] for _ in range(99)]
for i in range(99):
    for j in range(1, 7):
        if i + j < 99:
            states[i][i+j] += 1/6

states = p.linalg.inv(p.identity(99) - states)
print(sum(states[0]))


