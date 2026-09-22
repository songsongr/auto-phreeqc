---
title: "REACTION"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-40.htm"
source_file: "phreeqc3-40.htm"
retrieved: 2026-09-22
category: keyword
---
# REACTION

## REACTION

This keyword data block is used to define irreversible reactions that transfer specified amounts of elements to or from the aqueous solution during batch-reaction calculations. REACTION steps are specified explicitly and do not depend on solution composition or time. The [KINETICS](phreeqc3-24.htm#50593793_55637) and RATES data blocks should be used to model the rates of irreversible reactions that evolve with time and vary with solution composition.

###### Example data block 1

```phreeqc
Line 0:  REACTION 5 Add sodium chloride and calcite to solution.
Line 1a:      NaCl     2.0
Line 1b:      Calcite  0.001
Line 2:       0.25     0.5     0.75     1.0  moles
```

###### Explanation 1

Line 0: REACTION [ number ] [ description ]

REACTION is the keyword for the data block.

number --A positive number designates this stoichiometric reaction definition. A range of numbers also may be given in the form m-n , where m and n are positive integers, m is less than n , and the two numbers are separated by a hyphen without intervening spaces. Default is 1.

description --Optional comment that describes the stoichiometric reaction.

Line 1: ( phase name or formula ), [ relative stoichiometry ]

phase name or formula --If a phase name is given, the program uses the stoichiometry of that phase as defined by [PHASES](phreeqc3-36.htm#50593793_84418) input; otherwise, formula is a chemical formula to be used in the stoichiometric reaction. Additional lines can be used to define additional reactants.

relative stoichiometry --Amount of this reactant relative to other reactants; it is a molar ratio between reactants. In the Example data block, the reaction contains 2,000 times more NaCl (Line 1a) than calcite (line 1b). Default is 1.0 unitless (mol/mol).

Line 2: list of reaction amounts, [ units ]

list of reaction amounts --A separate calculation will be made for each listed amount. If [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204) is false (default), Example data block 1 performs the calculation as follows: the first step adds 0.25 mol of reaction (assuming units are “moles”) to the initial solution; the second step adds 0.5 mol of reaction to the initial solution; the third 0.75 mol; and the fourth 1.0 mol; each reaction step begins with the same initial solution and adds only the amount of reaction specified. If [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204) keyword is true , the calculations are performed as follows: the first step adds 0.25 mol of reaction and the intermediate results are saved as the starting point for the next step; then 0.5 mol of reaction are added and the intermediate results saved; then 0.75 mol; then 1.0 mol; the total amount of reaction added to the initial solution is 2.5 mol. The total amount of each reactant added at any step in the reaction is the reaction amount times the relative stoichiometric coefficient of the reactant. Additional lines may be used to define all reactant amounts.

units --Units may be moles, millimoles, or micromoles. Units must follow all reaction amounts. Default is moles.

If Line 2 is not entered, the default is one step of 1.0 mol.

###### Example data block 2

```phreeqc
Line 0: REACTION 5 Add sodium chloride and calcite to reaction solution.
Line 1a:     NaCl       2.0
Line 1b:     Calcite    0.001
Line 2:      1.0 moles in 4 steps
```

###### Explanation 2

Same as Example data block 1.

Line 1: ( phase name or formula ) , [ relative stoichiometry ]

Line 2: reaction amount [ units ] [ in steps ]

reaction amount --A single reaction amount is entered. This amount of reaction will be added in steps steps.

units --Same as Example data block 1.

in steps --“ in ” indicates that the stoichiometric reaction will be divided into steps number of steps. If [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204) is false (default), Example data block 2 performs the calculations as follows: the first step adds 0.25 mol of reaction to the initial solution; the second step adds 0.5 mol of reaction to the initial solution; the third 0.75 mol; and the fourth 1.0 mol. If [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204) keyword is true , the calculations are performed as follows: each of the four steps adds 0.25 mol of reaction and the intermediate results are saved as the starting point for the next step.

###### Notes

The REACTION data block is used to increase or decrease solution concentrations by specified amounts of reaction. If the product of reaction amount and relative stoichiometry is positive, then the phase name or formula will be added to the solution; if the product is negative, the phase name or formula will be removed from the solution. The specified reactions are added to or removed from solution without regard to equilibrium, time, or reaction kinetics. Irreversible reactions that evolve in time or depend on concentration must be modeled with the [KINETICS](phreeqc3-24.htm#50593793_55637) and RATES keywords.

Example data block 1 with [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204) false and Example data block 2 with [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204) true or false will generate the same solution compositions after 0.25, 0.5, 0.75, and 1.0 mol of reaction have been added. Example data block 1 with [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204) true generates results after 0.25, 0.75, 1.5, and 2.5 mol of reaction have been added.

If a phase name is used to define the stoichiometry of a reactant, that phase must have been defined by [PHASES](phreeqc3-36.htm#50593793_84418) input in the database or in the input data file. If negative relative stoichiometries or negative reaction amounts are used, it is possible to remove more of an element than is present in the system, which results in negative concentrations. Negative concentrations will cause the calculations to fail. It is possible to “evaporate” a solution by removing H 2 O or dilute a solution by adding H 2 O. If more reaction steps are defined in the [KINETICS](phreeqc3-24.htm#50593793_55637), [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966), or [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016) data blocks than in REACTION , then the final reaction amount defined by REACTION will be repeated for the additional steps. Suppose only one reaction step of 1.0 mol is specified in a REACTION data block and two temperature steps are specified in a [REACTION_TEMPERATURE](phreeqc3-42.htm#50593793_75016) data block. If [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204) is false , then the total amount of reaction added by the end of step 1 and step 2 is the same, 1.0 mol. However, if [INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204) is true , the total amount of reaction added by the end of step 1 will be 1.0 mol and by the end of step 2 will be 2.0 mol.

###### Example problems

The keyword REACTION is used in example problems [4](phreeqc3-66.htm#50593807_70531), [5](phreeqc3-67.htm#50593807_31870), [6](phreeqc3-68.htm#50593807_49505), [7](phreeqc3-69.htm#50593807_44022), [10](phreeqc3-72.htm#50593807_24858), [17](phreeqc3-79.htm#50593807_83128), [19](phreeqc3-81.htm#50593807_18716), [20](phreeqc3-82.htm#50593807_33272), and [22](phreeqc3-84.htm#50593807_97000).

###### Related keywords

[INCREMENTAL_REACTIONS](phreeqc3-19.htm#50593793_79204), [KINETICS](phreeqc3-24.htm#50593793_55637), [PHASES](phreeqc3-36.htm#50593793_84418), [RATES](phreeqc3-39.htm#50593793_97907), [REACTION_PRESSURE](phreeqc3-41.htm#50593793_65966), and REACTION_TEMPERATURE .
