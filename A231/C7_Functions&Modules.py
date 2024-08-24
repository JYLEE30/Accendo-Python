def areaOfCircle(R):
    c = (22/7)*R**2
    return c

b = [3,5,6,7]

for num in b:
    print("%.2f" % areaOfCircle(num))

#Lambda (Not in Final Exam)
A=list(map(lambda x: x*x, [1,2,3]))
print(A)