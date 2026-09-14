#!/usr/bin/env python3
"""Erzeugt den Sprachleitfaden als PDF aus Markdown.
Aufruf: python3 scripts/text_pdf.py (beliebiges Arbeitsverzeichnis).
Unterstützt Überschriften, Absätze, Listen, Tabellen und <!-- pagebreak -->.
Abhängigkeit: reportlab. Die Markdown-Datei ist die bearbeitbare Textquelle.
"""
from pdf_fonts import register_fonts
register_fonts()
from pathlib import Path
from html import escape
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Saison_2026-2027/Trainersprache/01_Saetze_und_Ansprachen.md'
OUT=SRC.with_suffix('.pdf')
navy=HexColor('#17354A'); ink=HexColor('#253744')
styles={
 'body':ParagraphStyle('body',fontName='Coach',fontSize=10,leading=14,spaceAfter=6,textColor=ink),
 'title':ParagraphStyle('title',fontName='CoachBold',fontSize=21,leading=26,spaceAfter=14,textColor=navy,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='CoachBold',fontSize=13,leading=18,spaceBefore=9,spaceAfter=9,textColor=navy,keepWithNext=True),
 'cell':ParagraphStyle('cell',fontName='Coach',fontSize=9.5,leading=13,textColor=ink),
}
def markup(s):
 s=escape(s)
 return re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
def foot(c,doc):
 c.saveState();c.setFillColor(navy);c.rect(0,802,596,40,fill=1,stroke=0);c.setFillColor(white);c.setFont('CoachBold',9);c.drawString(42,818,'E2-TRAINER | TRAINERSPRACHE | SAISON 2026/2027')
 c.setFillColor(ink);c.setFont('Coach',9);c.drawString(42,26,'Kurze Hinweise. Ehrliches Lob. Gemeinsam lernen.');c.drawRightString(553,26,str(doc.page));c.restoreState()
lines=SRC.read_text().splitlines(); story=[];i=0
while i<len(lines):
 line=lines[i].strip()
 if not line:i+=1;continue
 if line=='<!-- pagebreak -->':story.append(PageBreak());i+=1;continue
 if line.startswith('|'):
  rows=[]
  while i<len(lines) and lines[i].strip().startswith('|'):
   cells=[s.strip() for s in lines[i].strip().strip('|').split('|')]
   if not all(re.fullmatch(r'[:\- ]+',v) for v in cells):rows.append([Paragraph(markup(v),styles['cell']) for v in cells])
   i+=1
  t=Table(rows,colWidths=[151,360],repeatRows=1,hAlign='LEFT')
  t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#DDEBEF')),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#F3F6F7')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
  story.extend([t,Spacer(1,9)]);continue
 if line.startswith('# '):story.append(Paragraph(markup(line[2:]),styles['title']))
 elif line.startswith('## '):story.append(Paragraph(markup(line[3:]),styles['h2']))
 elif re.match(r'^\d+\. ',line):story.append(Paragraph(markup(line),styles['body']))
 elif line.startswith('- '):story.append(Paragraph('• '+markup(line[2:]),styles['body']))
 else:
  group=[line]
  while i+1<len(lines) and lines[i+1].strip() and not lines[i+1].startswith(('#','|','- ','<!--')) and not re.match(r'^\d+\. ',lines[i+1]):
   i+=1;group.append(lines[i].strip())
  story.append(Paragraph(markup(' '.join(group)),styles['body']))
 i+=1
SimpleDocTemplate(str(OUT),pagesize=(595.28,841.89),leftMargin=42,rightMargin=42,topMargin=57,bottomMargin=48,title='Trainersprache: Sätze und Ansprachen | E-Jugend').build(story,onFirstPage=foot,onLaterPages=foot)
print(OUT)
