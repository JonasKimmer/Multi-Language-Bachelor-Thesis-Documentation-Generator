# Test-Anleitung (Deutsch)

## Schnelltest mit Beispiel-Projekt

### Schritt 1: Dependencies installieren

```bash
pip install -r requirements.txt
```

### Schritt 2: Test-Projekt erstellen

```bash
# Erstelle ein einfaches Test-Projekt
mkdir -p test-project/src
cd test-project

# Erstelle eine Python-Datei
cat > src/main.py <<'EOF'
"""Beispiel-Anwendung für Tests."""

class Calculator:
    """Eine einfache Rechner-Klasse."""

    def add(self, a, b):
        """Addiere zwei Zahlen."""
        return a + b

    def multiply(self, a, b):
        """Multipliziere zwei Zahlen."""
        return a * b

def main():
    """Hauptfunktion."""
    calc = Calculator()
    result = calc.add(5, 3)
    print(f"Ergebnis: {result}")

if __name__ == "__main__":
    main()
EOF

# Erstelle eine JavaScript-Datei
cat > src/app.js <<'EOF'
// Beispiel JavaScript Anwendung

class UserManager {
    constructor() {
        this.users = [];
    }

    addUser(name, email) {
        this.users.push({ name, email });
    }

    getUsers() {
        return this.users;
    }
}

const manager = new UserManager();
manager.addUser("Max", "max@example.com");
EOF

# Git initialisieren
git init
git add .
git commit -m "Initial commit: Add calculator and user manager"

# Noch ein paar Commits
echo "# Test Project" > README.md
git add README.md
git commit -m "Add README"

echo "tests/" > .gitignore
git add .gitignore
git commit -m "Add gitignore"
```

### Schritt 3: Dry-Run Test

```bash
cd ..  # zurück zum Tool-Verzeichnis
python thesis_doc_gen.py \
  --repo-path ./test-project \
  --output ./test-output \
  --dry-run
```

**Erwartete Ausgabe:**
```
=== DRY RUN MODE ===
Would generate the following:
  - Output directory: ./test-output
  - 8 documentation chapters
  - Up to 5 diagrams
  - Combined documentation file
  - Code statistics JSON files
```

### Schritt 4: Voller Test mit API

#### Option A: Mit Claude API (Original)

```bash
# API Key setzen
export ANTHROPIC_API_KEY="sk-ant-dein-key-hier"

# Konfiguration erstellen
cat > test-config.yaml <<'EOF'
project:
  name: "Test Projekt"
  author: "Test Nutzer"
  supervisor: "Prof. Test"
  university: "Test Hochschule"
  year: 2025

analysis:
  languages: auto
  exclude_paths:
    - node_modules/
    - venv/

output:
  language: de
  chapter_length: 300  # Kürzer für Tests

documentation:
  style: academic
  include_code_examples: true
EOF

# Generiere Dokumentation
python thesis_doc_gen.py \
  --repo-path ./test-project \
  --output ./test-output \
  --config test-config.yaml \
  --verbose
```

#### Option B: Mit Llama 3.1 8B (siehe unten)

```bash
# Llama mit Ollama (lokal, kostenlos)
python thesis_doc_gen.py \
  --repo-path ./test-project \
  --output ./test-output \
  --config test-config.yaml \
  --model llama \
  --verbose
```

### Schritt 5: Ergebnisse prüfen

```bash
# Zeige generierte Dateien
ls -lh test-output/

# Zeige Executive Summary
cat test-output/00_executive_summary.md

# Zeige Diagramme
ls -lh test-output/diagrams/

# Zeige Statistiken
cat test-output/code_stats/language_distribution.json
```

## Test mit echtem Projekt

```bash
# Teste mit deinem echten Projekt
python thesis_doc_gen.py \
  --repo-path ~/projects/meine-bachelorarbeit \
  --output ~/thesis/dokumentation \
  --config config.yaml \
  --verbose
```

## Troubleshooting beim Testen

### Problem: "ANTHROPIC_API_KEY not found"
**Lösung:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# Oder nutze Llama (siehe unten)
```

### Problem: "No Git repository found"
**Lösung:** Git initialisieren:
```bash
cd test-project
git init
git add .
git commit -m "Initial commit"
```

### Problem: Keine Dateien gefunden
**Lösung:** Prüfe ob Dateien im richtigen Format sind:
```bash
find test-project -name "*.py" -o -name "*.js"
```

### Problem: API zu langsam/teuer
**Lösung:** Nutze Llama 3.1 8B lokal (siehe nächster Abschnitt)

## Performance-Test

```bash
# Miss die Zeit
time python thesis_doc_gen.py \
  --repo-path ./test-project \
  --output ./test-output \
  --config test-config.yaml

# Typische Zeiten:
# - Kleines Projekt (<20 Dateien): 2-3 Minuten
# - Mittleres Projekt (20-100 Dateien): 3-7 Minuten
# - Großes Projekt (>100 Dateien): 7-15 Minuten
```

## Unit-Tests (TODO - für Entwickler)

```bash
# Teste einzelne Komponenten
python -m pytest tests/ -v

# Teste spezifischen Analyzer
python -c "
from thesis_doc_gen.analyzers.python import PythonAnalyzer
from pathlib import Path
analyzer = PythonAnalyzer()
result = analyzer.analyze_file(Path('test-project/src/main.py'))
print(f'Found {len(result[\"classes\"])} classes')
"
```

## Validierung der Ausgabe

### Prüfe ob alle Kapitel generiert wurden
```bash
expected_chapters=(
  "00_executive_summary.md"
  "01_systemarchitektur.md"
  "02_code_struktur.md"
  "03_implementierung_chronologie.md"
  "04_technische_entscheidungen.md"
  "05_feature_backlog.md"
  "06_mehrwert_analyse.md"
  "07_methodik.md"
)

for chapter in "${expected_chapters[@]}"; do
  if [ -f "test-output/$chapter" ]; then
    echo "✓ $chapter"
  else
    echo "✗ $chapter FEHLT!"
  fi
done
```

### Prüfe Diagramme
```bash
# Alle Diagramme sollten valide Mermaid-Syntax haben
for diagram in test-output/diagrams/*.mmd; do
  if grep -q "```mermaid" "$diagram"; then
    echo "✓ $(basename $diagram) ist valide"
  else
    echo "✗ $(basename $diagram) hat keine Mermaid-Syntax!"
  fi
done
```

### Prüfe Wort-Anzahl
```bash
# Jedes Kapitel sollte mindestens 200 Wörter haben
for chapter in test-output/*.md; do
  words=$(wc -w < "$chapter")
  echo "$(basename $chapter): $words Wörter"
done
```

## Test-Checkliste

- [ ] Dependencies installiert
- [ ] Test-Projekt erstellt
- [ ] Dry-run erfolgreich
- [ ] Voller Durchlauf erfolgreich
- [ ] Alle 8 Kapitel generiert
- [ ] Diagramme generiert
- [ ] Statistiken erstellt
- [ ] Kombiniertes Dokument erstellt
- [ ] Keine Fehler in Logs
- [ ] Dokumentation ist lesbar und sinnvoll
