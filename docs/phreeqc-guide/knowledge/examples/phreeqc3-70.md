---
title: "Example 8--Surface Complexation"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-70.htm"
source_file: "phreeqc3-70.htm"
retrieved: 2026-09-22
category: example
---
# Example 8--Surface Complexation

## Example 8--Surface Complexation

In all surface complexation models, sorption is a function of both chemical and electrostatic energy as described by the free energy relationship:

### ΔGtot = ΔGads + zFψ, (21)

where ΔG is the Gibbs energy (J/mol), z is the charge number (unitless) of the sorbed species, F is the Faraday constant (96,485 C/mol), ψ is the potential (V), and subscripts tot and ads indicate total and chemical adsorption energy, respectively. Sorption is stronger when the Gibbs energy decreases. Thus, a counter-ion that carries a charge opposite to the surface charge tends to be sorbed electrostatically, while a co-ion that carries a charge with the same sign as the surface tends to be rejected.

PHREEQC has two models for surface complexation. One is based on the Dzombak and Morel (1990) database for complexation of heavy metal ions on hydrous ferric oxide (Hfo), or ferrihydrite. Ferrihydrite, like many other oxy-hydroxides, binds metals and protons on strong and weak sites and develops a charge depending on the ions sorbed. The model uses the Gouy-Chapman equation to relate surface charge and potential.

The other model is CD-MUSIC, which also can accommodate multiple surface sites. In addition, the charge, the potential, and even the sorbed species can be distributed over two additional planes in the double layer that extends from the surface into the free (electrically neutral) solution. The CD-MUSIC model has more options to fit experimental data and initially was developed for sorption on goethite, but has been applied to many metal-oxide surfaces. An example is given in the PHREEQC Help file, which is available by installing http://www.hydrochemistry.eu/phreeqc.chm.exe (accessed June 25, 2012).

Neither of the models considers that a charged surface, when centrifuged and separated from a solution, must have a shell of co- and counter-ions that compensates the surface charge in an electrical double layer (EDL). However, PHREEQC can integrate the concentrations in the diffuse layer ( -diffuse_layer ), or calculate the average concentrations with the Donnan option ( -Donnan ). It also is possible to ignore the electrostatic contribution by use of the identifier -no_edl . This non-electrostatic model does not consider the effects of the development of surface charge on the formation of surface complexes, with the result that surface complexes are treated mathematically, much like aqueous complexes.

The following example of the Gouy-Chapman model is taken from Dzombak and Morel (1990, chapter 8). Sorption of zinc on hydrous ferric oxide is simulated by using weak and strong sites on the oxide surface. Protons and zinc ions compete for the two types of binding sites, which is described by mass-action equations. The equations take into account the dependence of the activities of surface species on the potential at the surface; in turn, the potential at the surface is related to the surface charge by the Gouy-Chapman relation. The example considers the sorption of zinc on hydrous ferric oxides as a function of pH for low (10 -7 mol/kgw) and high (10 -4 mol/kgw) zinc concentration in 0.1 mol/kgw sodium nitrate electrolyte.

