# E2-Trainer

Trainings- und Organisationsunterlagen für die **E-Jugend, Saison 2026/2027**.

**Planungsstandard:** Dienstag und Donnerstag je 90 Minuten, **14–17 Kinder**, zwei Trainer. Jedes Training enthält die erwartete und tatsächliche Teilnehmerzahl, eine Materialliste für den Tag, konkrete Übungen mit Zeiten und Feldmaßen sowie Varianten für jede Teilnehmerzahl.

## Schnellzugriff

- [Erste Trainingswoche: Ablauf, Material und Skizzen (PDF)](Saison_2026-2027/Trainingswochen/W01_2026-09-14/E-Jugend_Trainingsplan_Woche_1.pdf)
- [Erste Trainingswoche: bearbeitbarer Text](Saison_2026-2027/Trainingswochen/W01_2026-09-14/Wochenplan.md)
- [Trainersprache: Sätze und Ansprachen (PDF)](Saison_2026-2027/Trainersprache/01_Saetze_und_Ansprachen.pdf)
- [Trainersprache: bearbeitbarer Text](Saison_2026-2027/Trainersprache/01_Saetze_und_Ansprachen.md)
- [Viertelplanung für Spieltage](Vorlagen/Spieltag.md)

## Ablage

| Ordner | Inhalt |
|---|---|
| `Saison_2026-2027/Saisonplanung` | Trainingsgrundsätze, Saisonziele, bestätigte Rahmenbedingungen |
| `Saison_2026-2027/Trainingswochen` | Ein Ordner je Trainingswoche mit Ablauf, Material, Varianten und PDF-Skizzen |
| `Saison_2026-2027/Spieltage` | Organisation, Viertelbesetzung, kurze Rückblicke |
| `Saison_2026-2027/Turniere` | Turnierplanung, Ablauf und Nachbereitung |
| `Saison_2026-2027/Hallentraining` | Hallenübungen und angepasste Wochenpläne |
| `Saison_2026-2027/Teamaktivitaeten` | Gemeinsame Ausflüge, Feiern und Aktionen |
| `Saison_2026-2027/Trainersprache` | Einfache deutsche Sätze, Coachinghinweise und Ansprachen |
| `Vorlagen` | Wiederverwendbare Vorlagen für Wochen, Spieltage und Aktivitäten |
| `scripts` | Nachvollziehbare PDF-Erzeugung aus Text und gezeichneten Skizzen |

Ordnernamen enthalten keine Leerzeichen oder Umlaute, die Dokumente verwenden normales Deutsch. Nächste Saison erhält einen eigenen Ordner `Saison_2027-2028`.

## Klarstellungen aus unseren Gesprächen

Jede geklärte Trainingsfrage wird künftig in `Ergaenzungen_und_Klarstellungen.md` im betreffenden Wochenordner festgehalten – mit Übungsname, Trainingstag und PDF-Seite. [Klarstellungen zu W01](Saison_2026-2027/Trainingswochen/W01_2026-09-14/Ergaenzungen_und_Klarstellungen.md). Die dauerhaften Arbeitsregeln stehen in [AGENTS.md](AGENTS.md).

## Benennung und Pflege

- Trainingswoche: `W01_2026-09-14` (fortlaufende Trainingswoche + Montag der Woche; **keine Kalenderwochennummer**).
- Spieltag: `2026-09-18_Attenkirchen`.
- Turnier oder Aktivität: `JJJJ-MM-TT_Kurztitel`.
- Textdateien sind bearbeitbar; PDFs dienen zum Ausdrucken. Bei Änderungen beide Fassungen aktualisieren.
- Unbestätigte Termine und Regeln deutlich als offen markieren. Der aktuelle Spielmodus stammt aus den Angaben des Trainers, nicht aus einer hier geprüften Spielordnung.

## PDFs erzeugen

Python 3 und ReportLab installieren:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/wochenplan_w01.py
python3 scripts/text_pdf.py
```

Der Wochenplan enthält direkt gezeichnete, skalierbare Skizzen. `text_pdf.py` erzeugt den Sprachleitfaden aus seiner Markdown-Datei. Beide Skripte funktionieren unabhängig vom aktuellen Arbeitsverzeichnis. Die PDF-Schriften werden aus dem ReportLab-Paket eingebettet; zusätzliche Schriftinstallationen sind nicht erforderlich.
