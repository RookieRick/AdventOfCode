package main

import (
	"fmt"
	"strconv"
	"strings"

	"rookierick.com/aoc/internal/utils/inputs"
)

const debug = false

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
		if isSafeReport(report) {
			safeCount++
		} else {
			unsafeReports = append(unsafeReports, report)
		}
	}
	fmt.Println("Part 1 safe count: ", safeCount)

	// part 2 - take another pass through those captured as unsafe to see if they can be salvaged
	preScreened := 0 // counter to see how many we can reject outright for having more than 1 "unsafe" delta

reportLoop: // label the outer loop so we can jump to next report if we find a safe variant.
	for _, report := range unsafeReports {
		var deltas []int
		var negatives, positives, zeros int

		dump := func() {
			if debug {
				fmt.Println("report: ", report, "deltas:", deltas)
			}
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
					preScreened++
					continue reportLoop
				}
			} else if (positives > 1 && negatives+zeros > 1) || (negatives > 1 && positives+zeros > 1) {
				dump()
				preScreened++
				continue reportLoop
			}
		}
		// if we made it this far, we haven't ruled this one out as having multiple zeros or more than 1 mismatched delta type..
		// we could probably be clever here about how we remove and retry, but in the interest of time I'll just brute force it:
		for skip := range len(report) {
			modifiedReport := make([]int, 0)
			modifiedReport = append(modifiedReport, report[:skip]...)
			modifiedReport = append(modifiedReport, report[skip+1:]...)
			if isSafeReport(modifiedReport) {
				safeCount++
				continue reportLoop
			}
		}
	}
	fmt.Printf("Rejected %v of %v reports in prescreening\n", preScreened, len(unsafeReports))

	fmt.Println("Part 2 safe count:", safeCount)
	fmt.Println("fin.")

}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func isSafeReport(levels []int) bool {
	lastDelta := 0 // negative if delta was in descending order, positive if ascending, 0 if equal (unsafe)
	for i := range len(levels) - 1 {
		delta := levels[i+1] - levels[i]
		if delta == 0 || abs(delta) > 3 {
			// violated constraint of delta between 1..3
			return false
		}
		if (delta < 0 && lastDelta > 0) || (delta > 0 && lastDelta < 0) {
			// violated all ascending/descending constraint
			return false
		}
		lastDelta = delta
	}
	return true
}
