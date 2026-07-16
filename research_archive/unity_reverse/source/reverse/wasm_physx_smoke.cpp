// Minimal Node/WebAssembly smoke test for the locally rebuilt scalar PhysX.
// This deliberately creates a real PxPhysics scene instead of merely exporting
// a header constant, so a passing run proves the Emscripten static libraries
// can host the backend required by the remaining WebGL-vs-x64 investigation.

#include <PxPhysicsAPI.h>
#include <extensions/PxDefaultAllocator.h>
#include <emscripten/emscripten.h>

#include <array>
#include <cmath>
#include <cstring>
#include <vector>

using namespace physx;

namespace {

class SilentErrorCallback final : public PxErrorCallback {
public:
    void reportError(PxErrorCode::Enum, const char*, const char*, int) override {}
};

SilentErrorCallback gError;
PxDefaultAllocator gAllocator;
std::array<float, 12> gTwoStoneOutput{};

// PhysX's default memory stream helpers live in the extensions library, which
// is intentionally not part of the minimal scalar WebAssembly archive.  Keep
// this bridge self-contained instead of silently linking a differently-built
// extensions binary.
class MemoryOutputStream final : public PxOutputStream {
public:
    PxU32 write(const void* source, PxU32 count) override {
        const size_t offset = bytes.size();
        bytes.resize(offset + count);
        std::memcpy(bytes.data() + offset, source, count);
        return count;
    }

    std::vector<PxU8> bytes;
};

class MemoryInputData final : public PxInputData {
public:
    explicit MemoryInputData(const std::vector<PxU8>& source)
        : bytes(source), position(0) {}

    PxU32 read(void* destination, PxU32 count) override {
        const PxU32 available = static_cast<PxU32>(bytes.size()) - position;
        const PxU32 copied = count < available ? count : available;
        if (copied) {
            std::memcpy(destination, bytes.data() + position, copied);
            position += copied;
        }
        return copied;
    }

    PxU32 getLength() const override { return static_cast<PxU32>(bytes.size()); }
    void seek(PxU32 offset) override {
        const PxU32 length = getLength();
        position = offset < length ? offset : length;
    }
    PxU32 tell() const override { return position; }

private:
    const std::vector<PxU8>& bytes;
    PxU32 position;
};

class InlineDispatcher final : public PxCpuDispatcher {
public:
    void submitTask(PxBaseTask& task) override {
        task.run();
        task.release();
    }

    uint32_t getWorkerCount() const override { return 1; }
};

PxFilterFlags smokeFilter(
    PxFilterObjectAttributes,
    PxFilterData,
    PxFilterObjectAttributes,
    PxFilterData,
    PxPairFlags& pairFlags,
    const void*,
    PxU32
) {
    pairFlags = PxPairFlag::eCONTACT_DEFAULT;
    return PxFilterFlag::eDEFAULT;
}

PxConvexMesh* makeStoneMesh(PxPhysics& physics, PxCooking& cooking) {
    constexpr unsigned kFaces = 256;
    constexpr float kRadius = 0.140875f;
    constexpr float kHalfHeight = 0.115f;
    std::array<PxVec3, kFaces * 2> points{};
    for (unsigned index = 0; index < kFaces; ++index) {
        const float angle = 2.0f * PxPi * static_cast<float>(index) / static_cast<float>(kFaces);
        const PxVec3 ring(kRadius * std::cos(angle), 0.0f, kRadius * std::sin(angle));
        points[index * 2] = ring + PxVec3(0.0f, kHalfHeight, 0.0f);
        points[index * 2 + 1] = ring - PxVec3(0.0f, kHalfHeight, 0.0f);
    }
    PxConvexMeshDesc desc;
    desc.points.count = static_cast<PxU32>(points.size());
    desc.points.stride = sizeof(PxVec3);
    desc.points.data = points.data();
    desc.flags = PxConvexFlag::eCOMPUTE_CONVEX;
    desc.quantizedCount = 255;
    desc.vertexLimit = 255;
    MemoryOutputStream stream;
    PxConvexMeshCookingResult::Enum result;
    if (!cooking.cookConvexMesh(desc, stream, &result)) {
        return nullptr;
    }
    MemoryInputData data(stream.bytes);
    return physics.createConvexMesh(data);
}

PxRigidDynamic* makeStone(
    PxPhysics& physics,
    PxConvexMesh& mesh,
    PxMaterial& material,
    float x,
    float z,
    float vx,
    float vz
) {
    PxRigidDynamic* body = physics.createRigidDynamic(PxTransform(PxVec3(x, 0.115f, z)));
    if (!body) return nullptr;
    PxShape* shape = physics.createShape(PxConvexMeshGeometry(&mesh), material, true);
    if (!shape) {
        body->release();
        return nullptr;
    }
    body->attachShape(*shape);
    shape->release();
    body->setMass(20.0f);
    body->setMassSpaceInertiaTensor(PxVec3(0.17881061f, 0.18922293f, 0.17881061f));
    body->setLinearDamping(0.0f);
    body->setAngularDamping(0.05f);
    body->setSolverIterationCounts(6, 1);
    body->setMaxDepenetrationVelocity(10.0f);
    body->setLinearVelocity(PxVec3(vx, 0.0f, vz));
    return body;
}

}  // namespace

