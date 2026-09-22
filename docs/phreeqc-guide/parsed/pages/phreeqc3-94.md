---
title: "KINETICS_RAW"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-94.htm"
source_file: "phreeqc3-94.htm"
retrieved: 2026-09-22
category: keyword
---
# KINETICS_RAW

## KINETICS_RAW

This keyword data block is written by the [DUMP](phreeqc3-11.htm#50593793_49635) operation. It is intended to be used to reinitialize simulations at the point that the [DUMP](phreeqc3-11.htm#50593793_49635) command was executed or to transfer the definition of an assemblage of kinetic reactants between IPhreeqc modules.

###### Notes

The KINETICS_RAW data block contains a complete listing of the internal data structures that define an assemblage of kinetic reactants. KINETICS_RAW data blocks are written by [DUMP](phreeqc3-11.htm#50593793_49635) and read by PHREEQC without user modification. The formats should be considered dynamic because future modifications to PHREEQC could result in additional data that are included in the KINETICS_RAW data block.

###### Related keywords

[KINETICS](phreeqc3-24.htm#50593793_55637) and [KINETICS_MODIFY](phreeqc3-93.htm#50593805_79000).
