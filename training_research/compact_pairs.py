"""Namespace-safe compact forward-input/reference association.

record_id is local to a source collection and is reused across compact files.
The authoritative pairing is the matching gzip stem and one-based row number.
Full request fingerprints resolve an external catalogue without using outcomes.
"""
from __future__ import annotations

import gzip
import hashlib
import itertools
import json


def request_fingerprint(request):
    stones = [{"index": int(s["index"]), "x": float(s["x"]), "y": float(s["y"]),
               "yaw": float(s.get("yaw", 0.))} for s in sorted(request["stones"], key=lambda s: s["index"])]
    payload = {"record_id": request.get("record_id"), "scene_key": request.get("scene_key"),
               "active_index": int(request["active_index"]), "stones": stones,
               "selection": request["selection"]}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def iter_pairs(data):
    for input_path in sorted(data.glob("*.inputs.jsonl.gz")):
        reference_path = input_path.with_name(input_path.name.replace(".inputs.", ".references."))
        with gzip.open(input_path, "rt", encoding="utf-8") as inputs, \
             gzip.open(reference_path, "rt", encoding="utf-8") as references:
            for line, (a, b) in enumerate(itertools.zip_longest(inputs, references), 1):
                if a is None or b is None:
                    raise ValueError("compact paired files have different lengths: "+input_path.name)
                request, reference = json.loads(a), json.loads(b)
                if request["record_id"] != reference["record_id"]:
                    raise ValueError("compact pair record_id differs: %s:%d" % (input_path.name, line))
                yield request, reference, {"input_file": input_path.name,
                                           "reference_file": reference_path.name, "line": line}


def references_for_requests(data, requests, *, seeds_only=False):
    wanted = {request_fingerprint(r) for r in requests}
    found = {}
    for request, reference, location in iter_pairs(data):
        key = request_fingerprint(request)
        if key in wanted and key not in found:
            # An exactly identical task can have several real forward witnesses.
            # Pick the first original paired witness in stable source-file order.
            found[key] = ({"physics_seed": reference["physics_seed"]} if seeds_only else dict(reference))
            found[key]["paired_location"] = location
    if set(found) != wanted:
        raise ValueError("catalog request has no exact original paired reference")
    return found
