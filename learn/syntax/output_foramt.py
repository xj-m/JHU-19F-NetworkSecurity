# Format with %  
"""
# print integer and float value 
print("Geeks : % 2d, Portal : % 5.2f" %(1, 05.333))
  
# NOTE:  %[flags][width][.precision]type 
# print integer value 
print("Total students : % 1d, Boys : % 2d" %(240, 120)) 
  
# print octal value 
print("% 7.3o"% (25)) 

# print exponential value 
print("% 10.3E"% (356.08977)) 
"""
def printt(string):
    print(string+'test')
printt("test")

# Align
print_string = "I love geeksforgeeks"
print(print_string)
print (print_string.ljust(40, '-'))
print(print_string.center(40))
print(print_string.rjust(40))

# column output
data = [['a', 'b', 'c'], ['aaaaaaaaaa', 'b', 'c'], ['a', 'bbbbbbbbbb', 'c']]
col_width = max(len(word) for row in data for word in row) + 2  # padding
for row in data:
    print ("".join(word.ljust(col_width) for word in row))

