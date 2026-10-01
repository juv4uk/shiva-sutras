import sys
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else 'prototype')  # path to prototype/ of commit 7a2aa38
import upc14v2 as g, upc14v2_sandhi as sd, upc14v2_script as sc
S=g.SOUNDS
def tryit(name,seq):
    out=[]
    for s in ('iast','devanagari','cyrillic'):
        try:
            t=sc.encode_text(seq,s); back=sc.decode_text(t,s)
            out.append(f"{s}:{t!r}->{'OK' if back==seq else 'LOSSY'}")
        except Exception as e: out.append(f"{s}:RAISES {type(e).__name__}")
    print(f"[{name}]",' | '.join(out))
pa=g.e_long(g.e_long(S['a'])); print('pluta a unpack:',g.unpack(pa)); tryit('pluta a (e_long twice)',(pa,))
pf=g.e_long(g.e_long(S['f'])); tryit('pluta ṛ',(pf,))
r=sd.final_stop('y','n'); print('final_stop(y,n) ->',r.left,r.right)
for lab in ('y~','v~','l~'):
    try: sd.code_of(lab); print('code_of',lab,'ok')
    except Exception as e: print('code_of',lab,'RAISES',type(e).__name__)
# invalid inputs
for bad in (0,-1,1<<14,'a',None,True):
    try: print('encode_text',repr(bad),'->',sc.encode_text((bad,),'iast'))
    except Exception as e: print('encode_text',repr(bad),'RAISES',type(e).__name__)
for bad in (None,b'k',123):
    try: print('decode_text',repr(bad),'->',sc.decode_text(bad,'iast'))
    except Exception as e: print('decode_text',repr(bad),'RAISES',type(e).__name__)
try: print(sc.decode_text('','iast'), repr(sc.encode_text((),'devanagari')))
except Exception as e: print('empty RAISES',e)
