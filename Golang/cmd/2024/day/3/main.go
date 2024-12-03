package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/dlclark/regexp2"
	"rookierick.com/aoc/internal/utils/inputs"
)

func main() {
	input, err := inputs.GetInput()
	if err != nil {
		panic(err)
	}

	mulRegex := regexp2.MustCompile(`mul\((?'x'\d+),(?'y'\d+)\)`, regexp2.None)
	//part2Regex := regexp2.MustCompile(`do\(\).*?(?!don\'t\(\)).*?mul\((?'x'\d+),(?'y'\d+)\)`, regexp2.None)
	if err != nil {
		panic(err)
	}

	// regexes := make([]*regexp2.Regexp, 0)
	// regexes = append(regexes, part1Regex)
	// regexes = append(regexes, part1Regex)

	results := []int{0, 0}
	// unspecified in problem and doesn't affect part 1 - ASSUMING for part 2 should transcend newlines?
	smashedInput := strings.Join(input, "")

	inputs := make([][]string, 2)
	// part 1 just uses raw input (smashed because I felt like it)
	inputs[0] = []string{smashedInput}

	// for part2, just split on "don't", everything to left is valid, then subdivide right and repeat
	// prepend a "do()" to simplify split+parse and account for default starting condition
	inputs[1] = make([]string, 0)
	subPrograms := strings.Split("do()"+smashedInput, "don't()")
	for _, sp := range subPrograms {
		noops, executable, found := strings.Cut(sp, "do()")
		_ = noops
		if found {
			inputs[1] = append(inputs[1], executable)
		}
	}

	for part := range 2 {
		for _, line := range inputs[part] {
			// ok so this screams regex
			// and hooray for dlclark for negative lookaround support (like I didn't have to google the correct "regex term" for that....)
			//   ....and, ok I apparently don't know how to write the correct negative lookaround, so time to stop trying to force
			//   regex to do things it really shouldn't and just parse the damn thing.
			//   OH "at the beginning of the program mul instructions are ENABLED"  :facepalm: --> still go ahead and just split the strings..

			subMatch, _ := mulRegex.FindStringMatch(line) //FindAllStringSubmatch(line, -1)
			//var subMatches []string
			for subMatch != nil {
				x, _ := strconv.Atoi(subMatch.GroupByName("x").Capture.String())
				y, _ := strconv.Atoi(subMatch.GroupByName("y").Capture.String())
				fmt.Printf("Adding %d x %d = %d\n", x, y, x*y)
				results[part] += x * y

				subMatch, _ = mulRegex.FindNextMatch(subMatch)
			}
		}
	}

	fmt.Println("Results:", results)
	fmt.Println("fin.")

}
