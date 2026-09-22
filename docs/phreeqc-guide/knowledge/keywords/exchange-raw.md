---
title: "EXCHANGE_RAW"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-90.htm"
source_file: "phreeqc3-90.htm"
retrieved: 2026-09-22
category: keyword
---
# EXCHANGE_RAW

## EXCHANGE_RAW

This keyword data block is written by the [DUMP](phreeqc3-11.htm#50593793_49635) operation. It is intended to be used to reinitialize simulations at the point that the [DUMP](phreeqc3-11.htm#50593793_49635) command was executed, or to transfer exchange-assemblage compositions between IPhreeqc modules.

###### Notes

The EXCHANGE_RAW data block contains a complete listing of the internal data structures that define an exchange assemblage. EXCHANGE_RAW data blocks are written by [DUMP](phreeqc3-11.htm#50593793_49635) and read by PHREEQC without user modification. The formats should be considered dynamic because future modifications to PHREEQC could result in additional data that are included in the EXCHANGE_RAW data block.

###### Related keywords

[EXCHANGE](phreeqc3-14.htm#50593793_49135) and [EXCHANGE_MODIFY](phreeqc3-89.htm#50593805_65476).
