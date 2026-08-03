"""
╔══════════════════════════════════════════════════════════════════════╗
║  DISCLAIMER: Data herein are provided "as is", with no warranties.   ║
║  Verify critical values independently before use.                    ║
╚══════════════════════════════════════════════════════════════════════╝

Thermal property units (SI, at ~20 °C unless noted):
    cond_thermal  [W/(m·K)]   thermal conductivity
    density       [kg/m³]     mass density
    specific_heat [J/(kg·K)]  specific heat capacity at constant pressure
"""

from .material import Material, AIR, COPPER, PEC
from .const import C0, Z0, PI, EPS0, MU0

EISO: float = (Z0 / (2 * PI)) ** 0.5
EOMNI = (3 * Z0 / (4 * PI)) ** 0.5

##MATERIALS
VACUUM = Material(
    color="EMERGE-AIR",
    opacity=0.05,
    cond_thermal=0.026,
    density=1.225,
    specific_heat=1005,
)

############################################################
#                         METALS                         #
############################################################

GREY = "#bfbfbf"
MET_ALUMINUM = Material(
    cond=3.77e7,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Aluminum",
    cond_thermal=237,
    density=2700,
    specific_heat=897,
)
MET_CARBON = Material(
    cond=3.33e4,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Carbon",
    cond_thermal=1.7,
    density=2267,
    specific_heat=709,
)
MET_CHROMIUM = Material(
    cond=5.56e6,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Chromium",
    cond_thermal=93.9,
    density=7150,
    specific_heat=449,
)
MET_COPPER = Material(
    cond=5.8e7,
    color="EMERGE-COPPER",
    opacity=1.0,
    _metal=True,
    name="Copper",
    cond_thermal=401,
    density=8960,
    specific_heat=385,
)
MET_GOLD = Material(
    cond=4.10e7,
    color="#d4af37",
    opacity=0.5,
    _metal=True,
    name="Gold",
    cond_thermal=318,
    density=19300,
    specific_heat=129,
)
MET_INDIUM = Material(
    cond=6.44e6,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Indium",
    cond_thermal=81.8,
    density=7310,
    specific_heat=233,
)
MET_IRIDIUM = Material(
    cond=2.13e7,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Iridium",
    cond_thermal=147,
    density=22560,
    specific_heat=131,
)
MET_IRON = Material(
    cond=1.04e7,
    color="#aaaaaa",
    opacity=0.5,
    _metal=True,
    name="Iron",
    cond_thermal=80.4,
    density=7874,
    specific_heat=449,
)
MET_LEAD = Material(
    cond=4.84e6,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Lead",
    cond_thermal=35.3,
    density=11340,
    specific_heat=129,
)
MET_MAGNESIUM = Material(
    cond=2.38e7,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Magnesium",
    cond_thermal=156,
    density=1738,
    specific_heat=1023,
)
MET_NICKEL = Material(
    cond=1.14e7,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Nickel",
    cond_thermal=90.9,
    density=8908,
    specific_heat=444,
)
MET_NICHROME = Material(
    cond=9.09e5,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Nichrome",
    cond_thermal=11.3,
    density=8400,
    specific_heat=450,
)
MET_PALLADIUM = Material(
    cond=9.42e6,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Palladium",
    cond_thermal=71.8,
    density=12020,
    specific_heat=244,
)
MET_PLATINUM = Material(
    cond=9.42e6,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Platinum",
    cond_thermal=71.6,
    density=21450,
    specific_heat=133,
)
MET_RHODIUM = Material(
    cond=2.22e7,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Rhodium",
    cond_thermal=150,
    density=12410,
    specific_heat=243,
)
MET_SILVER = Material(
    cond=6.29e7,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Silver",
    cond_thermal=429,
    density=10490,
    specific_heat=235,
)
MET_TANTALUM = Material(
    cond=6.44e6,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Tantalum",
    cond_thermal=57.5,
    density=16690,
    specific_heat=140,
)
MET_TANTALUM_NITRIDE = Material(
    cond=3.97e5,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Tantalum Nitride",
    cond_thermal=8.8,
    density=14300,
    specific_heat=200,
)
MET_TIN = Material(
    cond=8.66e6,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Tin",
    cond_thermal=66.8,
    density=7265,
    specific_heat=228,
)
MET_TITANIUM = Material(
    cond=1.82e6,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Titanium",
    cond_thermal=21.9,
    density=4507,
    specific_heat=523,
)
MET_TUNGSTEN = Material(
    cond=1.79e7,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Tungsten",
    cond_thermal=173,
    density=19250,
    specific_heat=132,
)
MET_ZINC = Material(
    cond=1.76e7,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Zinc",
    cond_thermal=116,
    density=7134,
    specific_heat=388,
)
MET_ZIRCONIUM = Material(
    cond=2.44e7,
    color=GREY,
    opacity=0.5,
    _metal=True,
    name="Zirconium",
    cond_thermal=22.6,
    density=6506,
    specific_heat=278,
)


############################################################
#                       SEMICONDUCTORS                     #
############################################################

