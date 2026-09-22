---
title: "Example 14--Advective Transport, Cation Exchange, Surface Complexation, and Mineral Equilibria"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-76.htm"
source_file: "phreeqc3-76.htm"
retrieved: 2026-09-22
category: example
---
# Example 14--Advective Transport, Cation Exchange, Surface Complexation, and Mineral Equilibria

## Example 14--Advective Transport, Cation Exchange, Surface Complexation, and Mineral Equilibria

This example uses the phase-equilibrium, cation-exchange, and surface-complexation reaction capabilities of PHREEQC in combination with advective-transport capabilities to model the evolution of water in the Central Oklahoma aquifer. The geochemistry of the aquifer has been described by Parkhurst and others (1996). Two predominant water types occur in the aquifer: a calcium magnesium bicarbonate water with pH in the range of 7.0 to 7.5 in the unconfined part of the aquifer and a sodium bicarbonate water with pH in the range of 8.5 to 9.2 in the confined part of the aquifer. In addition, marine-derived sodium chloride brines exist below the aquifer and presumably in fluid inclusions and dead-end pore spaces within the aquifer. Large concentrations of arsenic, selenium, chromium, and uranium occur naturally within the aquifer. Arsenic is associated almost exclusively with the high-pH, sodium bicarbonate water type.

The conceptual model for the calculation of this example assumes that brines initially filled the aquifer. The aquifer contains calcite, dolomite, clays with cation-exchange capacity, and hydrous-ferric-oxide surfaces; initially, the cation exchanger and surfaces are in equilibrium with the brine. The aquifer is assumed to be recharged with rainwater that is concentrated by evaporation and equilibrates with calcite and dolomite in the vadose zone. This water then enters the saturated zone and reacts with calcite and dolomite in the presence of the cation exchanger and hydrous-ferric-oxide surfaces.

The calculations use the advective-transport capabilities of PHREEQC with just a single cell representing the saturated zone. A total of 200 pore volumes of recharge water are advected into the cell and, with each pore volume, the water is equilibrated with the minerals, cation exchanger, and the surfaces in the cell. The evolution of water chemistry in the cell represents the evolution of the water chemistry at a point near the top of the saturated zone of the aquifer.

#### Thermodynamic Data

