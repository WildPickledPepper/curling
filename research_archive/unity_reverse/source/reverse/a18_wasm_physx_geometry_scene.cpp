#include "PxPhysicsAPI.h"
#include "GuBigConvexData.h"
#include "GuConvexMesh.h"
#include "GuGeometryUnion.h"
#include "GuContactMethodImpl.h"
#include "geomutils/GuContactBuffer.h"
#include "pcm/GuPersistentContactManifold.h"
#include "pipeline/PxcNpWorkUnit.h"
#include "PxsTransformCache.h"
#include "PxsShapeSim.h"
#include "PxvGeometry.h"
#include "a18_wasm_scene_assets.generated.h"
#include <emscripten/emscripten.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <vector>

using namespace physx;

#ifndef A18_USE_LOCAL_RELEASE_HEIGHT
#define A18_USE_LOCAL_RELEASE_HEIGHT 0
#endif

class Allocator final : public PxAllocatorCallback {
public:
    void* allocate(size_t size, const char*, const char*, int) override {
        void* result = nullptr;
        return posix_memalign(&result, 16, size) == 0 ? result : nullptr;
    }
    void deallocate(void* pointer) override { std::free(pointer); }
};

class Errors final : public PxErrorCallback {
public:
    void reportError(PxErrorCode::Enum, const char* message, const char*, int) override {
        std::fprintf(stderr, "%s\n", message);
    }
};

class InlineDispatcher final : public PxCpuDispatcher {
public:
    void submitTask(PxBaseTask& task) override { task.run(); task.release(); }
    PxU32 getWorkerCount() const override { return 1; }
};

class MemoryOutput final : public PxOutputStream {
public:
    PxU32 write(const void* source, PxU32 count) override {
        const PxU8* bytes = static_cast<const PxU8*>(source);
        data.insert(data.end(), bytes, bytes + count);
        return count;
    }
    std::vector<PxU8> data;
};

class MemoryInput final : public PxInputData {
public:
    explicit MemoryInput(const std::vector<PxU8>& bytes) : data(bytes), offset(0) {}
    PxU32 read(void* destination, PxU32 count) override {
        const PxU32 available = getLength() - offset;
        const PxU32 copied = count < available ? count : available;
        std::memcpy(destination, data.data() + offset, copied);
        offset += copied;
        return copied;
    }
    PxU32 getLength() const override { return static_cast<PxU32>(data.size()); }
    void seek(PxU32 position) override { offset = position <= getLength() ? position : getLength(); }
    PxU32 tell() const override { return offset; }
private:
    const std::vector<PxU8>& data;
    PxU32 offset;
};

static Allocator gAllocator;
static Errors gErrors;
static InlineDispatcher gDispatcher;
static PxFoundation* gFoundation = nullptr;
static PxPhysics* gPhysics = nullptr;
static PxScene* gScene = nullptr;
static PxRigidDynamic* gStone = nullptr;
static PxRigidDynamic* gTarget = nullptr;
static PxShape* gStoneShape = nullptr;
static PxShape* gTargetShape = nullptr;
static PxConvexMesh* gStoneMesh = nullptr;
static PxMaterial* gStoneMaterial = nullptr;
static PxMaterial* gTargetMaterial = nullptr;
static PxU32 gB20ContactCount = 0;
static PxU32 gB20Role = 0;
static PxContactPairPoint gB20Points[16];
static PxU32 gB20PointCount = 0;
static const float kB20PcmCenterDistance = 0.30175f;
// Unity's released active and reset stationary stones share this serialized
// prefab-space quaternion basis. It is not a first-PCM pose injection.
static const PxQuat kB20PrefabQuaternion(6.65790267e-8f, 0.0f, 0.0f, 1.0f);
static bool gB20DiagnosticFeatureSeed = false;
static bool gB20MaterialTransitionCurrentPose = false;
struct B20NarrowphaseTrace {
    bool valid = false;
    PxTransform transform0;
    PxTransform transform1;
    PxU16 flags = 0;
    PxU8 statusFlags = 0;
    PxU8 frictionPatchCount = 0;
    PxU32 index = 0;
    PxU32 transformCache0 = 0;
    PxU32 transformCache1 = 0;
    PxU32 edgeIndex = 0;
    PxU32 npIndex = 0;
    PxU16 cacheSize = 0;
    PxU8 cachePairData = 0;
    PxU8 cacheManifoldFlags = 0;
    PxU8 manifoldHeader[12] = {};
    PxU32 pcmContactCount = 0;
    Gu::ContactPoint pcmContacts[4];
    PxU32 sceneDirectContactCount = 0;
    Gu::ContactPoint sceneDirectContacts[4];
    PxReal contactDistance = 0.0f;
    PxReal meshContactMargin = 0.0f;
    PxReal toleranceLength = 0.0f;
    PxReal transformContactDistance0 = 0.0f;
    PxReal transformContactDistance1 = 0.0f;
};
static B20NarrowphaseTrace gB20Narrowphase;
static Gu::ContactPoint gB21DirectContacts[Gu::ContactBuffer::MAX_CONTACTS];
static PxU32 gB21DirectContactCount = 0;

