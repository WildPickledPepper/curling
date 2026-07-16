#include "PxPhysicsAPI.h"
#include <cstdio>
#include <cstdlib>

using namespace physx;

class Allocator final : public PxAllocatorCallback {
public:
    void* allocate(size_t size, const char*, const char*, int) override {
        void* result = nullptr;
        return posix_memalign(&result, 16, size) == 0 ? result : nullptr;
    }

    void deallocate(void* pointer) override {
        std::free(pointer);
    }
};

class Errors final : public PxErrorCallback {
public:
    void reportError(PxErrorCode::Enum, const char* message, const char*, int) override {
        std::fprintf(stderr, "%s\n", message);
    }
};

class InlineDispatcher final : public PxCpuDispatcher {
public:
    void submitTask(PxBaseTask& task) override {
        task.run();
        task.release();
    }

    PxU32 getWorkerCount() const override { return 1; }
};

static PxFilterFlags smokeFilter(
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

namespace physx {
class PxcNpThreadContext;
struct PxcNpWorkUnit;
namespace Gu { struct Cache; }
struct PxsContactManagerOutput;
void curling_pyphysx_capture_narrowphase_pcm(
    const PxcNpThreadContext&, const PxcNpWorkUnit&, const Gu::Cache&,
    const PxsContactManagerOutput&, bool
) {}
}

int main() {
    Allocator allocator;
    Errors errors;
    PxFoundation* foundation = PxCreateFoundation(PX_PHYSICS_VERSION, allocator, errors);
    if (!foundation) return 2;

    PxTolerancesScale scale;
    PxPhysics* physics = PxCreatePhysics(PX_PHYSICS_VERSION, *foundation, scale);
    if (!physics) return 3;

    PxSceneDesc desc(scale);
    desc.gravity = PxVec3(0.0f, -9.81f, 0.0f);
    InlineDispatcher dispatcher;
    desc.cpuDispatcher = &dispatcher;
    desc.filterShader = smokeFilter;
    desc.flags |= PxSceneFlag::eENABLE_PCM;
    PxScene* scene = physics->createScene(desc);
    if (!scene) return 4;

    PxMaterial* material = physics->createMaterial(0.5f, 0.5f, 0.0f);
    PxRigidDynamic* body = physics->createRigidDynamic(PxTransform(PxVec3(0.0f, 1.0f, 0.0f)));
    PxShape* shape = physics->createShape(PxBoxGeometry(0.1f, 0.1f, 0.1f), *material, true);
    body->attachShape(*shape);
    shape->release();
    scene->addActor(*body);
    scene->simulate(0.01f);
    scene->fetchResults(true);
    const PxVec3 p = body->getGlobalPose().p;
    std::printf("scene-smoke p=(%.9f,%.9f,%.9f)\n", p.x, p.y, p.z);

    body->release();
    material->release();
    scene->release();
    physics->release();
    foundation->release();
    return 0;
}
