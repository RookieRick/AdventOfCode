package main

import (
	"fmt"
	"regexp"
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

	lineSplitter := regexp.MustCompile(`^Card\s+(.*)+:(.*)\|(.*)$`) // card ID, winning nums, your nums

	winCounts := make([]int, len(input)) // simple ledge for traversal in part 2

	splitAndConvert := func(in string) []int {
		result := []int{}
		nums := strings.Fields(in)
		for _, num := range nums {
			parsed, _ := strconv.Atoi(num)
			result = append(result, parsed)
		}
		return result
	}

	sumPart1 := 0

	for i, line := range input {
		fmt.Println(line)
		parts := lineSplitter.FindStringSubmatch(line)

		winningCount := 0

		// ignore card ID for now at least (part 1)
		winningNums := map[int]bool{} // poor man's set
		for _, n := range splitAndConvert(parts[2]) {
			winningNums[n] = true
		}

		for _, cardNum := range splitAndConvert(parts[3]) {
			if winningNums[cardNum] {
				winningCount += 1
			}
		}

		if winningCount > 0 {
			sumPart1 += 1 << (winningCount - 1)
			winCounts[i] = winningCount
		}

	}

	fmt.Printf("Part 1: %v\n", sumPart1)

	// part 2

	part2Total := 0
	for i := len(winCounts) - 1; i >= 0; i-- {
		count := 1 // always count self
		if winCounts[i] > 0 {
			for j := i + 1; j <= len(winCounts) && j <= i+winCounts[i]; j++ {
				count += winCounts[j]
			}
		}
		winCounts[i] = count
		part2Total += count
	}
	fmt.Printf("Part 2: %v\n", part2Total)

	fmt.Println("fin.")

}