class ContactCapture final : public PxSimulationEventCallback {
public:
    void onConstraintBreak(PxConstraintInfo*, PxU32) override {}
    void onWake(PxActor**, PxU32) override {}
    void onSleep(PxActor**, PxU32) override {}
    void onTrigger(PxTriggerPair*, PxU32) override {}
    void onAdvance(const PxRigidBody* const*, const PxTransform*, const PxU32) override {}
    void onContact(const PxContactPairHeader& header, const PxContactPair* pairs, PxU32 count) override {
        if (!gStone || !gTarget) return;
        const bool activeFirst = header.actors[0] == gStone && header.actors[1] == gTarget;
        const bool targetFirst = header.actors[0] == gTarget && header.actors[1] == gStone;
        if (!activeFirst && !targetFirst) return;
        for (PxU32 i = 0; i < count; ++i) {
            if (pairs[i].events & (PxPairFlag::eNOTIFY_TOUCH_FOUND | PxPairFlag::eNOTIFY_TOUCH_PERSISTS)) {
                gB20ContactCount = pairs[i].contactCount;
                gB20Role = activeFirst ? 1u : 2u;
                gB20PointCount = pairs[i].extractContacts(gB20Points, 16);
            }
        }
    }
};

static ContactCapture gContactCapture;

static PxFilterFlags contactFilter(
    PxFilterObjectAttributes, PxFilterData, PxFilterObjectAttributes, PxFilterData,
    PxPairFlags& pairFlags, const void*, PxU32
) {
    pairFlags = PxPairFlag::eCONTACT_DEFAULT |
        PxPairFlag::eNOTIFY_TOUCH_FOUND |
        PxPairFlag::eNOTIFY_TOUCH_PERSISTS |
        PxPairFlag::eNOTIFY_CONTACT_POINTS;
    return PxFilterFlag::eDEFAULT;
}

namespace physx {
struct PxsContactManagerOutput;
void curling_pyphysx_capture_narrowphase_pcm(
    const PxcNpThreadContext& context, const PxcNpWorkUnit& input, const Gu::Cache& cache,
    const PxsContactManagerOutput&, bool after
) {
    if (!gStone || !gTarget || !context.mTransformCache) return;
    const PxTransform& transform0 = context.mTransformCache->getTransformCache(input.mTransformCache0).transform;
    const PxTransform& transform1 = context.mTransformCache->getTransformCache(input.mTransformCache1).transform;
    const PxVec3 activeP = gStone->getGlobalPose().p;
    const PxVec3 targetP = gTarget->getGlobalPose().p;
    const bool activeTarget =
        (transform0.p - activeP).magnitudeSquared() < 0.01f &&
        (transform1.p - targetP).magnitudeSquared() < 0.01f;
    const bool targetActive =
        (transform0.p - targetP).magnitudeSquared() < 0.01f &&
        (transform1.p - activeP).magnitudeSquared() < 0.01f;
    if (!activeTarget && !targetActive) return;
    if (after) {
        // mContactDistance is set inside discreteNarrowPhase, so only the
        // after hook observes the parameters actually consumed by PCM.
        gB20Narrowphase.contactDistance = context.mNarrowPhaseParams.mContactDistance;
        gB20Narrowphase.meshContactMargin = context.mNarrowPhaseParams.mMeshContactMargin;
        gB20Narrowphase.toleranceLength = context.mNarrowPhaseParams.mToleranceLength;
        gB20Narrowphase.transformContactDistance0 = context.mContactDistance[input.mTransformCache0];
        gB20Narrowphase.transformContactDistance1 = context.mContactDistance[input.mTransformCache1];
        gB20Narrowphase.pcmContactCount = PxMin(context.mContactBuffer.count, PxU32(4));
        for (PxU32 i = 0; i < gB20Narrowphase.pcmContactCount; ++i) {
            gB20Narrowphase.pcmContacts[i] = context.mContactBuffer.contacts[i];
        }
        // Same Scene geometry wrappers, transforms and resolved params as the
        // real call, but a fresh cache/manifold. This is a read-only B21
        // discriminator: it never writes the manager's cache or output.
        Gu::LargePersistentContactManifold directManifold;
        Gu::Cache directCache;
        directCache.setManifold(&directManifold);
        Gu::ContactBuffer directBuffer;
        directBuffer.reset();
        Gu::pcmContactConvexConvex(
            input.shapeCore0->geometry, input.shapeCore1->geometry,
            transform0, transform1, context.mNarrowPhaseParams,
            directCache, directBuffer, nullptr
        );
        gB20Narrowphase.sceneDirectContactCount = PxMin(directBuffer.count, PxU32(4));
        for (PxU32 i = 0; i < gB20Narrowphase.sceneDirectContactCount; ++i) {
            gB20Narrowphase.sceneDirectContacts[i] = directBuffer.contacts[i];
        }
        return;
    }
    gB20Narrowphase.valid = true;
    gB20Narrowphase.transform0 = transform0;
    gB20Narrowphase.transform1 = transform1;
    gB20Narrowphase.flags = input.flags;
    gB20Narrowphase.statusFlags = input.statusFlags;
    gB20Narrowphase.frictionPatchCount = input.frictionPatchCount;
    gB20Narrowphase.index = input.index;
    gB20Narrowphase.transformCache0 = input.mTransformCache0;
    gB20Narrowphase.transformCache1 = input.mTransformCache1;
    gB20Narrowphase.edgeIndex = input.mEdgeIndex;
    gB20Narrowphase.npIndex = input.mNpIndex;
    gB20Narrowphase.cacheSize = cache.mCachedSize;
    gB20Narrowphase.cachePairData = cache.mPairData;
    gB20Narrowphase.cacheManifoldFlags = cache.mManifoldFlags;
    gB20Narrowphase.contactDistance = context.mNarrowPhaseParams.mContactDistance;
    gB20Narrowphase.meshContactMargin = context.mNarrowPhaseParams.mMeshContactMargin;
    gB20Narrowphase.toleranceLength = context.mNarrowPhaseParams.mToleranceLength;
    gB20Narrowphase.transformContactDistance0 = context.mContactDistance[input.mTransformCache0];
    gB20Narrowphase.transformContactDistance1 = context.mContactDistance[input.mTransformCache1];
    if (cache.mCachedData && cache.isManifold()) {
        // This is the fixed 12-byte header at offset 64 of the scalar
        // LargePersistentContactManifold: counts/capacity and A/B features.
        std::memcpy(gB20Narrowphase.manifoldHeader, cache.mCachedData + 64, sizeof(gB20Narrowphase.manifoldHeader));
        if (gB20DiagnosticFeatureSeed) {
            // 14000 first-PCM Unity header feature bytes. This is a strictly
            // opt-in causality probe; it is never enabled by the normal B20 path.
            static const PxU8 kUnityFeatureBytes[8] = {66, 17, 176, 4, 0, 9, 0, 0};
            std::memcpy(cache.mCachedData + 67, kUnityFeatureBytes, sizeof(kUnityFeatureBytes));
        }
    }
}
}

