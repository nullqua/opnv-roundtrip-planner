# 🚍 ÖPNV Roundtrip Planner

> Ein intelligenter Routenplaner für Rundtouren im öffentlichen Nahverkehr
> 
> *An intelligent route planner for roundtrips on public transit*

![Status](https://img.shields.io/badge/status-in%20development-yellow)
[![License:  MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 🇩🇪 Deutsch

### Das Problem

Herkömmliche Routing-Apps suchen den **kürzesten Weg von A nach B**. 
Diese App löst ein anderes Problem: 

> _"Ich möchte genau **60 Minuten** Bus/Bahn fahren und am Ende wieder an meinem **Startpunkt** ankommen."_

### Use Cases
- Entspanntes Sightseeing ohne festes Ziel
- Stadtentdeckung mit fester Zeitbegrenzung
- "Digital Detox" Fahrten mit Aussicht
- Leute, die einfach gerne Bus/Bahn fahren

### Technologie
- **Frontend:** React + TypeScript (Vite)
- **Backend:** Python + FastAPI
- **Daten:** GTFS-Fahrplandaten (beschränkt auf Bielefeld)

---

## 🇬🇧 English

### The Problem

Conventional routing apps find the **shortest path from A to B**. 
This app solves a different problem:

> _"I want to ride the bus/train for exactly **60 minutes** and end up back at my **starting point**."_

### Use Cases
- Relaxed sightseeing without a fixed destination
- City exploration with a time limit
- "Digital detox" rides with a view
- People who just love riding the bus or subway

### Technology
- **Frontend:** React + TypeScript (Vite)
- **Backend:** Python + FastAPI
- **Data:** GTFS schedule data (for now only Bielefeld)

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/nullqua/opnv-roundtrip-planner. git

# Backend
cd backend
pip install -r requirements. txt
uvicorn src.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

## License

MIT © nullqua 2025
