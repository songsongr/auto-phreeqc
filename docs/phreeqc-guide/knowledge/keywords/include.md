---
title: "INCLUDE$"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-18.htm"
source_file: "phreeqc3-18.htm"
retrieved: 2026-09-22
category: keyword
---
# INCLUDE$

## INCLUDE$

This keyword is used to insert the contents of another file into the input or database file. The inserted file may extend the data block of the preceding keyword and (or) add additional keyword data blocks. Files that are inserted may contain further INCLUDE$ statements. The files are included dynamically, which means that an input file can write a file with [DUMP](phreeqc3-11.htm#50593793_49635) or [USER_PUNCH](phreeqc3-60.htm#50593793_56415) and subsequently include that file into the input stream.

###### Example

Input file:

```phreeqc
	SOLUTION
		pH	6
	INCLUDE$ A
	END
```

File A:

```phreeqc
		Na	2
		S(6)	1
	INCLUDE$ B
```

File B:

```phreeqc
	EQUILIBRIUM_PHASES
		Calcite
```

Is equivalent to the following input:

```phreeqc
	SOLUTION
		pH	6
		Na	2
		S(6)	1
	EQUILIBRIUM_PHASES
		Calcite
	END
```

###### Notes

The INCLUDE$ keyword is used to include a file into the input file. The inclusion is done as PHREEQC is processing the input file and running simulations. Thus, it is possible to use a [DUMP](phreeqc3-11.htm#50593793_49635) or [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) data block to write a file that is included at a later point in the run. The keyword may be used in database files or input files.

###### Example problems

The keyword INCLUDE$ is used in example problems [8](phreeqc3-70.htm#50593807_58878), [20](phreeqc3-82.htm#50593807_33272), and [21](phreeqc3-83.htm#50593807_68313).

###### Related keywords

[DUMP](phreeqc3-11.htm#50593793_49635) and [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) .
