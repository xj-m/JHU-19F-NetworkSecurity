# test string range select
print("test string ragne select".center(100,'-'))
test_string_list = []
for i in range(1,11):
    # a = ''+ i
    # TODO: why this not working
    test_string_list.append(str(i))

print("length of 10 element string:"+str(len(test_string_list)))
print(test_string_list)
print(test_string_list[1:2])
print(test_string_list[:9])
print(test_string_list[1:])
print(test_string_list[0:])
# [a:b], it contains b, but not a

# test  inside for
print('test inside for'.center(100,'-'))
for str in test_string_list:
    print(str)
print([str for str in test_string_list[:5]])

# test for get words in string
test_string = '1 2 3 4 5 '
print(test_string.split(' ')[0])

# NOTE: get type, use type()