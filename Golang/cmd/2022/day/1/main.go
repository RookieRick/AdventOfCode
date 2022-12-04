package main

import (
	"fmt"
	"math"
	"sort"
	"strconv"

	"rookierick.com/aoc/internal/utils/inputs"
)

func main() {
	input, err := inputs.GetInput()
	if err != nil {
		panic(err)
	}
	fmt.Println(len(input))

	// Part 1:
	packs := []float64{} // may or may not need to actually collect these.. ok yeah we do for part 2 :)
	currentPack := 0.0
	maxPack := 0.0
	for _, weight := range input {
		if weight != "" {
			currentWeight, _ := strconv.ParseFloat(weight, 64)
			currentPack += currentWeight
		} else {
			packs = append(packs, currentPack)
			maxPack = math.Max(maxPack, currentPack)
			currentPack = 0
		}
	}
	if currentPack > 0 { // catch last one if there's not an empty line at EOF
		packs = append(packs, currentPack)
		maxPack = math.Max(maxPack, currentPack)
	}
	fmt.Println("Max pack: ", maxPack)

	// part 2:
	sort.Float64s(packs)
	topThree := 0.0
	for _, weight := range packs[len(packs)-3:] {
		topThree += weight
	}
	fmt.Println("Top 3: ", topThree)

}
