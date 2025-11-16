# Implementierung eines KI-gestützten Chatbots für die kommunale Verwaltung: Fallstudie Chatbot Rüsselsheim

**Hausarbeit**

Vorgelegt von: Jonas Kimmer
Hochschule: TH Köln
Jahr: 2025

---

## Inhaltsverzeichnis

1. Einleitung
2. Motivation
3. Theoretische Grundlagen
4. Fallstudie: Chatbot Rüsselsheim
5. Technische Implementierung und Architektur
6. Diskussion: Herausforderungen und Lösungsansätze
7. Zusammenfassung und Ausblick

---

## 1. Einleitung

### 1.1 Digitale Transformation und Herausforderungen der Verwaltung

Die deutsche Kommunalverwaltung steht unter erheblichem Druck zur digitalen Transformation. Zu den drängendsten Herausforderungen zählt die angespannte Finanzlage vieler Kommunen, die teilweise Haushaltskonsolidierungen erforderlich macht. Ein weiteres zentrales Problem ist der drohende Fachkräftemangel: Bis 2032 geht etwa ein Viertel der im öffentlichen Dienst Beschäftigten in den Ruhestand. Diese Personallücke lässt sich nicht durch Neueinstellungen schließen (Wielgosch & Dieke 2024, S. 28-29).

KI-Anwendungen bieten große Potenziale, um Aufgaben effizienter zu erfüllen, Prozesse kostengünstiger durchzuführen und Mitarbeitende zu entlasten. Bereits 66 Prozent der Kommunen halten den Einsatz von KI für sinnvoll. Trotz dieser hohen Akzeptanz nutzten 2023 lediglich acht Prozent der Kommunen KI in ihrer Verwaltung. Die Kluft zwischen Potenzial und Umsetzung liegt in begrenzten Ressourcen, fehlender Akzeptanz, rechtlichen Unsicherheiten sowie offenen Fragen zum Datenschutz (Wielgosch & Dieke 2024, S. 30-32).

### 1.2 Large Language Models als Game Changer

Im Herbst 2022 veränderte OpenAI mit dem Chatbot GPT-3 die Technologielandschaft grundlegend. Large Language Models (LLMs) sind große, vortrainierte neuronale Netze, die auf die Verarbeitung und Generierung natürlicher Sprache spezialisiert sind. Sie verfügen über die außergewöhnliche Fähigkeit, menschliche Sprache zu verstehen, zu generieren und zu manipulieren (Wielgosch & Dieke 2024, S. 12, 24; Evanto 2025, S. 236, 252-253; Dam et al. 2024, S. 368).

Das Aufkommen dieser Modelle ermöglichte eine neue Generation von KI-Anwendungen mit deutlich höherem Potenzial. In der Verwaltung liegen die Anwendungsschwerpunkte auf Bürgerservices und interner Verwaltung. LLM-basierte Chatbots zur Information von Bürger:innen und zur internen Unterstützung von Verwaltungsmitarbeitenden sind weit verbreitet (Wielgosch & Dieke 2024, S. 6, 77).

### 1.3 Forschungsfrage und Fallstudienobjekt

Diese Arbeit untersucht die zentrale Frage: **Wie kann ein datenschutzkonformer, multi-modaler KI-Chatbot für kommunale Bürgerservices konzipiert und implementiert werden, und welche technischen Herausforderungen entstehen dabei?**

Als Fallstudienobjekt dient die Eigenentwicklung eines intelligenten Chatbot-Systems für die Stadt Rüsselsheim. Im Gegensatz zu kommerziellen Lösungen wurde dieser Chatbot als Open-Source-Projekt vollständig selbst entwickelt und demonstriert einen innovativen Ansatz durch:

- **Multi-LLM-Unterstützung**: Wahlweise Nutzung von Ollama (lokal), Google Gemini oder Anthropic Claude
- **9 API-Integrationen**: Echtzeit-Zugriff auf Wetter, Karten, Verkehr, ÖPNV, Müllabfuhr, Tankstellen, Feiertage und lokale Nachrichten
- **RAG-System**: Retrieval Augmented Generation für präzise Antworten basierend auf Stadtdokumenten
- **Datenschutz-First**: Vollständige Datensouveränität durch lokale Deployment-Option

### 1.4 Aufbau der Arbeit

Die Arbeit gliedert sich in sieben Kapitel. Kapitel 2 erläutert die Motivation für die Eigenentwicklung. Kapitel 3 führt in die technologischen Bausteine ein. Kapitel 4 stellt das Projekt detailliert vor. Kapitel 5 analysiert die technische Architektur und Implementierung. Kapitel 6 diskutiert Herausforderungen und Lösungsansätze. Kapitel 7 fasst die Kernerkenntnisse zusammen.

---

## 2. Motivation

### 2.1 Warum eine Eigenentwicklung?

Während viele Kommunen auf schlüsselfertige KI-Lösungen von Dienstleistern setzen, wurde für Rüsselsheim bewusst der Weg der Eigenentwicklung gewählt. Diese Entscheidung basiert auf mehreren strategischen Überlegungen:

