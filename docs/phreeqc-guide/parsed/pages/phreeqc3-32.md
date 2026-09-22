---
title: "MIX_SOLID_SOLUTION"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-32.htm"
source_file: "phreeqc3-32.htm"
retrieved: 2026-09-22
category: keyword
---
# MIX_SOLID_SOLUTION

## MIX_SOLID_SOLUTION

This keyword data block is used to define a new set of solid solutions by mixing sets of previously defined solid solutions. This keyword simply sums moles of solid solution phases to define a new set of solid solutions that can be used in subsequent simulations; it does not cause any speciation or reaction calculation.

###### Example data block

```phreeqc
Line 0:  MIX_SOLID_SOLUTION 2 Mixing SOLID_SOLUTION 5, 6, and 7.
Line 1a:      5     1.1
Line 1b:      6     0.5
Line 1c:      7     0.3
```

###### Explanation

Line 0: MIX_SOLID_SOLUTION [number] [description]

MIX_SOLID_SOLUTION is the keyword for the data block.

number--A positive number designates the new solid solution user number. Default is 1.

description--Optional comment that describes the mixture.

Line 1: solid solution number, mixing fraction

solid solution number--User number of a solid solution definition.

mixing fraction--Decimal number that is multiplied times the moles of each phase in the specified solid solutions definition; the mixture is the sum of each phase times its mixing fraction. Mixing fractions may be greater than 1.0.

###### Notes

In mixing, each phase in each solid solution is multiplied by its mixing fraction, and a new set of solid solutions is calculated by summing over all of the fractional solid solution definitions. In the Example data block, if the moles of calcite in solid solutions 5, 6, and 7 were 0.1, 0.2, and 0.3, the moles of calcite in the mixture would be 0.1x1.1+0.2x0.5+0.3x0.3 = 0.3. MIX_SOLID_SOLUTION is followed only by COPY , DUMP , and DELETE in the sequence of operations of a simulation.

###### Related keywords

MIX , MIX_EQUILIBRIUM_PHASES , MIX_EXCHANGE , MIX_GAS_PHASE , MIX_KINETICS , MIX_SOLUTION , and MIX_SURFACE .