SEMI_SILICON = Material(
    er=11.7,
    tand=0.005,
    color="#b4b4b4",
    opacity=0.5,
    _metal=True,
    name="Silicon",
    cond_thermal=148,
    density=2329,
    specific_heat=700,
)
SEMI_SILICON_N = Material(
    er=7.5,
    tand=0.0003,
    color="#a0a0a0",
    opacity=0.5,
    _metal=True,
    name="Silicon Nitride",
    cond_thermal=30,
    density=3170,
    specific_heat=700,
)
SEMI_SILICON_OXIDE = Material(
    er=3.9,
    tand=0.0001,
    color="#e0e0e0",
    opacity=0.5,
    _metal=True,
    name="Silicon Dioxide",
    cond_thermal=1.4,
    density=2200,
    specific_heat=730,
)
SEMI_GERMANIUM = Material(
    er=16.0,
    tand=0.001,
    color="#787878",
    opacity=0.5,
    _metal=True,
    name="Germanium",
    cond_thermal=60.2,
    density=5323,
    specific_heat=320,
)
SEMI_GAAS = Material(
    er=13.1,
    tand=0.0016,
    color="#aa8888",
    opacity=0.5,
    _metal=True,
    name="Gallium Arsenide",
    cond_thermal=55,
    density=5317,
    specific_heat=330,
)
SEMI_GA_N = Material(
    er=8.9,
    tand=0.002,
    color="#8888cc",
    opacity=0.5,
    _metal=True,
    name="Gallium Nitride",
    cond_thermal=130,
    density=6150,
    specific_heat=490,
)
SEMI_INP = Material(
    er=12.5,
    tand=0.0015,
    color="#cc99aa",
    opacity=0.5,
    _metal=True,
    name="Indium Phosphide",
    cond_thermal=68,
    density=4810,
    specific_heat=310,
)
SEMI_ALN = Material(
    er=8.6,
    tand=0.0003,
    color="#ccccee",
    opacity=0.5,
    _metal=True,
    name="Aluminum Nitride",
    cond_thermal=285,
    density=3260,
    specific_heat=740,
)
SEMI_AL2O3 = Material(
    er=9.8,
    tand=0.0002,
    color="#eaeaea",
    opacity=0.5,
    _metal=True,
    name="Alumina",
    cond_thermal=35,
    density=3950,
    specific_heat=765,
)
SEMI_SAPPHIRE = Material(
    er=9.4,
    tand=0.0001,
    color="#ddddff",
    opacity=0.5,
    _metal=True,
    name="Sapphire",
    cond_thermal=46,
    density=3980,
    specific_heat=761,
)
SEMI_DIAMOND = Material(
    er=5.5,
    tand=0.00005,
    color="#cceeff",
    opacity=0.5,
    _metal=True,
    name="Diamond",
    cond_thermal=2200,
    density=3510,
    specific_heat=509,
)
SEMI_HBN = Material(
    er=4.0,
    tand=0.0001,
    color="#eeeeff",
    opacity=0.5,
    _metal=True,
    name="Hexagonal Boron Nitride",
    cond_thermal=400,
    density=2100,
    specific_heat=800,
)
SEMI_SIOXNY = Material(
    er=5.0,
    tand=0.002,
    color="#ddddee",
    opacity=0.5,
    _metal=True,
    name="Silicon Oxynitride",
    cond_thermal=1.8,
    density=2400,
    specific_heat=720,
)


############################################################
#                          LIQUIDS                         #
############################################################

LIQ_WATER = Material(
    er=80.1,
    cond=0.0,
    color="#0080ff",
    opacity="EMERE-DIEL",
    _metal=True,
    name="Water",
    cond_thermal=0.6,
    density=998,
    specific_heat=4182,
)
LIQ_FERRITE = Material(
    er=12.0,
    ur=2000,
    tand=0.02,
    color="#994d4d",
    opacity="EMERE-DIEL",
    name="Ferrite",
    cond_thermal=5.0,
    density=5000,
    specific_heat=750,
)

############################################################
#                        DIELECTRICS                       #
############################################################

#  TRADEMARKS: All product names (e.g. "DUROID") are the property of their
#  respective owners.  Use of them here does not imply any affiliation with or
#  endorsement by those owners.

# --- Generic / common polymers ---
# Thermal conductivity for PCB substrates is typically in the range 0.2–0.95 W/(m·K).
# Where datasheets don't specify density or specific heat, typical values for the
# base polymer class are used:
#   PTFE-based laminates:   k~0.25, rho~2150, cp~1000
#   Hydrocarbon/ceramic:    k~0.5–0.8, rho~1800–2100, cp~900–1100
#   Epoxy/glass (FR4-like): k~0.3, rho~1850–1900, cp~1100
#   Pure PTFE:              k~0.25, rho~2150, cp~1000

DIEL_PTFE = Material(
    er=2.1,
    tand=0.0002,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Teflon",
    cond_thermal=0.25,
    density=2150,
    specific_heat=1000,
)
DIEL_POLYIMIDE = Material(
    er=3.4,
    tand=0.02,
    color="#b8b8b8",
    name="Polyimide",
    cond_thermal=0.12,
    density=1420,
    specific_heat=1090,
)
DIEL_CERAMIC = Material(
    er=6.0,
    tand=0.001,
    color="#efead1",
    name="Ceramic",
    cond_thermal=2.0,
    density=3800,
    specific_heat=800,
)

