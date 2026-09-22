---
title: "RUN_CELLS"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-43.htm"
source_file: "phreeqc3-43.htm"
retrieved: 2026-09-22
category: keyword
---
# RUN_CELLS

## RUN_CELLS

This keyword data block is used to run reaction simulations for a specified set of cells. For a specified cell number, n, all reactants numbered n are reacted together and the resulting reactant compositions are saved to the same cell number. If multiple steps have been defined in [KINETICS](phreeqc3-24.htm#50593793_55637) n, [REACTION](phreeqc3-40.htm#50593793_75635) n, [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966) n, or [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016) n data blocks, multiple calculations will be done for each cell. It is possible to specify the starting time and the time step for cells that have kinetic reactants; these time values defined in RUN_CELLS supersede the definitions in the [KINETICS](phreeqc3-24.htm#50593793_55637) data block.

###### Example data block

```phreeqc
Line 0: RUN_CELLS
Line 1:	-cells	1 2
Line 2:		5-6
Line 2a:		7
Line 3:	-start_time		100 day
Line 4:	-time_step		10  day
```

###### Explanation

Line 0: RUN_CELLS

RUN_CELLS is the keyword for the data block. No other data are input on the keyword line.

Line 1: -cells list of cell numbers

-cells --Identifier for a list of cells to be run. Optionally, cell , cells , or -c [ ells ].

list of cell numbers --A list of cell numbers. Each item of the list may be a single cell number or a range of cell numbers defined by two integers separated by a hyphen, with no intervening spaces.

Line 2: list of cell numbers

list of cell numbers --The list of cell numbers for the -cells identifier may be continued on multiple lines.

Line 3: -start_time time [unit]

-start_time --Identifier defining a start time for cells that have kinetic reactants. Optionally, start_time or -s [ tart_time ].

time --Time at the beginning of the simulation for a cell that has kinetic reactants, s.

unit --Optional time unit may be second , minute , hour , day , year , or an abbreviation of one of these units. The time is converted to seconds after reading the data block; all internal calculations, Basic functions, and output times are in seconds. Default is second.

Line 4: -time_step time_step [unit]

-time_step --Identifier defining a time step for cells that have kinetic reactants. Optionally, time_step or -t [ ime_step ].

time_step --Time step for the simulation for a cell that has kinetic reactants, s.

unit --Optional time unit may be second , minute , hour , day , year , or an abbreviation of one of these units. The time_step is converted to seconds after reading the data block; all internal calculations, Basic functions, and output times are in seconds. Default is second.

###### Notes

The RUN_CELLS data block is a streamlined method for running a simulation that uses all reactants that have been defined with the same identification number (cell number). The calculation for a cell defined in the -cells data block is equivalent to a series of [USE](phreeqc3-57.htm#50593793_78143) and [SAVE](phreeqc3-44.htm#50593793_81857) data blocks for all of the reactants with a specified cell number. If both a solution and a mix definition exist for a cell number, the mix definition is used in preference to the solution. If multiple steps have been defined in [KINETICS](phreeqc3-24.htm#50593793_55637), [REACTION](phreeqc3-40.htm#50593793_75635), [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966), or [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016) data blocks, then multiple calculations will be done for that cell.

It is possible to specify an initial time for a kinetic integration by using the -start_time identifier and to override the time step from the [KINETICS](phreeqc3-24.htm#50593793_55637) data block by using the -time_step identifier. If -time_step is not defined or a [KINETICS](phreeqc3-24.htm#50593793_55637) data block is not defined for the cell, then the calculations occur exactly as they would by a series of [USE](phreeqc3-57.htm#50593793_78143) and [SAVE](phreeqc3-44.htm#50593793_81857) data blocks. If -time_step is defined, then the kinetic reaction will be integrated over an interval of time_step. If nmax is the maximum number of steps defined for the cell with [KINETICS](phreeqc3-24.htm#50593793_55637), [REACTION](phreeqc3-40.htm#50593793_75635), [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966), or [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016) data blocks, then the kinetic reaction will be divided into nmax equal increments; the results are equivalent to defining “ -step time_step in nmax steps” in the [KINETICS](phreeqc3-24.htm#50593793_55637) data block. The time_step will be used for all subsequent RUN_CELLS calculations or until it is changed with another -time_step definition in a RUN_CELLS data block.

The RUN_CELLS data block simplifies the definition of repetitive reactions in batch calculations. It also is intended to be used when an IPhreeqc module implements geochemical reactions in a reactive-transport model. For example, if a transport model has a set of cells numbered 1 through n , and the chemical reactants for those cells are saved as identification numbers 1 through n in an IPhreeqc module, then a simple sequential calculation can be implemented. The transport code is used to transport elemental concentrations conservatively, and the concentrations for solutions in the IPhreeqc module are updated with a series of [SOLUTION_MODIFY](phreeqc3-101.htm#50593805_89789) data blocks. Geochemical reactions are calculated by the data block: RUN_CELLS ; -cells 1- n . The new compositions of solutions and reactants are automatically stored in the IPhreeqc module and new solution concentrations are retrieved by extracting data defined by [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) or by the output from a [DUMP](phreeqc3-11.htm#50593793_49635) data block. The new solution concentrations then are used to begin a new conservative transport step.

###### Example problems

The keyword RUN_CELLS is used in example problem [20](phreeqc3-82.htm#50593807_33272).

###### Related keywords

[DUMP](phreeqc3-11.htm#50593793_49635), [SAVE](phreeqc3-44.htm#50593793_81857), [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239), [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_96148), and [USE](phreeqc3-57.htm#50593793_78143).
