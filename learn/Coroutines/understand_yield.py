# https://lotabout.me/2017/Python-Generator/
from formatter import *

printx('yield example start')
def fibonacci():
    a, b = (0, 1)
    while True:
        yield a
        a, b = b, a+b

fibos = fibonacci()
print(next(fibos)) #=> 0
print(next(fibos)) #=> 1
print(next(fibos)) #=> 1
print(next(fibos)) #=> 2
printx('yield example ends')

printx('non-yield example start')
class Fibonacci():
    def __init__(self):
        self.a, self.b = (0, 1)
    def __iter__(self):
        return self
    def __next__(self):
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        return result

fibos = Fibonacci()
print(next(fibos)) #=> 0
print(next(fibos)) #=> 1
print(next(fibos)) #=> 1
print(next(fibos)) #=> 2
printx('non-yield example ends')

printx('understand yield start')
def generator():
    print('before')
    yield            # break 1
    print('middle')
    yield            # break 2
    print('after')
    yield

x = generator()
next(x)
#=> before
next(x)
#=> middle
next(x)
#=> after
#=> exception StopIteration
printx('understand yield ends')

printx('yield from (1) start')
def odds(n):
    for i in range(n):
        if i % 2 == 1:
            yield i

def evens(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

def odd_even(n):
    for x in odds(n):
        yield x
    for x in evens(n):
        yield x

for x in odd_even(6):
    print(x)
#=> 1, 3, 5, 0, 2, 4
printx('yield from (1) ends')

printx('yield from (2) start')
def odds(n):
    for i in range(n)
        if i % 2 == 1:
            yield i

def evens(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

def odd_even(n):
    yield from odds(n)
    yield from evens(n)


for x in odd_even(6):
    print(x)
printx('yield from (2) ends')



printx('(NOTE: for coroutine)advanced yield skill start')
def averager():
    sum = 0
    num = 0
    while True:
        sum += (yield sum / num if num > 0 else 0)
        num += 1

x = averager()
x.send(None)
#=> 0
x.send(1)
#=> 1.0
x.send(2)
#=> 1.5
x.send(3)
#=> 2.0
printx('(NOTE: for coroutine)yield skill ends')