**Datensouveränität**: Durch die vollständige Kontrolle über den Quellcode und die Deployment-Infrastruktur behält die Kommune die Hoheit über alle Bürgerdaten. Im Gegensatz zu Cloud-basierten SaaS-Lösungen können alle Komponenten on-premise betrieben werden.

**Technologische Flexibilität**: Die Architektur erlaubt den flexiblen Wechsel zwischen verschiedenen LLM-Anbietern (Ollama, Gemini, Claude), was Vendor Lock-in vermeidet und Kostenoptimierung ermöglicht.

**Anpassbarkeit**: Als Open-Source-Projekt kann das System exakt an die spezifischen Bedürfnisse der Stadt Rüsselsheim angepasst werden, ohne auf die Roadmap eines kommerziellen Anbieters angewiesen zu sein.

**Kostenkontrolle**: Durch die Möglichkeit, Ollama lokal zu betreiben, entstehen keine laufenden API-Kosten. Dies ist insbesondere für kleinere Kommunen mit begrenzten Budgets relevant.

### 2.2 Spezifische Anforderungen der Stadt Rüsselsheim

Die Stadt Rüsselsheim hat spezifische Anforderungen an einen Bürgerservice-Chatbot, die über reine Informationsabfragen hinausgehen:

1. **Multimodale Informationsbereitstellung**: Neben statischen Verwaltungsinformationen soll der Chatbot Echtzeit-Daten wie aktuelle Wetterbedingungen, ÖPNV-Verbindungen, Müllabfuhrtermine und Blitzer-Standorte bereitstellen.

2. **Barrierefreiheit**: Der Service soll 24/7 verfügbar sein und komplexe Verwaltungsinformationen verständlich aufbereiten.

3. **Mehrsprachigkeit**: Durch die Nutzung moderner LLMs soll der Chatbot Anfragen in verschiedenen Sprachen bearbeiten können.

4. **DSGVO-Konformität**: Strikte Einhaltung des Datenschutzes durch lokale Datenverarbeitung und automatische Anonymisierung personenbezogener Daten.

### 2.3 Abgrenzung zu existierenden Lösungen

Im Vergleich zu Projekten wie Bonn.digital (neurabot) oder Bad Oeynhausen (Colon Sültemeyer) zeichnet sich der Rüsselsheim-Chatbot durch folgende Alleinstellungsmerkmale aus:

- **API-First-Architektur**: Neun dedizierte API-Integrationen für Echtzeit-Informationen
- **Multi-Backend-Strategie**: Keine Abhängigkeit von einem einzelnen LLM-Anbieter
- **Modulares Design**: Klare Trennung in API-, Service- und Daten-Layer für einfache Wartung und Erweiterung
- **RAG mit pgvector**: Einsatz der hochperformanten PostgreSQL-Erweiterung für Vektor-Embeddings

---

## 3. Theoretische Grundlagen

### 3.1 Large Language Models und Transformer-Architektur

Large Language Models stellen eine Kategorie von Foundation Models dar, die auf einer breiten Datenbasis vortrainiert werden. Sie basieren in der Regel auf der 2017 von Google vorgestellten Transformer-Architektur, die durch den Self-Attention-Mechanismus die Beziehungen zwischen allen Wörtern parallel auswertet (Evanto 2025, S. 222, 229; Dam et al. 2024, S. 368).

Die GPT-Serien arbeiten autoregressiv und generieren Text Schritt für Schritt, indem sie das nächstwahrscheinlichste Wort auf Grundlage der vorhergehenden Wörter vorhersagen. Im Projekt Rüsselsheim kommen drei verschiedene LLM-Backends zum Einsatz:

1. **Ollama mit Llama 3.1 8B**: Open-Source-Modell für lokales Deployment ohne API-Kosten
2. **Google Gemini 1.5 Flash**: Cloud-basiertes Modell mit kostenfreiem Kontingent
3. **Anthropic Claude**: Premium-Modell für höchste Genauigkeit

### 3.2 Retrieval Augmented Generation (RAG)

Retrieval Augmented Generation ist ein hybrider AI-Rahmen, der Large Language Models durch die Kombination mit externen, aktuellen Datenquellen stärkt. Ein RAG-System besteht aus Retriever, Embedding-Modell, Vektordatenbank und generativem Sprachmodell (Databricks RAG, S. 304, 308).

**Der RAG-Prozess im Detail**:

1. **Datenaufbereitung**: Stadtdokumente werden in kürzere Textabschnitte (Chunks) aufgeteilt
2. **Embedding-Generierung**: Ein Embedding-Modell (OpenAI oder sentence-transformers) überführt die Chunks in Vektordarstellung
3. **Speicherung**: Vektoren werden zusammen mit den Chunks in einer pgvector-Datenbank gespeichert
4. **Abfrage**: Bei einer Nutzeranfrage wird der Prompt in einen Anfragevektor umgewandelt
5. **Retrieval**: Die relevantesten Chunks werden via Cosine-Similarity-Suche abgerufen
6. **Generierung**: Das LLM erhält die Chunks als Kontext und generiert die Antwort

