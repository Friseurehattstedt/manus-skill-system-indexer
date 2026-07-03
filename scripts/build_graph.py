#!/usr/bin/env python3
"""
Manus System Brain — Knowledge Graph Builder
=============================================
Baut einen vollständigen Wissensgraphen aus:
- Manus Skills (SKILL.md-Dateien)
- Konnektoren (config.json)
- Abhängigkeiten und semantische Beziehungen

Output: knowledge-graph/graph.json (NetworkX node-link Format)
        knowledge-graph/GRAPH_REPORT.md (menschenlesbar)

Kompatibel mit: Graphify, NetworkX, jeder JSON-Parser
"""

import json
import os
import re
import sys
from pathlib import Path

import networkx as nx
from networkx.readwrite import json_graph

# ── Pfade ──────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
CONFIG_FILE = Path.home() / ".manus" / "config" / "config.json"
OUTPUT_DIR = REPO_ROOT / "knowledge-graph"
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Skill-Kategorien (semantisch) ──────────────────────────────────────────
SKILL_CATEGORIES = {
    "seo": ["seo-audit", "seo-competitor-analysis", "backlink-analysis",
            "content-gap-analysis", "keyword-research", "website-traffic-checker",
            "similarweb-analytics"],
    "system": ["skill-creator", "manus-config", "manus-api", "persistent-computing",
               "automation-and-scheduling", "builtin-llm-models", "internet-skill-finder"],
    "media": ["imagegen", "music-prompter", "tts-prompter"],
    "integration": ["gws-best-practices", "github-gem-seeker"],
}

# Connector-Keywords → Skill-Verbindungen
CONNECTOR_SKILL_MAP = {
    "Ahrefs": ["backlink-analysis", "website-traffic-checker", "seo-audit"],
    "Ahrefs API": ["backlink-analysis", "website-traffic-checker", "keyword-research"],
    "Semrush": ["keyword-research", "seo-competitor-analysis", "content-gap-analysis"],
    "Similarweb": ["similarweb-analytics", "website-traffic-checker"],
    "DataForSEO": ["keyword-research", "website-traffic-checker"],
    "GitHub": ["github-gem-seeker", "manus-api", "skill-creator"],
    "OpenAI": ["builtin-llm-models", "manus-api"],
    "Google Drive": ["gws-best-practices"],
    "Google Sheets": ["gws-best-practices", "keyword-research"],
    "Google Docs": ["gws-best-practices"],
    "Google Slides": ["gws-best-practices"],
    "Slack": ["automation-and-scheduling", "manus-api"],
    "Notion": ["automation-and-scheduling"],
    "Airtable": ["automation-and-scheduling"],
}

# Skill-zu-Skill-Abhängigkeiten (aus SKILL.md-Inhalten abgeleitet)
SKILL_DEPENDENCIES = {
    "backlink-analysis": ["website-traffic-checker", "seo-audit"],
    "content-gap-analysis": ["keyword-research", "website-traffic-checker"],
    "seo-competitor-analysis": ["website-traffic-checker", "seo-audit"],
    "seo-audit": ["website-traffic-checker", "backlink-analysis"],
    "keyword-research": ["website-traffic-checker"],
    "imagegen": ["skill-creator"],
    "music-prompter": ["skill-creator"],
    "tts-prompter": ["skill-creator"],
    "internet-skill-finder": ["skill-creator", "github-gem-seeker"],
    "manus-api": ["automation-and-scheduling", "manus-config"],
    "persistent-computing": ["manus-config", "automation-and-scheduling"],
    "builtin-llm-models": ["manus-api"],
    "gws-best-practices": ["automation-and-scheduling"],
}


def parse_skill_frontmatter(skill_md_path: Path) -> dict:
    """Liest Name und Beschreibung aus SKILL.md-Frontmatter."""
    content = skill_md_path.read_text(encoding="utf-8", errors="ignore")
    fm_match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
    name = skill_md_path.parent.name
    description = ""
    if fm_match:
        fm = fm_match.group(1)
        name_m = re.search(r"^name:\s*(.+)", fm, re.MULTILINE)
        desc_m = re.search(r"^description:\s*>?\s*\n?(.*?)(?=\n\w|\Z)", fm, re.DOTALL)
        if name_m:
            name = name_m.group(1).strip()
        if desc_m:
            description = desc_m.group(1).strip().replace("\n", " ").replace("  ", " ")
    # Zähle Dateien im Skill
    files = list(skill_md_path.parent.rglob("*"))
    has_scripts = any("scripts" in str(f) for f in files)
    has_references = any("references" in str(f) for f in files)
    word_count = len(content.split())
    return {
        "name": name,
        "description": description[:300],
        "has_scripts": has_scripts,
        "has_references": has_references,
        "word_count": word_count,
        "file_count": len([f for f in files if f.is_file()]),
    }


def get_skill_category(skill_dir: str) -> str:
    for cat, skills in SKILL_CATEGORIES.items():
        if skill_dir in skills:
            return cat
    return "general"


