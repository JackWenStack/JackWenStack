"""Generate the original JW identity and responsive profile artwork. Stdlib only."""
from html import escape
from pathlib import Path
from profile_brand import INK, WHITE, BLUE, MUTED, J, W, polygon, mark

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
FONT = 'Arial, Helvetica, sans-serif'
# Original chamfered lettering; paths keep the name identical across platforms.
LETTERS = {
 'J': (94,'M0 0H94V102L66 130H26L0 104V76H26V92L38 104H54L68 90V26H0Z'),
 'A': (104,'M0 130L38 0H66L104 130H78L71 106H31L24 130ZM39 80H63L51 36Z'),
 'C': (98,'M28 0H98V26H38L26 38V92L38 104H98V130H28L0 102V28Z'),
 'K': (109,'M0 0H26V51L73 0H107L52 64L109 130H75L26 78V130H0Z'),
 'W': (138,'M0 0H27L43 88L58 36H80L96 88L111 0H138L110 130H84L69 81L54 130H28Z'),
 'E': (96,'M0 0H96V26H26V52H85V78H26V104H96V130H0Z'),
 'N': (106,'M0 130V0H25L80 85V0H106V130H81L26 45V130Z'),
}


def text(x,y,value,size=20,color=WHITE,weight=400,spacing=0):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}">{escape(value)}</text>'


def word(value,x,y,scale=1,color=WHITE):
    result=[];offset=0
    for letter in value:
        if letter==' ':offset+=48;continue
        width,path=LETTERS[letter]
        result.append(f'<path transform="translate({offset})" d="{path}" fill-rule="evenodd"/>')
        offset+=width+14
    return f'<g transform="translate({x} {y}) scale({scale})" fill="{color}">'+''.join(result)+'</g>'


def sculpture(x,y,scale):
    def project(p):
        u,v=p
        return (u*.96+v*.22,v*.94-u*.19)
    result=[]
    for outline in (J,W):
        face=[project(p) for p in outline]
        back=[(u+29,v+36) for u,v in face]
        result.append(polygon(back,fill='#162845',stroke='#37619a',stroke_width='.8'))
        for index,a in enumerate(face):
            b=face[(index+1)%len(face)]
            dx,dy=b[0]-a[0],b[1]-a[1]
            if dx*36-dy*29>0:
                result.append(polygon([a,b,(b[0]+29,b[1]+36),(a[0]+29,a[1]+36)],fill='url(#edge)',stroke='#49617f',stroke_width='.45'))
        result.append(polygon(face,fill='url(#silver)',stroke='#e9f1ff',stroke_width='1.2',stroke_linejoin='round'))
    return f'<g transform="translate({x} {y}) scale({scale})">'+''.join(result)+'</g>'


