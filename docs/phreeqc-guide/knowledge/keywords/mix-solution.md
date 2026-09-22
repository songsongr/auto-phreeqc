---
title: "MIX_SOLUTION"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-33.htm"
source_file: "phreeqc3-33.htm"
retrieved: 2026-09-22
category: keyword
---
# MIX_SOLUTION

## MIX_SOLUTION

This keyword data block is used to define a new solution by mixing previously defined solutions. This keyword simply sums moles of elements to define a new solution that can be used in subsequent simulations; unlike MIX , it does not cause any speciation or reaction calculation.

###### Example data block

```phreeqc
Line 0:  MIX_SOLUTION 2 Mixing SOLUTION 5, 6, and 7.
Line 1a:      5     1.1
Line 1b:      6     0.5
Line 1c:      7     0.3
```

###### Explanation

Line 0: MIX_SOLUTION [number] [description]

MIX_SOLUTION is the keyword for the data block.

number--A positive number designates the new solution user number. Default is 1.

description--Optional comment that describes the mixture.

Line 1: solution number, mixing fraction

solution number--User number of a solution definition.

mixing fraction--Decimal number that is multiplied times the moles of each element in the specified solution definition; the mixture is the sum of each element times its mixing fraction. Mixing fractions may be greater than 1.0.

###### Notes

In mixing, the amount of each element is multiplied by its mixing fraction and a new solution is calculated by summing over all of the fractional solution definitions. In the Example data block, if the moles of Ca in equilibrium phases 5, 6, and 7 were 0.1, 0.2, and 0.3, the moles of Ca in the mixture would be 0.1x1.1+0.2x0.5+0.3x0.3 = 0.3. MIX_SOLUTION is followed only by COPY , DUMP , and DELETE in the sequence of operations of a simulation.

###### Related keywords

MIX , MIX_EQUILIBRIUM_PHASES , MIX_EXCHANGE , MIX_GAS_PHASE , MIX_KINETICS , MIX_SOLID_SOLUTION , and MIX_SURFACE .
