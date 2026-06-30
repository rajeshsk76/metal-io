"""Production, geography, and reserves data for green metals (keyed by metal id)."""

MARKET_DATA: dict[str, dict[str, str]] = {
    "lithium": {
        "World Production (2025)": "290,000 tons (lithium content)",
        "Top Producing Countries": "Australia (~36%), China (~17%), Chile (~20%), Argentina, Zimbabwe",
        "Major Companies / Mines": "Albemarle, SQM, Ganfeng Lithium, Tianqi Lithium, Pilbara Minerals",
        "World Reserves": "~30 million tons",
    },
    "cobalt": {
        "World Production (2024)": "290,000 tons (mine production)",
        "Top Producing Countries": "DRC (~74-76%), Indonesia, Australia, Russia",
        "Major Companies / Mines": "Glencore, China Molybdenum (Tenke Fungurume), Eurasian Resources Group",
        "World Reserves": "~11 million tons",
    },
    "nickel": {
        "World Production (2025)": "~3.9 million tons",
        "Top Producing Countries": "Indonesia (~53%), Philippines (~18%), Russia, Australia",
        "Major Companies / Mines": "Tsingshan, Vale, BHP, Norilsk Nickel",
        "World Reserves": "~140 million tons",
    },
    "graphite": {
        "World Production (2025)": "~1.4 – 1.8 million tons",
        "Top Producing Countries": "China (~78%), Brazil, Mozambique, Canada",
        "Major Companies / Mines": "China Northern Graphite, Syrah Resources, Imerys",
        "World Reserves": "China dominant",
    },
    "copper": {
        "World Production (2025)": "~23 million tons (mine)",
        "Top Producing Countries": "Chile (~28%), Peru (~12%), DRC (~10%), United States",
        "Major Companies / Mines": "Codelco, Freeport-McMoRan, BHP, Glencore, Rio Tinto",
        "World Reserves": "~870 million tons",
    },
    "manganese": {
        "World Production (2025)": "~21 million tons",
        "Top Producing Countries": "South Africa (~33%), Gabon (~17%), Australia (~15%), China",
        "Major Companies / Mines": "South32, Assmang, Eramet, Ningxia Tianyuan",
        "World Reserves": "~1.8 billion tons",
    },
    "silicon": {
        "World Production (2025)": "Significant; China dominant",
        "Top Producing Countries": "China (~69-85%), Norway, Russia, Brazil",
        "Major Companies / Mines": "China state-linked, Elkem, Ferroglobe",
        "World Reserves": "Abundant",
    },
    "aluminum": {
        "World Production (2025)": "~110 million tons (bauxite)",
        "Top Producing Countries": "Australia (~34%), Guinea (~14%), Brazil (~10%), China",
        "Major Companies / Mines": "Rio Tinto, Alcoa, Rusal, Chalco",
        "World Reserves": "~55–75 billion tons",
    },
    "neodymium": {
        "World Production (2025)": "~390,000 tons REO total",
        "Top Producing Countries": "China (~60-70%), United States, Australia, Myanmar",
        "Major Companies / Mines": "China Northern Rare Earth, MP Materials, Lynas",
        "World Reserves": "China holds ~44 million tons REO",
    },
    "zinc": {
        "World Production (2025)": "~12 million tons",
        "Top Producing Countries": "China (~31%), Peru (~14%), Australia (~10%), India",
        "Major Companies / Mines": "Glencore, Teck Resources, Boliden, Hindustan Zinc",
        "World Reserves": "~200–250 million tons",
    },
}