# Llama 3.1 8B Anleitung (Deutsch)

## Warum Llama 3.1 8B?

**Vorteile gegenüber Claude:**
- ✅ **100% KOSTENLOS** (lokal mit Ollama)
- ✅ **Offline nutzbar** (keine Internet-Verbindung nötig)
- ✅ **Datenschutz** (Code verlässt deinen Computer nicht)
- ✅ **Keine API-Limits**
- ✅ **Schnell** (bei guter Hardware)

**Nachteile:**
- ⚠️ Qualität der Texte etwas geringer als Claude
- ⚠️ Benötigt ca. 8 GB RAM
- ⚠️ Langsamer als Claude API (je nach Hardware)

## Installation (3 Optionen)

### Option 1: Ollama (EMPFOHLEN - lokal & kostenlos)

**Schritt 1: Ollama installieren**

```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Oder manuell von: https://ollama.com/download
```

**Schritt 2: Llama 3.1 8B herunterladen**

```bash
ollama pull llama3.1:8b
```

**Schritt 3: Testen**

```bash
# Ollama starten (läuft im Hintergrund)
ollama serve

# Test
ollama run llama3.1:8b "Hallo, wie geht es dir?"
```

**Schritt 4: Tool nutzen**

```bash
python thesis_doc_gen.py \
  --repo-path ./mein-projekt \
  --output ./docs \
  --llm-backend llama-ollama
```

---

### Option 2: HuggingFace API (Cloud, kostenlos mit Limits)

**Schritt 1: Account erstellen**
- Gehe zu https://huggingface.co/
- Erstelle kostenlosen Account

**Schritt 2: API Token erstellen**
- Gehe zu https://huggingface.co/settings/tokens
- Erstelle neuen Token

**Schritt 3: Token setzen**

```bash
export HUGGINGFACE_API_KEY="hf_your_token_here"
```

**Schritt 4: Tool nutzen**

```bash
python thesis_doc_gen.py \
  --repo-path ./mein-projekt \
  --output ./docs \
  --llm-backend llama-hf
```

---

### Option 3: Hybrid (Ollama + Claude)

Du kannst auch beide kombinieren:

```bash
# Erst die Code-Analyse durchführen (ohne LLM)
python thesis_doc_gen.py \
  --repo-path ./mein-projekt \
  --output ./docs \
  --dry-run

# Dann einzelne Kapitel mit Llama testen
python thesis_doc_gen.py \
  --repo-path ./mein-projekt \
  --output ./docs-llama \
  --llm-backend llama-ollama

# Und parallel mit Claude für Vergleich
python thesis_doc_gen.py \
  --repo-path ./mein-projekt \
  --output ./docs-claude \
  --llm-backend claude
```

## Verwendung

### Basis-Verwendung mit Ollama

```bash
python thesis_doc_gen.py \
  --repo-path ~/projects/meine-ba \
  --output ~/thesis/docs \
  --llm-backend llama-ollama \
  --verbose
```

### Mit anderem Llama-Model

```bash
# Liste verfügbare Modelle
ollama list

# Nutze anderes Modell (z.B. größeres 70B Modell)
python thesis_doc_gen.py \
  --repo-path ./projekt \
  --output ./docs \
  --llm-backend llama-ollama \
  --llm-model llama3.1:70b
```

### Mit HuggingFace

```bash
export HUGGINGFACE_API_KEY="hf_..."

python thesis_doc_gen.py \
  --repo-path ./projekt \
  --output ./docs \
  --llm-backend llama-hf
```

## Konfiguration für Llama anpassen

Erstelle `config-llama.yaml`:

```yaml
project:
  name: "Mein Projekt"
  author: "Dein Name"
  supervisor: "Prof. Dr. XY"
  university: "TH Köln"
  year: 2025

analysis:
  languages: auto

output:
  language: de
  chapter_length: 400  # Kürzer für schnellere Llama-Generierung

documentation:
  style: academic
  include_code_examples: true
  max_code_lines_per_example: 20  # Weniger für bessere Qualität
```

Dann nutzen:

```bash
python thesis_doc_gen.py \
  --repo-path ./projekt \
  --output ./docs \
  --config config-llama.yaml \
  --llm-backend llama-ollama
```

## Performance-Optimierung

### Ollama Performance verbessern

```bash
# GPU-Beschleunigung nutzen (falls verfügbar)
# Ollama nutzt automatisch CUDA/Metal

# Mehr RAM für Ollama freigeben
# In ~/.ollama/config.yaml:
# num_gpu: 1
# num_thread: 8
```

### Schnellere Generierung

```yaml
# In config.yaml
output:
  chapter_length: 300  # Statt 600

documentation:
  max_code_lines_per_example: 15  # Statt 30
```

## Qualitätsvergleich

### Llama 3.1 8B (Ollama)
- **Geschwindigkeit**: Mittel (abhängig von Hardware)
- **Kosten**: Kostenlos
- **Qualität**: Gut (ca. 80% von Claude)
- **Best für**: Erste Entwürfe, Brainstorming, Offline-Arbeit

### Claude Sonnet
- **Geschwindigkeit**: Schnell
- **Kosten**: ~$1-3 pro Projekt
- **Qualität**: Exzellent
- **Best für**: Finale Dokumentation, wissenschaftliche Präzision

