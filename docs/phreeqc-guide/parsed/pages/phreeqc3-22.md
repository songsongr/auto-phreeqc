---
title: "ISOTOPE_ALPHAS"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-22.htm"
source_file: "phreeqc3-22.htm"
retrieved: 2026-09-22
category: keyword
---
# ISOTOPE_ALPHAS

## ISOTOPE_ALPHAS

This keyword data block is used to enable printing of isotopic fractionation factors, referred to as alphas, to the output file. A Basic function defined in [CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035) is used to calculate the fractionation factor from the current isotopic composition of species or phases and an analytical expression for a fractionation factor is evaluated by a definition in [MIX_EQUILIBRIUM_PHASES](phreeqc3-28.htm#50593793_52088). These two values and related data are printed in the output file under the heading “Isotope Alphas”. The ISOTOPE_ALPHAS data block is used in the database file iso.dat and is unlikely to be used in any other context.

###### Example data block

```phreeqc
Line 0: ISOTOPE_ALPHAS
Line 1:	Alpha_D_OH-/H2O(l)			Log_alpha_D_OH-/H2O(l)
Line 2:	Alpha_T_OH-/H2O(l)			Log_alpha_T_OH-/H2O(l)
```

###### Explanation

Line 0: ISOTOPE_ALPHAS

ISOTOPE_ALPHAS is the keyword for the data block. No other data are input on the keyword line.

Line 1: calculate_values_function named_expression

calculate_values_function --The name of a calculate values function ([CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035) data block) that evaluates a fractionation factor based on the isotopic compositions of species or phases.

named_expression --The name of a named expression ([MIX_EQUILIBRIUM_PHASES](phreeqc3-28.htm#50593793_52088) data block) that evaluates an analytical expression for a fractionation factor between species or phases.

###### Notes

This keyword data block is used to implement the treatment of isotopes as individual thermodynamic components (Thorstenson and Parkhurst, 2000, 2004). If R is defined to be the ratio of the number of moles of the minor isotope to the number of moles of the predominant isotope in a species or phase, then the fractionation factor, or alpha, is the ratio of R in one species or phase to R in another species or phase. In the Example data block given in this section, the fractionation factors are calculated for deuterium (D) and tritium (T) between hydroxide ion and liquid water. Analytical expressions for fractionation factors are defined in the database through the use of the [MIX_EQUILIBRIUM_PHASES](phreeqc3-28.htm#50593793_52088) data block and are incorporated into equilibrium constants for species and phases in [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_61994) and [PHASES](phreeqc3-36.htm#50593793_84418) data blocks. The fractionation factor based on solution and phase composition can be calculated by Basic functions that are defined in the [CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035) data block. At equilibrium, fractionation factors derived from the composition of the solution and other phases should equal the fractionation factor derived from the named expression, just as the ion-activity product of a phase should equal the equilibrium constant at equilibrium. This correspondence between composition-derived and analytical fractionation factors is printed in the output file under the heading “Isotope Alphas”. The ISOTOPE_ALPHAS data block only defines quantities to print and by itself does not affect the equilibrium distribution of species in a simulation.

The use of [CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035) functions to evaluate isotope alphas may be expensive in terms of computer time. If -isotope_alphas is true ([PRINT](phreeqc3-38.htm#50593793_92102) data block), all isotope alphas defined in the database or the input file are evaluated for each reaction calculation, even if the relevant isotopes are not in the reaction system. The Basic function SUM_SPECIES, which is used in many of the isotope alpha calculations, is especially time consuming. Minimizing the number of isotope alphas that are defined, minimizing the use of the SUM_SPECIES function in the [CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035) programs, and setting -isotope_alphas false in a [PRINT](phreeqc3-38.htm#50593793_92102) data block will decrease execution times for isotopic calculations.

###### Example problems

The keyword ISOTOPE_ALPHAS is used in the iso.dat database.

###### Related keywords

[CALCULATE_VALUES](phreeqc3-7.htm#50593793_35035), [ISOTOPE_RATIOS](phreeqc3-23.htm#50593793_17097), and [MIX_EQUILIBRIUM_PHASES](phreeqc3-28.htm#50593793_52088).
