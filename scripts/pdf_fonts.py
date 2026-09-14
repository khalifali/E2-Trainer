"""Portable PDF-Schriften aus dem vorhandenen ReportLab-Paket einbetten."""
from pathlib import Path
import reportlab
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def register_fonts():
    fonts = Path(reportlab.__file__).resolve().parent / 'fonts'
    pdfmetrics.registerFont(TTFont('Coach', str(fonts / 'Vera.ttf')))
    pdfmetrics.registerFont(TTFont('CoachBold', str(fonts / 'VeraBd.ttf')))
    pdfmetrics.registerFontFamily('Coach', normal='Coach', bold='CoachBold', italic='Coach', boldItalic='CoachBold')
