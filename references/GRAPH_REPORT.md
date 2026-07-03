# Manus System Brain — Knowledge Graph Report

> Automatisch generiert von `knowledge-graph/build_graph.py`  
> Knoten: **35** | Kanten: **65** | Skills: **19** | Konnektoren: **11**

---

## Überblick

Dieses System besteht aus **19 Skills** und **11 Konnektoren** (2 aktiv). Der Wissensgraph enthält 35 Knoten und 65 semantische Verbindungen.

---

## Skills nach Kategorie

### SEO & Marketing

| Skill | Beschreibung | Scripts | Refs | Wörter |
|---|---|:---:|:---:|---:|
| **backlink-analysis** |  |  | ✓ | 2,547 |
| **content-gap-analysis** |  | ✓ | ✓ | 4,638 |
| **keyword-research** |  | ✓ | ✓ | 1,199 |
| **seo-audit** |  | ✓ | ✓ | 3,194 |
| **seo-competitor-analysis** |  | ✓ | ✓ | 1,477 |
| **similarweb-analytics** |  |  |  | 518 |
| **website-traffic-checker** |  |  | ✓ | 1,750 |

### System & Infrastruktur

| Skill | Beschreibung | Scripts | Refs | Wörter |
|---|---|:---:|:---:|---:|
| **automation-and-scheduling** |  |  | ✓ | 2,654 |
| **builtin-llm-models** |  | ✓ |  | 1,779 |
| **internet-skill-finder** |  | ✓ | ✓ | 212 |
| **manus-api** |  |  |  | 1,257 |
| **manus-config** |  |  |  | 1,365 |
| **persistent-computing** |  |  | ✓ | 1,262 |
| **skill-creator** |  | ✓ | ✓ | 1,425 |

### Medien & Kreation

| Skill | Beschreibung | Scripts | Refs | Wörter |
|---|---|:---:|:---:|---:|
| **imagegen** |  |  | ✓ | 2,330 |
| **music-prompter** |  |  |  | 1,742 |
| **tts-prompter** |  |  |  | 2,485 |

### Integrationen & Tools

| Skill | Beschreibung | Scripts | Refs | Wörter |
|---|---|:---:|:---:|---:|
| **github-gem-seeker** |  |  |  | 650 |
| **gws-best-practices** |  |  |  | 747 |

---

## Zentrale Knoten (höchste Vernetzung)

Die folgenden Knoten haben die meisten Verbindungen im Graphen — sie sind die kritischsten Teile des Systems:

| Rang | Knoten | Typ | Verbindungen |
|:---:|---|---|:---:|
| 1 | **website-traffic-checker** | skill | 10 |
| 2 | **SEO & Marketing** | category | 8 |
| 3 | **System & Infrastruktur** | category | 8 |
| 4 | **automation-and-scheduling** | skill | 7 |
| 5 | **manus-api** | skill | 7 |
| 6 | **keyword-research** | skill | 6 |
| 7 | **skill-creator** | skill | 6 |
| 8 | **backlink-analysis** | skill | 5 |
| 9 | **seo-audit** | skill | 5 |
| 10 | **content-gap-analysis** | skill | 4 |

---

## Aktive Konnektoren

| Konnektor | Beschreibung |
|---|---|
| **GitHub** | Manage repositories, track code changes, and collaborate on team projects |
| **OpenAI** | Leverage GPT model series for intelligent text generation and processing |

---

## Skill-Verbindungen (Synergien)

Diese Skills ergänzen sich gegenseitig und sollten kombiniert eingesetzt werden:

- **`seo-audit`** → `backlink-analysis` + `website-traffic-checker`
- **`content-gap-analysis`** → `keyword-research` + `seo-competitor-analysis`
- **`manus-api`** → `automation-and-scheduling` + `manus-config`
- **`imagegen`** → `tts-prompter` + `music-prompter`

---

## Für KI-Modelle: Wie dieser Graph genutzt wird

```
# Graphen laden und abfragen (Python/NetworkX)
import json
import networkx as nx
from networkx.readwrite import json_graph

with open('knowledge-graph/graph.json') as f:
    G = json_graph.node_link_graph(json.load(f), edges='links')

# Alle Skills finden
skills = [d['label'] for _, d in G.nodes(data=True) if d.get('type') == 'skill']

# Nachbarn eines Skills finden
neighbors = list(G.neighbors('skill:seo-audit'))
```

---

*Generiert am: 2026-07-03 13:03 UTC*