---
title: "REACTION_PRESSURE_RAW"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-97.htm"
source_file: "phreeqc3-97.htm"
retrieved: 2026-09-22
category: keyword
---
# REACTION_PRESSURE_RAW

## REACTION_PRESSURE_RAW

This keyword data block is written by the [DUMP](phreeqc3-11.htm#50593793_49635) operation. It is intended to be used to reinitialize simulations at the point that the [DUMP](phreeqc3-11.htm#50593793_49635) command was executed, or to transfer reaction-pressure specifications defined by [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966) data blocks between IPhreeqc modules.

###### Notes

The REACTION_PRESSURE_RAW data block contains a complete listing of the internal data structure that defines reaction temperatures (as defined in [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966) data blocks). REACTION_PRESSURE_RAW data blocks are written by [DUMP](phreeqc3-11.htm#50593793_49635) and can be read directly by PHREEQC. The format of the [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966) data block is sufficiently simple, so that a REACTION_PRESSURE_RAW data block is not needed; simply use [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966) to define new reaction pressures.

###### Related keywords

[REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966).