static bool patchUnityRuntimeHull(PxConvexMesh& mesh) {
    Gu::ConvexMesh& guMesh = static_cast<Gu::ConvexMesh&>(mesh);
    Gu::ConvexHullData& hull = guMesh.getHull();
    hull.mNbEdges.clearBit();
    const PxU32 hullBytes = guMesh.getBufferSize();
    if (hullBytes != sizeof(kA18RuntimeHull)) {
        std::fprintf(stderr, "runtime-hull-size-mismatch local=%u unity=%zu\n",
            hullBytes, sizeof(kA18RuntimeHull));
        return false;
    }
    std::memcpy(static_cast<void*>(hull.mPolygons), kA18RuntimeHull, sizeof(kA18RuntimeHull));

    Gu::BigConvexRawData* big = hull.mBigConvexRawData;
    if (!big) {
        std::fprintf(stderr, "runtime-hull-bigconvex-missing\n");
        return false;
    }
    const PxU32 samplesBytes = static_cast<PxU32>(big->mNbSamples) * 2;
    const PxU32 valenciesBytes = static_cast<PxU32>(big->mNbVerts) * sizeof(Gu::Valency);
    const PxU32 adjacentBytes = static_cast<PxU32>(big->mNbAdjVerts);
    if (samplesBytes != sizeof(kA18BigConvexSamples) ||
        valenciesBytes != sizeof(kA18BigConvexValencies) ||
        adjacentBytes != sizeof(kA18BigConvexAdjacent)) {
        std::fprintf(stderr, "runtime-hull-bigconvex-size-mismatch samples=%u/%zu valencies=%u/%zu adjacent=%u/%zu\n",
            samplesBytes, sizeof(kA18BigConvexSamples), valenciesBytes, sizeof(kA18BigConvexValencies),
            adjacentBytes, sizeof(kA18BigConvexAdjacent));
        return false;
    }
    std::memcpy(big->mSamples, kA18BigConvexSamples, sizeof(kA18BigConvexSamples));
    std::memcpy(big->mValencies, kA18BigConvexValencies, sizeof(kA18BigConvexValencies));
    std::memcpy(big->mAdjacentVerts, kA18BigConvexAdjacent, sizeof(kA18BigConvexAdjacent));
    std::printf("runtime-hull-patched bytes=%u big=(%u,%u,%u)\n",
        hullBytes, samplesBytes, valenciesBytes, adjacentBytes);
    return true;
}

static PxVec3 unityF32Rotate(const PxQuat& q, const PxVec3& input) {
    // Exact operation grouping recovered from Unity's locked-axis setter bridge.
    const float vx = 2.0f * input.x;
    const float vy = 2.0f * input.y;
    const float vz = 2.0f * input.z;
    const float w2 = q.w * q.w - 0.5f;
    const float dot2 = (q.x * vx + q.y * vy) + q.z * vz;
    return PxVec3(
        (vx * w2 + (q.y * vz - q.z * vy) * q.w) + q.x * dot2,
        (vy * w2 + (q.z * vx - q.x * vz) * q.w) + q.y * dot2,
        (vz * w2 + (q.x * vy - q.y * vx) * q.w) + q.z * dot2
    );
}

static PxVec3 unityLockedAngularSetter(const PxQuat& poseQ, float requestedWy) {
    const PxQuat inverse(-poseQ.x, -poseQ.y, -poseQ.z, poseQ.w);
    const PxVec3 local = unityF32Rotate(inverse, PxVec3(0.0f, requestedWy, 0.0f));
    return unityF32Rotate(poseQ, PxVec3(0.0f, local.y, 0.0f));
}

extern "C" EMSCRIPTEN_KEEPALIVE void a19_reset(
    float px, float py, float pz, float qx, float qy, float qz, float qw,
    float vx, float vy, float vz, float wx, float wy, float wz
) {
    if (!gStone) return;
    gStone->setGlobalPose(PxTransform(PxVec3(px, py, pz), PxQuat(qx, qy, qz, qw)));
    gStone->setLinearVelocity(PxVec3(vx, vy, vz));
    gStone->setAngularVelocity(PxVec3(wx, wy, wz));
    gStone->wakeUp();
}

