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
NAME_WIDTH=sum(NAME_FONT.getlength(char)+2 for char in NAME)-2
name_x=(W-NAME_WIDTH)/2
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
    ball_x,ball_y=ball_position(p)
    # The court reacts to the ball; the name stays centered throughout each hit.
    for x in range(64,1240,48):
        line(d,[(x,165),(640+(x-640)*1.02,299)],FAINT,1)
    for y in [177,201,237,278]:line(d,[(58,y),(1222,y)],FAINT,1)
    for x in range(64,1230,16):
        height=3+25*math.exp(-((x-ball_x)/110)**2)
        d.rectangle((x,298-height,x+5,298),fill=blend(RULE,BLUE,height/50))
    for i,(char,x,width) in enumerate(LETTERS):
        strength=0
        for hit,index in enumerate(HITS):
            distance=abs(q-(hit*2+1))
            if i==index:strength=max(strength,max(0,1-distance/.25))
        d.text((x,24-5*strength),char,font=NAME_FONT,fill=blend(TEXT,ACCENT,strength))
        d.rectangle((x+2,135,x+width-2,140),fill=blend(RULE,ACCENT,strength))
    # Brief, directional impact fragments follow hits, rather than looping ornaments.
    for hit,index in enumerate(HITS):
        age=(q-(hit*2+1))%10
        if age<.48:
            _,hx,hw=LETTERS[index];hx+=hw/2
            for k in range(7):
                angle=math.pi*(.12+.76*k/6)
                distance=age*100
                sx=hx+math.cos(angle)*distance;sy=142+math.sin(angle)*distance
                color=blend(BG,ACCENT,(1-age/.48)*.85)
                line(d,[(sx,sy),(sx+math.cos(angle)*7,sy+math.sin(angle)*7)],color,2)
    # Breakout-style scene: a paddle meets the ball, which lights the name's letters.
    pair=min(int(q)//2,4);u=(q-pair*2)/2
    paddle_x=lerp(BOTTOMS[pair],BOTTOMS[pair+1],ease(u))
    line(d,[(58,301),(1222,301)],RULE,1)
    for side in [58,1222]:
        line(d,[(side,167),(side,301)],RULE,2)
    d.rounded_rectangle((paddle_x-55,282,paddle_x+55,292),radius=3,fill=ACCENT)
    line(d,[(paddle_x-42,284),(paddle_x+42,284)],'#FFBEA9',1)
    for hit in range(5):
        age=(q-hit*2)%10
        if age<.35:
            size=age*110
            color=blend(BG,ACCENT,(1-age/.35)*.8)
            for direction in [-1,1]:
                sx=BOTTOMS[hit]+direction*(58+size)
                line(d,[(sx,286),(sx+direction*13,286)],color,2)
    for k in range(12,0,-1):
        x,y=ball_position(p-k*.002)
        c=blend(BG,BLUE,(13-k)/16)
        radius=2+(12-k)/6
        d.rectangle((x-radius,y-radius,x+radius,y+radius),fill=c)
    d.rectangle((ball_x-6,ball_y-6,ball_x+6,ball_y+6),fill=TEXT)
    label='ANDROID   /   WEB   /   BACKEND'
    text(d,(W-font(22,True).getlength(label))/2,326,label,22,MUTED,True)
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
    # Three synthetic messages become a continuous, clipped listing feed.
    panel=Image.new('RGB',(510,243),BG);d=ImageDraw.Draw(panel)
    loads=[('İstanbul','Ankara','TIR','20 ton','İST / ANK'),('Bursa','İzmir','Kamyon','12 ton','BRS / İZM'),('Kocaeli','Konya','TIR','24 ton','KCL / KNY')]
    cycle=(p%1)*len(loads);index=int(cycle);u=cycle-index
    origin,destination,vehicle,weight,short=loads[index]
    clamp=lambda value:max(0,min(1,value))
    visible=ease(clamp(u/.12))*(1-ease(clamp((u-.82)/.16)))
    text(d,0,4,'MESAJLAR',17,MUTED,True)
    text(d,263,4,'İLAN AKIŞI',17,MUTED,True)
    # The next messages wait behind the one being parsed.
    for x,y,width in [(13,64,187),(7,54,199)]:
        d.rounded_rectangle((x,y,x+width,y+113),radius=7,fill=FAINT,outline=RULE)
    source=Image.new('RGBA',(215,124),(0,0,0,0));sd=ImageDraw.Draw(source)
    sd.rounded_rectangle((0,0,214,123),radius=7,fill=SURFACE,outline=RULE)
    sd.rectangle((0,13,2,109),fill=ACCENT)
    text(sd,14,12,origin+' →',25)
    text(sd,14,42,destination,25)
    text(sd,14,88,vehicle+' · '+weight,21,BLUE)
    scan=clamp((u-.12)/.37)
    if .12<u<.49:
        scan_x=8+197*scan
        line(sd,[(scan_x,8),(scan_x,115)],blend(SURFACE,BLUE,.5),1)
    source.putalpha(source.getchannel('A').point(lambda a:round(a*visible)))
    panel.paste(source,(0,round(41+8*(1-visible))),source)
    # A real queue transition: each completed card pushes the previous cards down.
    feed=Image.new('RGB',(247,207),BG)
    enter=ease(clamp((u-.18)/.26))
    def listing(which,y,incoming=False):
        card=Image.new('RGB',(247,94),SURFACE);cd=ImageDraw.Draw(card)
        cd.rounded_rectangle((0,0,246,93),radius=7,outline=RULE,width=1)
        a,b,v,t,_=loads[which%len(loads)]
        alpha=clamp((u-.47)/.15) if incoming else 1
        text(cd,13,13,a+' → '+b,21,blend(SURFACE,TEXT,alpha))
        line(cd,[(13,51),(234,51)],RULE,1)
        for value,x,start in [(v,13,.57),(t,144,.67)]:
            alpha=clamp((u-start)/.13) if incoming else 1
            text(cd,x,64,value,19,blend(SURFACE,BLUE,alpha))
        if incoming:
            cd.rectangle((13,88,13+round(219*clamp((u-.40)/.40)),90),fill=blend(RULE,ACCENT,clamp((u-.40)/.40)))
        else:cd.rectangle((13,88,232,90),fill=ACCENT)
        feed.paste(card,(0,round(y)))
    listing(index-2,108+108*enter)
    listing(index-1,108*enter)
    if enter>0:listing(index,-108+108*enter,True)
    panel.paste(feed,(263,36))
    # Extracted fields travel along three short arcs into the new card.
    for j,value in enumerate([short,vehicle,weight]):
        t=(u-(.30+j*.10))/.22
        if 0<t<1:
            target_x,target_y=[(385,53),(300,105),(434,105)][j]
            tx=lerp(106,target_x,ease(t));ty=lerp(78+j*28,target_y,t)-28*math.sin(t*math.pi)
            alpha=math.sin(t*math.pi)
            chip_width=font(15,True).getlength(value)+18
            chip=Image.new('RGBA',(round(chip_width),26),(0,0,0,0));cd=ImageDraw.Draw(chip)
            cd.rounded_rectangle((0,0,chip.width-1,25),radius=4,fill=SURFACE,outline=BLUE)
            text(cd,9,3,value,15,TEXT,True)
            chip.putalpha(chip.getchannel('A').point(lambda a:round(a*alpha)))
            panel.paste(chip,(round(tx-chip.width/2),round(ty)),chip)
    d=ImageDraw.Draw(panel)
    # The small route strip ties the extraction to the two cities in the message.
    route_alpha=visible
    line(d,[(16,201),(198,201)],RULE,1)
    for x in [16,198]:d.ellipse((x-3,198,x+3,204),fill=BLUE)
    route_x=lerp(16,198,ease(clamp((u-.12)/.68)))
    d.ellipse((route_x-3,198,route_x+3,204),fill=blend(BLUE,ACCENT,route_alpha))
    a,b=short.split(' / ')
    text(d,9,213,a,15,blend(BG,MUTED,route_alpha),True)
    text(d,180,213,b,15,blend(BG,MUTED,route_alpha),True)
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

PAPER='#141A22'
PAPER_INK='#D8E1EB'
PAPER_RULE='#2B3542'

def notebook_page(title,lines,writing=1,back=False):
    page=Image.new('RGB',(235,202),PAPER);d=ImageDraw.Draw(page)
    for y in [58,87,116,145,174]:line(d,[(14,y),(221,y)],PAPER_RULE,1)
    text(d,15,13,title,17,PAPER_INK,True)
    if not back:
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
            line(d,[(15,114),(end,114)],BLUE,2)
    return page

def notebook_scene(p):
    p%=1
    panel=Image.new('RGB',(510,243),BG);d=ImageDraw.Draw(panel)
    d.rounded_rectangle((8,13,502,235),radius=9,fill='#080B10',outline=RULE)
    left=notebook_page('NOTLAR',['Proje planı','Arayüz taslakları','API notları'],1)
    first=notebook_page('TASLAKLAR',['Ekran akışı','Veri modeli','Kontrol listesi'],1)
    next_page=notebook_page('YENİ SAYFA',['Yeni ekran','Klavye kısayolları','Son kontroller'],max(0,min(1,(p-.23)/.31)))
    back=notebook_page('FİKİRLER',['Daha sade','Daha hızlı','Daha akıcı'],1)
    if p<.14:turning=0
    elif p<.42:turning=ease((p-.14)/.28)
    elif p<.58:turning=1
    elif p<.86:turning=1-ease((p-.58)/.28)
    else:turning=0
    # Both sides use the same hinge, including the two resting endpoints.
    hinge=255
    panel.paste(left,(20,23))
    panel.paste(next_page,(hinge,23))
    d=ImageDraw.Draw(panel)
    for offset in [0,3]:
        line(d,[(21,227+offset),(489,227+offset)],PAPER_RULE,1)
    angle=turning*math.pi
    width=max(1,round(235*abs(math.cos(angle))))
    front=first if turning<.5 else back
    shaded=ImageEnhance.Brightness(front).enhance(.56+.44*abs(math.cos(angle)))
    left_edge=hinge if turning<.5 else hinge-width
    shadow_alpha=round(95*math.sin(angle))
    if shadow_alpha:
        shade=Image.new('RGBA',panel.size,(0,0,0,0));sd=ImageDraw.Draw(shade)
        sd.rectangle((left_edge+8,29,left_edge+width+10,228),fill=(0,0,0,shadow_alpha))
        panel=Image.alpha_composite(panel.convert('RGBA'),shade).convert('RGB')
    for col in range(width):
        fraction=col/max(1,width-1)
        source_x=min(234,round(fraction*234))
        outer=fraction if turning<.5 else 1-fraction
        lift=round(math.sin(angle)*22*outer**1.5)
        strip=shaded.crop((source_x,0,source_x+1,202)).resize((1,202-2*lift),Image.Resampling.BILINEAR)
        panel.paste(strip,(left_edge+col,23+lift))
    d=ImageDraw.Draw(panel)
    edge=left_edge+width-1 if turning<.5 else left_edge
    lift=round(math.sin(angle)*22)
    line(d,[(edge,23+lift),(edge,225-lift)],PAPER_RULE,1)
    # Draw the binding last so a moving sheet cannot erase or displace the rings.
    d.rectangle((hinge-3,23,hinge+3,225),fill='#080B10')
    for y in [49,83,117,151,185,215]:
        d.rounded_rectangle((hinge-9,y,hinge+9,y+4),radius=2,fill='#657182')
        line(d,[(hinge-6,y),(hinge+6,y)],'#A2ACB8',1)
    return panel

def noteflow(im,p):
    panel=notebook_scene(p)
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
    header(.12).save(OUT/'profile-arcade-header-v2-still.png',optimize=True)
    hp=header(.12).quantize(colors=64)
    header_frames=[header(i/180).quantize(palette=hp,dither=Image.Dither.NONE) for i in range(180)]
    header_frames[0].save(OUT/'profile-arcade-header-v2.gif',save_all=True,append_images=header_frames[1:],duration=50,loop=0,optimize=True,disposal=1)
    for project in PROJECTS:
        if project[-1] not in options.only:continue
        stem='motion-'+project[-1]+('-v3' if project[-1] in {'yukio','noteflow'} else '')
        still_phase=.26 if project[-1]=='yukio' else .08 if project[-1]=='noteflow' else .35
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
