"""Bemaßte Dienstagsskizzen; Koordinaten in Metern ab linker Torecke des Feldes."""
import math
from reportlab.platypus import Flowable
from reportlab.lib.colors import HexColor, white

class TuesdayDiagram(Flowable):
    def __init__(self, kind):
        super().__init__()
        self.kind, self.width, self.height = kind, 511, 390

    def draw(self):
        c = self.canv
        navy, blue, red, green, gold = map(HexColor, ['#17354A','#2473a5','#bb4f4f','#16836c','#d79626'])
        def xy(x,y): return 64+10*x, 62+10*y
        def label(x,y,t,size=8,col=navy):
            c.setFillColor(col); c.setFont('Coach',size); c.drawString(x,y,t)
        def player(x,y,t,col=blue,ball=False):
            X,Y=xy(x,y); c.setFillColor(col);c.setStrokeColor(white);c.circle(X,Y,8,fill=1)
            c.setFillColor(white);c.setFont('CoachBold',6);c.drawCentredString(X,Y-2,t)
            if ball: c.setFillColor(navy);c.circle(X+9,Y-6,2.5,fill=1,stroke=0)
        def path(points,col=blue,dash=False,thick=1.4):
            c.setStrokeColor(col);c.setLineWidth(thick);c.setDash(4,3) if dash else c.setDash()
            coords=[xy(*p) for p in points]
            for a,b in zip(coords,coords[1:]):c.line(*a,*b)
            c.setDash();a,b=coords[-2:];ang=math.atan2(b[1]-a[1],b[0]-a[0])
            for z in [-.5,.5]:c.line(*b,b[0]-6*math.cos(ang+z),b[1]-6*math.sin(ang+z))
        def num(x,y,n):
            X,Y=xy(x,y);c.setFillColor(white);c.setStrokeColor(navy);c.circle(X,Y,7,fill=1)
            c.setFillColor(navy);c.setFont('CoachBold',7);c.drawCentredString(X,Y-2,str(n))
        def dim(a,b,t,vertical=False):
            X,Y=xy(*a);U,V=xy(*b);c.setStrokeColor(navy);c.setLineWidth(.6);c.line(X,Y,U,V)
            if vertical:
                c.line(X-3,Y,X+3,Y);c.line(U-3,V,U+3,V)
                c.saveState();c.translate(X-6,(Y+V)/2);c.rotate(90);c.setFont('Coach',8);c.setFillColor(navy);c.drawCentredString(0,0,t);c.restoreState()
            else:
                c.line(X,Y-3,X,Y+3);c.line(U,V-3,U,V+3);label((X+U)/2-12,Y+5,t)
        # Fixed field geometry in every drawing.
        c.setFillColor(HexColor('#eaf3e9'));c.setStrokeColor(HexColor('#7da084'));c.rect(*xy(0,0),300,230,fill=1)
        dim((0,-2),(30,-2),'30 m');dim((-3,0),(-3,23),'23 m',True)
        X,Y=xy(12.5,0);c.setFillColor(white);c.setStrokeColor(navy);c.rect(X,Y-7,50,7,fill=1)
        # Torbreite ist auf der Aufbaukarte im Text angegeben.
        for cx in [4,26]:
            for x in [cx-1.5,cx+1.5]:
                c.setFillColor(gold);c.circle(*xy(x,23),3,fill=1,stroke=0)
        label(*xy(2.4,24),'3 m',7);label(*xy(24.4,24),'3 m',7)
        X,Y=xy(15,15);c.setFillColor(gold);c.rect(X-5,Y-8,10,16,fill=1,stroke=0)
        if self.kind in ['MEASURE','V1','V2','V3']:
            c.setFillColor(HexColor('#d7e9f4'));c.rect(*xy(0,10),300,40,fill=1,stroke=0)
            # Restore mannequin above shaded band, draw boundaries as training aids.
            c.setStrokeColor(blue);c.setDash(2,3)
            for y in [10,14]:c.line(*xy(0,y),*xy(30,y))
            c.setDash();c.setFillColor(gold);c.rect(X-5,Y-8,10,16,fill=1,stroke=0)
            player(15,1,'TW')
            label(385,171,'Abschluss:',8);label(385,157,'10-14 m',9,blue)
            label(385,137,'bei Bedarf',7);label(385,125,'8-10 m',8)
            # Six waiting players = the two other trios, beyond start line.
            for i,x in enumerate([3,6,9]):player(x,27,'2'+chr(97+i),HexColor('#7c919b'))
            for i,x in enumerate([21,24,27]):player(x,27,'3'+chr(97+i),HexColor('#7c919b'))
            label(71,354,'Trio 2 wartet seitlich');label(270,354,'Trio 3 wartet seitlich')
            label(79,369,'Rückweg außen am Feld; neuer Start erst bei freiem Schussweg.',7)
            player(5,21,'P',ball=True);player(15,21,'A')
            if self.kind=='MEASURE':
                player(15,23,'D1',red);player(19,12,'D2',red)
                c.setStrokeColor(gold);c.setDash(3,2);c.circle(*xy(15,15),20,stroke=1);c.setDash()
                dim((32,0),(32,15),'15 m zur Figur',True)
                dim((28,15),(28,21),'6 m',True)
                label(387,278,'D1: Variante 1',8,red);label(387,262,'D2: Variante 2/3',8,red)
                label(387,230,'Figur mittig',8)
                label(387,97,'Kreis: 2 m',8);label(387,83,'Abstand halten',8)
            else:
                path([(6,21),(14,21)]);num(10,22,1)
                path([(15,20),(14.6,18.5),(13,17),(12.5,15),(12,13)],green);num(10.6,16.5,2)
                if self.kind=='V1':
                    player(15,23,'D',red)
                    path([(16,22.4),(17,19),(16.8,16),(15.5,13)],red,True)
                    label(385,278,'D wartet, bis',8,red);label(385,264,'A die Höhe der',8,red);label(385,250,'Figur erreicht.',8,red)
                    path([(12,12),(14,1.8)],navy,False,2.2);num(10.5,8,3)
                else:
                    player(19,12,'D',red);path([(18.5,12.5),(15.3,14)],red,True)
                    label(385,278,'D startet beim',8,red);label(385,264,'ersten Kontakt',8,red);label(385,250,'von A.',8,red)
                    if self.kind=='V2':
                        path([(12,12),(14,1.8)],navy,False,2.2);num(10.5,8,3)
                        path([(20,13),(25,18),(26,22)],red);num(27.5,18,4)
                        label(385,222,'Roter Pfeil:',8);label(385,208,'nur nach',8);label(385,194,'Ballgewinn!',8)
                    else:
                        path([(5,20),(6,16),(7,12)],blue,True);num(4.5,15,2)
                        path([(11.5,12),(8,11.5)],blue);num(9,10,3)
                        path([(7.5,10.7),(13.5,1.8)],navy,False,2.2);num(7,6.5,4)
                        label(385,222,'Beispiel:',8);label(385,208,'A passt zu P.',8)
                        label(385,97,'A darf auch',8);label(385,83,'selbst schießen.',8)
        else:
            # All ten children are shown; only one pair is highlighted.
            positions=[(4,5,6,7),(23,5,25,7),(6,14,8,16),(22,15,24,17),(12,20,15,21)]
            for i,(a,b,d,e) in enumerate(positions):
                col=blue if i==0 else HexColor('#7c919b')
                player(a,b,str(i+1)+'A',col,True);player(d,e,str(i+1)+'B',col,self.kind=='WARM1')
            if self.kind=='WARM1':
                path([(4,4),(7,3),(10,5),(9,8)],green);num(11,7,1)
                path([(6,6),(8,5),(11,7)],green,True);num(12,10,2)
                label(385,279,'5 Paare =',9);label(385,264,'10 Kinder',9)
                label(385,233,'Jeder hat',8);label(385,219,'einen Ball.',8)
                label(385,186,'A führt,',8);label(385,172,'B folgt mit Ball.',8)
                label(385,130,'Kein Torschuss.',8)
            else:
                # Highlight one possible gate action away from other pairs.
                path([(4.5,6),(5.6,6.8)],blue)
                path([(6,8),(4,12),(4,18),(4,21)],green);num(2,17,1)
                path([(4,22),(4,25)],blue);num(2,25,2)
                player(4,26,'1A',HexColor('#709fbb'))
                path([(3,6),(1,15),(1,25),(3,26)],blue,True)
                label(385,279,'5 Paare,',9);label(385,264,'5 Bälle',9)
                label(385,232,'Helles 1A =',8);label(385,218,'spätere Position,',8)
                label(385,204,'kein extra Kind.',8)
                label(385,175,'Nur ein freies',8);label(385,161,'Tor anlaufen.',8)
                label(385,130,'Tor danach',8);label(385,116,'gleich freigeben.',8)
            label(66,369,'Alle Paare bewegen sich gleichzeitig. Wege sind nur Beispiele.',8)
            label(66,354,'Figur bleibt stehen; mit Abstand daran vorbeidribbeln.',8)
        label(35,16,'Blau durchgezogen: Pass | Grün: Dribbling | Gestrichelt: Bewegung',7.5)
        label(35,3,'Dicker schwarzer Pfeil: Schuss | Rot: Verteidiger | Gelb: Figur / Hütchen',7.5)