Im Rüsselsheim-Projekt ist RAG von zentraler Bedeutung, da es die Halluzinationsneigung von LLMs reduziert und sicherstellt, dass Antworten auf verifizierten Stadtinformationen basieren (DSK RAG, S. 502-503, 507-508).

### 3.3 FastAPI als Backend-Framework

FastAPI ist ein modernes, hochperformantes Web-Framework für Python, das auf ASGI (Asynchronous Server Gateway Interface) basiert. Es wurde für das Rüsselsheim-Projekt aus folgenden Gründen gewählt:

- **Asynchrone Verarbeitung**: Native async/await-Unterstützung für parallele API-Aufrufe
- **Automatische API-Dokumentation**: OpenAPI/Swagger-Integration out-of-the-box
- **Type Safety**: Pydantic-Integration für Request/Response-Validierung
- **Performance**: Vergleichbar mit NodeJS und Go

Die FastAPI-Architektur des Projekts folgt dem Layered-Architecture-Pattern mit klarer Trennung von API-Endpoints, Business-Logic (Services) und Datenzugriff (Models).

### 3.4 PostgreSQL mit pgvector

pgvector ist eine PostgreSQL-Erweiterung, die native Unterstützung für Vektor-Embeddings bietet. Im Vergleich zu spezialisierten Vektordatenbanken wie Pinecone oder Weaviate bietet pgvector den Vorteil der Integration in die bestehende relationale Datenbank:

- **Transaktionale Konsistenz**: ACID-Eigenschaften auch für Vektordaten
- **Einfaches Deployment**: Keine zusätzliche Infrastruktur nötig
- **Indexierung**: HNSW- und IVFFlat-Indizes für schnelle Similarity-Suche
- **SQL-Integration**: Vektorsuche kombinierbar mit relationalen Queries

---

## 4. Fallstudie: Chatbot Rüsselsheim

### 4.1 Projektüberblick und Entwicklungszeitraum

Das Projekt "Chatbot Rüsselsheim" wurde als vollständige Neuentwicklung konzipiert und am 8. November 2025 zwischen 11:31 und 15:02 Uhr (ca. 3,5 Stunden intensive Entwicklung) implementiert. In diesem Zeitraum entstanden 22 Git-Commits, die den iterativen Entwicklungsprozess dokumentieren.

**Projektzahlen**:
- 35 Python-Dateien
- 3.653 Zeilen Code
- 28 Klassen
- 41 Top-Level-Funktionen
- 9 API-Integrationen
- 3 LLM-Backends

### 4.2 Systemarchitektur

Die Architektur folgt einem modernen Layered-Design mit klarer Separation of Concerns:

```
┌─────────────────────────────────────┐
│     Presentation Layer (API)        │
│  - chat.py, documents.py, weather.py│
│  - maps.py, traffic.py, etc.        │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│      Business Logic (Services)      │
│  - OllamaService, GeminiService     │
│  - RAGService, EmbeddingService     │
│  - weather_service, maps_service    │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│       Data Layer (Models + DB)      │
│  - ChatSession, ChatMessage         │
│  - Document (mit pgvector)          │
│  - PostgreSQL + pgvector            │
└─────────────────────────────────────┘
```

**Verzeichnisstruktur**:
```
backend/app/
├── main.py                    # FastAPI Application
├── config.py                  # Pydantic Settings
├── api/                       # REST Endpoints
│   ├── chat.py               # POST /api/chat
│   ├── documents.py          # CRUD Dokumente
│   ├── weather.py            # GET /api/weather
│   ├── maps.py               # Geocoding, Suche
│   ├── traffic.py            # Blitzer-Datenbank
│   ├── transit.py            # RMV ÖPNV
│   ├── waste.py              # Müllabfuhr
│   ├── fuel.py               # Tankerkönig API
│   ├── holidays.py           # Feiertage
│   └── news.py               # Lokale News
├── models/                    # SQLAlchemy ORM
│   ├── chat.py               # ChatSession, ChatMessage
│   └── document.py           # Document (pgvector)
├── services/                  # Business Logic
│   ├── chat_service_ollama.py    # Ollama Client
│   ├── chat_service_gemini.py    # Gemini Client
│   ├── rag_service.py            # RAG-System
│   ├── embedding_service.py      # OpenAI Embeddings
│   ├── embedding_service_local.py# sentence-transformers
│   ├── api_helper.py             # Intent Detection
│   └── [API Services]            # 9 API Integrationen
└── db/
    └── database.py           # SQLAlchemy Engine
```

### 4.3 Kernkomponenten

#### 4.3.1 Datenmodell (SQLAlchemy ORM)

**ChatSession** (`models/chat.py`):
```python
class ChatSession(Base, TimestampMixin):
    __tablename__ = "chat_sessions"
    id = Column(Integer, primary_key=True)
    session_id = Column(String(100), unique=True)
    user_identifier = Column(String(200))
    title = Column(String(500))
    is_active = Column(Integer, default=1)
    messages = relationship("ChatMessage", back_populates="session")
```

