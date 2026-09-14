#!/usr/bin/env python3
"""Erzeugt den bebilderten Wochenplan W01 als PDF.
Aufruf aus beliebigem Verzeichnis: python3 scripts/wochenplan_w01.py
Abhängigkeit: reportlab. Maße sind Trainingsvorschläge, keine Spielordnung.
"""
from pdf_fonts import register_fonts
register_fonts()
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
import math
P=str(ROOT / 'Saison_2026-2027/Trainingswochen/W01_2026-09-14/E-Jugend_Trainingsplan_Woche_1.pdf')
c=canvas.Canvas(P,pagesize=(595.28,841.89)); c.setTitle('E-Jugend | Erste Spielwoche | 15.-18. September 2026')
navy=HexColor('#17354A'); blue=HexColor('#2275B8'); red=HexColor('#CB4C4C'); green=HexColor('#EAF3E9'); orange=HexColor('#E79B26'); ink=HexColor('#253744')
style=ParagraphStyle('body',fontName='Coach',fontSize=11,leading=16,textColor=ink)
page=0

def txt(s,x,y,w=505,size=10):
 st=ParagraphStyle('x',parent=style,fontSize=size,leading=size*1.34)
 p=Paragraph(s,st); _,h=p.wrap(w,1000);p.drawOn(c,x,y-h);return y-h-9

def start(k,title,sub):
 global page
 page+=1;c.setFillColor(navy);c.rect(0,735,596,107,fill=1,stroke=0)
 c.setFillColor(HexColor('#B6D9CE'));c.setFont('CoachBold',10);c.drawString(42,805,k.upper())
 c.setFillColor(white);c.setFont('CoachBold',min(23, 23*505/max(505,c.stringWidth(title,'CoachBold',23))));c.drawString(42,771,title)
 c.setFont('Coach',10);c.drawString(42,749,sub)
 c.setFillColor(ink);c.setFont('Coach',9);c.drawString(42,27,'E-Jugend | 14-17 Kinder | 2 Trainer | Erste Spielwoche 2026');c.drawRightString(552,27,str(page))

def end(): c.showPage()
def section(title,body,y):
 y=txt('<b>'+title+'</b>',42,y,size=12);return txt(body,42,y)
def table(rows,y,widths):
 data=[[Paragraph(str(v),ParagraphStyle('t',parent=style,fontSize=9.5,leading=13)) for v in row] for row in rows]
 t=Table(data,colWidths=widths);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#DDEBEF')),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#F3F6F7')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)])); _,h=t.wrap(510,600);t.drawOn(c,42,y-h);return y-h-16

def field(x,y,w,h,dimx,dimy):
 c.setFillColor(green);c.setStrokeColor(HexColor('#719777'));c.setLineWidth(1.2);c.rect(x,y,w,h,fill=1)
 c.setFont('CoachBold',10);c.setFillColor(ink);c.drawCentredString(x+w/2,y+h+12,dimx)
 c.saveState();c.translate(x-14,y+h/2);c.rotate(90);c.drawCentredString(0,0,dimy);c.restoreState()
 return lambda a,b:(x+a*w,y+b*h)
def player(x,y,label='',color=blue,ball=False):
 c.setFillColor(color);c.setStrokeColor(white);c.circle(x,y,9,fill=1,stroke=1);c.setFont('CoachBold',7);c.setFillColor(white);c.drawCentredString(x,y-2.5,label)
 if ball:
  c.setFillColor(ink);c.circle(x+12,y-7,3,fill=1,stroke=0)
def cone(x,y):
 c.setFillColor(orange);c.setStrokeColor(ink);p=c.beginPath();p.moveTo(x,y+5);p.lineTo(x-4,y-4);p.lineTo(x+4,y-4);p.close();c.drawPath(p,fill=1,stroke=1)
def gate(x,y,d=18):cone(x-d/2,y);cone(x+d/2,y)
def arrow(a,b,dashed=False):
 c.setStrokeColor(ink);c.setLineWidth(1.3);c.setDash(4,3) if dashed else c.setDash();c.line(*a,*b);c.setDash();ang=math.atan2(b[1]-a[1],b[0]-a[0]);
 for q in [-.5,.5]:c.line(*b,b[0]-7*math.cos(ang+q),b[1]-7*math.sin(ang+q))
