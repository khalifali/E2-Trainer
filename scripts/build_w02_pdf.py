#!/usr/bin/env python3
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, String, Polygon
from pathlib import Path
import math

OUT=Path(__file__).resolve().parents[1]/"Saison_2026-2027/Trainingswochen/W02_2026-09-21/E-Jugend_Trainingsplan_Woche_2.pdf"
N=HexColor("#17354A"); G=HexColor("#EAF3E9"); B=HexColor("#2473A5"); R=HexColor("#BB4F4F"); Y=HexColor("#D79626"); X=HexColor("#6F7F87")
ss=getSampleStyleSheet()
H1=ParagraphStyle("H1",parent=ss["Heading1"],fontName="Helvetica-Bold",fontSize=18,leading=21,textColor=N,spaceAfter=8)
H2=ParagraphStyle("H2",parent=ss["Heading2"],fontName="Helvetica-Bold",fontSize=12,leading=15,textColor=N,spaceBefore=4,spaceAfter=5)
BD=ParagraphStyle("BD",parent=ss["BodyText"],fontName="Helvetica",fontSize=9,leading=12,textColor=N,spaceAfter=5)
SM=ParagraphStyle("SM",parent=BD,fontSize=7.8,leading=10)
def p(s,st=BD): return Paragraph(s,st)
def arr(d,a,b,c=B,w=2):
 x1,y1=a;x2,y2=b;d.add(Line(x1,y1,x2,y2,strokeColor=c,strokeWidth=w));q=math.atan2(y2-y1,x2-x1);s=6
 d.add(Polygon([x2,y2,x2-s*math.cos(q-.5),y2-s*math.sin(q-.5),x2-s*math.cos(q+.5),y2-s*math.sin(q+.5)],fillColor=c,strokeColor=c))
def pl(d,x,y,t,c=B):
 d.add(Circle(x,y,7,fillColor=c,strokeColor=white));d.add(String(x,y-2,t,fontName="Helvetica-Bold",fontSize=5.5,fillColor=white,textAnchor="middle"))
def co(d,x,y): d.add(Circle(x,y,2.8,fillColor=Y,strokeColor=None))
def base(title):
 d=Drawing(480,225);x=55;y=25;w=300;h=180;d.add(String(0,212,title,fontName="Helvetica-Bold",fontSize=10,fillColor=N));d.add(Rect(x,y,w,h,fillColor=G,strokeColor=HexColor("#7DA084")));return d,x,y,w,h
def dims(d,x,y,w,h,lx,ly):
 d.add(Line(x,y-12,x+w,y-12,strokeColor=N));d.add(String(x+w/2,y-9,lx,fontSize=7,fillColor=N,textAnchor="middle"));d.add(Line(x-15,y,x-15,y+h,strokeColor=N));d.add(String(x-12,y+h/2,ly,fontSize=7,fillColor=N))
def goal(d,x,y,w=42): d.add(Rect(x-w/2,y,w,5,fillColor=white,strokeColor=N))
def warm1():
 d,x,y,w,h=base("Aufwärmen 1 | Dribbel-Fangen");dims(d,x,y,w,h,"20 m","20 m")
 for i,(a,b) in enumerate([(30,40),(75,125),(130,65),(185,135),(250,45),(50,155),(215,20),(265,95),(110,20),(165,110)]): pl(d,x+a,y+b,str(i+1),R if i<2 else B)
 d.add(String(375,160,"10 Kinder · alle mit Ball",fontName="Helvetica-Bold",fontSize=8,fillColor=N));d.add(String(375,140,"2 Fänger ebenfalls mit Ball",fontSize=8,fillColor=N));return d
def warm2():
 d,x,y,w,h=base("Aufwärmen 2 | Hütchentore + Reaktion");dims(d,x,y,w,h,"20 m","20 m")
 for gx,gy in [(45,40),(145,40),(245,40),(80,115),(210,120),(145,160)]: co(d,x+gx-10,y+gy);co(d,x+gx+10,y+gy)
 for i,(a,b) in enumerate([(30,80),(70,55),(120,95),(170,55),(230,80),(260,140),(185,140),(105,150),(40,140),(145,125)]):pl(d,x+a,y+b,str(i+1))
 d.add(String(375,160,"5-6 Tore · je 2 m breit",fontName="Helvetica-Bold",fontSize=8,fillColor=N));d.add(String(375,135,"Tor · Dreh · Wechsel · Druck",fontSize=8,fillColor=N));return d