extern "C" EMSCRIPTEN_KEEPALIVE void a19_step(float vx, float vy, float vz, float requestedWy) {
    if (!gStone || !gScene) return;
    gStone->setLinearVelocity(PxVec3(vx, vy, vz));
    gStone->setAngularVelocity(unityLockedAngularSetter(gStone->getGlobalPose().q, requestedWy));
    gScene->simulate(0.01f);
    gScene->fetchResults(true);
}

extern "C" EMSCRIPTEN_KEEPALIVE void a19_get_state(float* out) {
    if (!gStone || !out) return;
    const PxTransform pose = gStone->getGlobalPose();
    const PxVec3 linear = gStone->getLinearVelocity();
    const PxVec3 angular = gStone->getAngularVelocity();
    out[0] = pose.p.x; out[1] = pose.p.y; out[2] = pose.p.z;
    out[3] = pose.q.x; out[4] = pose.q.y; out[5] = pose.q.z; out[6] = pose.q.w;
    out[7] = linear.x; out[8] = linear.y; out[9] = linear.z;
    out[10] = angular.x; out[11] = angular.y; out[12] = angular.z;
}

static void writeState(PxRigidDynamic* body, float* out) {
    if (!body || !out) return;
    const PxTransform pose = body->getGlobalPose();
    const PxVec3 linear = body->getLinearVelocity();
    const PxVec3 angular = body->getAngularVelocity();
    out[0] = pose.p.x; out[1] = pose.p.y; out[2] = pose.p.z;
    out[3] = pose.q.x; out[4] = pose.q.y; out[5] = pose.q.z; out[6] = pose.q.w;
    out[7] = linear.x; out[8] = linear.y; out[9] = linear.z;
    out[10] = angular.x; out[11] = angular.y; out[12] = angular.z;
}

extern "C" EMSCRIPTEN_KEEPALIVE void b20_reset(
    float px, float py, float pz, float qx, float qy, float qz, float qw,
    float vx, float vy, float vz, float wx, float wy, float wz
) {
    if (!gStone || !gTarget) return;
    gB20ContactCount = 0;
    gB20Role = 0;
    gB20PointCount = 0;
    gB20Narrowphase.valid = false;
    // 14000 RESETSTATE target (protocol x=2.375, y=5.2) in Unity native Y-up.
    gTarget->setActorFlag(PxActorFlag::eDISABLE_SIMULATION, false);
    // Unity Reset writes only Rigidbody.position. Keep the actor's existing
    // quaternion instead of replacing it with identity on every shot.
    PxTransform targetPose = gTarget->getGlobalPose();
    targetPose.p = PxVec3(-69.57740021f, 14.41978455f, 54.15000153f);
    gTarget->setGlobalPose(targetPose);
    gTarget->setLinearVelocity(PxVec3(0.0f));
    gTarget->setAngularVelocity(PxVec3(0.0f));
    gTargetShape->setFlag(PxShapeFlag::eSIMULATION_SHAPE, true);
    gTarget->putToSleep();
    gStone->setActorFlag(PxActorFlag::eDISABLE_SIMULATION, false);
    a19_reset(px, py, pz, qx, qy, qz, qw, vx, vy, vz, wx, wy, wz);
    gStoneShape->setFlag(PxShapeFlag::eSIMULATION_SHAPE, true);
    gStoneMaterial->setStaticFriction(0.0f);
    gStoneMaterial->setDynamicFriction(0.0f);
}

extern "C" EMSCRIPTEN_KEEPALIVE void b20_step(float vx, float vy, float vz, float requestedWy) {
    if (!gStone || !gTarget || !gScene) return;
    gB20ContactCount = 0;
    gB20Role = 0;
    gB20PointCount = 0;
    gB20Narrowphase.valid = false;
    gStone->setLinearVelocity(PxVec3(vx, vy, vz));
    gStone->setAngularVelocity(unityLockedAngularSetter(gStone->getGlobalPose().q, requestedWy));
    // The default retains the old predictive bridge. The opt-in diagnostic
    // instead restores material only at the actual PCM-tick pose, so we can
    // distinguish an early stone-ice friction tick from pair lifecycle state.
    const PxVec3 current = gStone->getGlobalPose().p;
    const PxVec3 predicted = current + PxVec3(vx, vy, vz) * 0.01f;
    const PxVec3 transitionProbe = gB20MaterialTransitionCurrentPose ? current : predicted;
    if ((transitionProbe - gTarget->getGlobalPose().p).magnitude() <= kB20PcmCenterDistance) {
        gStoneMaterial->setStaticFriction(0.6f);
        gStoneMaterial->setDynamicFriction(0.6f);
        gTarget->wakeUp();
    }
    gScene->simulate(0.01f);
    gScene->fetchResults(true);
}

extern "C" EMSCRIPTEN_KEEPALIVE void b20_physics_step() {
    if (!gStone || !gTarget || !gScene) return;
    gB20ContactCount = 0;
    gB20Role = 0;
    gB20PointCount = 0;
    gB20Narrowphase.valid = false;
    if ((gStone->getGlobalPose().p - gTarget->getGlobalPose().p).magnitude() <= kB20PcmCenterDistance) {
        gStoneMaterial->setStaticFriction(0.6f);
        gStoneMaterial->setDynamicFriction(0.6f);
        gTarget->wakeUp();
    }
    gScene->simulate(0.01f);
    gScene->fetchResults(true);
}

