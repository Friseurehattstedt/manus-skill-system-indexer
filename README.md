# System Indexer — öffentlicher Bootstrap

Dieser öffentliche Skill erklärt Agenten, wie sie die private, kanonische
Systemwahrheit finden und verifizieren. Er ist **nicht** selbst die
Systemwahrheit.

## Sicherheitsgrenze

Dieses Repository enthält absichtlich keinen internen Wissensgraphen, keinen
Graph-Bericht, kein Systeminventar, keine Secrets und keine Venture-Daten. Der
private Brain-Graph wird niemals hierher gespiegelt.

## Start

1. Öffne das private Repository `Friseurehattstedt/manus-system-brain` nur mit
   vom Menschen bereitgestelltem Zugriff.
2. Lies dort `SYSTEM.md`, `registry/system-state.yaml` und
   `docs/runbooks/session-start.md`.
3. Bei Venture-Arbeit lies zusätzlich dessen `registry/venture-state.yaml`.
4. Wenn eine Pflichtquelle fehlt, melde `context_not_verified` statt zu raten.

Der vollständige Vertrag steht in `references/BOOTSTRAP_CONTRACT.md`.

## Repository prüfen

```bash
python3 scripts/verify_bootstrap.py
```