def press1():
 d,x,y,w,h=base("Übung 1 | Nicht vor das eigene Tor - nach außen lösen");dims(d,x,y,w,h,"18 m","22 m");goal(d,x+w/2,y)
 for gx in [65,235]:co(d,x+gx-12,y+h);co(d,x+gx+12,y+h)
 pl(d,x+150,y+72,"V");pl(d,x+150,y+122,"A",R);arr(d,(x+150,y+116),(x+150,y+82),R,1.4);arr(d,(x+150,y+72),(x+70,y+158),B,2)
 d.add(String(375,165,"V: ca. 10 m vor Tor",fontName="Helvetica-Bold",fontSize=8,fillColor=N));d.add(String(375,145,"A: 4-5 m hinter V",fontSize=8,fillColor=N));d.add(String(375,120,"Außentore je 3 m",fontSize=8,fillColor=N));return d
def press2():
 d,x,y,w,h=base("Übung 2 | 2 gegen 2 - gemeinsam aus dem Druck");dims(d,x,y,w,h,"20 m","18 m");goal(d,x+w/2,y)
 for gx in [55,245]:co(d,x+gx-12,y+h);co(d,x+gx+12,y+h)
 pl(d,x+105,y+68,"V1");pl(d,x+195,y+68,"V2");pl(d,x+120,y+120,"A1",R);pl(d,x+180,y+120,"A2",R);pl(d,x+150,y+20,"TW",X);arr(d,(x+150,y+28),(x+105,y+60),X,1.4);arr(d,(x+105,y+68),(x+58,y+158),B,2);return d
def pass3():
 d,x,y,w,h=base("Übung 3 | Drei Pässe -> Mitnahme -> Torschuss");dims(d,x,y,w,h,"18 m","22 m");goal(d,x+w/2,y)
 pl(d,x+55,y+155,"A");pl(d,x+145,y+120,"B");pl(d,x+235,y+150,"C");d.add(Rect(x+145,y+55,10,16,fillColor=Y,strokeColor=None))
 arr(d,(x+62,y+151),(x+137,y+123));arr(d,(x+153,y+123),(x+227,y+147));arr(d,(x+230,y+142),(x+165,y+82));arr(d,(x+165,y+82),(x+170,y+25),N,2.3)
 d.add(String(375,165,"2 Stationen · je 5 Kinder",fontName="Helvetica-Bold",fontSize=8,fillColor=N));d.add(String(375,145,"A-B / B-C: je 7-8 m",fontSize=8,fillColor=N));d.add(String(375,120,"Figur ca. 10 m vor Tor",fontSize=8,fillColor=N));return d
def foot(c,doc):
 c.saveState();c.setStrokeColor(HexColor("#C8D8DC"));c.line(20*mm,15*mm,190*mm,15*mm);c.setFillColor(N);c.setFont("Helvetica",7.5);c.drawString(20*mm,10*mm,"SC Kirchdorf | E-Jugend | Woche 2");c.drawRightString(190*mm,10*mm,str(doc.page));c.restoreState()
