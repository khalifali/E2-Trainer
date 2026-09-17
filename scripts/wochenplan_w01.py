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
y=table([['Minute','Inhalt','Dauer / Seite'],['0-5','Begrüßung; zwei bekannte Merksätze','5 Min.'],['5-17','Locker durch Hütchentore dribbeln','12 Min. / S. 2'],['17-20','Trinken und Gruppen einteilen','3 Min.'],['20-35','Torjagd: Passen, Mitnehmen, Freilaufen','15 Min. / S. 6'],['35-50','Spielaufbau 7 gegen 2 mit Konter','15 Min. / S. 7, 12'],['50-55','Trinken, Teams und Aufgaben erklären','5 Min.'],['55-82','7 gegen 7, ggf. Joker: 12 + 3 Pause + 12','27 Min. / S. 5'],['82-90','Locker auslaufen/gehen, trinken, Freitag besprechen','8 Min.'] ],y,[62,320,123])
txt('Saison-Rahmen: Ankommen - Aufwärmen mit Ball - Technik - spielnah anwenden - Abschlussspiel - kurzer Rückblick. Donnerstag bleibt die Reihenfolge gleich, die Belastung ist vor diesem Freitagsspiel geringer.',42,y,size=9.5)
end()
start('Aufwärmen | beide Tage','Dribbeln durch Hütchentore','Dienstag: 15 Minuten | Donnerstag: 12 Minuten | 14-17 Kinder gleichzeitig; Skizze für 15')
f=field(157,402,280,280,'25 m (bei 17: 28 m)','25 m (bei 17: 28 m)')
for a,b in [(.2,.2),(.55,.15),(.8,.3),(.3,.45),(.68,.5),(.17,.7),(.48,.8),(.82,.8)]:gate(*f(a,b),22)
for i,(a,b) in enumerate([(.08,.1),(.35,.13),(.72,.13),(.88,.45),(.48,.34),(.1,.4),(.35,.64),(.58,.64),(.9,.66),(.1,.88),(.35,.92),(.65,.91),(.89,.93),(.48,.55),(.7,.35)]):player(*f(a,b),str(i+1),ball=True)
legend(375)
y=section('Aufbau','Acht Hütchentore, jeweils ca. 2 m breit, unregelmäßig verteilen. Zwischen den Toren genügend Platz lassen. Jedes Kind hat einen Ball. Bei 17 Kindern auf ca. 28 × 28 m erweitern. Material: 14-17 Bälle, 20 Hütchen (16 für Tore + 4 Ecken). Ein Trainer erklärt, der andere hilft.',330)
y=section('Dienstag: Ablauf in vier Schritten','3 Min. frei dribbeln. 4 Min. nach jedem Tor ein anderes freies Tor wählen. 4 Min.: „Stopp“, mit der Sohle anhalten, 2-3 Sek. umschauen, erst bei „Weiter“ losdribbeln. Zum Schluss 4 Runden mit je 45 Sek. Durchgänge zählen + 15 Sek. locker dribbeln. Eigene Durchgangszahl verbessern; niemand scheidet aus.',y)
y=section('Donnerstag: vertraut und locker','4 Min. frei durch verschiedene Tore. 4 Min. wechselnd mit rechts und links führen. 4 Min.: „Stopp“, 2-3 Sek. umschauen, erst bei „Weiter“ locker losdribbeln. Kein Zeitwettbewerb und keine zusätzlichen Sprintserien.',y)
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
start('Donnerstag | Hauptübung 1','Torjagd: Pass und Mitnahme','20.-35. Minute | 15 Minuten | Zwei Felder, alle spielen gleichzeitig')
f=field(143,488,310,215,'22-25 m','18-20 m')
for a,b in [(.25,.27),(.72,.25),(.25,.73),(.72,.73)]:gate(*f(a,b),33)
for a,b,l in [(.25,.12,'A'),(.25,.44,'A'),(.8,.87,'A')]:player(*f(a,b),l,ball=l=='A' and b==.12)
for a,b in [(.48,.2),(.56,.57),(.2,.9)]:player(*f(a,b),'B',red)
player(*f(.84,.48),'J',orange)
arrow(f(.25,.17),f(.25,.39));arrow(f(.28,.45),f(.43,.48))
legend(460)
y=section('Aufbau und Punkte','Je Feld vier Hütchentore, 2-3 m breit, mit freiem Auslauf. 7 Kinder: 3 gegen 3 + Joker; 8: 4 gegen 4; 9: 4 gegen 4 + Joker. Ein Trainer je Feld. Pass durch ein Tor zu einem Mitspieler + kontrollierte erste Mitnahme aus der Torlinie ins Freie = 1 Punkt. Joker spielen beim Team mit Ball und dürfen Punkte vorbereiten und erzielen.',413)
y=section('Freilaufen und Entscheidungen','Alle Tore sind von beiden Seiten nutzbar. Nach einem Punkt bleibt der Ball beim Team; ein anderes Tor suchen. Das letzte Tor zählt erst nach einem Punkt an einem anderen Tor oder nach gegnerischem Ballgewinn wieder. Gegner dürfen aktiv erobern, aber nicht dauerhaft im Tor parken. Keine feste Passfolge, kein Kontaktlimit.',y)
y=section('Drei Runden und kurze Wechsel','2 Min. zeigen + 3 × 4 Min. spielen + zweimal 30 Sek. Jokerwechsel/Trinken. Runde 1: kennenlernen. Runde 2: vor der Annahme links/rechts schauen. Runde 3: eigene Punktzahl aus Runde 2 verbessern. Niemand scheidet aus. Ausball: Gegner spielt ein oder dribbelt ein; 3 m Platz lassen. Direkter Neustart durch ein Tor zählt noch nicht.',y)
y=section('Anpassen und Material','Zu schwer: breitere Tore, zunächst zwei Kontakte zur Mitnahme. Optional eine standfeste Figur pro Feld zwischen zwei Toren: aus ihrem Schatten anbieten; Laufwege freihalten. Insgesamt 24 Hütchen, 4 Bälle, Leibchen, optional 2 Figuren. Mindestens 3 m zwischen den Feldern.',y)
txt('<b>Ansage:</b> „Passt durch ein freies Tor. Nehmt ins Freie mit! Danach ein anderes Tor suchen und wieder anbieten!“',42,y,size=10)
end()
start('Donnerstag | Hauptübung 2','Spielaufbau mit Balljägern','35.-50. Minute | 15 Minuten | Standard: 7 gegen 2 | Rotation und Nebenfeld: S. 12')
f=field(143,488,310,215,'ca. 30 m Breite','ca. 35 m Länge')
goal(*f(.5,0),52)
gate(*f(.2,1),36);gate(*f(.8,1),36)
for a,b,l in [(.5,.08,'TW'),(.23,.25,'V'),(.77,.25,'V'),(.12,.55,'M'),(.5,.5,'M'),(.88,.55,'M'),(.55,.84,'S')]:player(*f(a,b),l)
for a,b in [(.38,.36),(.68,.63)]:player(*f(a,b),'B',red)
arrow(f(.46,.1),f(.26,.23));arrow(f(.23,.3),f(.14,.5))
legend(460)
y=section('Sieben bauen auf, zwei jagen','Die Sieben sind 1 Torwart + 6 Feldspieler in 2-3-1. Sie greifen zwei 3 m breite Dribbeltore an: kontrolliert durchdribbeln = 1 Punkt. Die Gegner erobern den Ball und dürfen auf das Jugendtor schießen = 1 Punkt. Bei Ballverlust sofort umschalten; Zurückerobern ist erlaubt.',413)
y=section('Start und freie Lösungen','Torwart spielt vom Boden zu einem frei gewählten Mitspieler. Gegner starten etwa 8 m vor ihm und greifen mit dem ersten Pass an. Nach Tor, Punkt oder Toraus neuer Ball vom Torwart. Seitenaus: flach einspielen oder eindribbeln. Rückpass, Seitenwechsel und Andribbeln erlauben; keine feste Passkette.',y)
y=section('Druck dosieren','Mit 2 Gegnern beginnen. Bei vielen Ballverlusten zunächst breiter aufbauen oder auf 1 Gegner reduzieren. Wenn mehrere Angriffe gelingen, auf 3 Gegner steigern. Nicht automatisch erschweren. Startabstand, Punkte und Dribbeltore sind Trainingssonderregeln.',y)
y=section('Zeit und Neustarts','2 Min. zeigen + 4 × 3 Min. spielen + insgesamt 1 Min. Rollenwechsel. In Runde 2 und 4 ersten Angriff von der Seitenlinie starten: zwei Mitspieler bieten sich kurz bzw. weiter vorne an. Einspielen/Eindribbeln ersetzt den alten Einwurfteil. Grundlage: hinterlegter BFV-Merkzettel 2025/26; Gültigkeit 2026/27 nicht bestätigt.',y)
txt('<b>Ansage:</b> „Macht das Feld breit! Welche Seite ist frei? Die Balljäger dürfen nach Ballgewinn auf unser Tor schießen!“',42,y,size=10)
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
y=table([['Material','Für den Tag bereitlegen'],['Bälle','17 Trainingsbälle. Torjagd: 4; Aufbau und Nebenfeld: 5; Abschlussspiel: 4. Zwischen Übungen wiederverwenden.'],['Hütchen / Markierungsteller','40 Stück: Torjagd 24; Aufbau 8 + Nebenfeld 4; 4 Reserve. Aufwärmen: 20 davon. Optional 2 standfeste Trainingsfiguren.'],['Leibchen','9 blau + 9 rot + 3 gelb = 21.'],['Tore','2 gesicherte Jugendtore; beim Aufbau ein Tor, im Abschlussspiel beide.'],['Trainerzubehör','Uhr/Timer, Pumpe mit Nadel, Maßband, Plan und leere Viertel-Aufstellung.'],['Am Platz','Trinkflasche je Kind, zugängliches Erste-Hilfe-Set.']],y,[132,373])
y=table([['Übung','Gleichzeitig benötigt'],['Dribbeln (S. 2)','14-17 Kinder, 14-17 Bälle, 20 Hütchen'],['Torjagd (S. 6)','Je 7-9 Kinder; 24 Hütchen, 4 Bälle, Leibchen; optional 2 Figuren'],['Aufbau (S. 7, 12)','Hauptfeld: 7 + 2; übrige Kinder Nebenfeld. 1 Tor, 12 Hütchen, 5 Bälle, Leibchen'],['Abschlussspiel (S. 5)','14 Spielrollen + 0-3 Joker; 2 Tore, 6 Hütchen, 4 Bälle, Leibchen']],y,[132,373])
y=section('Felder und Trainer','Aufwärmen wie Dienstag. Torjagd: zwei Felder, je 22-25 × 18-20 m. Danach Aufbau 35 × 30 m und Nebenfeld 15 × 12 m, mindestens 3 m Abstand. Je ein Trainer pro Feld; der Co-Trainer kann mit dem bekannten Aufwärmen beginnen, falls du später eintriffst.',y)
section('Belastung steuern','Kurze Erklärungen, viele Ballaktionen. Gegnerzahl beim Aufbau dem Können anpassen. Keine zusätzlichen Sprintserien. Abschlussspiel zweimal 12 Min. Bei Müdigkeit kürzen. Die letzten 8 Min. bleiben für Trinken, lockeres Gehen und den positiven Abschluss.',y)
end()
start('Alle Übungen | feste Varianten','So passen 14-17 Kinder hinein','Vor jeder Einheit zählen | Niemand fällt aus einer Übung heraus')
y=table([['Kinder','Passgruppen','Zwei Trainergruppen'],['14','7 Paare','7 + 7'],['15','6 Paare + 1 Dreiergruppe','7 + 8'],['16','8 Paare','8 + 8'],['17','7 Paare + 1 Dreiergruppe','8 + 9']],714,[54,260,191])
y=section('Aufwärmen und Passen','Alle Kinder machen gleichzeitig mit. Bei 14-16: 25 × 25 m, bei 17: ca. 28 × 28 m. Pro Kind ein Ball beim Dribbeln; pro Paar/Trio ein Ball beim Passen. Gruppen bleiben in Bewegung, acht Hütchentore werden gemeinsam genutzt.',y)
y=table([['Gruppe','Kleines Spiel Dienstag','Torjagd Donnerstag'],['7','3 gegen 3 + 1 Joker; ca. 22 × 18 m','3 gegen 3 + Joker; ca. 22 × 18 m'],['8','4 gegen 4; ca. 28 × 20 m','4 gegen 4; ca. 25 × 20 m'],['9','4 gegen 4 + 1 Joker; ca. 30 × 22 m','4 gegen 4 + Joker; ca. 25 × 20 m']],y,[54,260,191])
y=section('Spielaufbau Donnerstag','Immer 7 Aufbauspieler inklusive Torwart gegen 1, 2 oder 3 Gegner. Alle übrigen Kinder spielen beim zweiten Trainer im Nebenfeld. Nach zwei Runden Aufbaugruppen tauschen; einzelne Rollen nach etwa 90 Sek. wechseln. Genaue Einteilung: S. 12.',y)
y=table([['Kinder','Abschlussspiel an beiden Tagen'],['14','7 gegen 7, jeweils inklusive Torwart.'],['15','7 gegen 7 + 1 neutraler Joker im Feld.'],['16','7 gegen 7 + 2 neutrale Außenjoker, je einer an jeder Seitenlinie.'],['17','7 gegen 7 + 1 Innenjoker + 2 Außenjoker.']],y,[54,451])
y=section('Joker einfach erklären','Dienstag und Abschlussspiel: Joker helfen dem Team mit Ball und schießen keine Tore. Bei der Torjagd dürfen Joker Punkte erzielen. Außenjoker bewegen sich entlang ihrer Seitenlinie außerhalb des Feldes, werden nicht angegriffen und passen zurück ins Feld. Hinter ihnen ca. 2 m freien Raum lassen. Kein Kontaktlimit; zügig weiterspielen.',y)
txt('Joker im Kleinfeld nach jeder Runde tauschen, im Abschlussspiel in der Blockpause. Über beide Trainingstage verschiedene Kinder einsetzen. Am Freitag gelten ausschließlich die Spieltagsrollen und Viertelwechsel.',42,y,size=10)
end()
start('Donnerstag | Organisation','Rotation ohne Warteschlangen','Ergänzung zu S. 7 | Zwei Trainer | Alle Kinder bleiben beteiligt')
y=section('Gruppen und Rollen','Gruppe A baut in Runde 1-2 auf, Gruppe B in Runde 3-4. Jeweils sieben Kinder bilden die Aufbaugruppe. Die andere Gruppe stellt die zwei Balljäger. Alle übrigen Kinder spielen Ballhalten im Nebenfeld, auch überzählige Kinder der aktuellen Aufbaugruppe.',715)
y=table([['Kinder','Gruppen A / B','Nebenfeld bei 7 gegen 2'],['14','7 / 7','5: 2 gegen 2 + Joker'],['15','7 / 8','6: 3 gegen 3'],['16','8 / 8','7: 3 gegen 3 + Joker'],['17','8 / 9','8: 4 gegen 4']],y,[60,125,320])
y=section('Wechsel nach etwa 90 Sekunden','Bei der nächsten Spielunterbrechung zwei neue Balljäger aus deren Gruppe holen. Hat die Aufbaugruppe acht oder neun Kinder, ihre ein bzw. zwei übrigen Kinder mit Feldspielern austauschen. Sie bleiben Mitglieder der Aufbaugruppe und werden nicht zu weiteren Gegnern. Der zweite Trainer koordiniert die Wechsel. Torwartwechsel in einer Rundenpause ermöglichen.',y)
y=section('Nebenfeld: Ballhalten mit Punkten','Etwa 15 × 12 m, mindestens 3 m vom Hauptfeld entfernt. Drei Pässe am Stück = 1 Punkt; danach weiter ab null. Bei Ballgewinn Rollen sofort wechseln. Ein Joker hilft immer dem Team mit Ball; Joker regelmäßig tauschen. Ausball: Gegner spielt flach ein oder dribbelt ein. Ersatzball bereithalten.',y)
y=table([['Gegner im Hauptfeld','Kinder im Nebenfeld (14 / 15 / 16 / 17 gesamt)'],['1 Gegner','6 / 7 / 8 / 9'],['2 Gegner','5 / 6 / 7 / 8'],['3 Gegner','4 / 5 / 6 / 7']],y,[140,365])
y=txt('Nebenfeld: 4 = 2 gegen 2; 5 = 2 gegen 2 + Joker; 6 = 3 gegen 3; 7 = 3 gegen 3 + Joker; 8 = 4 gegen 4; 9 = 4 gegen 4 + Joker. Bei neun Kindern Feld bei Bedarf etwas vergrößern.',42,y)
y=section('Kurze Signale','„Wechsel!“ nur bei einer Unterbrechung: vorbereitete Kinder tauschen die Rollen. „Weiter!“ sobald alle stehen. Nach Runde 2: „Jetzt baut die andere Gruppe auf.“ Keine zusätzlichen Warte- oder Laufrunden.',y)
txt('<b>Stand 17.09.2026:</b> Torjagd und Aufbau mit Gegnern ersetzen die früheren Donnerstagsübungen. Der bearbeitbare Wochenplan und die Ergänzungsdatei enthalten die ausführlichen Regeln.',42,y,size=9.5)
end();c.save();print(P)

