---
name: system-indexer
description: >
  Verwaltet und aktualisiert den zentralen Wissensgraphen des Manus-Systems (System Brain).
  Nutze diesen Skill wenn: neue Skills hinzugefügt wurden, Konnektoren geändert wurden,
  du den Überblick über alle verfügbaren Skills und ihre Verbindungen brauchst,
  oder du den Graphen abfragen möchtest um den richtigen Skill für eine Aufgabe zu finden.
  Enthält den Wissensgraphen als graph.json (NetworkX-Format) und GRAPH_REPORT.md.
---

# System Indexer

Dieser Skill ist das Gedächtnis des Manus-Systems. Er verwaltet den Wissensgraphen, der alle Skills, Konnektoren und ihre Beziehungen beschreibt.

## Schnellzugriff

Für einen sofortigen Überblick: Lies `knowledge-graph/GRAPH_REPORT.md`.

Für programmatische Abfragen: Nutze `knowledge-graph/graph.json` mit NetworkX.

## Wann diesen Skill nutzen

- **Vor komplexen Aufgaben**: Prüfe, welche Skills und Konnektoren relevant sind.
- **Nach Änderungen**: Wenn ein neuer Skill hinzugefügt oder ein Konnektor aktiviert wurde.
- **Für Routing**: Um den kürzesten Pfad von einer Aufgabe zum richtigen Skill zu finden.

## Wissensgraph aktualisieren

```bash
python3 knowledge-graph/build_graph.py
```

Das Skript liest automatisch alle `SKILL.md`-Dateien und die Konnektor-Konfiguration und baut den Graphen neu auf.

## Graphen abfragen (Python)

```python
import json
import networkx as nx
from networkx.readwrite import json_graph

with open("knowledge-graph/graph.json") as f:
    G = json_graph.node_link_graph(json.load(f), edges="links")

# Alle Skills anzeigen
skills = [(n, d["label"]) for n, d in G.nodes(data=True) if d.get("type") == "skill"]

# Nachbarn eines Skills (verwandte Skills/Konnektoren)
neighbors = list(G.neighbors("skill:seo-audit"))

# Kürzester Pfad zwischen zwei Knoten
path = nx.shortest_path(G, "skill:content-gap-analysis", "connector:ahrefs")
```

## Graphen-Struktur

Der Graph enthält folgende Knotentypen:

| Typ | Beschreibung | Beispiel |
|---|---|---|
| `skill` | Ein Manus-Skill | `skill:seo-audit` |
| `connector` | Eine externe API/Integration | `connector:ahrefs` |
| `category` | Übergeordnete Kategorie | `category:seo` |
| `system` | Das Gesamtsystem | `system:manus-os` |

Kantentypen: `BELONGS_TO`, `COMPLEMENTS`, `USED_BY`, `CONTAINS`
