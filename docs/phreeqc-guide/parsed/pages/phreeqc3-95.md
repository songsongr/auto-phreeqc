---
title: "REACTION_MODIFY"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-95.htm"
source_file: "phreeqc3-95.htm"
retrieved: 2026-09-22
category: keyword
---
# REACTION_MODIFY

## REACTION_MODIFY

This keyword data block is used to modify the definition of a previously defined irreversible reaction. New reactants may be added, and the stoichiometry of reactants may be changed. The format of the data block is the same as [REACTION_RAW](phreeqc3-96.htm#50593805_50923) data block, except that the data block need not be complete. The REACTION_MODIFY data block can be used selectively to change data items. The Example data block lists a subset of identifiers that can be used in REACTION_MODIFY data blocks.

###### Example data block

```phreeqc
Line 0: REACTION_MODIFY 1 				Adding calcite and MgSO4
Line 1:	  -units			uMol
Line 2:	  -reactant_list
Line 3:		Calcite		2
Line 3a:		MgSO4		0.2
Line 4:	  -steps
Line 5:		.1
Line 6:	  -equal_increments			1
Line 7:	  -count_steps			10
```

###### Explanation

Line 0: REACTION_MODIFY number [ description ]

REACTION_MODIFY is the keyword for the data block.

number --Positive integer to identify the stoichiometric reaction to modify.

description --Optional comment that describes the stoichiometric reaction.

Line 1: -units units

-units --Units are moles, millimoles, micromoles, or an abbreviation of these units. Optionally, units or -u [ nits ].

Line 2: -reactant_list

-reactant_list --Begins a data block that defines reactants in the stoichiometric reaction. Optionally, reactant_list or -r [ eactant_list ].

Line 3: ( phase name or formula ) , relative stoichiometry

( phase name or formula )--The name of a phase defined in a [PHASES](phreeqc3-36.htm#50593793_84418) data block or a chemical formula; see ( phase name or formula ) in the description of the [REACTION](phreeqc3-40.htm#50593793_75635) data block.

relative stoichiometry --Amount of this reactant relative to other reactants; see relative stoichiometry in the description of the [REACTION](phreeqc3-40.htm#50593793_75635) data block.

Line 4: -steps

-steps --Begins a data block that defines the steps for the reaction. Optionally, steps or -s [ teps ].

Line 5: list of reaction amounts

list of reaction amounts --Defines the amounts of the stoichiometric reaction to add to a solution or mixture; see reaction amounts in the description of the [REACTION](phreeqc3-40.htm#50593793_75635) data block.

Line 6: -equal_increments ( 1 or 0 )

-equal_increments --Defines whether a single reaction amount is divided into one or more equal steps as specified by -count_steps ; see “ in ” in the description of the [REACTION](phreeqc3-40.htm#50593793_75635) data block. Optionally, equal_increments or -eq [ ual_increments ].

( 1 or 0 )--A value of 1 indicates true, and the first reaction amount is split into equal increments. A value of 0 indicates false, and the list of reaction amounts determines the amounts of the stoichiometric reaction added to a solution or mixture.

Line 7: -count_steps n

-count_steps --If -equal_increments is equal to 1, the value of n determines the number of equal increments for the reaction; see “ in ” in the description of the [REACTION](phreeqc3-40.htm#50593793_75635) data block. Optionally, count_steps or -c [ ount_steps ].

n --Number of equal steps for the stoichiometric reaction.

###### Notes

The REACTION_MODIFY data block allows modification of a preexisting stoichiometric reaction definition. The most common uses of the data block are to add a new reactant to the list of reactants, to change the relative coefficients of reactants, and to change the reactant amounts. It also is possible to change the units for the reaction and whether the reaction is added in equal increments or as defined by a list of reaction increments.

REACTION_MODIFY modifies only the data items specifically defined in the data block. Any data items in the stoichiometric reaction definition not modified by the data block remain unchanged. If -steps is defined in the data block, the previous list of reaction amounts is removed and is replaced by the new definitions.

###### Related keywords

[REACTION](phreeqc3-40.htm#50593793_75635) and [REACTION_RAW](phreeqc3-96.htm#50593805_50923).
