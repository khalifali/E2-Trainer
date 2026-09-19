#!/usr/bin/env python3
"""W02 aus Markdown mit drei maßfreien Vektorskizzen erzeugen (ReportLab)."""
from pathlib import Path
import re, math
from html import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from pdf_fonts import register_fonts
from w02_diagrams import TuesdayDiagram

register_fonts()
ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'Saison_2026-2027/Trainingswochen/W02_2026-09-21'
PDF = FOLDER / 'E-Jugend_Trainingsplan_Woche_2.pdf'
NAVY, GREEN, RED, BLUE = [HexColor(x) for x in ['#17354A','#eaf3e9','#bb4f4f','#2473a5']]
styles = {
 'body': ParagraphStyle('body',fontName='Coach',fontSize=9.3,leading=12.7,spaceAfter=7,textColor=NAVY),
 'h1': ParagraphStyle('h1',fontName='CoachBold',fontSize=20,leading=24,spaceAfter=12,textColor=NAVY),
 'h2': ParagraphStyle('h2',fontName='CoachBold',fontSize=11,leading=15,spaceBefore=4,spaceAfter=6,textColor=NAVY),
 'table': ParagraphStyle('table',fontName='Coach',fontSize=8.7,leading=11.5,textColor=NAVY),
}
def inline(s):
 s=escape(s.replace("→", "->"))
 s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
 s=re.sub(r'`([^`]+)`',r'\1',s)
 s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',s)
 return s

class Diagram(Flowable):
 def __init__(self,kind):
  Flowable.__init__(self); self.kind=kind; self.width=511; self.height=166 if kind!='SETUP' else 240
 def draw(self):
  c=self.canv
  def label(x,y,t,size=8):
   c.setFillColor(NAVY);c.setFont('Coach',size);c.drawString(x,y,t)
  def box(x,y,w,h):
   c.setFillColor(GREEN);c.setStrokeColor(HexColor('#7da084'));c.rect(x,y,w,h,fill=1)
  def p(x,y,t,col=BLUE):
   c.setFillColor(col);c.setStrokeColor(white);c.circle(x,y,8,fill=1);c.setFillColor(white);c.setFont('CoachBold',6.5);c.drawCentredString(x,y-2,t)
  def arrow(x,y,X,Y,dashed=False):
   c.setStrokeColor(NAVY);c.setLineWidth(1);c.setDash(3,2) if dashed else c.setDash();c.line(x,y,X,Y);c.setDash()
   a=math.atan2(Y-y,X-x)
   for z in [-.5,.5]:c.line(X,Y,X-6*math.cos(a+z),Y-6*math.sin(a+z))
  def goal(x,y,w=34):
   c.setFillColor(white);c.setStrokeColor(NAVY);c.rect(x-w/2,y,w,5,fill=1)
  def gate(x,y):
   c.setFillColor(HexColor('#df9b32'));c.circle(x-11,y,3,fill=1,stroke=0);c.circle(x+11,y,3,fill=1,stroke=0)
  if self.kind=='SETUP':
   box(25,25,360,135);c.setStrokeColor(NAVY);c.setDash(3,3);c.line(205,25,205,160);c.setDash()
   c.setFillColor(white);c.rect(19,76,6,32,fill=1);c.rect(385,76,6,32,fill=1)
   label(49,141,'Gruppe 1: 10 Kinder');label(237,141,'Gruppe 2: 10 Kinder')
   arrow(150,92,60,92);arrow(260,92,350,92)
   label(64,58,'Schussrichtung');label(264,58,'Schussrichtung')
   label(162,10,'Mittelraum / Trainer')
   box(156,186,98,45);label(166,217,'Nebenfeld');label(177,199,'3 gegen 3');label(270,187,'5 m Abstand',7)
   label(41,168,'7-gegen-7-Feld: ca. 55 × 35 m')
  else:
   box(20,20,260,135);goal(150,20,44);p(150,35,'TW');gate(54,151);gate(247,151)
   if self.kind=='SHOOT':
    p(145,136,'A');p(62,127,'P');p(185,79,'D',RED)
    c.setFillColor(HexColor('#df9b32'));c.rect(143,93,13,15,fill=1,stroke=0)
    arrow(73,128,132,135);arrow(146,125,126,100);arrow(126,100,127,75);arrow(127,70,143,42)
    label(298,142,'Beispiel: Variante 2',10)
    label(298,123,'P passt, A nimmt mit.')
    label(298,107,'Figur umdribbeln, D entscheidet mit.')
    label(298,91,'Schuss bei freiem Weg.')
    label(298,70,'D gewinnt: Konter zum Außentor.')
    label(298,49,'Zwei weitere Trios seitlich warten;')
    label(298,34,'insgesamt 10 Kinder je Hälfte.')
   else:
    for x,y,t in [(72,61,'V1'),(227,61,'V2'),(147,98,'V3')]:p(x,y,t)
    for x,y,t in [(99,85,'J1'),(204,100,'J2'),(185,130,'J3')]:p(x,y,t,RED)
    for x,y,t in [(54,144,'ZL'),(247,144,'ZR'),(145,144,'ZM')]:p(x,y,t,HexColor('#a77720'))
    arrow(138,39,81,56);arrow(70,72,56,131)
    label(298,142,'Beispiel: 10 Kinder',10)
    label(298,123,'Blau: TW + 3 Aufbauspieler')
    label(298,107,'Rot: 3 Balljäger')
    label(298,91,'Gold: 3 bewegliche Zielspieler')
    label(298,70,'Sicher außen anspielen: 2 Punkte')
    label(298,54,'Sicher nach vorne: 1 Punkt')
    label(298,34,'Jäger greifen das große Tor an.')
  label(20,0,'Skizze nicht maßstäblich. Pfeile = beispielhafter Ballweg; gelbe Punkte = Außentore.',7)

