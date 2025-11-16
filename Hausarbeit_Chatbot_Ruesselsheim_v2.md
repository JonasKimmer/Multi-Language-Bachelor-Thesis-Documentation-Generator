# Implementierung eines KI-gestützten Chatbots für die kommunale Verwaltung: Fallstudie Chatbot Rüsselsheim

**Hausarbeit**

Vorgelegt von: Jonas Kimmer
Hochschule: TH Köln
Jahr: 2025

---

## 1. Einleitung

### 1.1 Digitale Transformation und Herausforderungen der Verwaltung

Die deutsche Kommunalverwaltung steht unter erheblichem Druck zur digitalen Transformation. Zu den drängendsten Herausforderungen zählt die angespannte Finanzlage vieler Kommunen, die teilweise Haushaltskonsolidierungen erforderlich macht. Ein weiteres zentrales Problem ist der drohende Fachkräftemangel: Bis 2032 geht etwa ein Viertel der im öffentlichen Dienst Beschäftigten in den Ruhestand. Diese Personallücke lässt sich nicht durch Neueinstellungen schließen (Wielgosch & Dieke 2024, S. 28-29).

KI-Anwendungen bieten große Potenziale, um Aufgaben effizienter zu erfüllen, Prozesse kostengünstiger durchzuführen und Mitarbeitende zu entlasten. Bereits 66 Prozent der Kommunen halten den Einsatz von KI für sinnvoll. Trotz dieser hohen Akzeptanz nutzten 2023 lediglich acht Prozent der Kommunen KI in ihrer Verwaltung. Die Kluft zwischen Potenzial und Umsetzung liegt in begrenzten Ressourcen, fehlender Akzeptanz, rechtlichen Unsicherheiten sowie offenen Fragen zum Datenschutz (Wielgosch & Dieke 2024, S. 30-32).

### 1.2 Large Language Models als technologischer Wendepunkt

Im Herbst 2022 veränderte OpenAI mit ChatGPT die Technologielandschaft grundlegend. Large Language Models (LLMs) sind große, vortrainierte neuronale Netze, die auf die Verarbeitung und Generierung natürlicher Sprache spezialisiert sind. Das Aufkommen dieser Modelle ermöglichte eine neue Generation von KI-Anwendungen mit deutlich höherem Potenzial. In der Verwaltung liegen die Anwendungsschwerpunkte auf Bürgerservices und interner Verwaltung (Wielgosch & Dieke 2024, S. 6, 77; Evanto 2025, S. 236).

### 1.3 Forschungsfrage

Diese Arbeit untersucht die zentrale Frage: **Welche konzeptionellen und technischen Entscheidungen ermöglichen die datenschutzkonforme Implementierung eines multi-modalen KI-Chatbots für kommunale Bürgerservices, und welche Rolle spielt dabei die Wahl zwischen Eigenentwicklung und kommerzieller Lösung?**

Als Fallstudienobjekt dient die Eigenentwicklung eines Chatbot-Systems für die Stadt Rüsselsheim, das sich durch Multi-LLM-Unterstützung, umfangreiche API-Integrationen und ein Retrieval Augmented Generation (RAG) System auszeichnet.

### 1.4 Aufbau der Arbeit

Die Arbeit gliedert sich in sechs Kapitel. Kapitel 2 diskutiert die strategische Motivation für Eigenentwicklungen. Kapitel 3 erläutert die theoretischen Grundlagen. Kapitel 4 analysiert die Fallstudie konzeptionell. Kapitel 5 diskutiert zentrale Herausforderungen. Kapitel 6 fasst die Erkenntnisse zusammen.

---

## 2. Strategische Überlegungen: Eigenentwicklung vs. kommerzielle Lösung

### 2.1 Das Dilemma kommunaler KI-Beschaffung

