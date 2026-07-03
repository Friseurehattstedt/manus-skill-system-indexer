#!/usr/bin/env python3
"""
Manus System Brain — Universeller Wissensgraph-Builder
=======================================================
Baut EINEN zentralen Wissensgraphen aus ALLEN Teilen des Systems:

  1. Universelle Manus-Skills (skills/)
  2. Projekt-Skills (projects/*/skills/)
  3. Projekt-Wissen (projects/*/knowledge/)
  4. Konnektoren (Manus config.json)
  5. Repositories (GitHub-Struktur)

SYSTEMGEDANKE: Alles ist ein Knoten. Nichts ist eine Insel.

Output: knowledge-graph/graph.json  (NetworkX node-link, offener Standard)
        knowledge-graph/GRAPH_REPORT.md (für Menschen + KI lesbar)

Kompatibel mit: Graphify, NetworkX, jedem JSON-Parser, allen KI-Modellen.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import networkx as nx
from networkx.readwrite import json_graph

# ── Pfade ──────────────────────────────────────────────────────────────────
REPO_ROOT    = Path(__file__).parent.parent
SKILLS_DIR   = REPO_ROOT / "skills"
PROJECTS_DIR = REPO_ROOT / "projects"
CONFIG_FILE  = Path.home() / ".manus" / "config" / "config.json"
OUTPUT_DIR   = REPO_ROOT / "knowledge-graph"
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Kategorien universeller Manus-Skills ──────────────────────────────────
MANUS_SKILL_CATEGORIES = {
    "seo":         ["backlink-analysis", "content-gap-analysis", "keyword-research",
                    "seo-audit", "seo-competitor-analysis", "similarweb-analytics",
                    "website-traffic-checker"],
    "system":      ["automation-and-scheduling", "builtin-llm-models", "internet-skill-finder",
                    "manus-api", "manus-config", "persistent-computing", "skill-creator",
                    "system-indexer"],
    "media":       ["imagegen", "music-prompter", "tts-prompter"],
    "integration": ["github-gem-seeker", "gws-best-practices"],
    "token-efficiency": ["caveman", "superpowers-core", "superpowers-debugging", "superpowers-verification"],
}

# Salon-Projekt-Skill-Kategorien
SALON_SKILL_CATEGORIES = {
    "salon-content": ["content-production", "social-content", "social-media-manager"],
    "salon-seo":     ["programmatic-seo", "schema-markup", "seo-audit"],
    "salon-dev":     ["pr-review-expert"],
    # Design-Skills (neu)
    "salon-design":  ["emil-design-eng", "review-animations", "ui-ux-pro-max",
                      "uiux-design", "uiux-design-system", "uiux-brand", "uiux-ui-styling",
                      "brandkit", "image-to-code", "extract-design-system", "web-design-guidelines"],
}

# Konnektor → Skill-Verbindungen
CONNECTOR_SKILL_MAP = {
    "Ahrefs":        ["backlink-analysis", "website-traffic-checker", "seo-audit"],
    "Ahrefs API":    ["backlink-analysis", "keyword-research"],
    "Semrush":       ["keyword-research", "seo-competitor-analysis", "content-gap-analysis"],
    "Similarweb":    ["similarweb-analytics", "website-traffic-checker"],
    "DataForSEO":    ["keyword-research", "website-traffic-checker"],
    "GitHub":        ["github-gem-seeker", "manus-api", "skill-creator"],
    "OpenAI":        ["builtin-llm-models", "manus-api"],
    "Google Drive":  ["gws-best-practices"],
    "Google Sheets": ["gws-best-practices", "keyword-research"],
    "Google Docs":   ["gws-best-practices"],
    "Google Slides": ["gws-best-practices"],
    "Slack":         ["automation-and-scheduling", "manus-api"],
    "Notion":        ["automation-and-scheduling"],
    "Cloudflare":    ["salon-website"],
    "Phorest":       ["salon-website"],
    "Wix":           ["salon-website"],
}

# Skill-zu-Skill-Synergien
SKILL_SYNERGIES = {
    "backlink-analysis":      ["website-traffic-checker", "seo-audit"],
    "content-gap-analysis":   ["keyword-research", "website-traffic-checker"],
    "seo-competitor-analysis":["website-traffic-checker", "seo-audit"],
    "seo-audit":              ["website-traffic-checker", "backlink-analysis"],
    "keyword-research":       ["website-traffic-checker"],
    "imagegen":               ["skill-creator"],
    "music-prompter":         ["skill-creator"],
    "tts-prompter":           ["skill-creator"],
    "internet-skill-finder":  ["skill-creator", "github-gem-seeker"],
    "manus-api":              ["automation-and-scheduling", "manus-config"],
    "persistent-computing":   ["manus-config", "automation-and-scheduling"],
    "builtin-llm-models":     ["manus-api"],
    "gws-best-practices":     ["automation-and-scheduling"],
    # Salon-Synergien
    "content-production":     ["seo-audit", "keyword-research", "social-content"],
    "programmatic-seo":       ["schema-markup", "keyword-research"],
    "social-content":         ["content-production", "social-media-manager"],
    "schema-markup":          ["seo-audit", "programmatic-seo"],
    # Design-Synergien (neu)
    "emil-design-eng":        ["review-animations", "ui-ux-pro-max", "image-to-code"],
    "review-animations":      ["emil-design-eng", "web-design-guidelines"],
    "ui-ux-pro-max":          ["uiux-design", "uiux-design-system", "uiux-brand", "uiux-ui-styling",
                               "extract-design-system", "brandkit"],
    "uiux-design":            ["ui-ux-pro-max", "uiux-design-system"],
    "uiux-design-system":     ["extract-design-system", "uiux-brand", "uiux-ui-styling"],
    "uiux-brand":             ["brandkit", "uiux-design-system"],
    "uiux-ui-styling":        ["ui-ux-pro-max", "web-design-guidelines"],
    "brandkit":               ["uiux-brand", "image-to-code"],
    "image-to-code":          ["emil-design-eng", "brandkit", "ui-ux-pro-max"],
    "extract-design-system":  ["uiux-design-system", "ui-ux-pro-max"],
    "web-design-guidelines":  ["ui-ux-pro-max", "review-animations"],
}

# Projekt-zu-Skill-Verbindungen — EBENE 1: Unternehmens-OS
PROJECT_USES_SKILLS = {
    "salon-os": ["seo-audit", "content-gap-analysis", "keyword-research",
                 "website-traffic-checker", "backlink-analysis", "imagegen",
                 "automation-and-scheduling", "social-content", "schema-markup",
                 # Design-Skills
                 "emil-design-eng", "ui-ux-pro-max", "web-design-guidelines",
                 "extract-design-system", "image-to-code", "brandkit"],
}


def parse_skill_frontmatter(skill_md_path: Path) -> dict:
    content = skill_md_path.read_text(encoding="utf-8", errors="ignore")
    fm_match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
    name = skill_md_path.parent.name
    description = ""
    if fm_match:
        fm = fm_match.group(1)
        name_m = re.search(r'^name:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
        desc_m = re.search(r"^description:\s*>?\s*\n?(.*?)(?=\n\w|\Z)", fm, re.DOTALL)
        if name_m:
            name = name_m.group(1).strip()
        if desc_m:
            description = desc_m.group(1).strip().replace("\n", " ").replace("  ", " ")
    files = list(skill_md_path.parent.rglob("*"))
    return {
        "name": name,
        "description": description[:300],
        "has_scripts": any("scripts" in str(f) for f in files),
        "has_references": any("references" in str(f) for f in files),
        "word_count": len(content.split()),
        "file_count": len([f for f in files if f.is_file()]),
    }


def build_graph() -> nx.Graph:
    G = nx.Graph()
    all_skill_nodes = {}  # skill_dir_name → node_id

    # ── EBENE 0: Intelligence Layer (System-Kern) ────────────────────────────
    G.add_node("system:brain", label="Manus System Brain",
               type="system", layer="core",
               description="EBENE 0: Intelligence Layer. Koordiniert alle Unternehmens-OS und Satelliten.",
               repo="Friseurehattstedt/manus-system-brain",
               community=0)

    # ── EBENE 0: Universelle Skills (Teil des Intelligence Layer) ──────────
    print("[build] Universelle Manus-Skills...")
    cat_community = {"seo": 1, "system": 2, "media": 3, "integration": 4, "token-efficiency": 5}

    for cat, skills in MANUS_SKILL_CATEGORIES.items():
        cat_node = f"category:manus-{cat}"
        cat_labels = {"seo": "SEO & Marketing", "system": "System & Infrastruktur",
                      "media": "Medien & Kreation", "integration": "Integrationen",
                      "token-efficiency": "Token-Effizienz & Qualität"}
        G.add_node(cat_node, label=cat_labels[cat], type="category",
                   layer="manus", community=cat_community[cat])
        G.add_edge("system:brain", cat_node, relation="CONTAINS", confidence="EXTRACTED")

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        meta = parse_skill_frontmatter(skill_md)
        node_id = f"skill:{skill_dir.name}"
        cat = next((c for c, s in MANUS_SKILL_CATEGORIES.items() if skill_dir.name in s), "system")
        G.add_node(node_id, label=meta["name"], type="skill", layer="manus",
                   category=cat, description=meta["description"],
                   has_scripts=meta["has_scripts"], has_references=meta["has_references"],
                   word_count=meta["word_count"], file_count=meta["file_count"],
                   source_file=f"skills/{skill_dir.name}/SKILL.md",
                   community=cat_community.get(cat, 2))
        all_skill_nodes[skill_dir.name] = node_id
        G.add_edge(f"category:manus-{cat}", node_id, relation="CONTAINS", confidence="EXTRACTED")
        print(f"  + Manus-Skill: {meta['name']} [{cat}]")

    # ── EBENE 1: Unternehmens-OS (z.B. salon-os) ────────────────────────────
    print("\n[build] Projekte...")
    if PROJECTS_DIR.exists():
        for project_dir in sorted(PROJECTS_DIR.iterdir()):
            if not project_dir.is_dir():
                continue
            proj_node = f"project:{project_dir.name}"
            proj_readme = project_dir / "README.md"
            proj_desc = ""
            proj_repo = ""
            if proj_readme.exists():
                content = proj_readme.read_text(encoding="utf-8", errors="ignore")
                repo_m = re.search(r"Repo.*?`([^`]+)`", content)
                if repo_m:
                    proj_repo = repo_m.group(1)
                proj_desc = content.split("\n")[2][:200] if len(content.split("\n")) > 2 else ""

            proj_label = "Salon OS — Die Friseure Gumbert & Partner" if project_dir.name == "salon-os" else project_dir.name.replace("-", " ").title()
            proj_layer = "unternehmens-os" if project_dir.name.endswith("-os") else "project"
            G.add_node(proj_node, label=proj_label,
                       type="project", layer=proj_layer,
                       description=proj_desc, repo=proj_repo, community=5)
            G.add_edge("system:brain", proj_node, relation="COORDINATES", confidence="EXTRACTED")
            print(f"  + Projekt: {project_dir.name}")

            # Projekt-Skills
            proj_skills_dir = project_dir / "skills"
            if proj_skills_dir.exists():
                for skill_dir in sorted(proj_skills_dir.iterdir()):
                    if not skill_dir.is_dir():
                        continue
                    skill_md = skill_dir / "SKILL.md"
                    if not skill_md.exists():
                        continue
                    meta = parse_skill_frontmatter(skill_md)
                    node_id = f"skill:{project_dir.name}:{skill_dir.name}"
                    cat = next((c for c, s in SALON_SKILL_CATEGORIES.items()
                                if skill_dir.name in s), "salon-general")
                    G.add_node(node_id, label=meta["name"], type="skill", layer="project",
                               category=cat, description=meta["description"],
                               project=project_dir.name,
                               source_file=f"projects/{project_dir.name}/skills/{skill_dir.name}/SKILL.md",
                               community=5)
                    all_skill_nodes[f"{project_dir.name}:{skill_dir.name}"] = node_id
                    G.add_edge(proj_node, node_id, relation="USES", confidence="EXTRACTED")
                    print(f"    + Projekt-Skill: {meta['name']}")

            # Projekt-Knowledge-Knoten
            proj_knowledge_dir = project_dir / "knowledge"
            if proj_knowledge_dir.exists():
                knowledge_files = list(proj_knowledge_dir.glob("*.md"))
                if knowledge_files:
                    know_node = f"knowledge:{project_dir.name}"
                    G.add_node(know_node, label=f"Wissen: {project_dir.name}",
                               type="knowledge", layer="project",
                               file_count=len(knowledge_files), community=5)
                    G.add_edge(proj_node, know_node, relation="DOCUMENTED_BY", confidence="EXTRACTED")
                    print(f"    + Knowledge: {len(knowledge_files)} Dateien")

            # Projekt nutzt universelle Skills
            for skill_name in PROJECT_USES_SKILLS.get(project_dir.name, []):
                if skill_name in all_skill_nodes:
                    G.add_edge(proj_node, all_skill_nodes[skill_name],
                               relation="USES", confidence="INFERRED")

    # ── EBENE 4: Skill-Synergien ───────────────────────────────────────────
    print("\n[build] Skill-Synergien...")
    for skill_name, deps in SKILL_SYNERGIES.items():
        src_key = skill_name
        src_node = all_skill_nodes.get(src_key) or all_skill_nodes.get(f"salon-website:{src_key}")
        if not src_node:
            continue
        for dep in deps:
            dep_node = all_skill_nodes.get(dep) or all_skill_nodes.get(f"salon-website:{dep}")
            if dep_node and src_node != dep_node:
                G.add_edge(src_node, dep_node, relation="COMPLEMENTS", confidence="INFERRED")

    # ── EBENE 5: Konnektoren ───────────────────────────────────────────────
    print("\n[build] Konnektoren...")
    connectors_loaded = 0
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            config = json.load(f)
        important = set(CONNECTOR_SKILL_MAP.keys())
        for c in config.get("connectors", []):
            name = c.get("name", "")
            if not c.get("enabled") and name not in important:
                continue
            node_id = f"connector:{name.lower().replace(' ', '-')}"
            G.add_node(node_id, label=name, type="connector", layer="connector",
                       enabled=c.get("enabled", False),
                       description=c.get("brief", "")[:200], community=6)
            connectors_loaded += 1
            for conn_name, skill_list in CONNECTOR_SKILL_MAP.items():
                if conn_name.lower() == name.lower():
                    for s in skill_list:
                        target = all_skill_nodes.get(s) or f"project:{s}"
                        if G.has_node(target):
                            G.add_edge(node_id, target, relation="USED_BY", confidence="EXTRACTED")
    print(f"  + {connectors_loaded} Konnektoren")

    print(f"\n[build] Fertig: {G.number_of_nodes()} Knoten, {G.number_of_edges()} Kanten")
    return G


def write_graph_json(G: nx.Graph, path: Path):
    data = json_graph.node_link_data(G, edges="links")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[output] graph.json → {path}")


def write_graph_report(G: nx.Graph, path: Path):
    manus_skills  = [(n,d) for n,d in G.nodes(data=True) if d.get("type")=="skill" and d.get("layer")=="manus"]
    proj_skills   = [(n,d) for n,d in G.nodes(data=True) if d.get("type")=="skill" and d.get("layer")=="project"]
    projects      = [(n,d) for n,d in G.nodes(data=True) if d.get("type")=="project"]
    connectors    = [(n,d) for n,d in G.nodes(data=True) if d.get("type")=="connector"]
    enabled_conn  = [(n,d) for n,d in connectors if d.get("enabled")]
    top_nodes     = sorted([(n,d,G.degree(n)) for n,d in G.nodes(data=True)], key=lambda x:-x[2])[:10]

    lines = [
        "# Manus System Brain — Wissensgraph-Bericht",
        "",
        "> **Für jeden KI-Agenten:** Lies zuerst `SYSTEM.md` um den Systemgedanken zu verstehen. Dieser Bericht ist der operative Überblick.",
        "",
        f"> Generiert: {datetime.now().strftime('%Y-%m-%d %H:%M')} | "
        f"Knoten: **{G.number_of_nodes()}** | Kanten: **{G.number_of_edges()}** | "
        f"Manus-Skills: **{len(manus_skills)}** | Projekt-Skills: **{len(proj_skills)}** | "
        f"Projekte: **{len(projects)}** | Konnektoren: **{len(connectors)}**",
        "",
        "---",
        "",
        "## Systemarchitektur",
        "",
        "Das System besteht aus drei Ebenen, die alle im Graphen verbunden sind:",
        "",
        "| Ebene | Was | Anzahl |",
        "|---|---|:---:|",
        f"| **Kern** | Manus System Brain (dieses Repo) | 1 |",
        f"| **Universelle Skills** | Plattformübergreifende Fähigkeiten | {len(manus_skills)} |",
        f"| **Projekte** | Spezifische Anwendungen (z.B. Salon-Website) | {len(projects)} |",
        f"| **Projekt-Skills** | Projektspezifische Fähigkeiten | {len(proj_skills)} |",
        f"| **Konnektoren** | Externe APIs und Integrationen | {len(connectors)} ({len(enabled_conn)} aktiv) |",
        "",
        "---",
        "",
        "## Universelle Manus-Skills",
        "",
    ]

    cat_labels = {"seo": "SEO & Marketing", "system": "System & Infrastruktur",
                  "media": "Medien & Kreation", "integration": "Integrationen"}
    for cat, label in cat_labels.items():
        cat_skills = [(n,d) for n,d in manus_skills if d.get("category")==cat]
        if not cat_skills:
            continue
        lines += [f"### {label}", "", "| Skill | Beschreibung | Scripts | Wörter |",
                  "|---|---|:---:|---:|"]
        for n, d in sorted(cat_skills, key=lambda x: x[1].get("label","")):
            desc = d.get("description","")[:80].replace("|","/")
            s = "✓" if d.get("has_scripts") else ""
            lines.append(f"| **{d.get('label',n)}** | {desc} | {s} | {d.get('word_count',0):,} |")
        lines.append("")

    lines += ["---", "", "## Projekte", ""]
    for n, d in projects:
        lines += [f"### {d.get('label', n)}", "",
                  f"**Repo:** `{d.get('repo','—')}` | **Beschreibung:** {d.get('description','')[:120]}",
                  ""]
        proj_name = n.replace("project:", "")
        p_skills = [(sn,sd) for sn,sd in proj_skills if sd.get("project")==proj_name]
        if p_skills:
            lines += ["**Projekt-spezifische Skills:**", ""]
            for sn, sd in p_skills:
                lines.append(f"- **{sd.get('label',sn)}** — {sd.get('description','')[:80]}")
            lines.append("")
        univ_skills = [sn for sn in G.neighbors(n) if G.nodes[sn].get("type")=="skill" and G.nodes[sn].get("layer")=="manus"]
        if univ_skills:
            labels = [G.nodes[s].get("label",s) for s in univ_skills]
            lines.append(f"**Nutzt universelle Skills:** {', '.join(labels)}")
            lines.append("")

    lines += ["---", "", "## Zentrale Knoten (höchste Vernetzung)", "",
              "| Rang | Knoten | Typ | Ebene | Verbindungen |",
              "|:---:|---|---|---|:---:|"]
    for i, (n, d, deg) in enumerate(top_nodes, 1):
        lines.append(f"| {i} | **{d.get('label',n)}** | {d.get('type','')} | {d.get('layer','')} | {deg} |")

    lines += ["", "---", "", "## Aktive Konnektoren", ""]
    if enabled_conn:
        lines += ["| Konnektor | Beschreibung |", "|---|---|"]
        for n, d in enabled_conn:
            lines.append(f"| **{d.get('label',n)}** | {d.get('description','')[:80].replace('|','/')} |")
    else:
        lines.append("_Keine Konnektoren aktiv._")

    lines += ["", "---", "", "## Für KI-Agenten: Graph abfragen", "",
              "```python", "import json, networkx as nx",
              "from networkx.readwrite import json_graph", "",
              "with open('knowledge-graph/graph.json') as f:",
              "    G = json_graph.node_link_graph(json.load(f), edges='links')", "",
              "# Alle Projekte", "projects = [d['label'] for _,d in G.nodes(data=True) if d.get('type')=='project']",
              "# Skills eines Projekts", "skills = list(G.neighbors('project:salon-website'))",
              "# Kürzester Pfad", "path = nx.shortest_path(G, 'project:salon-website', 'connector:ahrefs')",
              "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[output] GRAPH_REPORT.md → {path}")


if __name__ == "__main__":
    print("=" * 60)
    print("Manus System Brain — Universeller Wissensgraph-Builder")
    print("=" * 60)
    G = build_graph()
    write_graph_json(G, OUTPUT_DIR / "graph.json")
    write_graph_report(G, OUTPUT_DIR / "GRAPH_REPORT.md")
    print("\nFertig!")
