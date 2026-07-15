# Manus System Brain — Wissensgraph-Bericht

> **Für jeden KI-Agenten:** Lies zuerst `SYSTEM.md` um den Systemgedanken zu verstehen. Dieser Bericht ist der operative Überblick.

> Generiert: 2026-07-15 01:05 | Knoten: **156** | Kanten: **254** | Manus-Skills: **54** | Projekt-Skills: **11** | Projekte: **3** | Konnektoren: **12**

---

## Systemarchitektur

Vier-Ebenen-Architektur (siehe SYSTEM.md + docs/architecture/vier-ebenen-architektur.md); im Graphen verbunden:

| Ebene | Was | Anzahl |
|---|---|:---:|
| **Kern** | Manus System Brain (dieses Repo) | 1 |
| **Universelle Skills** | Plattformübergreifende Fähigkeiten | 54 |
| **Projekte** | Spezifische Anwendungen (z.B. Salon-Website) | 3 |
| **Projekt-Skills** | Projektspezifische Fähigkeiten | 11 |
| **Konnektoren** | Externe APIs und Integrationen | 12 (2 aktiv) |

---

## Fähigkeiten (Capability Registry v0.1)

32 registrierte Fähigkeiten — Quelle: `registry/capabilities.yaml` (validiert im Build).

| Fähigkeit | Art | Status | Techn. Rolle | Prüfstand |
|---|---|---|---|---|
| **Freigabe-Wächter** (`agent:approval-gatekeeper`) | agent | draft | intelligenz | — |
| **Klassifikations-Agent** (`agent:classification`) | agent | draft | intelligenz | — |
| **Extraktions-Agent** (`agent:extraction`) | agent | draft | intelligenz | — |
| **Graph-Gedächtnis-Agent** (`agent:graph-memory`) | agent | draft | intelligenz | — |
| **Eingangs-Agent** (`agent:intake`) | agent | draft | intelligenz | — |
| **API-Wächter (os-api-watch)** (`arbeitsablauf:os-api-watch`) | arbeitsablauf | active | adapter | — |
| **Golden Task 1: Vertrag klassifizieren** (`golden-task:1`) | golden-task | active | intelligenz | — |
| **Golden Task 10: Neues Modul nach Template planen** (`golden-task:10`) | golden-task | active | intelligenz | — |
| **Golden Task 2: Kündigungsfrist extrahieren** (`golden-task:2`) | golden-task | active | intelligenz | — |
| **Golden Task 3: Tool bewerten** (`golden-task:3`) | golden-task | active | intelligenz | — |
| **Golden Task 4: Notfallkarte erstellen** (`golden-task:4`) | golden-task | active | intelligenz | — |
| **Golden Task 5: Website-Verbesserung vorschlagen** (`golden-task:5`) | golden-task | active | intelligenz | — |
| **Golden Task 6: Marketingidee strukturieren** (`golden-task:6`) | golden-task | active | intelligenz | — |
| **Golden Task 7: MCP-Server bewerten** (`golden-task:7`) | golden-task | active | intelligenz | — |
| **Golden Task 8: Secret-Leak-Risiko erkennen** (`golden-task:8`) | golden-task | active | intelligenz | — |
| **Golden Task 9: Graph-Nodes aus Dokument erzeugen** (`golden-task:9`) | golden-task | active | intelligenz | — |
| **AI Is Replaceable** (`policy:ai-is-replaceable`) | policy | active | intelligenz | — |
| **Human Approval First** (`policy:human-approval-first`) | policy | active | intelligenz | — |
| **No Hidden Memory Dependency** (`policy:no-hidden-memory-dependency`) | policy | active | intelligenz | — |
| **No Secrets in Knowledge Systems** (`policy:no-secrets-in-knowledge-systems`) | policy | active | intelligenz | — |
| **Read-only First** (`policy:read-only-first`) | policy | active | intelligenz | — |
| **Reuse First / Open Source First** (`policy:reuse-first`) | policy | active | intelligenz | — |
| **Gehärteten Server aufsetzen** (`setup-blueprint:hetzner-server`) | setup-blueprint | active | infrastruktur | — |
| **Neuen API-Token anlegen** (`setup-blueprint:token-anlegen`) | setup-blueprint | active | secret-verwaltung | — |
| **contract-intake** (`skill:contract-intake`) | skill | draft | intelligenz | — |
| **deadline-extraction** (`skill:deadline-extraction`) | skill | draft | intelligenz | — |
| **emergency-card** (`skill:emergency-card`) | skill | draft | intelligenz | — |
| **graph-memory-entry** (`skill:graph-memory-entry`) | skill | draft | intelligenz | — |
| **tool-evaluation** (`skill:tool-evaluation`) | skill | draft | intelligenz | — |
| **Hetzner salon-core (CPX32, nbg1)** (`system:salon-core`) | system | active | infrastruktur | — |
| **uptime-kuma** (`system:uptime-kuma`) | system | active | monitoring | — |
| **vaultwarden** (`system:vaultwarden`) | system | active | secret-verwaltung | — |

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
| **brand** |  | ✓ | 343 |
| **brandkit** |  |  | 2,600 |
| **builtin-llm-models** |  | ✓ | 1,779 |
| **design** |  | ✓ | 1,546 |
| **design-system** |  | ✓ | 838 |
| **emil-design-eng** |  |  | 3,887 |
| **extract-design-system** |  |  | 292 |
| **game-dev** |  | ✓ | 803 |
| **image-to-code** |  |  | 5,820 |
| **internet-skill-finder** |  | ✓ | 212 |
| **manus-api** |  |  | 1,257 |
| **manus-config** |  |  | 1,411 |
| **manus-pptx** |  |  | 3,396 |
| **persistent-computing** |  |  | 1,262 |
| **read-special-images** |  | ✓ | 594 |
| **review-animations** |  |  | 1,118 |
| **skill-creator** |  | ✓ | 1,425 |
| **system-indexer** |  | ✓ | 278 |
| **typst-pdf-maker** |  | ✓ | 835 |
| **ui-styling** |  | ✓ | 1,149 |
| **ui-ux-pro-max** |  | ✓ | 6,898 |
| **web-design-guidelines** |  |  | 176 |
| **webdev-custom-dockerfile** |  |  | 1,768 |
| **webdev-data-api** |  |  | 64 |
| **webdev-file-storage** |  |  | 235 |
| **webdev-image-generation** |  |  | 227 |
| **webdev-llm-integration** |  |  | 697 |
| **webdev-manus-oauth** |  |  | 908 |
| **webdev-maps-integration** |  |  | 159 |
| **webdev-owner-notifications** |  |  | 129 |
| **webdev-periodic-updates** |  |  | 2,121 |
| **webdev-readme-fullstack** |  |  | 4,362 |
| **webdev-readme-mobile** |  |  | 3,419 |
| **webdev-readme-mobile-backend** |  |  | 4,951 |
| **webdev-readme-static** |  |  | 3,211 |
| **webdev-ssr-conversion** |  | ✓ | 3,786 |
| **webdev-voice-transcription** |  |  | 150 |

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

