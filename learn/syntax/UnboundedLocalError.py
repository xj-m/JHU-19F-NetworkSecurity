# NOTE: first letter of a class
import sys

class testClass:
    def __init__(self,para1):
        self.para1 = para1
    def pr(self):
        print (self.para1)

def main(args):
    testClass = testClass(1)
    testClass.pr()

if __name__=="__main__":
    main(sys.argv[1:])

# Unbounded Local error test
# round 1
print("round 1")
counter = 0
def increment():
  counter += 1
increment()

# round 2
print("round 2")
counter = [0]
def increment():
  counter[0] += 1
increment()
print (counter[0])
# NOTE: make the var changable