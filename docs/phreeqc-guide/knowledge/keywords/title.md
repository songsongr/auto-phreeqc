---
title: "TITLE"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-55.htm"
source_file: "phreeqc3-55.htm"
retrieved: 2026-09-22
category: keyword
---
# TITLE

## TITLE

This keyword data block is used to include a comment for a simulation in the output file. The comment will appear in the echo of the input data, and it will appear at the beginning of the simulation calculations.

###### Example data block

```phreeqc
Line 0:  TITLE The title may begin on this line,
Line 1a: or on this line.
Line 1b: It continues until a keyword is found at the beginning of a line
Line 1c: or until the end of the file.
```

###### Explanation

Line 0: TITLE comment

TITLE is the keyword for the data block. Optionally, COMMENT .

comment --The first line of a title (or comment) may begin on the same line as the keyword.

Line 1: comment

comment --The title (or comment) may continue on as many lines as necessary. Lines are read and saved as part of the title until a keyword begins a line or until the end of the input file.

###### Notes

Be careful not to begin a line of the title with a keyword because that signals the end of the TITLE data block. The TITLE data block is intended to document a simulation in the output file. If more than one title keyword is entered for a simulation, each will appear in the output file as part of the echo of the input data, but only the last will also appear at the beginning of the simulation calculations. The characters “#” and “;” have special meanings in PHREEQC input files; in the TITLE data block, the “#” will cause the remainder of the line to be excluded from comment and “;” will have the same effect as a line break at that character position. Lines that are entirely white space (tabs and spaces) and comments (characters following “#”) are eliminated.

###### Example problems

The keyword TITLE is used in all examples, [1](phreeqc3-63.htm#50593807_24208) through [22](phreeqc3-84.htm#50593807_97000).
