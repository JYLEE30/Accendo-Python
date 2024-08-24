import pandas as pd

# Eg. 1
a = (["saya", "suka", "makan"],
     ["saya", "suka", "makan"])
b = pd.DataFrame(a, columns = ['ID','Name', 'Age'])
print(b)

# Eg. 2
a = ["saya", "suka", "makan"]