def legend(y):
 player(53,y,'A');txt('Team A',68,y+7,70,9);player(153,y,'B',red);txt('Team B',168,y+7,70,9);player(253,y,'J',orange);txt('Joker',268,y+7,55,9);cone(345,y);txt('Hütchen',356,y+7,75,9)
 arrow((440,y),(468,y));txt('Ballweg',476,y+7,65,9)
 txt('Gestrichelter Pfeil = Laufweg ohne Ball. Schwarzer Punkt = Ball. Positionen sind Beispiele.',42,y-18,size=9)
def goal(x,y,w=36):
 c.setStrokeColor(ink);c.setFillColor(white);c.rect(x-w/2,y-5,w,10,fill=1)

start('Wochenübersicht','Unser Ablauf für die Saison','Dienstag, 15.09.2026 | Donnerstag, 17.09.2026 | Spiel: Freitag, 18.09.2026')
y=txt('<b>Erwartet: 14-17 Kinder, 2 Trainer.</b> Material je Tag: S. 9-10; Aufteilungen: S. 11.<br/><b>Wochenziel:</b> Nach dem Pass wieder anbieten. Bei eigenem Ball Platz schaffen, bei Ballverlust gemeinsam zurückhelfen. Freitag: 7 gegen 7, vier Viertel à 15 Minuten; Wechsel nur zwischen den Vierteln nach deiner Vorgabe.',42,716)
y=txt('<b>Dienstag | 90 Minuten | Lernen und anwenden</b>',42,y,size=13)
y=table([['Minute','Inhalt','Dauer / Seite'],['0-5','Begrüßung, Wochenziel, kurze Demonstration','5 Min.'],['5-20','Aufwärmen: Dribbeln durch Hütchentore','15 Min. / S. 2'],['20-22','Trinken, Paare bilden','2 Min.'],['22-37','Passen durch Tore und Freilaufen','15 Min. / S. 3'],['37-52','3 gegen 3 + Joker und 4 gegen 4','15 Min. / S. 4'],['52-55','Trinken, Teams und Positionen erklären','3 Min.'],['55-88','7 gegen 7, ggf. Joker: 15 + 3 Pause + 15','33 Min. / S. 5'],['88-90','Abschlussfrage, gemeinsames Aufräumen starten','2 Min.'] ],y,[62,320,123])
y=txt('<b>Donnerstag | 90 Minuten | Wiederholen und sicher werden</b>',42,y,size=13)
y=table([['Minute','Inhalt','Dauer / Seite'],['0-5','Begrüßung; zwei bekannte Merksätze','5 Min.'],['5-17','Locker durch Hütchentore dribbeln','12 Min. / S. 2'],['17-20','Trinken und Gruppen einteilen','3 Min.'],['20-35','Pass, Mitnahme und gezielter Torschuss','15 Min. / S. 6'],['35-50','Spielaufbau und Einwurf ohne Gegnerdruck','15 Min. / S. 7'],['50-55','Trinken, Teams und Aufgaben erklären','5 Min.'],['55-82','7 gegen 7, ggf. Joker: 12 + 3 Pause + 12','27 Min. / S. 5'],['82-90','Locker auslaufen/gehen, trinken, Freitag besprechen','8 Min.'] ],y,[62,320,123])
txt('Saison-Rahmen: Ankommen - Aufwärmen mit Ball - Technik - spielnah anwenden - Abschlussspiel - kurzer Rückblick. Donnerstag bleibt die Reihenfolge gleich, die Belastung ist vor diesem Freitagsspiel geringer.',42,y,size=9.5)
end()
start('Aufwärmen | beide Tage','Dribbeln durch Hütchentore','Dienstag: 15 Minuten | Donnerstag: 12 Minuten | 14-17 Kinder gleichzeitig; Skizze für 15')
f=field(157,402,280,280,'25 m (bei 17: 28 m)','25 m (bei 17: 28 m)')
for a,b in [(.2,.2),(.55,.15),(.8,.3),(.3,.45),(.68,.5),(.17,.7),(.48,.8),(.82,.8)]:gate(*f(a,b),22)
for i,(a,b) in enumerate([(.08,.1),(.35,.13),(.72,.13),(.88,.45),(.48,.34),(.1,.4),(.35,.64),(.58,.64),(.9,.66),(.1,.88),(.35,.92),(.65,.91),(.89,.93),(.48,.55),(.7,.35)]):player(*f(a,b),str(i+1),ball=True)
legend(375)
y=section('Aufbau','Acht Hütchentore, jeweils ca. 2 m breit, unregelmäßig verteilen. Zwischen den Toren genügend Platz lassen. Jedes Kind hat einen Ball. Bei 17 Kindern auf ca. 28 × 28 m erweitern. Material: 14-17 Bälle, 20 Hütchen (16 für Tore + 4 Ecken). Ein Trainer erklärt, der andere hilft.',330)
y=section('Dienstag: Ablauf in vier Schritten','3 Min. frei dribbeln. 4 Min. nach jedem Tor die Richtung ändern. 4 Min. auf Signal mit der Sohle stoppen, hochschauen und zu einem freien Tor weiter. Zum Schluss 4 Runden mit je 45 Sek. Tore sammeln + 15 Sek. locker dribbeln. Eigene Trefferzahl verbessern; niemand scheidet aus.',y)
y=section('Donnerstag: vertraut und locker','4 Min. frei durch verschiedene Tore. 4 Min. wechselnd mit rechts und links führen. 4 Min. auf Signal stoppen, hochschauen und locker weiter. Kein Zeitwettbewerb und keine zusätzlichen Sprintserien.',y)
section('Sagen und beobachten','„Ball nah am Fuß!“ - „Schau hoch!“ - „Wo ist Platz?“ Bei Zusammenstößen Feld vergrößern oder Tore weiter auseinanderstellen.',y)
end()
start('Dienstag | Hauptübung 1','Passen und wieder anbieten','22.-37. Minute | 15 Minuten | 14-17 Kinder | Aufteilung siehe S. 11')
f=field(150,416,285,250,'25 m (bei 17: 28 m)','25 m (bei 17: 28 m)')
for a,b in [(.25,.35),(.7,.7),(.7,.2),(.2,.8),(.5,.52),(.85,.47),(.45,.12),(.45,.9)]:gate(*f(a,b),23)
player(*f(.25,.2),'A',ball=True);player(*f(.25,.5),'B');arrow(f(.25,.25),f(.25,.46));arrow(f(.29,.22),f(.7,.85),True);arrow(f(.29,.52),f(.66,.64))
player(*f(.7,.85),'A',color=HexColor('#79A8CA'));player(*f(.7,.61),'B',color=HexColor('#79A8CA'))
txt('1. Pass durch Tor',59,713,205,10);txt('2. B dribbelt; A läuft mit',282,713,270,10)
legend(389)
y=section('Organisation','Gleiches Feld und gleiche acht Tore wie beim Aufwärmen. 14: 7 Paare; 15: 6 Paare + 1 Trio; 16: 8 Paare; 17: 7 Paare + 1 Trio. Material: 7-8 Bälle, 20 Hütchen. Die Skizze zeigt nur ein Paar in zwei aufeinanderfolgenden Situationen; alle Gruppen bewegen sich gleichzeitig frei im Feld.',344)
y=section('So läuft eine Aktion ab','A passt durch ein Hütchentor zu B. B nimmt seitlich mit und dribbelt zu einem anderen freien Tor. A läuft ohne Ball mit und stellt sich auf dessen gegenüberliegender Seite anspielbar auf. B passt durch dieses Tor zu A. Nicht zweimal hintereinander dasselbe Tor nutzen.',y)
y=section('Dreiergruppe und Zeitaufteilung','Dreiergruppe: feste Reihenfolge A - B - C - A; alle laufen zum nächsten Tor mit. 3 Min. vormachen und ausprobieren, 5 Min. genau passen und mitnehmen, 5 Min. nach dem Pass zügig anbieten, 2 Min. saubere Tore-Pässe zählen.',y)
section('Traineraufgabe','Jeder Trainer begleitet eine Hälfte der Gruppen. „Erst schauen, dann passen!“ - „Nimm in den freien Raum mit!“ - „Nach dem Pass weiterbewegen!“ Keine Kontaktbegrenzung.',y)
end()
start('Dienstag | Hauptübung 2','Kleine Spiele, viele Aktionen','37.-52. Minute | 15 Minuten | Ein Trainer pro Feld')
f=field(72,435,192,205,'22 m','18 m');g=field(325,420,215,230,'28 m','20 m')
for fun in [f,g]:
 gate(*fun(.5,0),25);gate(*fun(.5,1),25)