# --- Arlon AD Series (hydrocarbon/ceramic PTFE) ---
_AD_K, _AD_RHO, _AD_CP = 0.50, 2000, 1000
DIEL_AD10 = Material(
    er=10.2,
    tand=0.0078,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD10",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD1000 = Material(
    er=10.2,
    tand=0.0023,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD1000",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD250 = Material(
    er=2.5,
    tand=0.0018,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD250",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD250_PIM = Material(
    er=2.5,
    tand=0.0018,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD250 PIM",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD250A = Material(
    er=2.50,
    tand=0.0015,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD250A",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD250C = Material(
    er=2.50,
    tand=0.0014,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD250C",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD255 = Material(
    er=2.55,
    tand=0.0018,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD255",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD255A = Material(
    er=2.55,
    tand=0.0015,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD255A",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD255C = Material(
    er=2.55,
    tand=0.0014,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD255C",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD260A = Material(
    er=2.60,
    tand=0.0017,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD260A",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD270 = Material(
    er=2.7,
    tand=0.0023,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD270",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD300 = Material(
    er=3,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD300",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD300_PIM = Material(
    er=3,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD300 PIM",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD300A = Material(
    er=3.00,
    tand=0.002,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD300A",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD300C = Material(
    er=2.97,
    tand=0.002,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD300C",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD320 = Material(
    er=3.2,
    tand=0.0038,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD320",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD320_PIM = Material(
    er=3.2,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD320 PIM",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD320A = Material(
    er=3.20,
    tand=0.0032,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD320A",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD350 = Material(
    er=3.5,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD350",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD350_PIM = Material(
    er=3.5,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD350 PIM",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD350A = Material(
    er=3.50,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD350A",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD410 = Material(
    er=4.1,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD410",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD430 = Material(
    er=4.3,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD430",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD450 = Material(
    er=4.5,
    tand=0.0035,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD450",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD450A = Material(
    er=4.5,
    tand=0.0035,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD450 A",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD5 = Material(
    er=5.1,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD5",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AD600 = Material(
    er=5.90,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AD600",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_AR1000 = Material(
    er=9.8,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="AR1000",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)
DIEL_CER_10 = Material(
    er=10.00,
    tand=0.0035,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="CER 10",
    cond_thermal=_AD_K,
    density=_AD_RHO,
    specific_heat=_AD_CP,
)

