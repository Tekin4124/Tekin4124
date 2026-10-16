#!/usr/bin/env python3
"""Render the profile's dark mechanical header and project cards with Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets';OUT.mkdir(exist_ok=True)
BG='#0D1117';PANEL='#151C25';LINE='#334151';TEXT='#E6EDF3';MUTED='#A3AFBE';ACCENT='#F47B58';BLUE='#7AA9DD'
FONT='/usr/share/fonts/urw-base35/NimbusSans-Bold.otf'
MONO='/usr/share/fonts/dejavu-sans-mono-fonts/DejaVuSansMono.ttf'
def font(size,mono=False):return ImageFont.truetype(MONO if mono else FONT,size)
def text(d,xy,value,size=24,color=TEXT,mono=False):d.text(xy,value,font=font(size,mono),fill=color)
def line(d,points,color=LINE,width=2):d.line(points,fill=color,width=width,joint='curve')
def gear(d,x,y,angle):
    for i in range(12):
        a=angle+i*math.tau/12
        line(d,[(x+math.cos(a)*21,y+math.sin(a)*21),(x+math.cos(a)*28,y+math.sin(a)*28)],MUTED,5)
    d.ellipse((x-22,y-22,x+22,y+22),fill=PANEL,outline=MUTED,width=3)
    for i in range(3):
        a=angle+i*math.tau/3;line(d,[(x+7*math.cos(a),y+7*math.sin(a)),(x+17*math.cos(a),y+17*math.sin(a))],MUTED,3)
    d.ellipse((x-5,y-5,x+5,y+5),fill=ACCENT)

def hero(phase=0):
    phase %= 1.0
    im=Image.new('RGB',(1280,460),BG);d=ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,1278,458),radius=20,outline=LINE,width=2)
    text(d,(47,40),'MUHAMMET TEKİN',82)
    text(d,(51,140),'Android  /  Web  /  Backend',24,MUTED,True)
    # The indicator, gears, and belt all complete whole cycles in eight seconds.
    d.ellipse((1116,49,1216,149),outline=LINE,width=2)
    d.arc((1123,56,1209,142),int(phase*360),int(phase*360)+100,fill=ACCENT,width=4)
    d.ellipse((1161,94,1171,104),fill=BLUE)
    for i,(x,label) in enumerate([(192,'ANDROID'),(418,'WEB'),(644,'BACKEND'),(870,'AI')]):
        d.rounded_rectangle((x,234,x+174,342),radius=8,fill=PANEL,outline=LINE,width=2)
        text(d,(x+14,246),label,19,MUTED,True)
        direction=1 if i%2==0 else -1
        gear(d,x+87,303,direction*phase*math.tau)
        line(d,[(x+87,234),(x+87,210),(1185,210),(1185,337)],LINE,2)
        d.ellipse((x+82,205,x+92,215),fill=BLUE)
    d.rounded_rectangle((48,355,1232,400),radius=22,fill=PANEL,outline=LINE,width=2)
    # Wrap evenly spaced rollers, avoiding an item popping at the end of a cycle.
    shift=(phase*320)%80
    for i in range(-1,17):
        x=48+i*80+shift
        if 65<=x<=1215:
            d.ellipse((x-6,372,x+6,384),outline=LINE,width=2)
    # Three quiet moving signals remain clipped within the track.
    for i in range(3):
        x=80+((i*360+phase*1080)%1080)
        d.rounded_rectangle((x,366,x+24,388),radius=5,fill=ACCENT if i==0 else BLUE)
    line(d,[(82,428),(1198,428)],LINE,1)
    return im

def card(number,title,description,stack,kind):
    im=Image.new('RGB',(620,242),BG);d=ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,618,240),radius=16,fill=PANEL,outline=LINE,width=2)
    text(d,(28,25),number,16,ACCENT,True)
    text(d,(27,58),title,50)
    text(d,(29,125),description,25,MUTED)
    line(d,[(29,181),(589,181)],LINE,1)
    text(d,(29,200),stack,16,MUTED,True)
    x=550;y=64
    if kind=='truck':
        d.rectangle((x-29,y,x+6,y+30),outline=BLUE,width=3)
        line(d,[(x+7,y+9),(x+24,y+9),(x+34,y+24),(x+34,y+32),(x+6,y+32)],BLUE,3)
        for cx in [x-15,x+22]:d.ellipse((cx-6,y+25,cx+6,y+37),fill=ACCENT,outline=PANEL,width=2)
    elif kind=='flow':
        for yy in [y,y+18,y+36]:d.rectangle((x-30,yy,x-4,yy+10),fill=BLUE)
        line(d,[(x+9,y+3),(x+29,y+3),(x+29,y+41),(x+9,y+41)],ACCENT,3)
    elif kind=='room':
        d.rectangle((x-24,y-1,x+20,y+46),outline=BLUE,width=3);d.ellipse((x+6,y+22,x+12,y+28),fill=ACCENT)
    elif kind=='photo':
        d.rectangle((x-32,y,x+29,y+44),outline=BLUE,width=3)
        line(d,[(x-28,y+39),(x-10,y+17),(x+6,y+34),(x+17,y+23),(x+26,y+39)],BLUE,3)
        d.ellipse((x+11,y+6,x+20,y+15),fill=ACCENT)
    elif kind=='contact':
        d.rectangle((x-29,y+3,x+29,y+42),outline=BLUE,width=3)
        line(d,[(x-29,y+3),(x,y+25),(x+29,y+3)],ACCENT,3)
    else:
        for xx in [x-29,x+2]:d.rectangle((xx,y,xx+28,y+43),outline=BLUE,width=3)
        for yy in [y+12,y+23,y+34]:line(d,[(x-23,yy),(x-7,yy)],ACCENT,2)
    return im

def main():
    hero().save(OUT/'profile-dark-static.png',optimize=True)
    palette=hero().quantize(colors=48)
    frames=[hero(i/200).quantize(palette=palette,dither=Image.Dither.NONE) for i in range(200)]
    # Complete frames and background disposal avoid trails in GIF decoders.
    frames[0].save(OUT/'profile-dark.gif',save_all=True,append_images=frames[1:],duration=40,loop=0,optimize=False,disposal=2)
    projects=[('01','Yükio','Lojistik ilan eşleştirme','KOTLIN / COMPOSE / ROOM','truck'),('02','TekinFlow','Satın alma ve teslimat','COMPOSE / REACT / KTOR','flow'),('03','RoomFlow','Toplantı odası ekranları','ANDROID / NODE / DOCKER','room'),('04','Ultra HD','Fotoğraf restorasyonu','PYTHON / PYTORCH / GRADIO','photo'),('05','NoteFlow','İki sayfalı dijital defter','JAVASCRIPT / NODE / SQLITE','notes'),('06','İletişim','Proje ve iş birliği','MUHAMMET-TEKIN.DEV','contact')]
    for project in projects:card(*project).save(OUT/f'dark-project-{project[0]}.png',optimize=True)
    print('GIF bytes:',(OUT/'profile-dark.gif').stat().st_size)
if __name__=='__main__':main()
