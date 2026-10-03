#!/usr/bin/env python3
"""W04: bearbeitbaren Wochenplan mit passenden Vektorskizzen als PDF ausgeben."""
from pathlib import Path
import math
import re
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from pdf_fonts import register_fonts

register_fonts()
ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'Saison_2026-2027/Trainingswochen/W04_2026-10-05'
PDF = FOLDER / 'E-Jugend_Trainingsplan_Woche_4.pdf'
NAVY, GREEN, RED, BLUE, GOLD = map(HexColor, ['#17354a','#eaf3e9','#bb4f4f','#2473a5','#a77720'])
styles = {
    'body': ParagraphStyle('body',fontName='Coach',fontSize=10,leading=13.5,spaceAfter=7,textColor=NAVY),
    'h1': ParagraphStyle('h1',fontName='CoachBold',fontSize=20,leading=24,spaceAfter=10,textColor=NAVY),
    'h2': ParagraphStyle('h2',fontName='CoachBold',fontSize=11,leading=15,spaceBefore=4,spaceAfter=6,textColor=NAVY),
    'table': ParagraphStyle('table',fontName='Coach',fontSize=9.2,leading=12.3,textColor=NAVY),
}

def inline(s):
    s = escape(s.replace('→', '-&gt;'))
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`([^`]+)`', r'\1', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', s)
    return s.replace('-&amp;gt;', '-&gt;')

class Diagram(Flowable):
    def __init__(self, kind):
        super().__init__()
        self.kind, self.width, self.height = kind, 511, 142

    def draw(self):
        c = self.canv
        def text(x, y, s, size=7.5):
            c.setFillColor(NAVY); c.setFont('Coach', size); c.drawString(x,y,s)
        def pitch(x=30,y=22,w=250,h=105):
            c.setFillColor(GREEN); c.setStrokeColor(HexColor('#7da084')); c.rect(x,y,w,h,fill=1)
        def player(x,y,t,col=BLUE):
            c.setFillColor(col); c.setStrokeColor(white); c.circle(x,y,7,fill=1)
            c.setFillColor(white); c.setFont('CoachBold',5.5); c.drawCentredString(x,y-2,t)
        def arrow(x,y,X,Y,col=NAVY,dash=False):
            c.setStrokeColor(col); c.setLineWidth(1.2); c.setDash(3,2) if dash else c.setDash()
            c.line(x,y,X,Y); c.setDash()
            a=math.atan2(Y-y,X-x)
            for b in [-.45,.45]: c.line(X,Y,X-5*math.cos(a+b),Y-5*math.sin(a+b))
        def goal(x,y,w=40):
            c.setFillColor(white); c.setStrokeColor(NAVY); c.rect(x-w/2,y,w,5,fill=1)
        def gate(x,y,w=24):
            c.setFillColor(GOLD)
            for X in [x-w/2,x+w/2]: c.circle(X,y,2.5,fill=1,stroke=0)
        def note(lines):
            for i,s in enumerate(lines): text(299,118-i*15,s)
        k=self.kind
        if k=='SETUP':
            pitch(30,25,250,95)
            c.setFillColor(white);c.setStrokeColor(NAVY);c.rect(25,57,5,30,fill=1);c.rect(280,57,5,30,fill=1)
            c.setDash(3,2);c.line(134,25,134,120);c.line(175,25,175,120);c.setDash()
            arrow(114,74,48,74);arrow(195,74,264,74)
            text(51,103,'7-8 Kinder');text(192,103,'7-9 Kinder');text(147,52,'9 m',6.5)
            text(71,31,'T1');text(233,31,'T2');text(86,130,'ca. 55 m × 35 m')
            note(['Je Hälfte: 23 m × 24 m','Schüsse zu den äußeren Toren','Mittelraum bleibt frei','Ein Trainer je Hälfte','T1 / T2 = Trainerposition'])
        elif k=='GIVEGO':
            pitch();gate(166,67)
            player(143,42,'A');player(220,80,'B')
            arrow(151,47,210,76,BLUE);text(181,52,'1',7)
            arrow(143,50,169,102,BLUE,True);text(139,88,'2',7)
            arrow(214,86,181,105,BLUE);text(204,106,'3',7)
            c.setStrokeColor(BLUE);c.circle(174,109,7,fill=0);text(172,106,'A',6)
            note(['Beispielpaar, 2 Kinder gezeigt','1: A passt seitlich zu B','2: A läuft durch das freie Tor','3: B passt in As Lauf','Je Hälfte vier Tore verteilen'])
        elif k=='TRIANGLE':
            pitch();goal(156,22);player(156,37,'TW',GOLD)
            player(156,112,'A');player(220,92,'B');player(92,76,'C')
            arrow(164,110,212,94,BLUE);text(186,115,'1',7)
            arrow(148,105,138,73,BLUE,True)
            arrow(212,89,145,68,BLUE);text(177,84,'2',7)
            arrow(135,67,100,72,BLUE);text(113,61,'3',7)
            arrow(91,67,139,29,BLUE);text(101,38,'4',7)
            note(['4 aktive Kinder gezeigt','A-B-A: Doppelpass','Danach A-C, C schließt ab','Später C als Verteidiger','Weitere Kinder seitlich warten'])
        elif k in ('THREEVTWO','TWOVTWO'):
            pitch();goal(156,22);player(156,35,'TW',GOLD);gate(67,124);gate(242,124)
            player(127,98,'A1');player(221,87,'A2')
            if k=='THREEVTWO':player(70,107,'A3')
            player(149,76,'D1',RED);player(176,54,'D2',RED)
            arrow(134,98,213,88,BLUE);arrow(146,83,133,91,RED);arrow(179,62,183,88,RED,True)
            note(([ '6 aktive Kinder gezeigt' ] if k=='THREEVTWO' else ['5 aktive Kinder gezeigt']) + ['D1 macht Druck, D2 sichert','Rot gestrichelt: Passweg schließen','Ballgewinn: auf die gelben Tore','Warteplätze seitlich außerhalb'])
            text(44,130,'23 × 24 m' if k=='THREEVTWO' else '20 × 18 m')
        elif k=='INTERCEPT':
            pitch(53,22,180,105)
            for x,y,t in [(74,44,'A1'),(140,39,'A2'),(212,52,'A3'),(197,108,'A4'),(86,107,'A5')]:player(x,y,t)
            player(103,65,'D1',RED);player(163,82,'D2',RED)
            arrow(97,61,82,49,RED);arrow(157,87,147,108,RED,True)
            arrow(95,108,188,108,BLUE)
            text(105,130,'14 m × 14 m')
            note(['7 Kinder: 5 gegen 2','D1 setzt A1 unter Druck','D2 liest den nächsten Pass','Blau: möglicher weiterer Pass','Feldgröße nach Erfolg anpassen'])
        elif k=='MATCH':
            pitch(30,22,250,105);c.setStrokeColor(NAVY);c.line(155,22,155,127)
            c.setFillColor(white);c.rect(25,60,5,26,fill=1);c.rect(280,60,5,26,fill=1)
            for x,y,t in [(42,73,'TW'),(78,49,'V'),(78,100,'V'),(113,36,'M'),(113,73,'M'),(113,113,'M'),(142,73,'A')]:player(x,y,t)
            for x,y,t in [(268,73,'TW'),(232,49,'V'),(232,100,'V'),(197,36,'M'),(197,73,'M'),(197,113,'M'),(168,73,'A')]:player(x,y,t,RED)
            note(['14 Kinder gezeigt: 7 gegen 7','ca. 55 m × 35 m','15-17 Kinder: Joker ergänzen','Positionen sind Orientierung','Nach dem Pass neu anbieten'])
        text(30,7,'Skizze nicht maßstäblich. Blau/Rot = Teams.' if k=='MATCH' else 'Skizze nicht maßstäblich. Blau = Angriff; Rot = Abwehr; Pfeile zeigen Beispielaktionen.',6.6)

def footer(c,doc):
    c.setStrokeColor(HexColor('#c8d8dc'));c.line(42,34,553,34)
    c.setFillColor(NAVY);c.setFont('Coach',7.5)
    c.drawString(42,22,'SC Kirchdorf | E2 | Woche 4 | 14-17 Kinder | 2 Trainer')
    c.drawRightString(553,22,str(doc.page))

def build():
    story=[]
    for page_idx,page in enumerate((FOLDER/'Wochenplan.md').read_text().split('<!-- PAGE -->')):
        if page_idx: story.append(PageBreak())
        for block in re.split(r'\n\s*\n',page.strip()):
            block=block.strip()
            if not block: continue
            if block.startswith('[['):
                story.extend([Diagram(block[2:-2]),Spacer(1,7)]);continue
            if block.startswith('|'):
                rows=[]
                for line in block.splitlines():
                    cells=[x.strip() for x in line.strip('|').split('|')]
                    if all(re.fullmatch(r'[-: ]+',v) for v in cells):continue
                    rows.append([Paragraph(inline(v),styles['table']) for v in cells])
                widths={2:[60,451],3:[48,231.5,231.5]}[len(rows[0])]
                t=Table(rows,colWidths=widths,hAlign='LEFT',repeatRows=1)
                t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#dce9ed')),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#f3f6f7')]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
                story.extend([t,Spacer(1,7)]);continue
            key='h1' if block.startswith('# ') else 'h2' if block.startswith('## ') else 'body'
            if key!='body':block=block.split(' ',1)[1]
            story.append(Paragraph(inline(block.replace('\n',' ')),styles[key]))
    SimpleDocTemplate(str(PDF),pagesize=(595.28,841.89),leftMargin=42,rightMargin=42,topMargin=35,bottomMargin=44,title='E-Jugend Trainingsplan Woche 4',author='SC Kirchdorf | Trainerplanung').build(story,onFirstPage=footer,onLaterPages=footer)
    print(PDF)

if __name__=='__main__':build()
