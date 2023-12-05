package main

import (
	"fmt"
	"strconv"
	"strings"

	"rookierick.com/aoc/internal/utils/inputs"
)

func main() {
	input, err := inputs.GetInput()
	if err != nil {
		panic(err)
	}
	fmt.Println(len(input))

	sum1 := 0
	sum2 := 0

	limits := map[string]int{"red": 12, "green": 13, "blue": 14}

	for i, line := range input {
		possible := true
		data := strings.Split(line, ":")[1]
		sets := strings.Split(data, ";")
		mins := map[string]int{"red": 0, "green": 0, "blue": 0} // slightly counter-intuitive, we're finding local max but it's the minimum number REQUIRED for the game

		for _, set := range sets {
			cubes := strings.Split(set, ",")
			for _, cubeCount := range cubes {
				countAndType := strings.Split(strings.Trim(cubeCount, " "), " ")
				count, _ := strconv.Atoi(countAndType[0])
				color := countAndType[1]
				if count > limits[color] {
					possible = false
				}
				if count > mins[color] {
					mins[color] = count
				}
			}
		}
		if possible {
			sum1 += i + 1 // Game ID - not bothering to parse this as they are just sequentially numbered
		}
		gamePower := 1
		for _, v := range mins {
			gamePower *= v
		}
		sum2 += gamePower
	}

	fmt.Printf("Part 1: %v\n", sum1)
	fmt.Printf("Part 2: %v\n", sum2)
}
