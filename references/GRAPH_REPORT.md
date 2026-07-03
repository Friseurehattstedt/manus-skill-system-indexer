# Manus System Brain — Wissensgraph-Bericht

> **Für jeden KI-Agenten:** Lies zuerst `SYSTEM.md` um den Systemgedanken zu verstehen. Dieser Bericht ist der operative Überblick.

> Generiert: 2026-07-03 15:47 | Knoten: **49** | Kanten: **83** | Manus-Skills: **20** | Projekt-Skills: **11** | Projekte: **1** | Konnektoren: **12**

---

## Systemarchitektur

Das System besteht aus drei Ebenen, die alle im Graphen verbunden sind:

| Ebene | Was | Anzahl |
|---|---|:---:|
| **Kern** | Manus System Brain (dieses Repo) | 1 |
| **Universelle Skills** | Plattformübergreifende Fähigkeiten | 20 |
| **Projekte** | Spezifische Anwendungen (z.B. Salon-Website) | 1 |
| **Projekt-Skills** | Projektspezifische Fähigkeiten | 11 |
| **Konnektoren** | Externe APIs und Integrationen | 12 (2 aktiv) |

---

## Universelle Manus-Skills

### SEO & Marketing

| Skill | Beschreibung | Scripts | Wörter |
|---|---|:---:|---:|
| **backlink-analysis** |  |  | 2,547 |
| **content-gap-analysis** |  | ✓ | 4,638 |
| **keyword-research** |  | ✓ | 1,199 |
| **seo-audit** |  | ✓ | 3,194 |
| **seo-competitor-analysis** |  | ✓ | 1,477 |
| **similarweb-analytics** |  |  | 518 |
| **website-traffic-checker** |  |  | 1,750 |

### System & Infrastruktur

| Skill | Beschreibung | Scripts | Wörter |
|---|---|:---:|---:|
| **automation-and-scheduling** |  |  | 2,654 |
| **builtin-llm-models** |  | ✓ | 1,779 |
| **internet-skill-finder** |  | ✓ | 212 |
| **manus-api** |  |  | 1,257 |
| **manus-config** |  |  | 1,365 |
| **persistent-computing** |  |  | 1,262 |
| **skill-creator** |  | ✓ | 1,425 |
| **system-indexer** |  | ✓ | 440 |

### Medien & Kreation

| Skill | Beschreibung | Scripts | Wörter |
|---|---|:---:|---:|
| **imagegen** |  |  | 2,330 |
| **music-prompter** |  |  | 1,742 |
| **tts-prompter** |  |  | 2,485 |

### Integrationen

| Skill | Beschreibung | Scripts | Wörter |
|---|---|:---:|---:|
| **github-gem-seeker** |  |  | 650 |
| **gws-best-practices** |  |  | 747 |

---

## Projekte

### Salon OS — Die Friseure Gumbert & Partner

**Repo:** `Friseurehattstedt/salon-os` | **Beschreibung:** **GitHub-Repo:** `Friseurehattstedt/salon-os` (privat)

**Projekt-spezifische Skills:**

- **brandkit** — 
- **emil-design-eng** — 
- **extract-design-system** — 
- **image-to-code** — 
- **review-animations** — 
- **ui-ux-pro-max** — 
- **brand** — 
- **design** — 
- **design-system** — 
- **ui-styling** — 
- **web-design-guidelines** — 

**Nutzt universelle Skills:** seo-audit, content-gap-analysis, keyword-research, website-traffic-checker, backlink-analysis, imagegen, automation-and-scheduling

---

## Zentrale Knoten (höchste Vernetzung)

| Rang | Knoten | Typ | Ebene | Verbindungen |
|:---:|---|---|---|:---:|
| 1 | **Salon OS — Die Friseure Gumbert & Partner** | project | unternehmens-os | 19 |
| 2 | **website-traffic-checker** | skill | manus | 10 |
| 3 | **System & Infrastruktur** | category | manus | 9 |
| 4 | **SEO & Marketing** | category | manus | 8 |
| 5 | **automation-and-scheduling** | skill | manus | 7 |
| 6 | **keyword-research** | skill | manus | 7 |
| 7 | **manus-api** | skill | manus | 7 |
| 8 | **backlink-analysis** | skill | manus | 6 |
| 9 | **seo-audit** | skill | manus | 6 |
| 10 | **skill-creator** | skill | manus | 6 |

---

## Aktive Konnektoren

| Konnektor | Beschreibung |
|---|---|
| **GitHub** | Manage repositories, track code changes, and collaborate on team projects |
| **OpenAI** | Leverage GPT model series for intelligent text generation and processing |

---

## Für KI-Agenten: Graph abfragen

```python
import json, networkx as nx
from networkx.readwrite import json_graph

with open('knowledge-graph/graph.json') as f:
    G = json_graph.node_link_graph(json.load(f), edges='links')

# Alle Projekte
projects = [d['label'] for _,d in G.nodes(data=True) if d.get('type')=='project']
# Skills eines Projekts
skills = list(G.neighbors('project:salon-website'))
# Kürzester Pfad
path = nx.shortest_path(G, 'project:salon-website', 'connector:ahrefs')
```
