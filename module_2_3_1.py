# 2-й вариант - без break, чисто на логике
mylist = [42, 69, 322, 13, 0, 99, -5, 9, 8, 7, -6, 5]
i = 0
while i < len(mylist) and mylist[i] >= 0:
    print(mylist[i])
    i = i + 1
print(type(mylist))
