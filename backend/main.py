import sys

print("Python backend started")
sys.stdout.flush()

while True:
    line = sys.stdin.readline().strip()
    if line:
        operation, numbers = line.split(':')
        num1, num2 = map(float, numbers.split(','))
       
        if operation == "sum":
            result = num1 + num2
        elif operation == "proizvedenie":
            result = num1 * num2
        elif operation == "division":
            result = num1 // num2
        else:
            result = num1 - num2
        print(result)
        sys.stdout.flush()