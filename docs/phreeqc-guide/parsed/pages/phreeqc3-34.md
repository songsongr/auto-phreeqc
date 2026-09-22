---
title: "MIX_SURFACE"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-34.htm"
source_file: "phreeqc3-34.htm"
retrieved: 2026-09-22
category: keyword
---
# MIX_SURFACE

## MIX_SURFACE

This keyword data block is used to define a new set of surfaces by mixing sets of previously defined surfaces. This keyword simply sums moles of surface sites and elements to define a new set of surfaces that can be used in subsequent simulations; it does not cause any speciation or reaction calculation.

###### Example data block

```phreeqc
Line 0:  MIX_SURFACE 2 Mixing SURFACE 5, 6, and 7.
Line 1a:      5     1.1
Line 1b:      6     0.5
Line 1c:      7     0.3
```

###### Explanation

Line 0: MIX_SURFACE [number] [description]

MIX_SURFACE is the keyword for the data block.

number--A positive number designates the new surface user number. Default is 1.

description--Optional comment that describes the mixture.

Line 1: surface number, mixing fraction

surface number--User number of a surface definition.

mixing fraction--Decimal number that is multiplied times the moles of each surface site and element in the specified surface definition; the mixture is the sum of moles of each surface site and element times its mixing fraction. Mixing fractions may be greater than 1.0.

###### Notes

In mixing, each surface site and element is multiplied by its mixing fraction, and a new set of surface is calculated by summing over all of the fractional surfaces definitions. In the Example data block, if the moles of Surf in surfaces 5, 6, and 7 were 0.1, 0.2, and 0.3, the moles of Surf in the mixture would be 0.1x1.1+0.2x0.5+0.3x0.3 = 0.3. MIX_SURFACE is followed only by COPY , DUMP , and DELETE in the sequence of operations of a simulation.

###### Related keywords

MIX , MIX_EQUILIBRIUM_PHASES , MIX_EXCHANGE , MIX_GAS_PHASE , MIX_KINETICS , MIX_SOLID_SOLUTION , and MIX_SOLUTION .
