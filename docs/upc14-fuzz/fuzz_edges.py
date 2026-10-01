import sys, random, itertools, unicodedata
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else 'prototype')  # prototype/ of stage 2 (IAST keys)
import upc14v2 as g, upc14v2_sandhi as sd, upc14v2_script as sc
S=g.SOUNDS
base=[S[k] for k in S]; longs=[g.e_long(S[k]) for k in ('a','i','u','ṛ')]
nas=[g.e_nasal(c) for c in base if g.unpack(c).aperture>=g.VOWEL]; lnas=[g.e_nasal(c) for c in longs]
extra=[sd.code_of(x) for x in ('ỹ','ṽ','l̃')]
plut=[g.e_long(g.e_long(S[k])) for k in ('a','i','u','ṛ','ḷ')]+[g.e_long(S[k]) for k in ('e','o','ai','au')]
plut+= [g.e_nasal(c) for c in plut]
sym=list(dict.fromkeys(base+longs+nas+lnas+extra+plut)); print('symbols',len(sym))
scripts=('iast','devanagari','cyrillic')
# (a) exhaustive length 1-3
for s in scripts:
    seen={}; bad=coll=0
    for L in (1,2):
        for seq in itertools.product(sym,repeat=L):
            t=sc.encode_text(seq,s)
            if sc.decode_text(t,s)!=seq: bad+=1
            if t in seen: coll+=1
            seen[t]=seq
    print('exhaustive len1-2',s,'roundtrip failures',bad,'collisions',coll,'strings',len(seen))
# (b) unspellable codes
def tryraise(name,code):
    r=[]
    for s in scripts:
        try: sc.encode_text((code,),s); r.append('NO ERROR')
        except Exception as e: r.append(type(e).__name__)
    print(name,r)
v=g.unpack(S['ḷ']); tryraise('long ḷ',g.e_long(S['ḷ']))
ve=g.unpack(S['e']); tryraise('short e',g.Vertex(ve.place,0,ve.aperture,g.SHORT,ve.voice,ve.asp).code)
vr=g.unpack(S['r']); tryraise('nasal r',g.Vertex(vr.place,1,vr.aperture,vr.length,vr.voice,vr.asp).code)
print('pluta i round trip:',[sc.decode_text(sc.encode_text((g.e_long(g.e_long(S['i'])),),sx),sx)==(g.e_long(g.e_long(S['i'])),) for sx in scripts])  # spelled since the pluta codec
# (c) strict decoder
cases=[('k·h','iast'),('·k','iast'),('k·','iast'),('k··h','iast'),('k·a','iast'),('क्अ','devanagari'),('к·г','cyrillic'),('кг','cyrillic'),('к·ґ','cyrillic')]
for t,s in cases:
    out=[]
    for strict in (True,False):
        try: out.append([sc.to_iast(c) for c in sc.decode_text(t,s,strict=strict)])
        except Exception as e: out.append(type(e).__name__)
    print(f"{s:10s} {t!r:10s} strict={out[0]} | non-strict={out[1]}")
# (d) bijection on accepted strings: random strings, strict decode -> if accepted then encode == NFC(text)
random.seed(1001)
for s in scripts:
    toks=[sc.encode_text((c,),s) for c in sym]+['·',' ','‍','‌','|','̃','̄','̣']
    acc=viol=0
    for _ in range(100000):
        text=''.join(random.choice(toks) for _ in range(random.randint(1,7)))
        try: seq=sc.decode_text(text,s)
        except Exception: continue
        acc+=1
        if sc.encode_text(seq,s)!=unicodedata.normalize('NFC',text): viol+=1
    print('random strings',s,'accepted',acc,'strict-bijection violations',viol)
