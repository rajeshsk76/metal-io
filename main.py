#!/usr/bin/env python3
"""
Critical Metals Value Chain + Real Data Matrix
Green Industry Focus
"""

import pandas as pd
from pathlib import Path

# ============================================================
# 1. OFFICIAL USGS 2025 LIST OF 60 CRITICAL MINERALS
# ============================================================
CRITICAL_MINERALS_2025 = [
    "Aluminum", "Antimony", "Arsenic", "Barite", "Beryllium", "Bismuth", "Boron",
    "Cerium", "Cesium", "Chromium", "Cobalt", "Copper", "Dysprosium", "Erbium",
    "Europium", "Fluorspar", "Gadolinium", "Gallium", "Germanium", "Graphite",
    "Hafnium", "Holmium", "Indium", "Iridium", "Lanthanum", "Lead", "Lithium",
    "Lutetium", "Magnesium", "Manganese", "Metallurgical coal", "Neodymium",
    "Nickel", "Niobium", "Palladium", "Phosphate", "Platinum", "Potash",
    "Praseodymium", "Rhenium", "Rhodium", "Rubidium", "Ruthenium", "Samarium",
    "Scandium", "Silicon", "Silver", "Tantalum", "Tellurium", "Terbium",
    "Thulium", "Tin", "Titanium", "Tungsten", "Uranium", "Vanadium",
    "Ytterbium", "Yttrium", "Zinc", "Zirconium"
]

print(f"✅ Loaded {len(CRITICAL_MINERALS_2025)} critical minerals from USGS 2025 list.\n")

# ============================================================
# 2. STANDARD VALUE CHAIN STAGES
# ============================================================
STAGES = [
    "1. Deposit Type / Geology",
    "2. Mining / Extraction",
    "3. Concentration / Beneficiation",
    "4. Intermediate Processing / Smelting",
    "5. Refining / Chemical Processing",
    "6. Final Market Product"
]

