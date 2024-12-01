package main

import (
	"fmt"

	"rookierick.com/aoc/internal/utils/inputs"
)

func main() {
	input, err := inputs.GetInput()
	if err != nil {
		panic(err)
	}
	fmt.Println(len(input))

	for _, line := range input {
		fmt.Println(line)
	}

	fmt.Println("fin.")

}