story=[p("Woche 2 | Mutig abschließen, sicher verteidigen",H1),p("SC Kirchdorf · E-Jugend · 22. und 24. September 2026"),p("<b>Wochenziel:</b> Dienstag: Pass, Dribbling und Abschluss. Donnerstag: unter Druck vor dem eigenen Tor ruhig bleiben, nach außen lösen und anschließend Passfolgen mit Torschuss trainieren."),p("<b>Donnerstag neu für ca. 10 Kinder:</b> zwei Aufwärmübungen, zwei Übungen zum Lösen aus Druck, Drei-Pass-Abschluss und 5 gegen 5."),p("Die Feldmaße sind Orientierungswerte und können je nach Leistungsstand angepasst werden.",SM),PageBreak(),p("Dienstag | Pass, Dribbling, Schuss",H1),p("Der Dienstag bleibt inhaltlich wie bisher geplant: Aufwärmen mit Ball, danach die Torjäger-Challenge in drei Varianten und anschließend viel freies Spiel."),p("<b>Hauptpunkte:</b> erster Kontakt nach vorne; am Hindernis vorbeidribbeln; vor dem Schuss hochschauen; Verteidiger schützt die Mitte und lenkt nach außen."),PageBreak(),p("Donnerstag | ca. 10 Kinder | 90 Minuten",H1),p("<b>Ziel:</b> Druck erkennen, Ball nach außen sichern und anschließend schnell wieder Fußball spielen."),p("Zeitplan",H2)]
rows=[["Minute","Inhalt"],["0-5","Begrüßung + Ziel"],["5-15","Dribbel-Fangen"],["15-25","Hütchentore + Reaktion"],["25-40","Nicht vor das eigene Tor - nach außen lösen"],["40-55","2 gegen 2 - gemeinsam aus dem Druck"],["55-70","Drei Pässe -> Abschluss"],["70-88","5 gegen 5"],["88-90","Lob + Aufräumen"]]
t=Table([[p(str(c),SM) for c in r] for r in rows],colWidths=[28*mm,145*mm]);t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),HexColor("#DCE9ED")),("GRID",(0,0),(-1,-1),.3,HexColor("#C8D8DC")),("VALIGN",(0,0),(-1,-1),"TOP"),("PADDING",(0,0),(-1,-1),4)]));story.append(t)
story += [PageBreak(),p("Donnerstag | Aufwärmen",H1),warm1(),p("<b>10 Minuten:</b> 20 × 20 m. Alle Kinder mit Ball; zwei Fänger ebenfalls mit Ball. Wer abgeschlagen wird, übernimmt die Fängerrolle."),warm2(),p("<b>10 Minuten:</b> 5-6 Hütchentore à ca. 2 m. Kommandos: Tor, Dreh, Wechsel, Druck. Kopf hoch und freie Tore erkennen."),PageBreak(),p("Donnerstag | Druck vor dem eigenen Tor",H1),press1(),p("<b>15 Minuten:</b> Zwei Gruppen à etwa fünf Kinder. V wird von A unter Druck gesetzt. Erster Kontakt seitlich vom eigenen Tor weg; kontrolliert durch ein 3-m-Außentor lösen. Gewinnt A den Ball, sofort aufs große Tor."),p("<b>Merksatz:</b> „Vor dem Tor nicht blind quer - Druck kommt, Ball nach außen!“"),press2(),p("<b>15 Minuten:</b> 20 × 18 m. Zwei Verteidiger bauen gegen zwei Angreifer auf. TW/Trainer eröffnet. Verteidiger lösen durch ein Außentor; nach Ballgewinn greifen die Angreifer sofort das große Tor an."),PageBreak(),p("Donnerstag | Drei Pässe und Abschluss",H1),pass3(),p("<b>15 Minuten:</b> Zwei Stationen mit je fünf Kindern. A -> B, B -> C, C spielt den dritten Pass in den Lauf von A. A nimmt mit, geht an der Figur vorbei und schließt ab."),p("<b>Rotation:</b> A -> B -> C -> A. Später darf ein Verteidiger nach dem dritten Pass seitlich Druck machen."),PageBreak(),p("Donnerstag | Abschlussspiel 5 gegen 5",H1),p("<b>18 Minuten freies Spiel.</b> Feld ca. 35 × 25 m auf zwei große Jugendtore. Normales Tor = 1 Punkt; Tor nach mindestens drei Pässen = 2 Punkte. Bonusregel weglassen, falls sie das Spiel bremst."),p("<b>Trainer:</b> wenig stoppen. Nur gelegentlich erinnern: „Wo ist außen?“ - „Nicht vor unser Tor!“ - „Hilf deinem Mitspieler!“")]
SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=15*mm,bottomMargin=20*mm,title="E-Jugend Trainingsplan Woche 2").build(story,onFirstPage=foot,onLaterPages=foot)
print(OUT)