# ============================================================
# 3. DETAILED VALUE CHAINS (10 Key Green Metals)
# ============================================================
value_chains = {
    "Lithium": [
        "Pegmatite (hard rock spodumene) or Lithium-rich brine in salars",
        "Open-pit mining of pegmatite or pumping of lithium-rich brine",
        "Hard rock: Crushing + flotation → Spodumene concentrate (5.5–6.5% Li₂O)\nBrine: Solar evaporation ponds",
        "Hard rock: Sulfuric acid roasting + leaching\nBrine: Direct Lithium Extraction (DLE)",
        "Conversion to battery-grade Lithium Carbonate (Li₂CO₃) or Lithium Hydroxide (LiOH)",
        "Battery-grade Lithium Carbonate or Lithium Hydroxide"
    ],
    "Cobalt": [
        "Sediment-hosted copper-cobalt deposits or nickel laterite by-product",
        "Open-pit or underground mining of copper-cobalt ore",
        "Crushing, grinding, flotation or leaching → Mixed Hydroxide Precipitate (MHP)",
        "Smelting or HPAL → Cobalt matte or mixed sulfide/hydroxide",
        "Solvent extraction + electrowinning → Cobalt sulfate (CoSO₄) or high-purity metal",
        "Cobalt Sulfate or Cobalt Metal"
    ],
    "Nickel": [
        "Laterite (oxide) or Magmatic sulfide deposits",
        "Open-pit (laterite) or underground (sulfide) mining",
        "Laterite: HPAL or ferronickel smelting\nSulfide: Froth flotation → Nickel concentrate",
        "Laterite: HPAL → Mixed Hydroxide Precipitate (MHP)\nSulfide: Flash smelting → Nickel matte",
        "Refining of matte/MHP → Class 1 Nickel or Nickel Sulfate",
        "Class 1 Nickel or Nickel Sulfate"
    ],
    "Graphite (Natural)": [
        "Flake graphite in metamorphic rocks (schist, gneiss)",
        "Open-pit or underground mining of graphite ore",
        "Crushing, grinding, flotation → Flake graphite concentrate (80–95% C)",
        "Spheronization + purification (acid/thermal) to >99.9% C",
        "Coating / surface treatment for battery anodes",
        "Battery-grade Spherical Graphite or Purified Flake Graphite"
    ],
    "Copper": [
        "Porphyry copper deposits, sediment-hosted, or VMS",
        "Open-pit (most common) or underground mining",
        "Crushing, grinding, froth flotation → Copper concentrate (20–30% Cu)",
        "Smelting → Copper matte then blister copper (98–99%)",
        "Electrolytic refining (electrorefining) → 99.99% pure Copper Cathode",
        "Copper Cathode (99.99% Cu)"
    ],
    "Manganese": [
        "Sedimentary manganese deposits or lateritic weathering",
        "Open-pit mining of manganese ore",
        "Crushing, screening, gravity/magnetic separation → Manganese concentrate",
        "Smelting in electric arc furnace → Ferromanganese or Silicomanganese",
        "Electrolytic process → Electrolytic Manganese Metal (EMM) or Manganese Sulfate",
        "EMM or Manganese Sulfate"
    ],
    "Silicon (Metallurgical/Solar)": [
        "Quartzite or high-purity quartz deposits",
        "Open-pit mining of quartzite",
        "Crushing and screening to quartz lumps",
        "Carbothermic reduction in submerged arc furnace → Metallurgical Grade Silicon (MG-Si)",
        "Siemens process or fluidized bed reactor → Solar Grade Silicon",
        "MG-Si or Solar Grade Silicon"
    ],
    "Aluminum": [
        "Bauxite deposits (lateritic weathering)",
        "Open-pit mining of bauxite ore",
        "Crushing, washing, screening → Bauxite concentrate",
        "Bayer process → Alumina (Al₂O₃)",
        "Hall-Héroult process → Primary Aluminum metal",
        "Primary Aluminum ingots / billets"
    ],
    "Neodymium (Rare Earth)": [
        "Carbonatite or alkaline igneous deposits (bastnäsite, monazite)",
        "Open-pit or underground mining of rare earth ore",
        "Crushing, grinding, flotation/gravity separation → Rare earth concentrate",
        "Cracking / leaching → Mixed rare earth solution or carbonate",
        "Solvent extraction → Neodymium oxide / metal",
        "Neodymium Metal or NdFeB magnet alloy"
    ],
    "Zinc": [
        "Sediment-hosted massive sulfide (SHMS), VMS, or MVT deposits",
        "Underground or open-pit mining of zinc ore (sphalerite)",
        "Crushing, grinding, froth flotation → Zinc concentrate (50–60% Zn)",
        "Roasting → Zinc oxide, then leaching → Zinc sulfate solution",
        "Electrowinning → High-purity Zinc metal cathodes",
        "Special High Grade (SHG) Zinc (99.995% Zn)"
    ]
}

