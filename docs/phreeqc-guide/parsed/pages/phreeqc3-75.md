---
title: "Example 13--1D Transport in a Dual Porosity Column With Cation Exchange"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-75.htm"
source_file: "phreeqc3-75.htm"
retrieved: 2026-09-22
category: example
---
# Example 13--1D Transport in a Dual Porosity Column With Cation Exchange

## Example 13--1D Transport in a Dual Porosity Column With Cation Exchange

This example demonstrates the capabilities of PHREEQC to calculate flow in a dual-porosity medium with diffusive exchange among the mobile and immobile pores. The flexible input format and the modular definition of additional solutions and reactants in PHREEQC allow inclusion of heterogeneities and various complexities within a 1D column. This example considers a column filled with small clay beads of 2 cm diameter, which act as dual porosity or stagnant zones. Both the first-order exchange approximation and finite differences are applied in this example, and transport of both a conservative and a retarded (by ion exchange) chemical is considered. It is furthermore shown how a heterogeneous column can be modeled by prescribing mixing factors to account for diffusion between mobile and immobile cells with the keyword [MIX](phreeqc3-27.htm#50593793_23725).

#### Stagnant Zone Calculation Using the First-Order Exchange Approximation With Implicit Mixing Factors

The first example input file, example 13A ([table 33](phreeqc3-75.htm#50593807_69841)), is for a column with a uniform distribution of the stagnant porosity along the column. The 20 mobile cells are numbered 1 through 20. Each mobile cell, n , exchanges with one immobile cell, which is numbered 20 + 1 + n (cells 22 through 41 are immobile cells). All cells are given an identical initial solution and exchange complex, but these could be defined individually for each cell. It also is possible to distribute the immobile cells over the column non-uniformly, simply by omitting solutions for the stagnant cells that are not present. The connections between the mobile-zone and the stagnant-zone cells and among stagnant-zone cells can be varied along the column as well, but this requires that mixing factors among the mobile and immobile cells are prescribed by using the keyword [MIX](phreeqc3-27.htm#50593793_23725).

As defined in [table 33](phreeqc3-75.htm#50593807_69841), the column initially contains a 1 mmol/L KNO 3 solution in both the mobile and the stagnant zones ([SOLUTION](phreeqc3-48.htm#50593793_30253) 1-41). An NaCl-NO 3 solution flows into the column ([SOLUTION](phreeqc3-48.htm#50593793_30253) 0). An exchange complex with 1 mmol of sites is defined for each cell ([EXCHANGE](phreeqc3-14.htm#50593793_84573) 1-41), and exchange coefficients are specified to give linear retardation R = 2 for Na+ ([EXCHANGE_SPECIES](phreeqc3-16.htm#50593793_65476)). The first [TRANSPORT](phreeqc3-56.htm#50593793_87317) data block is used to define the physical and flow characteristics of the first transport simulation. The column is 2 m in length and is discretized in 20 cells ( -cells ) of 0.1 m ( -lengths ). A pulse of five shifts ( -shifts ) of the infilling solution ([SOLUTION](phreeqc3-48.htm#50593793_30253) 0) is introduced into the column. The length of time for each shift is 3,600 s ( -time_step ), which results in a velocity in the mobile pores vm = 0.1 / 3,600 = 2.78×10 -5 m/s. The dispersivity is set to 0.015 m for all cells ( -dispersivities ). The diffusion coefficient is set to 0.0 ( -diffusion_coefficient ).

The stagnant/mobile interchange is defined by using the first-order exchange approximation. The stagnant zone consists of spheres with radius r = 0.01 m, diffusion coefficient De = 3.×10 -10 m 2 /s, and shape factor fs ®1 = 0.21 (Parkhurst and Appelo, 1999, “Transport in Dual Porosity Media”, table 1). These variables give an exchange factor α = 6.8×10 -6 s -1 . Mobile porosity is εm = 0.3 ( -stagnant ) and immobile porosity εim = 0.1. For the first-order exchange approximation in PHREEQC, a single cell immobile zone and the parameters α, εm and εim are specified with -stagnant . This stagnant zone definition causes each cell in the mobile zone (numbered 1 through 20) to have an associated cell in the immobile zone (numbered 22 through 41). The [PRINT](phreeqc3-38.htm#50593793_92102) data block is used to eliminate all printing to the output file.

Following the pulse of NaCl solution, 10 shifts of 1 mmol KNO 3 /L (second [SOLUTION](phreeqc3-48.htm#50593793_30253) 0) are introduced into the column. The second [TRANSPORT](phreeqc3-56.htm#50593793_87317) data block does not redefine any of the column or flow characteristics, but specifies that results for cells 1 through 20 ( -punch_cells ) be written to the selected output file after 10 shifts ( -punch_frequency ). The data blocks [SELECTED_OUTPUT](phreeqc3-45.htm#50593793_20239) and [USER_PUNCH](phreeqc3-60.htm#50593793_56415) specify the data to be written to the selected-output file, and [USER_GRAPH](phreeqc3-58.htm#50593793_26121) plots the same data.

Table 33. Input file for example 13A: Stagnant zone with implicitly defined mixing factors.

|  |
```phreeqc
TITLE Example 13A.--1 mmol/L NaCl/NO3 enters column with stagnant zones.
```

|  |
```phreeqc
                    Implicit definition of first-order exchange model.
```

|  |
```phreeqc
SOLUTION 0    # 1 mmol/L NaCl
```

|  |
```phreeqc
   units   mmol/l
```

|  |
```phreeqc
   pH       7.0
```

|  |
```phreeqc
   pe      13.0    O2(g)   -0.7
```

|  |
```phreeqc
   Na       1.0    # Na has Retardation = 2
```

|  |
```phreeqc
   Cl       1.0    # Cl has Retardation = 1, stagnant exchange
```

|  |
```phreeqc
   N(5)     1.0    # NO3 is conservative
```

|  |
```phreeqc
#       charge imbalance is no problem ...
```

|  |
```phreeqc
END
```

|  |
```phreeqc
SOLUTION 1-41  # Column with KNO3
```

|  |
```phreeqc
   units   mmol/l
```

|  |
```phreeqc
   pH       7.0
```

|  |
```phreeqc
   pe      13.0   O2(g)    -0.7
```

|  |
```phreeqc
   K        1.0
```

|  |
```phreeqc
   N(5)     1.0
```

|  |
```phreeqc
EXCHANGE_SPECIES # For linear exchange, make KX exch. coeff. equal to NaX
```

|  |
```phreeqc
   K+ + X- = KX
```

|  |
```phreeqc
   log_k   0.0
```

|  |
```phreeqc
   -gamma  3.5     0.015
```

|  |
```phreeqc
EXCHANGE 1-41
```

|  |
```phreeqc
   -equil  1
```

|  |
```phreeqc
   X       1.e-3
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
TRANSPORT
```

|  |
```phreeqc
   -cells  20
```

|  |
```phreeqc
   -shifts 5
```

|  |
```phreeqc
   -flow_direction  forward
```

|  |
```phreeqc
   -time_step       3600
```

|  |
```phreeqc
   -boundary_conditions   flux  flux
```

|  |
```phreeqc
   -diffusion_coefficient 0.0
```

|  |
```phreeqc
   -lengths         0.1
```

|  |
```phreeqc
   -dispersivities  0.015
```

|  |
```phreeqc
   -stagnant   1  6.8e-6  0.3        0.1
```

|  |
```phreeqc
#   1 stagnant layer^, ^alpha, ^epsil(m), ^epsil(im)
```

|  |
```phreeqc
END
```

|  |
```phreeqc
SOLUTION 0  # Original solution with KNO3 reenters
```

|  |
```phreeqc
   units   mmol/l
```

|  |
```phreeqc
   pH       7.0
```

|  |
```phreeqc
   pe      13.0   O2(g)    -0.7
```

|  |
```phreeqc
   K        1.0
```

|  |
```phreeqc
   N(5)     1.0
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
   -file   ex13a.sel
```

|  |
```phreeqc
   -reset  false
```

|  |
```phreeqc
   -solution
```

|  |
```phreeqc
   -distance       true
```

|  |
```phreeqc
USER_PUNCH
```

|  |
```phreeqc
   -headings Cl_mmol Na_mmol
```

|  |
```phreeqc
  10 PUNCH TOT("Cl")*1000, TOT("Na")*1000
```

|  |
```phreeqc
TRANSPORT
```

|  |
```phreeqc
   -shifts 10
```

|  |
```phreeqc
   -punch_cells        1-20
```

|  |
```phreeqc
   -punch_frequency    10
```

|  |
```phreeqc
USER_GRAPH 1 Example 13A
```

|  |
```phreeqc
   -headings Distance Na Cl
```

|  |
```phreeqc
   -chart_title "Dual Porosity, First-Order Exchange with Implicit Mixing Factors"
```

|  |
```phreeqc
   -axis_titles "Distance, in meters" "Millimoles per kilogram water"
```

|  |
```phreeqc
   -axis_scale x_axis 0 2
```

|  |
```phreeqc
   -axis_scale y_axis 0 0.8
```

|  |
```phreeqc
   -plot_concentration_vs x
```

|  |
```phreeqc
   -start
```

|  |
```phreeqc
  10 GRAPH_X DIST
```

|  |
```phreeqc
  20 GRAPH_Y TOT("Na")*1000 TOT("Cl")*1000
```

|  |
```phreeqc
  -end
```

|  |
```phreeqc
END
```

The mixing factors mixfm and mixfim for the first-order exchange approximation for this example are as follows (Parkhurst and Appelo, 1999, equations 121 and 123):

### (24)

where t is the time step, and

### . (25)

The retardation factors R m and R im do not appear in the formulas for mixf im and mixf m because in PHREEQC, the retardation is a consequence of chemical reactions. According to equations [24](phreeqc3-75.htm#50593807_27886) and [25](phreeqc3-75.htm#50593807_24559), for this example, the mixing factors are calculated to be mixfim = 0.20886 and mixfm = 0.06962. The mixing factors differ for the mobile cell and the immobile cell to account for the different volumes of mobile and immobile water.

In PHREEQC, a mixing of mobile and stagnant water is done after each diffusion/dispersion step. This means that the time step decreases when the cells are made smaller and when more diffusive steps (“mixruns”) are performed. A 20-cell model as in [table 33](phreeqc3-75.htm#50593807_69841) has one mixrun. A 100-cell model would have three mixruns, and the time step for calculating mixfim would be (3,600/5) / 3 = 240 s. A time step t = 240 s leads to mixfim = 0.01614 in the 100-cell model.

#### Stagnant Zone Calculation Using the First-Order Exchange Approximation With Explicit Mixing Factors

The input file with explicit mixing factors for a uniform distribution of the stagnant zones is given in [table 34](phreeqc3-75.htm#50593807_94576). The [SOLUTION](phreeqc3-48.htm#50593793_30253) data blocks are identical to the previous input file ([table 33](phreeqc3-75.htm#50593807_69841)). One stagnant layer without further information is defined (-stagnant 1, in the [TRANSPORT](phreeqc3-56.htm#50593793_87317) data block). The mobile/immobile exchange is set by the mix fraction given in the [MIX](phreeqc3-27.htm#50593793_23725) data blocks. The results of this input file are identical with the results from the previous input file in which the shortcut notation was used. However, the explicit definition of mix factors illustrates that a non-uniform distribution of the stagnant zones, or other physical properties of the stagnant zone, can be included in PHREEQC simulations by varying the mixing fractions that define the exchange among mobile and immobile cells.

Table 34. Input file for example 13B: Stagnant zone with explicitly defined mixing factors.

|  |
```phreeqc
TITLE Example 13B.--1 mmol/l NaCl/NO3 enters column with stagnant zones.
```

|  |
```phreeqc
                    Explicit definition of first-order exchange factors.
```

|  |
```phreeqc
SOLUTION 0    # 1 mmol/l NaCl
```

|  |
```phreeqc
   units   mmol/l
```

|  |
```phreeqc
   pH       7.0
```

|  |
```phreeqc
   pe      13.0    O2(g)   -0.7
```

|  |
```phreeqc
   Na       1.0    # Na has Retardation = 2
```

|  |
```phreeqc
   Cl       1.0    # Cl has Retardation = 1, stagnant exchange
```

|  |
```phreeqc
   N(5)     1.0    # NO3 is conservative
```

|  |
```phreeqc
#       charge imbalance is no problem ...
```

|  |
```phreeqc
END
```

|  |
```phreeqc
SOLUTION 1-41  # Column with KNO3
```

|  |
```phreeqc
   units   mmol/l
```

|  |
```phreeqc
   pH       7.0
```

|  |
```phreeqc
   pe      13.0   O2(g)    -0.7
```

|  |
```phreeqc
   K        1.0
```

|  |
```phreeqc
   N(5)     1.0
```

|  |
```phreeqc
EXCHANGE_SPECIES # For linear exchange, make KX exch. coeff. equal to NaX
```

|  |
```phreeqc
   K+ + X- = KX
```

|  |
```phreeqc
   log_k   0.0
```

|  |
```phreeqc
   -gamma  3.5     0.015
```

|  |
```phreeqc
EXCHANGE 1-41
```

|  |
```phreeqc
   -equil  1
```

|  |
```phreeqc
   X       1.e-3
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
MIX  1;  1 .93038;      22 .06962       ;MIX  2;         2 .93038;      23 .06962;
```

|  |
```phreeqc
MIX  3;  3 .93038;      24 .06962       ;MIX  4;         4 .93038;      25 .06962;
```

|  |
```phreeqc
MIX  5;  5 .93038;      26 .06962       ;MIX  6;         6 .93038;      27 .06962;
```

|  |
```phreeqc
MIX  7;  7 .93038;      28 .06962       ;MIX  8;         8 .93038;      29 .06962;
```

|  |
```phreeqc
MIX  9;  9 .93038;      30 .06962       ;MIX 10;        10 .93038;      31 .06962;
```

|  |
```phreeqc
MIX 11; 11 .93038;      32 .06962       ;MIX 12;        12 .93038;      33 .06962;
```

|  |
```phreeqc
MIX 13; 13 .93038;      34 .06962       ;MIX 14;        14 .93038;      35 .06962;
```

|  |
```phreeqc
MIX 15; 15 .93038;      36 .06962       ;MIX 16;        16 .93038;      37 .06962;
```

|  |
```phreeqc
MIX 17; 17 .93038;      38 .06962       ;MIX 18;        18 .93038;      39 .06962;
```

|  |
```phreeqc
MIX 19; 19 .93038;      40 .06962       ;MIX 20;        20 .93038;      41 .06962;
```

|  |
```phreeqc
#
```

|  |
```phreeqc
MIX 22;  1 .20886;      22 .79114       ;MIX 23;         2 .20886;      23 .79114;
```

|  |
```phreeqc
MIX 24;  3 .20886;      24 .79114       ;MIX 25;         4 .20886;      25 .79114;
```

|  |
```phreeqc
MIX 26;  5 .20886;      26 .79114       ;MIX 27;         6 .20886;      27 .79114;
```

|  |
```phreeqc
MIX 28;  7 .20886;      28 .79114       ;MIX 29;         8 .20886;      29 .79114;
```

|  |
```phreeqc
MIX 30;  9 .20886;      30 .79114       ;MIX 31;        10 .20886;      31 .79114;
```

|  |
```phreeqc
MIX 32; 11 .20886;      32 .79114       ;MIX 33;        12 .20886;      33 .79114;
```

|  |
```phreeqc
MIX 34; 13 .20886;      34 .79114       ;MIX 35;        14 .20886;      35 .79114;
```

|  |
```phreeqc
MIX 36; 15 .20886;      36 .79114       ;MIX 37;        16 .20886;      37 .79114;
```

|  |
```phreeqc
MIX 38; 17 .20886;      38 .79114       ;MIX 39;        18 .20886;      39 .79114;
```

|  |
```phreeqc
MIX 40; 19 .20886;      40 .79114       ;MIX 41;        20 .20886;      41 .79114;
```

|  |
```phreeqc
TRANSPORT
```

|  |
```phreeqc
   -cells  20
```

|  |
```phreeqc
   -shifts 5
```

|  |
```phreeqc
   -flow_direction  forward
```

|  |
```phreeqc
   -time_step       3600
```

|  |
```phreeqc
   -boundary_conditions   flux  flux
```

|  |
```phreeqc
   -diffusion_coefficient 0.0
```

|  |
```phreeqc
   -lengths         0.1
```

|  |
```phreeqc
   -dispersivities  0.015
```

|  |
```phreeqc
   -stagnant        1
```

|  |
```phreeqc
END
```

|  |
```phreeqc
SOLUTION 0  # Original solution reenters
```

|  |
```phreeqc
   units   mmol/l
```

|  |
```phreeqc
   pH       7.0
```

|  |
```phreeqc
   pe      13.0   O2(g)    -0.7
```

|  |
```phreeqc
   K        1.0
```

|  |
```phreeqc
   N(5)     1.0
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
   -file   ex13b.sel
```

|  |
```phreeqc
   -reset  false
```

|  |
```phreeqc
   -distance       true
```

|  |
```phreeqc
   -solution
```

|  |
```phreeqc
USER_PUNCH
```

|  |
```phreeqc
   -headings Cl_mmol Na_mmol
```

|  |
```phreeqc
  10 PUNCH TOT("Cl")*1000, TOT("Na")*1000
```

|  |
```phreeqc
TRANSPORT
```

|  |
```phreeqc
   -shifts  10
```

|  |
```phreeqc
   -punch_cells        1-20
```

|  |
```phreeqc
   -punch_frequency    10
```

|  |
```phreeqc
USER_GRAPH 1 Example 13B
```

|  |
```phreeqc
   -headings Distance Na Cl
```

|  |
```phreeqc
   -chart_title "Dual Porosity, First-Order Exchange with Explicit Mixing Factors"
```

|  |
```phreeqc
   -axis_titles "Distance, in meters" "Millimoles per kilogram water"
```

|  |
```phreeqc
   -axis_scale x_axis 0 2
```

|  |
```phreeqc
   -axis_scale y_axis 0 0.8
```

|  |
```phreeqc
   -plot_concentration_vs x
```

|  |
```phreeqc
   -start
```

|  |
```phreeqc
  10 GRAPH_X DIST
```

|  |
```phreeqc
  20 GRAPH_Y TOT("Na")*1000 TOT("Cl")*1000
```

|  |
```phreeqc
   -end
```

|  |
```phreeqc
END
```

#### Stagnant Zone Calculation Using a Finite Difference Approximation

The stagnant zone consists of spheres with radius r = 0.01 m. Diffusion into the spheres induces radially symmetric concentration changes according to the differential equation:

### . (26)

The calculation in finite differences can therefore be simplified to one (radial) dimension. The calculation follows the theory outlined in Parkhurst and Appelo (1999, section “Transport in Dual Porosity Media”). The stagnant zone is divided into a number of layers that mix by diffusion. In this example, the sphere is cut in five equidistant layers with Δ r = 0.002 m. Five stagnant layers are defined under keyword [TRANSPORT](phreeqc3-56.htm#50593793_87317) with -stagnant 5 ([table 35](phreeqc3-75.htm#50593807_63916)). Mixing is specified among adjacent cells in the stagnant layers with [MIX](phreeqc3-27.htm#50593793_23725) data blocks; the mixing factors are calculated by [See ,](phreeqc3-75.htm#50593807_40135) and [28](phreeqc3-75.htm#50593807_18727). For a neighbor cell, the mixing factor is

### , (27)

and for the central cell, it is

### , (28)

where, D e is the effective diffusion coefficient, Δ t is the time interval, Vj is the volume of cell j (m3), Aij is the shared surface area of cell i and j (m2), hij is the distance between midpoints of cells i and j (m), and fbc is the correction factor for boundary cells (dimensionless). The values for mobile cell 1 and associated. immobile cells are given in [table 36](phreeqc3-75.htm#50593807_26060). The cells in the immobile layer are numbered as n + ( l × cells) + 1, where n is the number of a mobile cell, l is the number of the stagnant layer, and cells is the total number of mobile cells. In this example, the boundary cell in the stagnant zone for cell number 1 is cell number 22 and the other four stagnant layers are cell numbers 42, 62, 82, and 102, with number 102 being the innermost cell of the sphere, which is connected only to one other cell (cell 82). The volume of the mobile cell (cell 1) is expressed relative to the volume of a sphere of radius 0.01 m, by multiplying this volume by εm / εim (4.19×10 -6 × 0.3 / 0.1 = 1.26×10 -5 ). In [table 36](phreeqc3-75.htm#50593807_26060) the value for fbc is 1.72, as calculated with the following equation from Parkhurst and Appelo (1999, equation 127):

Table 35. Input file for example 13C: Stagnant zone with diffusion calculated by finite differences (partial listing).

|  |
```phreeqc
TITLE Example 13C.--1 mmol/l NaCl/NO3 enters column with stagnant zones.
```

|  |
```phreeqc
                    5 layer stagnant zone with finite differences.
```

|  |
```phreeqc
SOLUTION 0    # 1 mmol/l NaCl
```

|  |
```phreeqc
        units   mmol/l
```

|  |
```phreeqc
        pH       7.0
```

|  |
|  |
```phreeqc
        pe      13.0    O2(g)   -0.7
```

|  |
```phreeqc
        Na       1.0    # Na has Retardation = 2
```

|  |
```phreeqc
        Cl       1.0    # Cl has Retardation = 1, stagnant exchange
```

|  |
```phreeqc
        N(5)     1.0    # NO3 is conservative
```

|  |
```phreeqc
#       charge imbalance is no problem ...
```

|  |
```phreeqc
END
```

|  |
```phreeqc
SOLUTION 1-121
```

|  |
```phreeqc
        units   mmol/l
```

|  |
```phreeqc
        pH       7.0
```

|  |
```phreeqc
        pe      13.0   O2(g)    -0.7
```

|  |
```phreeqc
        K        1.0
```

|  |
```phreeqc
        N(5)     1.0
```

|  |
```phreeqc
EXCHANGE_SPECIES # For linear exchange, make KX exch. coeff. equal to NaX
```

|  |
```phreeqc
        K+ + X- = KX
```

|  |
```phreeqc
        log_k   0.0
```

|  |
```phreeqc
        -gamma  3.5     0.015
```

|  |
```phreeqc
EXCHANGE 1-121
```

|  |
```phreeqc
        -equilibrate  1
```

|  |
```phreeqc
        X             1.e-3
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
        -reset false
```

|  |
```phreeqc
        -echo_input true
```

|  |
```phreeqc
MIX    1;    1  0.90712;   22  0.09288
```

|  |
```phreeqc
MIX   22;    1  0.57098;   22  0.21656;   42  0.21246
```

|  |
```phreeqc
MIX   42;   22  0.35027;   42  0.45270;   62  0.19703
```

|  |
```phreeqc
MIX   62;   42  0.38368;   62  0.44579;   82  0.17053
```

|  |
```phreeqc
MIX   82;   62  0.46286;   82  0.42143;  102  0.11571
```

|  |
```phreeqc
MIX  102;   82  0.81000;  102  0.19000
```

|  |
|  |
```phreeqc
#
```

|  |
```phreeqc
#   MIX definitions omitted for mobile cells
```

|  |
```phreeqc
#   2-19 and associated immobile cells
```

|  |
|  |
```phreeqc
#
```

|  |
```phreeqc
MIX   20;   20  0.90712;   41  0.09288
```

|  |
```phreeqc
MIX   41;   20  0.57098;   41  0.21656;   61  0.21246
```

|  |
```phreeqc
MIX   61;   41  0.35027;   61  0.45270;   81  0.19703
```

|  |
```phreeqc
MIX   81;   61  0.38368;   81  0.44579;  101  0.17053
```

|  |
```phreeqc
MIX  101;   81  0.46286;  101  0.42143;  121  0.11571
```

|  |
```phreeqc
MIX  121;  101  0.81000;  121  0.19000
```

|  |
```phreeqc
TRANSPORT
```

|  |
```phreeqc
   -cells  20
```

|  |
```phreeqc
   -shifts 5
```

|  |
```phreeqc
   -flow_direction  forward
```

|  |
```phreeqc
   -time_step       3600
```

|  |
```phreeqc
   -boundary_conditions   flux  flux
```

|  |
```phreeqc
   -diffusion_coefficient 0.0
```

|  |
```phreeqc
   -lengths         0.1
```

|  |
```phreeqc
   -dispersivities  0.015
```

|  |
```phreeqc
   -stagnant        5
```

|  |
```phreeqc
END
```

|  |
```phreeqc
SOLUTION 0  # Original solution reenters
```

|  |
```phreeqc
   units   mmol/l
```

|  |
```phreeqc
   pH       7.0
```

|  |
```phreeqc
   pe      13.0   O2(g)    -0.7
```

|  |
```phreeqc
   K        1.0
```

|  |
```phreeqc
   N(5)     1.0
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
   -file   ex13c.sel
```

|  |
```phreeqc
   -reset  false
```

|  |
```phreeqc
   -distance       true
```

|  |
```phreeqc
   -solution
```

|  |
```phreeqc
USER_PUNCH
```

|  |
```phreeqc
   -headings Cl_mmol Na_mmol
```

|  |
```phreeqc
  10 PUNCH TOT("Cl")*1000, TOT("Na")*1000
```

|  |
```phreeqc
TRANSPORT
```

|  |
```phreeqc
   -shifts  10
```

|  |
```phreeqc
   -punch_cells        1-20
```

|  |
```phreeqc
   -punch_frequency    10
```

|  |
```phreeqc
USER_GRAPH 1 Example 13C
```

|  |
```phreeqc
        -headings Distance Na Cl
```

|  |
```phreeqc
   -chart_title "Dual Porosity, Finite-Difference Approximation"
```

|  |
```phreeqc
   -axis_titles "Distance, in meters" "Millimoles per kilogram water"
```

|  |
```phreeqc
   -axis_scale x_axis 0 2
```

|  |
```phreeqc
   -axis_scale y_axis 0 0.8
```

|  |
```phreeqc
   -plot_concentration_vs x
```

|  |
```phreeqc
   -start
```

|  |
```phreeqc
  10 GRAPH_X DIST
```

|  |
```phreeqc
  20 GRAPH_Y TOT("Na")*1000 TOT("Cl")*1000
```

|  |
```phreeqc
    -end
```

|  |
```phreeqc
END
```

### , (29)

where, V m is the volume of the mobile zone and V bc is the volume of the boundary cell that contacts the mobile zone. It is noted that using fbc = 1.81 slightly improves the fit to an analytical solution given in Crank (1975) for diffusion into spheres in a closed vessel (a beaker with solution and clay beads). However, changing fbc to 1.81 has little effect on the concentration profiles for the columns that are shown in figure 14, and various calculations have shown that fbc = 2 provides good results in general.

Table 36. Mixing factors for finite difference calculation of diffusion in spheres.

[-, undefined value for cell]

|  |
Cell

|

r , m

Vj , m 3

Aij , m 2

hij , m

fbc

mixfij

mixfjj

mixfjk

|  |
102

- 0.001
- 3.35e-8
- 5.03e-5
- 0.002
- 1
- 0.81
- 0.19
- -
|  |
82

- 0.003
- 2.35e-7
- 2.01e-4
- 0.002
- 1
- 0.463
- 0.421
- 0.116
|  |
62

- 0.005
- 6.37e-7
- 4.52e-4
- 0.002
- 1
- 0.384
- 0.446
- 0.170
|  |
42

- 0.007
- 1.24e-6
- 8.04e-4
- 0.002
- 1
- 0.350
- 0.453
- 0.197
|  |
22

- 0.009
- 2.04e-6
- 1.26e-3
- 0.002
- 1.72
- 0.571
- 0.217
- 0.212
|  |
1

- -
- 1.26e-5
- -
- -
- -
- -
- 0.907
- 0.093
Note in [table 35](phreeqc3-75.htm#50593807_63916) that 121 solutions are defined, 1 through 20 for the mobile cells, and the rest for the immobile cells. The input file is identical with the previous one, except for -stagnant 5 and the mixing factors among the cells. Although not all the mixing factors are shown in [table 35](phreeqc3-75.htm#50593807_63916), the remaining mixing factors are identical for subsequent cells and their neighboring stagnant cells. In this example with clay beads, only radial (1D) diffusion is considered, and only mixing among cells in different layers is defined; however, it is possible to include mixing among the immobile cells of adjacent mobile cells.

Figure 14 compares the concentration profiles in the mobile cells obtained with examples 13A and 13B with example 13C. The basic features of the two simulations are the same. The positions of the peaks, as calculated by the two simulations, are similar. The Cl - peak is near 1.2 m, but would be at about 1.45 m in the absence of stagnant zones. The integrated concentrations in the mobile porosity are about equal for the first-order exchange and the finite difference simulations. The exchange factor fs ®1 = 0.21 for the first-order exchange approximation appears to provide adequate accuracy for this simulation. However, the first-order exchange approximation produces lower peaks and more tailing than the more exact solution obtained with finite differences. Discrepancies can also appear as deviations in the breakthrough curve (Van Genuchten, 1985). The first-order exchange model is probably least accurate when applied to simulating the transport behavior of spheres; other shapes of the stagnant area can give a better correspondence. It is clear that the linear exchange model is much easier to apply because any explicit model requires the preparation of extended lists of mixing factors (notice that a separate simulation with [USER_PUNCH](phreeqc3-60.htm#50593793_56415) can serve that purpose, as illustrated in examples [8](phreeqc3-70.htm#50593807_58878) and [21](phreeqc3-83.htm#50593807_68313)), which change when the discretization is adjusted. The calculation time for a finite difference model with multiple immobile-zone layers also may be considerably longer than for the single immobile-zone layer of the first-order exchange approximation.
