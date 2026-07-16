"use strict";

const fs = require("fs");

function maxAbs(values) {
  return values.reduce((maximum, value) => Math.max(maximum, Math.abs(value)), 0);
}

function subtract(left, right) {
  return left.map((value, index) => value - right[index]);
}

function squaredDistance(left, right) {
  return left.reduce((sum, value, index) => sum + (value - right[index]) ** 2, 0);
}

function loadUnityPcm(eventsPath) {
  const candidates = [];
  for (const line of fs.readFileSync(eventsPath, "utf8").split(/\r?\n/)) {
    if (!line) continue;
    const event = JSON.parse(line);
    const data = event.data;
    if (event.type !== "physx.native.after" || data?.hook?.name !== "PxcPCMContactConvexConvex") continue;
    const dump = data.extraDumps?.[0];
    const contacts = dump?.contactBuffer?.decoded?.contactsPreview;
    const transform0 = dump?.transform0?.decoded;
    const transform1 = dump?.transform1?.decoded;
    if (!transform0 || !transform1 || !Array.isArray(contacts)) continue;
    candidates.push({ callIndex: data.callIndex, transform0, transform1, contacts });
  }
  if (!candidates.length) throw new Error("no captured Unity convex-convex PCM records");
  return candidates;
}

function pairContacts(localContacts, unityContacts) {
  const remaining = unityContacts.map((contact, index) => ({ contact, index }));
  return localContacts.map((local, localIndex) => {
    remaining.sort((left, right) => squaredDistance(local.point, left.contact.point) - squaredDistance(local.point, right.contact.point));
    const unity = remaining.shift();
    const pointDelta = subtract(local.point, unity.contact.point);
    const normalDelta = subtract(local.normal, unity.contact.normal);
    return {
      localIndex,
      unityIndex: unity.index,
      local,
      unity: unity.contact,
      pointDelta,
      pointDistance: Math.sqrt(squaredDistance(local.point, unity.contact.point)),
      normalDelta,
      normalDistance: Math.sqrt(squaredDistance(local.normal, unity.contact.normal)),
      separationDelta: local.separation - unity.contact.separation,
    };
  });
}

function main() {
  const [eventsPath, b20Path, outputPath] = process.argv.slice(2);
  if (!eventsPath || !b20Path || !outputPath) {
    throw new Error("usage: node audit_b20_same_run_contactbuffer.js <events.jsonl> <b20.json> <output.json>");
  }
  const b20 = JSON.parse(fs.readFileSync(b20Path, "utf8"));
  const local = b20.firstContact;
  if (!local?.narrowphase || !Array.isArray(local.contacts)) throw new Error("B20 result has no first narrowphase contact");

  const candidates = loadUnityPcm(eventsPath);
  const matching = candidates.map((unity) => {
    const positionError = squaredDistance(local.narrowphase.transform0.p, unity.transform0.p)
      + squaredDistance(local.narrowphase.transform1.p, unity.transform1.p);
    const quaternionError = squaredDistance(local.narrowphase.transform0.q, unity.transform0.q)
      + squaredDistance(local.narrowphase.transform1.q, unity.transform1.q);
    return { unity, score: positionError + quaternionError };
  }).sort((left, right) => left.score - right.score)[0].unity;

  const transform = {
    activePositionDelta: subtract(local.narrowphase.transform0.p, matching.transform0.p),
    activeQuaternionDelta: subtract(local.narrowphase.transform0.q, matching.transform0.q),
    targetPositionDelta: subtract(local.narrowphase.transform1.p, matching.transform1.p),
    targetQuaternionDelta: subtract(local.narrowphase.transform1.q, matching.transform1.q),
  };
  transform.maxPositionComponentDelta = maxAbs([...transform.activePositionDelta, ...transform.targetPositionDelta]);
  transform.maxQuaternionComponentDelta = maxAbs([...transform.activeQuaternionDelta, ...transform.targetQuaternionDelta]);

  const localPcmContacts = local.narrowphase.pcmContacts;
  if (!Array.isArray(localPcmContacts) || !localPcmContacts.length) {
    throw new Error("B20 narrowphase trace did not capture the raw PCM ContactBuffer");
  }
  const pairs = pairContacts(localPcmContacts, matching.contacts);
  const maxPointDistance = Math.max(...pairs.map((pair) => pair.pointDistance));
  const maxNormalDistance = Math.max(...pairs.map((pair) => pair.normalDistance));
  const maxSeparationDelta = Math.max(...pairs.map((pair) => Math.abs(pair.separationDelta)));
  const floatUlpAcceptance = maxPointDistance <= 5.960464477539063e-8
    && maxNormalDistance <= 5.960464477539063e-8
    && maxSeparationDelta <= 5.960464477539063e-8;

  const report = {
    schema: "b20_same_run_contactbuffer_audit_v1",
    policy: "Matches the nearest Unity PCM record by actual narrowphase transforms; neither Unity pose nor cache is injected into B20.",
    b20FirstContact: {
      role: local.role,
      contactCount: local.contactCount,
      tickSerial: local.tickSerial,
    },
    unityMatchedCall: matching.callIndex,
    unityContactCount: matching.contacts.length,
    transform,
    contactPairs: pairs,
    acceptance: {
      roleAndCountMatch: local.role === "active_to_target" && localPcmContacts.length === matching.contacts.length,
      transformNearMatch: transform.maxPositionComponentDelta <= 1e-4 && transform.maxQuaternionComponentDelta <= 1e-4,
      contactBufferFloatUlpMatch: floatUlpAcceptance,
      maxPointDistance,
      maxNormalDistance,
      maxSeparationDelta,
    },
  };
  fs.writeFileSync(outputPath, `${JSON.stringify(report, null, 2)}\n`);
  console.log(JSON.stringify(report.acceptance));
}

main();
