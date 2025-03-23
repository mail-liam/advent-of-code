package main

import "testing"

EXAMPLE_DATA = "3   4
4   3
2   5
1   3
3   9
3   3"

func TestPart1(t *testing.T) {
	result := main.Part1(EXAMPLE_DATA)

	if result != 11 {
		t.Errorf("Invalid result for Part 1 Example Data. Received %q. Expected 11", result)
	}
}