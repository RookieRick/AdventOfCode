package main

import (
	"fmt"
	"math"
	"sort"
	"strconv"
	"strings"

	"rookierick.com/aoc/internal/utils/inputs"
)

func main() {
	input, err := inputs.GetInput()
	if err != nil {
		panic(err)
	}

	leftVals := []int{}
	rightVals := []int{}

	for _, line := range input {
		splitVals := strings.Fields(line)

		leftVal, _ := strconv.Atoi(splitVals[0])
		rightVal, _ := strconv.Atoi(splitVals[1])

		leftVals = append(leftVals, leftVal)
		rightVals = append(rightVals, rightVal)
	}

	for part := 1; part <= 2; part++ {
		sum := 0

		sort.Ints(leftVals)
		sort.Ints(rightVals)

		if part == 1 {
			for i := 0; i < len(leftVals); i++ {
				sum += int(math.Abs(float64(leftVals[i]) - float64(rightVals[i])))
			}
		} else {
			counts := make(map[int]int)
			for _, val := range rightVals {
				counts[val]++
			}
			for _, val := range leftVals {
				sum += val * counts[val]
			}
		}

		fmt.Printf("Part %v: %v \n", part, sum)
	}

	fmt.Println("fin.")

}
