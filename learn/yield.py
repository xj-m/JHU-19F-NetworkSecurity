def f123():
    yield 1
    yield 2
    yield 3

for item in f123():
    print (item)