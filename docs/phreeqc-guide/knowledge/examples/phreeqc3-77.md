---
title: "Example 15--1D Transport: Kinetic Biodegradation, Cell Growth, and Sorption"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-77.htm"
source_file: "phreeqc3-77.htm"
retrieved: 2026-09-22
category: example
---
# Example 15--1D Transport: Kinetic Biodegradation, Cell Growth, and Sorption

## Example 15--1D Transport: Kinetic Biodegradation, Cell Growth, and Sorption

A test problem for advective-dispersive-reactive transport was developed by Tebes-Stevens and Valocchi (1997) and Tebes-Stevens and others (1998). Although based on relatively simple speciation chemistry, the solution to the problem demonstrates several interacting chemical processes that are common to many environmental problems: bacterially mediated degradation of an organic substrate; bacterial cell growth and decay; metal sorption; and aqueous speciation, including metal-ligand complexation. In this example, the test problem is solved with PHREEQC, which produces results almost identical to those of Tebes-Stevens and Valocchi (1997) and Tebes-Stevens and others (1998).

The test problem models the transport processes when a pulse of water containing NTA (nitrylotriacetate) and cobalt is injected into a column. The problem includes advection and dispersion in the column, aqueous equilibrium reactions, and kinetic reactions for NTA degradation, growth of biomass, and cobalt sorption.

#### Transport Parameters