extern "C" EMSCRIPTEN_KEEPALIVE void b20_set_target_simulation(int enabled) {
    if (!gTarget) return;
    gTarget->setActorFlag(PxActorFlag::eDISABLE_SIMULATION, enabled == 0);
}

extern "C" EMSCRIPTEN_KEEPALIVE void b20_set_feature_seed_diagnostic(int enabled) {
    gB20DiagnosticFeatureSeed = enabled != 0;
}

extern "C" EMSCRIPTEN_KEEPALIVE void b20_set_material_transition_current_pose(int enabled) {
    gB20MaterialTransitionCurrentPose = enabled != 0;
}

extern "C" EMSCRIPTEN_KEEPALIVE void b20_get_shape_offsets(float* out) {
    if (!out || !gStoneShape || !gTargetShape) return;
    out[0] = gStoneShape->getContactOffset();
    out[1] = gStoneShape->getRestOffset();
    out[2] = gTargetShape->getContactOffset();
    out[3] = gTargetShape->getRestOffset();
}

extern "C" EMSCRIPTEN_KEEPALIVE void b20_get_state(int which, float* out) {
    writeState(which == 0 ? gStone : gTarget, out);
}

extern "C" EMSCRIPTEN_KEEPALIVE void b20_get_contact(float* out) {
    if (!out) return;
    out[0] = static_cast<float>(gB20ContactCount);
    out[1] = static_cast<float>(gB20Role); // 1=active->target, 2=target->active
}

extern "C" EMSCRIPTEN_KEEPALIVE void b20_get_contacts(float* out) {
    if (!out) return;
    out[0] = static_cast<float>(gB20PointCount);
    for (PxU32 i = 0; i < gB20PointCount; ++i) {
        const PxContactPairPoint& point = gB20Points[i];
        const PxU32 base = 1 + i * 7;
        out[base + 0] = point.position.x;
        out[base + 1] = point.position.y;
        out[base + 2] = point.position.z;
        out[base + 3] = point.normal.x;
        out[base + 4] = point.normal.y;
        out[base + 5] = point.normal.z;
        out[base + 6] = point.separation;
    }
}

extern "C" EMSCRIPTEN_KEEPALIVE void b20_get_narrowphase(float* out) {
    if (!out) return;
    out[0] = gB20Narrowphase.valid ? 1.0f : 0.0f;
    out[1] = static_cast<float>(gB20Narrowphase.flags);
    out[2] = static_cast<float>(gB20Narrowphase.statusFlags);
    const PxTransform transforms[2] = {gB20Narrowphase.transform0, gB20Narrowphase.transform1};
    for (PxU32 i = 0; i < 2; ++i) {
        const PxU32 base = 3 + i * 7;
        out[base + 0] = transforms[i].p.x;
        out[base + 1] = transforms[i].p.y;
        out[base + 2] = transforms[i].p.z;
        out[base + 3] = transforms[i].q.x;
        out[base + 4] = transforms[i].q.y;
        out[base + 5] = transforms[i].q.z;
        out[base + 6] = transforms[i].q.w;
    }
    out[17] = static_cast<float>(gB20Narrowphase.frictionPatchCount);
    out[18] = static_cast<float>(gB20Narrowphase.index);
    out[19] = static_cast<float>(gB20Narrowphase.transformCache0);
    out[20] = static_cast<float>(gB20Narrowphase.transformCache1);
    out[21] = static_cast<float>(gB20Narrowphase.edgeIndex);
    out[22] = static_cast<float>(gB20Narrowphase.npIndex);
    out[23] = static_cast<float>(gB20Narrowphase.cacheSize);
    out[24] = static_cast<float>(gB20Narrowphase.cachePairData);
    out[25] = static_cast<float>(gB20Narrowphase.cacheManifoldFlags);
    for (PxU32 i = 0; i < 12; ++i) out[26 + i] = static_cast<float>(gB20Narrowphase.manifoldHeader[i]);
    out[38] = static_cast<float>(gB20Narrowphase.pcmContactCount);
    for (PxU32 i = 0; i < gB20Narrowphase.pcmContactCount; ++i) {
        const Gu::ContactPoint& point = gB20Narrowphase.pcmContacts[i];
        const PxU32 base = 39 + i * 7;
        out[base + 0] = point.point.x;
        out[base + 1] = point.point.y;
        out[base + 2] = point.point.z;
        out[base + 3] = point.normal.x;
        out[base + 4] = point.normal.y;
        out[base + 5] = point.normal.z;
        out[base + 6] = point.separation;
    }
    out[67] = gB20Narrowphase.contactDistance;
    out[68] = gB20Narrowphase.meshContactMargin;
    out[69] = gB20Narrowphase.toleranceLength;
    out[70] = gB20Narrowphase.transformContactDistance0;
    out[71] = gB20Narrowphase.transformContactDistance1;
    out[72] = static_cast<float>(gB20Narrowphase.sceneDirectContactCount);
    for (PxU32 i = 0; i < gB20Narrowphase.sceneDirectContactCount; ++i) {
        const Gu::ContactPoint& point = gB20Narrowphase.sceneDirectContacts[i];
        const PxU32 base = 73 + i * 7;
        out[base + 0] = point.point.x;
        out[base + 1] = point.point.y;
        out[base + 2] = point.point.z;
        out[base + 3] = point.normal.x;
        out[base + 4] = point.normal.y;
        out[base + 5] = point.normal.z;
        out[base + 6] = point.separation;
    }
}