Kommunen stehen bei der Einführung von KI-Chatbots vor einer grundlegenden strategischen Entscheidung: Sollen sie auf schlüsselfertige Lösungen externer Dienstleister setzen oder eigene Systeme entwickeln? Diese Entscheidung hat weitreichende Implikationen für Datensouveränität, Kosten und technologische Abhängigkeit.

Die WIK-Studie zeigt, dass mindestens 82 der 143 identifizierten KI-Anwendungen in deutschen Kommunen mit öffentlichen Fördermitteln finanziert werden und viele als schlüsselfertige Lösungen von Start-ups implementiert sind. Dies ermöglicht einen niedrigschwelligen Einstieg auch für weniger digitalisierte Kommunen (Wielgosch & Dieke 2024, S. 54, 94-95).

### 2.2 Argumente für die Eigenentwicklung

Die Entscheidung für eine Eigenentwicklung im Fall Rüsselsheim basiert auf vier strategischen Säulen:

**Datensouveränität**: In der öffentlichen Verwaltung ist die Kontrolle über Bürgerdaten von besonderer Bedeutung. Während kommerzielle SaaS-Lösungen typischerweise Cloud-basiert operieren, ermöglicht eine Eigenentwicklung die vollständige on-premise-Deployment. Dies adressiert die in der Literatur identifizierte Hauptsorge kommunaler Datenschutzbeauftragter bezüglich der Übertragung personenbezogener Daten an Drittanbieter (DSK RAG 2025, S. 486).

**Vendor Lock-in Vermeidung**: Die Multi-Backend-Strategie des Rüsselsheimer Systems illustriert einen Ansatz zur Vermeidung technologischer Abhängigkeit. Während kommerzielle Lösungen typischerweise an einen LLM-Anbieter gebunden sind, erlaubt die flexible Architektur den Wechsel zwischen verschiedenen Modellen je nach Kosten-Nutzen-Verhältnis und Verfügbarkeit.

**Langfristige Kostenbetrachtung**: Obwohl Eigenentwicklungen höhere initiale Entwicklungskosten verursachen, entfallen laufende Lizenzgebühren. Bei geschätzten monatlichen Kosten kommerzieller Lösungen von 500-2.000€ amortisiert sich die Eigenentwicklung mittelfristig, insbesondere bei lokalem Betrieb mit Open-Source-Modellen.

**Anpassungsfähigkeit**: Die spezifischen Anforderungen einer Kommune – etwa die Integration lokaler Datenquellen wie Müllabfuhrkalender oder ÖPNV-Verbindungen – erfordern oft maßgeschneiderte Lösungen, die kommerzielle Anbieter nicht standardmäßig abdecken.

### 2.3 Grenzen der Eigenentwicklung

Trotz dieser Vorteile sind Eigenentwicklungen nicht für alle Kommunen geeignet. Sie setzen voraus:

1. **Technische Kompetenz**: Eigene IT-Abteilungen mit Expertise in modernen Technologien (FastAPI, LLMs, Vektordatenbanken)
2. **Personelle Ressourcen**: Entwicklung und Wartung binden signifikante Kapazitäten
3. **Langfristige Perspektive**: ROI realisiert sich erst nach mehreren Jahren
4. **Bereitschaft zu Risiko**: Eigenentwicklungen tragen technische und organisatorische Risiken

Kleinere Kommunen ohne entsprechende IT-Infrastruktur profitieren weiterhin von schlüsselfertigen Lösungen, die professionellen Support und garantierte Verfügbarkeit bieten.

---

## 3. Theoretische Grundlagen

### 3.1 Large Language Models: Von regelbasierten Systemen zur generativen KI

Die Evolution der Conversational AI lässt sich in drei Phasen gliedern. Frühe Systeme wie ELIZA (1966) basierten auf regelbasierten Ansätzen mit fest vorgegebenen Antwortmustern. Sie stießen schnell an Grenzen, sobald Nutzereingaben von hinterlegten Regeln abwichen (Evanto 2025, S. 217; Dam et al. 2024, S. 362).

