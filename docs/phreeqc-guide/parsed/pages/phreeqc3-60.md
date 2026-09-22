---
title: "USER_PUNCH"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-60.htm"
source_file: "phreeqc3-60.htm"
retrieved: 2026-09-22
category: keyword
---
# USER_PUNCH

## USER_PUNCH

This keyword data block is used to define Basic programs that print user-defined quantities to a selected-output file. Multiple SELECTED_OUTPUT definitions using different values of n are possible; each is used to write a different file. USER_PUNCH n writes to the file defined in SELECTED_OUTPUT n. Any Basic “PUNCH” statement will write to the selected-output file.

###### Example data block

```phreeqc
Line 0: USER_PUNCH
Line 1:      -headings Na+ Mg+2 Pairs Rxn_increment 
Line 2:      -start
Basic:  10 REM convert to ppm
Basic:  20 PUNCH MOL("Na+")* 22.99 * 1000 
Basic:  30 PUNCH MOL("Mg+2")* 24.3 * 1000 
Basic:  40 pairs = MOL("NaCO3-") + MOL("MgCO3") 
Basic:  50 PUNCH pairs
Basic:  60 REM punch reaction increment
Basic:  70 PUNCH RXN
Line 3:      -end
```

###### Explanation

Line 0: USER_PUNCH [number] [description]

USER_PUNCH is the keyword for the data block.

number--Positive number to designate this selected-output definition. Default is 1.

description--Optional comment that describes the selected-output data.

Line 1: -headings list of column headings

-headings --Headings will appear on the first line of the selected-output file. Optionally, heading , headings , or -h [ eadings ].

list of column headings --White-space-delimited (any combination of spaces and tabs) list of column headings.

Line 2: -start

-start --Indicates the start of the Basic program. Optional.

Basic: numbered Basic statement

numbered Basic statement --A valid Basic language statement that must be numbered. The statements are evaluated in the order of the line numbers. Statements and functions that are available through the Basic interpreter are listed in [The Basic Interpreter](phreeqc3-61.htm#50593797_44206), tables [7](phreeqc3-61.htm#50593797_51264) and [8](phreeqc3-61.htm#50593797_27680).

Line 3: -end

-end --Indicates the end of the Basic program. Optional. Note the hyphen is required to avoid a conflict with the keyword END .

###### Notes

USER_PUNCH allows the user to write a Basic program to make calculations and print selected results to the selected-output file as PHREEQC is running. Results of PUNCH Basic statements are written directly to the selected-output file after each calculation. The Basic program is useful for writing results in the desired units or in a format that can be plotted directly. All of the functions defined in [The Basic Interpreter](phreeqc3-61.htm#50593797_44206) (tables [7](phreeqc3-61.htm#50593797_51264) and [8](phreeqc3-61.htm#50593797_27680)) are available in USER_PUNCH Basic programs. USER_PUNCH has no effect unless a [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) data block has been defined. Writing results of [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) and USER_PUNCH can be enabled or suspended with the -selected_output identifier in the [PRINT](phreeqc3-38.htm#50593793_92102) data block. If the -selected_output identifier in the [PRINT](phreeqc3-38.htm#50593793_92102) data block is false , then all selected output, including USER_PUNCH , is disabled; if true , then all selected output, including USER_PUNCH , is enabled. The [USER_PRINT](phreeqc3-59.htm#50593793_55085) data block is similar to USER_PUNCH , except that PRINT Basic statements are used to write results to the output file.

Multiple SELECTED_OUTPUT data blocks may be defined by using different identifying numbers. Multiple USER_PUNCH data blocks may also be defined. SELECTED_OUTPUT data block n controls the writing of USER_PUNCH n. If SELECTED_OUTPUT n is not defined, USER_PUNCH n will not write any data. If both SELECTED_OUTPUT n and USER_PUNCH n are defined, then identifiers -selected_output in PRINT and -active and -user_punch in SELECTED_OUTPUT will determine the data that will be written to file. If -selected_output in PRINT is false, no data are written to any selected-output file. For SELECTED_OUTPUT n, if -active is false, no data are written; if -active is true the data defined by SELECTED_OUTPUT n are written and the value of -user_punch determines whether USER_PUNCH n data will be written.

###### Example problems

The keyword USER_PUNCH is used in example problems [6](phreeqc3-68.htm#50593807_49505), [8](phreeqc3-70.htm#50593807_58878), [9](phreeqc3-71.htm#50593807_39217), [10](phreeqc3-72.htm#50593807_24858), [11](phreeqc3-73.htm#50593807_46434), [12](phreeqc3-74.htm#50593807_12946), [13](phreeqc3-75.htm#50593807_22265), [14](phreeqc3-76.htm#50593807_89290), [15](phreeqc3-77.htm#50593807_40270), [20](phreeqc3-82.htm#50593807_33272), and [21](phreeqc3-83.htm#50593807_68313).

###### Related keywords

[PRINT](phreeqc3-38.htm#50593793_92102), [RATES](phreeqc3-39.htm#50593793_97907), [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239), [USER_GRAPH](phreeqc3-58.htm#50593793_26121), and [USER_PRINT](phreeqc3-59.htm#50593793_55085).
