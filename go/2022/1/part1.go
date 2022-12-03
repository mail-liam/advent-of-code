package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {
	file, _ := os.Open("input.txt")
	reader := bufio.NewScanner(file)

	totals := make([]int, 0)
	current := 0
	var num int
	more := false
	for {
		more = reader.Scan()
		line := reader.Text()

		if line != "" {
			num, _ = strconv.Atoi(line)
			current += num
		} else if current != 0{
			totals = append(totals, current)
			current = 0
		}

		if !more {
			break
		}
	}
	maximum := 0
	for _, num := range totals {
		if num > maximum {
			maximum = num
		}
	}
	fmt.Print(maximum)
}