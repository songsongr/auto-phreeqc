---
title: "SOLUTION_MODIFY"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-101.htm"
source_file: "phreeqc3-101.htm"
retrieved: 2026-09-22
category: keyword
---
# SOLUTION_MODIFY

## SOLUTION_MODIFY

This keyword data block is used to modify the definition of a previously defined solution composition. New elements may be added to the solution, and the number of moles of elements may be changed. However, care is needed to preserve the correct relations between the number of moles of elements, equivalents of charge imbalance, and moles of hydrogen and oxygen. Initial estimates for log activity of master species are updated automatically if the number of moles of an element is adjusted; alternatively, new initial estimates for log activity of master species may be specified explicitly with -activities . The format of the data block is the same as the [SOLUTION_RAW](phreeqc3-102.htm#50593805_69484) data block except that the data block need not be complete. The SOLUTION_MODIFY data block can be used selectively to change data items. The Example data block lists a subset of identifiers that can be used in SOLUTION_MODIFY data blocks.

###### Example data block

```phreeqc
Line 0:  SOLUTION_MODIFY 1 Modified solution description
Line 1:	-temp              25
Line 2:	-total_h           111.01243359981
Line 3:	-total_o           55.506216800086
Line 4:	-cb                -3.657928589893e-10
Line 5:	-totals
Line 6:		Cl	0.0020000000000003
Line 6a:		Fe(2)	3.9999998897204e-007
Line 6b:		Fe(3)	1.1027960586156e-014
Line 6d:		Na	0.0020000000000003
Line 6c:		S	0.02012
Line 13:	-pressure		100
```

The following lines optionally set initial estimates of master variables.

```phreeqc
Line 7:	-pH	6.61
Line 8:	-pe	0
Line 9:	-mu	0.07
Line 10:	-ah2o	0.9985
Line 11:	-activities
Line 12a:		Cl	-3.0
Line 12b:		Fe(2)	-7.6
Line 12c:		Fe(3)	-23.4
Line 12d:		Na	-3.0
Line 12e:		S	-3.9
```

###### Explanation

Line 0: SOLUTION_MODIFY number [ description ]

SOLUTION_MODIFY is the keyword for the data block.

number --Positive integer to identify the solution to modify.

description --Optional comment that describes the solution.

Line 1: -temp tc

-temp tc --Sets the temperature for the solution; tc is in degrees Celsius.

Line 2: -total_h moles

-total_h moles --Total moles of hydrogen in the solution. A solution with one kilogram of water, contains approximately 111.0 moles of hydrogen; however, the value must be known precisely to set the correct redox conditions.

Line 3: -total_o moles

-total_o moles --Total moles of oxygen in the solution. A solution with one kilogram of water, contains approximately 55.5 moles of oxygen; however, the value must be known precisely to set the correct redox conditions.

Line 4: -cb equivalents

-cb equivalents --Equivalents of charge imbalance in the solution. Although physical solutions are nearly perfectly balanced in charge, analytical errors can result in apparent charge imbalances for solutions. Surface reactions without explicit definition of the double layer composition also can impart charge imbalances to a solution. The value of the charge imbalance must be known precisely to set the correct redox conditions.

Line 5: -totals

-totals --Identifier begins a block of data that modifies the number of moles of elements or element valence states in the solution.

Line 6: ( Element or element valence state ) moles

Element or element valence state --An element or element valence state that has been defined in a [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910) data block. If a redox element is specified (that is, a redox element name without following parentheses), all valence states of the element are removed from the solution and moles is the total number of moles of the redox element in solution, inclusive of all valence states. If an element valence state is defined (that is, a redox element name with following parentheses), then, if present, the element (no parentheses) is removed from solution, and the element valence state (with parentheses) is added to the solution.

moles --Number of moles of the element or element valence state in the solution.

Line 7: -pH pH

-pH pH --Sets the initial estimate of the pH, which is used in solving the system of nonlinear equations that define solution equilibrium.

Line 8: -pe pe

-pe pe --Sets the initial estimate of the pe, which is used in solving the system of nonlinear equations that define solution equilibrium.

Line 9: -mu mu

-mu mu --Sets the initial estimate of the ionic strength, which is used in solving the system of nonlinear equations that define solution equilibrium.

Line 10: -ah2o ah2o

-ah2o ah2o --Sets the initial estimate of the activity of water, which is used in solving the system of nonlinear equations that define solution equilibrium.

Line 11: -activities

-activities --Identifier begins a data block that sets initial estimates of the activities of the master species, which are used in solving the system of nonlinear equations that define solution equilibrium. For redox elements, the activity of only one redox state is used in solving the equilibrium equations. The activity used is usually that of the primary master species; however, it is possible that the equations have been rewritten so that the primary master species has been replaced by one of the secondary master species, in which case, the initial estimate of the secondary master species is the one that is used to begin solving the nonlinear equations that define solution equilibrium. When the number of moles of an element are changed, log activities for that element [and (or) element valence states] automatically will be adjusted by log of the new number of moles divided by the old number of moles. Use of -activities overrides this automatic adjustment for each element in the -activities list.

Line 12: master species , log activity

master species --An element or element valence state master species that has been defined in a [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910) data block.

log activity --Initial estimate of the log activity of the master species, which is used in solving the system of nonlinear equations that define solution equilibrium.

Line 13: -pressure pressure

-pressure pressure--Sets the pressure for the solution, in atm.

###### Notes

The SOLUTION_MODIFY data block allows modification of a preexisting solution definition. Lines 1 through 6 in the Example data block set the temperature and the number of moles of elements and element redox states for the solution. Care is needed to maintain concordance between the number of moles of elements (including hydrogen and oxygen) and the charge imbalance. Inconsistent alteration of the moles of elements and equivalents of charge imbalance will result in unexpected pH and redox reactions.

Lines 7 through 12 set initial estimates of unknowns for the equations that define solution equilibrium but do not affect the actual solution composition or the ultimate values of the numerical solution to the equations. The definitions on lines 7 through 12 could affect whether a numerical solution is found or the number of iterations needed to find a numerical solution. The initial estimates of unknowns can make a substantial difference in the number of iterations to solve a chemical system and, consequently, in run times, especially for transport calculations. If the number of moles of an element is adjusted ( -totals ), by default, the log activity associated with that element is automatically adjusted by the log of the ratio of the new moles to the old moles. Logic is included to adjust valence states as well as total moles of a redox element. Use of -activities for an element supersedes the automatic adjustment for log activities for that element.

The most common use of a SOLUTION_MODIFY data block is expected to be in transport models that use IPhreeqc modules. The transport code is used to transport elemental concentrations conservatively, and then the moles of elements in the solutions in the IPhreeqc module are updated with the transport results by using a series of [SOLUTION_MODIFY](phreeqc3-101.htm#50593805_96148) data blocks. Geochemical reactions are calculated in the IPhreeqc module, and the new compositions of solutions are retrieved by extracting data defined by [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) or by the output from a [DUMP](phreeqc3-11.htm#50593793_49635) data block. The reacted solution concentrations then are used to begin a new conservative transport step in the transport model. Care is needed to convert the moles of an element in an IPhreeqc solution (as written with [DUMP](phreeqc3-11.htm#50593793_49635)) to the concentration of the element used in the transport code, and, conversely, to convert the concentrations from transport to the number of moles in an IPhreeqc solution.

SOLUTION_MODIFY modifies only the data items specifically defined in the data block. Any data items in the solution definition not modified by the data block remain unchanged. Modification of the number of moles of redox elements requires special care. A redox element is defined simply by the element name and represents the total moles of that element, including all valence states. A redox element valence state is defined by the element name followed by a valence state in parentheses. When a redox element is defined in -totals , all element valence states are removed from the solution, and only the total concentration remains. When a redox element valence state is defined in -totals , then the redox element (total moles), if it is present, is removed, but other valence-state concentrations are retained.

###### Related keywords

[SOLUTION](phreeqc3-48.htm#50593793_30253) and [SOLUTION_RAW](phreeqc3-102.htm#50593805_69484).
