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
# Align

cstr = "I love geeksforgeeks"
	
# Printing the center aligned 
# string with fillchr 
print ("Center aligned string with fillchr: ") 
print (cstr.center(40, '#')) 

# Printing the left aligned 
# string with "-" padding 
print ("The left aligned string is : ") 
print (lstr.ljust(40, '-')) 

# Printing the right aligned string 
# with "-" padding 
print ("The right aligned string is : ") 
print (rstr.rjust(40, '-')) 