def footer(c,doc):
 c.setStrokeColor(HexColor('#c8d8dc'));c.line(42,34,553,34)
 c.setFillColor(NAVY);c.setFont('Coach',8);c.drawString(42,22,'SC Kirchdorf | E-Jugend | Woche 2 | 20 Kinder | 1 Trainer')
 c.drawRightString(553,22,str(doc.page))

def build():
 story=[]
 for page_idx,page in enumerate((FOLDER/'Wochenplan.md').read_text().split('<!-- PAGE -->')):
  if page_idx:story.append(PageBreak())
  blocks=re.split(r'\n\s*\n',page.strip())
  for block in blocks:
   block=block.strip()
   if not block:continue
   if block.startswith('[['):
    kind=block[2:-2]
    drawing=TuesdayDiagram(kind) if kind in ['MEASURE','WARM1','WARM2','V1','V2','V3'] else Diagram(kind)
    story.extend([drawing,Spacer(1,8)]);continue
   if block.startswith('|'):
    rows=[]
    for line in block.splitlines():
     cells=[x.strip() for x in line.strip('|').split('|')]
     if all(re.fullmatch(r'[-: ]+',v) for v in cells):continue
     rows.append([Paragraph(inline(v),styles['table']) for v in cells])
    n=len(rows[0]);widths={2:[85,426],3:[60,220,231],4:[51,94,233,133]}[n]
    t=Table(rows,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#dce9ed')),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#f3f6f7')]),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story.extend([t,Spacer(1,8)]);continue
   key='h1' if block.startswith('# ') else 'h2' if block.startswith('## ') else 'body'
   if key!='body':block=block.split(' ',1)[1]
   story.append(Paragraph(inline(block.replace('\n',' ')),styles[key]))
 SimpleDocTemplate(str(PDF),pagesize=(595.28,841.89),rightMargin=42,leftMargin=42,topMargin=35,bottomMargin=44,title='E-Jugend Trainingsplan Woche 2',author='SC Kirchdorf | Trainerplanung').build(story,onFirstPage=footer,onLaterPages=footer)
 print(PDF)
if __name__=='__main__':build()
