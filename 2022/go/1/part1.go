package main

import (
	"fmt"
	"os"
)

func main() {
	data, _ := os.ReadFile("input.txt")

	for _, line := range data {
		fmt.Print(line)
		fmt.Print("-----")
	}
}