The database wateq4f.dat contains thermodynamic data for the aqueous species of arsenic according to the compilation of Nordstrom and Archer (2003) and the surface complexation constants from Dzombak and Morel (1990). Unfortunately, these two sets of thermodynamic data are not internally consistent because the surface complexation constants were fit by using a different set of thermodynamic constants for arsenic aqueous species. To be consistent in the calculations, the thermodynamic data for both arsenic aqueous speciation and arsenic surface complexation are defined according to Dzombak and Morel (1990). The database phreeqc.dat was used for the calculations with the arsenic thermodynamic data defined with the [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910), [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_96148), [SURFACE_MASTER_SPECIES](phreeqc3-53.htm#50593793_58106), and [SURFACE_SPECIES](phreeqc3-54.htm#50593793_92844) data blocks within the input file.

#### Initial Conditions

Parkhurst and others (1996) provide data from which it is possible to estimate the moles of calcite, dolomite, and cation-exchange sites in the aquifer per liter of water. The weight percent ranges from 0 to 2 percent for calcite and 0 to 7 percent for dolomite, with dolomite much more abundant. Porosity is stated to be 0.22. Cation-exchange capacity for the clay ranges from 20 to 50 meq/100 g (milliequivalent per 100 grams), with an average clay content of 30 percent. For these example calculations, calcite was assumed to be present at 0.1 weight percent and dolomite, at 3 weight percent; by assuming a rock density of 2.7 kg/L, these percentages correspond to 0.1 mol/L for calcite and 1.6 mol/L for dolomite. The number of cation-exchange sites was estimated to be 1.0 eq/L.

The amount of arsenic on the surface was estimated from sequential extraction data on core samples (Mosier and others, 1991). Arsenic concentrations in the solid phases generally ranged from 10 to 20 ppm, which corresponds to 1.3 to 2.6 mmol/L arsenic. The number of surface sites were estimated from the amount of extractable iron in sediments, which ranged from 1.6 to 4.4 percent (Mosier and others, 1991). A content of 2 percent iron for the sediments corresponds to 3.4 mol/L of iron. However, most of the iron is in goethite and hematite, which have far fewer surface sites than hydrous ferric oxide. The fraction of iron in hydrous ferric oxide was arbitrarily assumed to be 0.1. Thus, a total of 0.34 mol of iron was assumed to be present as hydrous ferric oxide, and using a value of 0.2 for the number of sites per mole of iron, a total of 0.07 mol of sites per liter was used in the calculations. A gram formula weight of 89 g/mol was used to estimate that the mass of hydrous ferric oxide was 30 g/L (gram per liter). The specific surface area was assumed to be 600 m 2 /g.

The brine that initially fills the aquifer was taken from Parkhurst and others (1996) and is given as solution 1 in the input file for this example ([table 37](phreeqc3-76.htm#50593807_88386)). The pure-phase assemblage containing calcite and dolomite is defined with the [EQUILIBRIUM_PHASES](phreeqc3-13.htm#50593793_61207) 1 data block. The brine is first equilibrated with calcite and dolomite and saved again as solution 1 ([SAVE](phreeqc3-44.htm#50593793_81857) data block). The number of cation exchange sites is defined with [EXCHANGE](phreeqc3-14.htm#50593793_84573) 1 and the number of surface sites is defined with [SURFACE](phreeqc3-52.htm#50593793_56392) 1. The initial exchange and the initial surface composition are determined by equilibrium with the brine, after equilibration with calcite and dolomite (note that equilibration of exchangers and surfaces before mineral equilibration will yield different results because of buffering by the sorbed elements). The concentration of arsenic in the brine (0.025 μmol/kgw) was determined by trial and error to give a total of approximately 1.8 mmol arsenic on the surface, which is consistent with the sequential extraction data.

Table 37. Input file for example 14.

|  |
```phreeqc
TITLE Example 14.--Transport with equilibrium_phases, exchange, and surface reactions
```

|  |
```phreeqc
#
```

|  |
```phreeqc
# Use phreeqc.dat
```

|  |
```phreeqc
# Dzombak and Morel (1990) aqueous and surface complexation models for arsenic
```

|  |
```phreeqc
# are defined here
```

|  |
```phreeqc
#
```

|  |
```phreeqc
SURFACE_MASTER_SPECIES
```

|  |
```phreeqc
        Surf    SurfOH
```

|  |
```phreeqc
SURFACE_SPECIES
```

|  |
```phreeqc
        SurfOH = SurfOH
```

|  |
```phreeqc
                log_k   0.0
```

|  |
```phreeqc
        SurfOH  + H+ = SurfOH2+
```

|  |
```phreeqc
                log_k   7.29
```

|  |
```phreeqc
        SurfOH = SurfO- + H+
```

|  |
```phreeqc
                log_k   -8.93
```

|  |
```phreeqc
        SurfOH + AsO4-3 + 3H+ = SurfH2AsO4 + H2O
```

|  |
```phreeqc
                log_k   29.31
```

|  |
```phreeqc
        SurfOH + AsO4-3 + 2H+ = SurfHAsO4- + H2O
```

|  |
```phreeqc
                log_k   23.51
```

|  |
```phreeqc
        SurfOH + AsO4-3 = SurfOHAsO4-3
```

|  |
```phreeqc
                log_k   10.58
```

|  |
```phreeqc
SOLUTION_MASTER_SPECIES
```

|  |
```phreeqc
        As       H3AsO4        -1.0     74.9216    74.9216
```

|  |
```phreeqc
SOLUTION_SPECIES
```

|  |
```phreeqc
        H3AsO4 = H3AsO4
```

|  |
```phreeqc
                log_k           0.0
```

|  |
```phreeqc
        H3AsO4 = AsO4-3 + 3H+
```

|  |
```phreeqc
                log_k   -20.7
```

|  |
```phreeqc
        H+ + AsO4-3 = HAsO4-2
```

|  |
```phreeqc
                log_k   11.50
```

|  |
```phreeqc
        2H+ + AsO4-3 = H2AsO4-
```

|  |
```phreeqc
                log_k           18.46
```

|  |
```phreeqc
SOLUTION 1 Brine
```

|  |
```phreeqc
        pH      5.713
```

|  |
```phreeqc
        pe      4.0     O2(g)   -0.7
```

|  |
```phreeqc
        temp    25.
```

|  |
```phreeqc
        units   mol/kgw
```

|  |
```phreeqc
        Ca      .4655
```

|  |
```phreeqc
        Mg      .1609
```

|  |
```phreeqc
        Na      5.402
```

|  |
```phreeqc
        Cl      6.642           charge
```

|  |
```phreeqc
        C       .00396
```

|  |
```phreeqc
        S       .004725
```

|  |
```phreeqc
        As      .025 umol/kgw
```

|  |
```phreeqc
END
```

|  |
```phreeqc
USE solution 1
```

|  |
```phreeqc
EQUILIBRIUM_PHASES 1
```

|  |
```phreeqc
        Dolomite        0.0     1.6
```

|  |
```phreeqc
        Calcite         0.0     0.1
```

|  |
```phreeqc
SAVE solution 1
```

|  |
```phreeqc
# prints initial condition to the selected-output file
```

|  |
```phreeqc
SELECTED_OUTPUT
```

|  |
```phreeqc
        -file ex14.sel
```

|  |
```phreeqc
        -reset false
```

|  |
```phreeqc
        -step
```

|  |
```phreeqc
USER_PUNCH
```

|  |
```phreeqc
        -head  m_Ca m_Mg m_Na umol_As pH mmol_sorbedAs
```

|  |
```phreeqc
  10 PUNCH TOT("Ca"), TOT("Mg"), TOT("Na"), TOT("As")*1e6, -LA("H+"), SURF("As", "Surf")*1000
```

|  |
```phreeqc
END
```

|  |
```phreeqc
PRINT
```

|  |
```phreeqc
# skips print of initial exchange and initial surface to the selected-output file
```

|  |
```phreeqc
        -selected_out false
```

|  |
```phreeqc
EXCHANGE 1
```

|  |
```phreeqc
        -equil with solution 1
```

|  |
```phreeqc
        X       1.0
```

|  |
```phreeqc
SURFACE 1
```

|  |
```phreeqc
        -equil solution 1
```

|  |
```phreeqc
# assumes 1/10 of iron is HFO
```

|  |
```phreeqc
        SurfOH           0.07    600.    30.
```

|  |
```phreeqc
END
```

|  |
```phreeqc
SOLUTION 0 20 x precipitation
```

|  |
```phreeqc
        pH      4.6
```

|  |
```phreeqc
        pe      4.0     O2(g)   -0.7
```

|  |
```phreeqc
        temp    25.
```

|  |
```phreeqc
        units   mmol/kgw
```

|  |
```phreeqc
        Ca      .191625
```

|  |
```phreeqc
        Mg      .035797
```

|  |
```phreeqc
        Na      .122668
```

|  |
```phreeqc
        Cl      .133704
```

|  |
```phreeqc
        C       .01096
```

|  |
```phreeqc
        S       .235153         charge
```

|  |
```phreeqc
EQUILIBRIUM_PHASES 0
```

|  |
```phreeqc
        Dolomite        0.0     1.6
```

|  |
```phreeqc
        Calcite         0.0     0.1
```

|  |
```phreeqc
        CO2(g)          -1.5    10.
```

|  |
```phreeqc
SAVE solution 0
```

|  |
```phreeqc
END
```

|  |
```phreeqc
PRINT
```

|  |
```phreeqc
        -selected_out true
```

|  |
```phreeqc
		-status false
```

|  |
```phreeqc
ADVECTION
```

|  |
```phreeqc
        -cells 1
```

|  |
```phreeqc
        -shifts 200
```

|  |
```phreeqc
        -print_frequency 200
```

|  |
```phreeqc
USER_GRAPH 1 Example 14
```

|  |
```phreeqc
        -headings PV As(ppb) Ca(M) Mg(M) Na(M) pH
```

|  |
```phreeqc
        -chart_title "Chemical Evolution of the Central Oklahoma Aquifer"
```

|  |
```phreeqc
        -axis_titles "Pore volumes or shift number" "Log(Concentration, in ppb or molal)" "pH"
```

|  |
```phreeqc
        -axis_scale x_axis 0 200
```

|  |
```phreeqc
        -axis_scale y_axis 1e-6 100 auto auto Log
```

|  |
```phreeqc
  10 GRAPH_X STEP_NO
```

|  |
```phreeqc
  20 GRAPH_Y TOT("As") * 74.92e6, TOT("Ca"), TOT("Mg"), TOT("Na")
```

|  |
```phreeqc
  30 GRAPH_SY -LA("H+")
```

|  |
```phreeqc
END
```

#### Recharge Water

The water entering the saturated zone of the aquifer was assumed to be in equilibrium with calcite and dolomite at a vadose-zone of 10 -1.5 atm. The fourth simulation in the input set (the simulation following the third [END](phreeqc3-12.htm#50593793_63178) statement) generates this water composition and stores it as solution 0 by using [SAVE](phreeqc3-44.htm#50593793_81857) ([table 37](phreeqc3-76.htm#50593807_88386)).

#### Advective-Transport Calculations

The [ADVECTION](phreeqc3-6.htm#50593793_87438) data block ([table 37](phreeqc3-76.htm#50593807_88386)) provides the necessary information to advect the recharge water into the cell representing the saturated zone. A total of 200 shifts is specified, which is equivalent to 200 pore volumes because only a single cell is used in this calculation.

The results of the calculations are plotted in figure 15. During the initial five pore volumes, the high concentrations of sodium, calcium, and magnesium decrease such that sodium is the dominant cation and calcium and magnesium concentrations are small. The pH increases to more than 9.0 and arsenic concentrations increase to approximately 100 ppb. Over the next 45 pore volumes, the pH gradually decreases, and the arsenic concentrations decrease to negligible concentrations. At about 100 pore volumes, the calcium and magnesium become the dominant cations, and the pH stabilizes at the pH of the infilling recharge water.

The advective-transport calculations produce three types of water that are similar to water types observed in the aquifer: the initial brine, a sodium bicarbonate water, and a calcium and magnesium bicarbonate water. The calculated pH values are consistent with observations of aquifer water. In the sodium dominated waters, the calculated pH is generally greater than 8.0 and sometimes greater than 9.0; in the calcium magnesium bicarbonate waters, the pH is slightly greater than 7.0. Sensitivity calculations indicate that the maximum pH depends on the amount of exchanger present. Decreasing the number of cation exchange sites decreases the maximum pH. Simulated arsenic concentrations are similar to values observed in the aquifer, where the maximum concentrations are from 75 to 150 ppb. Lower maximum pH values produce lower maximum arsenic concentrations. The stability constant for the surface complexation reactions have been taken directly from the literature; a decrease in the log K for the predominant arsenic complexation reaction tends to decrease the maximum arsenic concentration as well. In conclusion, the model results, which were based largely on measured values and literature thermodynamic data, can explain the trends in major ion chemistry, pH, and arsenic concentrations within the aquifer.
