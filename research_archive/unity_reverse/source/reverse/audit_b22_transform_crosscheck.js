"use strict";

const fs = require("fs");

function squaredDistance(a, b) {
  return a.reduce((sum, value, index) => sum + (value - b[index]) ** 2, 0);
}

function compare(local, unity) {
  const remaining = unity.map((contact, index) => ({ contact, index }));
  const pairs = local.map((contact, localIndex) => {
    remaining.sort((a, b) => squaredDistance(contact.point, a.contact.point) - squaredDistance(contact.point, b.contact.point));
    const match = remaining.shift();
    return {
      localIndex,
      unityIndex: match.index,
      pointDistance: Math.sqrt(squaredDistance(contact.point, match.contact.point)),
      normalDistance: Math.sqrt(squaredDistance(contact.normal, match.contact.normal)),
      separationDelta: contact.separation - match.contact.separation,
    };
  });
  return {
    pairs,
    maxPointDistance: Math.max(...pairs.map((pair) => pair.pointDistance), 0),
    maxNormalDistance: Math.max(...pairs.map((pair) => pair.normalDistance), 0),
    maxSeparationDelta: Math.max(...pairs.map((pair) => Math.abs(pair.separationDelta)), 0),
  };
}

async function main() {
  const [sceneJs, b21AuditPath, b22ScenePath, outputPath] = process.argv.slice(2);
  if (!sceneJs || !b21AuditPath || !b22ScenePath || !outputPath) {
    throw new Error("usage: node audit_b22_transform_crosscheck.js <scene.js> <b21-audit.json> <b22-scene.json> <output.json>");
  }
  const b21 = JSON.parse(fs.readFileSync(b21AuditPath, "utf8"));
  const b22 = JSON.parse(fs.readFileSync(b22ScenePath, "utf8"));
  const unity = b21.unity;
  const local = b22.firstContact.narrowphase;

  const createModule = require(sceneJs);
  const module = await createModule({ noInitialRun: false });
  module.cwrap("a19_init", null, [])();
  const direct = module.cwrap("b21_direct_pcm", null, new Array(15).fill("number"));
  const getContacts = module.cwrap("b21_get_direct_contacts", null, ["number"]);
  const ptr = module._malloc((1 + 64 * 7) * 4);

  const invoke = (name, transform0, transform1) => {
    direct(...transform0.p, ...transform0.q, ...transform1.p, ...transform1.q, 0);
    getContacts(ptr);
    const values = module.HEAPF32.subarray(ptr >> 2, (ptr >> 2) + 1 + 64 * 7);
    const contactCount = values[0];
    const contacts = [];
    for (let index = 0; index < contactCount; index += 1) {
      const base = 1 + index * 7;
      contacts.push({
        point: Array.from(values.slice(base, base + 3)),
        normal: Array.from(values.slice(base + 3, base + 6)),
        separation: values[base + 6],
      });
    }
    return { name, transform0, transform1, contactCount, contacts, comparison: compare(contacts, unity.contacts) };
  };

  const result = {
    schema: "b22_transform_crosscheck_v1",
    policy: "Direct PCM only. It changes no PxScene state and uses no Unity cache or feature bytes.",
    unityTransforms: { active: unity.transform0, target: unity.transform1 },
    localSceneTransforms: { active: local.transform0, target: local.transform1 },
    cases: [
      invoke("unity_active_unity_target", unity.transform0, unity.transform1),
      invoke("local_active_local_target", local.transform0, local.transform1),
      invoke("unity_active_local_target", unity.transform0, local.transform1),
      invoke("local_active_unity_target", local.transform0, unity.transform1),
    ],
  };
  module._free(ptr);
  fs.writeFileSync(outputPath, `${JSON.stringify(result, null, 2)}\n`);
  process.stdout.write(`${JSON.stringify(result.cases.map((entry) => ({
    name: entry.name,
    contactCount: entry.contactCount,
    maxPointDistance: entry.comparison.maxPointDistance,
    maxNormalDistance: entry.comparison.maxNormalDistance,
    maxSeparationDelta: entry.comparison.maxSeparationDelta,
  })))}\n`);
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exitCode = 1;
});