Die zweite Generation nutzte Machine Learning für Intent Recognition und Slot Filling, blieb aber auf vordefinierte Antwortdomänen beschränkt. Der Durchbruch erfolgte mit Transformer-basierten Large Language Models, die auf umfangreichen Textkorpora vortrainiert werden und natürliche Sprache generieren, ohne auf feste Antwortmuster angewiesen zu sein (Dam et al. 2024, S. 365).

### 3.2 Retrieval Augmented Generation: Bridging the Knowledge Gap

Ein zentrales Problem von LLMs ist ihre "Halluzinations"-Neigung – die Generierung zuversichtlicher, aber faktisch falscher Antworten. Dies rührt daher, dass LLMs Text durch Wahrscheinlichkeitsberechnungen für das jeweils nächste Wort erzeugen, nicht auf Basis eines geprüften Wissensspeichers (Dam et al. 2024, S. 347; Evanto 2025, S. 231).

Retrieval Augmented Generation (RAG) adressiert dieses Problem durch einen hybriden Ansatz: Anstatt sich ausschließlich auf das statische Trainingswissen zu verlassen, ruft das System zur Laufzeit relevante Dokumente aus einer Wissensbasis ab und integriert diese als Kontext in die Generierung. Dies verbessert nicht nur die Faktentreue, sondern ermöglicht auch die Aktualität der Informationen (Databricks RAG, S. 304, 306).

Der RAG-Prozess gliedert sich in zwei Phasen:

**Indexierungsphase**: Dokumente werden in semantisch kohärente Textabschnitte (Chunks) segmentiert und durch Embedding-Modelle in hochdimensionale Vektorrepräsentationen überführt. Diese werden in einer Vektordatenbank gespeichert, die effiziente Ähnlichkeitssuchen ermöglicht.

**Abrufphase**: Die Nutzeranfrage wird ebenfalls in einen Vektor transformiert. Durch Cosine-Similarity-Suche werden die relevantesten Dokument-Chunks identifiziert, dem LLM als erweiterter Kontext bereitgestellt und die Antwort generiert.

### 3.3 RAG vs. Fine-Tuning: Ein technologischer Vergleich

Die Anpassung von LLMs an domänenspezifisches Wissen kann prinzipiell durch zwei Ansätze erfolgen: RAG oder Fine-Tuning. Beide Methoden verfolgen unterschiedliche Philosophien mit jeweils spezifischen Vor- und Nachteilen.

**Fine-Tuning** modifiziert die internen Gewichtungen des neuronalen Netzes durch weiteres Training auf domänenspezifischen Daten. Dies verändert das "gelernte Wissen" des Modells permanent und ist besonders geeignet, wenn das Modell eine neue "Sprache" oder einen spezifischen Stil erlernen soll (Databricks RAG, S. 319-320).

**RAG** hingegen belässt das Modell unverändert und beeinflusst lediglich den Eingabeprompt durch externe Kontextinformationen. Für kommunale Anwendungen bietet RAG entscheidende Vorteile:

1. **Effizienz**: Kein kostenintensives Retraining notwendig, sofortige Einsatzfähigkeit
2. **Aktualität**: Die Wissensbasis kann kontinuierlich aktualisiert werden ohne Modell-Neutraining
3. **DSGVO-Konformität**: Daten verbleiben in kontrollierbarer Datenbank, einfache Umsetzung von Betroffenenrechten (Auskunft, Löschung, Berichtigung)
4. **Modell-Agnostik**: Beliebige LLMs können genutzt werden, Wechsel ohne Datenverlust möglich

Die Datenschutzkonferenz hebt hervor, dass RAG im Gegensatz zu trainierten Modellen die Daten in der Vektordatenbank einfach aktualisieren, löschen und beauskunften kann, was für die Einhaltung der DSGVO von zentraler Bedeutung ist (DSK RAG 2025, S. 502-503).

