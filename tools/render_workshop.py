#!/usr/bin/env python3
"""Draw the profile's original mechanical artwork. No remote image service."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets';OUT.mkdir(exist_ok=True)
PAPER='#F2EDDF';INK='#1F2724';ORANGE='#ED542D';GRAY='#BFBBAE';WHITE='#FFFCF4';BLUE='#3459DC'
FONT='/usr/share/fonts/urw-base35/NimbusSans-Bold.otf'
MONO='/usr/share/fonts/dejavu-sans-mono-fonts/DejaVuSansMono.ttf'
def f(size,mono=False):return ImageFont.truetype(MONO if mono else FONT,size)
def txt(d,xy,text,size=24,color=INK,mono=False):d.text(xy,text,font=f(size,mono),fill=color)
def line(d,points,color=INK,width=3):d.line(points,fill=color,width=width,joint='curve')
def gear(d,x,y,r,angle):
    for i in range(10):
        a=angle+i*math.tau/10
        line(d,[(x+math.cos(a)*(r-6),y+math.sin(a)*(r-6)),(x+math.cos(a)*(r+5),y+math.sin(a)*(r+5))],INK,8)
    d.ellipse((x-r+3,y-r+3,x+r-3,y+r-3),fill=PAPER,outline=INK,width=5)
    d.ellipse((x-8,y-8,x+8,y+8),fill=ORANGE)
    for i in range(3):
        a=angle+i*math.tau/3;line(d,[(x+12*math.cos(a),y+12*math.sin(a)),(x+(r-10)*math.cos(a),y+(r-10)*math.sin(a))],INK,4)

def hero(t=0):
    im=Image.new('RGB',(1280,770),PAPER);d=ImageDraw.Draw(im)
    txt(d,(48,30),'MUHAMMET TEKİN',24)
    txt(d,(914,34),'DARICA  /  YAZILIM',18,mono=True)
    line(d,[(48,78),(1232,78)],width=2)
    txt(d,(42,94),'BİR BUTON',119)
    txt(d,(42,205),'DEDİLER.',119)
    # A perforated, overconfident job ticket.
    d.rectangle((845,112,1231,331),fill=WHITE,outline=INK,width=3)
    for x in range(858,1230,22):d.ellipse((x,106,x+10,118),fill=PAPER)
    txt(d,(866,132),'İŞ EMRİ   /   0001',18,mono=True)
    line(d,[(865,170),(1212,170)],width=1)
    phrases=[("Abi şuraya bi'",'buton eklesene.'),("Bi' de mobilde",'çalışsın.'),('Madem başladık,','panel de olsun.')]
    a,b=phrases[int(t//4)%3]
    txt(d,(865,187),a,31);txt(d,(865,226),b,31)
    txt(d,(866,289),'TAHMİNİ SÜRE: 5 DK',18,mono=True)
    line(d,[(1023,303),(1208,289)],ORANGE,3)
    txt(d,(48,352),'Küçük istekler, birbirine bağlı büyük işler.',26)
    # Feed paper, conveyor, drive wheels, and four deliberately physical modules.
    y=597
    d.rounded_rectangle((48,y,1232,y+57),radius=28,fill=INK)
    for x in range(76,1230,30):
        offset=(t*30)%30
        line(d,[(x-offset,y+10),(x-offset+10,y+47)],PAPER,2)
    for x in [94,242,390,538,686,834,982,1186]:
        d.ellipse((x-12,y+17,x+12,y+41),fill=PAPER,outline=GRAY,width=2)
    for x,label,num in [(250,'ANDROID','01'),(455,'WEB','02'),(660,'BACKEND','03'),(865,'AI','04')]:
        d.rectangle((x,439,x+175,590),fill=WHITE,outline=INK,width=3)
        d.rectangle((x,439,x+175,475),fill=INK)
        txt(d,(x+12,446),label,21,PAPER,True)
        txt(d,(x+14,486),num,18,ORANGE,True)
        gear(d,x+91,537,29,t*1.3+(x/100))
        for sx in [x+8,x+167]:
            d.ellipse((sx-2,581,sx+2,585),fill=INK)
        # The machines share a very unnecessary overhead plumbing system.
        line(d,[(x+87,439),(x+87,412),(1123,412),(1123,474)],INK,4)
        d.ellipse((x+82,407,x+92,417),fill=ORANGE,outline=INK,width=2)
    # Giant lever and little absurd output.
    gear(d,136,535,38,-t)
    angle=-0.8+0.15*math.sin(t*math.tau/3)
    end=(136+66*math.cos(angle),535+66*math.sin(angle))
    line(d,[(136,535),end],INK,8);d.ellipse((end[0]-10,end[1]-10,end[0]+10,end[1]+10),fill=ORANGE,outline=INK,width=3)
    txt(d,(76,680),'GİRDİ: "UFAK Bİ’ İŞ"',17,mono=True)
    d.rectangle((1082,480,1201,519),fill=ORANGE,outline=INK,width=3)
    txt(d,(1095,489),'TAMAM',20,WHITE)
    # A tiny finished button moves down the final belt; a new one always follows.
    u=(t%4)/4
    bx=1061+130*u;by=565+min(u*4,1)*26
    d.rounded_rectangle((bx,by,bx+43,by+22),radius=6,fill=ORANGE,outline=PAPER,width=2)
    for k in range(3):
        sx=1112+k*12;sy=461-((t*18+k*12)%36)
        line(d,[(sx,sy),(sx+4,sy-6)],ORANGE,2)
    txt(d,(1010,680),'ÇIKTI: BİR BUTON.',17,mono=True)
    line(d,[(48,725),(1232,725)],width=2)
    txt(d,(48,740),'ANDROID  /  WEB  /  BACKEND  /  YAPAY ZEKA',16,mono=True)
    txt(d,(1040,740),'İŞ DEVAM EDİYOR.',15,ORANGE,True)
    return im

def project(number,title,description,stack,kind):
    im=Image.new('RGB',(620,302),PAPER);d=ImageDraw.Draw(im)
    d.rectangle((2,2,617,299),outline=INK,width=3)
    d.rectangle((3,3,78,298),fill=INK)
    txt(d,(18,22),number,30,PAPER,True)
    for y in range(85,275,20):line(d,[(24,y),(55,y)],GRAY,1)
    txt(d,(100,22),'ATÖLYEDEN ÇIKANLAR',17,mono=True)
    txt(d,(99,62),title,53)
    for i,row in enumerate(description):txt(d,(101,137+i*33),row,25)
    line(d,[(101,230),(588,230)],width=2)
    txt(d,(101,250),stack,17,mono=True)
    # Unique little part drawings instead of stock logos.
    x=553;y=74
    if kind=='truck':
        d.rectangle((x-29,y,x+6,y+30),outline=INK,width=3);line(d,[(x+7,y+9),(x+24,y+9),(x+34,y+24),(x+34,y+32),(x+6,y+32)],width=3)
        for cx in [x-15,x+22]:d.ellipse((cx-6,y+25,cx+6,y+37),fill=ORANGE,outline=INK,width=2)
    elif kind=='flow':
        for yy in [y,y+18,y+36]:d.rectangle((x-30,yy,x-4,yy+10),fill=ORANGE)
        line(d,[(x+9,y+3),(x+29,y+3),(x+29,y+41),(x+9,y+41)],width=3)
    elif kind=='room':
        d.rectangle((x-24,y-1,x+20,y+46),outline=INK,width=3);d.ellipse((x+6,y+22,x+12,y+28),fill=ORANGE)
        d.rectangle((x-37,y+11,x-29,y+25),fill=ORANGE)
    elif kind=='photo':
        d.rectangle((x-32,y,x+29,y+44),outline=INK,width=3);line(d,[(x-28,y+39),(x-10,y+17),(x+6,y+34),(x+17,y+23),(x+26,y+39)],width=3)
        d.ellipse((x+11,y+6,x+20,y+15),fill=ORANGE)
    elif kind=='tea':
        d.arc((x-29,y+10,x+16,y+42),0,180,fill=INK,width=3)
        line(d,[(x-29,y+26),(x-29,y+8),(x+16,y+8),(x+16,y+26)],width=3)
        d.arc((x+11,y+10,x+30,y+27),260,100,fill=ORANGE,width=3)
        line(d,[(x-35,y+43),(x+25,y+43)],INK,3)
    else:
        for xx in [x-29,x+2]:d.rectangle((xx,y,xx+28,y+43),outline=INK,width=3)
        for yy in [y+12,y+23,y+34]:line(d,[(x-23,yy),(x-7,yy)],ORANGE,2)
    return im

def main():
    hero().save(OUT/'workshop-still.png',optimize=True)
    # One shared palette keeps edges stable and the animation inexpensive.
    palette=hero().quantize(colors=24)
    frames=[hero(i/10).quantize(palette=palette,dither=Image.Dither.NONE) for i in range(120)]
    frames[0].save(OUT/'one-button-workshop.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True,disposal=1)
    projects=[('01','Yükio',['Mesaj kalabalığından','yük ilanına.'],'KOTLIN / COMPOSE / ROOM','truck'),('02','TekinFlow',['Siparişten teslimata,','aynı işin peşinde.'],'COMPOSE / REACT / KTOR','flow'),('03','RoomFlow',['"Bu oda boş mu?"','Ekrana bak.'],'ANDROID / NODE / DOCKER','room'),('04','Ultra HD',['Eski fotoğraflara','bir şans daha.'],'PYTHON / PYTORCH / GRADIO','photo'),('05','NoteFlow',['Defter açık.','Fikirler dağınık olabilir.'],'JAVASCRIPT / NODE / SQLITE','notes'),('06',"Bi’ çay?",['İş için de olur,','kod muhabbeti için de.'],'MUHAMMET-TEKIN.DEV','tea')]
    for p in projects:project(*p).save(OUT/f'project-{p[0]}.png',optimize=True)
    print('Generated GIF bytes:',(OUT/'one-button-workshop.gif').stat().st_size)
if __name__=='__main__':main()