// The scalar PhysX archive was built with pyphysx's optional trace hooks.
// The production bridge supplies these callbacks; this standalone smoke test
// intentionally supplies inert versions so it can exercise the same archive.
namespace physx {
class PxcNpThreadContext;
struct PxcNpWorkUnit;
struct PxsContactManagerOutput;
namespace Gu { class Cache; }
void curling_pyphysx_capture_narrowphase_pcm(
    const PxcNpThreadContext&, const PxcNpWorkUnit&, const Gu::Cache&,
    const PxsContactManagerOutput&, bool
) {}
void curling_pyphysx_prepare_narrowphase_pcm_cache(
    PxcNpThreadContext&, const PxcNpWorkUnit&, Gu::Cache&
) {}
}  // namespace physx

extern "C" EMSCRIPTEN_KEEPALIVE int curling_physx_wasm_smoke() {
    PxFoundation* foundation = PxCreateFoundation(PX_PHYSICS_VERSION, gAllocator, gError);
    if (!foundation) {
        return 1;
    }
    PxTolerancesScale scale;
    PxPhysics* physics = PxCreatePhysics(PX_PHYSICS_VERSION, *foundation, scale, false, nullptr);
    if (!physics) {
        foundation->release();
        return 2;
    }
    PxSceneDesc sceneDesc(scale);
    sceneDesc.gravity = PxVec3(0.0f, -9.81f, 0.0f);
    InlineDispatcher dispatcher;
    sceneDesc.cpuDispatcher = &dispatcher;
    sceneDesc.filterShader = smokeFilter;
    PxScene* scene = physics->createScene(sceneDesc);
    const int result = scene ? 0 : 3;
    if (scene) {
        scene->release();
    }
    physics->release();
    foundation->release();
    return result;
}

extern "C" EMSCRIPTEN_KEEPALIVE int curling_physx_wasm_two_stone_step(
    float x0, float z0, float vx0, float vz0,
    float x1, float z1, float vx1, float vz1
) {
    gTwoStoneOutput.fill(0.0f);
    PxFoundation* foundation = PxCreateFoundation(PX_PHYSICS_VERSION, gAllocator, gError);
    if (!foundation) return 1;
    PxTolerancesScale scale;
    PxPhysics* physics = PxCreatePhysics(PX_PHYSICS_VERSION, *foundation, scale, false, nullptr);
    if (!physics) { foundation->release(); return 2; }
    PxCookingParams cookingParams(scale);
    PxCooking* cooking = PxCreateCooking(PX_PHYSICS_VERSION, *foundation, cookingParams);
    if (!cooking) { physics->release(); foundation->release(); return 3; }
    PxSceneDesc sceneDesc(scale);
    sceneDesc.gravity = PxVec3(0.0f, -9.81f, 0.0f);
    InlineDispatcher dispatcher;
    sceneDesc.cpuDispatcher = &dispatcher;
    sceneDesc.filterShader = smokeFilter;
    PxScene* scene = physics->createScene(sceneDesc);
    PxMaterial* ice = physics->createMaterial(0.02f, 0.02f, 0.0f);
    PxMaterial* stone = physics->createMaterial(0.6f, 0.6f, 1.0f);
    PxConvexMesh* mesh = makeStoneMesh(*physics, *cooking);
    if (!scene || !ice || !stone || !mesh) {
        if (mesh) mesh->release();
        if (stone) stone->release();
        if (ice) ice->release();
        if (scene) scene->release();
        cooking->release(); physics->release(); foundation->release();
        return 4;
    }
    PxRigidStatic* floor = physics->createRigidStatic(PxTransform(PxQuat(PxHalfPi, PxVec3(0.0f, 0.0f, 1.0f))));
    PxShape* floorShape = physics->createShape(PxPlaneGeometry(), *ice, true);
    floor->attachShape(*floorShape);
    floorShape->release();
    PxRigidDynamic* a = makeStone(*physics, *mesh, *stone, x0, z0, vx0, vz0);
    PxRigidDynamic* b = makeStone(*physics, *mesh, *stone, x1, z1, vx1, vz1);
    if (!floor || !a || !b) {
        if (a) a->release(); if (b) b->release(); if (floor) floor->release();
        mesh->release(); stone->release(); ice->release(); scene->release(); cooking->release(); physics->release(); foundation->release();
        return 5;
    }
    scene->addActor(*floor); scene->addActor(*a); scene->addActor(*b);
    scene->simulate(0.01f); scene->fetchResults(true);
    const PxTransform pa = a->getGlobalPose(); const PxTransform pb = b->getGlobalPose();
    const PxVec3 va = a->getLinearVelocity(); const PxVec3 vb = b->getLinearVelocity();
    gTwoStoneOutput = {pa.p.x, pa.p.z, va.x, va.z, pa.q.y, a->getAngularVelocity().y,
                        pb.p.x, pb.p.z, vb.x, vb.z, pb.q.y, b->getAngularVelocity().y};
    a->release(); b->release(); floor->release(); mesh->release(); stone->release(); ice->release(); scene->release(); cooking->release(); physics->release(); foundation->release();
    return 0;
}

extern "C" EMSCRIPTEN_KEEPALIVE float curling_physx_wasm_two_stone_output(int index) {
    return (index >= 0 && index < static_cast<int>(gTwoStoneOutput.size())) ? gTwoStoneOutput[static_cast<size_t>(index)] : 0.0f;
}
