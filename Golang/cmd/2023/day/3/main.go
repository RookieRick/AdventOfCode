package main

import (
	"fmt"
	"strconv"
	"strings"

	"rookierick.com/aoc/internal/utils/inputs"
)

type potentialGearCollection struct {
	// potentialGears will be indexed by the position of the "*" with a list of numbers adjacent
	// (which we'll post-process to select only those with exactly 2)

	padded         []string // ref back to "schematic"
	currentIndices []string
	potentialGears map[string][]int // indexed by position of "*'"
}

// collect will look at whether a symbol represents a potential gear, and will record it as such.
// intended for use during parsing of a number; provides fodder for record
func (pgc *potentialGearCollection) collect(y int, x int) {
	if pgc.padded[y][x] == '*' {
		pgc.currentIndices = append(pgc.currentIndices, fmt.Sprintf("%v,%v", y, x))
	}
}

// record is intended to call after we've finished parsing a number and will record that number
// in the list for each potential gear adjacent to it
func (pgc *potentialGearCollection) record(num int) {
	for _, index := range pgc.currentIndices {
		pgc.potentialGears[index] = append(pgc.potentialGears[index], num)
	}
	pgc.currentIndices = []string{} // reset and prepare for next collect
}

func (pgc *potentialGearCollection) process() int {
	sum := 0
	for _, adjacentNums := range pgc.potentialGears {
		if len(adjacentNums) == 2 {
			sum += adjacentNums[0] * adjacentNums[1]
		}
	}
	return sum
}

func main() {
	input, err := inputs.GetInput()
	if err != nil {
		panic(err)
	}
	fmt.Println(len(input))

	// note let's leverage fact that data is rectangular - we'll simplify our lives in the processing stage if we pad the edges
	// so we don't have to constantly check bounds...
	emptyLine := strings.Repeat(".", len(input[0])+2)
	padded := []string{emptyLine}
	for _, line := range input {
		padded = append(padded, "."+line+".")
	}
	padded = append(padded, emptyLine)

	partNums := []int{}

	pgc := potentialGearCollection{
		padded:         padded,
		currentIndices: []string{},
		potentialGears: map[string][]int{},
	}

	for lineNum, line := range padded {
		// rather than parse every number, let's find the "symbols" and then just look around them..
		// actually, no.. what if there are TWO symbols adjacent to a number - don't want to count the number twice
		// so just scan line by line, pick out numbers, and look at neighbors until you find a symbol or exhaust possible neighbors..

		numStartCursor := -1
		numEndCursor := -1
		isPartNumber := false
		for i := 0; i < len(line); i++ {
			if isNumeric(line[i]) {
				if numStartCursor == -1 { // start a new number
					numStartCursor = i
					// at start of number, we need to check prev chars as well as above/below
					for offset := -1; offset <= 1; offset++ {
						if isSymbol(padded[lineNum+offset][i-1]) {
							isPartNumber = true
							pgc.collect(lineNum+offset, i-1)
							// break // once we determine it's a part num don't keep checking (no loner true for part 2 lol)
						}
						if offset != 0 && isSymbol(padded[lineNum+offset][i]) {
							isPartNumber = true
							pgc.collect(lineNum+offset, i)
							//break
						}
					}
				} else if !isPartNumber { // reading a number and haven't previously noted as part # so check above/below
					if isSymbol(padded[lineNum-1][i]) || isSymbol(padded[lineNum+1][i]) {
						isPartNumber = true
						pgc.collect(lineNum-1, i)
						pgc.collect(lineNum+1, i)
					}
				}
				numEndCursor = i
			} else { // not numeric
				if numEndCursor > -1 { // we were parsing a number, so need to finish that
					// note we've already checked the immediate top/bottom neighbors of last char
					if !isPartNumber {
						for offset := -1; offset <= 1; offset++ {
							if isSymbol(padded[lineNum+offset][i]) {
								isPartNumber = true
								//break
								pgc.collect(lineNum+offset, i)
							}
						}
					}

					if isPartNumber {
						// now we've got cursors for start and end, AND have determined it's a part num, so record it.
						partNum, _ := strconv.Atoi(line[numStartCursor : numEndCursor+1])
						partNums = append(partNums, partNum) // part 1 collection
						pgc.record(partNum)                  // part 2 collection
					}
				}
				// and finally reset our cursors and state var:
				numStartCursor = -1
				numEndCursor = -1
				isPartNumber = false
			}
		}
	}
	// at this point we should have a complete list of part numbers (as strings) so just need to parse and sum
	sum := 0
	for _, partNum := range partNums {
		sum += partNum
	}
	fmt.Printf("part 1: %v\n", sum)
	fmt.Printf("part 2: %v\n", pgc.process())

}

func isNumeric(b byte) bool {
	return b >= '0' && b <= '9'
}

func isSymbol(b byte) bool {
	return b != '.' && (b < '0' || b > '9')
}
