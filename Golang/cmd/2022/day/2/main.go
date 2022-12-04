package main

import (
	"fmt"
	"strings"

	"rookierick.com/aoc/internal/utils/inputs"
)

func main() {
	input, err := inputs.GetInput()
	if err != nil {
		panic(err)
	}
	fmt.Println(len(input))

	shapeValues := map[string]int{
		"A": 1, // rock - beats 3, beaten by 2
		"B": 2, // paper - beats 1, beaten by 3
		"C": 3, // scissors - beats 2, beaten by 1
		"X": 1,
		"Y": 2,
		"Z": 3,
	}
	scoreLookup := map[int]int{
		// anything vs same thing: mine - theirs = 0
		// rock vs paper: 1 - 2 = -1 lose,  vs scissors: 1 - 3 = -2, win
		// scissors vs paper: 3 - 2 = 1 win, vs rock: 3 - 1 = 2, lose
		// paper vs rock: 2 -1 = 1 win, vs scissors: 2 - 3 = -1 lose
		0:  3, // draw
		1:  6, // win
		-2: 6, // win
		-1: 0, // lose
		2:  0, //lose
	}

	strategyOutcomes := map[string]map[string]int{
		// first key is our desired outcome, second is opponent's move
		// There's a more clever algorithm to be had than this brute force map here but whatever
		// Lose
		"X": {"A": shapeValues["C"], "B": shapeValues["A"], "C": shapeValues["B"]},
		// Draw:
		"Y": {"A": shapeValues["A"] + 3, "B": shapeValues["B"] + 3, "C": shapeValues["C"] + 3},
		// Win:
		"Z": {"A": shapeValues["B"] + 6, "B": shapeValues["C"] + 6, "C": shapeValues["A"] + 6},
	}

	totalScore := []int{0, 0} // per puzzle part

	for _, round := range input {
		split := strings.Split(round, " ")
		theirs := shapeValues[split[0]]
		mine := shapeValues[split[1]]
		totalScore[0] += mine + scoreLookup[mine-theirs]
		totalScore[1] += strategyOutcomes[split[1]][split[0]]
	}
	fmt.Println("Total score (part 1): ", totalScore[0])
	fmt.Println("Total score (part 2): ", totalScore[1])
}
