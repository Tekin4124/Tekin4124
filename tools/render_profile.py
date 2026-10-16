#!/usr/bin/env python3
"""Original typographic profile artwork; all motion is rendered locally with Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor, ImageEnhance
import math
import argparse

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

def blend(a,b,t):
    a=ImageColor.getrgb(a) if isinstance(a,str) else a
    b=ImageColor.getrgb(b) if isinstance(b,str) else b
    return tuple(round(lerp(x,y,t)) for x,y in zip(a,b))

NAME='MUHAMMET TEKİN'
NAME_FONT=font(109)
LETTERS=[]
name_x=40
for char in NAME:
    width=NAME_FONT.getlength(char)
    if char!=' ':LETTERS.append((char,name_x,width))
    name_x+=width+2
BOTTOMS=[92,710,1110,780,270,92]
HITS=[2,10,6,12,3]
GAME_POINTS=[]
for i in range(5):
    GAME_POINTS.append((BOTTOMS[i],281))
    _,x,width=LETTERS[HITS[i]]
    GAME_POINTS.append((x+width/2,140))
GAME_POINTS.append((BOTTOMS[-1],281))

def ball_position(p):
    q=(p%1)*10;segment=int(q);t=q-segment
    return (lerp(GAME_POINTS[segment][0],GAME_POINTS[segment+1][0],t),lerp(GAME_POINTS[segment][1],GAME_POINTS[segment+1][1],t))

def header(p=0):
    p%=1
    im=Image.new('RGB',(1280,365),BG);d=ImageDraw.Draw(im)
    q=p*10
    for i,(char,x,width) in enumerate(LETTERS):
        strength=0
        for hit,index in enumerate(HITS):
            distance=abs(q-(hit*2+1))
            if i==index:strength=max(strength,max(0,1-distance/.25))
        d.text((x,24),char,font=NAME_FONT,fill=blend(TEXT,ACCENT,strength))
        d.rectangle((x+2,135,x+width-2,138),fill=blend(RULE,ACCENT,strength))
    # Breakout-style scene: a paddle meets the ball, which lights the name's letters.
    pair=min(int(q)//2,4);u=(q-pair*2)/2
    paddle_x=lerp(BOTTOMS[pair],BOTTOMS[pair+1],ease(u))
    line(d,[(40,298),(1240,298)],RULE,1)
    d.rounded_rectangle((paddle_x-48,282,paddle_x+48,290),radius=3,fill=ACCENT)
    for k in range(5,0,-1):
        x,y=ball_position(p-k*.0025)
        c=blend(BG,BLUE,(6-k)/10)
        d.rectangle((x-3,y-3,x+3,y+3),fill=c)
    x,y=ball_position(p);d.rectangle((x-4,y-4,x+4,y+4),fill=TEXT)
    text(d,40,326,'ANDROID   /   WEB   /   BACKEND',24,MUTED,True)
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
    # The entire sequence is clipped into its own panel; nothing can spill above the card.
    panel=Image.new('RGB',(510,243),BG);d=ImageDraw.Draw(panel)
    text(d,1,7,'MESAJ',17,MUTED,True)
    d.rectangle((0,35,509,94),fill=SURFACE)
    text(d,14,53,'İstanbul → Ankara · TIR · 20 ton',23)
    text(d,1,116,'İLAN KARTI',17,MUTED,True)
    d.rectangle((0,144,509,236),fill=SURFACE,outline=RULE,width=1)
    line(d,[(15,194),(494,194)],RULE,1)
    def reveal(start):
        visible=max(0,min(1,(p-start)/.13))
        return visible*(1-ease(max(0,min(1,(p-.87)/.13))))
    text(d,16,156,'İstanbul → Ankara',27,blend(SURFACE,TEXT,reveal(.12)))
    text(d,16,207,'ARAÇ',14,MUTED,True)
    text(d,82,202,'TIR',21,blend(SURFACE,BLUE,reveal(.34)))
    text(d,271,207,'TONAJ',14,MUTED,True)
    text(d,349,202,'20 ton',21,blend(SURFACE,BLUE,reveal(.53)))
    im.paste(panel,(700,15))

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

PAPER='#D7DEE5'
PAPER_INK='#293542'
PAPER_RULE='#AAB8C5'

def notebook_page(title,lines,writing=1,back=False):
    page=Image.new('RGB',(235,202),PAPER);d=ImageDraw.Draw(page)
    for y in [58,87,116,145,174]:line(d,[(14,y),(221,y)],PAPER_RULE,1)
    text(d,15,13,title,17,PAPER_INK,True)
    if back:
        for y,length in [(49,146),(78,175),(107,112)]:line(d,[(15,y),(15+length,y)],PAPER_RULE,2)
    else:
        cursor=None
        for i,value in enumerate(lines):
            progress=max(0,min(1,writing*len(lines)-i))
            shown=value[:round(len(value)*progress)]
            text(d,15,38+i*29,shown,17,PAPER_INK)
            if 0<progress<1:cursor=(15+font(17).getlength(shown)+3,38+i*29)
        if cursor:
            x,y=cursor;line(d,[(x,y),(x,y+18)],ACCENT,2)
        if writing>.5:
            # A restrained annotation highlight stays beneath the text baseline.
            end=15+143*min(1,(writing-.5)*2)
            line(d,[(15,114),(end,114)],ACCENT,3)
    return page

def notebook_scene(p):
    panel=Image.new('RGB',(510,243),BG)
    left=notebook_page('NOTLAR',['Proje planı','Arayüz taslakları','API notları'],1)
    first=notebook_page('TASLAKLAR',['Ekran akışı','Veri modeli','Kontrol listesi'],min(1,p/.28))
    next_page=notebook_page('YENİ SAYFA',['Yeni taslak','Bağlantılar','Son düzenleme'],max(0,min(1,(p-.69)/.21)))
    turning=max(0,min(1,(p-.34)/.36))
    panel.paste(left,(14,23))
    panel.paste(next_page if turning>0 else first,(261,23))
    d=ImageDraw.Draw(panel)
    # Bound pages and the slim spine give the turn a physical anchor.
    for offset in [3,6]:
        line(d,[(15+offset,227+offset),(496,227+offset)],RULE,1)
    d.rectangle((250,23,260,225),fill=RULE)
    for y in [58,109,160,211]:
        d.rounded_rectangle((245,y,265,y+4),radius=2,fill=MUTED)
    if turning==0:return panel
    angle=turning*math.pi
    width=max(1,round(235*abs(math.cos(angle))))
    front=first if turning<.5 else notebook_page('',['','',''],1,back=True)
    shaded=ImageEnhance.Brightness(front).enhance(.65+.35*abs(math.cos(angle)))
    # Render the page in vertical strips with a changing outer edge, creating a curled turn.
    left_edge=261 if turning<.5 else 261-width
    shadow_alpha=round(50*math.sin(angle))
    if shadow_alpha:
        shade=Image.new('RGBA',panel.size,(0,0,0,0));sd=ImageDraw.Draw(shade)
        sd.rectangle((left_edge+5,27,left_edge+width+8,226),fill=(0,0,0,shadow_alpha))
        panel=Image.alpha_composite(panel.convert('RGBA'),shade).convert('RGB')
    for col in range(width):
        fraction=col/max(1,width-1)
        source_x=min(234,round(fraction*234))
        if turning>=.5:source_x=234-source_x
        outer=fraction if turning<.5 else 1-fraction
        lift=round(math.sin(angle)*18*outer)
        strip=shaded.crop((source_x,0,source_x+1,202)).resize((1,202-2*lift),Image.Resampling.BILINEAR)
        panel.paste(strip,(left_edge+col,23+lift))
    d=ImageDraw.Draw(panel)
    edge=left_edge+width-1 if turning<.5 else left_edge
    lift=round(math.sin(angle)*18)
    line(d,[(edge,23+lift),(edge,225-lift)],PAPER_RULE,1)
    return panel

def noteflow(im,p):
    panel=notebook_scene(p)
    if p>.93:panel=Image.blend(panel,notebook_scene(0),ease((p-.93)/.07))
    im.paste(panel,(700,15))

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
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only',nargs='*',choices=[p[-1] for p in PROJECTS],default=[p[-1] for p in PROJECTS])
    options=parser.parse_args()
    header(.12).save(OUT/'profile-arcade-header-still.png',optimize=True)
    hp=header(.12).quantize(colors=64)
    header_frames=[header(i/180).quantize(palette=hp,dither=Image.Dither.NONE) for i in range(180)]
    header_frames[0].save(OUT/'profile-arcade-header.gif',save_all=True,append_images=header_frames[1:],duration=50,loop=0,optimize=True,disposal=1)
    for project in PROJECTS:
        if project[-1] not in options.only:continue
        stem='motion-'+project[-1]+('-v2' if project[-1] in {'yukio','noteflow'} else '')
        still_phase=.75 if project[-1]=='yukio' else .30 if project[-1]=='noteflow' else .35
        frame(project,still_phase).save(OUT/(stem+'-still.png'),optimize=True)
        palette=frame(project,still_phase).quantize(colors=64)
        frames=[frame(project,i/COUNT).quantize(palette=palette,dither=Image.Dither.NONE) for i in range(COUNT)]
        frames[0].save(OUT/(stem+'.gif'),save_all=True,append_images=frames[1:],duration=FRAME_MS,loop=0,optimize=True,disposal=1)
        print(stem,(OUT/(stem+'.gif')).stat().st_size)
        mobile_frame(project,still_phase).save(OUT/(stem+'-mobile-still.png'),optimize=True)
        mobile_palette=mobile_frame(project,still_phase).quantize(colors=64)
        mobile_frames=[mobile_frame(project,i/COUNT).quantize(palette=mobile_palette,dither=Image.Dither.NONE) for i in range(COUNT)]
        mobile_frames[0].save(OUT/(stem+'-mobile.gif'),save_all=True,append_images=mobile_frames[1:],duration=FRAME_MS,loop=0,optimize=True,disposal=1)

if __name__=='__main__':main()
