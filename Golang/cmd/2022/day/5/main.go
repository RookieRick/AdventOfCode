package main

import (
	"fmt"
	"strconv"
	"strings"

	"rookierick.com/aoc/internal/utils/inputs"
)

type stack []byte

func (s *stack) push(char byte) {
	// for convenience since this is a custom made stack, we'll just "ignore" push of space characters
	if char != ' ' {
		*s = append(*s, char)
	}
}

func (s *stack) pop() byte {
	char := (*s)[len(*s)-1]
	*s = (*s)[:len(*s)-1]
	return char
}

func main() {
	input, err := inputs.GetInput()
	if err != nil {
		panic(err)
	}
	fmt.Println(len(input))

	// awfully tempting to just hard-code the starting stacks but let's be a good kid and try to parse EVERYTHING..
	// we'll just read until we get to blank line..  At that point we have our "stacks" including labels, they're
	// just "addressed" with a "y" axis that has 0 at top and points down
	// note though we CAN make some inferrences from the structure of the input data..  (e.g., < 11 fixed-width columns with one-char index)
	headerLines := make([]string, 0)
	instructions := make([]string, 0)

	markerObserved := false
	for _, line := range input {
		if line == "" {
			markerObserved = true
		} else if markerObserved {
			// TODO: we can actually parse these inline during initial scan
			instructions = append(instructions, line)
		} else {
			headerLines = append(headerLines, line)
		}
	}

	indicesLine := headerLines[len(headerLines)-1]
	// can't use e.g., strings.Fields for the "stacks" because they have just empty spaces between..
	// so instead, just leverage constraints..  cols (relative to zero) 1, 5, 9, 13, etc..
	for part := 1; part <= 2; part++ {
		indices := make([]byte, 0)
		stacks := make(map[byte]*stack)
		for i := 1; i < len(headerLines[len(headerLines)-1]); i += 4 {
			indices = append(indices, indicesLine[i])
			stacks[indicesLine[i]] = &stack{}
			for j := len(headerLines) - 2; j >= 0; j-- {
				stacks[indicesLine[i]].push(headerLines[j][i])
			}
		}

		for i := 0; i < len(instructions); i++ {
			instruction := strings.Fields(instructions[i])
			//instruction will now be a slice like ["move", "5", "from", "3", "to", "6"]
			// instructions all use the same grammar so we only need to extract the values.. for
			// quantity we'll need an int, for the indices a byte
			quantity, _ := strconv.Atoi(instruction[1])
			source := stacks[instruction[3][0]]
			dest := stacks[instruction[5][0]]

			if part == 2 {
				intermediate := &stack{}
				for j := 0; j < quantity; j++ {
					intermediate.push(source.pop())
				}
				source = intermediate // we'll reverse back off of this to move chunks in order
			}

			for j := 0; j < quantity; j++ {
				dest.push(source.pop())
			}

			//fmt.Println(instruction, quantity, source, dest)
		}

		result := ""
		for _, key := range indices {
			result += string(stacks[key].pop()) // let's hope we don't have any empty stacks..?
		}

		fmt.Println("Part ", part, ": ", result)
	}
	fmt.Println("fin.")
}
