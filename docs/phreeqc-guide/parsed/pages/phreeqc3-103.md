---
title: "SURFACE_MODIFY"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-103.htm"
source_file: "phreeqc3-103.htm"
retrieved: 2026-09-22
category: keyword
---
# SURFACE_MODIFY

## SURFACE_MODIFY

This keyword data block is used to modify the definition of a previously defined surface-assemblage composition. New surfaces and surface-site types may be added, and the quantity of each surface-site type may be changed. In addition, it is possible to change the elemental composition of the surface and the elemental composition in the diffuse layer of the surface. The format of the data block is the same as the [SURFACE_RAW](phreeqc3-104.htm#50593805_23326) data block except that the data block need not be complete. The SURFACE_MODIFY data block can be used selectively to change data items. This Example data block lists a subset of identifiers that can be used in SURFACE_MODIFY data blocks.

###### Example data block

```phreeqc
Line 0:  SURFACE_MODIFY      1 Surface assemblage after simulation 2.
Line 1:	-only_counter_ions			0
Line 2:	-thickness			1e-008
Line 3:	-debye_lengths			0
Line 4:	-DDL_viscosity			1
Line 5:	-DDL_limit			0.8
Line 6:	-component				Hfo_sOH
 
Line 7:		-charge_balance			0.0010927661324556
Line 8:		-Dw			1e-009
Line 9:		-totals
Line 10:			Ca		0.0008229045119665
Line 10a:			H		0.0094469571085231
Line 10b:			Hfo_s		0.01
Line 10c:			O   		0.01
Line 6a:	-component				Hfo_wOH
 
Line 7a:		-charge_balance        -0.0010124274171143
Line 9a:		-totals
Line 10d:			Ca		1.1196909316487e-007
Line 10e:			H		0.00094211950362998
Line 10f:			Hfo_w		0.0010000000015016
Line 10g:			O		0.0029934399595643
Line 10h:			S		0.00050535150978271
Line 11:	-charge_component				Hfo
 
Line 12:		-specific_area			600
Line 13:		-grams			1
Line 14:		-charge_balance			-1.5437177225538e-012
Line 15:		-capacitance0			1
Line 16:		-capacitance1			5
Line 17:		-diffuse_layer_totals
Line 18:			Ca		6.7655957651525e-007
Line 18a:			H		0.66607460244918
Line 18b:			Na		2.2662527289495e-006
Line 18c:			O		0.33320521533783
Line 18d:			S		4.1978356284299e-005
```

###### Explanation

Line 0: SURFACE_MODIFY number [ description ]

SURFACE_MODIFY is the keyword for the data block.

number --Positive integer to identify the surface assemblage to modify.

description --Optional comment that describes the surface assemblage.

Line 1: -only_counter_ions ( 1 or 0 )

-only_counter_ions --Excludes co-ions in diffuse layer. See Line 7 in Explanation 1 of the [SURFACE](phreeqc3-52.htm#50593793_56392) data block.

(1 or 0)--A value of 1 indicates true. A value of 0 indicates false.

Line 2: -thickness thickness

-thickness --Thickness of diffuse layer. See -Donnan and -diffuse_layer in the [SURFACE](phreeqc3-52.htm#50593793_56392) data block. Optionally, thickness or -t [ hickness ].

thickness --Thickness of diffuse layer, m.

Line 3: -debye_lengths lengths

-debye_lengths --A factor for the Debye length is defined to determine the thickness of the diffuse layer. See -Donnan in the [SURFACE](phreeqc3-52.htm#50593793_56392) data block. Optionally, debye_lengths or -de [ bye_lengths ].

lengths --Factor used to calculate the thickness of the diffuse layer, unitless.

Line 4: -DDL_viscosity fraction

-DDL_viscosity --When considering multicomponent diffusion in the diffuse layer of surfaces, fraction is the viscosity in the diffuse layer relative to the viscosity in the free pore space. See -Donnan in the [SURFACE](phreeqc3-52.htm#50593793_56392) data block. Optionally, DDL_viscosity or -DD [ L_viscosity ].

fraction --Viscosity in the diffuse layer divided by the viscosity in the free pore space, unitless.

Line 5: -DDL_limit limit

-DDL_limit --If debye_lengths are used to define the thickness of the diffuse layer, limit is the maximum fraction of the total water that can be in the diffuse layer. See -Donnan in the [SURFACE](phreeqc3-52.htm#50593793_56392) data block. Optionally, DDL_limit or -DDL_l [ imit ].

limit --Maximum fraction of water in the diffuse layer, unitless.

Line 6: -component s urface site formula

-component --Identifier that indicates that information for a surface site will be defined. The identifier -component is required to precede the other identifiers that define information for the surface site. Optionally, component or -c [ omponent ].

surface site formula --Surface site formula. Surface site names have an underscore that is preceded by the surface name. The formula is a charge-balanced formula for the surface site.

Line 7: -charge_balance equiv

-charge_balance --Sum of the charge for all the species of the surface site. Optionally, charge_balance or -charge_b [ alance ].

equiv --Surface charge for the surface site defined by -component , eq.

Line 8: -Dw diffusion coefficient

-Dw --Diffusion coefficient for the surface site, which is used only if -multi_D is true in a [TRANSPORT](phreeqc3-56.htm#50593793_87317) simulation. Optionally, Dw or -D [ w ].

diffusion coefficient --Diffusion coefficient for the surface site, m 2 /s.

Line 9: -totals

-totals --Identifier begins a block of data containing the moles of elements related to the surface site. Optionally, totals or -t [ otals ].

Line 10: element moles

element --An element name or a surface site name.

moles --Moles of element or surface site, mol.

Line 11: -charge_component

-charge_component --Identifier that indicates that information on surface charge for a surface will be defined. The identifier -charge_component is required to precede the other identifiers that define information for the surface charge. Optionally, charge_component or -ch [ arge_component ].

surface name --Name of the surface. Surface site names have an underscore; the surface name precedes the underscore.

Line 12: -specific_area area

-specific_area --Specific area for the surface. See the [SURFACE](phreeqc3-52.htm#50593793_56392) data block. Optionally, specific_area or -s [ specific_area ].

area --Specific area for the surface, m 2 /g, or, if the surface is related to an equilibrium phase or kinetic reactant, m 2 /mol.

Line 13: -grams grams

-grams --Mass of the material containing the surface. See the [SURFACE](phreeqc3-52.htm#50593793_56392) data block. Optionally, grams or -g [ rams ].

grams --Mass of material containing the surface, g.

Line 14: -charge_balance equiv

-charge_balance --Charge of the surface, including the charge in the diffuse layer. If -Donnan or -diffuse_layer are defined for the [SURFACE](phreeqc3-52.htm#50593793_56392), then the charge balance for the surface will be near zero, such that the charge in the diffuse layer will be equal to the sum of the charge for all species for all surface sites for that surface. Optionally, charge_balance or -c [ harge_balance ].

equiv --Charge for the surface, eq.

Line 15: -capacitance0 c

-capacitance0 --Capacitance for the 0-1 planes in the CD-MUSIC formulation. See -capacitances in the [SURFACE](phreeqc3-52.htm#50593793_56392) data block. Optionally, capacitance0 or -ca [ pacitance0 ].

c --Capacitance for the 0-1 planes, F/m 2 .

Line 16: -capacitance1 c

-capacitance1 --Capacitance for the 1-2 planes in the CD-MUSIC formulation. See -capacitances in the [SURFACE](phreeqc3-52.htm#50593793_56392) data block. Optionally, capacitance1 or -capacitance1 .

c --Capacitance for the 1-2 planes, F/m 2 .

Line 17: -diffuse_layer_totals

-diffuse_layer_totals --Identifier begins a block of data containing the moles of elements in the diffuse layer for a surface. Values are present only if -Donnan or -diffuse_layer are defined for the surface. Optionally, diffuse_layer_totals or -d [ iffuse_layer_totals ].

Line 18: element, moles

element --An element name.

moles --Moles of element in the diffuse layer for the surface, mol.

###### Notes

The SURFACE_MODIFY data block allows modification of a preexisting surface assemblage, but care is needed for any modifications because data items have interdependencies. Although it is possible to add a new surface or surface site to a surface assemblage, defining consistent data for the new item is difficult. It is important that the -totals data block is consistent with the -charge_balance for surface components and that the -diffuse_layer_totals data block is consistent with the -charge_balance for surface charge components. If charge balance is not preserved, unexpected pH and redox conditions will result.

One use of the SURFACE_MODIFY data block might be in transporting surfaces, for example in conjunction with a sediment transport model. Another use might be for diffusive transport in the diffuse layer of surfaces. These transport calculations need to transport the charge [component -charge_balance and (or) charge-component -charge_balance ], elements [component -totals and (or) charge-component -diffuse_layer_totals ], and possibly other quantities, such as -grams and -specific area . SURFACE_MODIFY data blocks could be used to update surface-assemblage definitions after the transport calculations.

A SURFACE_MODIFY data block modifies only the data items specifically defined in the data block. Any data items in the surface assemblage definition not modified by the data block remain unchanged. Note specifically, that the -totals data block modifies all elements included in the data block, but the number of moles of any element related to the surface site that is not listed in the data block will remain unchanged.

###### Related keywords

[SURFACE](phreeqc3-52.htm#50593793_56392) and [SURFACE_RAW](phreeqc3-104.htm#50593805_23326).