# --- CLTE / Comclad / CuClad / CUFLON / DICLAD series (PTFE-based) ---
_PTFE_K, _PTFE_RHO, _PTFE_CP = 0.25, 2150, 1000
DIEL_CLTE = Material(
    er=2.96,
    tand=0.0023,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="CLTE",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_CLTE_AT = Material(
    er=3.00,
    tand=0.0013,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="CLTE-AT",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_CLTE_LC = Material(
    er=2.94,
    tand=0.0025,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="CLTE LC",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_CLTE_XT = Material(
    er=2.94,
    tand=0.0012,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="CLTE XT",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_COMCLAD_HF_ER2 = Material(
    er=2,
    tand=0.0025,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Comclad HF ER2",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_COMCLAD_HF_ER3 = Material(
    er=3,
    tand=0.0025,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Comclad HF ER3",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_COMCLAD_HF_ER4 = Material(
    er=4,
    tand=0.0025,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Comclad HF ER4",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_COMCLAD_HF_ER5 = Material(
    er=5,
    tand=0.0025,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Comclad HF ER5",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_COMCLAD_HF_ER6 = Material(
    er=6,
    tand=0.0025,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Comclad HF ER6",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_COPPER_CLAD_ULTEM = Material(
    er=3.05,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Copper clad ULTEM",
    cond_thermal=0.22,
    density=1270,
    specific_heat=1100,
)
DIEL_CUCLAD_217LX = Material(
    er=2.17,
    tand=0.0009,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Copper Clad 217LX",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_CUCLAD_233LX = Material(
    er=2.33,
    tand=0.0013,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Cpper Clad 233LX",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_CUCLAD_250GT = Material(
    er=2.5,
    tand=0.0018,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Copper Clad 250GT",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_CUCLAD_250GX = Material(
    er=2.4,
    tand=0.0018,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Copper Clad 250GX",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_CUFLON = Material(
    er=2.05,
    tand=0.00045,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="CUFLON",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_DICLAD_522 = Material(
    er=2.4,
    tand=0.0018,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="DICLAD 522",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_DICLAD_527 = Material(
    er=2.4,
    tand=0.0018,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="DICLAD 527",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_DICLAD_870 = Material(
    er=2.33,
    tand=0.0013,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="DICLAD 870",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_DICLAD_880 = Material(
    er=2.17,
    tand=0.0009,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="DICLAD 880",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_DICLAD_880_PIM = Material(
    er=2.17,
    tand=0.0009,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="DICLAD 880 PIM",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)

# --- GETEK (epoxy-based) ---
_EPOXY_K, _EPOXY_RHO, _EPOXY_CP = 0.30, 1900, 1100
DIEL_GETEK_3p5 = Material(
    er=3.5,
    tand=0.01,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="GETEK(3.5)",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)
DIEL_GETEK_3p8 = Material(
    er=3.8,
    tand=0.01,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="GETEK(3.8)",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)

# --- IS680 series (PTFE/glass) ---
DIEL_IS6802_80 = Material(
    er=2.80,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="IS6802 80",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_IS6803_00 = Material(
    er=3.00,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="IS6803 00",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_IS6803_20 = Material(
    er=3.20,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="IS6803 20",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_IS6803_33 = Material(
    er=3.33,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="IS6803 33",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_IS6803_38 = Material(
    er=3.38,
    tand=0.0032,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="IS6803 38",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_IS6803_45 = Material(
    er=3.45,
    tand=0.0035,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="IS6803 45",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_ISOCLAD_917 = Material(
    er=2.17,
    tand=0.0013,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Isoclad 917",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_ISOCLAD_933 = Material(
    er=2.33,
    tand=0.0016,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Isoclad 933",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)

# --- Isola (epoxy/resin based) ---
DIEL_ISOLA_I_TERA_MT = Material(
    er=3.45,
    tand=0.0030,
    color="#3c9747",
    name="Isola I Tera Mt",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)
DIEL_ISOLA_NELCO_4000_13 = Material(
    er=3.77,
    tand=0.008,
    color="#3c9747",
    name="Isola Nelco 4000 13",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)

# --- Matsushita / misc ---
DIEL_MAT_25N = Material(
    er=3.38,
    tand=0.0025,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Mat 25n",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_MAT25FR = Material(
    er=3.58,
    tand=0.0035,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Mat25fr",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_MEGTRON6R5775 = Material(
    er=3.61,
    tand=0.004,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Megtron6r5775",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)
DIEL_MERCURYWAVE_9350 = Material(
    er=3.5,
    tand=0.004,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Mercurywave 9350",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_MULTICLAD_HF = Material(
    er=3.7,
    tand=0.0045,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Multiclad HF",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)

# --- Nelco N-series (epoxy/PPO based) ---
DIEL_N_8000 = Material(
    er=3.5,
    tand=0.011,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco N8000",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)
DIEL_N4350_13RF = Material(
    er=3.5,
    tand=0.0065,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco N4350 13RF",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)
DIEL_N4380_13RF = Material(
    er=3.8,
    tand=0.007,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco N4380 13RF",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)
DIEL_N8000Q = Material(
    er=3.2,
    tand=0.006,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco N8000Q",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)
DIEL_N9300_13RF = Material(
    er=3.0,
    tand=0.004,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco N9300 13RF",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)
DIEL_N9320_13RF = Material(
    er=3.2,
    tand=0.0045,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco N9320 13RF",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)
DIEL_N9338_13RF = Material(
    er=3.38,
    tand=0.0046,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco N9338 13RF",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)
DIEL_N9350_13RF = Material(
    er=3.48,
    tand=0.0055,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco N9350 13RF",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)
DIEL_NH9294 = Material(
    er=2.94,
    tand=0.0022,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NH9294",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NH9300 = Material(
    er=3.00,
    tand=0.0023,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NH9300",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NH9320 = Material(
    er=3.20,
    tand=0.0024,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NH9320",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NH9338 = Material(
    er=3.38,
    tand=0.0025,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NH9338",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NH9348 = Material(
    er=3.48,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NH9348",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NH9350 = Material(
    er=3.50,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NH9350",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NH9410 = Material(
    er=4.10,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NH9410",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NH9450 = Material(
    er=4.50,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NH9450",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NORCLAD = Material(
    er=2.55,
    tand=0.0011,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Norclad",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)

# --- Nelco NX / NY series (PTFE-ceramic) ---
DIEL_NX9240 = Material(
    er=2.40,
    tand=0.0016,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NX9240",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NX9245 = Material(
    er=2.45,
    tand=0.0016,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NX9245",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NX9250 = Material(
    er=2.50,
    tand=0.0017,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NX9250",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NX9255 = Material(
    er=2.55,
    tand=0.0018,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NX9255",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NX9260 = Material(
    er=2.60,
    tand=0.0019,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NX9260",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NX9270 = Material(
    er=2.70,
    tand=0.002,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NX9270",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NX9294 = Material(
    er=2.94,
    tand=0.0022,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NX9294",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NX9300 = Material(
    er=3.00,
    tand=0.0023,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NX9300",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NX9320 = Material(
    er=3.20,
    tand=0.0024,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NX9320",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NY9208 = Material(
    er=2.08,
    tand=0.0006,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NY9208",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NY9217 = Material(
    er=2.17,
    tand=0.0008,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NY9217",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NY9220 = Material(
    er=2.20,
    tand=0.0009,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NY9220",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_NY9233 = Material(
    er=2.33,
    tand=0.0011,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Nelco NY9233",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_POLYGUIDE = Material(
    er=2.320,
    tand=0.0005,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Polyguide",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)

# --- Rogers RF series (hydrocarbon/ceramic) ---
_HC_K, _HC_RHO, _HC_CP = 0.50, 1950, 1000
DIEL_RF_30 = Material(
    er=3.00,
    tand=0.0019,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RF-30",
    cond_thermal=_HC_K,
    density=_HC_RHO,
    specific_heat=_HC_CP,
)
DIEL_RF_301 = Material(
    er=2.97,
    tand=0.0018,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RF-301",
    cond_thermal=_HC_K,
    density=_HC_RHO,
    specific_heat=_HC_CP,
)
DIEL_RF_35 = Material(
    er=3.50,
    tand=0.0025,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RF-35",
    cond_thermal=_HC_K,
    density=_HC_RHO,
    specific_heat=_HC_CP,
)
DIEL_RF_35A2 = Material(
    er=3.50,
    tand=0.0015,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RF-35A2",
    cond_thermal=_HC_K,
    density=_HC_RHO,
    specific_heat=_HC_CP,
)
DIEL_RF_35P = Material(
    er=3.50,
    tand=0.0034,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RF-35P",
    cond_thermal=_HC_K,
    density=_HC_RHO,
    specific_heat=_HC_CP,
)
DIEL_RF_35TC = Material(
    er=3.50,
    tand=0.0011,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RF-35TC",
    cond_thermal=_HC_K,
    density=_HC_RHO,
    specific_heat=_HC_CP,
)
DIEL_RF_41 = Material(
    er=4.10,
    tand=0.0038,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RF-41",
    cond_thermal=_HC_K,
    density=_HC_RHO,
    specific_heat=_HC_CP,
)
DIEL_RF_43 = Material(
    er=4.30,
    tand=0.0033,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RF-43",
    cond_thermal=_HC_K,
    density=_HC_RHO,
    specific_heat=_HC_CP,
)
DIEL_RF_45 = Material(
    er=4.50,
    tand=0.0037,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RF-45",
    cond_thermal=_HC_K,
    density=_HC_RHO,
    specific_heat=_HC_CP,
)
DIEL_RF_60A = Material(
    er=6.15,
    tand=0.0038,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RF-60A",
    cond_thermal=_HC_K,
    density=_HC_RHO,
    specific_heat=_HC_CP,
)

# --- Rogers RO3000 series (PTFE/ceramic) ---
_RO3_K, _RO3_RHO, _RO3_CP = 0.50, 2100, 900
DIEL_RO3003 = Material(
    er=3.00,
    tand=0.0011,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RO3003",
    cond_thermal=0.50,
    density=_RO3_RHO,
    specific_heat=_RO3_CP,
)
DIEL_RO3006 = Material(
    er=6.15,
    tand=0.002,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RO3006",
    cond_thermal=0.61,
    density=_RO3_RHO,
    specific_heat=_RO3_CP,
)
DIEL_RO3010 = Material(
    er=10.2,
    tand=0.0022,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RO3010",
    cond_thermal=0.66,
    density=_RO3_RHO,
    specific_heat=_RO3_CP,
)
DIEL_RO3035 = Material(
    er=3.50,
    tand=0.0017,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RO3035",
    cond_thermal=0.50,
    density=_RO3_RHO,
    specific_heat=_RO3_CP,
)
DIEL_RO3203 = Material(
    er=3.02,
    tand=0.0016,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RO3203",
    cond_thermal=_RO3_K,
    density=_RO3_RHO,
    specific_heat=_RO3_CP,
)
DIEL_RO3206 = Material(
    er=6.15,
    tand=0.0027,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RO3206",
    cond_thermal=_RO3_K,
    density=_RO3_RHO,
    specific_heat=_RO3_CP,
)
DIEL_RO3210 = Material(
    er=10.2,
    tand=0.0027,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RO3210",
    cond_thermal=_RO3_K,
    density=_RO3_RHO,
    specific_heat=_RO3_CP,
)
DIEL_RO3730 = Material(
    er=3.00,
    tand=0.0016,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RO3730",
    cond_thermal=_RO3_K,
    density=_RO3_RHO,
    specific_heat=_RO3_CP,
)

# --- Rogers RO4000 series (hydrocarbon/ceramic, glass-reinforced) ---
DIEL_RO4003C = Material(
    er=3.38,
    tand=0.0029,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RO4003C",
    cond_thermal=0.71,
    density=1790,
    specific_heat=1000,
)
DIEL_RO4350B = Material(
    er=3.48,
    tand=0.0037,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RO4350B",
    cond_thermal=0.69,
    density=1860,
    specific_heat=1000,
)
DIEL_RO4350B_TX = Material(
    er=3.48,
    tand=0.0034,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RO4350B TX",
    cond_thermal=0.69,
    density=1860,
    specific_heat=1000,
)
DIEL_RO4360 = Material(
    er=6.15,
    tand=0.0038,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RO4360",
    cond_thermal=0.80,
    density=2100,
    specific_heat=950,
)
DIEL_RO4533 = Material(
    er=3.30,
    tand=0.0025,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RO4533",
    cond_thermal=0.65,
    density=1800,
    specific_heat=1000,
)
DIEL_RO4534 = Material(
    er=3.40,
    tand=0.0027,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RO4534",
    cond_thermal=0.65,
    density=1800,
    specific_heat=1000,
)
DIEL_RO4535 = Material(
    er=3.50,
    tand=0.0037,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RO4535",
    cond_thermal=0.65,
    density=1800,
    specific_heat=1000,
)
DIEL_RO4730 = Material(
    er=3.00,
    tand=0.0033,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RO4730",
    cond_thermal=0.60,
    density=1800,
    specific_heat=1000,
)

# --- Rogers RT/duroid series (PTFE-based) ---
_DUR_K, _DUR_RHO, _DUR_CP = 0.26, 2200, 1000
DIEL_RT_Duroid_5870 = Material(
    er=2.33,
    tand=0.0012,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RT/duroid 5870",
    cond_thermal=_DUR_K,
    density=_DUR_RHO,
    specific_heat=_DUR_CP,
)
DIEL_RT_Duroid_5880 = Material(
    er=2.20,
    tand=0.0009,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RT/duroid 5880",
    cond_thermal=_DUR_K,
    density=_DUR_RHO,
    specific_heat=_DUR_CP,
)
DIEL_RT_Duroid_5880LZ = Material(
    er=1.96,
    tand=0.0019,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RT/duroid 5880LZ",
    cond_thermal=0.22,
    density=1400,
    specific_heat=1000,
)
DIEL_RT_Duroid_6002 = Material(
    er=2.94,
    tand=0.0012,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RT/duroid 6002",
    cond_thermal=_DUR_K,
    density=_DUR_RHO,
    specific_heat=_DUR_CP,
)
DIEL_RT_Duroid_6006 = Material(
    er=6.15,
    tand=0.0027,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RT/duroid 6006",
    cond_thermal=0.48,
    density=2800,
    specific_heat=900,
)
DIEL_RT_Duroid_6010_2LM = Material(
    er=10.2,
    tand=0.0023,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RT/duroid 6010 2LM",
    cond_thermal=0.66,
    density=2900,
    specific_heat=900,
)
DIEL_RT_Duroid_6035HTC = Material(
    er=3.50,
    tand=0.0013,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RT/duroid 6035HTC",
    cond_thermal=1.44,
    density=2400,
    specific_heat=900,
)
DIEL_RT_Duroid_6202 = Material(
    er=2.94,
    tand=0.0015,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RT/duroid 6202",
    cond_thermal=_DUR_K,
    density=_DUR_RHO,
    specific_heat=_DUR_CP,
)
DIEL_RT_Duroid_6202PR = Material(
    er=2.90,
    tand=0.002,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers RT/duroid 6202PR",
    cond_thermal=_DUR_K,
    density=_DUR_RHO,
    specific_heat=_DUR_CP,
)

# --- Syron / misc ---
DIEL_SYRON_70000_002IN_Thick = Material(
    er=3.4,
    tand=0.0045,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Syron 70000 0.002in",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)
DIEL_SYRON_71000_004IN_THICK = Material(
    er=3.39,
    tand=0.005,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Syron 71000 0.004in",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)
DIEL_SYRON_71000INCH = Material(
    er=3.61,
    tand=0.006,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Syron 71000 Inch",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)

# --- Taconic series (PTFE-based unless noted) ---
DIEL_TACLAMPLUS = Material(
    er=2.10,
    tand=0.0004,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TacLam Plus",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)

# --- Rogers TC series (ceramic-filled) ---
DIEL_TC350 = Material(
    er=3.50,
    tand=0.002,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers TC350",
    cond_thermal=0.72,
    density=2050,
    specific_heat=950,
)
DIEL_TC600 = Material(
    er=6.15,
    tand=0.002,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers TC600",
    cond_thermal=0.72,
    density=2800,
    specific_heat=900,
)
DIEL_THETA = Material(
    er=3.85,
    tand=0.0123,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Theta",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)

# --- Taconic TL series (PTFE/glass) ---
DIEL_TLA_6 = Material(
    er=2.62,
    tand=0.0017,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLA-6",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLC_27 = Material(
    er=2.75,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLC-27",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLC_30 = Material(
    er=3.00,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLC-30",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLC_32 = Material(
    er=3.20,
    tand=0.003,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLC-32",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLC_338 = Material(
    er=3.38,
    tand=0.0034,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLC-338",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLC_35 = Material(
    er=3.50,
    tand=0.0037,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLC-35",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLE_95 = Material(
    er=2.95,
    tand=0.0028,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLE-95",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLF_34 = Material(
    er=3.40,
    tand=0.002,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLF-34",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLF_35 = Material(
    er=3.50,
    tand=0.002,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLF-35",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLG_29 = Material(
    er=2.87,
    tand=0.0027,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLG-29",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLG_30 = Material(
    er=3.00,
    tand=0.0038,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLG-30",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLP_3 = Material(
    er=2.33,
    tand=0.0009,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLP-3",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLP_5 = Material(
    er=2.20,
    tand=0.0009,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLP-5",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLP_5A = Material(
    er=2.17,
    tand=0.0009,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLP-5A",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLT_0 = Material(
    er=2.45,
    tand=0.0019,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLT-0",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLT_6 = Material(
    er=2.65,
    tand=0.0019,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLT-6",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLT_7 = Material(
    er=2.60,
    tand=0.0019,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLT-7",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLT_8 = Material(
    er=2.55,
    tand=0.0019,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLT-8",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLT_9 = Material(
    er=2.50,
    tand=0.0019,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLT-9",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLX_0 = Material(
    er=2.45,
    tand=0.0019,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLX-0",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLX_6 = Material(
    er=2.65,
    tand=0.0019,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLX-6",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLX_7 = Material(
    er=2.60,
    tand=0.0019,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLX-7",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLX_8 = Material(
    er=2.55,
    tand=0.0019,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLX-8",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLX_9 = Material(
    er=2.50,
    tand=0.0019,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLX-9",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLY_3 = Material(
    er=2.33,
    tand=0.0012,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLY-3",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLY_3F = Material(
    er=2.33,
    tand=0.0012,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLY-3F",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLY_5 = Material(
    er=2.20,
    tand=0.0009,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLY-5",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLY_5_L = Material(
    er=2.20,
    tand=0.0009,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLY-5L",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLY_5A = Material(
    er=2.17,
    tand=0.0009,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLY-5A",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TLY_5AL = Material(
    er=2.17,
    tand=0.0009,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TLY-5AL",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)

# --- Rogers TMM series (thermoset ceramic) ---
_TMM_K, _TMM_RHO, _TMM_CP = 0.72, 2200, 900
DIEL_TMM_10 = Material(
    er=9.20,
    tand=0.0022,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers TMM10",
    cond_thermal=_TMM_K,
    density=_TMM_RHO,
    specific_heat=_TMM_CP,
)
DIEL_TMM_10i = Material(
    er=9.80,
    tand=0.002,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers TMM10i",
    cond_thermal=_TMM_K,
    density=_TMM_RHO,
    specific_heat=_TMM_CP,
)
DIEL_TMM_3 = Material(
    er=3.27,
    tand=0.002,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers TMM3",
    cond_thermal=_TMM_K,
    density=1780,
    specific_heat=_TMM_CP,
)
DIEL_TMM_4 = Material(
    er=4.50,
    tand=0.002,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers TMM4",
    cond_thermal=_TMM_K,
    density=_TMM_RHO,
    specific_heat=_TMM_CP,
)
DIEL_TMM_6 = Material(
    er=6.00,
    tand=0.0023,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers TMM6",
    cond_thermal=_TMM_K,
    density=_TMM_RHO,
    specific_heat=_TMM_CP,
)

# --- TRF series ---
DIEL_TRF_41 = Material(
    er=4.10,
    tand=0.0035,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TRF-41",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TRF_43 = Material(
    er=4.30,
    tand=0.0035,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TRF-43",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TRF_45 = Material(
    er=4.50,
    tand=0.0035,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TRF-45",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)

# --- TSM series ---
DIEL_TSM_26 = Material(
    er=2.60,
    tand=0.0014,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TSM-26",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TSM_29 = Material(
    er=2.94,
    tand=0.0013,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TSM-29",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TSM_30 = Material(
    er=3.00,
    tand=0.0013,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TSM-30",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TSM_DS = Material(
    er=2.85,
    tand=0.001,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TSM-DS",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_TSM_DS3 = Material(
    er=3.00,
    tand=0.0011,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="TSM-DS3",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)

# --- Arlon Ultralam (PTFE-based) ---
DIEL_ULTRALAM_2000 = Material(
    er=2.4,
    tand=0.0019,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Arlon Ultralam 2000",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)
DIEL_ULTRALAM_3850 = Material(
    er=2.9,
    tand=0.0025,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Arlon Ultralam 3850",
    cond_thermal=_PTFE_K,
    density=_PTFE_RHO,
    specific_heat=_PTFE_CP,
)

# --- Rogers XT/duroid ---
DIEL_XT_Duroid_80000_002IN_Thick = Material(
    er=3.23,
    tand=0.0035,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers XT/duroid 80000 0.002in",
    cond_thermal=_DUR_K,
    density=_DUR_RHO,
    specific_heat=_DUR_CP,
)
DIEL_XT_Duroid_8100 = Material(
    er=3.54,
    tand=0.0049,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers XT/duroid 8100",
    cond_thermal=_DUR_K,
    density=_DUR_RHO,
    specific_heat=_DUR_CP,
)
DIEL_XT_Duroid_81000_004IN_Thick = Material(
    er=3.32,
    tand=0.0038,
    color="EMERGE-DIEL",
    opacity="EMERE-DIEL",
    name="Rogers XT/duroid 81000 0.004in",
    cond_thermal=_DUR_K,
    density=_DUR_RHO,
    specific_heat=_DUR_CP,
)
DIEL_TEFLON = Material(
    er=2.1,
    tand=0.0003,
    color="#eeeeee",
    opacity="EMERE-DIEL",
    name="Teflon",
    cond_thermal=0.25,
    density=2150,
    specific_heat=1000,
)

DIEL_IS420_approx = Material(
    er=4.5,
    tand=0.018,
    color="#CCDE30",
    opacity="EMERE-DIEL",
    name="ISOLA420 approximate",
    cond_thermal=_EPOXY_K,
    density=_EPOXY_RHO,
    specific_heat=_EPOXY_CP,
)

# Legacy FR Materials
_FR_K, _FR_RHO, _FR_CP = 0.30, 1900, 1100
DIEL_FR1 = Material(
    er=4.8,
    tand=0.025,
    color="#3c9747",
    opacity="EMERE-DIEL",
    name="FR-1 (Paper Phenolic)",
    cond_thermal=0.20,
    density=1400,
    specific_heat=1400,
)
DIEL_FR2 = Material(
    er=4.8,
    tand=0.02,
    color="#3c9747",
    opacity="EMERE-DIEL",
    name="FR-2 (Paper Phenolic)",
    cond_thermal=0.20,
    density=1400,
    specific_heat=1400,
)
DIEL_FR3 = Material(
    er=4.5,
    tand=0.02,
    color="#2b7a4b",
    opacity="EMERE-DIEL",
    name="FR-3 (Paper Epoxy)",
    cond_thermal=0.25,
    density=1500,
    specific_heat=1300,
)
DIEL_FR4 = Material(
    er=4.4,
    tand=0.015,
    color="#1e8449",
    opacity="EMERE-DIEL",
    name="FR-4 (Glass Epoxy)",
    cond_thermal=0.30,
    density=1850,
    specific_heat=1100,
)
DIEL_FR5 = Material(
    er=4.2,
    tand=0.012,
    color="#156e38",
    opacity="EMERE-DIEL",
    name="FR-5 (High-temp Glass Epoxy)",
    cond_thermal=0.35,
    density=1900,
    specific_heat=1100,
)
DIEL_FR6 = Material(
    er=5.2,
    tand=0.030,
    color="#145a32",
    opacity="EMERE-DIEL",
    name="FR-6 (Paper Resin, Low Thermal)",
    cond_thermal=0.15,
    density=1400,
    specific_heat=1400,
)

# Magnetic Materials
MU_METAL = Material(
    cond=1.0e6,
    ur=200000,
    color="#666680",
    opacity="EMERE-DIEL",
    name="Mu-metal",
    cond_thermal=10.9,
    density=8747,
    specific_heat=500,
)

############################################################
#                           FOAMS                          #
############################################################

# Foam thermal properties: very low conductivity (insulating), low density.
# Specific heat is for the base polymer (PMI ~1100, EPS/XPS ~1300, PU ~1500,
# PVC ~900, PET ~1200, glass ~800 J/(kg·K)).

FOAM_ROHACELL_31 = Material(
    er=1.05,
    tand=0.0005,
    color="#f0e1a1",
    opacity=0.15,
    name="Rohacell 31 (PMI Foam)",
    cond_thermal=0.031,
    density=32,
    specific_heat=1100,
)
FOAM_ROHACELL_51 = Material(
    er=1.07,
    tand=0.0006,
    color="#f0dea0",
    opacity=0.15,
    name="Rohacell 51 (PMI Foam)",
    cond_thermal=0.033,
    density=52,
    specific_heat=1100,
)
FOAM_ROHACELL_71 = Material(
    er=1.10,
    tand=0.0007,
    color="#e5d199",
    opacity=0.15,
    name="Rohacell 71 (PMI Foam)",
    cond_thermal=0.036,
    density=75,
    specific_heat=1100,
)

FOAM_PEI = Material(
    er=1.15,
    tand=0.0035,
    color="#e0b56f",
    opacity=0.15,
    name="PEI Foam",
    cond_thermal=0.035,
    density=60,
    specific_heat=1100,
)
FOAM_PMI = Material(
    er=1.10,
    tand=0.0008,
    color="#d9c690",
    opacity=0.15,
    name="PMI Foam",
    cond_thermal=0.034,
    density=52,
    specific_heat=1100,
)
FOAM_PVC = Material(
    er=1.20,
    tand=0.0040,
    color="#cccccc",
    opacity=0.15,
    name="PVC Foam",
    cond_thermal=0.035,
    density=80,
    specific_heat=900,
)
FOAM_EPS = Material(
    er=1.03,
    tand=0.0050,
    color="#f7f7f7",
    opacity=0.15,
    name="EPS Foam (Expanded Polystyrene)",
    cond_thermal=0.036,
    density=25,
    specific_heat=1300,
)
FOAM_XPS = Material(
    er=1.05,
    tand=0.0030,
    color="#e0e0e0",
    opacity=0.15,
    name="XPS Foam (Extruded Polystyrene)",
    cond_thermal=0.034,
    density=35,
    specific_heat=1300,
)
FOAM_PU = Material(
    er=1.10,
    tand=0.0080,
    color="#d0d0d0",
    opacity=0.15,
    name="PU Foam (Polyurethane)",
    cond_thermal=0.026,
    density=35,
    specific_heat=1500,
)
FOAM_GLAS = Material(
    er=3.10,
    tand=0.0050,
    color="#888888",
    opacity=0.15,
    name="Cellular Glass",
    cond_thermal=0.040,
    density=120,
    specific_heat=800,
)

FOAM_AIREX_C70 = Material(
    er=1.10,
    tand=0.0010,
    color="#f7e7a3",
    opacity=0.15,
    name="Airex C70 (PET Foam)",
    cond_thermal=0.034,
    density=60,
    specific_heat=1200,
)
FOAM_AIREX_T92 = Material(
    er=1.10,
    tand=0.0020,
    color="#f6d08a",
    opacity=0.15,
    name="Airex T92 (PET Foam)",
    cond_thermal=0.036,
    density=85,
    specific_heat=1200,
)
FOAM_PVC_CORECELL = Material(
    er=1.56,
    tand=0.0025,
    color="#aaaaaa",
    opacity=0.15,
    name="Corecell PVC Foam",
    cond_thermal=0.038,
    density=100,
    specific_heat=900,
)