### 3.4 Multi-LLM-Strategien: Technologische Diversifizierung

Die Landschaft der LLM-Anbieter ist durch Oligopol-Strukturen geprägt. Wenige Unternehmen (OpenAI, Google, Anthropic, Meta) dominieren den Markt, was Abhängigkeitsrisiken schafft. Für öffentliche Institutionen ist dies besonders problematisch, da Verfügbarkeit, Preisgestaltung und Datenschutzpraktiken nicht vollständig kontrollierbar sind.

Eine Multi-Backend-Strategie adressiert diese Risiken durch technologische Diversifizierung. Das Rüsselsheimer System implementiert drei parallele LLM-Backends:

**Lokale Open-Source-Modelle (Ollama/Llama)**: Maximale Datensouveränität durch vollständig on-premise Betrieb, keine laufenden API-Kosten, aber höhere Hardwareanforderungen und eingeschränkte Modellqualität bei kleineren Modellen.

**Cloud-basierte Commercial Models (Gemini, Claude)**: Höhere Antwortqualität, insbesondere bei komplexen Reasoning-Aufgaben, aber Abhängigkeit von Drittanbietern und laufende Kosten.

Die Architektur ermöglicht situationsabhängige Backend-Selektion: Routine-Anfragen können kosteneffizient lokal verarbeitet werden, während kritische Anfragen bei Bedarf premium-Modelle nutzen.

---

## 4. Fallstudie Chatbot Rüsselsheim: Konzeptionelle Analyse

### 4.1 Architektur-Paradigma: Layered Architecture und Separation of Concerns

Die Systemarchitektur folgt dem etablierten Layered-Architecture-Pattern mit drei klar definierten Schichten:

**Presentation Layer (API-Ebene)**: REST-Endpunkte für Chat-Interaktion und API-Integrationen. Diese Schicht ist verantwortlich für Request-Validierung und Response-Formatierung.

**Business Logic Layer (Service-Ebene)**: Enthält die Kernlogik des Systems, insbesondere Chat-Services für verschiedene LLM-Backends, RAG-Service für Dokumenten-Retrieval und API-Helper für Intent Detection.

**Data Access Layer (Model/DB-Ebene)**: Abstraktion des Datenbankzugriffs durch ORM-Models (SQLAlchemy) und direkte Vektor-Queries an pgvector.

Diese Trennung folgt dem Prinzip der Separation of Concerns und ermöglicht unabhängige Testbarkeit, einfachere Wartung und flexible Erweiterbarkeit. Änderungen an der Datenbankstruktur beeinflussen nicht die API-Schicht, neue LLM-Backends können ohne Modifikation der Endpunkte hinzugefügt werden.

### 4.2 Design Patterns: Strategische Anwendung etablierter Muster

Das System implementiert mehrere klassische Software-Design-Patterns:

**Strategy Pattern** für LLM-Backend-Selektion: Verschiedene Chat-Service-Implementierungen (OllamaService, GeminiService) erfüllen dasselbe Interface. Dies ermöglicht Laufzeit-Austauschbarkeit ohne Code-Änderungen – ein zentraler Vorteil für die Multi-Backend-Strategie.

**Dependency Injection** für Database Sessions: Services erhalten ihre Abhängigkeiten (insbesondere Datenbank-Sessions) als Konstruktor-Parameter, nicht durch globale Variablen. Dies erleichtert Unit-Testing durch Mock-Injection.

**Repository Pattern** durch ORM-Abstraktion: Datenbankzugriffe sind durch SQLAlchemy-Models gekapselt, was Portabilität zwischen verschiedenen Datenbanksystemen gewährleistet.

Die konsequente Anwendung dieser Patterns reflektiert Best Practices moderner Software-Engineering und differenziert das Projekt von prototypischen Lösungen.

### 4.3 API-First-Ansatz: Von statischer Information zu dynamischen Diensten

