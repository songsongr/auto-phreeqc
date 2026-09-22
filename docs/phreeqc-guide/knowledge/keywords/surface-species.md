---
title: "SURFACE_SPECIES"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-54.htm"
source_file: "phreeqc3-54.htm"
retrieved: 2026-09-22
category: keyword
---
# SURFACE_SPECIES

## SURFACE_SPECIES

This keyword data block is used to define a reaction and log K for each surface species, including surface master species. Normally, this data block is included in the database file and only additions and modifications are included in the input file. Surface species defined in Dzombak and Morel (1990) are defined in the standard set of databases; the master species are Hfo_w and Hfo_s for the weak and strong binding sites of hydrous ferric oxide.

###### Example data block 1

```phreeqc
Line 0:  SURFACE_SPECIES 
Line 1a: Surf_sOH = Surf_sOH
Line 2a:       log_k     0.0
Line 1b: Surf_sOH + H+ = Surf_sOH2+
Line 2b:      log_k     6.3
Line 1c: Surf_wOH = Surf_wOH
Line 2c       log_k     0.0
Line 1d: Surf_wOH + H+ = Surf_wOH2+
Line 2d:      log_k     4.3
```

###### Explanation 1

Line 0: SURFACE_SPECIES

Keyword for the data block. No other data are input on the keyword line.

Line 1: Association reaction

Association reaction for surface species. The defined species must be the first species to the right of the equal sign. The association reaction must precede all identifiers related to the surface species. Line 1a is a master-species identity reaction.

Line 2: log_k log K

log_k --Identifier for log K at 25 °C. Optionally, -log_k , logk , -l [ og_k ], or -l [ ogk ].

log K --Log K at 25 °C for the reaction. Log K for a master species is 0.0. Default is 0.0.

###### Notes 1

