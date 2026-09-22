---
title: "COPY"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-8.htm"
source_file: "phreeqc3-8.htm"
retrieved: 2026-09-22
category: keyword
---
# COPY

## COPY

This keyword data block is used to make copies of any of the numbered reactants, which include equilibrium-phase assemblages, exchange assemblages, gas phases, kinetic reactions, mix definitions, reactions, reaction-pressure definitions, reaction-temperature definitions, solid-solution assemblages, solutions, or surface assemblages. These reactants are usually defined by the [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207), [EXCHANGE](phreeqc3-14.htm#50593793_49135), [GAS_PHASE](phreeqc3-17.htm#50593793_83409), [KINETICS](phreeqc3-24.htm#50593793_55637), [MIX](phreeqc3-27.htm#50593793_23725), [REACTION](phreeqc3-40.htm#50593793_75635), [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966), [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016), [SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444), [SOLUTION](phreeqc3-48.htm#50593793_89789), and [SURFACE](phreeqc3-52.htm#50593793_56392) data blocks, but may be defined or modified with the [SAVE](phreeqc3-44.htm#50593793_81857), _RAW , or _MODIFY (see [See Appendix A. Keyword Data Blocks for Programmers](phreeqc3-86.htm#50593805_35187)) data blocks.

###### Example data block

```phreeqc
Line 0:  COPY equilibrium_phases 2 3-5
Line 0a: COPY exchange 1 11
Line 0b: COPY gas_phase 1 11
Line 0c: COPY kinetics 2 3-5
Line 0d: COPY mix 1 11
Line 0e: COPY reaction 1 11
Line 0f: COPY reaction_pressure 25 15
Line 0g: COPY reaction_temperature 2 3-5
Line 0h: COPY solid_solution 1 11
Line 0i: COPY solution 1 11
Line 0j: COPY surface 1 11
Line 0k: COPY cell 1 21
```

###### Explanation

Line 0: COPY reactant source_number destination_number_range

COPY is the keyword for the data block.

reactant --The word “ cell ”, or one of the 10 reactants that can be identified by an integer-- equilibrium_phases , exchange , gas_phase , kinetics , mix , reaction , reaction_pressure , reaction_temperature , solid_solution , solution , or surface.

source_number --An integer designating the reactant to be copied. If reactant is cell , all reactants identified by source_number will be copied.

destination_number_range --A single number or a range of numbers designated by an integer followed by a hyphen, followed by an integer, with no intervening spaces. A copy of the source reactant will be made for each of the numbers in the range. If reactant is cell , all reactants identified by source_number will be copied for each of the numbers in the range.

###### Notes

The COPY operations are done after all reaction, advection, and transport calculations for a simulation, but before the [DUMP](phreeqc3-11.htm#50593793_49635) and [DELETE](phreeqc3-10.htm#50593793_33574) operations. If the reactant numbered source_number does not exist, the copy request is ignored. The source_number reactant will be copied so that after the copy operation, reactants will exist with each of the numbers designated by destination_number_range . If cell is designated for reactant , then for each reactant numbered source_number , a new copy will be generated for each number in the range given by destination_number_range . Unlike [DELETE](phreeqc3-10.htm#50593793_33574) and [DUMP](phreeqc3-11.htm#50593793_49635), only a single number range is allowed for COPY . If a reactant with a specified number exists before the copy operation, that reactant will be overwritten.

###### Example problems

The keyword COPY is used in example problems [11](phreeqc3-73.htm#50593807_46434), [12](phreeqc3-74.htm#50593807_12946), and [15](phreeqc3-77.htm#50593807_40270).

###### Related keywords

[DUMP](phreeqc3-11.htm#50593793_49635), [DELETE](phreeqc3-10.htm#50593793_33574), [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207), [EXCHANGE](phreeqc3-14.htm#50593793_49135), [GAS_PHASE](phreeqc3-17.htm#50593793_83409), [KINETICS](phreeqc3-24.htm#50593793_55637), [MIX](phreeqc3-27.htm#50593793_23725), [REACTION](phreeqc3-40.htm#50593793_75635), [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966), [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016), [SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444), [SOLUTION](phreeqc3-48.htm#50593793_89789), and [SURFACE](phreeqc3-52.htm#50593793_56392).