Ein Alleinstellungsmerkmal des Rüsselsheimer Systems ist die umfangreiche Integration externer Datenquellen. Während viele kommunale Chatbots sich auf die Wiedergabe statischer Verwaltungsinformationen beschränken, integriert dieses System neun verschiedene APIs für Echtzeitdaten:

- **Öffentliche Verkehrsinfrastruktur**: Wetterdaten (Open-Meteo), Kartendienste (Nominatim/OSM), ÖPNV-Verbindungen (RMV)
- **Lokale Services**: Müllabfuhrkalender, Tankstellenpreise, Geschwindigkeitskontrollen
- **Verwaltungsinformationen**: Feiertage, lokale Nachrichten

Diese Multimodalität erfordert ein differenziertes Intent-Detection-System, das aus natürlichsprachlichen Anfragen die relevanten Informationsquellen identifiziert. Aktuell erfolgt dies durch Keyword-Matching – ein pragmatischer, aber limitierter Ansatz. Fortgeschrittenere Implementierungen könnten Machine-Learning-basierte Intent-Classifier nutzen.

### 4.4 Datenschutz-Architektur: DSGVO by Design

Das System implementiert Privacy by Design durch mehrere technische und organisatorische Maßnahmen:

**Lokale Deployment-Option**: Durch On-Premise-Betrieb mit Ollama verbleiben alle Daten innerhalb der kommunalen Infrastruktur. Dies eliminiert Risiken der Datenübertragung an Drittanbieter.

**RAG-basierte Datenhaltung**: Im Gegensatz zu Fine-Tuning, bei dem domänenspezifische Daten in das Modell integriert werden, verbleiben bei RAG alle Dokumente in einer kontrollierbaren PostgreSQL-Datenbank. Dies vereinfacht die Umsetzung von Betroffenenrechten gemäß Art. 15-22 DSGVO:
- Auskunft: SQL-Query auf die Documents-Tabelle
- Löschung: DELETE-Operation
- Berichtigung: UPDATE-Operation

**Session-basierte Anonymisierung**: Chatbot-Sessions müssen keine personenbezogenen Identifier enthalten. User-Tracking erfolgt nur über temporäre Session-IDs.

**Verschlüsselte Kommunikation**: Datenübertragung erfolgt ausschließlich über HTTPS/TLS.

---

## 5. Kritische Diskussion: Herausforderungen und offene Fragen

### 5.1 Das Persistente Problem der Halluzinationen

Trotz RAG-Integration bleibt die Halluzinations-Neigung von LLMs eine zentrale Herausforderung. Studien zeigen, dass selbst state-of-the-art Modelle bei komplexen Reasoning-Aufgaben signifikant an Genauigkeit verlieren (Dam et al. 2024, S. 345-346).

Im Kontext kommunaler Chatbots ist dies besonders problematisch, da fehlerhafte Auskünfte zu rechtlichen Konsequenzen führen können. Beispielsweise könnte eine falsche Aussage über Antragsfristen oder erforderliche Dokumente Bürger:innen benachteiligen.

Die Literatur identifiziert mehrere Mitigation-Strategien:
1. **Confidence Scoring**: LLMs sollten Unsicherheit explizit kommunizieren
2. **Human-in-the-Loop**: Kritische Anfragen werden an menschliche Sachbearbeiter eskaliert
3. **Fact-Checking**: Generated Outputs werden gegen strukturierte Datenbanken validiert
4. **Transparenz**: Quellenangaben zu verwendeten Dokumenten

Dennoch bleibt festzuhalten: Vollständige Eliminierung von Halluzinationen ist mit aktueller Technologie nicht möglich. Dies limitiert den Einsatzbereich auf informative, nicht-transaktionale Aufgaben.

### 5.2 Technologische Abhängigkeiten trotz Multi-Backend-Strategie

Während die Multi-Backend-Strategie Abhängigkeiten von einzelnen LLM-Anbietern reduziert, bestehen Abhängigkeiten auf anderen Ebenen fort:

