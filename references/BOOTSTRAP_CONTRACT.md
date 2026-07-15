# Bootstrap Contract

## Zweck

Der öffentliche System-Indexer ermöglicht Claude, Codex, Manus und anderen
Agenten denselben Einstieg. Kanonischer Zustand bleibt ausschließlich in den
privaten Eigentümer-Repositories.

## Handshake

Ein Agent bestätigt vor der Arbeit:

```yaml
context_status: verified | context_not_verified
canonical_sources_read: []
conflicts: []
authorized_repositories: []
authorized_effects: read_only | branch_changes | merge | deployment | live_write
```

## Quellenrangfolge

1. strukturierte State-/Registry-Dateien im privaten Eigentümer-Repository
2. aktive fachliche Artefakte im zuständigen Repository
3. daraus generierte Berichte
4. Chat-Übergaben und Erinnerungen

## Öffentliche Grenze

Unzulässig in diesem Repository sind:

- private Wissensgraphen und daraus erzeugte Berichte,
- interne System-, Connector-, Secret- oder Venture-Inventare,
- personenbezogene oder geschäftsvertrauliche Daten,
- lokale Credential-Pfade, Tokens oder Zugangsanweisungen.

Der Bootstrap vermittelt keine Schreib-, Merge-, Deployment- oder Live-Rechte.

