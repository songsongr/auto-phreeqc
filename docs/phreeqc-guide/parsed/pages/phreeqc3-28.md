---
title: "MIX_EQUILIBRIUM_PHASES"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-28.htm"
source_file: "phreeqc3-28.htm"
retrieved: 2026-09-22
category: keyword
---
# MIX_EQUILIBRIUM_PHASES

## MIX_EQUILIBRIUM_PHASES

This keyword data block is used to define a new set of equilibrium phases by mixing sets of previously defined equilibrium phases. This keyword simply sums moles of phases to define a new set of equilibrium phases that can be used in subsequent simulations; it does not cause any speciation or reaction calculation.

###### Example data block

```phreeqc
Line 0:  MIX_EQUILIBRIUM_PHASES 2 Mixing EQUILIBRIUM_PHASES 5, 6, and 7.
Line 1a:      5     1.1
Line 1b:      6     0.5
Line 1c:      7     0.3
```

###### Explanation

Line 0: MIX_EQUILIBRIUM_PHASES [number] [description]

MIX_EQUILIBRIUM_PHASES is the keyword for the data block.

number--A positive number designates the new equilibrium phases user number. Default is 1.

description--Optional comment that describes the mixture.

Line 1: equilibrium phases number, mixing fraction

equilibrium phases number--User number of an equilibrium phases definition.

mixing fraction--Decimal number that is multiplied times the moles of each phase in the specified equilibrium phases definition; the mixture is the sum of each equilibrium phase times its mixing fraction. Mixing fractions may be greater than 1.0.

###### Notes

In mixing, each phase is multiplied by its mixing fraction, and a new set of equilibrium phases is defined by summing over all of the fractional equilibrium phases definitions. In the Example data block, if the moles of calcite in equilibrium phases 5, 6, and 7 were 0.1, 0.2, and 0.3, the moles of calcite in the mixture would be 0.1x1.1+0.2x0.5+0.3x0.3 = 0.3. MIX_EQUILIBRIUM_PHASES is followed only by COPY , DUMP , and DELETE in the sequence of operations of a simulation.

###### Related keywords

MIX , MIX_EXCHANGE , MIX_GAS_PHASE , MIX_KINETICS , MIX_SOLID_SOLUTION , MIX_SOLUTION , and MIX_SURFACE .