extern "C" EMSCRIPTEN_KEEPALIVE void b21_direct_pcm(
    float p0x, float p0y, float p0z, float q0x, float q0y, float q0z, float q0w,
    float p1x, float p1y, float p1z, float q1x, float q1y, float q1z, float q1w,
    int unityFeatureSeed
) {
    gB21DirectContactCount = 0;
    if (!gStoneMesh) return;
    const PxMeshScale scale(PxVec3(0.11270001f, 0.115f, 0.11270001f));
    Gu::GeometryUnion shape0(PxConvexMeshGeometry(gStoneMesh, scale));
    Gu::GeometryUnion shape1(PxConvexMeshGeometry(gStoneMesh, scale));
    Gu::LargePersistentContactManifold manifold;
    if (unityFeatureSeed) {
        static const PxU8 kUnityFeatureBytes[8] = {66, 17, 176, 4, 0, 9, 0, 0};
        std::memcpy(reinterpret_cast<PxU8*>(&manifold) + 67, kUnityFeatureBytes, sizeof(kUnityFeatureBytes));
    }
    Gu::Cache cache;
    cache.setManifold(&manifold);
    Gu::ContactBuffer buffer;
    buffer.reset();
    const Gu::NarrowPhaseParams params(0.02f, 0.01f, 1.0f);
    const PxTransform transform0(PxVec3(p0x, p0y, p0z), PxQuat(q0x, q0y, q0z, q0w));
    const PxTransform transform1(PxVec3(p1x, p1y, p1z), PxQuat(q1x, q1y, q1z, q1w));
    Gu::pcmContactConvexConvex(shape0, shape1, transform0, transform1, params, cache, buffer, nullptr);
    gB21DirectContactCount = buffer.count;
    for (PxU32 i = 0; i < buffer.count; ++i) gB21DirectContacts[i] = buffer.contacts[i];
}

extern "C" EMSCRIPTEN_KEEPALIVE void b21_get_direct_contacts(float* out) {
    if (!out) return;
    out[0] = static_cast<float>(gB21DirectContactCount);
    for (PxU32 i = 0; i < gB21DirectContactCount; ++i) {
        const Gu::ContactPoint& point = gB21DirectContacts[i];
        const PxU32 base = 1 + i * 7;
        out[base + 0] = point.point.x;
        out[base + 1] = point.point.y;
        out[base + 2] = point.point.z;
        out[base + 3] = point.normal.x;
        out[base + 4] = point.normal.y;
        out[base + 5] = point.normal.z;
        out[base + 6] = point.separation;
    }
}

