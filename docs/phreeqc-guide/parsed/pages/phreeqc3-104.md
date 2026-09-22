---
title: "SURFACE_RAW"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-104.htm"
source_file: "phreeqc3-104.htm"
retrieved: 2026-09-22
category: keyword
---
# SURFACE_RAW

## SURFACE_RAW

This keyword data block is written by the [DUMP](phreeqc3-11.htm#50593793_49635) operation. It is intended to be used to reinitialize simulations at the point that the [DUMP](phreeqc3-11.htm#50593793_49635) command was executed or to transfer surface-assemblage compositions between IPhreeqc modules.

###### Notes

The SURFACE_RAW data block contains a complete listing of the internal data structures that define a surface assemblage. SURFACE_RAW data blocks are written by [DUMP](phreeqc3-11.htm#50593793_49635) and read by PHREEQC without user modification. The formats should be considered dynamic because future modifications to PHREEQC could result in additional data that are included in the SOLUTION_RAW data block.

###### Related keywords

[SURFACE](phreeqc3-52.htm#50593793_56392) and [SURFACE_MODIFY](phreeqc3-103.htm#50593805_78804).
