---
title: "USER_PRINT"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-59.htm"
source_file: "phreeqc3-59.htm"
retrieved: 2026-09-22
category: keyword
---
# USER_PRINT

## USER_PRINT

This keyword data block is used to define a Basic program that prints user-defined quantities to the output file. Any Basic “PRINT” statement will write to the output file.

###### Example data block

```phreeqc
Line 0: USER_PRINT
Line 1:      -start
Basic:  10 REM convert to ppm
Basic:  20 PRINT "Sodium:    ", MOL("Na+")* 22.99 * 1000 
Basic:  30 PRINT "Magnesium: ", MOL("Mg+2")* 24.3 * 1000 
Basic:  40 pairs = MOL("NaCO3-") + MOL("MgCO3") 
Basic:  50 PRINT "Pairs (mol/kgw): ", pairs
Basic:  60 REM print reaction increment
Basic:  70 PRINT "Rxn incr:  ", RXN
Line 2:      -end
```

###### Explanation

Line 0: USER_PRINT

USER_PRINT is the keyword for the data block. No other data are input on the keyword line.

Line 1: -start

-start --Indicates the start of the Basic program. Optional.

Basic: numbered Basic statement

numbered Basic statement --A valid Basic language statement that must be numbered. The statements are evaluated in the order of the line numbers. Statements and functions that are available through the Basic interpreter are listed in [The Basic Interpreter](phreeqc3-61.htm#50593797_44206), tables [7](phreeqc3-61.htm#50593797_51264) and [8](phreeqc3-61.htm#50593797_27680).

Line 2: -end

-end --Indicates the end of the Basic program. Optional. Note the hyphen is required to avoid a conflict with the keyword END .

###### Notes

USER_PRINT allows the user to write Basic programs to make calculations and print selected results as the program is running. Results of PRINT Basic statements are written directly to the output file after each calculation. More information on the Basic interpreter is available in the section [The Basic Interpreter](phreeqc3-61.htm#50593797_44206). All of the functions defined in [The Basic Interpreter](phreeqc3-61.htm#50593797_44206), tables [7](phreeqc3-61.htm#50593797_51264) and [8](phreeqc3-61.htm#50593797_27680), are available in USER_PRINT Basic programs. Writing results of USER_PRINT can be enabled or suspended with the -user_print identifier in the [PRINT](phreeqc3-38.htm#50593793_92102) data block. The [USER_PUNCH](phreeqc3-60.htm#50593793_56415) data block is similar to USER_PRINT , except that PUNCH Basic statements are used to write results to the selected-output file.

###### Example problems

The keyword USER_PRINT is used in example problems [6](phreeqc3-68.htm#50593807_49505), [10](phreeqc3-72.htm#50593807_24858), [12](phreeqc3-74.htm#50593807_12946), and [20](phreeqc3-82.htm#50593807_33272).

###### Related keywords

[PRINT](phreeqc3-38.htm#50593793_92102), [RATES](phreeqc3-39.htm#50593793_97907), [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239), and [USER_PUNCH](phreeqc3-60.htm#50593793_56415).
