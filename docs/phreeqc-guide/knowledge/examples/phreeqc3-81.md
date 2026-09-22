---
title: "Example 19--Modeling Cd+2 Sorption With Linear, Freundlich, and Langmuir Isotherms, and With a Deterministic Distribution of Sorption Sites for Organic Matter, Clay Minerals, and Iron Oxyhydroxides"
source: "https://water.usgs.gov/water-resources/software/PHREEQC/documentation/phreeqc3-html/phreeqc3-81.htm"
source_file: "phreeqc3-81.htm"
retrieved: 2026-09-22
category: example
---
# Example 19--Modeling Cd+2 Sorption With Linear, Freundlich, and Langmuir Isotherms, and With a Deterministic Distribution of Sorption Sites for Organic Matter, Clay Minerals, and Iron Oxyhydroxides

## Example 19--Modeling Cd +2 Sorption With Linear, Freundlich, and Langmuir Isotherms, and With a Deterministic Distribution of Sorption Sites for Organic Matter, Clay Minerals, and Iron Oxyhydroxides

Sorption of heavy metals and organic pollutants on natural materials can be described by linear, Freundlich, or Langmuir isotherms. All three isotherms can be calculated by PHREEQC, as shown in this example for Cd+2 sorbing on a loamy soil (Christensen, 1984; Appelo and Postma, 2005). A more mechanistic approach, also illustrated here, is to model the distribution of Cd+2 over the sorbing components in the soil, in this case, in and on organic matter, clay minerals, and iron oxyhydroxides.

Figure 19 shows the measured sorbed concentration (μg/g soil, microgram per gram) as a function of solute concentration (μg/L water, microgram per liter), and three isotherms defined by:

### , (33)

### , and (34)

### , (35)

