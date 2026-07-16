"use strict";

const fs = require("fs");

function squaredDistance(a, b) {
  return a.reduce((sum, value, index) => sum + (value - b[index]) ** 2, 0);
}

function readUnityFirstPcm(eventsPath) {
  for (const line of fs.readFileSync(eventsPath, "utf8").split(/\r?\n/)) {
    if (!line) continue;
    const event = JSON.parse(line);
    const data = event.data;
    if (event.type !== "physx.native.after" || data?.hook?.name !== "PxcPCMContactConvexConvex") continue;
    const dump = data.extraDumps?.[0];
    const contacts = dump?.contactBuffer?.decoded?.contactsPreview;
    const transform0 = dump?.transform0?.decoded;
    const transform1 = dump?.transform1?.decoded;
    if (transform0 && transform1 && Array.isArray(contacts)) {
      return { callIndex: data.callIndex, transform0, transform1, contacts };
    }
  }
  throw new Error("missing captured Unity convex-convex PCM");
}

function readContacts(module, getter, ptr) {
  getter(ptr);
  const data = module.HEAPF32.subarray(ptr >> 2, (ptr >> 2) + 1 + 64 * 7);
  const count = data[0];
  const contacts = [];
  for (let index = 0; index < count; index += 1) {
    const base = 1 + index * 7;
    contacts.push({
      point: Array.from(data.slice(base, base + 3)),
      normal: Array.from(data.slice(base + 3, base + 6)),
      separation: data[base + 6],
    });
  }
  return contacts;
}

function compare(local, unity) {
  const remaining = unity.map((contact, index) => ({ contact, index }));
  const pairs = local.map((contact, localIndex) => {
    remaining.sort((a, b) => squaredDistance(contact.point, a.contact.point) - squaredDistance(contact.point, b.contact.point));
    const match = remaining.shift();
    const pointDistance = Math.sqrt(squaredDistance(contact.point, match.contact.point));
    const normalDistance = Math.sqrt(squaredDistance(contact.normal, match.contact.normal));
    const separationDelta = contact.separation - match.contact.separation;
    return { localIndex, unityIndex: match.index, pointDistance, normalDistance, separationDelta, local, unity: match.contact };
  });
  return {
    pairs,
    maxPointDistance: Math.max(...pairs.map((pair) => pair.pointDistance), 0),
    maxNormalDistance: Math.max(...pairs.map((pair) => pair.normalDistance), 0),
    maxSeparationDelta: Math.max(...pairs.map((pair) => Math.abs(pair.separationDelta)), 0),
  };
}

async function main() {
  const [sceneJs, eventsPath, outputPath] = process.argv.slice(2);
  if (!sceneJs || !eventsPath || !outputPath) {
    throw new Error("usage: node audit_b21_wasm_direct_pcm.js <b21.js> <events.jsonl> <output.json>");
  }
  const unity = readUnityFirstPcm(eventsPath);
  const createModule = require(sceneJs);
  const module = await createModule({ noInitialRun: false });
  module.cwrap("a19_init", null, [])();
  const direct = module.cwrap("b21_direct_pcm", null, [
    "number", "number", "number", "number", "number", "number", "number",
    "number", "number", "number", "number", "number", "number", "number", "number",
  ]);
  const getContacts = module.cwrap("b21_get_direct_contacts", null, ["number"]);
  const ptr = module._malloc((1 + 64 * 7) * 4);
  const invoke = (featureSeed) => {
    direct(...unity.transform0.p, ...unity.transform0.q, ...unity.transform1.p, ...unity.transform1.q, featureSeed);
    const contacts = readContacts(module, getContacts, ptr);
    return { featureSeed: Boolean(featureSeed), contactCount: contacts.length, contacts, comparison: compare(contacts, unity.contacts) };
  };
  const fresh = invoke(0);
  const seeded = invoke(1);
  module._free(ptr);
  const result = {
    schema: "b21_wasm_direct_pcm_audit_v1",
    policy: "No PxScene, manager, cache from Unity, or actor lifecycle participates. Both calls use Unity's captured direct PCM transforms and the byte-validated local runtime hull.",
    unity: { callIndex: unity.callIndex, contactCount: unity.contacts.length, transform0: unity.transform0, transform1: unity.transform1, contacts: unity.contacts },
    wasmDirect: { fresh, unityFeatureSeedDiagnostic: seeded },
    discriminator: {
      freshMatchesUnity: fresh.contactCount === unity.contacts.length && fresh.comparison.maxPointDistance <= 5.960464477539063e-8 && fresh.comparison.maxNormalDistance <= 5.960464477539063e-8 && fresh.comparison.maxSeparationDelta <= 5.960464477539063e-8,
      seededMatchesUnity: seeded.contactCount === unity.contacts.length && seeded.comparison.maxPointDistance <= 5.960464477539063e-8 && seeded.comparison.maxNormalDistance <= 5.960464477539063e-8 && seeded.comparison.maxSeparationDelta <= 5.960464477539063e-8,
    },
  };
  fs.writeFileSync(outputPath, `${JSON.stringify(result, null, 2)}\n`);
  console.log(JSON.stringify(result.discriminator));
}

main().catch((error) => { process.stderr.write(`${error.stack || error}\n`); process.exitCode = 1; });