This Example data block assumes that Surf_w and Surf_s are defined in a [SURFACE_MASTER_SPECIES](phreeqc3-53.htm#50593793_58106) data block. Lines 1 and 2 may be repeated as necessary to define all of the surface reactions. An identity reaction is needed to define each master surface species, Lines 1a and 1c in this Example data block. The log K for the identity reaction must be 0.0, Lines 2a and 2c in this Example data block.

An underscore plus one or more lowercase letters is used to define different binding sites for the same surface. In the Example data block, association reactions for a strong and a weak binding site are defined for the surface named “Surf”. Multiple surfaces may be defined simply by defining multiple master surface species (for example, Surfa, Surfb, and Surfc). Multiple binding sites can be defined for each surface by using an underscore followed by one or more lower case letters. Binding sites on the same surface share the same surface area, and have the same electrostatic potential.

Temperature dependence of log K can be defined with enthalpy of reaction (identifier delta_h ) and the Van’t Hoff equation or with an analytical expression ( -analytical_expression ). It is also possible to define a temperature-dependent expression in [MIX_EQUILIBRIUM_PHASES](phreeqc3-28.htm#50593793_79962) and use -add_logk to add its value to the equilibrium constant for the surface species. See [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_61994) or [PHASES](phreeqc3-36.htm#50593793_84418) for examples.

The identifier -no_check can be used to disable checking charge and elemental balances (see [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_61994)). The use of -no_check is not recommended. If -no_check is used, then the -mole_balance identifier is needed to ensure the correct stoichiometry for the surface species. In PHREEQC version 1, the -no_check option was included to permit the stoichiometry of a species to be defined separately from the mass-action equation. Specifically, the sorption of uranium on iron oxides as described by Waite and others (1994) provides an example, where they use different coefficients in the mass-action equation than in the mole-balance equations. However, activity of a surface species is defined as mole fraction of sites occupied by the species in PHREEQC versions 2 and 3, which is inconsistent with activity that is defined as molality by Waite and others (1994) and PHREEQC version 1. It is noted that formulas with coefficients of only 1 in the mass-action-equation will give identical results for all PHREEQC versions. The -no_check and -mole_balance identifiers have been retained in version 3, but their use should be restricted to special sorption formulas; for example, for modeling Freundlich isotherms (see [See Modeling Cd+2 Sorption With Linear, Freundlich, and Langmuir Isotherms, and With a Deterministic Distribution of Sorption Sites for Organic Matter, Clay Minerals, and Iron Oxyhydroxides](phreeqc3-81.htm#50593807_18716), in the [Examples](phreeqc3-62.htm#50593807_31416)).

###### Example data block 2

```phreeqc
Line 0:  SURFACE_SPECIES 
Line 1a:	Goe_uniOH-0.5 = Goe_uniOH-0.5
Line 2a:		log_k 0
Line 3:		-Vm    8.51 1.15 -0.678 -2.83   2.38   0 2.0  14.5 
Line 4a:		-cd_music  0 0 0 
Line 1b:	Goe_uniOH-0.5 + H+ + AsO4-3 = Goe_uniOAsO3-2.5 + H2O
Line 2b:		log_k     20.1                 
Line 4b:		-cd_music 0.25  -2.25  0 
Line 1c:	Goe_uniOH-0.5 + H+ + AsO4-3 = Goe_uniOAsO3-2.5 + H2O
Line 2c:		log_k     20.1                 
Line 5:		-cd_music  -1 -6 0 0.25 5
Line 1d:	Goe_triO-0.5 + Na+ = Goe_triONa+0.5
Line 2d:		log_k    -1                    
Line 4c:		-cd_music  0 0 1
```

###### Explanation 2

Line 3: Same as Example data block 1.

Line 4: -cd_music deltaz 0 , deltaz 1 , deltaz 2

-cd_music --Identifier for CD-MUSIC electrostatic parameters. More recent papers by Hiemstra and others (for example, Stachowicz and others, 2006) use this form to define the change in charge for the 0, 1, and 2 planes. Optionally, cd_music or -cd [ _music ].

deltaz 0 --The change in charge at the plane of specific adsorption, or 0 plane.

deltaz 1 --The change in charge at the Stern layer, or 1 plane.

deltaz 2 --The change in charge at the diffuse layer, or 2 plane.

Line 5: -cd_music dz 0 , dz 1 , dz 2 , fraction , Z ion

-cd_music --Identifier CD-MUSIC electrostatic parameters. Early papers by Hiemstra and others (for example, Hiemstra and van Riemsdijk, 1996) used this form to define the change in charge for the 0, 1, and 2 planes. Parameters defined by this method are converted to parameters as in Line 3 by the following equations: and . The meaning of deltaz 2 is the same in Lines 3 and 4. Optionally, cd_music or -cd [ _music ].

dz 0 --The change in charge at the plane of specific adsorption, or 0 plane due to gain or loss of hydrogen and oxygen.

dz 1 --The change in charge at the Stern layer, or 1 plane due to hydrogen and oxygen in the ligand.

fraction --The fraction of the central ion charge that is associated with plane 0.

ion_z --The charge on the central ion.

###### Notes 2

This Example data block defines surface species for a CD-MUSIC surface. The definitions assume that Goe_uni has been defined as a site in a [SURFACE_MASTER_SPECIES](phreeqc3-53.htm#50593793_58106) data block. Lines 1 through 3 in Example data block 2 are the same as for Example data block 1, but Lines 4 and 5 are specific to CD-MUSIC surfaces. Line 4b and Line 5 define the same electrostatic parameters for the same surface species in two alternative forms. Line 4b is now the more common form for definition of the distribution of surface charge for a species, where the change in charge at the three charge planes--the 0 or specific adsorption plane, the 1 or Stern layer plane, and the 2 or diffuse layer plane--is specified directly. Line 5 is an older form that separates the change in charge into that related to hydrogen and oxygen and that related to the distribution of charge from the central ion. Any parameters defined in the form of Line 5 are converted to the form of Line 4 for all surface calculations.

An underscore plus one or more lowercase letters is used to define different binding sites for the same CD-MUSIC surface. In the Example data block, Goe_uni and Goe_tri are two site types for a goethite surface.

###### Example problems

The keyword SURFACE_SPECIES is used in example problems [8](phreeqc3-70.htm#50593807_58878), [14](phreeqc3-76.htm#50593807_89290), [19](phreeqc3-81.htm#50593807_18716), and [21](phreeqc3-83.htm#50593807_68313). It is also found in the Amm.dat, iso.dat, llnl.dat, minteq.dat, minteq.v4.dat, phreeqc.dat, pitzer.dat, and wateq4f.dat databases.

###### Related keywords

[PHASES](phreeqc3-36.htm#50593793_84418), [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_61994), [SURFACE](phreeqc3-52.htm#50593793_56392), and [SURFACE_MASTER_SPECIES](phreeqc3-53.htm#50593793_58106).
