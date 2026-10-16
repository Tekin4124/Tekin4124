#!/usr/bin/env python3
"""Original typographic profile artwork; all motion is rendered locally with Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets';OUT.mkdir(exist_ok=True)
BG='#0D1117';SURFACE='#111821';RULE='#283340';TEXT='#EDF1F5';MUTED='#A5AFBC';ACCENT='#F58262';BLUE='#90B6DD';FAINT='#19232F'
SANS='/usr/share/fonts/urw-base35/NimbusSans-Bold.otf'
MONO='/usr/share/fonts/dejavu-sans-mono-fonts/DejaVuSansMono.ttf'
W,H=1280,278
COUNT=120
FRAME_MS=50

def font(size,mono=False):return ImageFont.truetype(MONO if mono else SANS,size)
def text(d,x,y,s,size=24,color=TEXT,mono=False):d.text((x,y),s,font=font(size,mono),fill=color)
def line(d,xy,color=RULE,width=2):d.line(xy,fill=color,width=width)
def ease(v):return v*v*(3-2*v)
def lerp(a,b,v):return a+(b-a)*v

def header():
    im=Image.new('RGB',(1280,228),BG);d=ImageDraw.Draw(im)
    text(d,35,27,'MUHAMMET TEKİN',91)
    text(d,40,145,'ANDROID   /   WEB   /   BACKEND',25,MUTED,True)
    line(d,[(40,213),(1240,213)])
    d.rectangle((40,210,120,216),fill=ACCENT)
    return im

PROJECTS=[('01','Yükio','Lojistik ilan eşleştirme','KOTLIN · COMPOSE · ROOM','yukio'),('02','TekinFlow','Satın alma ve teslimat','COMPOSE · REACT · KTOR','tekinflow'),('03','RoomFlow','Toplantı odası ekranları','ANDROID · NODE · DOCKER','roomflow'),('04','Ultra HD','Fotoğraf restorasyonu','PYTHON · PYTORCH · GRADIO','ultrahd'),('05','NoteFlow','İki sayfalı dijital defter','JAVASCRIPT · NODE · SQLITE','noteflow')]

def base(project):
    num,title,desc,stack,_=project
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    text(d,38,24,num,18,ACCENT,True)
    text(d,35,62,title,70)
    text(d,40,150,desc,27,MUTED)
    text(d,40,224,stack,18,MUTED,True)
    line(d,[(650,34),(650,244)])
    line(d,[(40,275),(1240,275)])
    return im

def yukio(im,p):
    d=ImageDraw.Draw(im)
    # A message separates into the actual fields used by a load card.
    progress=ease((1-math.cos(p*math.tau))/2)
    line(d,[(700,57),(1210,57)])
    text(d,702,30,'MESAJ',17,MUTED,True)
    text(d,701,76,'İSTANBUL → ANKARA',27)
    text(d,702,113,'TIR  /  20 TON',20,MUTED,True)
    x=lerp(700,728,progress);y=lerp(167,151,progress)
    d.rectangle((x,y,1210,y+74),fill=SURFACE)
    d.rectangle((x,y,x+3,y+74),fill=ACCENT)
    text(d,x+19,y+12,'İstanbul → Ankara',26)
    text(d,x+20,y+47,'TIR',17,BLUE,True)
    text(d,x+188,y+47,'20 ton',17,BLUE,True)
    # Extraction strokes travel from message to their corresponding field.
    for sx,ex in [(763,766),(959,930)]:
        q=(p*2)%1
        yy=140+q*20
        line(d,[(sx,yy),(ex,yy+5)],ACCENT,3)

def tekinflow(im,p):
    d=ImageDraw.Draw(im)
    labels=['SİPARİŞ','SEVK','TESLİM']
    for i,label in enumerate(labels):
        x=700+i*175
        text(d,x,31,label,17,MUTED,True)
        line(d,[(x,60),(x+148,60)])
        for y in [92,130,168,206]:line(d,[(x,y),(x+135,y)],FAINT,2)
    # A single order travels through three workflow columns and back.
    u=(1-math.cos(p*math.tau))/2
    x=700+350*ease(u)
    d.rectangle((x,103,x+146,173),fill=SURFACE,outline=RULE,width=2)
    d.rectangle((x,103,x+146,106),fill=ACCENT)
    text(d,x+14,122,'TF-001',23)
    line(d,[(x+14,157),(x+101,157)],BLUE,3)
    for i in range(3):
        active=i<=round(u*2)
        d.rectangle((700+i*175,228,848+i*175,231),fill=ACCENT if active else RULE)

def roomflow(im,p):
    d=ImageDraw.Draw(im)
    x=720+460*((1-math.cos(p*math.tau))/2)
    occupied=825<x<1025
    text(d,700,32,'TOPLANTI ODASI',18,MUTED,True)
    text(d,699,74,'TOPLANTI' if occupied else 'MÜSAİT',45,ACCENT if occupied else TEXT)
    for i,label in enumerate(['10:30','11:00','11:30']):text(d,701+i*172,160,label,16,MUTED,True)
    d.rectangle((700,192,1210,222),fill=SURFACE)
    d.rectangle((825,192,1025,222),fill=RULE)
    line(d,[(x,179),(x,237)],ACCENT,3)

def photo_base():
    im=Image.new('RGB',(510,194),SURFACE);d=ImageDraw.Draw(im)
    # A typography test pattern illustrates the before/after interaction.
    text(d,32,27,'Aa',124,TEXT)
    for i in range(8):
        x=255+i*24
        line(d,[(x,34),(x,149)],MUTED,1+i%3)
    for y in [164,173,182]:line(d,[(33,y),(476,y)],RULE,1)
    return im
CLEAN=photo_base()
PIXEL=CLEAN.resize((51,20),Image.Resampling.BILINEAR).resize(CLEAN.size,Image.Resampling.NEAREST).filter(ImageFilter.GaussianBlur(1))

def ultrahd(im,p):
    d=ImageDraw.Draw(im)
    text(d,701,27,'ÖNCE',16,MUTED,True);text(d,1130,27,'SONRA',16,MUTED,True)
    cut=round(510*((1-math.cos(p*math.tau))/2))
    im.paste(PIXEL,(700,58));im.paste(CLEAN.crop((0,0,cut,194)),(700,58))
    d=ImageDraw.Draw(im);line(d,[(700+cut,58),(700+cut,252)],ACCENT,3)

def noteflow(im,p):
    d=ImageDraw.Draw(im)
    left=700;top=36
    d.rectangle((left,top,1210,245),fill=SURFACE)
    line(d,[(953,top+13),(953,232)],RULE)
    text(d,721,52,'NOTLAR',19,TEXT,True)
    text(d,976,52,'TASLAK',19,MUTED,True)
    for x in [722,977]:
        for y in [104,139,174,209]:line(d,[(x,y),(x+207,y)],RULE,1)
    # Writing strokes fill and clear as a single reversible loop.
    amount=4*((1-math.cos(p*math.tau))/2)
    for i in range(4):
        extent=max(0,min(1,amount-i))
        if extent:
            y=97+i*35
            line(d,[(722,y),(722+178*extent,y)],TEXT,3)
            if extent<1:line(d,[(722+178*extent,y-9),(722+178*extent,y+6)],ACCENT,2)
    for i,length in enumerate([124,180,92]):line(d,[(977,97+i*35),(977+length,97+i*35)],MUTED,2)

DRAWERS={'yukio':yukio,'tekinflow':tekinflow,'roomflow':roomflow,'ultrahd':ultrahd,'noteflow':noteflow}
def frame(project,p):
    p%=1.0
    im=base(project);DRAWERS[project[-1]](im,p);return im

def mobile_frame(project,p):
    desktop=frame(project,p)
    im=Image.new('RGB',(800,550),BG);d=ImageDraw.Draw(im)
    num,title,desc,stack,_=project
    text(d,40,20,num,18,ACCENT,True)
    text(d,36,57,title,67)
    text(d,40,137,desc,27,MUTED)
    text(d,40,184,stack,17,MUTED,True)
    preview=desktop.crop((680,15,1235,258)).resize((720,315),Image.Resampling.LANCZOS)
    im.paste(preview,(30,221))
    line(ImageDraw.Draw(im),[(40,548),(760,548)])
    return im

def main():
    header().save(OUT/'profile-motion-header.png',optimize=True)
    for project in PROJECTS:
        stem='motion-'+project[-1]
        frame(project,.35).save(OUT/(stem+'-still.png'),optimize=True)
        palette=frame(project,.35).quantize(colors=64)
        frames=[frame(project,i/COUNT).quantize(palette=palette,dither=Image.Dither.NONE) for i in range(COUNT)]
        frames[0].save(OUT/(stem+'.gif'),save_all=True,append_images=frames[1:],duration=FRAME_MS,loop=0,optimize=True,disposal=1)
        print(stem,(OUT/(stem+'.gif')).stat().st_size)
        mobile_frame(project,.35).save(OUT/(stem+'-mobile-still.png'),optimize=True)
        mobile_palette=mobile_frame(project,.35).quantize(colors=64)
        mobile_frames=[mobile_frame(project,i/COUNT).quantize(palette=mobile_palette,dither=Image.Dither.NONE) for i in range(COUNT)]
        mobile_frames[0].save(OUT/(stem+'-mobile.gif'),save_all=True,append_images=mobile_frames[1:],duration=FRAME_MS,loop=0,optimize=True,disposal=1)

if __name__=='__main__':main()
