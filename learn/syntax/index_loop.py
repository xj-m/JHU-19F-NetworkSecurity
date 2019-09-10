# from link https://treyhunner.com/2016/04/how-to-loop-with-indexes-in-python/
print("part 1: can print index".center(100,'-'))
presidents = ["Washington", "Adams", "Jefferson", "Madison", "Monroe", "Adams", "Jackson"]
for i in range(len(presidents)):
    print("President {}: {}".format(i + 1, presidents[i]))

print("part 2".center(100,'-'))
presidents = ["Washington", "Adams", "Jefferson", "Madison", "Monroe", "Adams", "Jackson"]
for num, name in enumerate(presidents[:len(presidents)], start=2):
    print("President {}: {}".format(num, name))

