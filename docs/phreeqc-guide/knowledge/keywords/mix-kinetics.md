---
title: "MIX_KINETICS"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-31.htm"
source_file: "phreeqc3-31.htm"
retrieved: 2026-09-22
category: keyword
---
# MIX_KINETICS

## MIX_KINETICS

This keyword data block is used to define a new set of kinetic reactions by mixing sets of previously defined kinetic reactions. This keyword simply sums moles of kinetic reactants to define a new set of kinetic reactants that can be used in subsequent simulations; it does not cause any speciation or reaction calculation.

###### Example data block

```phreeqc
Line 0:  MIX_KINETICS 2 Mixing KINETICS 5, 6, and 7.
Line 1a:      5     1.1
Line 1b:      6     0.5
Line 1c:      7     0.3
```

###### Explanation

Line 0: MIX_KINETICS [number] [description]

MIX_KINETICS is the keyword for the data block.

number--A positive number designates the new kinetics user number. Default is 1.

description--Optional comment that describes the mixture.

Line 1: kinetics number, mixing fraction

kinetics number--User number of a kinetics definition.

mixing fraction--Decimal number that is multiplied times the moles of each kinetic reaction in the specified kinetics definition; the mixture is the sum of each kinetic reaction times its mixing fraction. Mixing fractions may be greater than 1.0.

###### Notes

In mixing, the moles of each kinetic reaction is multiplied by its mixing fraction, and a new set of kinetic reactions is calculated by summing over all of the fractional kinetics definitions. In the Example data block, if the moles of calcite in kinetic definitions 5, 6, and 7 were 0.1, 0.2, and 0.3, the moles of calcite in the mixture would be 0.1x1.1+0.2x0.5+0.3x0.3 = 0.3. MIX_KINETICS is followed only by COPY , DUMP , and DELETE in the sequence of operations of a simulation.

###### Related keywords

MIX , MIX_EQUILIBRIUM_PHASES , MIX_EXCHANGE , MIX_GAS_PHASE , MIX_SOLID_SOLUTION , MIX_SOLUTION , and MIX_SURFACE .