def build_graph() -> nx.Graph:
    G = nx.Graph()

    # ── 1. Skill-Knoten ────────────────────────────────────────────────────
    print("[build] Lese Skills...")
    skill_nodes = {}
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        meta = parse_skill_frontmatter(skill_md)
        node_id = f"skill:{skill_dir.name}"
        category = get_skill_category(skill_dir.name)
        G.add_node(
            node_id,
            label=meta["name"],
            type="skill",
            category=category,
            description=meta["description"],
            has_scripts=meta["has_scripts"],
            has_references=meta["has_references"],
            word_count=meta["word_count"],
            file_count=meta["file_count"],
            source_file=f"skills/{skill_dir.name}/SKILL.md",
            community=list(SKILL_CATEGORIES.keys()).index(category) if category in SKILL_CATEGORIES else 4,
        )
        skill_nodes[skill_dir.name] = node_id
        print(f"  + Skill: {meta['name']} [{category}]")

    # ── 2. Kategorie-Knoten ────────────────────────────────────────────────
    print("[build] Erstelle Kategorie-Knoten...")
    cat_labels = {
        "seo": "SEO & Marketing",
        "system": "System & Infrastruktur",
        "media": "Medien & Kreation",
        "integration": "Integrationen & Tools",
    }
    for cat, label in cat_labels.items():
        G.add_node(
            f"category:{cat}",
            label=label,
            type="category",
            community=list(SKILL_CATEGORIES.keys()).index(cat),
        )
        # Verbinde Skills mit ihrer Kategorie
        for skill_dir in SKILL_CATEGORIES.get(cat, []):
            if skill_dir in skill_nodes:
                G.add_edge(
                    skill_nodes[skill_dir],
                    f"category:{cat}",
                    relation="BELONGS_TO",
                    confidence="EXTRACTED",
                )

    # ── 3. Skill-zu-Skill-Kanten ───────────────────────────────────────────
    print("[build] Verbinde Skills untereinander...")
    for skill_dir, deps in SKILL_DEPENDENCIES.items():
        if skill_dir not in skill_nodes:
            continue
        for dep in deps:
            if dep not in skill_nodes:
                continue
            G.add_edge(
                skill_nodes[skill_dir],
                skill_nodes[dep],
                relation="COMPLEMENTS",
                confidence="INFERRED",
            )

    # ── 4. Konnektoren laden ───────────────────────────────────────────────
    print("[build] Lese Konnektoren...")
    connectors_loaded = 0
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            config = json.load(f)
        connectors = config.get("connectors", [])
        enabled_connectors = [c for c in connectors if c.get("enabled")]
        # Alle Konnektoren als Knoten (enabled + wichtige disabled)
        important_names = set(CONNECTOR_SKILL_MAP.keys())
        for c in connectors:
            name = c.get("name", "")
            if not c.get("enabled") and name not in important_names:
                continue
            node_id = f"connector:{name.lower().replace(' ', '-')}"
            G.add_node(
                node_id,
                label=name,
                type="connector",
                enabled=c.get("enabled", False),
                description=c.get("brief", "")[:200],
                community=5,
            )
            connectors_loaded += 1
            # Verbinde mit Skills
            for conn_name, skill_list in CONNECTOR_SKILL_MAP.items():
                if conn_name.lower() == name.lower():
                    for skill_dir in skill_list:
                        if skill_dir in skill_nodes:
                            G.add_edge(
                                node_id,
                                skill_nodes[skill_dir],
                                relation="USED_BY",
                                confidence="EXTRACTED",
                            )
    print(f"  + {connectors_loaded} Konnektoren geladen")

    # ── 5. Zentral-Knoten: Manus OS ────────────────────────────────────────
    G.add_node(
        "system:manus-os",
        label="Manus OS",
        type="system",
        description="Zentrales KI-Agenten-Betriebssystem mit Skills, Konnektoren und Wissensbasis",
        community=6,
    )
    # Verbinde alle Kategorien mit dem Zentrum
    for cat in cat_labels:
        G.add_edge("system:manus-os", f"category:{cat}", relation="CONTAINS", confidence="EXTRACTED")

    print(f"\n[build] Graph fertig: {G.number_of_nodes()} Knoten, {G.number_of_edges()} Kanten")
    return G


def write_graph_json(G: nx.Graph, output_path: Path):
    data = json_graph.node_link_data(G, edges="links")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[output] graph.json → {output_path}")


