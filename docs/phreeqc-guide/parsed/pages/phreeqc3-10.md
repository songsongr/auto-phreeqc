---
title: "DELETE"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-10.htm"
source_file: "phreeqc3-10.htm"
retrieved: 2026-09-22
category: keyword
---
# DELETE

## DELETE

This keyword data block is used to delete reactants. Any reactant that is identified by an integer can be deleted, which includes reactants defined by [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207), [EXCHANGE](phreeqc3-14.htm#50593793_49135), [GAS_PHASE](phreeqc3-17.htm#50593793_83409), [KINETICS](phreeqc3-24.htm#50593793_55637), [MIX](phreeqc3-27.htm#50593793_23725), [REACTION](phreeqc3-40.htm#50593793_75635), [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966), [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016), [SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444), [SOLUTION](phreeqc3-48.htm#50593793_89789), and [SURFACE](phreeqc3-52.htm#50593793_56392) data blocks.

###### Example data block

```phreeqc
Line 0: DELETE
Line 1:	-equilibrium_phases		
Line 2:	-exchange			2 4
Line 3:				3 5
Line 4:	-gas_phase			2-4 5
Line 5:	-kinetics			3-5 2
Line 6:	-mix			2 3
Line 6a:	-mix			4 5
Line 7:	-reaction      			2-3 4 5
Line 8:	-reaction_pressure			2 3 4-5
Line 9:	-reaction_temperature 
Line 3a:				2 3 4 5
Line 10:	-solid_solution
Line 3b:				5 4 3 2
Line 11:	-solution 			2 3 4 5
Line 12:	-surface
Line 3c:				2-3 4-5
Line 3d:				5
Line 13:	-cells			2-5
Line 14:	-all
```

###### Explanation

Line 0: DELETE

DELETE is the keyword for the data block. No other data are input on the keyword line.

Line 1: -equilibrium_phases list_of_ranges

-equilibrium_phases --Identifier indicates that equilibrium-phase assemblages will be deleted. Optionally, -e [ quilibrium_phases ]; note that the hyphen is necessary to distinguish the identifier from the keyword [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Equilibrium-phase assemblages identified by any of the numbers in the list will be deleted. If list_of_ranges is empty, all equilibrium-phase-assemblage definitions will be deleted.

Line 2: -exchange list_of_ranges

-exchange --Identifier indicates that exchange assemblages will be deleted. Optionally, -ex [ change ]; note that the hyphen is necessary to distinguish the identifier from the keyword [EXCHANGE](phreeqc3-14.htm#50593793_49135).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Exchange assemblages identified by any of the numbers in the list will be deleted. If list_of_ranges is empty, all exchange-assemblage definitions will be deleted.

Line 3: list_of_ranges

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Line 3 can be used to begin a list of ranges or to continue a list of ranges.

Line 4: -gas_phase list_of_ranges

-gas_phase --Identifier indicates that gas phases will be deleted. Optionally, -g [ as_phase ]; note that the hyphen is necessary to distinguish the identifier from the keyword [GAS_PHASE](phreeqc3-17.htm#50593793_83409).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Gas phases identified by any of the numbers in the list will be deleted. If list_of_ranges is empty, all gas-phase definitions will be deleted.

Line 5: -kinetics list_of_ranges

-kinetics --Identifier indicates that kinetic reactants will be deleted. Optionally, -k [ inetics ]; note that the hyphen is necessary to distinguish the identifier from the keyword [KINETICS](phreeqc3-24.htm#50593793_55637).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Kinetics reactants identified by any of the numbers in the list will be deleted. If list_of_ranges is empty, all kinetic-reaction definitions will be deleted.

Line 6: -mix list_of_ranges

-mix --Identifier indicates that solution mix definitions will be deleted. Optionally, -m [ ix ]; note that the hyphen is necessary to distinguish the identifier from the keyword [MIX](phreeqc3-27.htm#50593793_23725).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Mix definitions identified by any of the numbers in the list will be deleted. If list_of_ranges is empty, all mix definitions will be deleted.

Line 7: -reaction list_of_ranges

-reaction --Identifier indicates that reactions will be deleted. Optionally, -r [ eaction ]; note that the hyphen is necessary to distinguish the identifier from the keyword [REACTION](phreeqc3-40.htm#50593793_75635).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Reactions identified by any of the numbers in the list will be deleted. If list_of_ranges is empty, all reaction definitions will be deleted.

Line 8: -reaction_pressure list_of_ranges

-reaction_pressure --Identifier indicates that reaction-pressure definitions will be deleted. Optionally, -reaction_p [ ressure ], pressure , or -pr [ essure ]; note that the hyphen is necessary to distinguish the identifier from the keyword [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Reaction-pressure definitions identified by any of the numbers in the list will be deleted. If list_of_ranges is empty, all reaction-pressure definitions will be deleted.

Line 9: -reaction_temperature list_of_ranges

-reaction_temperature --Identifier indicates that reaction-temperature definitions will be deleted. Optionally, -reaction_ [ temperature ], temperature , or -t [ emperature ]; note that the hyphen is necessary to distinguish the identifier from the keyword [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Reaction-temperature definitions identified by any of the numbers in the list will be deleted. If list_of_ranges is empty, all reaction-temperature definitions will be deleted.

Line 10: -solid_solution list_of_ranges

-solid_solution --Identifier indicates that solid-solution assemblages will be deleted. Optionally, -soli [ d_solutions ]; note that the hyphen is necessary to distinguish the identifier from the keyword [SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Solid-solution assemblages identified by any of the numbers in the list will be deleted. If list_of_ranges is empty, all solid-solution assemblage definitions will be deleted.

Line 11: -solution list_of_ranges

-solution --Identifier indicates that solutions will be deleted. Optionally, -s [ olution ]; note that the hyphen is necessary to distinguish the identifier from the keyword [SOLUTION](phreeqc3-48.htm#50593793_89789).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Solutions identified by any of the numbers in the list will be deleted. If list_of_ranges is empty, all solution definitions will be deleted.

Line 12: -surface list_of_ranges

-surface --Identifier indicates that surface assemblages will be deleted. Optionally, -su [ rfaces ]; note that the hyphen is necessary to distinguish the identifier from the keyword [SURFACE](phreeqc3-52.htm#50593793_56392).

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Surface assemblages identified by any of the numbers in the list will be deleted. If list_of_ranges is empty, all surface-assemblage definitions will be deleted.

Line 13: -cells list_of_ranges

-cells --Identifier indicates that all reactants identified by a specified number will be deleted, including equilibrium-phase assemblages, exchanger assemblages, gas phases, kinetic reactants, mix definitions, reaction definitions, reaction-temperature definitions, solid-solution assemblages, solutions, and surface assemblages. Optionally, -c [ ells ].

list_of_ranges --List of number ranges. The number ranges may be a single integer or a range defined by an integer, a hyphen, and an integer, without intervening spaces. Reactants of any type that are identified by any of the numbers in the list will be deleted. If list_of_ranges is empty, all numbered reactants of all types will be deleted (same as - all ) .

Line 14: -all

-all --All numbered reactants of all types will be deleted.

###### Notes

The DELETE data block allows reactants to be deleted. All definitions in the example at the beginning of this section, except the first, delete reactants numbered 2 through 5. The first definition, -equilibrium_phases with no list_of_ranges, causes all equilibrium-phase-assemblage definitions to be deleted. The DELETE operations follow the [COPY](phreeqc3-8.htm#50593793_76644) and [DUMP](phreeqc3-11.htm#50593793_49635) operations and are the last operations of a simulation.

Usually, it is not necessary to use the DELETE data block in PHREEQC simulations because new definitions of reactants automatically overwrite old definitions and all reactants are deleted at the end of a run. The DELETE data block may be useful to remove reactants from cells between advection or transport calculations, to conserve memory during a run, or for reinitializing IPhreeqc modules (Charlton and Parkhurst, 2011).

###### Related keywords

[COPY](phreeqc3-8.htm#50593793_76644), [DUMP](phreeqc3-11.htm#50593793_49635), [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207), [EXCHANGE](phreeqc3-14.htm#50593793_49135), [GAS_PHASE](phreeqc3-17.htm#50593793_83409), [KINETICS](phreeqc3-24.htm#50593793_55637), [MIX](phreeqc3-27.htm#50593793_23725), [REACTION](phreeqc3-40.htm#50593793_75635), [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966), [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016), [SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444), [SOLUTION](phreeqc3-48.htm#50593793_89789), and [SURFACE](phreeqc3-52.htm#50593793_56392).
