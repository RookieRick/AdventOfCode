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

	counter := 0
	counter2 := 0

	assignments := [][]int{{0, 0}, {0, 0}}
	for _, line := range input {
		pair := strings.Split(line, ",")
		for i, assignmentText := range pair {
			bounds := strings.Split(assignmentText, "-")
			assignments[i][0], _ = strconv.Atoi(bounds[0])
			assignments[i][1], _ = strconv.Atoi(bounds[1])
		}
		if assignments[0][0] >= assignments[1][0] && assignments[0][1] <= assignments[1][1] ||
			assignments[1][0] >= assignments[0][0] && assignments[1][1] <= assignments[0][1] {
			counter += 1
		}
		if assignments[0][1] >= assignments[1][0] && assignments[0][1] <= assignments[1][1] ||
			assignments[1][1] >= assignments[0][0] && assignments[1][1] <= assignments[0][1] {
			counter2 += 1
		}
	}
	fmt.Println("part 1: ", counter)
	fmt.Println("part 2: ", counter2)
}