static int a19_init_impl() {
    if (gStone) return 0;
    PxFoundation* foundation = PxCreateFoundation(PX_PHYSICS_VERSION, gAllocator, gErrors);
    if (!foundation) return 2;
    gFoundation = foundation;
    PxTolerancesScale scale;
    PxPhysics* physics = PxCreatePhysics(PX_PHYSICS_VERSION, *foundation, scale);
    if (!physics) return 3;

    PxSceneDesc sceneDesc(scale);
    sceneDesc.gravity = PxVec3(0.0f, -9.81f, 0.0f);
    sceneDesc.cpuDispatcher = &gDispatcher;
    sceneDesc.filterShader = contactFilter;
    sceneDesc.simulationEventCallback = &gContactCapture;
    sceneDesc.flags |= PxSceneFlag::eENABLE_PCM;
    PxScene* scene = physics->createScene(sceneDesc);
    if (!scene) return 4;
    gPhysics = physics;
    gScene = scene;

    PxMaterial* iceMaterial = physics->createMaterial(0.02f, 0.02f, 0.0f);
    PxMaterial* stoneMaterial = physics->createMaterial(0.0f, 0.0f, 1.0f);
    PxMaterial* targetMaterial = physics->createMaterial(0.6f, 0.6f, 1.0f);
    // Unity Ice/Bouncy materials both use PhysicMaterialCombine.Multiply.
    // During sliding this makes stone(0) x ice(0.02) exactly frictionless.
    iceMaterial->setFrictionCombineMode(PxCombineMode::eMULTIPLY);
    stoneMaterial->setFrictionCombineMode(PxCombineMode::eMULTIPLY);
    targetMaterial->setFrictionCombineMode(PxCombineMode::eMULTIPLY);
    iceMaterial->setRestitutionCombineMode(PxCombineMode::eMULTIPLY);
    stoneMaterial->setRestitutionCombineMode(PxCombineMode::eMULTIPLY);
    targetMaterial->setRestitutionCombineMode(PxCombineMode::eMULTIPLY);

    PxCookingParams cookingParams(scale);
    PxCooking* cooker = PxCreateCooking(PX_PHYSICS_VERSION, *foundation, cookingParams);
    if (!cooker) return 5;
    PxTriangleMeshDesc iceDesc;
    iceDesc.points.count = 121;
    iceDesc.points.stride = sizeof(A18Vec3);
    iceDesc.points.data = kA18IceVertices;
    iceDesc.triangles.count = 200;
    iceDesc.triangles.stride = sizeof(A18Tri);
    iceDesc.triangles.data = kA18IceTriangles;
    MemoryOutput iceCooked;
    if (!cooker->cookTriangleMesh(iceDesc, iceCooked)) return 6;
    MemoryInput iceInput(iceCooked.data);
    PxTriangleMesh* iceMesh = physics->createTriangleMesh(iceInput);
    if (!iceMesh) return 7;
    PxRigidStatic* ice = physics->createRigidStatic(PxTransform(PxVec3(-85.98600006f, 14.30478477f, 55.56601715f)));
    PxShape* iceShape = physics->createShape(
        PxTriangleMeshGeometry(iceMesh, PxMeshScale(PxVec3(4.99799156f, 1.01600003f, 0.99568027f))),
        *iceMaterial, true
    );
    ice->attachShape(*iceShape);
    iceShape->release();
    scene->addActor(*ice);

    A18Vec3 stoneVertices[512];
    for (PxU32 i = 0; i < 512; ++i) {
        // Unity native Y-up frame: recovered mesh source is X/Z/Y.
        stoneVertices[i] = {kA18StoneVertices[i].x, kA18StoneVertices[i].z, kA18StoneVertices[i].y};
    }
    PxConvexMeshDesc stoneDesc;
    stoneDesc.points.count = 512;
    stoneDesc.points.stride = sizeof(A18Vec3);
    stoneDesc.points.data = stoneVertices;
    stoneDesc.flags = PxConvexFlag::eCOMPUTE_CONVEX;
    stoneDesc.vertexLimit = 255;
    MemoryOutput stoneCooked;
    if (!cooker->cookConvexMesh(stoneDesc, stoneCooked)) return 8;
    MemoryInput stoneInput(stoneCooked.data);
    PxConvexMesh* stoneMesh = physics->createConvexMesh(stoneInput);
    if (!stoneMesh) return 9;
    if (!patchUnityRuntimeHull(*stoneMesh)) return 10;
    gStoneMesh = stoneMesh;
    cooker->release();
    const A18ReleaseTrace& release = kA18ReleaseTrace[0];
    const float releaseY = release.py + (
        A18_USE_LOCAL_RELEASE_HEIGHT ? -0.012615203857421875f : 0.0f
    );
    PxRigidDynamic* stone = physics->createRigidDynamic(PxTransform(
        PxVec3(release.px, releaseY, release.pz),
        PxQuat(release.qx, release.qy, release.qz, release.qw)
    ));
    PxShape* stoneShape = physics->createShape(
        PxConvexMeshGeometry(stoneMesh, PxMeshScale(PxVec3(0.11270001f, 0.115f, 0.11270001f))),
        *stoneMaterial, true
    );
    stoneShape->setContactOffset(0.01f);
    stone->attachShape(*stoneShape);
    gStoneShape = stoneShape;
    stoneShape->release();
    stone->setMass(19.1f);
    stone->setMassSpaceInertiaTensor(PxVec3(0.0f, 0.1892229261f, 0.0f));
    // Audit A/B: Unity's observed native setter retains the tiny world-z term
    // from the rotated yaw vector. PxRigidDynamic lock flags clear it locally,
    // while zero X/Z inverse inertia still supplies Unity's solver inertia.
    const bool usePhysxAngularLockFlags = true;
    if (usePhysxAngularLockFlags) {
        stone->setRigidDynamicLockFlag(PxRigidDynamicLockFlag::eLOCK_ANGULAR_X, true);
        stone->setRigidDynamicLockFlag(PxRigidDynamicLockFlag::eLOCK_ANGULAR_Z, true);
    }
    scene->addActor(*stone);
    gStone = stone;
    gStoneMaterial = stoneMaterial;

#ifdef A19_LIBRARY
    PxRigidDynamic* target = physics->createRigidDynamic(PxTransform(
        PxVec3(-69.57740021f, 14.41978455f, 54.15000153f), kB20PrefabQuaternion
    ));
    PxShape* targetShape = physics->createShape(
        PxConvexMeshGeometry(stoneMesh, PxMeshScale(PxVec3(0.11270001f, 0.115f, 0.11270001f))),
        *targetMaterial, true
    );
    targetShape->setContactOffset(0.01f);
    target->attachShape(*targetShape);
    gTargetShape = targetShape;
    targetShape->release();
    target->setMass(19.1f);
    target->setMassSpaceInertiaTensor(PxVec3(0.0f, 0.1892229261f, 0.0f));
    target->setRigidDynamicLockFlag(PxRigidDynamicLockFlag::eLOCK_ANGULAR_X, true);
    target->setRigidDynamicLockFlag(PxRigidDynamicLockFlag::eLOCK_ANGULAR_Z, true);
    targetShape->setFlag(PxShapeFlag::eSIMULATION_SHAPE, false);
    stoneShape->setFlag(PxShapeFlag::eSIMULATION_SHAPE, false);
    target->setActorFlag(PxActorFlag::eDISABLE_SIMULATION, true);
    stone->setActorFlag(PxActorFlag::eDISABLE_SIMULATION, true);
    scene->addActor(*target);
    gTarget = target;
    gTargetMaterial = targetMaterial;
#else
    targetMaterial->release();
#endif
    std::printf("release-height-mode local=%d initialY=%.9f unityY=%.9f\n",
        A18_USE_LOCAL_RELEASE_HEIGHT, releaseY, release.py);

#ifdef A19_LIBRARY
    return 0;
#else

    float maxPositionDelta = 0.0f;
    float maxQuaternionDelta = 0.0f;
    float maxPostSimAngularVelocityDelta = 0.0f;
    PxI32 firstDivergence = -1;
    PxI32 firstPostSimAngularVelocityDivergence = -1;
    for (PxU32 step = 0; step + 1 < 1560; ++step) {
        const A18ReleaseTrace& input = kA18ReleaseTrace[step];
        stone->setLinearVelocity(PxVec3(input.vx, input.vy, input.vz));
        stone->setAngularVelocity(unityLockedAngularSetter(stone->getGlobalPose().q, input.wy));
        scene->simulate(0.01f);
        scene->fetchResults(true);
        const PxTransform actual = stone->getGlobalPose();
        const PxVec3 actualW = stone->getAngularVelocity();
        maxPostSimAngularVelocityDelta = PxMax(maxPostSimAngularVelocityDelta, PxAbs(actualW.x - input.wx));
        maxPostSimAngularVelocityDelta = PxMax(maxPostSimAngularVelocityDelta, PxAbs(actualW.y - input.wyPost));
        maxPostSimAngularVelocityDelta = PxMax(maxPostSimAngularVelocityDelta, PxAbs(actualW.z - input.wz));
        if (firstPostSimAngularVelocityDivergence < 0 &&
            (PxAbs(actualW.x - input.wx) > 1.0e-8f ||
             PxAbs(actualW.y - input.wyPost) > 1.0e-8f ||
             PxAbs(actualW.z - input.wz) > 1.0e-8f)) {
            firstPostSimAngularVelocityDivergence = static_cast<PxI32>(step);
            std::printf("release-first-postsim-w-divergence step=%d actualP=(%.9f,%.9f,%.9f) unityP=(%.9f,%.9f,%.9f) actualQ=(%.9f,%.9f,%.9f,%.9f) unityQ=(%.9f,%.9f,%.9f,%.9f) actualW=(%.12g,%.12g,%.12g) unityW=(%.12g,%.12g,%.12g)\n",
                firstPostSimAngularVelocityDivergence,
                actual.p.x, actual.p.y, actual.p.z, input.px, input.py, input.pz,
                actual.q.x, actual.q.y, actual.q.z, actual.q.w,
                input.qx, input.qy, input.qz, input.qw,
                actualW.x, actualW.y, actualW.z, input.wx, input.wyPost, input.wz);
        }
        const A18ReleaseTrace& expected = kA18ReleaseTrace[step + 1];
        maxPositionDelta = PxMax(maxPositionDelta, PxAbs(actual.p.x - expected.px));
        maxPositionDelta = PxMax(maxPositionDelta, PxAbs(actual.p.y - expected.py));
        maxPositionDelta = PxMax(maxPositionDelta, PxAbs(actual.p.z - expected.pz));
        maxQuaternionDelta = PxMax(maxQuaternionDelta, PxAbs(actual.q.x - expected.qx));
        maxQuaternionDelta = PxMax(maxQuaternionDelta, PxAbs(actual.q.y - expected.qy));
        maxQuaternionDelta = PxMax(maxQuaternionDelta, PxAbs(actual.q.z - expected.qz));
        maxQuaternionDelta = PxMax(maxQuaternionDelta, PxAbs(actual.q.w - expected.qw));
        if (firstDivergence < 0 &&
            (PxAbs(actual.p.x - expected.px) > 1.0e-6f ||
             PxAbs(actual.p.y - expected.py) > 1.0e-6f ||
             PxAbs(actual.p.z - expected.pz) > 1.0e-6f ||
             PxAbs(actual.q.x - expected.qx) > 1.0e-7f ||
             PxAbs(actual.q.y - expected.qy) > 1.0e-7f ||
             PxAbs(actual.q.z - expected.qz) > 1.0e-7f ||
             PxAbs(actual.q.w - expected.qw) > 1.0e-7f)) {
            firstDivergence = static_cast<PxI32>(step + 1);
            std::printf("release-first-divergence step=%d actualP=(%.9f,%.9f,%.9f) unityP=(%.9f,%.9f,%.9f) actualQy=%.9f unityQy=%.9f\n",
                firstDivergence, actual.p.x, actual.p.y, actual.p.z,
                expected.px, expected.py, expected.pz, actual.q.y, expected.qy);
        }
    }
    const PxTransform pose = stone->getGlobalPose();
    const A18ReleaseTrace& expected = kA18ReleaseTrace[1559];
    std::printf("release-replay locks=%d steps=1559 maxP=%.9g maxQ=%.9g maxPostSimW=%.9g\n",
        usePhysxAngularLockFlags ? 1 : 0, maxPositionDelta, maxQuaternionDelta,
        maxPostSimAngularVelocityDelta);
    std::printf("release-replay actual p=(%.9f,%.9f,%.9f) q=(%.9f,%.9f,%.9f,%.9f)\n",
        pose.p.x, pose.p.y, pose.p.z, pose.q.x, pose.q.y, pose.q.z, pose.q.w);
    std::printf("release-replay unity  p=(%.9f,%.9f,%.9f) q=(%.9f,%.9f,%.9f,%.9f)\n",
        expected.px, expected.py, expected.pz, expected.qx, expected.qy, expected.qz, expected.qw);

    stone->release();
#ifdef A19_LIBRARY
    target->release();
#endif
    stoneMesh->release();
    ice->release();
    iceMesh->release();
    stoneMaterial->release();
#ifdef A19_LIBRARY
    targetMaterial->release();
#endif
    iceMaterial->release();
    scene->release();
    physics->release();
    foundation->release();
    return 0;
#endif
}

extern "C" EMSCRIPTEN_KEEPALIVE void a19_init() {
    a19_init_impl();
}

int main() {
    return a19_init_impl();
}
