# Multi-Language Bachelor Thesis Documentation Generator

Automatische Generierung von **wissenschaftlicher technischer Dokumentation** für Bachelorarbeiten aus Code-Repositories.

## Überblick

Dieses Tool scannt automatisch Ihr Code-Repository, analysiert die Struktur, Git-History und technische Entscheidungen und generiert eine vollständige wissenschaftliche Dokumentation auf Bachelor-Niveau.

### Was macht das Tool?

- **Multi-Language Support**: Python, JavaScript/TypeScript, Java, SQL
- **Intelligente Code-Analyse**: Erkennt Architektur, Design-Patterns, Abhängigkeiten
- **Git-History-Interpretation**: Versteht WARUM Entwicklung in bestimmter Reihenfolge erfolgte
- **Wissenschaftliche Formulierung**: Bachelor-Niveau mit korrekten Fachbegriffen
- **Automatische Diagramme**: Klassendiagramme, Architektur, Sequenzen (Mermaid)
- **7 Dokumentationskapitel**: Von Systemarchitektur bis Mehrwert-Analyse

### Warum wird das gebraucht?

Bachelorarbeiten erfordern oft 10+ Seiten technische Dokumentation mit:
- Architektur-Erklärungen
- Begründungen für technische Entscheidungen
- Entwicklungs-Chronologie
- Wissenschaftliche Formulierung

Manuell ist dies sehr zeitaufwändig. Dieses Tool automatisiert den Prozess komplett.

## Features

### 🎯 Kernfunktionen

- ✅ **Multi-Language Code-Analyse** (Python, JavaScript/TypeScript, Java, SQL)
- ✅ **Git-History-Analyse** (Commits, Entwicklungsphasen, Chronologie)
- ✅ **7 Dokumentationskapitel** (siehe unten)
- ✅ **5 Arten von Diagrammen** (Mermaid-Syntax)
- ✅ **Code-Statistiken** (LOC, Komplexität, Sprach-Verteilung)
- ✅ **Wissenschaftliche Formulierung** (Claude AI)
- ✅ **Flexible Konfiguration** (YAML)
- ✅ **CLI Interface** (einfache Nutzung)

### 📚 Generierte Dokumentationskapitel

1. **Executive Summary** - Projektüberblick
2. **Systemarchitektur** - Komponenten, Tech-Stack, Architektur-Pattern
3. **Code-Struktur & Design** - Module, Klassen, Design-Patterns
4. **Implementierungs-Chronologie** - Entwicklungsreihenfolge mit Begründung
5. **Technische Entscheidungen** - Alternativen, Vor-/Nachteile, Begründungen
6. **Feature-Backlog & Priorisierung** - Features, Scope-Management
7. **Mehrwert-Analyse** - Problem, Lösung, quantifizierbarer Nutzen
8. **Methodisches Vorgehen** - Entwicklungsmethodik, Testing, Tools

### 📊 Generierte Diagramme (Mermaid)

- **Klassendiagramm** - Klassen und Beziehungen
- **Architektur-Diagramm** - High-Level Komponenten
- **Sequenzdiagramm** - Haupt-Use-Case
- **ER-Diagramm** - Datenbank-Schema (falls SQL vorhanden)
- **Dependency-Graph** - Externe Abhängigkeiten

## Installation

### Voraussetzungen

- Python 3.8+
- Git (falls Git-History-Analyse gewünscht)
- Anthropic API Key (für Claude API)

### Setup

1. **Repository klonen oder herunterladen**

```bash
git clone <repository-url>
cd Multi-Language-Bachelor-Thesis-Documentation-Generator
```

2. **Dependencies installieren**

```bash
pip install -r requirements.txt
```

3. **API Key konfigurieren**

```bash
export ANTHROPIC_API_KEY="sk-ant-your-api-key-here"
```

Alternativ in `.bashrc` oder `.zshrc` eintragen:

```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-your-key"' >> ~/.bashrc
source ~/.bashrc
```

4. **Konfiguration anpassen**

```bash
cp config.yaml.example config.yaml
# Editiere config.yaml mit deinen Projekt-Details
```

## Verwendung

### Basis-Nutzung

```bash
python thesis_doc_gen.py \
  --repo-path ./my-project \
  --output ./docs
```

### Mit Konfigurationsdatei

