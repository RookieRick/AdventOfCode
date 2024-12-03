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

	var reports [][]int

	for _, line := range input {
		var rowNums []int
		for _, strVal := range strings.Fields(line) {
			val, _ := strconv.Atoi(strVal)
			rowNums = append(rowNums, val)
		}
		reports = append(reports, rowNums)
	}

	var unsafeReports [][]int
	safeCount := 0
	for _, report := range reports {
		// first determine asc/desc order and select appropriate "safety check" func
		firstDiff := report[0] - report[1]
		var unsafeDiff func(int) bool
		if firstDiff == 0 {
			unsafeReports = append(unsafeReports, report)
			continue // abs(diff) must be at least 1
		}

		if firstDiff > 0 {
			unsafeDiff = unsafeDiffDescending
		} else {
			unsafeDiff = unsafeDiffAscending
		}
		if unsafeDiff(firstDiff) {
			unsafeReports = append(unsafeReports, report)
			continue // diff not between 1 and 3 inclusive
		}
		// now check remainder of report values:
		safe := true
		for i := 1; i < len(report)-1; i++ {
			diff := report[i] - report[i+1]
			if unsafeDiff(diff) {
				safe = false
				unsafeReports = append(unsafeReports, report)
				break
			}
		}
		if safe {
			safeCount++
		}
	}
	fmt.Println("Part 1 safe count: ", safeCount)

	// part 2 - take another pass through those captured as unsafe to see if they can be salvaged

reportLoop: // label the outer loop so we can jump to next report if we find a safe variant.
	// slightly different approach now since we can't assume first pair indicates asc/desc..
	// (prob should have done it this way initially?) --> maybe rewrite the part that evaluates sequence as a func
	//   accepting an argument for max # of entries to remove..  (0 for part 1, 1 for part 2)
	//  Keep the "pre-rejection" stuff to winnow the field down before you go slightly more iterative..
	for _, report := range unsafeReports {
		var deltas []int
		var negatives, positives, zeros int

		dump := func() {
			fmt.Println("report: ", report, "deltas:", deltas)
		}

		for i := 0; i < len(report)-1; i++ {
			delta := report[i] - report[i+1]
			if delta == 0 {
				zeros++
			} else if delta > 0 {
				positives++
			} else {
				negatives++
			}
			deltas = append(deltas, delta)
			// fail fast if we detect an impossible situation:
			if zeros > 0 {
				if zeros > 1 || (positives > 0 && negatives > 0) { // multiple zero deltas or a zero and both pos and neg..
					dump()
					continue reportLoop
				}
			} else if (positives > 1 && negatives+zeros > 1) || (negatives > 1 && positives+zeros > 1) {
				//dump()
				continue reportLoop
			}
		}
		// if we made it this far, we haven't ruled this one out as having multiple zeros or more than 1 mismatched delta type..

	}

	fmt.Println("Part 2 safe count:", safeCount)
	fmt.Println("fin.")

}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func unsafeDiffAscending(diff int) bool {
	return diff >= 0 || abs(diff) > 3
}

func unsafeDiffDescending(diff int) bool {
	return diff <= 0 || abs(diff) > 3
}
