---
title: "GAS_PHASE_RAW"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-92.htm"
source_file: "phreeqc3-92.htm"
retrieved: 2026-09-22
category: keyword
---
# GAS_PHASE_RAW

## GAS_PHASE_RAW

This keyword data block is written by the [DUMP](phreeqc3-11.htm#50593793_49635) operation. It is intended to be used to reinitialize simulations at the point that the [DUMP](phreeqc3-11.htm#50593793_49635) command was executed, or to transfer gas-phase compositions between IPhreeqc modules.

###### Notes

The GAS_PHASE_RAW data block contains a complete listing of the internal data structures that define a gas phase. GAS_PHASE_RAW data blocks are written by [DUMP](phreeqc3-11.htm#50593793_49635) and read by PHREEQC without user modification. The formats should be considered dynamic because future modifications to PHREEQC could result in additional data that are included in the GAS_PHASE_RAW data block.

###### Related keywords

[GAS_PHASE](phreeqc3-17.htm#50593793_83409) and [GAS_PHASE_MODIFY](phreeqc3-91.htm#50593805_44837).
