import sys, random, itertools, unicodedata
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else 'prototype')  # prototype/ of stage 2 (IAST keys)
import upc14v2 as g, upc14v2_sandhi as sd, upc14v2_script as sc
S=g.SOUNDS
# the 59 symbols of the coordinator: 42 sounds + long ā ī ū ṝ + nasal vowels + long nasal vowels
base=[S[k] for k in S]
longs=[g.e_long(S[k]) for k in ('a','i','u','ṛ')]
nas=[g.e_nasal(c) for c in base if g.unpack(c).aperture>=g.VOWEL]
lnas=[g.e_nasal(c) for c in longs]
extra=[sd.code_of(x) for x in ('ỹ','ṽ','l̃')]
plut=[g.e_long(g.e_long(S[k])) for k in ('a','i','u','ṛ','ḷ')]+[g.e_long(S[k]) for k in ('e','o','ai','au')]
plut+= [g.e_nasal(c) for c in plut]
sym=list(dict.fromkeys(base+longs+nas+lnas+extra+plut))
print('symbols',len(sym))
scripts=('iast','devanagari','cyrillic')
random.seed(20261001)
res={s:{'roundtrip_fail':0,'n':0} for s in scripts}
ex=[]
for s in scripts:
    for _ in range(40000):
        L=random.randint(4,14); seq=tuple(random.choice(sym) for _ in range(L))
        try:
            t=sc.encode_text(seq,s); back=sc.decode_text(t,s)
        except Exception as e:
            res[s]['roundtrip_fail']+=1; ex.append((s,'EXC',str(e)[:60])); continue
        res[s]['n']+=1
        if back!=seq: res[s]['roundtrip_fail']+=1; ex.append((s,'MISMATCH',t))
print('random len4-14:',res, ex[:3])
# injectivity: encode distinct random sequences, look for equal strings
for s in scripts:
    seen={}; coll=0
    for _ in range(60000):
        L=random.randint(1,6); seq=tuple(random.choice(sym) for _ in range(L))
        t=sc.encode_text(seq,s)
        if t in seen and seen[t]!=seq: coll+=1; ex.append((s,'COLLISION',t,seen[t],seq))
        seen[t]=seq
    print('collisions',s,coll)
# transcode round trips between all script pairs
bad=0
for _ in range(20000):
    L=random.randint(1,10); seq=tuple(random.choice(sym) for _ in range(L))
    for a in scripts:
        for b in scripts:
            t=sc.encode_text(seq,a)
            if sc.decode_text(sc.transcode(t,a,b),b)!=seq: bad+=1
print('transcode failures',bad)