for a,b in [(.25,.2),(.75,.25),(.5,.45)]:player(*f(a,b),'A')
for a,b in [(.25,.8),(.75,.75),(.6,.58)]:player(*f(a,b),'B',red)
player(*f(.25,.5),'J',orange,True)
for a,b in [(.2,.2),(.75,.2),(.3,.4),(.75,.45)]:player(*g(a,b),'A')
for a,b in [(.2,.8),(.75,.8),(.25,.6),(.75,.6)]:player(*g(a,b),'B',red)
txt('<b>7 Kinder: 3 gegen 3 + Joker</b>',62,691,235,11);txt('<b>8 Kinder: 4 gegen 4</b>',320,691,235,11)
legend(390)
y=section('Aufbau und Spielregeln','Aufteilung nach Kinderzahl: S. 11; Skizze zeigt 15 Kinder. Material: 16 Hütchen, 4 Bälle, Leibchen. Die Felder mit mindestens 3 m Abstand anlegen. Je ein ca. 2 m breites Hütchentor auf jeder Grundlinie. Keine Torhüter. Ein Punkt zählt, wenn ein Kind kontrolliert durch das gegnerische Tor dribbelt. Bei Aus eindribbeln; Gegner geben Platz. Ersatzbälle liegen bei den Trainern.',344)
y=section('Ablauf: vier Runden','1 Min. erklären, dann 4 × 3 Min. spielen; zwischen Runde 1/2 und 2/3 jeweils 1 Min. Rückmeldung = 15 Min. Joker vor jeder neuen Runde wechseln; der letzte Wechsel erfolgt direkt. Der Joker hilft immer dem Team mit Ball.',y)
y=section('Worauf ihr achtet','Mit Ball: Bieten sich Kinder seitlich an? Nach Ballverlust: Helfen alle zurück? Nicht jede Aktion korrigieren. In einer Rückmeldung nur einen Punkt nennen. Bei wenigen erfolgreichen Aktionen das Feld etwas vergrößern.',y)
section('Kurze Zurufe','„Mach dich frei!“ - „Hilf deinem Mitspieler!“ - „Alle helfen zurück!“ Tore zählen normal; keine zusätzliche Pflichtzahl an Pässen.',y)
end()
start('Abschlussspiel | beide Tage','7 gegen 7 und Joker-Varianten','Dienstag: 15 + 3 + 15 Minuten | Donnerstag: 12 + 3 + 12 Minuten')
f=field(175,394,245,286,'ca. 35 m Breite','ca. 45 m Länge')
c.setStrokeColor(HexColor('#719777'));c.line(*f(0,.5),*f(1,.5));c.circle(*f(.5,.5),30,stroke=1,fill=0)
goal(*f(.5,0));goal(*f(.5,1))
for a,b,l in [(.5,.05,'TW'),(.27,.18,'V'),(.73,.18,'V'),(.14,.33,'M'),(.5,.32,'M'),(.86,.33,'M'),(.4,.45,'S')]:player(*f(a,b),l)
for a,b,l in [(.5,.95,'TW'),(.27,.82,'V'),(.73,.82,'V'),(.14,.67,'M'),(.5,.68,'M'),(.86,.67,'M'),(.6,.55,'S')]:player(*f(a,b),l,red)
player(*f(.87,.49),'J',orange)
legend(367)
y=section('Aufbau und Rollen','14 Kinder: 7 gegen 7; 15: +1 Innenjoker; 16: +2 Außenjoker; 17: +1 Innen- und 2 Außenjoker (S. 11). Skizze: 15 Kinder. Grundordnung: TW - 2 hinten (V) - 3 Mitte (M) - 1 vorne (S). Feldmaß: Trainingsvorschlag; euer Spieltagsfeld verwenden, falls bekannt. Material: 2 Tore, 6 Hütchen, 4 Bälle, Leibchen.',323)
y=section('Joker und Wechsel','Alle Joker helfen dem Team mit Ball und erzielen keine Tore. Außenjoker stehen je an einer Seitenlinie außerhalb des Feldes; sie sind nicht angreifbar. Rollen nur in der Pause tauschen. Joker sind Trainingsrollen; am Freitag gilt normales 7 gegen 7.',y)
y=section('Dienstag: Spielrhythmus kennenlernen','Zwei volle 15-Minuten-Blöcke. In der 3-Minuten-Pause trinken, ein Lob und einen Verbesserungspunkt geben. Ein Trainer begleitet jeweils ein Team. Nicht laufend unterbrechen.',y)
section('Donnerstag: kürzer und ohne Zusatzbelastung','Zwei 12-Minuten-Blöcke mit 3 Min. Pause. Aufgaben: breit anbieten, nach dem Pass bewegen, gemeinsam zurückhelfen. Bei Müdigkeit früher beenden und den Abschluss verlängern.',y)
end()
start('Donnerstag | Hauptübung 1','Pass, Mitnahme, Torschuss','20.-35. Minute | 15 Minuten | Zwei Stationen mit je 7-9 Kindern | Aufteilung S. 11')
f=field(130,403,330,270,'20 m','18 m')
goal(*f(.5,.96),70);player(*f(.5,.9),'TW',red)
for a,b in [(.23,.16),(.23,.07),(.13,.07)]:player(*f(a,b),'A',ball=True)
player(*f(.67,.4),'B');player(*f(.82,.4),'B');player(*f(.88,.25),'B')
cone(*f(.23,.23));cone(*f(.67,.34));arrow(f(.28,.19),f(.62,.38));arrow(f(.67,.45),f(.58,.67));arrow(f(.57,.7),f(.5,.9));arrow(f(.24,.24),f(.64,.32),True)
txt('Tor: 5 m breit',224,716,200,10);txt('Skizze: Station mit 7 Kindern',180,385,300,10)
y=section('Aufbau und Gruppen','Zwei gleiche Felder nebeneinander mit mindestens 3 m Abstand; pro Feld ein gesichertes Jugendtor und ein Trainer. Je Station 1 Torwart. 7 Kinder: A3/B3; 8: A4/B3; 9: A4/B4. Material insgesamt: 2 Tore, 12 Hütchen, 8 Bälle, Leibchen. A steht ca. 14 m, B ca. 10 m vor dem Tor, seitlich versetzt.',353)
y=section('Ablauf und Rotation','A passt flach zu B und stellt sich danach hinten bei B an. B nimmt Richtung Tor mit und schießt aus etwa 7-9 m. Anschließend Ball holen und mit Ball hinten bei A anstellen. Nächste Aktion erst, wenn der Schussweg frei ist. Torwart nach jeder Runde wechseln.',y)
y=section('Zeitaufteilung und Belastung','2 Min. vormachen. Dann 3 Runden à 4 Min., dazwischen je 30 Sek. Rollenwechsel = 15 Min. insgesamt. Runde 1: sicher treffen. Runde 2: zur anderen Seite aufbauen. Runde 3: Schussecke selbst wählen. Locker zurückgehen, keine Schusskraft-Wettbewerbe.',y)
section('Trainerhinweise','„Schau vor dem Pass!“ - „Erster Kontakt Richtung Tor!“ - „Genau schießen!“ Erfolg ermöglichen: Entfernung verkürzen, wenn Abschlüsse kaum gelingen. Übrige Bälle außerhalb des Schusswegs lagern.',y)
end()
start('Donnerstag | Hauptübung 2','Spielaufbau und Einwurf','35.-50. Minute | 15 Minuten | Ruhig durchspielen, ohne Gegnerdruck')
f=field(135,412,320,245,'ca. 35 m','ca. 22 m (halbes Feld)');goal(*f(.5,0))
for a,b,l in [(.5,.08,'TW'),(.22,.25,'V'),(.78,.25,'V'),(.12,.57,'M'),(.5,.53,'M'),(.88,.57,'M'),(.5,.86,'S')]:player(*f(a,b),l)
player(*f(0,.45),'E',orange,True)
arrow(f(.47,.1),f(.25,.24));arrow(f(.23,.29),f(.15,.52));arrow(f(.16,.6),f(.46,.82));arrow(f(.02,.46),f(.1,.55))
txt('E = Einwerfer (nur bei der Einwurf-Aufgabe)',145,394,355,10)
y=section('Organisation','Je Trainer 7-9 Kinder in einer Spielfeldhälfte (Aufteilung S. 11). Je 7 bilden die Grundordnung. Bei 8 kommt ein Einwerfer/Ballgeber dazu, bei 9 beide Rollen. Zusatzkinder wechseln nach jeder Aktion ins Feld. Bei 7 übernimmt ein Mittelfeldspieler den Einwurf. Material: 2 Tore, 8 Hütchen, 4 Bälle. Skizze: 8 Kinder.',362)
y=section('Erste 7 Minuten: vom Torwart aufbauen','Torwart spielt flach zu einem der beiden hinteren Spieler. Dieser nimmt mit und sucht einen freien Mittelfeldspieler; danach Richtung Stürmer weiterspielen. Ball zurück zum Start bringen. Rechts und links abwechseln. Gehen oder locker traben reicht. Dies ist eine Orientierungshilfe, kein starrer Pflicht-Spielzug.',y)
y=section('1 Minute wechseln, danach 7 Minuten Einwurf','Ball liegt an der Seitenlinie. Ein Kind bietet sich kurz, eines weiter vorne an. Einwerfer entscheidet, wirft und bietet sich danach im Feld wieder an. Nach jedem Versuch Rollen tauschen. Technik kurz vormachen: beide Hände, von hinter dem Kopf, beide Füße am Boden an oder hinter der Linie.',y)
section('Was am Freitag hängen bleiben soll','„Wenn unser Torwart den Ball hat, gehen wir auseinander.“ - „Beim Einwurf helfen zwei Kinder.“ Die konkreten Spielfortsetzungen richten sich am Spieltag nach euren Veranstalterregeln; hier wird kein gegnerischer Abstand vorgegeben.',y)
end()
start('Trainerblatt | Freitag vorbereiten','Einfach organisieren, klar begleiten','Spiel am 18.09.2026 | 7 gegen 7 | 4 × 15 Minuten laut deiner Vorgabe')
y=section('Material vor beiden Trainings','Materiallisten für Dienstag und Donnerstag: S. 9-10. Für bis zu 17 Kinder vorbereiten, tatsächliche Zahl zu Beginn eintragen. Felder vor Beginn vorbereiten; Hütchen wiederverwenden. Der Co-Trainer kann den Donnerstag mit dem bekannten Aufwärmen selbstständig beginnen.',715)
y=section('Donnerstag: letzte 8 Minuten','82-85: locker gehen, Ball wegräumen und trinken. 85-88: Treffpunkt, Ausrüstung und Viertelregel erklären. 88-90: ein kurzer positiver Teamabschluss. Keine zusätzliche Konditionseinheit am Ende.',y)
y=section('Viertelbesetzung vorher aufschreiben','Die 14-17 Trainingskinder sind nicht automatisch der Freitagskader. Erst klären, wer E1 bzw. E2 spielt. Für jedes Viertel 1 Torwart + 6 Feldspieler festlegen; Wechsel laut deiner Vorgabe nur in den Viertelpausen. Einsatzzeiten über mehrere Spieltage fair verteilen.',y)
y=table([['Rolle','Viertel 1','Viertel 2','Viertel 3','Viertel 4'],['Torwart','','','',''],['Hinten links','','','',''],['Hinten rechts','','','',''],['Mitte links','','','',''],['Mitte zentral','','','',''],['Mitte rechts','','','',''],['Vorne','','','','']],y,[105,100,100,100,100])
y=section('In der Viertelpause','Erst trinken und kurz Luft holen. Dann ein konkretes Lob und höchstens eine Aufgabe: „Ihr habt euch gut angeboten. Jetzt helfen wir nach Ballverlust schneller zurück.“ Anschließend Wechsel und neue Positionen ruhig nennen.',y)
y=section('Euer gemeinsamer Trainermaßstab','Erklärungen kurz halten und einmal zeigen. Fehler zulassen. Mutige Versuche und gegenseitige Hilfe loben. Nur ein Trainer spricht zur gleichen Zeit zur Gesamtgruppe. Nach dem Training kurz abgleichen: Was gelang, was wiederholen wir?',y)
txt('Planungsbasis: Angaben des Trainers zu Teilnehmerzahl und Spielmodus. Übungen und Feldmaße sind Trainingsvorschläge; Skizzen zeigen beispielhafte Positionen. Allgemeine Orientierung: DFB, Trainingsphilosophie Deutschland (www.dfb.de). Keine zusätzliche Prüfung der lokalen Spielordnung.',42,y,size=9)
end()
start('Dienstag | Packliste','Material und Teilnehmer','15.09.2026 | Erwartet: 14-17 Kinder | Betreuung: 2 Trainer | 90 Minuten')
y=txt('Tatsächlich dabei: ______ Kinder &nbsp;&nbsp; Trainer: __________________________<br/>Vor Beginn zählen und die passende Aufteilung auf S. 11 auswählen.',42,714)
y=table([['Material','Für den Tag bereitlegen'],['Bälle','17 passende Trainingsbälle, davon bei Spielen 4 als Spiel-/Ersatzbälle. Jeder hat beim Aufwärmen einen Ball.'],['Hütchen / Markierungsteller','48 Stück: bis 20 für das Aufwärmfeld, 16 für zwei Kleinfelder, 6 für das große Feld, 6 Reserve. Zwischen Übungen wiederverwenden.'],['Leibchen','9 blau + 9 rot + 3 gelb = 21. Gelb für Joker.'],['Tore','2 gesicherte Jugendtore. Kleine Dribbeltore werden aus Hütchen gebaut.'],['Trainerzubehör','1 Uhr/Timer, 1 Pumpe mit Nadel, 1 Maßband oder vorbereitete Feldmaße, dieser Plan.'],['Am Platz','Trinkflasche je Kind, zugängliches Erste-Hilfe-Set.']],y,[132,373])
y=section('Aufbau vor Beginn','Aufwärmfeld 25 × 25 m, bei 17 Kindern ca. 28 × 28 m. Acht Hütchentore à 2 m plus vier Ecken. Zwei Kleinfelder nach Gruppengröße (S. 11) mit Abstand. Großes Feld ca. 45 × 35 m bzw. euer bekanntes Spieltagsfeld.',y)
y=table([['Übung','Gleichzeitig benötigt'],['Dribbeln (S. 2)','14-17 Kinder, 14-17 Bälle, 20 Hütchen'],['Passen (S. 3)','14-17 Kinder, 7-8 Bälle, gleiches Hütchenfeld'],['Kleine Spiele (S. 4)','Zwei Gruppen mit 7-9 Kindern; 16 Hütchen, 4 Bälle, Leibchen'],['Abschlussspiel (S. 5)','14 Feld-/Torwartrollen + 0-3 Joker; 2 Tore, 6 Hütchen, 4 Bälle, Leibchen']],y,[132,373])
section('Wer macht was?','Du erklärst die gemeinsamen Übungen; der Co-Trainer zeigt mit dir vor und hilft einzelnen Kindern. Bei Kleinfeldspielen je ein Trainer pro Feld. Beim Abschlussspiel je ein Trainer pro Team; einer behält auch die Joker im Blick.',y)
end()
start('Donnerstag | Packliste','Material und Teilnehmer','17.09.2026 | Erwartet: 14-17 Kinder | Betreuung: 2 Trainer | 90 Minuten')
y=txt('Tatsächlich dabei: ______ Kinder &nbsp;&nbsp; Trainer: __________________________<br/>Vertraute Abläufe, weniger Belastung vor dem Freitagsspiel.',42,714)
y=table([['Material','Für den Tag bereitlegen'],['Bälle','17 passende Trainingsbälle. Später 8 an den Torschussstationen, 4 für Aufbau/Spiel.'],['Hütchen / Markierungsteller','40 Stück: 20 für Aufwärmen, 12 für zwei Schussstationen, 6 für das große Feld, 2 Reserve. Beim Aufbau-Üben 8 vorhandene Hütchen nutzen.'],['Leibchen','9 blau + 9 rot + 3 gelb = 21.'],['Tore','2 gesicherte Jugendtore, zuerst je eines pro Schussstation.'],['Trainerzubehör','Uhr/Timer, Pumpe mit Nadel, Maßband, Plan und leere Viertel-Aufstellung.'],['Am Platz','Trinkflasche je Kind, zugängliches Erste-Hilfe-Set.']],y,[132,373])
y=table([['Übung','Gleichzeitig benötigt'],['Dribbeln (S. 2)','14-17 Kinder, 14-17 Bälle, 20 Hütchen'],['Pass und Schuss (S. 6)','Je 7-9 Kinder; 2 Tore, 12 Hütchen (8 Ecken + 4 Startpunkte), 8 Bälle'],['Aufbau / Einwurf (S. 7)','Je 7-9 Kinder; 2 Tore, 8 Hütchen, 4 Bälle'],['Abschlussspiel (S. 5)','14 Spielrollen + 0-3 Joker; 2 Tore, 6 Hütchen, 4 Bälle, Leibchen']],y,[132,373])
y=section('Felder und Trainer','Aufwärmen wie Dienstag. Schussstationen je ca. 20 × 18 m, mit mindestens 3 m Abstand. Aufbau anschließend in zwei Hälften des großen Feldes. Je ein Trainer pro Gruppe; der Co-Trainer kann mit dem bekannten Aufwärmen beginnen, falls du später eintriffst.',y)
section('Belastung steuern','Zwischen Abschlüssen locker zurückgehen. Aufbau ohne Gegnerdruck üben. Abschlussspiel zweimal 12 Min. Bei Müdigkeit kürzen. Die letzten 8 Min. bleiben für Trinken, lockeres Gehen und den positiven Abschluss.',y)
end()
start('Alle Übungen | feste Varianten','So passen 14-17 Kinder hinein','Vor jeder Einheit zählen | Niemand fällt aus einer Übung heraus')
y=table([['Kinder','Passgruppen','Zwei Trainergruppen'],['14','7 Paare','7 + 7'],['15','6 Paare + 1 Dreiergruppe','7 + 8'],['16','8 Paare','8 + 8'],['17','7 Paare + 1 Dreiergruppe','8 + 9']],714,[54,260,191])
y=section('Aufwärmen und Passen','Alle Kinder machen gleichzeitig mit. Bei 14-16: 25 × 25 m, bei 17: ca. 28 × 28 m. Pro Kind ein Ball beim Dribbeln; pro Paar/Trio ein Ball beim Passen. Gruppen bleiben in Bewegung, acht Hütchentore werden gemeinsam genutzt.',y)
y=table([['Gruppe','Kleines Spiel Dienstag','Torschuss Donnerstag'],['7','3 gegen 3 + 1 Joker; ca. 22 × 18 m','1 TW + 3 bei A + 3 bei B'],['8','4 gegen 4; ca. 28 × 20 m','1 TW + 4 bei A + 3 bei B'],['9','4 gegen 4 + 1 Joker; ca. 30 × 22 m','1 TW + 4 bei A + 4 bei B']],y,[54,260,191])
y=section('Spielaufbau / Einwurf Donnerstag','Je Gruppe sieben Kinder in der Grundordnung. Bei 8: ein zusätzliches Kind als Einwerfer/Ballgeber. Bei 9: je ein Einwerfer und Ballgeber. Zusatzrollen nach jeder Aktion mit Feldspielern tauschen. Bei 7 wirft ein Mittelfeldspieler ein.',y)
y=table([['Kinder','Abschlussspiel an beiden Tagen'],['14','7 gegen 7, jeweils inklusive Torwart.'],['15','7 gegen 7 + 1 neutraler Joker im Feld.'],['16','7 gegen 7 + 2 neutrale Außenjoker, je einer an jeder Seitenlinie.'],['17','7 gegen 7 + 1 Innenjoker + 2 Außenjoker.']],y,[54,451])
y=section('Joker einfach erklären','Alle Joker helfen immer dem Team mit Ball und schießen keine Tore. Außenjoker bewegen sich entlang ihrer Seitenlinie außerhalb des Feldes, werden nicht angegriffen und passen zurück ins Feld. Hinter ihnen ca. 2 m freien Raum lassen. Kein Kontaktlimit; zügig weiterspielen.',y)
txt('Joker im Kleinfeld nach jeder Runde tauschen, im Abschlussspiel in der Blockpause. Über beide Trainingstage verschiedene Kinder einsetzen. Am Freitag gelten ausschließlich die Spieltagsrollen und Viertelwechsel.',42,y,size=10)
end();c.save();print(P)
