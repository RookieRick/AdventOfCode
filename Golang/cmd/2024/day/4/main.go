package main

import (
	"fmt"

	"rookierick.com/aoc/internal/utils/inputs"
)

type coord struct {
	x, y int
}

type cell struct {
	letter   rune
	position coord
}

var (
	maxX  int
	maxY  int
	cells map[coord]cell
)

func (c cell) traverse(direction coord, targetWord []rune) int {
	if c.letter != targetWord[0] {
		return 0
	}
	if len(targetWord) == 1 {
		// we matched the letter and it's the last in the word - success!
		return 1
	}
	targetX := c.position.x + direction.x
	targetY := c.position.y + direction.y
	if targetX < 0 || targetX > maxX || targetY < 0 || targetY > maxY {
		// can't traverse further this direction
		return 0
	}

	return cells[coord{x: targetX, y: targetY}].traverse(direction, targetWord[1:])
}

func (c cell) String() string {
	return string(c.letter)
}

func main() {
	cells = make(map[coord]cell)
	input, err := inputs.GetInput()
	if err != nil {
		panic(err)
	}

	targetWord := []rune{'X', 'M', 'A', 'S'}

	maxY = len(input) - 1
	maxX = len(input[0]) - 1

	// find all X's..  for each, traverse in every possible direction looking for sequence of chars.
	// could optimize by not bothering to search if you'll hit border but skip that for first cut..
	// note need to iterate to max+1 because we accounted for array indexing when creating them
	// (to make our cartesian coords work naturally)
	potentialStarts := make([]cell, 0)
	allA := make([]cell, 0)
	for j := range maxY + 1 {
		for i := range maxX + 1 {
			pos := coord{x: i, y: maxY - j}
			c := cell{letter: rune(input[j][i]), position: coord{x: i, y: maxY - j}}
			cells[pos] = c
			if c.letter == targetWord[0] {
				potentialStarts = append(potentialStarts, c)
			}
			if c.letter == 'A' {
				allA = append(allA, c)
			}
		}
	}

	matches := 0
	// would be kinda cool to do this inline in the same loop above (and basically lazy-create cells) but... eeeeh.
	for _, start := range potentialStarts {
		if start.letter == targetWord[0] {
			// todo iterate over all possible directions..
			for i := -1; i <= 1; i++ {
				for j := -1; j <= 1; j++ {
					if !(i == 0 && j == 0) { // don't "traverse" into ourselves
						matches += start.traverse(coord{x: i, y: j}, targetWord)
					}
				}
			}
		}
	}

	fmt.Println("Part 1 matches:", matches)

	matches = 0
	for _, start := range allA {
		// just brute force check diagonals - since we're using a map we don't really need to fuss with bounds checking
		pos := []coord{
			{x: start.position.x - 1, y: start.position.y - 1},
			{x: start.position.x + 1, y: start.position.y + 1},
			{x: start.position.x - 1, y: start.position.y + 1},
			{x: start.position.x + 1, y: start.position.y - 1},
		}
		if ((cells[pos[0]].letter == 'M' && cells[pos[1]].letter == 'S') || (cells[pos[0]].letter == 'S' && cells[pos[1]].letter == 'M')) &&
			((cells[pos[2]].letter == 'M' && cells[pos[3]].letter == 'S') || (cells[pos[2]].letter == 'S' && cells[pos[3]].letter == 'M')) {
			matches += 1
		}
	}

	fmt.Println("Part 2 matches:", matches)
}
