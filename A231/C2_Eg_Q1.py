import os
os.system('cls')

#Input
grossSalary = float(input("Please enter your gross salary: RM "))

#Process
if grossSalary > 1000:
    tax = float(grossSalary)*0.02
    print("The tax on your gross salary is: RM", "%.2f" % tax)
else:
    tax = 0
    print("Your tax has been waived.")

#Output
netSalary = float(grossSalary - tax)
print("Your net salary is: RM", "%.2f" % netSalary)