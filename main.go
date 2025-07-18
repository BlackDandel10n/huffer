package main

import (
	"fmt"
	"os"
)

type State uint8

const (
	HELP uint8 = 128
	nameString string = "huffer"
	
)


func showUsage() {
	fmt.Printf("%v [OPTION] [FILE]\n", nameString)
	fmt.Printf("Use %v --help to get more information\n", nameString)
}


func showHelp() {
	fmt.Printf("%v [OPTION] [FILE]\n", nameString)
	fmt.Println("A huffman encoder/decoder written in Go")
}


func main() {
	args := os.Args[1:]
	files := []string{}
	var state uint8 = 0
	
	// Parse arguments
	for _, arg := range(args) {
		if len(arg) > 0 && arg[0] == '-' {
			switch arg {
				case "-h":
					fallthrough
				case "--help":
					state |= HELP
				default:
					showUsage()
					return
			}
		} else {
			files = append(files, arg)
		}
	}
	
	// Show help
	if state & HELP == 128 {
		showHelp()
		return
	}
}
