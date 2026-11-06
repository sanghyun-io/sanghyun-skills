"""흐름 데이터 JSON 을 검증하고 assets/template.html 에 넣어 HTML 을 만든다.

usage: python render.py <data.json> <out.html>
       python render.py --self-test
"""
import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parents[1] / "assets" / "template.html"
KINDS = {"screen", "button", "system", "end", "fail"}
EDGE_TYPES = {"fwd", "err", "back"}
AUTH_LEVELS = {"none", "cond", "login", "admin", "unknown"}
TONES = {"green", "orange", "red", "blue", "purple", "gray"}


def validate(data):
    errors = []
    if not isinstance(data.get("title"), str) or not data["title"]:
        errors.append("title 이 비어 있다")
    cols = data.get("cols")
    if not isinstance(cols, list) or not cols:
        return errors + ["cols 가 비어 있다"]
    ids = set()
    for ci, col in enumerate(cols):
        for n in col.get("nodes", []):
            nid = n.get("id")
            where = f"cols[{ci}] node {nid!r}"
            if not nid or nid in ids:
                errors.append(f"{where}: id 가 없거나 중복")
            ids.add(nid)
            if n.get("kind") not in KINDS:
                errors.append(f"{where}: kind 는 {sorted(KINDS)} 중 하나")
            if not n.get("title"):
                errors.append(f"{where}: title 없음")
            for k, c in enumerate(n.get("calls", [])):
                cw = f"{where} calls[{k}]"
                for f in ("m", "p", "fe", "be"):
                    if not c.get(f):
                        errors.append(f"{cw}: {f} 없음")
                level = (c.get("auth") or {}).get("level")
                if level not in AUTH_LEVELS:
                    errors.append(f"{cw}: auth.level 은 {sorted(AUTH_LEVELS)} 중 하나")
                for t in c.get("tags", []):
                    if t.get("tone", "gray") not in TONES:
                        errors.append(f"{cw}: tag tone 은 {sorted(TONES)} 중 하나")
    for i, e in enumerate(data.get("edges", [])):
        for end in ("from", "to"):
            if e.get(end) not in ids:
                errors.append(f"edges[{i}]: {end}={e.get(end)!r} 노드가 없다")
        if e.get("type", "fwd") not in EDGE_TYPES:
            errors.append(f"edges[{i}]: type 은 {sorted(EDGE_TYPES)} 중 하나")
    linked = {e.get("from") for e in data.get("edges", [])} | {e.get("to") for e in data.get("edges", [])}
    orphans = sorted(ids - linked)
    if orphans and len(ids) > 1:
        errors.append(f"화살표가 하나도 없는 노드: {orphans}")
    return errors


def render(data):
    html = TEMPLATE.read_text(encoding="utf-8")
    marker = "/*__DATA__*/null"
    assert marker in html, "template 에 데이터 자리표시자가 없다"
    # </script> 가 데이터에 들어 있어도 스크립트가 끊기지 않게 한다
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return html.replace(marker, payload)


def main(argv):
    if argv[1:] == ["--self-test"]:
        ok = {"title": "t", "cols": [{"title": "A", "nodes": [
            {"id": "a", "kind": "screen", "title": "A", "calls": [
                {"m": "GET", "p": "/x", "fe": "f:1", "be": "b:1", "auth": {"level": "none"}}]},
            {"id": "b", "kind": "end", "title": "B"}]}],
            "edges": [{"from": "a", "to": "b", "label": "</script>"}]}
        assert validate(ok) == [], validate(ok)
        assert "<\\/script>" in render(ok)
        bad = {"title": "t", "cols": [{"title": "A", "nodes": [{"id": "a", "kind": "x", "title": "A"}]}],
               "edges": [{"from": "a", "to": "zz"}]}
        errs = validate(bad)
        assert any("kind" in e for e in errs) and any("zz" in e for e in errs), errs
        print("self-test ok")
        return 0
    if len(argv) != 3:
        print(__doc__)
        return 2
    data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        print("데이터 오류:", *errors, sep="\n- ")
        return 1
    out = Path(argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(data), encoding="utf-8")
    calls = sum(len(n.get("calls", [])) for c in data["cols"] for n in c["nodes"])
    print(f"wrote {out} (cols={len(data['cols'])}, calls={calls}, edges={len(data.get('edges', []))})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
