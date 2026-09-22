---
title: "EQUILIBRIUM_PHASES_MODIFY"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-87.htm"
source_file: "phreeqc3-87.htm"
retrieved: 2026-09-22
category: keyword
---
# EQUILIBRIUM_PHASES_MODIFY

## EQUILIBRIUM_PHASES_MODIFY

This keyword data block is used to modify the definition of a previously defined equilibrium-phase assemblage. New phases may be added and the quantity of each phase may be changed. The format of the data block is the same as the [EQUILIBRIUM_PHASES_RAW](phreeqc3-88.htm#50593805_52879) data block, except that the data block need not be complete. The EQUILIBRIUM_PHASES_MODIFY data block can be used selectively to change data items. The Example data block lists a subset of identifiers that can be used in the EQUILIBRIUM_PHASES_MODIFY data block.

###### Example data block

```phreeqc
Line 0:	EQUILIBRIUM_PHASES_MODIFY 1 Added Barite
Line 1:	-component		Barite
Line 2:		-add_formula			BaCl2
Line 3:		-si			0
Line 4:		-moles			10
Line 5:		-force_equality			0
Line 6:		-dissolve_only			1
Line 7:		-precipitate_only			0
```

###### Explanation

Line 0: EQUILIBRIUM_PHASES_MODIFY number [ description ]

EQUILIBRIUM_PHASES_MODIFY is the keyword for the data block.

number --Positive integer to identify the equilibrium-phase assemblage to modify.

description --Optional comment that describes the equilibrium-phase assemblage.

Line 1: -component name

-component --Identifier that indicates information will be defined for a phase in the equilibrium-phase assemblage. The identifier -component is required to precede the other identifiers for a phase definition. Optionally, component or -c [ omponent ].

name --Name of a phase that has been defined in a [PHASES](phreeqc3-36.htm#50593793_84418) data block.

Line 2: -add_formula alternative formula

-add_formula --Defines a reactant other than the phase that reacts to produce equilibrium; see alternative formula in the description of the [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) data block. Optionally, add_formula or -a [ dd_formula ].

alternative formula --Phase name or chemical formula.

Line 3: -si saturation index

-si --Defines the target saturation index for the phase; see saturation index in the description of the [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) data block. Optionally, si or -s [ i ].

saturation index --Target saturation index for the phase.

Line 4: -moles moles

-moles --Defines the amount of the phase that can react; see amount in the description of the [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) data block. Optionally, moles or -m [ oles ].

moles --Moles of phase or alternative formula .

Line 5: -force_equality ( 1 or 0 )

-force_equality --Defines whether the equation for phase equilibrium is an inequality or equality constraint in the set of equations to be solved; see -force_equality in the description of the [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) data block. Optionally, force_equality or -f [ orce_equality ].

( 1 or 0 )--A value of 1 indicates true. A value of 0 indicates false.

Line 6: -dissolve_only ( 1 or 0 )

-dissolve_only --Defines whether the phase is required only to dissolve; see -dissolve_only in the description of the [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) data block. Optionally, dissolve_only or -di [ ssolve_only ].

Line 7: -precipitate_only ( 1 or 0 )

-precipitate_only --Defines whether the phase is required only to precipitate; see -precipitate_only in the description of the [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) data block. Optionally, precipitate_only or -p [ recipitate_only ].

###### Notes

The EQUILIBRIUM_PHASES_MODIFY data block allows modification of a preexisting equilibrium-phase assemblage. The most common uses are to add a new phase to the phase assemblage and to change the amount of a phase that is present in the assemblage. It also is possible to change the target saturation index for a phase, whether the phase can only dissolve or can only precipitate, and whether an equality or inequality constraint is included for the phase in the set of equations that are solved.

EQUILIBRIUM_PHASES_MODIFY modifies only the data items specifically defined in the data block. Any data items in the equilibrium-phases definition not modified by the data block remain unchanged.

###### Related keywords

[EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) and [EQUILIBRIUM_PHASES_RAW](phreeqc3-88.htm#50593805_52879).
