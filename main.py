import json
# print Hello world
print("\nHello world\n")

# if else
if 5 > 1:
    print("5 > 1  TRUE!\n")

a = 8
if a == 5:
    print("a = 5")
elif a == 10:
    print("a = 10")
else:
    print("a != 5 AND a != 10\n")

# for loop
for x in range(1, 6):
    print("Test for loop : ",x)
print("End program\n")

# numeric - array (list)
number = [2, 4, 6, 8, 10, 12]
print("number[3] :",number[3])
print("number list  :",number,"\n")

# associative array (dict)
scores  = {"SCS307": 4 , "SCS343": 3 ,"SCS302":3.5, "SCS408": 4 }
brands = {"Toyota": 1 , "BMW": 2 , "Honda": 3}
print("scores SCS408 = ",scores["SCS408"] )
print("scores  dict :",scores, "\n" )

# save array to json
print("JSON ↓↓")
print("scores",json.dumps(scores))
print("brands",json.dumps(brands),"\n")

with open("brands.json", "w") as f:
    json.dump(brands,f)