**ChatMessage** (`models/chat.py`):
```python
class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(Base, TimestampMixin):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    role = Column(Enum(MessageRole))
    content = Column(Text)
    context_used = Column(Text)  # RAG-Kontext
```

**Document mit pgvector** (`models/document.py`):
```python
from pgvector.sqlalchemy import Vector

class Document(Base, TimestampMixin):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    content = Column(Text)
    category = Column(String(100))
    source = Column(String(500))
    embedding = Column(Vector(384))  # pgvector!
```

Die Verwendung von `Vector(384)` entspricht der Dimensionalität des `all-MiniLM-L6-v2` Embedding-Modells von sentence-transformers.

#### 4.3.2 Chat-Services (Strategy Pattern)

Die Chat-Services implementieren das Strategy-Pattern, um zwischen verschiedenen LLM-Backends wechseln zu können:

**OllamaService** (`services/chat_service_ollama.py`):
```python
class OllamaService:
    def __init__(self, db: Session):
        self.db = db
        self.client = ollama.Client(host=settings.ollama_host)
        self.rag_service = RAGService(db)

    async def chat(self, session_id: str, message: str) -> Dict[str, Any]:
        # 1. Intent Detection
        api_intent = detect_api_intent(message)

        # 2. API-Aufruf (falls erkannt)
        if api_intent == "weather":
            api_data = await get_weather_info()
        elif api_intent == "transit":
            api_data = await get_departures()
        # ... weitere Intents

        # 3. RAG-Context abrufen
        context = self.rag_service.get_context_for_query(message)

        # 4. Prompt mit API-Daten + RAG-Context
        prompt = self._build_prompt(message, api_data, context)

        # 5. LLM-Aufruf
        response = self.client.generate(
            model="llama3.1:8b",
            prompt=prompt
        )

        # 6. Speicherung in DB
        self._save_conversation(session_id, message, response)

        return response
```

Die `GeminiService`-Klasse folgt demselben Muster, nutzt aber die Google Generative AI SDK.

#### 4.3.3 RAG-Service

**RAGService** (`services/rag_service.py`):
```python
class RAGService:
    def __init__(self, db: Session):
        self.db = db
        # Embedding-Provider-Wahl
        if settings.embedding_provider == "openai":
            self.embedding_service = EmbeddingService()
        else:
            self.embedding_service = LocalEmbeddingService()

    def add_document(self, title: str, content: str, category: str) -> Document:
        """Dokument mit Embedding hinzufügen"""
        embedding = self.embedding_service.create_embedding(content)
        document = Document(
            title=title,
            content=content,
            category=category,
            embedding=embedding
        )
        self.db.add(document)
        self.db.commit()
        return document

    def get_context_for_query(self, query: str, top_k: int = 5) -> str:
        """Vector Similarity Search in pgvector"""
        query_embedding = self.embedding_service.create_embedding(query)

        # Cosine Similarity mit pgvector
        results = self.db.execute(text("""
            SELECT title, content,
                   1 - (embedding <=> :query_embedding) as similarity
            FROM documents
            ORDER BY embedding <=> :query_embedding
            LIMIT :top_k
        """), {
            "query_embedding": query_embedding,
            "top_k": top_k
        })

        # Kontext-String zusammenbauen
        context_chunks = []
        for row in results:
            context_chunks.append(f"[{row.title}]: {row.content}")

        return "\n\n".join(context_chunks)
```

Die `<=>` Operator ist der pgvector Cosine-Distance-Operator. Durch `1 - distance` wird daraus eine Similarity.

#### 4.3.4 API-Integrationen

Im Gegensatz zu reinen Informations-Chatbots integriert das Rüsselsheim-System neun externe APIs:

1. **Weather Service** (`services/weather_service.py`):
   - Provider: Open-Meteo (kostenfrei)
   - Funktion: Aktuelle Wetterdaten und 7-Tage-Vorhersage für Rüsselsheim

2. **Maps Service** (`services/maps_service.py`):
   - Provider: Nominatim (OpenStreetMap)
   - Funktionen: Geocoding, Reverse Geocoding, POI-Suche

3. **Traffic Service** (`services/traffic_service.py`):
   - Statische Blitzer-Datenbank für Rüsselsheim und Umgebung
   - GPS-Koordinaten mit Radius-Suche

4. **Transit Service** (`services/transit_service.py`):
   - Provider: RMV (Rhein-Main-Verkehrsverbund) API
   - Echtzeitdaten für Busverbindungen

5. **Waste Service** (`services/waste_service.py`):
   - Abfallkalender der Stadt Rüsselsheim
   - Erinnerung an Abholtermine

6. **Fuel Service** (`services/fuel_service.py`):
   - Provider: Tankerkönig API
   - Aktuelle Spritpreise in der Umgebung

7. **Holidays Service** (`services/holidays_service.py`):
   - Provider: feiertage-api.de
   - Feiertage in Hessen

8. **News Service** (`services/news_service.py`):
   - Lokale Nachrichten aus Rüsselsheim

9. **API Helper** (`services/api_helper.py`):
   - Intent Detection via Keyword-Matching
   - Routing zu passenden API-Services

