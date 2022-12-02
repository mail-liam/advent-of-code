package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
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
	
	sort.Ints(totals)
	n := len(totals)
	fmt.Println(totals[n-1] + totals[n-2] + totals[n-3])
}