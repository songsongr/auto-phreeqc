---
title: "Appendix A. Keyword Data Blocks for Programmers"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-86.htm"
source_file: "phreeqc3-86.htm"
retrieved: 2026-09-22
category: concept
---
# Appendix A. Keyword Data Blocks for Programmers

## Appendix A. Keyword Data Blocks for Programmers

A number of keywords are intended to be used when scripting or programming with an IPhreeqc module (Charlton and Parkhurst, 2011). The IPhreeqc module provides a set of methods that expose the full capabilities of PHREEQC to other programs and allows retrieval of specified values (as defined in [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) and [USER_PUNCH](phreeqc3-60.htm#50593793_56415)).

One use of an IPhreeqc module is to incorporate geochemical reactions into a transport model. The strategy is to specify reactants for a set of cells in an IPhreeqc module and perform geochemical reactions for a time step with the [RUN_CELLS](phreeqc3-43.htm#50593793_78104) data block. The solution concentrations are retrieved from the module, transported by the transport model, and returned to the IPhreeqc module for renewed geochemical calculations. A series of keyword data blocks have been written that facilitate transferring and modifying concentration data. These data blocks end with the suffixes _MODIFY and _RAW . In this reactive-transport strategy, [SOLUTION_MODIFY](phreeqc3-101.htm#50593805_89789) could be used to update solution concentrations in the IPhreeqc module after a transport step. [SOLUTION_MODIFY](phreeqc3-101.htm#50593805_89789) is related to [SOLUTION_RAW](phreeqc3-102.htm#50593805_69484), which is an input data block that is written by the [DUMP](phreeqc3-11.htm#50593793_49635) operation and contains a complete description of a solution composition. [SOLUTION_MODIFY](phreeqc3-101.htm#50593805_89789) has the same format as [SOLUTION_RAW](phreeqc3-102.htm#50593805_69484) and allows one or more data items of the solution composition to be modified and also allows new data items (moles of another element in solution, for example) to be added.

Keyword equivalents to [SOLUTION_MODIFY](phreeqc3-101.htm#50593805_89789) and [SOLUTION_RAW](phreeqc3-102.htm#50593805_69484) data blocks exist for equilibrium-phase assemblages, exchange assemblages, gas phases, solid-solution assemblages, surface assemblages, kinetic-reaction assemblages, stoichiometric reactions, reaction pressures, and reaction temperatures. A complete list of _MODIFY and _RAW data blocks is given in [See List of keyword data blocks for scripting and programming.](phreeqc3-86.htm#50593805_33821). There is no keyword MIX_RAW or MIX_MODIFY because the [MIX](phreeqc3-27.htm#50593793_23725) data block can be used. Similarly, REACTION_TEMPERATURE_MODIFY and REACTION_TEMPERATURE_MODIFY data blocks are not needed; the [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966) and [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016) data blocks can be used to modify temperature definitions. The set of _MODIFY keywords provides capabilities to change any data item in any reactant. Although transport is expected to apply primarily to solutions, it would be possible to transport exchange assemblages analogously to solutions by transporting the elements that define the composition of exchangers and then updating the exchange composition of a cell by using [EXCHANGE_MODIFY](phreeqc3-89.htm#50593805_49135) with the results of the transport calculations.

###### List of keyword data blocks for scripting and programming.

|  |
Keyword data block

|

Function

|  |
[EQUILIBRIUM_PHASES_MODIFY](phreeqc3-87.htm#50593805_84573)

Modify the definition of an equilibrium-phase assemblage

|  |
[EQUILIBRIUM_PHASES_RAW](phreeqc3-88.htm#50593805_52879)

Complete description of an equilibrium-phase assemblage as written by [DUMP](phreeqc3-11.htm#50593793_49635)

|  |
[EXCHANGE_MODIFY](phreeqc3-89.htm#50593805_49135)

Modify the definition of an exchange assemblage

|  |
[EXCHANGE_RAW](phreeqc3-90.htm#50593805_34249)

Complete description of an exchange assemblage as written by [DUMP](phreeqc3-11.htm#50593793_49635)

|  |
[GAS_PHASE_MODIFY](phreeqc3-91.htm#50593805_44837)

Modify the definition of a gas phase

|  |
[GAS_PHASE_RAW](phreeqc3-92.htm#50593805_70184)

Complete description of a gas phase as written by [DUMP](phreeqc3-11.htm#50593793_49635)

|  |
[KINETICS_MODIFY](phreeqc3-93.htm#50593805_79204)

Modify the definition of a kinetic reactant assemblage

|  |
[KINETICS_RAW](phreeqc3-94.htm#50593805_64390)

Complete description of a kinetic reactant assemblage as written by [DUMP](phreeqc3-11.htm#50593793_49635)

|  |
[REACTION_MODIFY](phreeqc3-95.htm#50593805_31337)

Modify the definition of an irreversible reaction

|  |
[REACTION_RAW](phreeqc3-96.htm#50593805_50923)

Complete description of a REACTION definition as written by [DUMP](phreeqc3-11.htm#50593793_49635)

|  |
[REACTION_PRESSURE_RAW](phreeqc3-97.htm#50593805_86080)

Complete description of a REACTION_PRESSURE definition as written by [DUMP](phreeqc3-11.htm#50593793_49635)

|  |
[REACTION_TEMPERATURE_RAW](phreeqc3-98.htm#50593805_78104)

Complete description of a REACTION_TEMPERATURE definition as written by [DUMP](phreeqc3-11.htm#50593793_49635)

|  |
[SOLID_SOLUTIONS_MODIFY](phreeqc3-99.htm#50593805_81857)

Modify the definition of a solid-solution assemblage

|  |
[SOLID_SOLUTIONS_RAW](phreeqc3-100.htm#50593805_63833)

Complete description of a solid-solution assemblage as written by [DUMP](phreeqc3-11.htm#50593793_49635)

|  |
[SOLUTION_MODIFY](phreeqc3-101.htm#50593805_89789)

Modify the definition of a solution composition

|  |
[SOLUTION_RAW](phreeqc3-102.htm#50593805_69484)

Complete description of a solution as written by [DUMP](phreeqc3-11.htm#50593793_49635)

|  |
[SURFACE_MODIFY](phreeqc3-103.htm#50593805_78804)

Modify the definition of a surface-assemblage composition

|  |
[SURFACE_RAW](phreeqc3-104.htm#50593805_23326)

Complete description of a surface-assemblage composition as written by [DUMP](phreeqc3-11.htm#50593793_49635)

The _RAW data blocks (and possibly [MIX](phreeqc3-27.htm#50593793_23725)) are written by the [DUMP](phreeqc3-11.htm#50593793_49635) operation and are intended to be used without modification. The [DUMP](phreeqc3-11.htm#50593793_49635) operation can be used to save the state of a calculation. The _RAW data blocks that are written by [DUMP](phreeqc3-11.htm#50593793_49635) can be read by PHREEQC and the entire chemical state of the calculation will be restored to the point where [DUMP](phreeqc3-11.htm#50593793_49635) was executed. [DUMP](phreeqc3-11.htm#50593793_49635) also can be used to transfer data among IPhreeqc modules by dumping the data in one module and reading the data in another.

The use of the _MODIFY data blocks is complicated and subject to errors. Any item of data can be changed, but some are used for internal calculations, and changing the value externally has no effect. Some items cannot be reasonably changed, and others are interrelated so that a change to one may require a change to another as well. In particular, the number of moles of elements, including H and O, and the charge balance should not be changed independently because doing so may cause unforeseen pe and (or) pH changes. Varying just the number of moles of a single element (sodium for example) would be equivalent to adding or removing sodium metal from solution, which also would produce unexpected redox and pH reactions.

The _MODIFY data blocks are not intended for general use, but can be used by program developers. As such, developers are largely responsible for their use, and only limited support is provided. In the following description of input for _MODIFY keywords, a subset of the complete set of data in the _RAW data blocks is presented. Each subset is somewhat arbitrary, but has, in principle, the data items that could reasonably be changed with appropriate care.

###  EQUILIBRIUM_PHASES_MODIFY 

###  EQUILIBRIUM_PHASES_RAW 

###  EXCHANGE_MODIFY 

###  EXCHANGE_RAW 

###  GAS_PHASE_MODIFY 

###  GAS_PHASE_RAW 

###  KINETICS_MODIFY 

###  KINETICS_RAW 

###  REACTION_MODIFY 

###  REACTION_RAW 

###  REACTION_PRESSURE_RAW 

###  REACTION_TEMPERATURE_RAW 

###  SOLID_SOLUTIONS_MODIFY 

###  SOLID_SOLUTIONS_RAW 

###  SOLUTION_MODIFY 

###  SOLUTION_RAW 

###  SURFACE_MODIFY 

###  SURFACE_RAW 