The dimensions and hydraulic properties of the column are given in [table 38](phreeqc3-77.htm#50593807_95408).

Table 38. Hydraulic and physical properties of the column in example 15.

[m, meter; g/m 3 , gram per cubic meter; g/L, gram per liter; m/h, meter per hour]

|  |
Property

|

Value

|  |
Length of column

- 10.0 m
|  |
Porosity, unitless

- 0.4
|  |
Bulk density

- 1.5e6 g/m 3
|  |
Grams of sediment per liter (from porosity and bulk density)

- 3.75e3 g/L
|  |
Pore-water velocity

- 1.0 m/h
|  |
Longitudinal dispersivity

- 0.05 m
#### Aqueous Model

Tebes-Stevens and Valocchi (1997) defined an aqueous model to be used for this test problem that includes the identity of the aqueous species and log K s of the species; activity coefficients were assumed to be 1.0. The database file in [table 39](phreeqc3-77.htm#50593807_31710) was constructed on the basis of their aqueous model. For the PHREEQC simulation, NTA was defined as a new “element” in the [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910) data block named “Nta”. From this point on “NTA” will be referred to as “Nta” for consistency with the PHREEQC notation. The gram formula weight of Nta in [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910) is immaterial if input units are moles in the [SOLUTION](phreeqc3-48.htm#50593793_30253) data block, and is simply set to 1. The aqueous complexes of Nta are defined in the [SOLUTION_SPECIES](phreeqc3-50.htm#50593793_96148) data block. Note that the activity coefficients of all aqueous species are defined with a large value for the a parameter (1×10 7 ) in the -gamma identifier, which forces the activity coefficients to be very nearly 1.0.

Table 39. Database for example 15.

|  |
```phreeqc
SOLUTION_MASTER_SPECIES
```

|  |
```phreeqc
C        CO2            2.0     61.0173         12.0111
```

|  |
```phreeqc
Cl       Cl-            0.0     Cl              35.453
```

|  |
```phreeqc
Co       Co+2           0.0     58.93           58.93
```

|  |
```phreeqc
E        e-             0.0     0.0             0.0
```

|  |
```phreeqc
H        H+             -1.     1.008           1.008
```

|  |
```phreeqc
H(0)     H2             0.0     1.008
```

|  |
```phreeqc
H(1)     H+             -1.     1.008
```

|  |
```phreeqc
N        NH4+           0.0     14.0067         14.0067
```

|  |
```phreeqc
Na       Na+            0.0     Na              22.9898
```

|  |
```phreeqc
Nta      Nta-3          3.0     1.              1.
```

|  |
```phreeqc
O        H2O            0.0     16.00           16.00
```

|  |
```phreeqc
O(-2)    H2O            0.0     18.016
```

|  |
```phreeqc
O(0)     O2             0.0     16.00
```

|  |
```phreeqc
SOLUTION_SPECIES
```

|  |
```phreeqc
2H2O = O2 + 4H+ + 4e-
```

|  |
```phreeqc
        log_k   -86.08; -gamma  1e7   0.0
```

|  |
```phreeqc
2 H+ + 2 e- = H2
```

|  |
```phreeqc
        log_k   -3.15;  -gamma  1e7   0.0
```

|  |
```phreeqc
H+ = H+
```

|  |
```phreeqc
        log_k   0.0;    -gamma  1e7   0.0
```

|  |
```phreeqc
e- = e-
```

|  |
```phreeqc
        log_k   0.0;    -gamma  1e7   0.0
```

|  |
```phreeqc
H2O = H2O
```

|  |
```phreeqc
        log_k   0.0;    -gamma  1e7   0.0
```

|  |
```phreeqc
CO2 = CO2
```

|  |
```phreeqc
        log_k   0.0;    -gamma  1e7   0.0
```

|  |
```phreeqc
Na+ = Na+
```

|  |
```phreeqc
        log_k   0.0;    -gamma  1e7   0.0
```

|  |
```phreeqc
Cl- = Cl-
```

|  |
```phreeqc
        log_k   0.0;    -gamma  1e7   0.0
```

|  |
```phreeqc
Co+2 = Co+2
```

|  |
```phreeqc
        log_k   0.0;    -gamma  1e7   0.0
```

|  |
```phreeqc
NH4+ = NH4+
```

|  |
```phreeqc
        log_k   0.0;    -gamma  1e7   0.0
```

|  |
```phreeqc
Nta-3 = Nta-3
```

|  |
```phreeqc
        log_k   0.0;    -gamma  1e7   0.0
```

|  |
```phreeqc
Nta-3 + 3H+ = H3Nta
```

|  |
```phreeqc
        log_k   14.9;   -gamma  1e7   0.0
```

|  |
```phreeqc
Nta-3 + 2H+ = H2Nta-
```

|  |
```phreeqc
        log_k   13.3;   -gamma  1e7   0.0
```

|  |
```phreeqc
Nta-3 + H+ = HNta-2
```

|  |
```phreeqc
        log_k   10.3;   -gamma  1e7   0.0
```

|  |
```phreeqc
Nta-3 + Co+2 = CoNta-
```

|  |
```phreeqc
        log_k   11.7;   -gamma  1e7   0.0
```

|  |
```phreeqc
2 Nta-3 + Co+2 = CoNta2-4
```

|  |
```phreeqc
        log_k   14.5;   -gamma  1e7   0.0
```

|  |
```phreeqc
Nta-3 + Co+2 + H2O = CoOHNta-2 + H+
```

|  |
```phreeqc
        log_k   0.5;    -gamma  1e7   0.0
```

|  |
```phreeqc
Co+2 + H2O = CoOH+ + H+
```

|  |
```phreeqc
        log_k   -9.7;   -gamma  1e7   0.0
```

|  |
```phreeqc
Co+2 + 2H2O = Co(OH)2 + 2H+
```

|  |
```phreeqc
        log_k   -22.9;  -gamma  1e7   0.0
```

|  |
```phreeqc
Co+2 + 3H2O = Co(OH)3- + 3H+
```

|  |
```phreeqc
        log_k   -31.5;  -gamma  1e7   0.0
```

|  |
```phreeqc
CO2 + H2O = HCO3- + H+
```

|  |
```phreeqc
        log_k   -6.35;  -gamma  1e7   0.0
```

|  |
```phreeqc
CO2 + H2O = CO3-2 + 2H+
```

|  |
```phreeqc
        log_k   -16.68; -gamma  1e7   0.0
```

|  |
```phreeqc
NH4+ = NH3 + H+
```

|  |
```phreeqc
        log_k   -9.3;   -gamma  1e7   0.0
```

|  |
```phreeqc
H2O = OH- +  H+
```

|  |
```phreeqc
        log_k   -14.0;  -gamma  1e7   0.0
```

|  |
```phreeqc
END
```

#### Initial and Boundary Conditions

The background concentrations in the column are listed in [table 40](phreeqc3-77.htm#50593807_84769). The column contains no Nta or cobalt initially, but has a biomass of 1.36×10 -4 g/L. A flux boundary condition is applied at the inlet of the column, and for the first 20 h (hours), a solution with Nta and cobalt enters the column; the concentrations in the pulse also are given in [table 40](phreeqc3-77.htm#50593807_84769). After 20 h, the background solution is introduced at the inlet until the experiment ends after 75 h. Na and Cl were not in the original problem definition but were added for charge balancing sorption reactions for PHREEQC (see [Sorption Reactions](phreeqc3-77.htm#50593807_53998)).

#### Kinetic Degradation of Nta and Cell Growth

Nta is assumed to degrade in the presence of biomass and oxygen by the reaction:

```phreeqc
HNta2-
 + 1.62O2
 + 1.272H2
O + 2.424H+
 = 0.576C5
H7
O2
N + 3.12H2
CO3
 + 0.424NH4
+
.
```

PHREEQC requires kinetic reactants to be defined solely by the moles of each element that enter or leave the solution because of the reaction. Furthermore, the reactants should be charge balanced (no net charge should enter or leave the solution). The Nta reaction converts 1 mol HNta 2- (C 6 H 7 O 6 N) to 0.576 mol C 5 H 7 O 2 N, where the latter is chemically inert, and its concentration can be ignored. The difference in elemental mass contained in these two reactants provides the stoichiometry of the elements C, H, O, and N in the reaction. This stoichiometry is equal to the sum of the elements on the right-hand side of the equation, excluding C 5 H 7 O 2 N, minus the sum of the elements on the left-hand side of the equation. The corresponding change in aqueous element concentrations per mole of HNta 2- reaction is given in [table 41](phreeqc3-77.htm#50593807_41892) (positive coefficients indicate an increase in aqueous concentration, and negative coefficients indicate a decrease in aqueous concentration).

Table 40. Concentration data for example 15.

[g/L, gram per liter; mol/L, mole per liter; Nta, nitrylotriacetate; ---, absent in pulse]

|  |
Constituent

Type

Pulse concentration

Background concentration

|  |
H +

Aqueous

- 10.0e-6 mol/L
- 10.0e-6 mol/L
|  |
Total C

- 4.9e-7 mol/L
- 4.9e-7 mol/L
|  |
NH 4 +

- 0.0
- 0.0
|  |
O 2

- 3.125e-5 mol/L
- 3.125e-5 mol/L
|  |
Nta 3 -

- 5.23e-6 mol/L
- 0.0
|  |
Co 2+

- 5.23e-6 mol/L
- 0.0
|  |
Na

- 1.0e-3 mol/L
- 1.0e-3 mol/L
|  |
Cl

- 1.0e-3 mol/L
- 1.0e-3 mol/L
|  |
Biomass

Immobile

###### ---

- 1.36e-4 g/L
|  |
CoNta (ads)

###### ---

- 0.0
|  |
Co (ads)

###### ---

- 0.0
Table 41. Reaction stoichiometry for oxidation of Nta (nitrylotriacetate).

|  |
Component

Coefficient

|  |
Nta

###### -1.0

|  |
C

###### 3.12

|  |
H

###### 1.968

|  |
O

###### 4.848

|  |
N

###### 0.424

The following multiplicative Monod rate expression is used to describe the rate of Nta degradation:

### , (30)

where is the rate of HNta 2- degradation (mol L -1 h -1 , mole per liter per hour), is the maximum specific rate of substrate utilization (mol/g cells/h), is the biomass (g L-1h-1, gram per liter per hour), is the half-saturation constant for the substrate Nta (mol/L), is the half-saturation constant for the electron acceptor O 2 (mol/L), and c indicates concentration (mol/L). The rate of biomass production is dependent on the rate of substrate utilization and a first-order decay rate for the biomass:

### , (31)

where is the rate of cell growth (g L-1h-1), Y is the microbial yield coefficient (g cells/mol Nta), and b is the first-order biomass decay coefficient (h -1 ). The parameter values for these equations are listed in [table 42](phreeqc3-77.htm#50593807_19932).

Table 42. Kinetic rate parameters used in example 15.

[mol, mole; L, liter; g, gram; h, hour]

|  |
Parameter

Description

Parameter value

|  |
K s

Half-saturation constant for donor

- 7.64e-7 mol/L
|  |
K a

Half-saturation constant for acceptor

- 6.25e-6 mol/L
|  |
q m

Maximum specific rate of substrate utilization

- 1.418e-3 mol Nta/g cells/h
|  |
Y

Microbial yield coefficient

- 65.14 g cells/mol Nta
|  |
b

First-order microbial decay coefficient

- 0.00208 h -1
#### Sorption Reactions

Tebes-Stevens and Valocchi (1997) defined kinetic sorption reactions for Co 2+ and CoNta - by the rate equation:

### , (32)

where i is either Co 2+ or CoNta - (mol/L), s i is the sorbed concentration (mol/g sediment), is the mass transfer coefficient (h -1 ), and is the distribution coefficient (L/g, liter per gram). The values of the coefficients are given in [table 43](phreeqc3-77.htm#50593807_32866). The values of K d were defined to give retardation coefficients of 20 and 3 for Co 2+ and CoNta - , respectively. Because the sorption reactions are defined to be kinetic, the initial moles of these reactants and the rates of reaction are defined with [KINETICS](phreeqc3-24.htm#50593793_55637) and [RATES](phreeqc3-39.htm#50593793_97907) data blocks; no surface definitions ([SURFACE](phreeqc3-52.htm#50593793_56392), [SURFACE_MASTER_SPECIES](phreeqc3-53.htm#50593793_58106), or [SURFACE_SPECIES](phreeqc3-54.htm#50593793_92844)) are needed. Furthermore, all kinetic reactants are immobile, so that the sorbed species are not transported.

Table 43. Sorption coefficients for Co 2+ and CoNta - .

[h, hour; L/g, liter per gram]

|  |
Species

k m

K d

|  |
###### 1 h -1

###### 5.07e-3 L/g

|  |
CoNta -

###### 1 h -1

###### 5.33e-4 L/g

When modeling with PHREEQC, kinetic reactants must be charge balanced. For sorption of Co 2+ and CoNta - , 1 mmol of NaCl was added to the solution definitions to have counter ions for the sorption process. The kinetic sorption reactions were then defined to remove or introduce (depending on the sign of the mole transfer) CoCl 2 and NaCoNta, which are charge balanced. To convert from moles sorbed per gram of sediment ( s i ) to moles sorbed per liter of water, it is necessary to multiply by the grams of sediment per liter of water, 3.75×10 3 g/L.

#### Input File

[See Input file for example 15.](phreeqc3-77.htm#50593807_34043) shows the input file derived from the preceding problem definition. Although rates have been given in units of mol L-1h-1, rates in PHREEQC are always mol/s (mole per second), and all rates have been adjusted to seconds in the definition of rate expressions in the input file. The density of water is assumed to be 1 kg/L.

Table 44. Input file for example 15.

|  |
```phreeqc
DATABASE ex15.dat
```

|  |
```phreeqc
TITLE Example 15.--1D Transport: Kinetic Biodegradation, Cell Growth, and Sorption
```

|  |
```phreeqc
***********
```

|  |
```phreeqc
PLEASE NOTE: This problem requires database file ex15.dat!!
```

|  |
```phreeqc
***********
```

|  |
```phreeqc
PRINT
```

|  |
```phreeqc
        -reset false
```

|  |
```phreeqc
        -echo_input true
```

|  |
```phreeqc
		-status false
```

|  |
```phreeqc
SOLUTION 0 Pulse solution with NTA and cobalt
```

|  |
```phreeqc
        units umol/L
```

|  |
```phreeqc
        pH      6
```

|  |
```phreeqc
        C       .49
```

|  |
```phreeqc
        O(0)    62.5
```

|  |
```phreeqc
        Nta     5.23
```

|  |
```phreeqc
        Co      5.23
```

|  |
```phreeqc
        Na      1000
```

|  |
```phreeqc
        Cl      1000
```

|  |
```phreeqc
SOLUTION 1-10 Background solution initially filling column
```

|  |
```phreeqc
        units umol/L
```

|  |
```phreeqc
        pH      6
```

|  |
```phreeqc
        C       .49
```

|  |
```phreeqc
        O(0)    62.5
```

|  |
```phreeqc
        Na      1000
```

|  |
```phreeqc
        Cl      1000
```

|  |
```phreeqc
COPY solution 0 100 # for use later on, and in
```

|  |
```phreeqc
COPY solution 1 101 # 20 cells model
```

|  |
```phreeqc
END
```

|  |
```phreeqc
RATES Rate expressions for the four kinetic reactions
```

|  |
```phreeqc
#
```

|  |
```phreeqc
        HNTA-2
```

|  |
```phreeqc
        -start
```

|  |
```phreeqc
10 Ks = 7.64e-7
```

|  |
```phreeqc
20 Ka = 6.25e-6
```

|  |
```phreeqc
30 qm = 1.407e-3/3600
```

|  |
```phreeqc
40 f1 = MOL("HNta-2")/(Ks + MOL("HNta-2"))
```

|  |
```phreeqc
50 f2 = MOL("O2")/(Ka + MOL("O2"))
```

|  |
```phreeqc
60 rate = -qm * KIN("Biomass") * f1 * f2
```

|  |
```phreeqc
70 moles = rate * TIME
```

|  |
```phreeqc
80 PUT(rate, 1)   # save the rate for use in Biomass rate calculation
```

|  |
```phreeqc
90 SAVE moles
```

|  |
```phreeqc
        -end
```

|  |
```phreeqc
#
```

|  |
```phreeqc
        Biomass
```

|  |
```phreeqc
        -start
```

|  |
```phreeqc
10 Y = 65.14
```

|  |
```phreeqc
20 b = 0.00208/3600
```

|  |
```phreeqc
30 rate = GET(1)  # uses rate calculated in HTNA-2 rate calculation
```

|  |
```phreeqc
40 rate = -Y*rate -b*M
```

|  |
```phreeqc
50 moles = -rate * TIME
```

|  |
```phreeqc
60 if (M + moles) < 0 then moles = -M
```

|  |
```phreeqc
70 SAVE moles
```

|  |
```phreeqc
        -end
```

|  |
```phreeqc
#
```

|  |
```phreeqc
        Co_sorption
```

|  |
```phreeqc
        -start
```

|  |
```phreeqc
10 km = 1/3600
```

|  |
```phreeqc
20 kd = 5.07e-3
```

|  |
```phreeqc
30 solids = 3.75e3
```

|  |
```phreeqc
40 rate = -km*(MOL("Co+2") - (M/solids)/kd)
```

|  |
```phreeqc
50 moles = rate * TIME
```

|  |
```phreeqc
60 if (M - moles) < 0 then moles = M
```

|  |
```phreeqc
70 SAVE moles
```

|  |
```phreeqc
        -end
```

|  |
```phreeqc
#
```

|  |
```phreeqc
        CoNta_sorption
```

|  |
```phreeqc
        -start
```

|  |
```phreeqc
10 km = 1/3600
```

|  |
```phreeqc
20 kd = 5.33e-4
```

|  |
```phreeqc
30 solids = 3.75e3
```

|  |
```phreeqc
40 rate = -km*(MOL("CoNta-") - (M/solids)/kd)
```

|  |
```phreeqc
50 moles = rate * TIME
```

|  |
```phreeqc
60 if (M - moles) < 0 then moles = M
```

|  |
```phreeqc
70 SAVE moles
```

|  |
```phreeqc
        -end
```

|  |
```phreeqc
KINETICS 1-10 Four kinetic reactions for all cells
```

|  |
```phreeqc
        HNTA-2
```

|  |
```phreeqc
                -formula C -3.12 H -1.968 O -4.848 N -0.424 Nta 1.
```

|  |
```phreeqc
        Biomass
```

|  |
```phreeqc
                -formula        H 0.0
```

|  |
```phreeqc
                -m              1.36e-4
```

|  |
```phreeqc
        Co_sorption
```

|  |
```phreeqc
                -formula CoCl2
```

|  |
```phreeqc
                -m      0.0
```

|  |
```phreeqc
                -tol 1e-11
```

|  |
```phreeqc
        CoNta_sorption
```

|  |
```phreeqc
                -formula NaCoNta
```

|  |
```phreeqc
                -m      0.0
```

|  |
```phreeqc
                -tol 1e-11
```

|  |
```phreeqc
COPY kinetics 1 101 # to use with 20 cells
```

|  |
```phreeqc
END
```

|  |
```phreeqc
SELECTED_OUTPUT
```

|  |
```phreeqc
        -file   ex15.sel
```

|  |
```phreeqc
        -mol    Nta-3 CoNta- HNta-2 Co+2
```

|  |
```phreeqc
USER_PUNCH
```

|  |
```phreeqc
        -headings        hours   Co_sorb CoNta_sorb      Biomass
```

|  |
```phreeqc
        -start
```

|  |
```phreeqc
  10 punch TOTAL_TIME/3600 + 3600/2/3600
```

|  |
```phreeqc
  20 punch KIN("Co_sorption")/3.75e3
```

|  |
```phreeqc
  30 punch KIN("CoNta_sorption")/3.75e3
```

|  |
```phreeqc
  40 punch KIN("Biomass")
```

|  |
```phreeqc
USER_GRAPH 1 Example 15
```

|  |
```phreeqc
        -headings 10_cells: Co+2 CoNTA- HNTA-2 pH
```

|  |
```phreeqc
        -chart_title "Kinetic Biodegradation, Cell Growth, and Sorption: Dissolved Species"
```

|  |
```phreeqc
        -axis_titles "Time, in hours" "Micromoles per kilogram water" "pH"
```

|  |
```phreeqc
        -axis_scale x_axis 0 75
```

|  |
```phreeqc
        -axis_scale y_axis 0 4
```

|  |
```phreeqc
        -axis_scale secondary_y_axis 5.799 6.8 0.2 0.1
```

|  |
```phreeqc
        -plot_concentration_vs t
```

|  |
```phreeqc
        -start
```

|  |
```phreeqc
  10 x = TOTAL_TIME/3600 + 3600/2/3600
```

|  |
```phreeqc
  20 PLOT_XY -1, -1, line_width = 0, symbol_size = 0
```

|  |
```phreeqc
  30 PLOT_XY x, MOL("Co+2") * 1e6, color = Red, line_width = 0, symbol_size = 4
```

|  |
```phreeqc
  40 PLOT_XY x, MOL("CoNta-") * 1e6, color = Green, line_width = 0, symbol_size = 4
```

|  |
```phreeqc
  50 PLOT_XY x, MOL("HNta-2") * 1e6, color = Blue, line_width = 0, symbol_size = 4
```

|  |
```phreeqc
  60 PLOT_XY x, -LA("H+"), y-axis = 2, color = Magenta, line_width = 0, symbol_size = 4
```

|  |
```phreeqc
        -end
```

|  |
```phreeqc
USER_GRAPH 2 Example 15
```

|  |
```phreeqc
        -headings 10_cells: Co+2 CoNTA- Biomass
```

|  |
```phreeqc
        -chart_title "Kinetic Biodegradation, Cell Growth, and Sorption: Sorbed Species"
```

|  |
```phreeqc
        -axis_titles "Time, in hours"  "Nanomoles per kilogram water" \
```

|  |
```phreeqc
             "Biomass, in milligrams per liter"
```

|  |
```phreeqc
        -axis_scale x_axis 0 75
```

|  |
```phreeqc
        -axis_scale y_axis 0 2
```

|  |
```phreeqc
        -axis_scale secondary_y_axis 0 0.4
```

|  |
```phreeqc
        -plot_concentration_vs t
```

|  |
```phreeqc
        -start
```

|  |
```phreeqc
  10 x = TOTAL_TIME/3600 + 3600/2/3600
```

|  |
```phreeqc
  20 PLOT_XY -1, -1, line_width = 0, symbol_size = 0
```

|  |
```phreeqc
  30 PLOT_XY x, KIN("Co_sorption") / 3.75e3 * 1e9, color = Red, line_width = 0, symbol_size = 4
```

|  |
```phreeqc
  40 PLOT_XY x, KIN("CoNta_sorption") / 3.75e3 * 1e9, color = Green, line_width = 0, \
```

|  |
```phreeqc
       symbol_size = 4
```

|  |
```phreeqc
  50 PLOT_XY x, KIN("Biomass") * 1e3, y-axis = 2, color = Magenta, line_width = 0, \
```

|  |
```phreeqc
       symbol_size = 4
```

|  |
```phreeqc
        -end          -end
```

|  |
```phreeqc
TRANSPORT First 20 hours have NTA and cobalt in infilling solution
```

|  |
```phreeqc
        -cells                10
```

|  |
```phreeqc
        -lengths              1
```

|  |
```phreeqc
        -shifts               20
```

|  |
```phreeqc
        -time_step            3600
```

|  |
```phreeqc
        -flow_direction       forward
```

|  |
```phreeqc
        -boundary_conditions  flux flux
```

|  |
```phreeqc
        -dispersivities       .05
```

|  |
```phreeqc
        -correct_disp         true
```

|  |
```phreeqc
        -diffusion_coefficient 0.0
```

|  |
```phreeqc
        -punch_cells          10
```

|  |
```phreeqc
        -punch_frequency      1
```

|  |
```phreeqc
        -print_cells          10
```

|  |
```phreeqc
        -print_frequency      5
```

|  |
|  |
```phreeqc
COPY solution 101 0 # initial column solution becomes influent
```

|  |
```phreeqc
END
```

|  |
```phreeqc
TRANSPORT Last 55 hours with background infilling solution
```

|  |
```phreeqc
        -shifts               55
```

|  |
```phreeqc
COPY cell 100 0 # for the 20 cell model...
```

|  |
```phreeqc
COPY cell 101 1-20
```

|  |
```phreeqc
END
```

|  |
```phreeqc
USER_PUNCH
```

|  |
```phreeqc
        -start
```

|  |
```phreeqc
  10 punch TOTAL_TIME/3600 + 3600/4/3600
```

|  |
```phreeqc
  20 punch KIN("Co_sorption")/3.75e3
```

|  |
```phreeqc
  30 punch KIN("CoNta_sorption")/3.75e3
```

|  |
```phreeqc
  40 punch KIN("Biomass")
```

|  |
```phreeqc
        -end
```

|  |
```phreeqc
USER_GRAPH 1
```

|  |
```phreeqc
        -headings 20_cells: Co+2 CoNTA- HNTA-2 pH
```

|  |
```phreeqc
        -start
```

|  |
```phreeqc
  10 x = TOTAL_TIME/3600 + 3600/4/3600
```

|  |
```phreeqc
  20 PLOT_XY -1, -1, line_width = 0, symbol_size = 0
```

|  |
```phreeqc
  30 PLOT_XY x, MOL("Co+2") * 1e6, color = Red, symbol_size = 0
```

|  |
```phreeqc
  40 PLOT_XY x, MOL("CoNta-") * 1e6, color = Green, symbol_size = 0
```

|  |
```phreeqc
  50 PLOT_XY x, MOL("HNta-2") * 1e6, color = Blue, symbol_size = 0
```

|  |
```phreeqc
  60 PLOT_XY x, -LA("H+"), y-axis = 2, color = Magenta, symbol_size = 0
```

|  |
```phreeqc
        -end
```

|  |
```phreeqc
USER_GRAPH 2
```

|  |
```phreeqc
        -headings 20_cells: Co+2 CoNTA- Biomass
```

|  |
```phreeqc
        -start
```

|  |
```phreeqc
  10 x = TOTAL_TIME/3600 + 3600/4/3600
```

|  |
```phreeqc
  20 PLOT_XY -1, -1, line_width = 0, symbol_size = 0
```

|  |
```phreeqc
  30 PLOT_XY x, KIN("Co_sorption") / 3.75e3 * 1e9, color = Red, symbol_size = 0
```

|  |
```phreeqc
  40 PLOT_XY x, KIN("CoNta_sorption") / 3.75e3 * 1e9, color = Green, symbol_size = 0
```

|  |
```phreeqc
  60 PLOT_XY x, KIN("Biomass") * 1e3, y-axis = 2, color = Magenta, symbol_size = 0
```

|  |
```phreeqc
        -end
```

|  |
```phreeqc
TRANSPORT First 20 hours have NTA and cobalt in infilling solution
```

|  |
```phreeqc
        -cells                20
```

|  |
```phreeqc
        -lengths              0.5
```

|  |
```phreeqc
        -shifts               40
```

|  |
```phreeqc
        -initial_time         0
```

|  |
```phreeqc
        -time_step            1800
```

|  |
```phreeqc
        -flow_direction       forward
```

|  |
```phreeqc
        -boundary_conditions  flux  flux
```

|  |
```phreeqc
        -dispersivities       .05
```

|  |
```phreeqc
        -correct_disp         true
```

|  |
```phreeqc
        -diffusion_coefficient 0.0
```

|  |
```phreeqc
        -punch_cells          20
```

|  |
```phreeqc
        -punch_frequency      2
```

|  |
```phreeqc
        -print_cells          20
```

|  |
```phreeqc
        -print_frequency      10
```

|  |
```phreeqc
COPY cell 101 0
```

|  |
```phreeqc
END
```

|  |
```phreeqc
TRANSPORT Last 55 hours with background infilling solution
```

|  |
```phreeqc
        -shifts               110
```

|  |
```phreeqc
END
```

The 10-meter column was discretized with 10 cells of 1 meter each. The first two [SOLUTION](phreeqc3-48.htm#50593793_30253) data blocks ([table 44](phreeqc3-77.htm#50593807_34043)) define the infilling solution and the initial solution in cells 1 through 10. The solutions are copied to solution 100 and 101, to be used later in the 20-cell model.

The [RATES](phreeqc3-39.htm#50593793_97907) data block defines the rate expressions for four kinetic reactions: HNta-2, Biomass, Co_sorption, and CoNta_sorption. The rate expressions are initiated with -start , defined with numbered Basic-language statements, and terminated with -end . The last statement of each expression is SAVE followed by a variable name. This variable is the number of moles of reaction over the time subinterval and is calculated from an instantaneous rate (mol/s) times the length of the time subinterval (s), which is given by the variable “TIME”. Lines 30 and 20 in the first and second rate expressions and line 10 in the third and fourth rate expressions adjust parameters to units of seconds from units of hours. The function “MOL” returns the concentration of a species (mol/kgw), the function “M” returns the moles of the reactant for which the rate expression is being calculated, and “KIN” returns the moles of the specified kinetic reactant. The functions “PUT” and “GET” are used to save and retrieve a term that is common to both the HNta-2 and Biomass rate expressions (see also [See Reaction-Path Calculations](phreeqc3-68.htm#50593807_49505)).

The [KINETICS](phreeqc3-24.htm#50593793_55637) data block defines the names of the rate expressions that apply to each cell; cells 1 through 10 are defined simultaneously in this example. For each rate expression that applies to a cell, the formula of the reactant ( -formula ) and the moles of the reactant initially present ( -m , if needed to be different from the default of 1 mol) are defined. It is also possible to define a tolerance ( -tol ), in moles, for the accuracy of the numerical integration for a rate expression. Note that the HNta-2 rate expression generates a negative rate, so that elements with positive coefficients in the formula are removed from solution and negative coefficients add elements to solution. The biomass reaction adds “H 0.0”, or zero moles of hydrogen; in other words, it does not add or remove anything from solution. The assimilation of carbon and nutrients that is associated with biomass growth is ignored in this simulation. Also, the kinetics block is copied to [KINETICS](phreeqc3-24.htm#50593793_55637) 101, for use in the 20-cell model.

The [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) data block punches the molalities of the aqueous species Nta-3, CoNta-, HNta-2 and Co+2 to the file ex15.sel . To each line in the file, the [USER_PUNCH](phreeqc3-60.htm#50593793_56415) data block appends the time (in hours), the sorbed concentrations converted to mol/g sediment, and the biomass. [USER_GRAPH](phreeqc3-58.htm#50593793_26121) plots the concentrations as symbols without lines to facilitate the comparison with the 20-cell model.

The first [TRANSPORT](phreeqc3-56.htm#50593793_87317) data block defines the first 20 h of the experiment, during which Nta and cobalt are added at the column inlet. The column is defined to have 10 cells ( -cells ) of length 1 m ( -lengths ). The duration of the advective-dispersive transport simulation is 20 time steps ( -shifts ) of 3,600 seconds ( -time_step ). The direction of flow is forward ( -flow_direction ). Each end of the column is defined to have a flux boundary condition ( -boundary_conditions ). The dispersivity is 0.05 m ( -dispersivities ) and the diffusion coefficient is set to zero ( -diffusion_coefficient ). Data are written to the selected-output file only for cell 10 ( -punch_cells ) after each shift ( -punch_frequency ), and data are written to the output file only for cell 10 ( -print_cells ) after each fifth shift ( -print_frequency ).

At the end of the first advective-dispersive transport simulation, the initial column solution, which was stored as [SOLUTION](phreeqc3-48.htm#50593793_30253) 101, is copied to [SOLUTION](phreeqc3-48.htm#50593793_30253) 0, to become the influent for the next transport simulation. The second [TRANSPORT](phreeqc3-56.htm#50593793_87317) data block defines the final 55 h of the experiment, during which Nta and cobalt are not present in the infilling solution. All parameters are the same as in the previous [TRANSPORT](phreeqc3-56.htm#50593793_87317) data block; only the number of transport steps ( -shifts ) is increased to 55.

#### Grid Convergence

With advective-dispersive-reactive transport simulations, it is always necessary to check the numerical accuracy of the results. In general, analytical solutions will not be available for these complex simulations, so the only test of numerical accuracy is to refine the grid and time step, rerun the simulation, and compare the results. If simulations on two different grids give similar results, there is some assurance that the numerical errors are relatively small. If simulations on two different grids give significantly different results, the grid must be refined again and the process repeated. Unfortunately, doubling the grid size at least quadruples the number of solution calculations that must be made because the number of cells doubles and the time step is halved. If the cell size approaches the size of the dispersivity, it may require even more solution calculations because the number of mix steps in the dispersion calculation will increase as well.

To test grid convergence in this example, the number of cells in the column were doubled. All keyword data blocks that defined compositions for the range 1 through 10 were changed to 1 through 20. In addition, the parameters for advective-dispersive transport were adjusted to be consistent with the new number of cells. The final [TRANSPORT](phreeqc3-56.htm#50593793_87317) data block in [table 44](phreeqc3-77.htm#50593807_34043) defines the 20-cell model. The number of cells and number of shifts are doubled; the cell length and time step are halved. To print information for the same location as the 10-cell model (the end of the column), the -punch_cells and -print_cells are set to cell 20. To print information at the same time in the simulation as the 10-cell model, -punch_frequency is set to every 2 shifts, -print_frequency is set to every 10 shifts, and the time step for going from the cell-midpoint to the column-end is halved on line 10 in [USER_PUNCH](phreeqc3-60.htm#50593793_56415).

#### Results

The distributions of aqueous and immobile constituents in the column at the end of 75 h are shown in figures [See Dissolved concentrations and pH values at the outlet of the column for Nta and cobalt transport simulations with 10 (symbols) and 20 cells (lines).](examples.htm#50593807_23955) and [See Concentrations of sorbed species and biomass at the outlet of the column for Nta and cobalt transport simulations with 10 (symbols) and 20 cells (lines).](examples.htm#50593807_18547) for the 10- and 20-cell models. In the experiment, two pore volumes of water with Nta and cobalt were introduced to the column over the first 20 h and then followed by 5.5 pore volumes of background water over the next 55 h. At 10 h, HNta 2- begins to appear at the column outlet along with a rise in the pH (fig. 16). If Nta and cobalt were conservative and dispersion were negligible, the graph would show square pulses that increase at 10 h and decrease at 30 h. However, the movement of the Nta and cobalt is retarded relative to conservative movement by the sorption reactions, and small concentrations arrive early because of dispersion. The peak in Nta and cobalt concentrations occurs in the CoNta - complex between 30 and 40 h. The peak in Co 2+ concentration is even more retarded by its sorption reaction and does not show up until near the end of the experiment.

In figure 17, solid-phase concentrations are plotted against time for concentrations in the last cell of the column. The sorbed CoNta - concentration peaks between 30 and 40 h and lags slightly behind the peak in the dissolved concentration of the CoNta - complex. Initially, no Nta is present in the column and the biomass decreases slightly over the first 10 h because of the first-order decay rate for the biomass. When the Nta moves through the cells, the biomass increases because the Nta becomes available as substrate for microbes. After the peak in Nta has moved through the column, biomass concentrations level off and then begin to decrease because of decay. The K d for cobalt sorption gives a greater retardation coefficient than the K d for CoNta - sorption, and the sorbed concentration of Co 2+ appears to be still increasing at the end of the experiment.

Both the 10-cell and the 20-cell models give similar results, which indicates that the numerical errors in the advective-dispersive transport simulation are relatively small; furthermore, the results are very similar to results given by Tebes-Stevens and Valocchi (1997) and Tebes-Stevens and others (1998). However, Tebes-Stevens and Valocchi (1997) included another part to their test problem that increased the rate constants for the sorption reactions from 1 to 1,000 h -1 . The increased rate constants generate a stiff set of partial differential equations, which are equations that describe processes that occur on very different time scales. The stiff problem, with very fast sorption reactions, proved intractable for the explicit Runge-Kutta algorithm, but can be solved with the -cvode algorithm. With -cvode, the calculation of the slow sorption column takes about four times longer than with Runge-Kutta and calculation of the fast sorption column is about six times longer than for slow sorption. Another way to solve the stiff problem is to introduce the fast kinetic sorption reaction as an equilibrium process, which constitutes instantaneous rates. However, even with equilibrium sorption, grid convergence was computationally much more intensive; it was necessary to use 100 cells or more to arrive at a satisfactory solution. As an estimate of relative CPU times, the 20-cell model took 2.7 times the CPU time of the 10-cell model. A 200-cell model took approximately 600 times the CPU time of the 10-cell model.
