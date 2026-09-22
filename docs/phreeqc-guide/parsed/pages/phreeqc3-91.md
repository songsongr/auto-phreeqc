---
title: "GAS_PHASE_MODIFY"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-91.htm"
source_file: "phreeqc3-91.htm"
retrieved: 2026-09-22
category: keyword
---
# GAS_PHASE_MODIFY

## GAS_PHASE_MODIFY

This keyword data block is used to modify the definition of a previously defined gas phase. New gas components may be added, and the quantity of each gas component may be changed. In addition, it is possible to change the type of the gas phase between fixed pressure and fixed volume, and to change the total pressure of a fixed-pressure gas phase and the volume of a fixed-volume gas phase. The format of the data block is the same as the [GAS_PHASE_RAW](phreeqc3-92.htm#50593805_70184) data block except that the data block need not be complete. The GAS_PHASE_MODIFY data block can be used selectively to change data items. This Example data block lists a subset of identifiers that can be used in GAS_PHASE_MODIFY data blocks.

###### Example data block

```phreeqc
Line 0:  GAS_PHASE_MODIFY 1 Add CO2(g) component
Line 1:	-type               0
Line 2:	-total_p            1
Line 3:	-volume             1.5
Line 4:	-component		CO2(g)
Line 5:		-moles   1.4305508698401e-005
```

###### Explanation

Line 0: GAS_PHASE_MODIFY number [ description ]

GAS_PHASE_MODIFY is the keyword for the data block.

number --Positive integer to identify the gas phase to modify.

description --Optional comment that describes the gas phase.

Line 1: -type ( 1 or 0 )

-type --Identifier that indicates the type of the gas phase, either fixed pressure or fixed volume. Optionally, type or -t [ ype ].

( 1 or 0 )--1 indicates a fixed-volume gas phase, and 0 indicates a fixed-pressure gas phase.

Line 2: -total_p pressure

-total_p --Defines the pressure for a fixed-pressure gas phase. Optionally, pressure , total_p , -p [ ressure ], or -to [ tal_p ].

pressure --Total pressure of a fixed-pressure gas phase (atmospheres).

Line 3: -volume volume

-volume --Defines the volume for a fixed-volume gas phase. Optionally, volume or -v [ olume ].

volume --Total volume of a fixed-volume gas phase (liter).

Line 4: -component component_name

-component --Begins a data block that adds gas components or modifies the number of moles of gas components. Optionally, component or -c [ omponent ].

component_name --Name of a gas component as defined in a [PHASES](phreeqc3-36.htm#50593793_84418) data block.

Line 5: -moles moles

moles --Number of moles of the gas component in the gas phase; it is a positive number.

###### Notes

The GAS_PHASE_MODIFY data block allows modification of a preexisting gas phase. The most common uses are to change the pressure ( -total_p ) of a fixed-pressure gas phase, to change the volume ( -volume ) of a fixed-volume gas phase, to add a new gas component to the gas phase, and to change the number of moles of a gas component that is present in the gas phase. It also is possible to change the gas phase from a fixed-pressure gas phase to a fixed-volume gas phase, and the reverse.

The GAS_PHASE_MODIFY data block modifies only the data items specifically defined in the data block. Any data items in the gas-phase definition not modified by the data block remain unchanged. In particular, if a single new component is defined, any other gas components already defined in the gas phase are unchanged.

###### Related keywords

[GAS_PHASE](phreeqc3-17.htm#50593793_83409) and [GAS_PHASE_RAW](phreeqc3-92.htm#50593805_70184).