# ============================================================
# 4. REAL DATA (Production, Countries, Companies, Reserves)
# ============================================================
real_data = {
    "Lithium": {
        "World Production (2025)": "290,000 tons (lithium content)",
        "Top Producing Countries": "Australia (~36%), China (~17%), Chile (~20%), Argentina, Zimbabwe",
        "Major Companies / Mines": "Albemarle, SQM, Ganfeng Lithium, Tianqi Lithium, Pilbara Minerals",
        "World Reserves": "~30 million tons"
    },
    "Cobalt": {
        "World Production (2024)": "290,000 tons (mine production)",
        "Top Producing Countries": "DRC (~74-76%), Indonesia, Australia, Russia",
        "Major Companies / Mines": "Glencore, China Molybdenum (Tenke Fungurume), Eurasian Resources Group",
        "World Reserves": "~11 million tons"
    },
    "Nickel": {
        "World Production (2025)": "~3.9 million tons",
        "Top Producing Countries": "Indonesia (~53%), Philippines (~18%), Russia, Australia",
        "Major Companies / Mines": "Tsingshan, Vale, BHP, Norilsk Nickel",
        "World Reserves": "~140 million tons"
    },
    "Graphite (Natural)": {
        "World Production (2025)": "~1.4 – 1.8 million tons",
        "Top Producing Countries": "China (~78%), Brazil, Mozambique, Canada",
        "Major Companies / Mines": "China Northern Graphite, Syrah Resources, Imerys",
        "World Reserves": "China dominant"
    },
    "Copper": {
        "World Production (2025)": "~23 million tons (mine)",
        "Top Producing Countries": "Chile (~28%), Peru (~12%), DRC (~10%), United States",
        "Major Companies / Mines": "Codelco, Freeport-McMoRan, BHP, Glencore, Rio Tinto",
        "World Reserves": "~870 million tons"
    },
    "Manganese": {
        "World Production (2025)": "~21 million tons",
        "Top Producing Countries": "South Africa (~33%), Gabon (~17%), Australia (~15%), China",
        "Major Companies / Mines": "South32, Assmang, Eramet, Ningxia Tianyuan",
        "World Reserves": "~1.8 billion tons"
    },
    "Silicon (Metal)": {
        "World Production (2025)": "Significant; China dominant",
        "Top Producing Countries": "China (~69-85%), Norway, Russia, Brazil",
        "Major Companies / Mines": "China state-linked, Elkem, Ferroglobe",
        "World Reserves": "Abundant"
    },
    "Aluminum (Bauxite)": {
        "World Production (2025)": "~110 million tons (bauxite)",
        "Top Producing Countries": "Australia (~34%), Guinea (~14%), Brazil (~10%), China",
        "Major Companies / Mines": "Rio Tinto, Alcoa, Rusal, Chalco",
        "World Reserves": "~55–75 billion tons"
    },
    "Neodymium (Rare Earths)": {
        "World Production (2025)": "~390,000 tons REO total",
        "Top Producing Countries": "China (~60-70%), United States, Australia, Myanmar",
        "Major Companies / Mines": "China Northern Rare Earth, MP Materials, Lynas",
        "World Reserves": "China holds ~44 million tons REO"
    },
    "Zinc": {
        "World Production (2025)": "~12 million tons",
        "Top Producing Countries": "China (~31%), Peru (~14%), Australia (~10%), India",
        "Major Companies / Mines": "Glencore, Teck Resources, Boliden, Hindustan Zinc",
        "World Reserves": "~200–250 million tons"
    }
}

print("✅ Real data added for 10 key green industry metals.\n")

# ============================================================
# 5. BUILD DATAFRAMES
# ============================================================
def build_value_chain_matrix(value_chains_dict, stages_list):
    data = {}
    for metal, chain in value_chains_dict.items():
        if len(chain) != len(stages_list):
            chain = chain[:len(stages_list)] + [""] * (len(stages_list) - len(chain))
        data[metal] = chain
    df = pd.DataFrame(data, index=stages_list)
    df.index.name = "Value Chain Stage"
    return df

df_value_chain = build_value_chain_matrix(value_chains, STAGES)

real_data_rows = []
for metal, data in real_data.items():
    real_data_rows.append({
        "Metal": metal,
        "World Production (latest)": data.get("World Production (2025)", data.get("World Production (2024)", "N/A")),
        "Top Producing Countries": data["Top Producing Countries"],
        "Major Companies / Mines": data["Major Companies / Mines"],
        "World Reserves": data["World Reserves"]
    })

df_real_data = pd.DataFrame(real_data_rows)

# ============================================================
# 6. SAVE TO CSV (Correct path for current project)
# ============================================================
output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

df_value_chain.to_csv(output_dir / "critical_metals_value_chain_matrix.csv", encoding="utf-8-sig")
df_real_data.to_csv(output_dir / "critical_metals_real_data.csv", index=False, encoding="utf-8-sig")

print("✅ Files saved successfully in data/ folder:")
print(f"   - data/critical_metals_value_chain_matrix.csv")
print(f"   - data/critical_metals_real_data.csv\n")

# ============================================================
# 7. DISPLAY RESULTS
# ============================================================
print("=" * 100)
print("CRITICAL METALS VALUE CHAIN MATRIX (Green Industry Focus)")
print("=" * 100)
print(df_value_chain.to_string())
print("\n" + "=" * 100)

print("\nREAL DATA TABLE (Production, Countries, Companies, Reserves)")
print("=" * 100)
print(df_real_data.to_string(index=False))
print("\n" + "=" * 100)

print("\n✅ Script completed successfully.")
print("Next: We can expand to more metals, add visualizations, or build the Input-Output model.")