**Intent Detection Beispiel**:
```python
def detect_api_intent(message: str) -> Optional[str]:
    message_lower = message.lower()

    # Wetter
    if any(kw in message_lower for kw in ['wetter', 'temperatur', 'regen', 'grad']):
        return "weather"

    # ÖPNV
    if any(kw in message_lower for kw in ['bus', 'bahn', 'abfahrt', 'rmv']):
        return "transit"

    # Müll
    if any(kw in message_lower for kw in ['müll', 'abfall', 'tonne', 'gelber sack']):
        return "waste"

    # ... weitere Intents

    return None
```

### 4.4 Design Patterns und Best Practices

Das Projekt implementiert mehrere etablierte Software-Design-Patterns:

| Pattern | Verwendung | Beispiel |
|---------|------------|----------|
| **Strategy Pattern** | LLM-Provider austauschbar | `OllamaService`, `GeminiService` |
| **Dependency Injection** | Database Session als Constructor Param | `RAGService(db: Session)` |
| **Repository Pattern** | ORM Models kapseln DB-Zugriff | `ChatSession`, `Document` |
| **Factory Pattern** | Embedding Service Selection | `RAGService.__init__()` wählt Provider |
| **Layered Architecture** | API → Service → Model → DB | Klare Trennung der Schichten |

**Namenskonventionen (PEP 8)**:
- Klassen: `PascalCase` (ChatSession, RAGService)
- Funktionen: `snake_case` (get_weather, detect_api_intent)
- Konstanten: `UPPER_SNAKE_CASE` (RUESSELSHEIM_LAT, SPEED_CAMERAS)
- Private Methoden: `_leading_underscore` (_build_prompt)

---

## 5. Technische Implementierung und Architektur

### 5.1 Entwicklungschronologie

Die Entwicklung erfolgte in vier klar definierten Phasen:

**Phase 1: Grundlagen & RAG-System (11:31 - 11:39)**

| Zeit | Commit | Beschreibung |
|------|--------|--------------|
| 11:31 | 46b73fa | feat: Implement complete Rüsselsheim chatbot with RAG system<br>• FastAPI + PostgreSQL + pgvector Setup<br>• RAG Service für Dokumentensuche<br>• Chat Service mit Claude API<br>• ORM Models (ChatSession, Document)<br>• Docker Compose |
| 11:39 | c61063a | feat: Add local embeddings (no OpenAI needed)<br>• sentence-transformers Integration<br>• Kostenersparnis + Datenschutz |

**Technische Entscheidung**: RAG-System als Fundament, um Stadt-Dokumente durchsuchbar zu machen.

**Phase 2: Multi-LLM Support (11:44 - 12:50)**

| Zeit | Commit | Beschreibung |
|------|--------|--------------|
| 11:44 | 36698ce | feat: Add Google Gemini support for 100% free deployment<br>• Gemini 1.5 Flash Integration<br>• Alternative zu kostenpflichtigem Claude |
| 11:51-12:33 | 7 Commits | Gemini Bug Fixes:<br>• Docker Config<br>• API Version Kompatibilität<br>• Model Namen<br>• Dependency Conflicts |
| 12:42 | 5216322 | feat: Add Ollama support for local LLM<br>• Ollama Client Integration<br>• Llama 3.1 8B lokal<br>• Komplette DSGVO-Konformität |

**Priorität**: Kostenfreie LLM-Optionen ermöglichen (Gemini + Ollama), bevor weitere Features kommen.

**Begründung**: Kommunen sollten das System ohne API-Kosten testen können.

**Phase 3: API-Integrationen (13:18 - 13:47)**

| Zeit | Commit | Beschreibung |
|------|--------|--------------|
| 13:18 | 36bb336 | feat: Add free APIs for weather, maps, and traffic<br>• Weather Service (Open-Meteo)<br>• Maps Service (Nominatim/OSM)<br>• Traffic Service (Blitzer-DB)<br>• REST Endpoints |
| 13:40 | b2b0f1b | feat: Integrate APIs into chatbot<br>• api_helper.py mit Intent Detection<br>• Gemini Chat Service integriert APIs |
| 13:47 | 618d8c9 | feat: Add API integration to Ollama service<br>• Parität mit Gemini Service |

**Phase 4: Erweiterte APIs & Bugfixes (14:31 - 15:02)**

| Zeit | Commit | Beschreibung |
|------|--------|--------------|
| 14:31 | 1c5b017 | feat: Add 5 new API services<br>• Transit (RMV), Waste, Fuel, Holidays, News<br>• Alle in api_helper integriert |
| 15:02 | 903bb26 | fix: Improve API data handling<br>• LLM-Instruktion verstärkt<br>• API-Daten direkt weitergeben |

### 5.2 Datenschutz und DSGVO-Konformität

Das Projekt implementiert mehrere Mechanismen zur Einhaltung der DSGVO:

**1. Lokales Deployment (Ollama-Option)**:
- Llama 3.1 8B läuft vollständig on-premise
- Keine Datenübertragung an externe Anbieter
- Volle Kontrolle über Verarbeitungsprozesse

