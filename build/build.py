import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import GHOSTS, HOSTS, GAME, STORY, MISC, SRC
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
keep = ["id","w","lat","lon","name","short","year","end","place","status","st","src","diary","why","found","now","fun","q","o","a","ex","game"]
ghosts = [{k: g[k] for k in keep if k in g} for g in GHOSTS]
no3d = [g["id"] for g in GHOSTS if not os.path.exists(os.path.join(ROOT, "img/3d", g["id"] + ".webp"))]
data = dict(ghosts=ghosts, hosts=HOSTS, game=GAME, story=STORY, misc={k: v[2] for k, v in MISC.items()}, sources=SRC, no3d=no3d, photoAI=['kepler'])
t = open(os.path.join(ROOT, "build/template.html")).read()
assert "/*DATA*/" in t
out = t.replace("/*DATA*/", json.dumps(data, ensure_ascii=False))
open(os.path.join(ROOT, "index.html"), "w").write(out)
print("built", len(out), "bytes; no3d:", no3d)
