package main

import (
	"fmt"

	"rookierick.com/aoc/internal/utils/inputs"
)

// we'll define ringBuffer as a specialized queue - a ring buffer with (not terribly efficient) lookup and "distinct"
type ringBuffer struct {
	_buffer  []byte
	capacity int // if 0, the ring is infinite.. so it's just a queue
}

func (rb *ringBuffer) enqueue(char byte) {
	if rb.capacity > 0 && len(rb._buffer) == rb.capacity { // we're full, let the oldest value fall off
		rb.dequeue()
	}
	(*rb)._buffer = append(rb._buffer, char)
}

func (rb *ringBuffer) dequeue() byte {
	char := rb._buffer[0]
	(*rb)._buffer = rb._buffer[1:]
	return char
}

func (rb ringBuffer) contains(charToFind byte) bool {
	for _, char := range rb._buffer {
		if char == charToFind {
			return true
		}
	}
	return false
}

// distinct returns true if we have a full buffer with distinct values
func (rb ringBuffer) distinct() bool {
	if rb.capacity <= 0 {
		return false
	} // can't ever be "full" if it's infinite
	if len(rb._buffer) < rb.capacity {
		return false
	}

	observed := make(map[byte]bool)
	for _, val := range rb._buffer {
		if observed[val] {
			return false
		} else {
			observed[val] = true
		}
	}
	return true
}

func main() {
	input, err := inputs.GetInput()
	if err != nil {
		panic(err)
	}
	fmt.Println(len(input))

	buffer := input[0]

	for part := 1; part <= 2; part++ {
		tracker := ringBuffer{}
		if part == 1 {
			tracker.capacity = 3
		} else {
			tracker.capacity = 13
		}

		markerIndex := -1
		for i := 0; i < len(buffer); i++ {
			if tracker.distinct() && !tracker.contains(buffer[i]) {
				markerIndex = i + 1
				break
			} else {
				tracker.enqueue(buffer[i])
			}
		}
		fmt.Println("part ", part, ":", markerIndex)
	}
	fmt.Println("fin.")
}