## Empfohlener Workflow

### 1. Entwicklung (Llama - kostenlos)
```bash
# Mehrere Iterationen während Entwicklung
python thesis_doc_gen.py \
  --repo-path ./projekt \
  --output ./docs-draft \
  --llm-backend llama-ollama \
  --config config-short.yaml
```

### 2. Review & Verbesserung
- Prüfe generierte Kapitel
- Verbessere Code-Kommentare basierend auf Feedback
- Überarbeite Commit-Messages

### 3. Finale Version (Claude - bezahlt)
```bash
# Finale hochwertige Dokumentation
python thesis_doc_gen.py \
  --repo-path ./projekt \
  --output ./docs-final \
  --llm-backend claude \
  --config config.yaml
```

## Troubleshooting

### "Cannot connect to Ollama"

```bash
# Prüfe ob Ollama läuft
ps aux | grep ollama

# Starte Ollama
ollama serve

# In separatem Terminal:
python thesis_doc_gen.py --llm-backend llama-ollama ...
```

### "Model not found"

```bash
# Liste installierte Modelle
ollama list

# Installiere Llama 3.1 8B
ollama pull llama3.1:8b

# Oder nutze anderes installiertes Modell
python thesis_doc_gen.py --llm-model llama3.1:latest ...
```

### Ollama läuft, aber sehr langsam

```bash
# Prüfe System-Ressourcen
top

# Nutze kleineres Modell
ollama pull llama3.1:8b-q4_0  # Quantisierte Version

# Oder nutze HuggingFace API stattdessen
python thesis_doc_gen.py --llm-backend llama-hf ...
```

### HuggingFace API Fehler

```bash
# Prüfe API Key
echo $HUGGINGFACE_API_KEY

# Prüfe Rate Limits
# HuggingFace hat ~1000 Requests/Tag (kostenlos)

# Alternative: Nutze Ollama lokal
python thesis_doc_gen.py --llm-backend llama-ollama ...
```

### Qualität der Texte zu niedrig

**Tipps für bessere Ergebnisse mit Llama:**

1. **Bessere Code-Kommentare**
   - Llama braucht mehr Kontext als Claude
   - Füge Docstrings hinzu
   - Kommentiere komplexe Logik

2. **Bessere Commit-Messages**
   - Llama interpretiert Git-History basierend auf Commits
   - Schreibe aussagekräftige Messages

3. **Kürzere Kapitel**
   ```yaml
   output:
     chapter_length: 300  # Besser für Llama
   ```

4. **Mehr Kontext in config.yaml**
   ```yaml
   project:
     description: "Detaillierte Beschreibung..."
     goals: "Projektziele..."
   ```

5. **Post-Processing**
   - Generiere mit Llama
   - Überarbeite manuell
   - Eventuell einzelne Kapitel mit Claude neu generieren

## Modell-Empfehlungen

### Für unterschiedliche Hardware:

**16 GB RAM oder mehr:**
```bash
ollama pull llama3.1:8b  # Standard, beste Qualität
```

**8-16 GB RAM:**
```bash
ollama pull llama3.1:8b-q4_0  # Quantisiert, weniger RAM
```

**< 8 GB RAM:**
```bash
# Nutze HuggingFace API statt lokal
python thesis_doc_gen.py --llm-backend llama-hf
```

**Viel RAM (32+ GB) und Zeit:**
```bash
ollama pull llama3.1:70b  # Größeres Modell, bessere Qualität
python thesis_doc_gen.py --llm-model llama3.1:70b ...
```

## Kostenvergleich

### Llama (Ollama lokal)
- **Setup**: Einmalig 10-30 Min
- **Laufende Kosten**: 0 €
- **Pro Projekt**: 0 €
- **Strafe**: Etwas geringere Qualität

### Claude API
- **Setup**: 2 Min (API Key)
- **Laufende Kosten**: 0 € (pay-as-you-go)
- **Pro Projekt**: ~1-3 € (mittelgroß)
- **Vorteil**: Höchste Qualität

### Empfehlung
- **Entwicklung & Tests**: Llama (kostenlos)
- **Finale Abgabe**: Claude (beste Qualität)
- **Budget-bewusst**: Nur Llama + manuelle Überarbeitung

## FAQ

**Q: Ist Llama wirklich kostenlos?**
A: Ja! Mit Ollama lokal komplett kostenlos. Kein API-Limit.

**Q: Wie gut ist die Qualität vs. Claude?**
A: Ca. 70-80% von Claude. Für erste Entwürfe absolut ausreichend.

**Q: Kann ich beides nutzen?**
A: Ja! Generiere Entwürfe mit Llama, finale Version mit Claude.

**Q: Brauche ich Internet für Ollama?**
A: Nein! Nach dem Download von llama3.1:8b läuft alles offline.

**Q: Wie lange dauert die Generierung?**
A: Mit Llama lokal: 5-15 Min (je nach Hardware). Mit Claude: 3-7 Min.

**Q: Versteht Llama auch Deutsch?**
A: Ja, Llama 3.1 ist multilingual und generiert gute deutsche Texte.