def write_graph_report(G: nx.Graph, output_path: Path):
    """Erstellt einen menschenlesbaren Bericht im Markdown-Format."""
    skills = [(n, d) for n, d in G.nodes(data=True) if d.get("type") == "skill"]
    connectors = [(n, d) for n, d in G.nodes(data=True) if d.get("type") == "connector"]
    enabled_conn = [(n, d) for n, d in connectors if d.get("enabled")]

    # Top-Knoten nach Grad (Zentralität)
    degree_dict = dict(G.degree())
    top_nodes = sorted(
        [(n, d, degree_dict[n]) for n, d in G.nodes(data=True)],
        key=lambda x: -x[2]
    )[:10]

    lines = [
        "# Manus System Brain — Knowledge Graph Report",
        "",
        "> Automatisch generiert von `knowledge-graph/build_graph.py`  ",
        f"> Knoten: **{G.number_of_nodes()}** | Kanten: **{G.number_of_edges()}** | Skills: **{len(skills)}** | Konnektoren: **{len(connectors)}**",
        "",
        "---",
        "",
        "## Überblick",
        "",
        f"Dieses System besteht aus **{len(skills)} Skills** und **{len(connectors)} Konnektoren** "
        f"({len(enabled_conn)} aktiv). Der Wissensgraph enthält {G.number_of_nodes()} Knoten und "
        f"{G.number_of_edges()} semantische Verbindungen.",
        "",
        "---",
        "",
        "## Skills nach Kategorie",
        "",
    ]

    cat_labels = {
        "seo": "SEO & Marketing",
        "system": "System & Infrastruktur",
        "media": "Medien & Kreation",
        "integration": "Integrationen & Tools",
        "general": "Allgemein",
    }
    for cat, label in cat_labels.items():
        cat_skills = [(n, d) for n, d in skills if d.get("category") == cat]
        if not cat_skills:
            continue
        lines.append(f"### {label}")
        lines.append("")
        lines.append("| Skill | Beschreibung | Scripts | Refs | Wörter |")
        lines.append("|---|---|:---:|:---:|---:|")
        for n, d in sorted(cat_skills, key=lambda x: x[1].get("label", "")):
            desc = d.get("description", "")[:80].replace("|", "/")
            has_s = "✓" if d.get("has_scripts") else ""
            has_r = "✓" if d.get("has_references") else ""
            wc = d.get("word_count", 0)
            lines.append(f"| **{d.get('label', n)}** | {desc} | {has_s} | {has_r} | {wc:,} |")
        lines.append("")

    lines += [
        "---",
        "",
        "## Zentrale Knoten (höchste Vernetzung)",
        "",
        "Die folgenden Knoten haben die meisten Verbindungen im Graphen — sie sind die "
        "kritischsten Teile des Systems:",
        "",
        "| Rang | Knoten | Typ | Verbindungen |",
        "|:---:|---|---|:---:|",
    ]
    for i, (n, d, deg) in enumerate(top_nodes, 1):
        label = d.get("label", n)
        ntype = d.get("type", "")
        lines.append(f"| {i} | **{label}** | {ntype} | {deg} |")

    lines += [
        "",
        "---",
        "",
        "## Aktive Konnektoren",
        "",
    ]
    if enabled_conn:
        lines.append("| Konnektor | Beschreibung |")
        lines.append("|---|---|")
        for n, d in enabled_conn:
            desc = d.get("description", "")[:80].replace("|", "/")
            lines.append(f"| **{d.get('label', n)}** | {desc} |")
    else:
        lines.append("_Keine Konnektoren aktiv._")

    lines += [
        "",
        "---",
        "",
        "## Skill-Verbindungen (Synergien)",
        "",
        "Diese Skills ergänzen sich gegenseitig und sollten kombiniert eingesetzt werden:",
        "",
    ]
    for skill_dir, deps in {
        "seo-audit": ["backlink-analysis", "website-traffic-checker"],
        "content-gap-analysis": ["keyword-research", "seo-competitor-analysis"],
        "manus-api": ["automation-and-scheduling", "manus-config"],
        "imagegen": ["tts-prompter", "music-prompter"],
    }.items():
        if skill_dir in [d.get("source_file", "").split("/")[1] for _, d in skills]:
            deps_str = " + ".join(f"`{d}`" for d in deps)
            lines.append(f"- **`{skill_dir}`** → {deps_str}")

    lines += [
        "",
        "---",
        "",
        "## Für KI-Modelle: Wie dieser Graph genutzt wird",
        "",
        "```",
        "# Graphen laden und abfragen (Python/NetworkX)",
        "import json",
        "import networkx as nx",
        "from networkx.readwrite import json_graph",
        "",
        "with open('knowledge-graph/graph.json') as f:",
        "    G = json_graph.node_link_graph(json.load(f), edges='links')",
        "",
        "# Alle Skills finden",
        "skills = [d['label'] for _, d in G.nodes(data=True) if d.get('type') == 'skill']",
        "",
        "# Nachbarn eines Skills finden",
        "neighbors = list(G.neighbors('skill:seo-audit'))",
        "```",
        "",
        "---",
        "",
        "*Generiert am: " + __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M") + " UTC*",
    ]

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[output] GRAPH_REPORT.md → {output_path}")


if __name__ == "__main__":
    print("=" * 60)
    print("Manus System Brain — Knowledge Graph Builder")
    print("=" * 60)
    G = build_graph()
    write_graph_json(G, OUTPUT_DIR / "graph.json")
    write_graph_report(G, OUTPUT_DIR / "GRAPH_REPORT.md")
    print("\nFertig!")
