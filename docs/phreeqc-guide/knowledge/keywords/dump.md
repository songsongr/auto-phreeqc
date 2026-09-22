---
title: "DUMP"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-11.htm"
source_file: "phreeqc3-11.htm"
retrieved: 2026-09-22
category: keyword
---
# DUMP

## DUMP

This keyword data block is used to write complete definitions of reactants to a specified file. The reactants are written in a “raw” format that saves the exact chemical state of each specified reactant. The raw data blocks are intended to be used intact to reinitialize simulations at the current state of the calculations or to transfer reactants from one IPhreeqc module (Charlton and Parkhurst, 2011) to another.

###### Example data block

```phreeqc
Line 0: DUMP
Line 1:	-file			myfile.dmp
Line 2:	-append 			true
Line 3:	-equilibrium_phases		
Line 4:	-exchange			2 4
Line 5:				3 5
Line 6:	-gas_phase			2-4 5
Line 7:	-kinetics			3-5 2
Line 8:	-mix			2 3
Line 8a:	-mix			4 5
Line 9:	-reaction      			2-3 4 5
Line 10:	-reaction_pressure			2 3 4 5
Line 11:	-reaction_temperature			5
Line 5a:				2 3 4
Line 12:	-solid_solution
Line 5b:				5 4 3 2
Line 13:	-solution 			2 3 4 5
Line 14:	-surface
Line 5c:				2-3 4-5
Line 5d:				5
Line 15:	-cells			2-5
Line 16:	-all
```

###### Explanation

Line 0: DUMP

DUMP is the keyword for the data block. No other data are input on the keyword line.

Line 1: -file file_name

-file --Identifier is used to specify the name of the file to which the dump data are written. Optionally, file or -f [ ile ].

file_name -- Name of file where dump data are written. File names must conform to operating system conventions. Default is dump.out .

Line 2: -append [( True or False )]

-append --Identifier is used to specify whether the dump data will overwrite existing data or will be appended to the end of the file, if the file exists. Default is false at startup; any data in the dump file are overwritten. Optionally, append or -a [ ppend ].

( True or False )--A value of true indicates that the dump data will be appended to the end of the dump file. A value of false indicates that any data in the dump file will be overwritten. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

Line 3: -equilibrium_phases list_of_ranges

