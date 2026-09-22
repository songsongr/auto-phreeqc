---
title: "MIX_GAS_PHASE"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-30.htm"
source_file: "phreeqc3-30.htm"
retrieved: 2026-09-22
category: keyword
---
# MIX_GAS_PHASE

## MIX_GAS_PHASE

This keyword data block is used to define a new gas phase by mixing sets of previously defined gas phases. This keyword simply sums moles of gases to define a new gas phase that can be used in subsequent simulations; it does not cause any speciation or reaction calculation.

###### Example data block

```phreeqc
Line 0:  MIX_GAS_PHASE 2 Mixing GAS_PHASE 5, 6, and 7.
Line 1a:      5     1.1
Line 1b:      6     0.5
Line 1c:      7     0.3
```

###### Explanation

Line 0: MIX_GAS_PHASE [number] [description]

MIX_GAS_PHASE is the keyword for the data block.

number--A positive number designates the new gas phase user number. Default is 1.

description--Optional comment that describes the mixture.

Line 1: gas phase number, mixing fraction

gas phase number--User number of a gas phase definition.

mixing fraction--Decimal number that is multiplied times the moles of each gas component in the specified gas phase definition; the mixture is the sum of each gas component times its mixing fraction. Mixing fractions may be greater than 1.0.

###### Notes

In mixing, each gas phase is multiplied by its mixing fraction and a new gas phase is calculated by summing over all of the fractional gas phase definitions. In the Example data block, if the moles of CO2(g) in gas phases 5, 6, and 7 were 0.1, 0.2, and 0.3, the moles of CO2(g) in the mixture would be 0.1x1.1+0.2x0.5+0.3x0.3 = 0.3. MIX_GAS_PHASE is followed only by COPY , DUMP , and DELETE in the sequence of operations of a simulation.

###### Related keywords

MIX , MIX_EQUILIBRIUM_PHASES , MIX_EXCHANGE , MIX_KINETICS , MIX_SOLID_SOLUTION , MIX_SOLUTION , and MIX_SURFACE .
