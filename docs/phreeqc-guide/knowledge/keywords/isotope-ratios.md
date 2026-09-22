---
title: "ISOTOPE_RATIOS"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-23.htm"
source_file: "phreeqc3-23.htm"
retrieved: 2026-09-22
category: keyword
---
# ISOTOPE_RATIOS

## ISOTOPE_RATIOS

This keyword data block is used to enable printing of isotopic ratios in species or phases to the output file. A Basic function defined in [CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035) is used to calculate an isotope ratio, which is then printed in the output file under the heading “Isotope Ratios”. The ISOTOPE_RATIOS data block is used in the database file iso.dat and is unlikely to be used in any other context.

###### Example data block

```phreeqc
Line 0: ISOTOPE_RATIOS
Line 1:	R(D)_H2O(l)             D
Line 1a:	R(T)_H2O(l)             T
Line 1b:	R(D)_OH-                D
Line 1c:	R(T)_OH-                T
```

###### Explanation

Line 0: ISOTOPE_RATIOS

ISOTOPE_RATIOS is the keyword for the data block. No other data are input on the keyword line.

Line 1: calculate_values_function isotope

calculate_values_function --The name of a calculate values function ([CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035) data block) that evaluates an isotopic ratio based on the isotopic compositions of species or phases.

isotope --The name of the isotope used in calculating the isotope ratio.

###### Notes

This keyword data block is used to implement the treatment of isotopes as individual thermodynamic components (Thorstenson and Parkhurst, 2000, 2004). An isotopic ratio, R, is defined to be the ratio of the number of moles of the minor isotope to the number of moles of the predominant isotope in a species or phase. A fractionation factor is defined as the ratio of two R s. In the Example data block given in this section, isotopic ratios are calculated for deuterium (D) and tritium (T) in liquid water and in the hydroxide ion. The isotopic ratios based on solution and phase compositions are calculated by Basic functions defined in the [CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035) data block. For example, the [CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035) function that defines the deuterium to 1H ratio in hydroxide is as follows:

```phreeqc
R(D)_OH-
     -start
10 ratio = -9999.999
20 if (TOT("D") <= 0) THEN GOTO 100
30 total_D = sum_species("*{O,[18O]}D*","D")
40 total_H = sum_species("*{O,[18O]}H*","H")
50 if (total_H <= 0) THEN GOTO 100
60 ratio = total_D/total_H
100 save ratio
     -end
```

Results of evaluating the Basic functions specified in the ISOTOPE_RATIOS data block are printed in the output file under the heading “Isotope Ratios”. The ISOTOPE_RATIOS data block only defines quantities to print and by itself does not affect the equilibrium distribution of species in a simulation.

The use of [CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035) functions to evaluate isotope ratios may be expensive in terms of computer time. If -isotope_ratios is true ([PRINT](phreeqc3-38.htm#50593793_92102) data block), isotope ratios are evaluated for each isotope in the reaction system. The Basic function SUM_SPECIES, which is used in many of the isotope ratio calculations, is especially time consuming. Minimizing the number of isotope ratios that are defined in the database and input file, minimizing the use of the SUM_SPECIES function in the [CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035) programs, and setting -isotope_ratios false in a [PRINT](phreeqc3-38.htm#50593793_92102) data block will decrease execution times for isotopic calculations.

###### Example problems

The keyword ISOTOPE_RATIOS is used in the iso.dat database.

###### Related keywords

[CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035), [ISOTOPE_ALPHAS](phreeqc3-22.htm#50593793_17508), and [MIX_EQUILIBRIUM_PHASES](phreeqc3-28.htm#50593793_52088).
