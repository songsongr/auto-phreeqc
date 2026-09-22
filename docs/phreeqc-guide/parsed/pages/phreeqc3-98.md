---
title: "REACTION_TEMPERATURE_RAW"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-98.htm"
source_file: "phreeqc3-98.htm"
retrieved: 2026-09-22
category: keyword
---
# REACTION_TEMPERATURE_RAW

## REACTION_TEMPERATURE_RAW

This keyword data block is written by the [DUMP](phreeqc3-11.htm#50593793_49635) operation. It is intended to be used to reinitialize simulations at the point that the [DUMP](phreeqc3-11.htm#50593793_49635) command was executed or to transfer reaction-temperature specifications defined by [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016) data blocks between IPhreeqc modules.

###### Notes

The REACTION_TEMPERATURE_RAW data block contains a complete listing of the internal data structure that defines reaction temperatures (as defined in [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016) data blocks). REACTION_TEMPERATURE_RAW data blocks are written by [DUMP](phreeqc3-11.htm#50593793_49635) and can be read directly by PHREEQC. The format of the [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016) data block is sufficiently simple, so that a REACTION_TEMPERATURE_MODIFY data block is not needed; simply use [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016) to define new reaction temperatures.

###### Related keywords

[REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016).