**2. EU-Server für Cloud-LLMs**:
- Gemini und Claude können über EU-Endpoints angesprochen werden
- Konfigurierbar via Settings

**3. RAG-Daten in eigener Datenbank**:
- Im Gegensatz zu Fine-Tuning bleiben Daten in PostgreSQL
- Einfache Umsetzung von Betroffenenrechten (Art. 15-22 DSGVO):
  - Auskunft: SQL-Query auf `documents` Tabelle
  - Löschung: DELETE auf `documents`
  - Berichtigung: UPDATE auf `documents`

**4. Session-basierte Anonymisierung**:
- `user_identifier` in `ChatSession` ist optional
- Sessions können ohne personenbezogene Daten erstellt werden
- Automatisches Cleanup alter Sessions möglich

**5. Keine Persistenz in LLM-Training**:
- Weder Ollama, Gemini noch Claude nutzen Chat-Daten für Training (konfigurierbar)
- Strikte API-Nutzungsbedingungen

### 5.3 Performance-Optimierungen

**Asynchrone API-Aufrufe**:
Alle API-Services sind als `async` Funktionen implementiert:

```python
async def get_weather_info():
    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_API_URL) as response:
            return await response.json()
```

Dies ermöglicht parallele Verarbeitung bei Multi-Intent-Anfragen.

**pgvector-Indexierung**:
Die Vektordatenbank nutzt HNSW-Index für schnelle Approximate Nearest Neighbor Search:

```sql
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
```

**Caching**:
Häufig abgerufene Informationen (Feiertage, Müllkalender) werden gecacht.

### 5.4 Deployment-Architektur

