#Question 6
temp = float(input("Please enter the temperature (Celsius): "))

if ((temp==0) and (temp<=30)):
    print("Status: Cold")
elif ((temp>30) and (temp<=50)):
    print("Status: Medium")
elif ((temp>50) and (temp<=70)):
    print("Status: Hot")
elif ((temp>70) and (temp<=100)):
    print("Status: Very Hot")

print()

#Question 7
weight = float(input("Please enter the weight (kg): "))

if ((weight>0) and (weight<=2)):
    rm = float("Payment cost: RM ", "%.2f" % 2.5)
elif ((weight>2) and (weight<=5)):
    rm = float(3.8)
    print("Payment cost: RM ", )
elif ((weight>5) and (weight<=10)):
    rm = float(6.0)
    print("Payment cost: RM ")
elif ((weight>10) and (weight<=20)):
    rm = float(10.0)
    print("Payment cost: RM ")
elif (weight>20):
    print("Payment cost: VOID")
print()

#Question 8

#Question 9

#Question 10