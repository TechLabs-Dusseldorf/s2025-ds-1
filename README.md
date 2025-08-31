# Global Electricity Production Analysis

**Team:** Group 1 – TechLabs Düsseldorf (Spring 2025)  
**Dataset:** Global Electricity Production (Kaggle, 2010–2023)  
**Scenario:** Commissioned by the **Global Energy Alliance (GEA)** for the annual *Global Energy Outlook*.

---

## Project Overview
We analyze historical electricity production by **country** and **energy source** to surface:
- global trends,
- top producers,
- energy mix dynamics,
- renewable growth (YoY).

Outputs are **policy-relevant** insights for sustainability and energy security.

---

## Tech Stack
- **Python** 3.11+
- **Libraries:** `pandas`, `matplotlib`
- **Collaboration:** GitHub
- **Presentation (optional):** Jupyter Notebook, PowerPoint, Streamlit*

> *Streamlit planned for future interactive dashboards.

---

## Structure
```bash
s2025-ds-1/
├── data/
│ └── global_electricity_production_data.csv
├── outputs/ # plots (ignored by git)
├── py_files/
│ ├── clean_code.py # utils: load/clean/aggregate/plot
│ └── main.py # CLI runner
├── notebooks/ # explorations
├── requirements.txt
├── .gitignore
└── README.md
```
---

## How to Run

# Environment
```bash
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

# quick run (no plots)
```bash
python py_files/main.py --no-plot
```

# show plots
```bash
python py_files/main.py
```

# save plots
```bash
mkdir -p outputs
python py_files/main.py \
  --save-plot outputs/yearly_total.png \
  --save-solar-wind outputs/solar_wind.png
```

---

## Key Findings (Beginner Phase)

2010 → 2023: ~+9% global production (≈40.5M → 44.1M GWh).  

- **Balances:** Net Production dominates; imports/exports smaller but strategically relevant.  
- **Top Producers:** USA, China, Japan, India, Canada (~half of global total).  
- **Mix:** Combustible fuels & coal/peat are large but slowly declining.  
- **Renewables:** ~4× growth (2010: 1.96M GWh → 2023: 7.67M GWh).  
  - Hydro largest (≈37.2M GWh total).  
  - Wind (~14.9M GWh) & Solar (~6.8M GWh) fastest growing.  

---

## Next Steps

- YoY renewable growth by country  
- Energy mix shifts (developed vs. developing)  
- Fossil dependence vs. renewable integration  
- Seasonality (Hydro in Norway, Solar in Australia, etc.)  

---

## Contributors

**Group 1 — TechLabs Düsseldorf Spring 2025**  
- Tanju Coskun  
- Elnaz Shishegaran  
- Desmond  
- Alkan  

**Mentors**  
- Moritz Dahm  
- Nopparat Wasikanon