**Nutzt universelle Skills:** seo-audit, content-gap-analysis, keyword-research, website-traffic-checker, backlink-analysis, imagegen, automation-and-scheduling, emil-design-eng, ui-ux-pro-max, web-design-guidelines, extract-design-system, image-to-code, brandkit

### sprachlern-app

**Repo:** `` | **Beschreibung:** Birkenbihl-Sprachlern-App. Getrennte Infrastruktur/Repo.

### warenwirtschaft-webapp

**Repo:** `—` | **Beschreibung:** Cloudflare-Webapp als Prozesszentrale (Wareneingang, Bestände, Anbieter, Arbeitszeit, Freigabe).

---

## Zentrale Knoten (höchste Vernetzung)

| Rang | Knoten | Typ | Ebene | Verbindungen |
|:---:|---|---|---|:---:|
| 1 | **System & Infrastruktur** | category | manus | 44 |
| 2 | **Manus System Brain** | system | core | 40 |
| 3 | **Salon OS — Die Friseure Gumbert & Partner** | project | unternehmens-os | 26 |
| 4 | **Human Approval First** | policy | core | 12 |
| 5 | **No Secrets in Knowledge Systems** | policy | core | 12 |
| 6 | **Read-only First** | policy | core | 12 |
| 7 | **ui-ux-pro-max** | skill | manus | 11 |
| 8 | **website-traffic-checker** | skill | manus | 10 |
| 9 | **SEO & Marketing** | category | manus | 8 |
| 10 | **automation-and-scheduling** | skill | manus | 7 |

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
