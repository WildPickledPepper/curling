#include "PxPhysicsAPI.h"
#include "solver/PxSolverDefs.h"
#include "CmPhysXCommon.h"
#include "CmSpatialVector.h"
#include "DySolverContext.h"
#include <emscripten/emscripten.h>
#include <cstring>

using namespace physx;

namespace physx
{
namespace Dy
{
void solveContact_BStaticBlock(const PxSolverConstraintDesc* desc, PxU32 constraintCount, SolverContext& cache);
}
}

static constexpr PxU32 kSolverBodyBytes = sizeof(PxSolverBody);
static constexpr PxU32 kConstraintBytes = 608;

extern "C" EMSCRIPTEN_KEEPALIVE PxU32 c14_solver_body_bytes()
{
    return kSolverBodyBytes;
}

extern "C" EMSCRIPTEN_KEEPALIVE PxU32 c14_constraint_bytes()
{
    return kConstraintBytes;
}

extern "C" EMSCRIPTEN_KEEPALIVE int c14_solve_static(
    const PxU8* bodyInput,
    const PxU8* constraintInput,
    PxU16 constraintLengthOver16,
    int doFriction,
    PxU8* bodyOutput,
    PxU8* constraintOutput)
{
    if (!bodyInput || !constraintInput || !bodyOutput || !constraintOutput ||
        constraintLengthOver16 == 0 || PxU32(constraintLengthOver16) * 16u > kConstraintBytes)
        return 1;

    alignas(16) PxSolverBody body;
    alignas(16) PxU8 constraint[kConstraintBytes];
    std::memcpy(&body, bodyInput, kSolverBodyBytes);
    std::memcpy(constraint, constraintInput, kConstraintBytes);

    PxSolverConstraintDesc desc = {};
    desc.bodyA = &body;
    desc.linkIndexA = PxSolverConstraintDesc::NO_LINK;
    desc.constraintLengthOver16 = constraintLengthOver16;
    desc.constraint = constraint;

    Dy::SolverContext context = {};
    context.doFriction = doFriction != 0;
    context.writeBackIteration = false;
    Dy::solveContact_BStaticBlock(&desc, 1, context);

    std::memcpy(bodyOutput, &body, kSolverBodyBytes);
    std::memcpy(constraintOutput, constraint, kConstraintBytes);
    return 0;
}