```bash
python thesis_doc_gen.py \
  --repo-path ~/projects/my-app \
  --output ~/thesis/documentation \
  --config config.yaml \
  --verbose
```

### Dry-Run (testen ohne zu generieren)

```bash
python thesis_doc_gen.py \
  --repo-path ./my-project \
  --output ./docs \
  --dry-run
```

### Spezifische Sprachen analysieren

```bash
python thesis_doc_gen.py \
  --repo-path ./my-project \
  --output ./docs \
  --languages python,javascript,sql
```

### CLI Optionen

```
--repo-path PATH       Pfad zum Code-Repository (erforderlich)
--output PATH          Output-Verzeichnis (default: ./docs)
--config PATH          Pfad zur Konfigurationsdatei (default: config.yaml)
--languages LANGS      Komma-separierte Liste von Sprachen (default: auto)
--verbose, -v          Ausführliche Logs
--dry-run             Zeige was gemacht würde ohne zu generieren
--version             Zeige Version
```

## Konfiguration

Die Datei `config.yaml` enthält alle Einstellungen:

```yaml
project:
  name: "Mein Projekt"
  author: "Max Mustermann"
  supervisor: "Prof. Dr. Schmidt"
  university: "TH Köln"
  year: 2025

analysis:
  languages: auto  # oder: [python, javascript, sql]
  exclude_paths:
    - node_modules/
    - venv/
    - __pycache__/
  max_file_size_kb: 500

output:
  format: [markdown]
  language: de  # oder: en
  chapter_length: 600  # Ziel-Wörter pro Kapitel

documentation:
  style: academic
  include_code_examples: true
  max_code_lines_per_example: 30
```

## Output-Struktur

Nach der Generierung enthält das Output-Verzeichnis:

```
docs/
├── 00_executive_summary.md
├── 01_systemarchitektur.md
├── 02_code_struktur.md
├── 03_implementierung_chronologie.md
├── 04_technische_entscheidungen.md
├── 05_feature_backlog.md
├── 06_mehrwert_analyse.md
├── 07_methodik.md
├── diagrams/
│   ├── architecture.mmd
│   ├── class_diagram.mmd
│   ├── sequence_main_flow.mmd
│   ├── er_diagram.mmd
│   └── dependency_graph.mmd
├── code_stats/
│   ├── language_distribution.json
│   └── repository_info.json
└── vollstaendige_dokumentation.md  (alle Kapitel kombiniert)
```

## Beispiel-Workflow

### 1. Vorbereitung

```bash
# Repository bereit haben
cd ~/projects/my-bachelor-project

# Tool installieren
cd ~/thesis-tools
git clone <this-repo>
cd Multi-Language-Bachelor-Thesis-Documentation-Generator
pip install -r requirements.txt

# API Key setzen
export ANTHROPIC_API_KEY="sk-ant-..."

# Konfiguration erstellen
cp config.yaml.example config.yaml
nano config.yaml  # Projekt-Details eintragen
```

### 2. Dokumentation generieren

```bash
python thesis_doc_gen.py \
  --repo-path ~/projects/my-bachelor-project \
  --output ~/thesis/technical-documentation \
  --config config.yaml \
  --verbose
```

### 3. Ergebnis prüfen

```bash
ls ~/thesis/technical-documentation/

# Kombinierte Dokumentation ansehen
cat ~/thesis/technical-documentation/vollstaendige_dokumentation.md

# Diagramme ansehen (z.B. in VS Code mit Mermaid Extension)
code ~/thesis/technical-documentation/diagrams/
```

### 4. In Bachelorarbeit einbinden

Die generierten Markdown-Dateien können:
- Direkt in LaTeX konvertiert werden (pandoc)
- In Word kopiert werden
- Als Basis für Überarbeitung dienen

## Unterstützte Programmiersprachen

| Sprache | Extensions | Features |
|---------|-----------|----------|
| **Python** | `.py`, `.pyw` | Klassen, Funktionen, Imports, Docstrings, Frameworks |
| **JavaScript/TypeScript** | `.js`, `.jsx`, `.ts`, `.tsx` | Klassen, Funktionen, Imports/Exports, Frameworks |
| **Java** | `.java` | Klassen, Interfaces, Methods, Packages, Frameworks |
| **SQL** | `.sql` | Tables, Views, Procedures, Functions, Indexes |

## Diagramme ansehen

