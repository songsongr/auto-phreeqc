---
title: "USE"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-57.htm"
source_file: "phreeqc3-57.htm"
retrieved: 2026-09-22
category: keyword
---
# USE

## USE

This keyword data block is used to specify explicitly which solution, exchange assemblage, gas phase, pure-phase assemblage, solid-solution assemblage, or surface assemblage is to be used in the batch-reaction calculation of a simulation. USE also can specify kinetically controlled reactions ([KINETICS](phreeqc3-24.htm#50593793_55637) data block), reaction parameters ([REACTION](phreeqc3-40.htm#50593793_75635) data block), reaction-pressure parameters ([REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966) data block), reaction-temperature parameters ([REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016) data block), and mixing parameters ([MIX](phreeqc3-27.htm#50593793_23725) data block) to be used in a batch-reaction calculation.

###### Example data block

```phreeqc
Line 0a: USE equilibrium_phases none 
Line 0b: USE exchange 2
Line 0c: USE gas_phase 3
Line 0d: USE kinetics 1
Line 0e: USE mix 1
Line 0f: USE reaction 2
Line 0g: USE reaction_pressure 1
Line 0h: USE reaction_temperature 1
Line 0i: USE solid_solution 6
Line 0j: USE solution 1
Line 0k: USE surface 1
```

###### Explanation

Line 0: USE keyword , ( number or none )

USE is the keyword for the data block.

keyword --One of 11 keywords, equilibrium_phases , exchange , gas_phase , kinetics , mix , reaction , reaction_pressure , reaction_temperature , solid_solutions , solution , or surface .

number --Positive integer associated with previously defined composition or reaction parameters.

none --No reactant of the type of the specified keyword will be used in the batch-reaction calculation.

###### Notes

Batch reactions are defined by allowing a solution or mixture of solutions to come to equilibrium with one or more of the following entities: an exchange assemblage, a pure-phase assemblage, a solid-solution assemblage, a surface assemblage, or a gas phase. In addition, kinetically controlled reactions, stoichiometric reactions, reaction pressures, and reaction temperatures can be specified for batch-reaction calculations.

Entities can be defined implicitly--a solution or mixture ([SOLUTION](phreeqc3-48.htm#50593793_89789) or [MIX](phreeqc3-27.htm#50593793_23725) keywords) must be defined within the simulation, then the first of each kind of entity defined in the simulation will be used to define the reaction system. Thus, the first solution (or mixture) will be brought together with the first of each of the following entities that is defined in the simulation: exchange assemblage ([EXCHANGE](phreeqc3-14.htm#50593793_49135)), gas phase ([GAS_PHASE](phreeqc3-17.htm#50593793_83409)), pure-phase assemblage ([EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207)), solid-solution assemblage ([SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444)), surface assemblage ([SURFACE](phreeqc3-52.htm#50593793_56392)); equilibrium among these entities will be calculated and maintained. Irreversible reactions may also be added implicitly to the system, and again, the first of the following entities that is defined in the simulation is added: kinetically controlled reaction ([KINETICS](phreeqc3-24.htm#50593793_55637)), stoichiometric reaction ([REACTION](phreeqc3-40.htm#50593793_75635)), reaction pressure ([REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966)), and reaction temperature ([REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016)).

Entities to be included in the system can be defined explicitly with the USE keyword. Any combination of USE keyword number data blocks can be used to define a system. “ USE keyword none ” can be used to eliminate an entity that was implicitly defined to be in the system. For example, if only a solution and a surface are defined in a simulation and the surface is defined to be in equilibrium with the solution, then implicitly, an additional batch-reaction calculation will be made to equilibrate the solution with the surface. Though not incorrect, the batch-reaction calculation will produce the same compositions for the solution and surface as previously defined. By including “ USE solution none ”, the batch-reaction calculation will be eliminated.

The composition of the solution, exchange assemblage, solid-solution assemblage, surface assemblage, pure-phase assemblage, or gas phase can be saved after a set of batch-reaction calculations with the [SAVE](phreeqc3-44.htm#50593793_81857) keyword.

The [RUN_CELLS](phreeqc3-43.htm#50593793_74089) data block can be used to define a specific batch-reaction calculation. With [RUN_CELLS](phreeqc3-43.htm#50593793_74089); -cells n , all reactants that are numbered n are put together and reacted. If [MIX](phreeqc3-27.htm#50593793_23725) n has been defined, it will take precedence over [SOLUTION](phreeqc3-48.htm#50593793_30253) n . If neither [MIX](phreeqc3-27.htm#50593793_23725) n nor [SOLUTION](phreeqc3-48.htm#50593793_30253) n have been defined, then no reaction will be calculated. USE data blocks have no effect on the selection of reactants for a [RUN_CELLS](phreeqc3-43.htm#50593793_74089) calculation. The compositions of reactants following a [RUN_CELLS](phreeqc3-43.htm#50593793_74089) calculation are automatically saved with the same identifying number, n .

###### Example problems

The keyword USE is used in example problems [2](phreeqc3-64.htm#50593807_28577), [3](phreeqc3-65.htm#50593807_51496), [6](phreeqc3-68.htm#50593807_49505), [7](phreeqc3-69.htm#50593807_44022), [8](phreeqc3-70.htm#50593807_58878), [10](phreeqc3-72.htm#50593807_24858), [14](phreeqc3-76.htm#50593807_89290), [20](phreeqc3-82.htm#50593807_33272), and [22](phreeqc3-84.htm#50593807_97000).

###### Related keywords

[EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207), [EXCHANGE](phreeqc3-14.htm#50593793_49135), [GAS_PHASE](phreeqc3-17.htm#50593793_83409), [KINETICS](phreeqc3-24.htm#50593793_55637), [MIX](phreeqc3-27.htm#50593793_23725), [REACTION](phreeqc3-40.htm#50593793_75635), [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966), [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016), [RUN_CELLS](phreeqc3-43.htm#50593793_74089), [SAVE](phreeqc3-44.htm#50593793_81857), [SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444), [SOLUTION](phreeqc3-48.htm#50593793_89789), and [SURFACE](phreeqc3-52.htm#50593793_56392).
