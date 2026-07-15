---
name: system-indexer
description: Öffentlicher, modellneutraler Bootstrap zum Auffinden und Prüfen der privaten kanonischen Systemwahrheit. Nutze ihn beim Sessionstart; er enthält selbst weder internen Graphen noch Systeminventar.
---

# System Indexer

Dieser Skill ist ein Wegweiser, keine Wissensdatenbank.

## Verbindlicher Ablauf

1. Nutze ausschließlich einen vom Menschen freigegebenen Zugriff auf das private
   Brain-Repository.
2. Lies dort in dieser Reihenfolge:
   - `SYSTEM.md`
   - `registry/system-state.yaml`
   - `docs/runbooks/session-start.md`
3. Bei Arbeit für eine Unternehmung lies außerdem im zuständigen privaten Repo
   `AGENTS.md` und `registry/venture-state.yaml`.
4. Ordne jede Aussage einem Scope zu: Branch, Main, Deployment oder Produktion.
5. Kann eine Pflichtquelle nicht geprüft werden, melde
   `context_not_verified`. Erfinde keine Ersatzwahrheit aus Chat-Verlauf,
   Erinnerungen oder diesem öffentlichen Skill.

## Grenzen

- Keine Zugangsdaten anfordern oder lokale Secret-Pfade voraussetzen.
- Keine internen Graphen, Reports, Systemlisten oder Venture-Daten hier ablegen.
- Keine Merge-, Deployment- oder Live-Rechte aus dem Bootstrap ableiten.
- Modellspezifische Adapter dürfen den privaten Systemvertrag nicht ersetzen.

Details und Prüfkriterien: `references/BOOTSTRAP_CONTRACT.md`.
