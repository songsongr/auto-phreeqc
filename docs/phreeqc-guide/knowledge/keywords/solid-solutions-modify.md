---
title: "SOLID_SOLUTIONS_MODIFY"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-99.htm"
source_file: "phreeqc3-99.htm"
retrieved: 2026-09-22
category: keyword
---
# SOLID_SOLUTIONS_MODIFY

## SOLID_SOLUTIONS_MODIFY

This keyword data block is used to modify the definition of a previously defined solid-solution assemblage. New solid solutions and new components of solid solutions may be added. The number of moles of each solid-solution component may be changed. The format of the data block is the same as the [SOLID_SOLUTIONS_RAW](phreeqc3-100.htm#50593805_63833) data block except that the data block need not be complete. The SOLID_SOLUTIONS_MODIFY data block can be used selectively to change data items. The Example data block lists a subset of identifiers that can be used in SOLID_SOLUTIONS_MODIFY data blocks.

###### Example data block

```phreeqc
Line 0:	SOLID_SOLUTION_MODIFY 1
Line 1:	-solid_solution			Calcite_SS
Line 2:		-component		calcite
Line 3:			-moles		0.2
Line 2a:		-component		rhodochrosite
Line 3a:			-moles		0.2
Line 2b:		-component		siderite	
Line 3b:			-moles		0.001
```

###### Explanation

Line 0: SOLID_SOLUTIONS_MODIFY number [ description ]

SOLID_SOLUTIONS_MODIFY is the keyword for the data block.

number --Positive integer to identify the solid-solution assemblage to modify.

description --Optional comment that describes the solid-solution assemblage.

Line 1: -solid_solution name

-solid_solution --Identifier that indicates a solid solution will be defined. The identifier -solid_solution is required to precede the other identifiers that define the solid-solution composition. Optionally, solid_solution or -s [ olid_solution ].

name --Name of the solid solution.

Line 2: -component component

-component --Identifier begins a data block that modifies a solid-solution component. The identifier -component is required to precede the modifications to the component. Optionally, component or -c [ omponent ].

component --The solid solution component to be added or modified. If component is already in the solid solution, then the number of moles is changed; if component is not in the solid solution, then it is added.

Line 3: -moles moles

-moles --Identifier for the number of moles of a solid-solution component. Optionally, moles or -m [ oles ].

moles --Number of moles of component in solid solution name .

###### Notes

The SOLID_SOLUTIONS_MODIFY data block allows modification of a preexisting solid-solution assemblage. The most common uses are to change the amount of a component in a solid solution, to add a new component to an ideal solid solution, and to add a new solid solution to a solid-solution assemblage.

SOLID_SOLUTIONS_MODIFY modifies only the data items specifically defined in the data block. Any data items in the solid-solution assemblage definition not modified by the data block remain unchanged.

###### Related keywords

[SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444) and [SOLID_SOLUTIONS_RAW](phreeqc3-100.htm#50593805_63833).
