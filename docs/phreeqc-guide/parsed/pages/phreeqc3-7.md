---
title: "CALCULATE_VALUES"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-7.htm"
source_file: "phreeqc3-7.htm"
retrieved: 2026-09-22
category: keyword
---
# CALCULATE_VALUES

## CALCULATE_VALUES

This keyword data block allows the definition of Basic functions that can be used in other PHREEQC Basic programs or to display isotopic compositions as defined in the [ISOTOPE_ALPHAS](phreeqc3-22.htm#50593793_17508) and [ISOTOPE_RATIOS](phreeqc3-23.htm#50593793_17097) data blocks. Isotope ratios are the ratio of moles of a minor isotope to moles of a major isotope in an aqueous, gas, or mineral species. Isotope alphas are the ratio of two isotope ratios, which is the fractionation factor between two species. The data block is used primarily to display results from the isotopic simulations, but also can be used to write Basic functions to simplify Basic programming for [RATES](phreeqc3-39.htm#50593793_97907), [USER_GRAPH](phreeqc3-58.htm#50593793_26121), [USER_PRINT](phreeqc3-59.htm#50593793_55085), and [USER_PUNCH](phreeqc3-60.htm#50593793_56415).

###### Example data block

```phreeqc
Line 0: CALCULATE_VALUES
Line 1: R(D)
Line 2: -start
Line 3:   10  ratio = -9999.999
Line 3a:  20  if (TOT("D") <= 0) THEN GOTO 100
Line 3b:  30  total_D = TOT("D")
Line 3c:  40  total_H = TOT("H")
Line 3d:  50  ratio = total_D/total_H
Line 3e:  100 SAVE ratio
Line 4: -end
```

###### Explanation

Line 0: CALCULATE_VALUES

CALCULATE_VALUES is the keyword for the data block. No other data are input on the keyword line.

Line 1: name of Basic function

name of Basic function --Alphanumeric character string that defines the name of the Basic function; no spaces are allowed. The function defined in this example would be evaluated in other PHREEQC Basic programs by using CALC_VALUE(“R(D)”).

Line 2: -start

-start --Identifier marks the beginning of a Basic program. Optional.

Line 3: numbered Basic statement

numbered Basic statement --A valid Basic language statement that must be numbered. The statements are evaluated in numerical order. The statement “SAVE expression ” must be included in the list of statements, where the value of expression is the result that is returned from the Basic function. Statements and functions that are available through the Basic interpreter are listed in [The Basic Interpreter](phreeqc3-61.htm#50593797_44206) (tables [7](phreeqc3-61.htm#50593797_51264) and [8](phreeqc3-61.htm#50593797_27680)).

Line 4: -end

-end --Identifier marks the end of a Basic function. Note the hyphen is required to avoid a conflict with the keyword END .

###### Notes

The CALCULATE_VALUES data block is used to write Basic functions. These functions have no arguments and return a single numeric result defined in the line with the SAVE command. The functions may be called from other PHREEQC Basic programs by using the function CALC_VALUE(“ function_name ”), where function_name is the name of a function defined in a CALCULATE_VALUES data block.

The CALCULATE_VALUES data block is used primarily to implement isotopic calculations as described in Thorstenson and Parkhurst (2002, 2004), but could be used for other purposes as well. The database iso.dat contains many instances of Basic functions in CALCULATE_VALUES data blocks. Basic functions have been written to calculate isotope ratios (moles of minor isotope divided by moles of major isotope) for a large number of isotopes and aqueous, gas, and mineral species. The example given at the beginning of this section calculates the ratio of deuterium to hydrogen in an aqueous solution. The functions also are used to calculate ratios of isotope ratios (alphas), which are equal to the fractionation factors among species. These functions are then specified in the [ISOTOPE_ALPHAS](phreeqc3-22.htm#50593793_17508) and [ISOTOPE_RATIOS](phreeqc3-23.htm#50593793_17097) data blocks to enable listing isotopic ratios and alphas in the output file. The functions also can be used in Basic programs in [RATES](phreeqc3-39.htm#50593793_97907), [USER_GRAPH](phreeqc3-58.htm#50593793_26121), [USER_PRINT](phreeqc3-59.htm#50593793_55085), and [USER_PUNCH](phreeqc3-60.htm#50593793_56415) data blocks.

###### Example problems

The keyword CALCULATE_VALUES is used in the database iso.dat.

###### Related keywords

[ISOTOPE_ALPHAS](phreeqc3-22.htm#50593793_17508), [ISOTOPE_RATIOS](phreeqc3-23.htm#50593793_17097), [RATES](phreeqc3-39.htm#50593793_97907), [USER_GRAPH](phreeqc3-58.htm#50593793_26121), [USER_PRINT](phreeqc3-59.htm#50593793_55085), and [USER_PUNCH](phreeqc3-60.htm#50593793_56415).