Die generierten Mermaid-Diagramme können mit folgenden Tools angesehen werden:

1. **VS Code**: Mermaid Extension installieren
2. **Online**: https://mermaid.live/
3. **CLI**: `mmdc` (mermaid-cli)
4. **In Markdown**: Direkt in GitHub/GitLab angezeigt

## Troubleshooting

### "ANTHROPIC_API_KEY not found"

```bash
# API Key setzen
export ANTHROPIC_API_KEY="sk-ant-your-key"

# Oder in config.yaml (nicht empfohlen für Sicherheit)
```

### "No Git repository found"

- Das ist ein Warning, kein Error
- Git-History-Kapitel wird übersprungen
- Andere Kapitel werden trotzdem generiert

### Zu wenig Speicher / API Limits

- Nutze `--languages` um nur spezifische Sprachen zu analysieren
- Erhöhe `max_file_size_kb` in config.yaml
- Füge mehr Pfade zu `exclude_paths` hinzu

### Generierte Kapitel zu generisch

- Füge mehr Kontext in `config.yaml` hinzu
- Stelle sicher dass Code gut kommentiert ist
- Nutze aussagekräftige Commit-Messages für bessere Git-Analyse

## Entwicklung

### Projekt-Struktur

```
thesis_doc_gen/
├── analyzers/
│   ├── base.py           # Basis-Analyzer
│   ├── python.py         # Python-Analyzer
│   ├── javascript.py     # JS/TS-Analyzer
│   ├── java.py           # Java-Analyzer
│   ├── sql.py            # SQL-Analyzer
│   └── factory.py        # Analyzer-Factory
├── utils/
│   ├── git_parser.py     # Git-History Parser
│   ├── file_scanner.py   # Datei-System Scanner
│   ├── claude_client.py  # Claude API Client
│   └── diagram_generator.py  # Mermaid-Diagramme
└── chapter_generator.py  # Dokumentations-Generator
```

### Neue Sprache hinzufügen

1. Erstelle `thesis_doc_gen/analyzers/new_language.py`
2. Erbe von `BaseAnalyzer`
3. Implementiere `analyze_file()` und `extract_structure()`
4. Registriere in `factory.py`

### Tests ausführen

```bash
# Unit tests (TODO: implement)
pytest tests/

# Integration test (mit echtem Projekt)
python thesis_doc_gen.py --repo-path ./test-project --dry-run
```

## FAQ

**Q: Kostet die Claude API Geld?**
A: Ja, Claude API ist kostenpflichtig. Ein typisches mittelgroßes Projekt kostet ca. $1-3 für die komplette Dokumentation.

**Q: Kann ich die Dokumentation auf Englisch generieren?**
A: Ja, setze `output.language: en` in `config.yaml`.

**Q: Funktioniert es ohne Git?**
A: Ja, das Git-History-Kapitel wird übersprungen, alle anderen Kapitel werden generiert.

**Q: Kann ich eigene Kapitel-Templates hinzufügen?**
A: Ja, erweitere `ChapterGenerator` in `chapter_generator.py`.

**Q: Wie lange dauert die Generierung?**
A: Ca. 3-7 Minuten für ein mittelgroßes Projekt (je nach API-Geschwindigkeit).

**Q: Sind die generierten Texte plagiatsfrei?**
A: Ja, Claude generiert originale Texte basierend auf DEINEM Code. Trotzdem empfohlen: Überarbeiten und mit eigenen Worten anpassen.

## Lizenz

MIT License - siehe LICENSE Datei.

## Autor

Entwickelt für Bachelorarbeiten an deutschen Hochschulen.

## Support

Bei Fragen oder Problemen:
1. Prüfe die [Troubleshooting](#troubleshooting) Sektion
2. Schaue in `thesis_doc_gen.log` für Details
3. Erstelle ein Issue im Repository

## Roadmap

- [ ] PDF-Export mit pandoc
- [ ] Support für C# und Go
- [ ] Interaktive Diagramm-Bearbeitung
- [ ] Template-System für eigene Kapitel
- [ ] Multi-Repository Support
- [ ] GUI Interface

## Changelog

### v1.0.0 (2025-01)
- Initial release
- Support für Python, JavaScript/TypeScript, Java, SQL
- 7 Dokumentationskapitel
- Mermaid-Diagramme
- Git-History-Analyse
- YAML-Konfiguration