Three keyword data blocks are required to define surface-complexation data for a simulation: [SURFACE_MASTER_SPECIES](phreeqc3-53.htm#50593793_58106), [SURFACE_SPECIES](phreeqc3-54.htm#50593793_92844), and [SURFACE](phreeqc3-52.htm#50593793_56392). The [SURFACE_MASTER_SPECIES](phreeqc3-53.htm#50593793_58106) data block in the default database files defines a surface named “Hfo” (hydrous ferric oxides) with two binding sites. The name of a binding site is composed of a name for the surface, “Hfo”, optionally followed by an underscore and a lowercase binding site designation, here “Hfo_w” and “Hfo_s” for “weak” and “strong”. The underscore notation is necessary only for surfaces with two or more binding sites. The notation allows a mole-balance equation to be derived for each of the binding sites (Hfo_w and Hfo_s, in this example). The charges that develop on the two binding sites are summed, and the total is used to calculate the potential at the surface.

Surface-complexation reactions derived from the summary of Dzombak and Morel (1990) are defined by the [SURFACE_SPECIES](phreeqc3-54.htm#50593793_92844) in the default database files for PHREEQC. However, the intrinsic stability constants used in this example of Dzombak and Morel (1990, chapter 8) differ from these summary values, and are therefore specified explicitly with a [SURFACE_SPECIES](phreeqc3-54.htm#50593793_92844) data block in the input file ([table 27](phreeqc3-70.htm#50593807_31182)). The reactions are taken from Dzombak and Morel (1990, p. 259) and entered in the input file ([table 27](phreeqc3-70.htm#50593807_31182)). Note that the activity effect of the potential term is not included in the mass-action expression but is added internally by PHREEQC.

Table 27. Input file for example 8.

|  |
```phreeqc
TITLE Example 8.--Sorption of zinc on hydrous iron oxides.
```

|  |
```phreeqc
SURFACE_SPECIES
```

|  |
```phreeqc
     Hfo_sOH  + H+ = Hfo_sOH2+
```

|  |
```phreeqc
     log_k  7.18
```

|  |
```phreeqc
     Hfo_sOH = Hfo_sO- + H+
```

|  |
```phreeqc
     log_k  -8.82
```

|  |
```phreeqc
     Hfo_sOH + Zn+2 = Hfo_sOZn+ + H+
```

|  |
```phreeqc
     log_k  0.66
```

|  |
```phreeqc
     Hfo_wOH  + H+ = Hfo_wOH2+
```

|  |
```phreeqc
     log_k  7.18
```

|  |
```phreeqc
     Hfo_wOH = Hfo_wO- + H+
```

|  |
```phreeqc
     log_k  -8.82
```

|  |
```phreeqc
     Hfo_wOH + Zn+2 = Hfo_wOZn+ + H+
```

|  |
```phreeqc
     log_k  -2.32
```

|  |
```phreeqc
SURFACE 1
```

|  |
```phreeqc
     Hfo_sOH        5e-6    600.    0.09
```

|  |
```phreeqc
     Hfo_wOH        2e-4
```

|  |
```phreeqc
#     -Donnan
```

|  |
```phreeqc
END
```

|  |
```phreeqc
SOLUTION 1
```

|  |
```phreeqc
     -units  mmol/kgw
```

|  |
```phreeqc
     pH      8.0
```

|  |
```phreeqc
     Zn      0.0001
```

|  |
```phreeqc
     Na      100.    charge
```

|  |
```phreeqc
     N(5)    100.
```

|  |
```phreeqc
SELECTED_OUTPUT
```

|  |
```phreeqc
     -file Zn1e_7
```

|  |
```phreeqc
     -reset false
```

|  |
```phreeqc
USER_PUNCH
```

|  |
```phreeqc
  10 FOR i = 5.0 to 8 STEP 0.25
```

|  |
```phreeqc
  20 a$ = EOL$ + "USE solution 1" + CHR$(59) + " USE surface 1" + EOL$
```

|  |
```phreeqc
  30 a$ = a$ + "EQUILIBRIUM_PHASES 1" + EOL$
```

|  |
```phreeqc
  40 a$ = a$ + "   Fix_H+ " + STR$(-i) + " NaOH 10.0" + EOL$
```

|  |
```phreeqc
  50 a$ = a$ + "END" + EOL$
```

|  |
```phreeqc
  60 PUNCH a$
```

|  |
```phreeqc
  70 NEXT i
```

|  |
```phreeqc
END
```

|  |
```phreeqc
SOLUTION 2
```

|  |
```phreeqc
     -units  mmol/kgw
```

|  |
```phreeqc
     pH      8.0
```

|  |
```phreeqc
     Zn      0.1
```

|  |
```phreeqc
     Na      100.    charge
```

|  |
```phreeqc
     N(5)    100.
```

|  |
```phreeqc
SELECTED_OUTPUT
```

|  |
```phreeqc
     -file Zn1e_4
```

|  |
```phreeqc
     -reset false
```

|  |
```phreeqc
USER_PUNCH
```

|  |
```phreeqc
  10 FOR i = 5 to 8 STEP 0.25
```

|  |
```phreeqc
  20 a$ = EOL$ + "USE solution 2" + CHR$(59) + " USE surface 1" + EOL$
```

|  |
```phreeqc
  30 a$ = a$ + "EQUILIBRIUM_PHASES 1" + EOL$
```

|  |
```phreeqc
  40 a$ = a$ + "   Fix_H+ " + STR$(-i) + " NaOH 10.0" + EOL$
```

|  |
```phreeqc
  50 a$ = a$ + "END" + EOL$
```

|  |
```phreeqc
  60 PUNCH a$
```

|  |
```phreeqc
  70 NEXT i
```

|  |
```phreeqc
END
```

|  |
```phreeqc
#
```

|  |
```phreeqc
# Model definitions
```

|  |
```phreeqc
#
```

|  |
```phreeqc
PHASES
```

|  |
```phreeqc
     Fix_H+
```

|  |
```phreeqc
     H+ = H+
```

|  |
```phreeqc
     log_k  0.0
```

|  |
```phreeqc
END
```

|  |
```phreeqc
#
```

|  |
```phreeqc
#   Zn = 1e-7
```

|  |
```phreeqc
SELECTED_OUTPUT
```

|  |
```phreeqc
     -file ex8.sel
```

|  |
```phreeqc
     -reset true
```

|  |
```phreeqc
     -molalities     Zn+2    Hfo_wOZn+      Hfo_sOZn+
```

|  |
```phreeqc
USER_PUNCH
```

|  |
```phreeqc
 10
```

|  |
```phreeqc
USER_GRAPH 1 Example 8
```

|  |
```phreeqc
     -headings pH Zn_solute Zn_weak_sites Zn_strong_sites Charge_balance
```

|  |
```phreeqc
     -chart_title "Total Zn = 1e-7 molal"
```

|  |
```phreeqc
     -axis_titles pH "Moles per kilogram water" "Charge balance, in milliequivalents"
```

|  |
```phreeqc
     -axis_scale x_axis 5.0 8.0 1 0.25
```

|  |
```phreeqc
     -axis_scale y_axis 1e-11 1e-6 1 1 log
```

|  |
```phreeqc
     -axis_scale sy_axis -0.15 0 0.03
```

|  |
```phreeqc
  -start
```

|  |
```phreeqc
  10 GRAPH_X -LA("H+")
```

|  |
```phreeqc
  20 GRAPH_Y MOL("Zn+2"), MOL("Hfo_wOZn+"), MOL("Hfo_sOZn+")
```

|  |
```phreeqc
  30 GRAPH_SY CHARGE_BALANCE * 1e3
```

|  |
```phreeqc
  -end
```

|  |
```phreeqc
INCLUDE$ Zn1e_7
```

|  |
```phreeqc
END
```

|  |
```phreeqc
USER_GRAPH 1
```

|  |
```phreeqc
     -detach
```

|  |
```phreeqc
END
```

|  |
```phreeqc
#
```

|  |
```phreeqc
#   Zn = 1e-4
```

|  |
```phreeqc
USER_GRAPH 2 Example 8
```

|  |
```phreeqc
     -chart_title "Total Zn = 1e-4 molal"
```

|  |
```phreeqc
     -headings pH Zn_solute Zn_weak_sites Zn_strong_sites Charge_balance
```

|  |
```phreeqc
     -axis_titles pH "Moles per kilogram water" "Charge balance, in milliequivalents"
```

|  |
```phreeqc
     -axis_scale x_axis 5.0 8.0 1 0.25
```

|  |
```phreeqc
     -axis_scale y_axis 1e-8 1e-3 1 1 log
```

|  |
```phreeqc
     -axis_scale sy_axis -0.15 0 0.03
```

|  |
```phreeqc
  -start
```

|  |
```phreeqc
  10 GRAPH_X -LA("H+")
```

|  |
```phreeqc
  20 GRAPH_Y MOL("Zn+2"), MOL("Hfo_wOZn+"), MOL("Hfo_sOZn+")
```

|  |
```phreeqc
  30 GRAPH_SY CHARGE_BALANCE * 1e3
```

|  |
```phreeqc
  -end
```

|  |
```phreeqc
INCLUDE$ Zn1e_4
```

|  |
```phreeqc
END
```

The composition and other characteristics of an assemblage of surfaces are defined with the [SURFACE](phreeqc3-52.htm#50593793_56392) data block. For each surface, the moles of each type of site and the surface area must be defined. In the input file, all the surface sites initially are in the uncharged, protonated form. Alternatively, the surface can be initialized to be in equilibrium with a solution with -equilibrate solution_number. In both cases, the composition of the surfaces will vary with the extent of subsequent reactions.

The number of binding sites and surface areas may remain fixed or may vary if the surface is related to an equilibrium phase or a kinetic reaction. In this example, the number of strong binding sites (Hfo_s, 5×10 -6 mol) and of weak binding sites (Hfo_w, 2×10 -4 mol) remain fixed. With -sites_units density, the number of sites per nm2 (square nanometer) may be entered, instead of moles. The surface area must be defined with two numbers, the area per mass of surface material (here, 600 m 2 /g) and the total mass of surface material (here, 0.09 g). The use of these two numbers is traditional, but only the surface area obtained from the product of the numbers is used to determine the specific charge and the surface potential. The surface area may be entered with any of the binding sites for a surface; in [table 27](phreeqc3-70.htm#50593807_31182), the surface area is entered with Hfo_s.

Two sodium nitrate solutions are defined with different concentrations of zinc ([SOLUTION](phreeqc3-48.htm#50593793_30253) 1 and 2 data blocks), which can be recalled later in the run by [USE](phreeqc3-57.htm#50593793_78143) solution 1 or 2. Together with the definitions of these solutions, [USER_PUNCH](phreeqc3-60.htm#50593793_56415) is used to generate a PHREEQC input file, as explained in the next paragraph. A pseudo-phase, “Fix_H+” is defined with the [PHASES](phreeqc3-36.htm#50593793_84418) data block. This phase is not real, but is used in the batch-reaction simulations to fix the pH at specified values.

The remaining simulations in the input file equilibrate the surface with either solution 1 or solution 2 for pH values that range from 5 to 8. It is possible to use the [REACTION](phreeqc3-40.htm#50593793_75635) data block to add or remove varying amounts of NaOH from the solution in a single simulation, but the reaction increments will not produce evenly spaced pH values and the size of the reaction increments is not known beforehand. Alternatively, evenly spaced pH values can be obtained by using the phase “Fix_H+” in an [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) data block; the saturation indices correspond to the desired pH. A separate simulation is needed for each pH, illustrated here for pH = 5.

```phreeqc
USE solution 1
USE surface 1
EQUILIBRIUM_PHASES 1
   Fix_H+           -5 NaOH 10.0
END
```

Writing a similar set of data blocks for each pH is easy, but tedious. However, a shortcut is available. The simulations can be generated with a small Basic program in keyword [USER_PUNCH](phreeqc3-60.htm#50593793_56415) and punched to the files zn1e_7 and zn1e_4. The Basic program punches a string, a$, that contains the PHREEQC keywords and instructions for each pH, which is set by the FOR-loop variable i. EOL$ is a function that returns a new-line character. During the run, the files are inserted in the input file with [INCLUDE$](phreeqc3-18.htm#50593793_74991) zn1e_7 and [INCLUDE$](phreeqc3-18.htm#50593793_74991) zn1e_4.

NaOH is added or removed from each solution to produce the specified saturation index for “Fix_H+” or log activity of H+ (which is the negative of pH). However, a very low pH may not be attainable by removing all of the sodium from the solution. In this case HNO3 should be used as reactant instead of NaOH.[1](#pgfId-1445948)

The results of the simulation are plotted in figure 9 and are consistent with the results shown in Dzombak and Morel (1990, figure 8.9). Zinc is more strongly sorbed at high pH values than at low pH values. In addition, at low concentrations of zinc, the strong binding sites outcompete the weak binding sites for zinc over the entire pH range, and at high pH, most of the zinc resides at the strong binding sites. At larger zinc concentrations, the strong binding sites predominate only at low pH. Because all the strong binding sites become filled at higher pH, most of the zinc resides at the more numerous weak binding sites at high pH and large zinc concentrations.

There is one more point to be noted in figure 9. The charge balance of the solution, plotted on the secondary Y axis, becomes negative with decreasing pH because the surface sorbs protons from the solution. If the solution and surface are separated (for example by [TRANSPORT](phreeqc3-56.htm#50593793_87317) or by a [SAVE](phreeqc3-44.htm#50593793_81857) and subsequent [USE](phreeqc3-57.htm#50593793_78143)), the surface will keep its positive charge, and the solution its negative counter-charge. Such a separation of electrical charge is physically impossible. In reality, an electrical double layer exists on the surface that counterbalances the surface charge, and which remains with the surface when surface and solution are separated, thus keeping both of them electrically neutral. If the identifier -Donnan is added in keyword [SURFACE](phreeqc3-52.htm#50593793_56392), the composition of the electrical double layer is calculated and stored with each of the surfaces in the assemblage; this explicitly calculated electrical double layer makes each surface a neutral entity. In the input file this option (-Donnan) can be uncommented, resulting in a zero charge balance when the file is run again.

1. It is possible to let the program determine whether NaOH or HNO 3 should be added to attain a pH if an additional pseudo phase is defined. The following example attains a pH of 2 and 10 without specifying different alternate reactions for the phase Fix_H+.

PHASES

NaNO3

NaNO3 = Na+ + NO3-

log_K -20

Fix_H+

H+ = H+

log_K 0

END

SOLUTION 1

EQUILIBRIUM_PHASES

NaNO3 0 10

Fix_H+ -2 HNO3 10

Fix_H+ -12 HNO3 10