where the brackets indicate concentrations in μg/g soil and μg/L water, and Linear, Freundlich, and Langmuir refer to the sorption sites that will be used in definitions for the [SURFACE](phreeqc3-52.htm#50593793_56392) keyword.

The three isotherms correspond to reactions and mass-action equations that can be entered in PHREEQC as follows:

### , (36)

### , (37)

and

### , (38)

where the square brackets indicate activities (unitless).

The Langmuir isotherm ([equation 35](phreeqc3-81.htm#50593807_72431)) and its PHREEQC formulation ([equation 38](phreeqc3-81.htm#50593807_53875)) are equivalent for sorption of Cd on 1 g soil when (Langmuir_total_sites) / 112.4×10 6 = molesLangmuir sites, PHREEQC, and (KLangmuir / 112.4×10 6 )-1 = KLangmuir, PHREEQC, where 112.4×10 6 μg/mol (microgram per mole) is the atomic weight of Cd. Thus, the Langmuir isotherm represents a valid chemical reaction that can be defined in PHREEQC. That is not the case for the linear and the Freundlich isotherms because the equations do not account for the decrease of the “free” sites when Cd+2 sorbs. However, in PHREEQC the number of sorption sites can be made large; for example moleslinear, PHREEQC = 10100 mol, so that a decrease of a few moles of free sites by surface complexation will be negligible relative to the total number of free sites. In activity terms, the effect of the large number of sites is that [Linear] = 1 at all times in [equation 36](phreeqc3-81.htm#50593807_58495). By reducing the constant in the mass-action equation by the same large number, the required distribution is satisfied. Thus, Klinear, PHREEQC = Klinear / moleslinear, PHREEQC. Similarly for the Freundlich equation, KFreundlich, PHREEQC = KFreundlich / molesFreundlich, PHREEQC. The remaining problem with the Freundlich equation ([equation 37](phreeqc3-81.htm#50593807_66908)) is that the stoichiometric coefficient for Cd+2 is n on the left-hand side of the equation, but is 1 on the right-hand side of the equation. This inconsistency can be ignored in PHREEQC by adding -no_check to the reaction equation.

The coefficients in the linear, Freundlich, and Langmuir isotherm equations that fit the measurements are taken from Appelo and Postma (2005). For the linear isotherm Klinear = 0.2 (L water / g soil), and for the Freundlich and Langmuir isotherms:

### , and (39)

### . (40)

The PHREEQC constants then become as follows:

### log(Klinear, PHREEQC) = log(0.2) - log(10100) = -100.7, (41)

### log(KFreundlich, PHREEQC) = log(0.421) + (0.722 - 1) × log(112.4×10 6 ) - log(10100) = -102.61, and (42)

### log(KLangmuir, PHREEQC) = log(112.4×10 6 / 30.9) = 6.56. (43)

The input file ([table 55](phreeqc3-81.htm#50593807_76566)) defines the sorption reactions with keywords [SURFACE_MASTER_SPECIES](phreeqc3-53.htm#50593793_58106) and [SURFACE_SPECIES](phreeqc3-54.htm#50593793_92844). To avoid accumulation of charge in the solution, the sorption formula is specified to be surfaceCdCl2 with -mole_balance for each of the reactions, where surface is Linear, Freundlich, or Langmuir. The keyword [SURFACE](phreeqc3-52.htm#50593793_56392) defines the moles of sites, and the identifier -no_edl specifies that the calculations will be done without the charge/potential term in the mass-action equations for the sorbed species. Next a 1 mM (millimolar) CaCl2 is entered with keyword [SOLUTION](phreeqc3-48.htm#50593793_30253), followed by a reaction of 0.7 mmol CdCl 2 in 20 steps ([REACTION](phreeqc3-40.htm#50593793_75635) data block). [USER_GRAPH](phreeqc3-58.htm#50593793_26121) plots the isotherms, and the experimental data are added to the plot with -plot_tsv_file ex19_meas.tsv.

Table 55. Input file for example 19.

|  |
```phreeqc
TITLE Example 19.--Linear, Freundlich and Langmuir isotherms for
```

|  |
```phreeqc
      Cd sorption on loamy sand. Calculates Example 7.1
```

|  |
```phreeqc
      from Appelo and Postma, 2005. Data from Christensen, 1984.
```

|  |
```phreeqc
SURFACE_MASTER_SPECIES
```

|  |
```phreeqc
      Linear Linear
```

|  |
```phreeqc
      Freundlich Freundlich
```

|  |
```phreeqc
      Langmuir Langmuir
```

|  |
```phreeqc
SURFACE_SPECIES
```

|  |
```phreeqc
  Linear = Linear
```

|  |
```phreeqc
  Linear + Cd+2 = LinearCd+2
```

|  |
```phreeqc
      -log_k -100.7         # log10(0.2) - 100
```

|  |
```phreeqc
      -mole_balance LinearCdCl2
```

|  |
```phreeqc
  Freundlich = Freundlich
```

|  |
```phreeqc
  Freundlich + 0.722 Cd+2 = FreundlichCd+2
```

|  |
```phreeqc
      -log_k -102.61        # log10(0.421) + (0.722 - 1) * log10(112.4e6) - 100
```

|  |
```phreeqc
      -no_check
```

|  |
```phreeqc
      -mole_balance FreundlichCdCl2
```

|  |
```phreeqc
  Langmuir = Langmuir
```

|  |
```phreeqc
  Langmuir + Cd+2 = LangmuirCd+2
```

|  |
```phreeqc
      -log_k 6.56           # log10(112.4 / 30.9e-6)
```

|  |
```phreeqc
      -mole_balance LangmuirCdCl2
```

|  |
```phreeqc
SURFACE 1
```

|  |
```phreeqc
      Linear 1e100 1 1
```

|  |
```phreeqc
      Freundlich 1e100 1 1
```

|  |
```phreeqc
      Langmuir 8.45e-8 1 1  # 9.5 / 112.4e6
```

|  |
```phreeqc
      -no_edl
```

|  |
```phreeqc
SOLUTION 1
```

|  |
```phreeqc
      pH  6
```

|  |
```phreeqc
      Ca  1
```

|  |
```phreeqc
      Cl  2
```

|  |
```phreeqc
REACTION 1
```

|  |
```phreeqc
      CdCl2 1
```

|  |
```phreeqc
      0.7e-6 in 20
```

|  |
```phreeqc
USER_GRAPH Example 19
```

|  |
```phreeqc
      -headings Linear Freundlich Langmuir
```

|  |
```phreeqc
      -chart_title "Sorption Isotherms"
```

|  |
```phreeqc
      -axis_titles "Dissolved Cd, in micrograms per kilogram water" \
```

|  |
```phreeqc
                    "Sorbed Cd, in micrograms per gram soil"
```

|  |
```phreeqc
      -plot_tsv_file ex19_meas.tsv
```

|  |
```phreeqc
      -axis_scale x_axis 0 40
```

|  |
```phreeqc
      -axis_scale y_axis 0 6
```

|  |
```phreeqc
      -initial_solutions true
```

|  |
```phreeqc
  -start
```

|  |
```phreeqc
10 x = act("Cd+2") * 112.4e6
```

|  |
```phreeqc
20 PLOT_XY x, mol("LinearCd+2")*112e6, color = Green, symbol = None, line_width = 2
```

|  |
```phreeqc
30 PLOT_XY x, mol("FreundlichCd+2")*112e6, color = Blue, symbol = None, line_width = 2
```

|  |
```phreeqc
40 PLOT_XY x, mol("LangmuirCd+2")*112e6, color = Orange, symbol = None, line_width = 2
```

|  |
```phreeqc
  -end
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
END
```

Christensen (1984) measured the exchange capacity of the soil (CEC = 56 meq/kg, milliequivalent per kilogram), the iron-oxyhydroxide content (2,790 ppm Fe), and organic matter content (OM = 0.7 weight percent), which can be inserted in a deterministic PHREEQC model. The database phreeqc.dat contains the exchange reaction of Cd+2 and Ca+2 (the predominant cation in the experiment) with the exchange site X-, and the surface complexation reactions of Cd+2 on hydrous ferric oxide (Hfo). Christensen measured the iron content by extracting the soil with dithionite, which reduces and dissolves all amorphous and crystalline iron oxyhydroxides. It is assumed that only 10 percent of analyzed iron has the reactivity represented by Hfo in the phreeqc.dat database. The measured exchange capacity is entered as moles X-, although part of the exchange capacity is located in organic matter, which is modeled separately. Organic matter binds Cd+2 more strongly than clay minerals, so the overestimation of the clay exchange capacity is assumed to be negligible. However, the assumption is checked (and corrected) in the model results, from which the contribution of organic matter to the CEC is estimated by summing the Ca-complexes on humic acid and the calcium excess in the double layer.

Complexation on organic matter can be modeled with WHAM, the Windermere Humic Acid Model of Tipping and Hurley (Tipping and Hurley, 1992; Tipping, 1998; Lofts and Tipping, 2000). The WHAM model was designed for humic and fulvic acids in surface water, but it has been applied to Cd sorption on organic matter in soils (Shi and others, 2007). Complexation constants are defined for protons and cations on a number of monodentate and bidentate binding sites, which can be entered simply as [SURFACE_SPECIES](phreeqc3-54.htm#50593793_92844) in PHREEQC. Furthermore, an empirical parameter for the charge-potential relation of the (probably spherical) humic molecules is incorporated into the Gouy Chapman relation that is used in PHREEQC by adjusting the specific surface area with a function that depends on the ionic strength of the solution (Appelo and Postma, 2005).

The input file ([table 56](phreeqc3-81.htm#50593807_88151)) starts with the [SOLUTION_MASTER_SPECIES](phreeqc3-49.htm#50593793_19910) for the complexing sites on humic acid and the [SURFACE_SPECIES](phreeqc3-54.htm#50593793_92844) for protons, Cd+2 and Ca+2. Next the [SURFACE](phreeqc3-52.htm#50593793_56392) is defined, with number of sites for 3.5 mg humic acid (1 g soil with 0.7 percent OM, is about 3.5 mg organic carbon, taken all as humic acid initially, but corrected to an active fraction by comparing model and measured results). In the WHAM model, the humic acid has a total charge of -7.1 meq/g (milliequivalent per gram), distributed over four monoprotic carboxylic sites (nHA carrying a charge of -2.84 meq/g humic acid), four monoprotic phenolic sites (nHB, charge = -1.42 meq/g humic acid) and twelve diprotic sites that combine carboxylic and phenolic charges (charge = -2.84 meq/g humic acid). Hfo, assumed to represent 10 percent of analyzed iron, is part of the same [SURFACE](phreeqc3-52.htm#50593793_56392). Keyword [EXCHANGE](phreeqc3-14.htm#50593793_84573) defines the moles of X- in 1 g soil, the [SOLUTION](phreeqc3-48.htm#50593793_30253) is 1 mM CaCl2 with a very small Cd+2 concentration to avoid a zero division in [USER_GRAPH](phreeqc3-58.htm#50593793_26121). [USER_GRAPH](phreeqc3-58.htm#50593793_26121) prints the contribution of organic matter to the CEC and the distribution coefficient for Cd+2 (L/kg, liter per kilogram), and plots the sorption of Cd+2 by organic matter, clay exchange, and iron oxyhydroxides (fig. 20).

Table 56. Input file for example 19B.

|  |
```phreeqc
TITLE Example 19B.--Cd sorption on X, Hfo and OC in loamy soil
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
        -user_print true
```

|  |
```phreeqc
SURFACE_MASTER_SPECIES
```

|  |
```phreeqc
# Monodentate 60%
```

|  |
```phreeqc
  H_a  H_aH;  H_b  H_bH;  H_c  H_cH;  H_d  H_dH
```

|  |
```phreeqc
  H_e  H_eH;  H_f  H_fH;  H_g  H_gH;  H_h  H_hH
```

|  |
```phreeqc
# Bidentate 40%
```

|  |
```phreeqc
  H_ab H_abH2;  H_ad H_adH2;  H_af H_afH2;  H_ah H_ahH2
```

|  |
```phreeqc
  H_bc H_bcH2;  H_be H_beH2;  H_bg H_bgH2;  H_cd H_cdH2
```

|  |
```phreeqc
  H_cf H_cfH2;  H_ch H_chH2;  H_de H_deH2;  H_dg H_dgH2
```

|  |
```phreeqc
SURFACE_SPECIES
```

|  |
```phreeqc
  H_aH = H_aH; log_k 0;  H_bH = H_bH; log_k 0;  H_cH = H_cH; log_k 0;  \
```

|  |
```phreeqc
       H_dH = H_dH; log_k 0;
```

|  |
```phreeqc
  H_eH = H_eH; log_k 0;  H_fH = H_fH; log_k 0;  H_gH = H_gH; log_k 0;  \
```

|  |
```phreeqc
       H_hH = H_hH; log_k 0;
```

|  |
|  |
```phreeqc
  H_abH2 = H_abH2; log_k 0;  H_adH2 = H_adH2; log_k 0;  H_afH2 = H_afH2; log_k 0;
```

|  |
```phreeqc
  H_ahH2 = H_ahH2; log_k 0;  H_bcH2 = H_bcH2; log_k 0;  H_beH2 = H_beH2; log_k 0;
```

|  |
```phreeqc
  H_bgH2 = H_bgH2; log_k 0;  H_cdH2 = H_cdH2; log_k 0;  H_cfH2 = H_cfH2; log_k 0;
```

|  |
```phreeqc
  H_chH2 = H_chH2; log_k 0;  H_deH2 = H_deH2; log_k 0;  H_dgH2 = H_dgH2; log_k 0;
```

|  |
```phreeqc
# Protons
```

|  |
```phreeqc
  H_aH = H_a- + H+; log_k  -1.59
```

|  |
```phreeqc
  H_bH = H_b- + H+; log_k  -2.70
```

|  |
```phreeqc
  H_cH = H_c- + H+; log_k  -3.82
```

|  |
```phreeqc
  H_dH = H_d- + H+; log_k  -4.93
```

|  |
|  |
```phreeqc
  H_eH = H_e- + H+; log_k  -6.88
```

|  |
```phreeqc
  H_fH = H_f- + H+; log_k  -8.72
```

|  |
```phreeqc
  H_gH = H_g- + H+; log_k  -10.56
```

|  |
```phreeqc
  H_hH = H_h- + H+; log_k  -12.40
```

|  |
|  |
```phreeqc
  H_abH2 = H_abH- + H+; log_k -1.59;  H_abH- = H_ab-2 + H+; log_k -2.70
```

|  |
```phreeqc
  H_adH2 = H_adH- + H+; log_k -1.59;  H_adH- = H_ad-2 + H+; log_k -4.93
```

|  |
```phreeqc
  H_afH2 = H_afH- + H+; log_k -1.59;  H_afH- = H_af-2 + H+; log_k -8.72
```

|  |
```phreeqc
  H_ahH2 = H_ahH- + H+; log_k -1.59;  H_ahH- = H_ah-2 + H+; log_k -12.40
```

|  |
```phreeqc
  H_bcH2 = H_bcH- + H+; log_k -2.70;  H_bcH- = H_bc-2 + H+; log_k -3.82
```

|  |
```phreeqc
  H_beH2 = H_beH- + H+; log_k -2.70;  H_beH- = H_be-2 + H+; log_k -6.88
```

|  |
```phreeqc
  H_bgH2 = H_bgH- + H+; log_k -2.70;  H_bgH- = H_bg-2 + H+; log_k -10.56
```

|  |
```phreeqc
  H_cdH2 = H_cdH- + H+; log_k -3.82;  H_cdH- = H_cd-2 + H+; log_k -4.93
```

|  |
```phreeqc
  H_cfH2 = H_cfH- + H+; log_k -3.82;  H_cfH- = H_cf-2 + H+; log_k -8.72
```

|  |
```phreeqc
  H_chH2 = H_chH- + H+; log_k -3.82;  H_chH- = H_ch-2 + H+; log_k -12.40
```

|  |
```phreeqc
  H_deH2 = H_deH- + H+; log_k -4.93;  H_deH- = H_de-2 + H+; log_k -6.88
```

|  |
```phreeqc
  H_dgH2 = H_dgH- + H+; log_k -4.93;  H_dgH- = H_dg-2 + H+; log_k -10.56
```

|  |
```phreeqc
# Calcium
```

|  |
```phreeqc
  H_aH + Ca+2 = H_aCa+ + H+; log_k  -3.20
```

|  |
```phreeqc
  H_bH + Ca+2 = H_bCa+ + H+; log_k  -3.20
```

|  |
```phreeqc
  H_cH + Ca+2 = H_cCa+ + H+; log_k  -3.20
```

|  |
```phreeqc
  H_dH + Ca+2 = H_dCa+ + H+; log_k  -3.20
```

|  |
|  |
```phreeqc
  H_eH + Ca+2 = H_eCa+ + H+; log_k  -6.99
```

|  |
```phreeqc
  H_fH + Ca+2 = H_fCa+ + H+; log_k  -6.99
```

|  |
```phreeqc
  H_gH + Ca+2 = H_gCa+ + H+; log_k  -6.99
```

|  |
```phreeqc
  H_hH + Ca+2 = H_hCa+ + H+; log_k  -6.99
```

|  |
|  |
```phreeqc
  H_abH2 + Ca+2 = H_abCa + 2H+; log_k -6.40
```

|  |
```phreeqc
  H_adH2 + Ca+2 = H_adCa + 2H+; log_k -6.40
```

|  |
```phreeqc
  H_afH2 + Ca+2 = H_afCa + 2H+; log_k -7.45
```

|  |
```phreeqc
  H_ahH2 + Ca+2 = H_ahCa + 2H+; log_k -10.2
```

|  |
```phreeqc
  H_bcH2 + Ca+2 = H_bcCa + 2H+; log_k -6.40
```

|  |
```phreeqc
  H_beH2 + Ca+2 = H_beCa + 2H+; log_k -10.2
```

|  |
```phreeqc
  H_bgH2 + Ca+2 = H_bgCa + 2H+; log_k -10.2
```

|  |
```phreeqc
  H_cdH2 + Ca+2 = H_cdCa + 2H+; log_k -6.40
```

|  |
```phreeqc
  H_cfH2 + Ca+2 = H_cfCa + 2H+; log_k -10.2
```

|  |
```phreeqc
  H_chH2 + Ca+2 = H_chCa + 2H+; log_k -10.2
```

|  |
```phreeqc
  H_deH2 + Ca+2 = H_deCa + 2H+; log_k -10.2
```

|  |
```phreeqc
  H_dgH2 + Ca+2 = H_dgCa + 2H+; log_k -10.2
```

|  |
```phreeqc
# Cadmium
```

|  |
```phreeqc
  H_aH + Cd+2 = H_aCd+ + H+; log_k  -1.52
```

|  |
```phreeqc
  H_bH + Cd+2 = H_bCd+ + H+; log_k  -1.52
```

|  |
```phreeqc
  H_cH + Cd+2 = H_cCd+ + H+; log_k  -1.52
```

|  |
```phreeqc
  H_dH + Cd+2 = H_dCd+ + H+; log_k  -1.52
```

|  |
|  |
```phreeqc
  H_eH + Cd+2 = H_eCd+ + H+; log_k  -5.57
```

|  |
```phreeqc
  H_fH + Cd+2 = H_fCd+ + H+; log_k  -5.57
```

|  |
```phreeqc
  H_gH + Cd+2 = H_gCd+ + H+; log_k  -5.57
```

|  |
```phreeqc
  H_hH + Cd+2 = H_hCd+ + H+; log_k  -5.57
```

|  |
|  |
```phreeqc
  H_abH2 + Cd+2 = H_abCd + 2H+; log_k -3.04
```

|  |
```phreeqc
  H_adH2 + Cd+2 = H_adCd + 2H+; log_k -3.04
```

|  |
```phreeqc
  H_afH2 + Cd+2 = H_afCd + 2H+; log_k -7.09
```

|  |
```phreeqc
  H_ahH2 + Cd+2 = H_ahCd + 2H+; log_k -7.09
```

|  |
```phreeqc
  H_bcH2 + Cd+2 = H_bcCd + 2H+; log_k -3.04
```

|  |
```phreeqc
  H_beH2 + Cd+2 = H_beCd + 2H+; log_k -7.09
```

|  |
```phreeqc
  H_bgH2 + Cd+2 = H_bgCd + 2H+; log_k -7.09
```

|  |
```phreeqc
  H_cdH2 + Cd+2 = H_cdCd + 2H+; log_k -3.04
```

|  |
```phreeqc
  H_cfH2 + Cd+2 = H_cfCd + 2H+; log_k -7.09
```

|  |
```phreeqc
  H_chH2 + Cd+2 = H_chCd + 2H+; log_k -7.09
```

|  |
```phreeqc
  H_deH2 + Cd+2 = H_deCd + 2H+; log_k -7.09
```

|  |
```phreeqc
  H_dgH2 + Cd+2 = H_dgCd + 2H+; log_k -7.09
```

|  |
|  |
```phreeqc
END
```

|  |
```phreeqc
SURFACE 1
```

|  |
```phreeqc
# 1 g soil = 0.7% Organic Matter ~ 3.5 mg Organic Carbon.
```

|  |
```phreeqc
# 7.1 meq charge per g OC
```

|  |
```phreeqc
# For Psi vs I (= ionic strength) dependence, adapt specific surface area in PHRC:
```

|  |
```phreeqc
# SS = 159300 - 220800/(I)^0.09 + 91260/(I)^0.18
```

|  |
```phreeqc
# Example: SS = 46514 m2/g for I = 0.003 mol/l
```

|  |
```phreeqc
#
```

|  |
```phreeqc
# 3.5 mg OC, 0.025 meq total charge, distributed over the sites:
```

|  |
```phreeqc
# charge on 4 nHA sites: -2.84 / 4 * 3.5e-3 / 1e3 (eq)
```

|  |
```phreeqc
  H_a  2.48e-06 46.5e3 3.50e-03
```

|  |
```phreeqc
  H_b  2.48e-06; H_c  2.48e-06; H_d  2.48e-06
```

|  |
```phreeqc
# charge on 4 nHB sites: 0.5 * charge on nHA sites
```

|  |
```phreeqc
  H_e  1.24e-06; H_f  1.24e-06; H_g  1.24e-06; H_h  1.24e-06
```

|  |
```phreeqc
# charge on 12 diprotic sites: -2.84 / 12 * 3.5e-3 / 1e3
```

|  |
```phreeqc
  H_ab 8.28e-07; H_ad 8.28e-07; H_af 8.28e-07; H_ah 8.28e-07
```

|  |
```phreeqc
  H_bc 8.28e-07; H_be 8.28e-07; H_bg 8.28e-07; H_cd 8.28e-07
```

|  |
```phreeqc
  H_cf 8.28e-07; H_ch 8.28e-07; H_de 8.28e-07; H_dg 8.28e-07
```

|  |
```phreeqc
        -Donnan
```

|  |
```phreeqc
# 1 g soil = 2.79 mg Fe = 0.05 mmol Fe = 4.45 mg FeOOH
```

|  |
```phreeqc
# 10% has ferrihydrite reactivity
```

|  |
```phreeqc
 Hfo_w 1e-6 600 4.45e-4
```

|  |
```phreeqc
 Hfo_s 0.025e-6
```

|  |
```phreeqc
        -equilibrate 1
```

|  |
```phreeqc
EXCHANGE 1
```

|  |
```phreeqc
 X 55.7e-6
```

|  |
```phreeqc
        -equilibrate 1
```

|  |
```phreeqc
SOLUTION 1
```

|  |
```phreeqc
  pH  6.0
```

|  |
```phreeqc
  Ca  1
```

|  |
```phreeqc
  Cl  2
```

|  |
```phreeqc
  Cd  1e-6
```

|  |
```phreeqc
REACTION 1
```

|  |
```phreeqc
  CdCl2 1
```

|  |
```phreeqc
  2e-6 in 20
```

|  |
```phreeqc
USER_GRAPH Example 19
```

|  |
```phreeqc
        -headings Cd_HumicAcids CdX2 Cd_Hfo TOTAL
```

|  |
```phreeqc
        -chart_title "Deterministic Sorption Model"
```

|  |
```phreeqc
        -axis_titles "Dissolved Cd, in micrograms per kilogram water" \
```

|  |
```phreeqc
                     "Sorbed Cd, in micrograms per gram soil"
```

|  |
```phreeqc
        -plot_tsv_file ex19_meas.tsv
```

|  |
```phreeqc
        -axis_scale x_axis 0 40
```

|  |
```phreeqc
        -axis_scale y_axis 0 6
```

|  |
```phreeqc
        -initial_solutions true
```

|  |
```phreeqc
  -start
```

|  |
```phreeqc
10 H_Cd = SURF("Cd", "H") + EDL("Cd", "H")
```

|  |
```phreeqc
20 print CHR$(10) + " ug Cd/L =", tot("Cd") * 112.4e6, " ug Cd/g = ", H_Cd * 112.4e6 \
```

|  |
```phreeqc
        ," Kd (L/kg) = ", H_Cd*1e3/tot("Cd"), " ug Cd/g in DL =", \
```

|  |
```phreeqc
        EDL("Cd", "H") * 112.4e6
```

|  |
```phreeqc
30 print "Excess meq Ca in DL =", EDL("Ca", "H")*2 - EDL("water", "H") * tot("Ca")*2
```

|  |
```phreeqc
40 print "Excess meq Cl in DL =", EDL("Cl", "H")   - EDL("water", "H") * tot("Cl")
```

|  |
```phreeqc
50 print "Surface charge      =", EDL("Charge", "H")
```

|  |
```phreeqc
55 af_OM = 1 / 9
```

|  |
```phreeqc
60 H_Ca = (SURF("Ca", "H") + EDL("Ca", "H")) * af_OM
```

|  |
```phreeqc
70 print 'Total Ca in/on organic matter =', H_Ca, ' CEC on OM =' H_Ca*200/TOT("X"),\
```

|  |
```phreeqc
        '%.'
```

|  |
```phreeqc
80 x = TOT("Cd") * 112.4e6
```

|  |
```phreeqc
90 H_Cd = H_Cd * 112.4e6 * af_OM
```

|  |
```phreeqc
100 CdX2 = mol("CdX2") * 112.4e6 * 0.96
```

|  |
```phreeqc
110 Hfo_Cd = (mol("Hfo_wOCd+") + mol("Hfo_sOCd+")) * 112.4e6
```

|  |
```phreeqc
120 PLOT_XY x, H_Cd, color = Green, line_width = 2, symbol = None
```

|  |
```phreeqc
130 PLOT_XY x, CdX2, color = Brown, line_width = 2, symbol = None
```

|  |
```phreeqc
140 PLOT_XY x, Hfo_Cd, color = Black, line_width = 2, symbol = None
```

|  |
```phreeqc
150 PLOT_XY x, H_Cd + CdX2 + Hfo_Cd, color = Red, line_width = 2, symbol = None
```

|  |
```phreeqc
  -end
```

|  |
```phreeqc
END
```

In line with many experimental results, figure 20 illustrates that Cd in soils is mainly bound to organic matter. The contribution of clay exchange is about 20 percent, and the contribution of iron-oxyhydroxide surface complexation is negligible. Actually, the sorbed concentration of Cd+2 on 3.5 mg humic acids would be nine times higher, but the concentration was reduced by multiplying with an active fraction of organic matter to match the measured data. The smaller active fraction is understandable because a soil contains lignin and a variety of other, less reactive compounds than the pure humic acid that formed the basis for the Tipping and Hurley database. Shi and others (2007) found an average active fraction of 0.6 for organic carbon concentrations that ranged from 0.18 to 7.15 weight percent in New Jersey soils, whereas Weng and others (2002) and Bonten and others (2008) used an active fraction of 0.3 for soil organic matter in the NICA-Donnan model.

Earlier it was assumed that the organic-matter contribution to the CEC was negligible. The assumption is checked by calculating the Ca exchanged on organic matter relative to the amount exchanged on clays. The amount of calcium exchanged on organic matter is printed in the output file for the largest cadmium concentration as:

```phreeqc
Total Ca in/on organic matter =  1.1810e-006  CEC on OM =  4.2407e+000 %.
```

Although the correction is so small as to be unnecessary, the CEC attributed to clays should be reduced by a factor of 0.96 to account for the 4 percent of the exchange capacity that is located in or on organic matter.
