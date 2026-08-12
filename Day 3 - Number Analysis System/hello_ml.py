numbers = []
while True:
    user_input = input("Enter a number or type 'exit' to finish: ").strip()
    if user_input == "":
        print("Please enter a number or 'exit'.")
        continue
    if user_input.lower() == "exit":
        break
    try:
        number = int(user_input)
    except ValueError:
        print("Invalid input. Enter a valid integer.")
        continue
    numbers.append(number)
    if number % 2 == 0:
        parity = "Even"
    else:
        parity = "Odd"
    if number > 0:
        sign = "Positive"
    elif number < 0:
        sign = "Negative"
    else:
        sign = "Zero"
    if number > 100:
        greater = "greater than 100"
    else:
        greater = "not greater than 100"
    print(f"Number {number}: {parity}, {sign}, {greater}")
print("\nNumber Analysis Summary")
if not numbers:
    print("No numbers were entered.")
else:
    total = len(numbers)
    evens = sum(1 for n in numbers if n % 2 == 0)
    odds = total - evens
    positives = sum(1 for n in numbers if n > 0)
    negatives = sum(1 for n in numbers if n < 0)
    zeros = sum(1 for n in numbers if n == 0)
    greater100 = sum(1 for n in numbers if n > 100)
    print(f"Total numbers entered: {total}")
    print(f"Even numbers: {evens}")
    print(f"Odd numbers: {odds}")
    print(f"Positive numbers: {positives}")
    print(f"Negative numbers: {negatives}")
    print(f"Zero entries: {zeros}")
    print(f"Numbers greater than 100: {greater100}")
