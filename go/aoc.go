package main

import (
	"fmt"
	"log"

	// "net/http"
	"os"

	"aocgo/parser"
)

func main() {
	values, err := parser.ProcessArgs(os.Args[1:])

	if err != nil {
		log.Fatal(err)
	}

	fmt.Print(values)
}
