---
name: system-indexer
description: "MUST read before any task that involves understanding the overall system architecture, finding the right skill for a task, or adding new skills/projects to the system. This skill manages the central knowledge graph of the Manus System Brain — the single source of truth that connects all skills, projects, and connectors. Use when: asked 'what skills do we have?', 'how does X connect to Y?', 'add a new project to the system', or 'update the knowledge graph'."
---

# System Indexer

## Systemgedanke (Pflichtlektüre)

Lies zuerst `SYSTEM.md` im Root des `manus-system-brain` Repositories. Der Systemgedanke ist: **Alles ist ein Knoten im zentralen Wissensgraphen. Nichts ist eine Insel.**

Das Manus System Brain ist ein hierarchisches System:

```
manus-system-brain (Kern)
├── skills/                    ← Universelle Manus-Skills (20 Stück)
├── projects/                  ← Projekt-Satelliten
│   └── salon-website/         ← Salon-Website + 6 Projekt-Skills
├── knowledge-graph/           ← Der zentrale Wissensgraph
│   ├── graph.json             ← Maschinenlesbar (NetworkX node-link)
│   ├── GRAPH_REPORT.md        ← Menschenlesbar
│   ├── build_graph.py         ← Graph neu aufbauen
│   └── sync_and_push.py       ← Auto-Sync (täglich 03:00 Uhr)
└── SYSTEM.md                  ← Der unveränderliche Systemgedanke
```

## Wann diesen Skill nutzen

Nutze diesen Skill wenn:
- Eine neue Session beginnt und du den Systemkontext verstehen musst
- Du wissen willst, welche Skills für eine Aufgabe existieren
- Du ein neues Projekt oder einen neuen Skill ins System integrieren willst
- Du den Graphen abfragen willst um Zusammenhänge zu verstehen

## Workflow

### 1. Systemkontext laden
```python
import json
import networkx as nx
from networkx.readwrite import json_graph
from pathlib import Path

# Wissensgraph laden
graph_path = Path("/home/ubuntu/manus-system-brain/knowledge-graph/graph.json")
with open(graph_path) as f:
    G = json_graph.node_link_graph(json.load(f), edges="links")

# Alle Projekte
projects = [(n, d["label"]) for n, d in G.nodes(data=True) if d.get("type") == "project"]
# Alle universellen Skills
skills = [(n, d["label"]) for n, d in G.nodes(data=True) if d.get("type") == "skill" and d.get("layer") == "manus"]
# Skills eines Projekts
salon_skills = list(G.neighbors("project:salon-website"))
```

### 2. Neues Projekt registrieren
Wenn ein neues Projekt (z.B. eine neue Website oder App) erstellt wird:
1. Erstelle `projects/<name>/README.md` mit Repo-Link und Beschreibung
2. Füge die Projekt-Skills unter `projects/<name>/skills/` hinzu
3. Füge das Projekt in `build_graph.py` unter `PROJECT_USES_SKILLS` ein
4. Führe `python3 knowledge-graph/build_graph.py` aus
5. Führe `python3 knowledge-graph/sync_and_push.py` aus

### 3. Neuen universellen Skill registrieren
Wenn ein neuer Manus-Skill importiert wird:
1. Der Skill liegt automatisch in `/home/ubuntu/skills/`
2. Füge ihn in `build_graph.py` unter `MANUS_SKILL_CATEGORIES` ein
3. Führe `python3 knowledge-graph/sync_and_push.py` aus

### 4. Wissensgraph manuell aktualisieren
```bash
cd /home/ubuntu/manus-system-brain
python3 knowledge-graph/sync_and_push.py
```

## GitHub-Repositories

| Repository | Zweck | Sichtbarkeit |
|---|---|---|
| `Friseurehattstedt/manus-system-brain` | Vollständiges System-Archiv | öffentlich |
| `Friseurehattstedt/manus-skill-system-indexer` | Importierbarer Manus-Skill | öffentlich |
| `Friseurehattstedt/salon-astro-website` | Salon-Website (Satellit) | privat |
