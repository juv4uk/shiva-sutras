#!/usr/bin/env python3
"""Statistics and sanity checks over the derived sutra edges (reads edges.tsv made by build_sutra_graph.py)."""
import collections, csv, sys, functools
edges=[tuple(r) for r in csv.reader(open(sys.argv[1]+"/edges.tsv",encoding="utf-8"),delimiter="\t")][1:]
def key(s): a,p,n=s.split("."); return (int(a),int(p),int(n))
by=collections.defaultdict(list)
for s,d,k,l in edges: by[k].append((s,d,l))
print("edges:",{k:len(v) for k,v in by.items()})
# anuvrtti
an=by["anuvrtti"]; srcs=collections.Counter(d for s,d,l in an); dsts={s for s,d,l in an}
print("sutras that inherit something:",len(dsts),"| most inherited-from:",[(s,c) for s,c in srcs.most_common(8)])
succ={}
for s,d,l in an: succ.setdefault(s,set()).add(d)
@functools.lru_cache(None)
def depth(s): return 1+max((depth(x) for x in succ.get(s,())),default=0) if succ.get(s) else 0
ds=sorted(((depth(s),s) for s in list(succ)),reverse=True)[:5]; print("longest anuvrtti chains (length, sutra):",ds)
bad=[(s,d) for s,d,l in an if key(d)>=key(s)]; print("anuvrtti edges pointing FORWARD (should be 0):",len(bad))
# adhikara
ad=by["adhikara"]; heads=collections.Counter(d for s,d,l in ad); print("adhikara heads:",len(heads),"| widest:",heads.most_common(5))
badad=[(s,d) for s,d,l in ad if key(d)>key(s)]; print("adhikara edges pointing forward:",len(badad))
# Kasika references
kr=by["kasika_ref"]; incoming=collections.Counter(d for s,d,l in kr); print("Kasika refs:",len(kr),"| most referenced:",incoming.most_common(8))
fl=collections.Counter(f for s,d,l in kr for f in (l.split(",") if l else []))
print("ref flags (same-sentence keywords):",dict(fl))
# apavada
ap=by["apavada"]; print("apavada edges resolved:",len(ap),"(explicit-ref",sum(1 for *_,l in ap if l.startswith("explicit")),", by name",sum(1 for *_,l in ap if l.startswith("name")),")")
un=[r for r in csv.reader(open(sys.argv[1]+"/apavada_unresolved.tsv",encoding="utf-8"),delimiter="\t")][1:]
print("sutras whose Kasika says `apavada` but no sutra could be resolved:",len(un))
print("examples in 6.1.77-113:",[(s,d) for s,d,l in ap if s.startswith("6.1.") and 77<=int(s.split('.')[2])<=113])
