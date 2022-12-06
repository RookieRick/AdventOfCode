package main

import (
	"fmt"

	"rookierick.com/aoc/internal/utils/inputs"
)

func main() {
	input, err := inputs.GetInput()
	if err != nil {
		panic(err)
	}
	fmt.Println(len(input))

	accum := 0
	accum2 := 0
	setIndex := 0
	currentSet := make([]string, 3)
	for _, line := range input {
		// at least for part 1, we don't need to actually split this up
		substrLen := len(line) / 2
		string1 := line[:substrLen]
		string2 := line[substrLen:]
		common := set(string1).Intersect(set(string2))
		accum += common.BitwiseSum()
		if setIndex < 3 {
			currentSet[setIndex] = line
			setIndex = (setIndex + 1) % 3 // reset our index to 0 once we've filled our buffer
		}
		if setIndex == 0 { // setIndex will always be incremented above on FIRST pass, so if we see 0 it means we filled buffer
			setCommon := set(currentSet[0]).Intersect(set(currentSet[1])).Intersect(set(currentSet[2]))
			accum2 += setCommon.BitwiseSum()
		}
	}
	fmt.Println("Part 1: ", accum)
	fmt.Println("Part 2: ", accum2)
}

func getPriority(char uint8) int {
	// fistshake at uppercase coming before lower in ascii table lol
	// note we don't bother validating input - if you pass something other than a..z or A..Z you're.. not solving day3 of 2022..
	if char > 'Z' {
		return int(char) - int('a') + 0
	} else {
		return int(char) - int('A') + 26
	}
}

// hat tip to https://codereview.stackexchange.com/questions/88307/checking-for-any-character-common-to-two-strings-go-is-50%C3%97-slower-than-python for the bitset idea and implementation
// adapted here to support more than 32 chars (we need 52, so we'll just use 64bit integer instead of 32)
// and to deal with the fact that we need lower AND uppercase - we can lean on our "priority" for that
// for now just embedding it here instead of e.g., a util as it seems pretty special-case...
// charSet is a limited bitset to contain all lowercase latin characters (a-z).
type charSet struct {
	bits uint64
}

// Set switches a bit to 1 for any given character in range a..z or A..Z
// Characters outside this range have undefined behavior.
func (c *charSet) Set(i uint8) {
	c.bits |= 1 << getPriority(i)
}

// Intersect returns intersection of two charSets intersect
func (c charSet) Intersect(o charSet) charSet {
	return charSet{bits: c.bits & o.bits}
}

func (c charSet) BitwiseSum() int {
	sum := 0
	for i := 1; i <= 52; i++ {
		if c.bits&(1<<(i-1)) != 0 {
			sum += i
		}
	}

	return sum
}

// set returns a charSet for all bytes in s. Bytes in s must be in the range of
// 'a' to 'z' (or uppercase). Anything outside that range is regarded as undefined behavior.
func set(s string) charSet {
	var c charSet
	for i := 0; i < len(s); i++ {
		c.Set(s[i])
	}
	return c
}
