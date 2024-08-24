import os
os.system('cls')

#Input
totalAmount = float(input("Please key in your total amount: RM "))

#Process
if totalAmount < 1000:
    discount = float(totalAmount)*0.02
elif ((totalAmount >= 1000) and (totalAmount < 5000)):
    discount = float(totalAmount)*0.05
else:
    discount = float(totalAmount)*0.10

nettAmount = totalAmount - discount

#Output
print("Your total discount is: RM", "%.2f" % discount)
print("Your net amount is: RM", "%.2f" % nettAmount)