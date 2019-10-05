from threading import Timer

def timeout():
    print("Game over")

# duration is in seconds
x = lambda : print("lambda")
t = Timer(4, x)
t.start()
print("test")

# wait for time completion
# t.join()