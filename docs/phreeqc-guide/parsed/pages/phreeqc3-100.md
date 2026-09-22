---
title: "SOLID_SOLUTIONS_RAW"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-100.htm"
source_file: "phreeqc3-100.htm"
retrieved: 2026-09-22
category: keyword
---
# SOLID_SOLUTIONS_RAW

## SOLID_SOLUTIONS_RAW

This keyword data block is written by the [DUMP](phreeqc3-11.htm#50593793_49635) operation. It is intended to be used to reinitialize simulations at the point that the [DUMP](phreeqc3-11.htm#50593793_49635) command was executed or to transfer solid-solution compositions between IPhreeqc modules.

###### Notes

The SOLID_SOLUTIONS_RAW data block contains a complete listing of the internal data structures that define a solid-solution assemblage. SOLID_SOLUTIONS_RAW data blocks are written by [DUMP](phreeqc3-11.htm#50593793_49635) and read by PHREEQC without user modification. The formats should be considered dynamic because future modifications to PHREEQC could result in additional data that are included in the SOLID_SOLUTIONS_RAW data block.

###### Related keywords

[SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444) and [SOLID_SOLUTIONS_MODIFY](phreeqc3-99.htm#50593805_30253).
