---
title: "EXCHANGE"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-14.htm"
source_file: "phreeqc3-14.htm"
retrieved: 2026-09-22
category: keyword
---
# EXCHANGE

## EXCHANGE

This keyword data block is used to define the amount and composition of an assemblage of exchangers. The initial composition of the exchange assemblage can be defined in two ways: (1) explicitly, by listing the composition of each exchange component; or (2) implicitly, by specifying that each exchanger is in equilibrium with a solution of fixed composition. The exchange master species, stoichiometries, and log K s for the exchange reactions are defined with the keywords [EXCHANGE_MASTER_SPECIES](phreeqc3-15.htm#50593793_33835) and [EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_60716). The number of exchange sites can be fixed, can be related to the amount of a phase in an equilibrium-phase assemblage, or can be related to the amount of a kinetic reactant.

###### Example data block 1

```phreeqc
Line 0:  EXCHANGE 10 Measured exchange composition
Line 1a:      CaX2     0.3
Line 1b:      MgX2     0.2
Line 1c:      NaX      0.5
Line 2a:      CaY2     Ca-montmorillonite					equilibrium_phase 0.165
Line 2b:      NaZ      Kinetic_clay					kinetic_reactant  0.1
Line 3:	-exchange_gammas				true
```

###### Explanation 1

Line 0: EXCHANGE [ number ] [ description ]

EXCHANGE is the keyword for the data block.

number --A positive number designates the exchange assemblage and its composition. A range of numbers may also be given in the form m-n , where m and n are positive integers, m is less than n , and the two numbers are separated by a hyphen without intervening spaces. Default is 1.

description --Optional comment that describes the exchanger.

Line 1: exchange formula, amount

exchange formula --Exchange species including stoichiometry of exchange ion and exchanger.

amount --Quantity of exchange species (mol).

Line 2: exchange formula, name, [( equilibrium_phase or kinetic_reactant )] , exchange_per_mole

exchange formula --Exchange species including stoichiometry of exchange ion and exchange site(s). The exchange formula must be charge balanced; if no exchange ions are included in the formula, then the exchange site must be uncharged.

name --Name of the pure phase or kinetic reactant that has this kind of exchange site. If name is a phase, the amount of the phase in an [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) data block with the same number as this exchange number (10, in the Example data block) will be used to determine the number of exchange sites. If name is a kinetic reactant, the amount of the reactant in a [KINETICS](phreeqc3-24.htm#50593793_55637) data block with the same number as this exchange number (10, in the Example data block) will be used to determine the number of exchange sites. Some care is needed in defining the stoichiometry of the exchange species if the exchangeable ions are related to a phase or kinetic reactant. The assumption is that some of the ions in the pure phase or kinetic reactant are available for exchange and these ions are defined through one or more entries of Line 2. The stoichiometry of the phase (defined in a [PHASES](phreeqc3-36.htm#50593793_84418) data block) or kinetic reactant (defined in a [KINETICS](phreeqc3-24.htm#50593793_55637) data block) must contain sufficient amounts of the exchangeable ions. From the Example data block (Line 2a) there must be at least 0.165 mol of calcium per mole of Ca-montmorillonite. From the Example data block (Line 2b) there must be at least 0.1 mol of sodium per mole of the reactant “kinetic_clay”.

equilibrium_phase or kinetic_reactant --If equilibrium_phase is used, the name on the line is a phase defined in an [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) data block. If kinetic_reactant is used, the name on the line is the rate name for a kinetic reactant defined in a [KINETICS](phreeqc3-24.htm#50593793_55637) data block. Optionally, e [ quilibrium_phase ] or k [ inetic_reactant ]. Default is equilibrium_phase .

exchange_per_mole --Number of moles of the exchange species per mole of phase or kinetic reactant, unitless (mol/mol).

Line 3: -exchange_gammas [( True or False )]

-exchange_gammas --This identifier selects whether exchange activity coefficients are assumed to be equal to aqueous activity coefficients when using the Pitzer or SIT aqueous model. This option has no effect when using ion-association aqueous models. Default is true if -exchange_gammas is not included. Optionally, exchange_gammas or -ex [ change_gammas ].

( True or False )--When using the Pitzer or SIT aqueous model, a value of true indicates that the aqueous activity coefficient for an ion will be used as the activity coefficient for the corresponding exchange species. A value of false indicates that activity of an exchange species will be equal to the equivalent fraction. If neither true nor false is entered on the line, true is assumed. Optionally, t [ rue ] or f [ alse ].

###### Notes 1

Line 1 may be repeated to define the entire composition of each exchanger. This Example data block defines the amount and composition of three exchangers, X, Y, and Z. Line 2 should be entered only once for each type of exchange site. The total number of exchange sites of X is 1.5 mol and the total concentrations of calcium, magnesium, and sodium on exchanger X are 0.3, 0.2, and 0.5 mol, respectively. When the composition of the exchanger is defined explicitly, such as in this Example data block, the exchanger will almost certainly not be in equilibrium with any of the solutions that have been defined. Any batch reaction that includes an explicitly defined exchanger will produce a reaction that causes change in solution and exchange composition.

Exchanger Y is related to the amount of Ca-montmorillonite in [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) 10, where 10 is the same number as the exchange-assemblage number. If m represents the moles of Ca-montmorillonite in [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) 10, then the number of moles of exchangeable component CaY 2 is 0.165 m , and the total number of exchange sites (Y) is 0.33 m (0.165 × 2). The stoichiometry of Ca must be at least 0.165 in the formula for Ca-montmorillonite. During batch-reaction simulations the exchange composition, including the moles of Ca exchanged, will change depending on competing species defined in [EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_60716). In addition, the moles of Ca-montmorillonite in [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) 10 may change, in which case the total moles of the exchange sites (Y) will change.

Exchanger Z is related to the amount of a kinetic reactant that dissolves and precipitates according to a rate expression named “kinetic_clay”. The formula for the kinetic reactant is defined in [KINETICS](phreeqc3-24.htm#50593793_55637) 10, where 10 is the same number as the exchange-assemblage number. If m represents the moles of kinetic_clay in [KINETICS](phreeqc3-24.htm#50593793_55637) 10, then the number of moles of exchangeable sodium (NaZ) is 0.1 m , which is equal to the total number of exchange sites. The stoichiometry of Na must be at least 0.1 in the formula for the kinetic reactant. The exchange composition will change during reaction calculations, depending on competing species defined in [EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_60716). In addition, the moles of kinetic_clay in [KINETICS](phreeqc3-24.htm#50593793_55637) 10 may change, in which case the total moles of the exchange sites (Z) will change.

The -exchange_gammas identifier selects whether exchange-species activity coefficients are set equal to aqueous activity coefficients for the Pitzer ( pitzer.dat database) or SIT ( sit.dat database) aqueous models. If -exchange_gammas is set to true, the activity coefficient for an exchange species is set equal to the activity coefficient of the corresponding aqueous species and is multiplied times the equivalent fraction of the exchange species to obtain the activity. If -exchange_gammas is set to false, the activity of an exchange species is equal to its equivalent fraction. For ion-association aqueous models (databases phreeqc.dat , wateq4f.dat , llnl.dat , minteq.dat , among others), exchange-species activity coefficient parameters (which are the same parameters as aqueous species) are defined in the [EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_60716) data block.

###### Example data block 2

```phreeqc
Line 0: EXCHANGE 1 Exchanger in equilibrium with solution 1
Line 1a:	X	1.0
Line 1b:	Xa	0.5
Line 2:	CaY2	Ca-montmorillonite   equilibrium_phase  0.165
Line 3:	-equilibrate with solution 1
Line 4:	-exchange_gammas				true
```

###### Explanation 2

Same as Example data block 1.

Line 1: exchange_site moles

exchange_site --Only the name of the exchange site needs to be entered.

moles --Quantity of exchange site (mol).

Line 2: exchange formula, name, [( equilibrium_phase or kinetic_reactant )] , exchange_per_mole (same as Example data block 1).

Line 3: -equilibrate number

-equilibrate --This string at the beginning of the line indicates that the exchange assemblage is defined to be in equilibrium with a given solution composition. Optionally, equil , equilibrate , equilibrium , -e [ quilibrate ], or -e [ quilibrium ].

number --Solution number with which the exchange assemblage is to be in equilibrium. Any alphabetic characters following the identifier and preceding an integer (“with solution” in Line 1) are ignored.

Line 4: -exchange_gammas [( True or False )]

-exchange_gammas --Same as Example data block 1.

###### Notes 2

The order of Lines 1, 2, 3, and 4 is not important. Line 3 should occur only once within the data block. Lines 1 and 2 may be repeated to define the amounts of other exchangers, if more than one exchanger is present in the assemblage. Example data block 2 requires PHREEQC to make a calculation to determine the composition of the exchange assemblage. The calculation will be performed before any batch-reaction calculations to determine the concentrations of each exchange component [such as CaX 2 , MgX 2 , or NaX (from the default database) provided calcium, magnesium, and sodium are present in solution] that would exist in equilibrium with the specified solution (solution 1 in this Example data block). The composition of the solution will not change during this calculation. When an exchange assemblage (as defined in Example data block 1 or Example data block 2) is placed in contact with a solution during a batch reaction, both the exchange composition and the solution composition will adjust to reach a new equilibrium.

The exchange ions given by the formulas in Lines 2 are not used in the initial exchange-composition calculation. However, the definition of the exchange ions is important for batch-reaction and transport calculations if the number of exchange sites is related to a pure phase or kinetic reactant. As the reactant, either a pure phase or a kinetic reactant, dissolves or precipitates, the number of exchange sites varies. Any new sites are initially filled with the exchangeable ions given in Line 2. When exchange sites are removed (for example, when a pure phase dissolves) then the net effect is to subtract from the pure phase formula the amount of the exchange ions defined in Line 2 and add an equivalent amount of ions to the solution. As an example, suppose some Ca-montmorillonite precipitates. Initially, calcium is in the exchange positions, but sodium replaces part of the calcium on the exchanger. When the montmorillonite dissolves again, the calcium in the formula for the phase is added to solution, the exchange ion (calcium from Line 2) is removed from solution, and the sodium and calcium from the exchanger is added to solution; the net effect is dissolution of (Na, Ca)-montmorillonite. Note that equilibrium for Ca-montmorillonite always uses the same mass-action equation, which includes only calcium, even though the composition of the phase is changing. Note also that this formulation implies that a pure Na-montmorillonite can never be attained because calcium must always be present to attain equilibrium with Ca-montmorillonite.

It is possible to realize a complete exchange of sodium and calcium by defining Y without cations under EXCHANGE , and a new equilibrium with only the structural ions of montmorillonite under [PHASES](phreeqc3-36.htm#50593793_84418). The combined reaction of exchanger and equilibrium phase must be electrically neutral. In the Example data block, the montmorillonite would be defined with a positive charge deficit of 0.165. When montmorillonite forms, the exchange sites Y increase in proportion and take cations from solution to exactly balance the charge deficit. Note that log_k for montmorillonite is adjusted by to account for an estimated contribution of 1 mmol/kgw (millimole per kilogram water) Ca in solution. Yet another possibility is to use the capabilities of the [SOLID_SOLUTIONS](phreeqc3-47.htm#50593793_77444) data block to define a variable composition solid solution between calcium and sodium montmorillonite end members.

```phreeqc
 
EXCHANGE 1 Exchanger in equilibrium with solution 1
    Y Montmorillonite equilibrium_phase  0.165
    -equilibrate with solution 1
PHASES
    -no_check        # must use no_check because of unbalanced equation
Montmorillonite      # Montmorillonite has 0.165 mol Y-/mol
Al2.33Si3.67O10(OH)2 + 12 H2O = 2.33 Al(OH)4- + 3.67 H4SiO4 + 2 H+
    log_k    -44.532 #Assume a Ca = 0.001 at equilibrium
    delta_h  58.373  kcal
```

An exchanger can be defined with a fixed number of sites initially, but through special definition of a kinetic reactant, the number of sites can vary with reaction progress. Changes in the number of exchange sites can be included in the [KINETICS](phreeqc3-24.htm#50593793_55637) keyword, under -formula . The combination of exchanger and kinetic reaction must be neutral.

```phreeqc
EXCHANGE 1
    # Z+ is related to Goethite, initial amount is 0.2 * m_go = 0.02
    Z   0.02
    -equil 1
KINETICS 1
    # Z has a charge of +1.0, Fe(OH)2+ sorbs anions.
    -formula  FeOOH 0.8  Fe(OH)2 0.2  Z  -0.2
    m    0.1
```

After a batch reaction has been simulated, it is possible to save the resulting exchange assemblage composition with the [SAVE](phreeqc3-44.htm#50593793_81857) keyword. If the new composition is not saved, the exchange assemblage composition will remain the same as it was before the batch reaction. After it has been defined or saved, the exchange assemblage can be used in subsequent simulations through the [USE](phreeqc3-57.htm#50593793_78143) keyword. [TRANSPORT](phreeqc3-56.htm#50593793_87317) and ADVECTION calculations automatically update the pure-phase assemblage and [SAVE](phreeqc3-44.htm#50593793_81857) has no effect during these calculations.

###### Example problems

The keyword EXCHANGE is used in example problems [11](phreeqc3-73.htm#50593807_46434), [12](phreeqc3-74.htm#50593807_12946), [13](phreeqc3-75.htm#50593807_22265) [14](phreeqc3-76.htm#50593807_89290), [19](phreeqc3-81.htm#50593807_18716), and [21](phreeqc3-83.htm#50593807_68313).

###### Related keywords

ADVECTION , [COPY](phreeqc3-8.htm#50593793_76644), DELETE , [DUMP](phreeqc3-11.htm#50593793_49635), [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207), [EXCHANGE_MASTER_SPECIES](phreeqc3-15.htm#50593793_33835), [EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_60716), [KINETICS](phreeqc3-24.htm#50593793_55637), [SAVE](phreeqc3-44.htm#50593793_81857) exchange , [TRANSPORT](phreeqc3-56.htm#50593793_87317), and [USE](phreeqc3-57.htm#50593793_55967) exchange .
