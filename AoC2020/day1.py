from AoC2020.inputs import get_input

if __name__ == "__main__":
    expenses = [expense for expense in get_input(1) if expense < 2021]

    # part 1:

    for i in range(0, len(expenses)):
        for j in range(i+1, len(expenses)):
            if expenses[i] + expenses[j] == 2020:
                print(f"{i}, {j}: {expenses[i]}*{expenses[j]}={expenses[i]*expenses[j]}")
                print("there should be only one but we'll let the loop keep running")

    # part 2:
    for i in range(0, len(expenses)):
        for j in range(i+1, len(expenses)):
            for k in range (j+1, len(expenses)):
                if expenses[i] + expenses[j] + expenses[k] == 2020:
                    print(f"{i}, {j}, {k}: {expenses[i]}*{expenses[j]}*{expenses[k]}={expenses[i]*expenses[j]*expenses[k]}")
                    print("there should be only one but we'll let the loop keep running")

    print("fin.")