**Embedding-Models**: Das RAG-System benötigt Embedding-Modelle zur Vektorisierung von Dokumenten und Anfragen. Wechsel des Embedding-Modells erfordert Re-Indexierung aller Dokumente.

**Vektor-Datenbank**: pgvector als PostgreSQL-Erweiterung ist eine spezifische Technologie-Entscheidung. Migration zu alternativen Vektor-DBs (Pinecone, Weaviate) würde signifikanten Aufwand erfordern.

**API-Abhängigkeiten**: Die neun integrierten APIs können jederzeit ihre Schnittstellen ändern, kostenpflichtig werden oder eingestellt werden. Dies erfordert kontinuierliche Wartung.

### 5.3 Akzeptanz und Change Management

Die technische Implementierung ist nur ein Aspekt erfolgreicher KI-Einführung. Wie die WIK-Studie betont, ist fehlende Akzeptanz bei Verwaltungsmitarbeitenden ein Haupthindernis (Wielgosch & Dieke 2024, S. 31, 76).

Kritische Erfolgsfaktoren umfassen:
- **Demonstrierbarer Nutzen**: Mitarbeitende müssen konkrete Arbeitserleichterung erfahren
- **Klare Kommunikation**: KI ersetzt nicht, sondern unterstützt
- **Transparenz über Limitationen**: Offene Diskussion von Fehlerquoten und Grenzen
- **Partizipation**: Einbindung in Entwicklungsprozess, Feedback-Mechanismen

Ohne erfolgreiche organisatorische Einbettung bleibt selbst technisch ausgereiftes System ungenutzt.

### 5.4 Rechtliche Unsicherheiten: Die KI-Verordnung

Die EU AI Act tritt schrittweise in Kraft und schafft erstmals verbindliche Regelungen für KI-Systeme. Kommunale Chatbots fallen typischerweise in die Kategorie "Limited Risk" mit Transparenzpflichten (Wielgosch & Dieke 2024, S. 40).

Offene Fragen umfassen:
- **Konkrete Compliance-Anforderungen**: Welche Dokumentationen sind erforderlich?
- **Haftung bei Fehlinformationen**: Wer haftet bei Schäden durch falsche Chatbot-Auskünfte?
- **Biometrie und Profiling**: Grenzen personalisierter Chatbot-Interaktionen

Die fehlenden zentralen Leitlinien für kommunale KI-Nutzung, die von Kommunen gewünscht werden, erschweren rechtssichere Implementierung (Wielgosch & Dieke 2024, S. 44).

### 5.5 Evaluierung und Qualitätssicherung

Ein fundamentales Problem der kommunalen KI-Praxis ist der Mangel an systematischer Evaluierung. Die WIK-Studie konstatiert: "Es fehlt an gesicherten Erkenntnissen über den tatsächlichen Mehrwert von KI-Anwendungen aus der kommunalen Praxis" (Wielgosch & Dieke 2024, S. 12).

Für RAG-Systeme sind herkömmliche KI-Bewertungsmodelle nicht ausreichend. Erforderlich sind hybride Metriken, die menschliches Urteilsvermögen, Relevanzbewertung und Grounding-Checks kombinieren (Databricks RAG, S. 288; Dam et al. 2024, S. 339-340).

Konkret fehlen standardisierte Benchmarks für:
- Antwortgenauigkeit bei verwaltungsspezifischen Anfragen
- Nutzer-Zufriedenheit über längere Nutzungszeiträume
- Entlastungseffekte für Verwaltungsmitarbeitende (quantifiziert)
- Total Cost of Ownership über Systemlebenszyklus

---

## 6. Zusammenfassung und Ausblick

### 6.1 Beantwortung der Forschungsfrage

Die Arbeit untersuchte, welche konzeptionellen und technischen Entscheidungen die datenschutzkonforme Implementierung eines multi-modalen KI-Chatbots ermöglichen.

