# Number Analysis System

A simple Python program that accepts numbers continuously, analyzes each number immediately, and shows a summary when the user exits.

## Features

- Accepts integer input repeatedly until the user types `exit`
- Classifies each number as `Even`/`Odd`
- Determines whether each number is `Positive`, `Negative`, or `Zero`
- Checks if each number is greater than `100`
- Prints an immediate analysis for each input
- Prints a final summary report of all entered numbers

## Usage

Run the program with:

```bash
python hello_ml.py
```

Enter numbers one by one. Type `exit` to finish and view the summary.

## Example Output

```
Enter a number or type 'exit' to finish: 10
Number 10: Even, Positive, not greater than 100
Enter a number or type 'exit' to finish: -5
Number -5: Odd, Negative, not greater than 100
Enter a number or type 'exit' to finish: 150
Number 150: Even, Positive, greater than 100
Enter a number or type 'exit' to finish: 0
Number 0: Even, Zero, not greater than 100
Enter a number or type 'exit' to finish: exit

Number Analysis Summary
Total numbers entered: 4
Even numbers: 3
Odd numbers: 1
Positive numbers: 2
Negative numbers: 1
Zero entries: 1
Numbers greater than 100: 1
```
