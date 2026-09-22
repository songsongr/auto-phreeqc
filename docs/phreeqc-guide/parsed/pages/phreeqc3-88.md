---
title: "EQUILIBRIUM_PHASES_RAW"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-88.htm"
source_file: "phreeqc3-88.htm"
retrieved: 2026-09-22
category: keyword
---
# EQUILIBRIUM_PHASES_RAW

## EQUILIBRIUM_PHASES_RAW

This keyword data block is written by the [DUMP](phreeqc3-11.htm#50593793_49635) operation. It is intended to be used to reinitialize simulations at the point that the [DUMP](phreeqc3-11.htm#50593793_49635) command was executed or to transfer equilibrium-phase compositions between IPhreeqc modules.

###### Notes

The EQUILIBRIUM_PHASES_RAW data block contains a complete listing of the internal data structures that define an equilibrium-phase assemblage. EQUILIBRIUM_PHASES_RAW data blocks are written by [DUMP](phreeqc3-11.htm#50593793_49635) and read by PHREEQC without user modification. The formats should be considered dynamic because future modifications to PHREEQC could result in additional data that are included in the EQUILIBRIUM_PHASES_RAW data block.

###### Related keywords

[EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) and [EQUILIBRIUM_PHASES_MODIFY](phreeqc3-87.htm#50593805_84573).