**Zentrale Erkenntnisse**:

**1. Eigenentwicklung vs. kommerzielle Lösung**: Die strategische Wahl hängt von Ressourcenverfügbarkeit, langfristiger Perspektive und Datensouveränitäts-Anforderungen ab. Eigenentwicklungen eignen sich für Kommunen mit eigener IT-Expertise und langfristigem Horizont, während kleinere Kommunen von schlüsselfertigen Lösungen profitieren.

**2. RAG als Schlüsseltechnologie**: Retrieval Augmented Generation erweist sich als superior gegenüber Fine-Tuning für kommunale Anwendungsfälle aufgrund von Effizienz, Datenschutz-Compliance und Aktualität.

**3. Multi-Backend-Strategie**: Die Diversifizierung über mehrere LLM-Anbieter reduziert Vendor Lock-in und ermöglicht Kosten-Flexibilität, schafft aber eigene Komplexität in Wartung und Betrieb.

**4. API-Integration**: Multimodale Informationsbereitstellung differenziert fortgeschrittene Systeme von reinen FAQ-Chatbots, erfordert aber robuste Intent-Detection.

**Limitationen**:

**Halluzinationen**: Trotz technischer Mitigationsstrategien bleibt das fundamentale Problem der LLM-Halluzinationen bestehen. Dies begrenzt Einsatzszenarien auf informative, nicht-transaktionale Aufgaben.

**Entwicklungsaufwand**: Eigenentwicklungen erfordern signifikante technische Expertise und personelle Ressourcen, die nicht alle Kommunen vorhalten.

**Evaluierungslücke**: Der Mangel an standardisierten Qualitätsmetriken erschwert objektive Vergleiche zwischen Lösungsansätzen.

### 6.2 Übertragbarkeit und Skalierung

Das Rüsselsheimer Projekt demonstriert einen Blueprint-Charakter für andere Kommunen. Übertragbare Komponenten umfassen die RAG-Architektur mit pgvector, das Multi-LLM-Backend-Design und das API-Integrations-Pattern.

Eine Veröffentlichung als Open-Source-Projekt würde den Nutzen maximieren: Kommunen könnten den Code adaptieren, Verbesserungen zurückgeben und gemeinsam Wartungskosten teilen. Dies entspräche dem Geist der Open Government Data-Bewegung.

Skalierung auf kommunale Verbünde (z.B. Rhein-Main-Gebiet) würde durch Multi-Tenancy-Erweiterungen ermöglicht, bei denen eine zentrale Instanz mehrere Kommunen bedient. Dies würde Effizienzgewinne durch geteilte Infrastruktur ermöglichen.

### 6.3 Ausblick: Von reaktiven Chatbots zu proaktiven Agenten

Die Zukunft kommunaler KI-Systeme liegt in der Weiterentwicklung von rein reaktiven Chatbots zu proaktiven Agenten-Systemen. Während aktuelle Systeme auf Nutzeranfragen reagieren, könnten zukünftige Generationen:

**Transaktionale Aufgaben übernehmen**: Terminbuchungen, Antragseinreichungen, Dokumenten-Uploads direkt aus dem Chat heraus.

**Proaktive Benachrichtigungen**: "Morgen ist Müllabholung", "Ihr Antrag ist bearbeitungsreif", "Neue Förderprogramme verfügbar".

**Multimodal interagieren**: Speech-to-Text und Text-to-Speech für barrierefreie Sprachinteraktion, Bildverarbeitung für Dokumenten-Upload und -Analyse.

**Föderiert lernen**: Verbesserungen aus einer Kommune fließen datenschutzkonform in andere ein, ohne rohe Daten zu teilen.

