import math
import statistics

with open("./raw_inputs/day7.txt") as input_file:
    raw = input_file.readline()
    positions = [int(val) for val in raw.split(",")]

# debug:
#positions = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]

target = statistics.median(positions)
fuel = sum([abs(start - target) for start in positions])
print(f"fuel={fuel}")

# target = round(statistics.mean(positions))  # this is intuitive and works for the debug data but not for the real data
# so just kinda brute force it..
min_fuel = math.inf
for target in range(min(positions), max(positions)+1):
    fuel = 0
    for start in [pos for pos in positions if pos != target]:
        distance = abs(start - target)
        consumed = int(((2 + (distance - 1)) / 2) * distance)
        fuel += consumed
        if fuel > min_fuel:
            break  # we've surpassed min, move on to next target
    min_fuel = min([fuel, min_fuel])


print(f"fuel={min_fuel}")


print("fin.")