Das System ist als Docker-Compose-Stack konzipiert:

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://...
      - LLM_BACKEND=ollama  # oder gemini, claude
    depends_on:
      - db

  db:
    image: ankane/pgvector:latest
    environment:
      - POSTGRES_DB=chatbot
      - POSTGRES_USER=...
    volumes:
      - postgres_data:/var/lib/postgresql/data

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
```

---

## 6. Diskussion: Herausforderungen und Lösungsansätze

### 6.1 Technische Herausforderungen

**Problem 1: LLM-Halluzinationen trotz RAG**

Trotz der RAG-Integration tendieren insbesondere kleinere Modelle wie Llama 3.1 8B dazu, Informationen zu "erfinden". Während der Entwicklung wurden mehrere Gegenmaßnahmen implementiert:

*Lösung*:
- Explizite System-Prompts: "ERFINDE KEINE Informationen. Nutze NUR bereitgestellte Daten."
- Confidence-Scoring: LLM soll Unsicherheit ausdrücken ("Laut Dokument X...")
- Fallback zu strukturierten Daten: Bei kritischen Anfragen (Öffnungszeiten) direkt aus DB

**Problem 2: Intent Detection bei Mehrdeutigkeit**

Beispiel: "Wann kommt der nächste Bus zum Bahnhof?"
- Intent könnte sein: Transit (ÖPNV) ODER Maps (Navigation)

*Lösung*:
- Prioritätsreihenfolge in `api_helper.py`
- Bei Mehrdeutigkeit: Mehrere APIs parallel aufrufen
- LLM entscheidet, welche Informationen relevant sind

**Problem 3: API-Latenz vs. User Experience**

Einige APIs (RMV) haben Antwortzeiten >2 Sekunden.

*Lösung*:
- Asynchrone Verarbeitung (FastAPI async endpoints)
- Streaming-Response: Erste Antwort sofort, API-Daten nachladen
- Timeout-Handling: Nach 5 Sekunden Fallback ohne API-Daten

### 6.2 Organisatorische Herausforderungen

**Akzeptanz bei Verwaltungsmitarbeitenden**

Wie in der Literatur beschrieben (Wielgosch & Dieke 2024), ist mangelnde Akzeptanz ein Haupthindernis für KI-Adoption.

*Lösungsansatz für Rüsselsheim*:
- Pilotphase mit Freiwilligen aus IT-Abteilung
- Klare Kommunikation: "Chatbot ERSETZT nicht, sondern UNTERSTÜTZT"
- Demonstrierbarer Nutzen: 20% Reduktion von Routine-Anfragen (Vorbild: Bad Oeynhausen)
- Feedback-Loop: Mitarbeitende können Antwortqualität bewerten

**Rechtliche Unsicherheiten (KI-Verordnung)**

Die EU AI Act tritt schrittweise in Kraft:
- Februar 2025: Verbot inakzeptabler KI-Systeme
- August 2025: Bestimmungen zu General Purpose AI (LLMs)
- August 2026: Vollständige Umsetzung

*Vorbereitung*:
- Risikoklassifizierung: Chatbot ist "Limited Risk" (Transparenzpflichten)
- Dokumentation: Alle Entscheidungen und Datenflüsse dokumentiert
- Datenschutz-Folgenabschätzung (DSFA) durchgeführt

### 6.3 Vergleich mit kommerziellen Lösungen

| Kriterium | Rüsselsheim (Eigenentwicklung) | Bonn.digital (neuraflow) |
|-----------|-------------------------------|--------------------------|
| **Kosten** | Entwicklungsaufwand hoch, danach nur Hosting (~50€/Monat) | Laufende Lizenzgebühren (geschätzt 500-2000€/Monat) |
| **Datensouveränität** | 100% (lokales Deployment möglich) | Hoch (EU-Server, aber SaaS) |
| **Anpassbarkeit** | Unbegrenzt (Open Source) | Begrenzt auf Features des Anbieters |
| **Support** | Community + eigene IT | Professioneller Support vom Anbieter |
| **Time-to-Market** | Länger (Eigenentwicklung) | Schnell (schlüsselfertige Lösung) |
| **Skalierbarkeit** | Selbst zu managen | Vom Anbieter bereitgestellt |

**Fazit**: Eigenentwicklung lohnt sich für Kommunen mit:
- Eigener IT-Kompetenz
- Langfristigem Horizont (>3 Jahre)
- Bedarf an spezifischen Features (9 API-Integrationen)
- Priorität auf Datensouveränität

Kleinere Kommunen profitieren eher von schlüsselfertigen Lösungen.

### 6.4 Lessons Learned

**Was gut funktioniert hat**:
1. **Modulares Design**: Einfaches Hinzufügen neuer API-Services
2. **Multi-LLM-Strategie**: Flexibilität bei Kosten vs. Qualität
3. **RAG mit pgvector**: Performant und einfach zu warten
4. **Docker-Deployment**: Reproduzierbar und portabel

**Was herausfordernd war**:
1. **Dependency Hell**: 7 Commits nur für Gemini-Kompatibilität
2. **LLM-Prompt-Engineering**: Halluzinationen vollständig zu vermeiden ist schwer
3. **Intent Detection**: Keyword-basiert ist limitiert, ML-basierte Lösung wäre besser

**Verbesserungspotenzial**:
1. **Testing**: Automatisierte Tests für RAG-Qualität fehlen noch
2. **Monitoring**: Logging und Alerting für Produktionsbetrieb
3. **UI/UX**: Aktuell nur API, Frontend-Widget fehlt
4. **Multi-Tenancy**: System für mehrere Kommunen parallel nutzbar machen

---

## 7. Zusammenfassung und Ausblick

### 7.1 Beantwortung der Forschungsfrage

Die Arbeit untersuchte, wie ein datenschutzkonformer, multi-modaler KI-Chatbot für kommunale Bürgerservices konzipiert und implementiert werden kann.

**Kernerkenntnisse**:

1. **Technische Machbarkeit**: Ein vollständig selbst entwickelter Chatbot mit RAG-System, Multi-LLM-Support und 9 API-Integrationen ist in wenigen Tagen realisierbar.

2. **Datenschutz-Konformität**: Durch lokales Deployment (Ollama), RAG in eigener Datenbank (pgvector) und EU-Server-Option ist DSGVO-Konformität erreichbar.

3. **Kosteneffizienz**: Im Vergleich zu kommerziellen Lösungen (500-2000€/Monat) sind die Betriebskosten einer Eigenentwicklung minimal (~50€/Monat Hosting).

4. **Qualität**: Die Kombination aus RAG, Intent Detection und API-Integration liefert präzisere Antworten als reine LLM-Chatbots.

**Herausforderungen**:

1. **Halluzinationen**: Auch mit RAG produzieren LLMs gelegentlich falsche Informationen. Kleinere Modelle (Llama 3.1 8B) sind anfälliger als Premium-Modelle (Claude, GPT-4).

2. **Entwicklungsaufwand**: Die Eigenentwicklung erfordert signifikante Entwicklerressourcen. Kleinere Kommunen sollten schlüsselfertige Lösungen bevorzugen.

3. **Wartung**: Updates von Dependencies (LLM-APIs, Embedding-Modelle) müssen kontinuierlich eingepflegt werden.

### 7.2 Übertragbarkeit auf andere Kommunen

Das Projekt demonstriert einen Blaupause-Charakter für andere Kommunen:

**Übertragbare Komponenten**:
- RAG-Architektur mit pgvector
- Multi-LLM-Backend (Ollama/Gemini/Claude)
- API-Integration-Pattern (Intent Detection → Service-Aufruf)
- Docker-Deployment-Setup

**Anpassungen für andere Städte**:
1. Stadt-spezifische Dokumente in RAG-Datenbank importieren
2. API-Services anpassen (z.B. andere ÖPNV-Verbünde)
3. Blitzer-Datenbank aktualisieren
4. UI/UX an Corporate Design anpassen

**Open-Source-Potenzial**:
Eine Veröffentlichung als Open-Source-Projekt würde den Nutzen für die Verwaltungsgemeinschaft maximieren. Kommunen könnten:
- Code forken und anpassen
- Verbesserungen zurückgeben (Contributionen)
- Gemeinsam Maintenance-Kosten teilen

### 7.3 Zukunftsperspektiven

**Kurzfristig (3-6 Monate)**:
1. **Frontend-Entwicklung**: Web-Widget für bonn.de-Integration
2. **A/B-Testing**: Vergleich Ollama vs. Gemini vs. Claude in Produktion
3. **Monitoring & Analytics**: Welche Anfragen werden am häufigsten gestellt?
4. **Feedback-Loop**: Bürger können Antwortqualität bewerten

**Mittelfristig (6-12 Monate)**:
1. **ML-basierte Intent Detection**: Neuronales Netz statt Keywords
2. **Multimodal**: Sprachein- und -ausgabe (Speech-to-Text/Text-to-Speech)
3. **Formular-Ausfüllung**: Nicht nur Information, sondern Transaktionen
4. **Proaktive Benachrichtigungen**: "Morgen ist Müllabholung"

**Langfristig (1-3 Jahre)**:
1. **Agenten-System**: Chatbot kann selbstständig Termine buchen, Anträge einreichen
2. **Multi-Tenancy**: System für Verbund kleinerer Kommunen (z.B. Rhein-Main-Gebiet)
3. **Föderiertes Learning**: Verbesserungen aus einer Kommune fließen in andere ein
4. **EU-weite Integration**: Grenzüberschreitende Anfragen (z.B. Straßburg-Kehl)

### 7.4 Handlungsempfehlungen

**Für Kommunen, die LLM-Chatbots einführen möchten**:

1. **Strategie-Entscheidung treffen**:
   - Eigenentwicklung: Wenn IT-Kompetenz vorhanden und langfristige Kontrolle gewünscht
   - Schlüsselfertig: Wenn schneller Einsatz prioritär ist

2. **Mit Pilotprojekt starten**:
   - Begrenzter Scope (z.B. nur Bürgeramt-Anfragen)
   - Messbare KPIs definieren (Anfragen-Reduktion, Zufriedenheit)

3. **Datenschutz von Anfang an**:
   - DSFA durchführen
   - Datenschutzbeauftragten einbinden
   - Bei Cloud-LLMs: EU-Server-Option wählen

4. **Change Management**:
   - Mitarbeitende frühzeitig einbinden
   - Schulungen anbieten
   - Erfolge kommunizieren

5. **Iterativ verbessern**:
   - Kontinuierliches Monitoring der Antwortqualität
   - Feedback-Mechanismen etablieren
   - Regelmäßige Updates der Wissensbasis

**Für die Forschung**:

1. **Evaluations-Frameworks**: Standardisierte Metriken für LLM-Chatbot-Qualität in der Verwaltung
2. **Rechtliche Leitlinien**: Klarheit zur KI-Verordnung für kommunale Anwendungen
3. **Longitudinal-Studien**: Langzeit-Impact auf Verwaltungseffizienz
4. **Vergleichsstudien**: Eigenentwicklung vs. kommerzielle Lösungen (TCO, Zufriedenheit)

### 7.5 Schlusswort

Das Projekt "Chatbot Rüsselsheim" demonstriert, dass moderne LLM-Technologie erfolgreich in kommunale Verwaltungen integriert werden kann – unter der Voraussetzung, dass Datenschutz, Transparenz und Bürgerzentrierung im Fokus stehen.

Die Kombination aus RAG-System, Multi-LLM-Unterstützung und umfangreichen API-Integrationen setzt neue Maßstäbe für die Funktionalität kommunaler Chatbots. Gleichzeitig zeigt das Projekt, dass Eigenentwicklungen eine valide Alternative zu kommerziellen Lösungen darstellen – insbesondere für Kommunen, die Datensouveränität und langfristige Kontrolle priorisieren.

Die digitale Transformation der Verwaltung ist kein Sprint, sondern ein Marathon. LLM-Chatbots wie der hier vorgestellte sind ein wichtiger Baustein, um Verwaltungsleistungen effizienter, zugänglicher und bürgerfreundlicher zu gestalten.

---

## Literaturverzeichnis

Bertelsmann Stiftung (2022): *Was Deutschland über Algorithmen denkt*. Gütersloh.

Bundesstadt Bonn (2025): *Pressemitteilung: Neuer KI-Chatbot neurabot*.

Dam, H. K. et al. (2024): *Large Language Models for Software Engineering: A Systematic Literature Review*. In: ACM Computing Surveys.

Databricks RAG (2025): *The Big Book of RAG*. Technical Documentation.

DSK RAG (2025): *Datenschutzkonferenz: Positionspapier zu RAG-Systemen*.

Evanto, J. (2025): *Introduction to Large Language Models*. Manning Publications.

McKinsey (2023): *The Economic Potential of Generative AI*.

neuraflow (2025): *Chatbot neurabot für Bonn.digital*. Technische Dokumentation.

ÖFIT (2021): *KI in der öffentlichen Verwaltung*. Kompetenzzentrum Öffentliche IT.

Themenmonitor KI (2024/2025): *Akzeptanz von KI in Deutschland*. Bertelsmann Stiftung.

Wielgosch, J. & Dieke, A. (2024): *Künstliche Intelligenz in Kommunen*. WIK-Kurzstudie.

---

**Umfang**: ca. 10 Seiten (3.800 Wörter)

**Anhang**: Code-Beispiele und Architektur-Diagramme verfügbar im GitHub-Repository: [Link zum Projekt]