def svg(width,height,title,description,body,defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>{defs}{body}</svg>\n')


def hero(mobile=False):
    width,height=(640,952) if mobile else (1200,780)
    body=f'<rect width="{width}" height="{height}" rx="4" fill="{INK}"/>'
    defs='''<defs><linearGradient id="silver" x1="0" y1="0" x2=".8" y2="1" gradientUnits="objectBoundingBox"><stop stop-color="#f5f8ff"/><stop offset=".27" stop-color="#aebdce"/><stop offset=".43" stop-color="#f7faff"/><stop offset=".49" stop-color="#8c9fb5"/><stop offset=".76" stop-color="#d6e0ec"/><stop offset="1" stop-color="#70859e"/></linearGradient><linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#778ca8"/><stop offset=".35" stop-color="#18283f"/><stop offset=".72" stop-color="#3263a4"/><stop offset="1" stop-color="#83b5ff"/></linearGradient><radialGradient id="floor"><stop stop-color="#3277e8" stop-opacity=".2"/><stop offset="1" stop-color="#3277e8" stop-opacity="0"/></radialGradient></defs>'''
    if mobile:
        body+=text(36,51,'JACKWENSTACK',24,MUTED,400,2)
        body+='<path d="M36 82H604" stroke="#263245"/>'
        body+='<ellipse cx="338" cy="379" rx="272" ry="60" fill="url(#floor)"/>'
        body+=sculpture(62,187,1.02)
        body+=word('JACK',36,454,1.28)
        body+=word('WEN',36,650,1.55)
        body+=text(39,913,'FULL-STACK DEVELOPER',27,MUTED,400,1)
    else:
        body+=text(56,56,'JACKWENSTACK',20,MUTED,400,2)
        body+=text(842,56,'Software, thoughtfully built.',20,MUTED)
        body+='<path d="M56 88H1144" stroke="#263245"/>'
        body+='<ellipse cx="660" cy="465" rx="360" ry="60" fill="url(#floor)"/>'
        body+=sculpture(285,218,1.22)
        body+=text(56,234,'Logic.',21,MUTED)
        body+=text(56,269,'Interface.',21,MUTED)
        body+=text(56,304,'Delivery.',21,MUTED)
        body+=word('JACK WEN',56,530,1.24)
        body+=text(60,736,'FULL-STACK DEVELOPER',21,MUTED,400,1.5)
        body+=text(931,736,'JAVA  /  VUE',21,BLUE,600,1.5)
    return svg(width,height,'Jack Wen — Digital craftsman & full-stack developer','A custom silver JW monogram and original chamfered Jack Wen lettering on a carbon-black canvas.',body,defs)


def practice(mobile=False):
    width,height=(640,644) if mobile else (1200,288)
    fg,muted,line='#171e2b','#536174','#cad3df'
    items=[('BUILD.','Backend systems','Java · Spring Boot','MySQL · Redis · Maven'),('CRAFT.','Frontend experience','Vue · TypeScript','JavaScript · Vite · HTML / CSS'),('SHIP.','Production delivery','Docker · Linux','Nginx · Git')]
    body=f'<rect width="{width}" height="{height}" rx="4" fill="#edf1f6"/>'
    for i,(title,caption,primary,secondary) in enumerate(items):
        if mobile:
            top=i*208
            body+=text(32,top+78,title,64,fg,700,-2)
            body+=text(34,top+128,primary,34,fg)
            body+=text(34,top+174,secondary,28,muted)
            if i<2:body+=f'<path d="M32 {top+204}H608" stroke="{line}"/>'
        else:
            left=[48,438,828][i]
            body+=text(left,51,caption,22,muted)
            body+=text(left-3,141,title,76,fg,700,-3)
            body+=text(left,198,primary,27,fg)
            body+=text(left,239,secondary,19 if i==1 else 22,muted)
            if i<2:body+=f'<path d="M{left+350} 36V246" stroke="{line}"/>'
    return svg(width,height,'Build systems. Craft interfaces. Ship software.','Backend: Java, Spring Boot, MySQL, Redis, Maven. Frontend: Vue, TypeScript, JavaScript, Vite, HTML and CSS. Delivery: Docker, Linux, Nginx and Git.',body)


def signoff(mobile=False):
    width,height=(640,200) if mobile else (1200,144)
    body=f'<rect width="{width}" height="{height}" rx="4" fill="{INK}"/>'
    if mobile:
        body+=mark(32,65,.16)
        body+=text(146,62,'Think clearly.',35,WHITE,700,-.5)
        body+=text(146,107,'Build deliberately.',35,WHITE,700,-.5)
        body+=text(148,161,'github.com/JackWenStack',25,MUTED)
    else:
        body+=mark(48,52,.21)
        body+=text(192,65,'Think clearly. Build deliberately.',34,WHITE,600,-.7)
        body+=text(194,104,'github.com/JackWenStack',20,MUTED)
        body+=text(1080,95,'↗',64,BLUE)
    return svg(width,height,'Think clearly. Build deliberately.','Jack Wen on GitHub.',body)


if __name__=='__main__':
    ASSETS.mkdir(exist_ok=True)
    assets={'hero.svg':hero(),'hero-mobile.svg':hero(True),'signoff.svg':signoff(),'signoff-mobile.svg':signoff(True)}
    for mobile in (False,True):
        name='practice'+('-mobile' if mobile else '')+'.svg'
        assets[name]=practice(mobile)
    for name,content in assets.items():
        (ASSETS/name).write_text(content,encoding='utf-8')
        print(f'{name}: {len(content.encode()):,} bytes')