-equilibrium_phases --Identifier indicates that equilibrium-phase assemblages will be dumped. Optionally, -e [ quilibrium_phases ]; note that the hyphen is necessary to distinguish the identifier from the keyword [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Equilibrium-phase assemblages identified by any of the numbers in the list will be dumped. If list_of_ranges is empty, all equilibrium-phase-assemblage definitions will be dumped.

Line 4: -exchange list_of_ranges

-exchange --Identifier indicates that exchange assemblages will be dumped. Optionally, -ex [ change ]; note that the hyphen is necessary to distinguish the identifier from the keyword [EXCHANGE](phreeqc3-14.htm#50593793_49135).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Exchange assemblages identified by any of the numbers in the list will be dumped. If list_of_ranges is empty, all exchange-assemblage definitions will be dumped.

Line 5: list_of_ranges

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Line 5 can be used to begin a list of ranges or to continue a list of ranges.

Line 6: -gas_phase list_of_ranges

-gas_phase --Identifier indicates that gas phases will be dumped. Optionally, -g [ as_phase ]; note that the hyphen is necessary to distinguish the identifier from the keyword [GAS_PHASE](phreeqc3-17.htm#50593793_83409).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Gas phases identified by any of the numbers in the list will be dumped. If list_of_ranges is empty, all gas-phase definitions will be dumped.

Line 7: -kinetics list_of_ranges

-kinetics --Identifier indicates that kinetic reactants will be dumped. Optionally, -k [ inetics ]; note that the hyphen is necessary to distinguish the identifier from the keyword [KINETICS](phreeqc3-24.htm#50593793_55637).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Kinetic reactants identified by any of the numbers in the list will be dumped. If list_of_ranges is empty, all kinetic-reaction definitions will be dumped.

Line 8: -mix list_of_ranges

-mix --Identifier indicates that mix definitions will be dumped. Optionally, -m [ ix ]; note that the hyphen is necessary to distinguish the identifier from the keyword [MIX](phreeqc3-27.htm#50593793_23725).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Mix definitions identified by any of the numbers in the list will be dumped. If list_of_ranges is empty, all mix definitions will be dumped.

Line 9: -reaction list_of_ranges

-reaction --Identifier indicates that reactions will be dumped. Optionally, -r [ eaction ]; note that the hyphen is necessary to distinguish the identifier from the keyword [REACTION](phreeqc3-40.htm#50593793_75635).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Reactions identified by any of the numbers in the list will be dumped. If list_of_ranges is empty, all reaction definitions will be dumped.

Line 10: -reaction_pressure list_of_ranges

-reaction_pressure --Identifier indicates that reaction-pressure definitions will be dumped. Optionally, -reaction_p [ ressure ], pressure , or -pr [ essure ]; note that the hyphen is necessary to distinguish the identifier from the keyword [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Reaction-pressure definitions identified by any of the numbers in the list will be dumped. If list_of_ranges is empty, all reaction-pressure definitions will be dumped.

Line 11: -reaction_temperature list_of_ranges

-reaction_temperature --Identifier indicates that reaction-temperature definitions will be dumped. Optionally, -reaction_ [ temperatures ], temperature , or -t [ emperature ]; note that the hyphen is necessary to distinguish the identifier from the keyword [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Reaction-temperature definitions identified by any of the numbers in the list will be dumped. If list_of_ranges is empty, all reaction-temperature definitions will be dumped.

Line 12: -solid_solution list_of_ranges

-solid_solution --Identifier indicates that solid-solution assemblages will be dumped. Optionally, -soli [ d_solutions ]; note that the hyphen is necessary to distinguish the identifier from the keyword [SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Solid-solution assemblages identified by any of the numbers in the list will be dumped. If list_of_ranges is empty, all solid-solution-assemblage definitions will be dumped.

Line 13: -solution list_of_ranges

-solution --Identifier indicates that solutions will be dumped. Optionally, -s [ olution ]; note that the hyphen is necessary to distinguish the identifier from the keyword [SOLUTION](phreeqc3-48.htm#50593793_89789).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Solutions identified by any of the numbers in the list will be dumped. If list_of_ranges is empty, all solution definitions will be dumped.

Line 14: -surface list_of_ranges

-surface --Identifier indicates that surface assemblages will be dumped. Optionally, -su [ rfaces ]; note that the hyphen is necessary to distinguish the identifier from the keyword [SURFACE](phreeqc3-52.htm#50593793_56392).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Surface assemblages identified by any of the numbers in the list will be dumped. If list_of_ranges is empty, all surface-assemblage definitions will be dumped.

Line 15: -cells list_of_ranges

-cells --Identifier indicates that all reactants identified by a specified number will be dumped, including equilibrium-phase assemblages, exchanger assemblages, gas phases, kinetic reactants, mix definitions, reaction definitions, reaction-temperature definitions, solid-solution assemblages, solutions, and surface assemblages. Optionally, cell , cells , or -c [ ells ].

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Reactants of any type that are identified by any of the numbers in the list will be dumped.

Line 16: -all

-all --Identifier indicates that all reactants will be dumped, including equilibrium-phase assemblages, exchanger assemblages, gas phases, kinetic reactants, mix definitions, reaction definitions, reaction-temperature definitions, solid-solution assemblages, solutions, and surface assemblages. Optionally, all or -al [ l ].

###### Notes

The DUMP data block allows a complete description of reactants to be written to a file in the raw formats. The unedited raw formats can be read directly by PHREEQC. The dump file can be included in an input file with keyword [INCLUDE$](phreeqc3-18.htm#50593793_74991) or can be read by an IPhreeqc module. All definitions of number ranges in the example at the beginning of this section, except for the first, dump reactants numbered 2 through 5. The first definition, -equilibrium_phases with no list_of_ranges, causes all equilibrium-phase assemblages to be dumped. The -cells identifier dumps reactants of all types that are identified by numbers in the list_of_ranges. The -all identifier dumps all reactants that are defined prior to or within the current simulation. The DUMP operations follow the [COPY](phreeqc3-8.htm#50593793_76644) operations and immediately precede the DELETE operations, which are the last operations of a simulation.

The raw format in which reactant data are written is not intended to be edited. Many of the fields are mandatory and deletion of them will cause an error when a raw data block is processed by PHREEQC. Furthermore, the raw formats may change. If additional capabilities are added to PHREEQC, the raw data formats will likely contain additional information to implement the new capabilities. Thus, data formatted in the raw formats may not be compatible with future versions of PHREEQC.

The DUMP data block may be useful to save the state of a transport or any other simulation to be able to restart calculations from that point; it is also possible to use the saved composition of a cell as the starting point for additional calculations. (Keyword [TRANSPORT](phreeqc3-56.htm#50593793_87317) also has a dump option for writing files at transport steps that are definable with identifier -dump_frequency .) When using IPhreeqc modules, DUMP can be used to write reactant compositions so that they can be transferred to other IPhreeqc modules; the DUMP data (string or file) can be read by another IPhreeqc module.

###### Related keywords

[COPY](phreeqc3-8.htm#50593793_76644), DELETE , [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207), [EQUILIBRIUM_PHASES_RAW](phreeqc3-88.htm#50593805_52879), [EXCHANGE](phreeqc3-14.htm#50593793_49135), [EXCHANGE_RAW](phreeqc3-90.htm#50593805_34249), [GAS_PHASE](phreeqc3-17.htm#50593793_83409), [GAS_PHASE_RAW](phreeqc3-92.htm#50593805_70184), [KINETICS](phreeqc3-24.htm#50593793_55637), [KINETICS_RAW](phreeqc3-94.htm#50593805_64390), [MIX](phreeqc3-27.htm#50593793_23725), [REACTION](phreeqc3-40.htm#50593793_75635), [REACTION_RAW](phreeqc3-96.htm#50593805_50923), [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966), [REACTION_PRESSURE_RAW](phreeqc3-97.htm#50593805_86080), [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016), [REACTION_TEMPERATURE_RAW](phreeqc3-98.htm#50593805_78104), [RUN_CELLS](phreeqc3-43.htm#50593793_78104), [SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444), [SOLID_SOLUTIONS_RAW](phreeqc3-100.htm#50593805_63833), [SOLUTION](phreeqc3-48.htm#50593793_89789), [SOLUTION_RAW](phreeqc3-102.htm#50593805_69484), [SURFACE](phreeqc3-52.htm#50593793_56392), and [SURFACE_RAW](phreeqc3-104.htm#50593805_23326).
