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
	fmt.Println(len(input))

	root := NewDirectory("/", nil)
	cwd := root

	// cheesy but easy:
	cmdHandlers := map[string]func([]string, ...string){
		// AoC == skip input validation and the like ;)
		// cd handler should expect exactly one arg
		"cd": func(outputBuffer []string, args ...string) {
			if args[0] == "/" {
				cwd = root
			} else if args[0] == ".." {
				if cwd.parent != nil {
					cwd = cwd.parent
				}
			} else {
				cwd = cwd.subdirectories[args[0]]
			}
		},
		// ls handler expects no args but should have an outputBuffer
		"ls": func(outputBuffer []string, args ...string) {
			for _, line := range outputBuffer {
				tokens := strings.Fields(line)
				if tokens[0] == "dir" {
					NewDirectory(tokens[1], cwd)
				} else {
					size, _ := strconv.Atoi(tokens[0])
					cwd.files[tokens[1]] = &File{name: tokens[1], size: size}
				}
			}
		},
	}

	i := 0
	for i < len(input) {
		line := input[i]
		tokens := strings.Fields(line)
		fmt.Println(tokens)
		if tokens[0] == "$" {
			cmd := tokens[1]
			cmdArgs := tokens[2:]
			// read output: lines until next command or EOF
			outputBuffer := []string{}
			i++
			for i < len(input) && input[i][0] != '$' {
				outputBuffer = append(outputBuffer, input[i])
				i++
			}
			cmdHandlers[cmd](outputBuffer, cmdArgs...)
		}
	}
	// we've loaded our entire directory structure, populate dir sizes:
	root.refreshSize()

	// and execute our search (for part 1)
	smallFiles := root.recursiveSearch(100000)
	smallFilesSum := 0
	for _, file := range smallFiles {
		smallFilesSum += file.size
	}
	fmt.Println("part 1: ", smallFilesSum)

	unusedSpace := 70000000 - root.size
	spaceNeeded := 30000000 - unusedSpace
	deleteDir := root.findSmallest(spaceNeeded)
	fmt.Println("part 2: delete: ", *deleteDir)

	fmt.Println("fin.")
}

type File struct {
	name string
	size int
}

type Directory struct {
	name           string
	size           int
	parent         *Directory
	subdirectories map[string]*Directory
	files          map[string]*File
}

func NewDirectory(name string, parent *Directory) *Directory {
	directory := Directory{
		name:           name,
		files:          map[string]*File{},
		subdirectories: map[string]*Directory{},
	}
	if parent != nil {
		directory.parent = parent
		parent.subdirectories[name] = &directory
	}
	return &directory
}

func (d *Directory) refreshSize() int {
	result := 0
	for _, file := range d.files {
		result += file.size
	}
	for _, sub := range d.subdirectories {
		result += sub.refreshSize()
	}
	d.size = result
	return result
}

func (d *Directory) recursiveSearch(maxSize int) []*Directory {
	result := []*Directory{}
	if d.size <= maxSize {
		result = append(result, d)
	}
	for _, subdir := range d.subdirectories {
		result = append(result, subdir.recursiveSearch(maxSize)...)
	}
	return result
}

func (d *Directory) findSmallest(minSize int) *Directory {
	var minDir *Directory
	if d.size >= minSize {
		minDir = d
	}
	for _, subdir := range d.subdirectories {
		subSmallest := subdir.findSmallest(minSize)
		if subSmallest != nil && (minDir == nil || subSmallest.size < minDir.size) {
			minDir = subSmallest
		}
	}

	return minDir
}
