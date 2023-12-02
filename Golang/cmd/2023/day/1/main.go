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

	sums := [2]int{0, 0}

	for _, line := range input {
		scannerPart1 := regexp.MustCompile(`^[^\d]*(\d).*?(\d)?[^\d]*$`)
		forwardScannerPart2 := regexp.MustCompile(`^.*?(\d|one|two|three|four|five|six|seven|eight|nine)`)
		backwardScannerPart2 := regexp.MustCompile(`^.*?(\d|` + reverseString(`one|two|three|four|five|six|seven|eight|nine`) + `)`)

		val1Part2 := forwardScannerPart2.FindStringSubmatch(line) // fullstring, first match (should always be present)
		lineReversed := reverseString(line)
		val2Part2 := backwardScannerPart2.FindStringSubmatch(lineReversed) // fullstring, first match (maybe blank)

		vals := [][]string{
			scannerPart1.FindStringSubmatch(line), // fullstring, first match, second (maybe)
			{"", val1Part2[1], val2Part2[1]},      // placeholder, matches from forward and reverse search, second one may be blank
		}

		parsed := [2]int{}

		for i := 0; i < 2; i++ {

			if vals[i][2] == "" {
				vals[i][2] = vals[i][1]
			}
			if i == 1 { // extra processing for part 2, convert to numeric
				for numericVal, wordVal := range []string{"ZERO", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"} {
					// zero should never match but whatever, I'm done with this stupid day 1 that belongs on day 15 lol
					for j := 1; j <= 2; j++ {
						vals[i][j] = strings.Replace(vals[i][j], wordVal, strconv.Itoa(numericVal), 1)
						vals[i][j] = strings.Replace(vals[i][j], reverseString(wordVal), strconv.Itoa(numericVal), 1)
					}
				}
			}
			val, _ := strconv.Atoi(vals[i][1] + vals[i][2])
			parsed[i] = val
			sums[i] += val
		}

	}

	fmt.Println("Part 1", sums[0])
	fmt.Println("Part 2", sums[1])

	fmt.Println("fin.")

}

func reverseString(str string) string { // thanks AI for saving me some typing :D
	reversedString := ""
	for i := len(str) - 1; i >= 0; i-- {
		reversedString += string(str[i])
	}
	return reversedString
}
