---
title: "REACTION_RAW"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-96.htm"
source_file: "phreeqc3-96.htm"
retrieved: 2026-09-22
category: keyword
---
# REACTION_RAW

## REACTION_RAW

This keyword data block is written by the [DUMP](phreeqc3-11.htm#50593793_49635) operation. It is intended to be used to reinitialize simulations at the point that the [DUMP](phreeqc3-11.htm#50593793_49635) command was executed or to transfer reactions defined by [REACTION](phreeqc3-40.htm#50593793_75635) data blocks between IPhreeqc modules.

###### Notes

The REACTION_RAW data block contains a complete listing of the internal data structures that define a stoichiometric reaction ([REACTION](phreeqc3-40.htm#50593793_75635) data block definition). REACTION_RAW data blocks are written by [DUMP](phreeqc3-11.htm#50593793_49635) and read by PHREEQC without user modification. The formats should be considered dynamic because future modifications to PHREEQC could result in additional data that are included in the REACTION_RAW data block.

###### Related keywords

[REACTION](phreeqc3-40.htm#50593793_75635) and [REACTION_MODIFY](phreeqc3-95.htm#50593805_31337).
