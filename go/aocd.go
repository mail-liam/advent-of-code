package main

import (
	"fmt"

	// "net/http"
	"os"
	"strconv"
)

func processArgs(args []string) ([]int, []string) {
	// Expect the input args in Year/Day/Part format
	if len(args) != 3 {
		return nil, []string{"Error: Expected 3 arguments (Year/Day/Part)"}
	}

	values := make([]int, 0, 3)
	errors := make([]string, 0, 3)

	year, err1 := strconv.Atoi(args[0])
	if err1 != nil {
		errors = append(errors, err1.Error())
	}
	if year < 2020 || year > 2025 {
		errors = append(errors, "Invalid Year - please specify a year between 2020 and 2025 (inclusive)")
	}

	day, err2 := strconv.Atoi(args[1])
	if err2 != nil {
		errors = append(errors, err2.Error())
	}
	if day < 1 || day > 25 {
		errors = append(errors, "Invalid Day - please specify a day between 1 and 25 (inclusive)")
	}

	part, err3 := strconv.Atoi(args[2])
	if err3 != nil {
		errors = append(errors, err3.Error())
	}
	if part != 1 && part != 2 {
		errors = append(errors, "Invalid Part - Must be either 1 or 2")
	}

	if len(errors) > 0 {
		return values, errors
	}

	values = append(values, year, day, part)

	return values, nil
}

func main() {
	values, errors := processArgs(os.Args[1:])

	if len(errors) > 0 {
		fmt.Println("Error handling inputs:")
		for _, e := range errors {
			fmt.Println(e)
		}
		os.Exit(1)
	}

	fmt.Print(values)
}
