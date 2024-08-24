#Eg 1
print('Hello World')
print()

#Eg 2
a = 'my name is jian yuan'
print(a)
print(len(a))

#Eg 3
import os
os.system('cls')

name = str(input("Tell me your name : "))
print (name)

a = 'string'
a = 'tail' #Overwrite above line

print(a)
print(len(a))
print(a[0])
print(a[-1])

name = input("Provide your name")
print(name)

number = input("Give me one number")
number = int(number)
print(number*2)

number2 = int(input("Give me one number"))
print(number2*2)

#LOOP
word = "more"
i = 0
for i in word:
    print(i)