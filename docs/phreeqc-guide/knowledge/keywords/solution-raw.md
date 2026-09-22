---
title: "SOLUTION_RAW"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-102.htm"
source_file: "phreeqc3-102.htm"
retrieved: 2026-09-22
category: keyword
---
# SOLUTION_RAW

## SOLUTION_RAW

This keyword data block is written by the [DUMP](phreeqc3-11.htm#50593793_49635) operation. It is intended to be used to reinitialize simulations at the point that the [DUMP](phreeqc3-11.htm#50593793_49635) command was executed, or to transfer solution compositions between IPhreeqc modules.

###### Notes

The SOLUTION_RAW data block contains a complete listing of the internal data structures that define a solution. SOLUTION_RAW data blocks are written by [DUMP](phreeqc3-11.htm#50593793_49635) and read by PHREEQC without user modification. The formats should be considered dynamic because future modifications to PHREEQC could result in additional data that are included in the SOLUTION_RAW data block.

###### Related keywords

[SOLUTION](phreeqc3-48.htm#50593793_30253) and [SOLUTION_MODIFY](phreeqc3-101.htm#50593805_96148).