Technologisch zeichnen sich Trends zu größeren Kontextfenstern ab (GPT-4 Turbo: 128k Tokens, Gemini 2.5: 1M Tokens), die komplexere Multi-Turn-Dialoge ermöglichen. RAG entwickelt sich von einer isolierten Technik zu integralen Komponenten hybrider Systeme, kombiniert mit strukturierten Datenbanken und Funktionsaufruf-Agenten (Databricks RAG, S. 309-310).

### 6.4 Handlungsempfehlungen

**Für Kommunen**:
1. Strategieentscheidung basierend auf Ressourcen, Zeithorizont und Datensouveränitäts-Anforderungen
2. Pilotprojekte mit begrenztem Scope und messbaren KPIs
3. Frühzeitige Einbindung von Datenschutzbeauftragten (DSFA)
4. Investition in Change Management und Mitarbeiter-Schulungen
5. Kontinuierliches Monitoring und iterative Verbesserung

**Für die Forschung**:
1. Entwicklung standardisierter Evaluations-Frameworks für kommunale LLM-Chatbots
2. Longitudinal-Studien zu langfristigem Impact auf Verwaltungseffizienz
3. Vergleichsstudien Eigenentwicklung vs. kommerzielle Lösungen (TCO, Qualität, Zufriedenheit)
4. Rechtliche Leitlinien zur praktischen Umsetzung der KI-Verordnung

**Für Regulatoren**:
1. Zentral bereitgestellte Leitlinien für sichere KI-Nutzung in Kommunen
2. Klarheit zu Haftungsfragen bei KI-Fehlinformationen
3. Förderung kommunaler Kooperation durch Open-Source-Initiativen

### 6.5 Schlusswort

Die digitale Transformation der Verwaltung ist kein Sprint, sondern ein Marathon. LLM-basierte Chatbots stellen einen wichtigen Baustein dar, um Verwaltungsleistungen effizienter, zugänglicher und bürgerfreundlicher zu gestalten. Das Projekt Chatbot Rüsselsheim demonstriert, dass moderne KI-Technologie erfolgreich in kommunale Kontexte integriert werden kann – unter der Voraussetzung, dass Datenschutz, Transparenz und realistische Erwartungen im Fokus stehen.

Die Kombination aus RAG-System, Multi-LLM-Unterstützung und umfangreichen API-Integrationen setzt neue Maßstäbe für kommunale Chatbots. Gleichzeitig zeigen die diskutierten Herausforderungen – Halluzinationen, rechtliche Unsicherheiten, Evaluierungslücken – dass der Weg zur vollständigen KI-Integration in die Verwaltung noch weit ist.

Entscheidend ist, dass Kommunen KI nicht als Selbstzweck betrachten, sondern als Werkzeug zur Bewältigung realer operativer Herausforderungen: Fachkräftemangel, Finanzrestriktionen, steigende Ansprüche der Bürger:innen. Technologie kann diese Probleme nicht allein lösen – aber bei durchdachter, menschenzentrierter Implementierung kann sie einen wertvollen Beitrag leisten.

---

## Literaturverzeichnis

Bertelsmann Stiftung (2022): *Was Deutschland über Algorithmen denkt*. Gütersloh.

Bundesstadt Bonn (2025): *Pressemitteilung: Neuer KI-Chatbot neurabot*.

Dam, H. K. et al. (2024): *Large Language Models for Software Engineering: A Systematic Literature Review*. In: ACM Computing Surveys.

Databricks RAG (2025): *The Big Book of RAG*. Technical Documentation.

DSK RAG (2025): *Datenschutzkonferenz: Positionspapier zu RAG-Systemen*.

Evanto, J. (2025): *Introduction to Large Language Models*. Manning Publications.

McKinsey (2023): *The Economic Potential of Generative AI*.

ÖFIT (2021): *KI in der öffentlichen Verwaltung*. Kompetenzzentrum Öffentliche IT.

Wielgosch, J. & Dieke, A. (2024): *Künstliche Intelligenz in Kommunen*. WIK-Kurzstudie.

---

**Umfang**: 10 Seiten (~4.200 Wörter)
