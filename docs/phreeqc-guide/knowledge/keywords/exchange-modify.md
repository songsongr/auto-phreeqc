---
title: "EXCHANGE_MODIFY"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-89.htm"
source_file: "phreeqc3-89.htm"
retrieved: 2026-09-22
category: keyword
---
# EXCHANGE_MODIFY

## EXCHANGE_MODIFY

This keyword data block is used to modify the definition of a previously defined exchange assemblage. New exchangers may be added and the quantity and composition of each exchanger may be altered. The format of the data block is the same as the [EXCHANGE_RAW](phreeqc3-90.htm#50593805_34249) data block except that the data block need not be complete.The EXCHANGE_MODIFY data block can be used selectively to change data items. The Example data blocks list a subset of identifiers that can be used in EXCHANGE_MODIFY data blocks.

###### Example data block 1

```phreeqc
Line 0:	EXCHANGE_MODIFY 1 Added Y
Line 1:	-component		Y
Line 2:		-totals
Line 3:			Na	1.0
Line 3a:			Y	1.0
Line 4:	-exchange_gammas				true
```

###### Explanation 1

Line 0: EXCHANGE_MODIFY number [ description ]

EXCHANGE_MODIFY is the keyword for the data block.

number --Positive integer to identify the exchange assemblage to modify.

description --Optional comment that describes the exchange assemblage.

Line 1: -component exchange site

-component --Identifier that indicates information for an exchanger in the exchange assemblage will be added or modified. The identifier -component is required to precede the other identifiers that define the exchanger. Optionally, component or -c [ omponent ].

exchange site --Exchange site formula.

Line 2: -totals

-totals --Identifier begins a block of data containing the moles of elements in the exchanger. Optionally, totals or -t [ otals ].

Line 3: element moles

element --An element name or an exchange site name.

moles --Moles of element or exchange site present in the exchanger; it is a positive number.

Line 4: -exchange_gammas ( 1 or 0 )

-exchange_gammas --This identifier selects whether exchange activity coefficients are assumed to be equal to aqueous activity coefficients when using the Pitzer or SIT aqueous model. Optionally, exchange_gammas or -ex [ change_gammas ]. The option has no effect when using ion-association aqueous models.

(1 or 0)--A value of 1 indicates true. A value of 0 indicates false.

###### Notes 1

The EXCHANGE_MODIFY data block allows modification of a preexisting exchange assemblage, but care is needed for any modifications because data items have interdependencies. The most common uses are to add a new exchanger to an exchange assemblage and to change the amount of an exchanger that is present in the assemblage. However, it is important that the -totals data block defines an exchange composition, such that the number of equivalents of exchange sites is balanced by an equal number of equivalents of ions. The totals are assumed to balance in charge, and any charge in the formulas of -totals will be ignored. If, for example, 1 mol of X, with master species X - , and 2 moles of Na, with master species Na + , are defined, it will be equivalent to adding 1 mol of NaX and 1 mol of Na metal, and unexpected pH and redox conditions will result. It also is possible to change the choice of activity coefficient option ( -exchange_gammas ) when using the Pitzer or SIT aqueous models.

EXCHANGE_MODIFY modifies only the data items specifically defined in the data block. Any data items in the exchanger definition not modified by the data block remain unchanged. Note specifically that the -totals data block modifies the elements as defined in the data block, but any element not listed in the data block will remain unchanged in the exchange composition.

###### Example data block 2

```phreeqc
Line 0:	EXCHANGE_MODIFY 1 Added Y
Line 1:	-component		NaY
	Line 2:		-totals
Line 3:			Na	0.002
Line 3a:			Y	0.002
Line 4:		-phase_name		Na-Mont
Line 5:		-phase_proportion			0.1
Line 6:	-exchange_gammas				true
```

###### Explanation 2

Line 1: -component exchange formula

-component --Defines the formula for the exchange site; see exchange formula in the description of the [EXCHANGE](phreeqc3-14.htm#50593793_49135) data block. Optionally, formula or -f [ ormula ].

exchange formula --Exchange site formula.

-totals --Same as Explanation 1.

Line 3: element moles .

element moles --Same as Explanation 1.

Line 4: ( -phase_name or -rate_name ) name

-phase_name --Defines the name of an equilibrium phase to which the number of exchange sites is related. See equilibrium_phase in the description of the [EXCHANGE](phreeqc3-14.htm#50593793_49135) data block. Optionally, phase_name or -p [ hase_name ].

-rate_name --Defines the name of a kinetic reactant to which the number of exchange sites is related. See kinetic_reactant in the description of the [EXCHANGE](phreeqc3-14.htm#50593793_49135) data block. Optionally, rate_name or -r [ ate_name ].

name --Name of an equilibrium phase or a kinetic reactant.

Line 5: -phase_proportion exchange_per_mole

-phase_proportion --Defines the number of moles of exchange formula per mole of phase or kinetic reactant; see exchange_per_mole in the description of the [EXCHANGE_MODIFY](phreeqc3-89.htm#50593805_49135) data block. Optionally, phase_proportion or -phase_p [ roportion ].

exchange_per_mole --Number of moles of the exchange formula per mole of phase or kinetic reactant, unitless.

Line 6: -exchange_gammas ( 1 or 0 ).

-exchange_gammas --Same as Explanation 1

###### Notes 2

This example shows how to add a new exchanger that is related to an equilibrium phase. As in Example data block 1, it is important that the -totals data block defines a charge-balanced exchange composition. If charge balance is not preserved or the number of moles of exchange sites is inconsistent with the number of moles of the phase, unexpected pH and redox conditions will result. Moreover, the number of moles of the exchange site (Y in this example) must be consistent with the number of moles of the equilibrium phase, as defined by the -phase_proportion and -formula identifiers. Use of -phase_name or -rate_name for an exchanger numbered n requires that an [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) n or [KINETICS](phreeqc3-24.htm#50593793_55637) n has been defined.

###### Related keywords

[EXCHANGE](phreeqc3-14.htm#50593793_49135) and [EXCHANGE_RAW](phreeqc3-90.htm#50593805_34249).
