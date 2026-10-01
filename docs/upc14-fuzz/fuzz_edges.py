import sys, unicodedata
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else 'prototype')  # path to prototype/ of commit 7a2aa38
import upc14v2 as g, upc14v2_sandhi as sd, upc14v2_script as sc
S=g.SOUNDS
def show(name, seq):
    out=[]
    for s in ('iast','devanagari','cyrillic'):
        try:
            t=sc.encode_text(seq,s); back=sc.decode_text(t,s)
            out.append(f"{s}: {t!r} -> {'OK' if back==seq else 'LOSSY (decodes to a different sequence)'}")
        except Exception as e:
            out.append(f"{s}: RAISES {type(e).__name__}")
    print(f"[{name}]"," | ".join(out))
# codes outside the 59
show('pluta a', (g.Vertex(g.unpack(S['a']).place,0,g.unpack(S['a']).aperture,g.PLUTA,0,0).code,))
show('pluta i', (g.Vertex(g.unpack(S['i']).place,0,g.unpack(S['i']).aperture,g.PLUTA,g.unpack(S['i']).voice,0).code,))
show('nasal y (8.4.45 y~)', (sd.code_of('y') if False else g.Vertex(g.unpack(S['y']).place,1,g.unpack(S['y']).aperture,g.unpack(S['y']).length,g.unpack(S['y']).voice,g.unpack(S['y']).asp).code,))
show('nasal v', (g.Vertex(g.unpack(S['v']).place,1,g.unpack(S['v']).aperture,g.unpack(S['v']).length,g.unpack(S['v']).voice,g.unpack(S['v']).asp).code,))
show('nasal l', (g.Vertex(g.unpack(S['l']).place,1,g.unpack(S['l']).aperture,g.unpack(S['l']).length,g.unpack(S['l']).voice,g.unpack(S['l']).asp).code,))
try:
    longx=g.e_long(S['x']); show('long ḷ (e_long(ḷ))',(longx,))
except Exception as e: print('long ḷ: e_long raises',e)
v=g.unpack(S['e']); 
try: show('short e (length 0)',(g.Vertex(v.place,0,v.aperture,g.SHORT,v.voice,v.asp).code,))
except Exception as e: print('short e: Vertex/code raises',type(e).__name__,e)
print('--- decoder acceptance of non-canonical strings')
def dec(t,s):
    try: r=sc.decode_text(t,s); return [ (sc.to_iast(c)) for c in r]
    except Exception as e: return f"RAISES {type(e).__name__}"
for t,s in [('k·h','iast'),('kh','iast'),('·k','iast'),('k·','iast'),('k··h','iast'),('k·a','iast'),('ka','iast'),
            ('ḳ','iast'),('ṛ','iast'),('ṝ','iast'),('ã','iast'),('ã','iast'),('ā̃','iast'),('ã̄','iast'),
            ('क्अ','devanagari'),('क','devanagari'),('कअ','devanagari'),('क्‍ह','devanagari'),('क्‌ह','devanagari'),('क््','devanagari'),('कँ','devanagari'),('अँ','devanagari'),('आँ','devanagari'),('कँा','devanagari'),('क़','devanagari'),('ॐ','devanagari'),('कः','devanagari'),
            ('к·х','cyrillic'),('кх','cyrillic'),('ш','cyrillic'),('ш́','cyrillic'),('ш́','cyrillic'),('a','cyrillic'),('ќ','cyrillic')]:
    print(f"{s:10s} {t!r:22s} -> {dec(t,s)}")
# Latin look-alike in Cyrillic and vice versa
print('cyrillic with Latin a:', dec('а','cyrillic'), dec('a','cyrillic'))
print('iast with Cyrillic а:', dec('а','iast'))
