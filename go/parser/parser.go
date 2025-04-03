package parser

import (
	"errors"
	"strconv"
)

func ProcessArgs(args []string) ([]int, error) {
	// Expect the input args in Year/Day/Part format
	if len(args) != 3 {
		return nil, errors.New("Expected 3 arguments (Year/Day/Part)")
	}

	parserErrors := make([]error, 0, 3)

	year, err1 := strconv.Atoi(args[0])
	if err1 != nil {
		parserErrors = append(parserErrors, err1)
	} else if year < 2020 || year > 2025 {
		parserErrors = append(parserErrors, errors.New("Invalid Year - please specify a year between 2020 and 2025 (inclusive)"))
	}

	day, err2 := strconv.Atoi(args[1])
	if err2 != nil {
		parserErrors = append(parserErrors, err2)
	} else if day < 1 || day > 25 {
		parserErrors = append(parserErrors, errors.New("Invalid Day - please specify a day between 1 and 25 (inclusive)"))
	}

	part, err3 := strconv.Atoi(args[2])
	if err3 != nil {
		parserErrors = append(parserErrors, err3)
	}
	if part != 1 && part != 2 {
		parserErrors = append(parserErrors, errors.New("Invalid Part - Must be either 1 or 2"))
	}

	if len(parserErrors) > 0 {
		return nil, errors.Join(parserErrors...)
	}

	return []int{year, day, part}, nil
}
