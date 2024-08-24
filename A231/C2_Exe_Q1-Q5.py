#Question 1
quantity = float(input("Please enter the petrol quantity you bought (in litre): "))
amount = float(quantity)*1.53
print("The amount to be paid is: RM", "%.2f" % amount)
print()

#Question 2
usd = float(input("Please enter the USD amount: "))
myr = float(usd)*3.80
print("The USD amount in RM is: RM", "%.2f" % myr)
print()

#Question 3
first = float(input("Please enter the first student mark: "))
second = float(input("Please enter the second student mark: "))
third = float(input("Please enter the third student mark: "))
average = float(first + second + third)/3
print("The average mark of the three student is: ", "%.2f" % average)
print()

#Question 4
number = float(input("Please enter a number: "))
if number == 0:
    print("The number you entered is a null value.")
elif number > 0:
    print("The number you entered is a positive value.")
elif number < 0:
    print("The number you entered is a negative value.")
print()

#Question 5
num1 = float(input("Please enter the first number: "))
num2 = float(input("Please enter the second number: "))
num3 = float(input("Please enter the third number: "))

if (num1 < num2):
    least = float(num1);
else:
    least = float(num2);
    if (num1 < num3):
        least = float(num3);
elif ((num2 < num1) & (num2 <num3)):
    least = float(num2);
else:
    least = float(num3);

print("The least number is:", "%.2f" % least)