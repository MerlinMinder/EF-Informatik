bl = "$multiply 4*5"

numbers = bl.split()[1]
print(int(numbers.split("*")[0])*int(numbers.split("*")[1]))

message = "$calculate 3*6"

calculate = message.split()[1]

if calculate[1] == "-":
    print(int(calculate[0])-int(calculate[2]))

if calculate[1] == "+":
    print(int(calculate[0])+int(calculate[2]))

if calculate[1] == "/":
    print(int(calculate[0])/int(calculate[2]))

if calculate[1] == "*":
    print(int(calculate[0])*int(calculate[2]))
