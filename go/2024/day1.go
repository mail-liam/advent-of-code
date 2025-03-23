package main

import (
	"fmt"
	"slices"
	"strconv"
	"strings"
)

func Part1(data string) int {
	lines := strings.Split(data, "\n")
	entries := len(lines)

	leftNums := make([]int, entries)
	rightNums := make([]int, entries)

	for i, line := range lines {
		fields := strings.Fields(line)
		
		leftNum, _ := strconv.Atoi(fields[0])
		leftNums[i] = leftNum

		rightNum, _ := strconv.Atoi(fields[1])
		rightNums[i] = rightNum
		
	}

	slices.Sort(leftNums)
	slices.Sort(rightNums)

	var result int = 0
	for i := range leftNums {
		left, right := leftNums[i], rightNums[i]

		if left > right {
			result += left - right
		} else {
			result += right - left
		}
	}

	return result
}

func main() {
	EXAMPLE_DATA := "3   4\n4   3\n2   5\n1   3\n3   9\n3   3"

	result := Part1(EXAMPLE_DATA)
	fmt.Println(result)
}