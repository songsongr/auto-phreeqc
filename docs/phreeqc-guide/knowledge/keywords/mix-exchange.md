---
title: "MIX_EXCHANGE"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-29.htm"
source_file: "phreeqc3-29.htm"
retrieved: 2026-09-22
category: keyword
---
# MIX_EXCHANGE

## MIX_EXCHANGE

This keyword data block is used to define a new set of exchangers by mixing sets of previously defined exchangers. This keyword sums moles of exchange sites and elements to define a new set of exchangers that can be used in subsequent simulations; it does not cause any speciation or reaction calculation.

###### Example data block

```phreeqc
Line 0:  MIX_EXCHANGE 2 Mixing EXCHANGE 5, 6, and 7.
Line 1a:      5     1.1
Line 1b:      6     0.5
Line 1c:      7     0.3
```

###### Explanation

Line 0: MIX_EXCHANGE [number] [description]

MIX_EXCHANGE is the keyword for the data block.

number--A positive number designates the new exchange user number. Default is 1.

description--Optional comment that describes the mixture.

Line 1: exchange number, mixing fraction

exchange number--User number of an exchange definition.

mixing fraction--Decimal number that is multiplied times the moles of each exchange site and element in the specified exchange definition; the mixture is the sum of each exchange site and element times its mixing fraction. Mixing fractions may be greater than 1.0.

###### Notes

In mixing, moles of each exchange site and element are multiplied by the mixing fraction, and a new set of exchangers is calculated by summing over all of the fractional exchange definitions. In the Example data block, if the moles of X in exchanger 5, 6, and 7 were 0.1, 0.2, and 0.3, the moles of X in the mixture would be 0.1x1.1+0.2x0.5+0.3x0.3 = 0.3. MIX_EXCHANGE is followed only by COPY , DUMP , and DELETE in the sequence of operations of a simulation.

###### Related keywords

MIX , MIX_EQUILIBRIUM_PHASES , MIX_GAS_PHASE , MIX_KINETICS , MIX_SOLID_SOLUTION , MIX_SOLUTION , and MIX_SURFACE .
