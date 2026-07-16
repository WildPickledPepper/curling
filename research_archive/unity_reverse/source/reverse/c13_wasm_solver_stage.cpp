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
void solveContactBlock(const PxSolverConstraintDesc* desc, PxU32 constraintCount, SolverContext& cache);
}
}

static constexpr PxU32 kSolverBodyBytes = sizeof(PxSolverBody);
static constexpr PxU32 kConstraintBytes = 320;
static constexpr PxU32 kConstraintSolveBytes = 304;

extern "C" EMSCRIPTEN_KEEPALIVE PxU32 c13_solver_body_bytes()
{
    return kSolverBodyBytes;
}

extern "C" EMSCRIPTEN_KEEPALIVE PxU32 c13_constraint_bytes()
{
    return kConstraintBytes;
}

extern "C" EMSCRIPTEN_KEEPALIVE int c13_solve_regular(
    const PxU8* bodyAInput,
    const PxU8* bodyBInput,
    const PxU8* constraintInput,
    int doFriction,
    PxU8* bodyAOutput,
    PxU8* bodyBOutput,
    PxU8* constraintOutput)
{
    if (!bodyAInput || !bodyBInput || !constraintInput || !bodyAOutput || !bodyBOutput || !constraintOutput)
        return 1;

    alignas(16) PxSolverBody bodyA;
    alignas(16) PxSolverBody bodyB;
    alignas(16) PxU8 constraint[kConstraintBytes];
    std::memcpy(&bodyA, bodyAInput, kSolverBodyBytes);
    std::memcpy(&bodyB, bodyBInput, kSolverBodyBytes);
    std::memcpy(constraint, constraintInput, kConstraintBytes);

    PxSolverConstraintDesc desc = {};
    desc.bodyA = &bodyA;
    desc.bodyB = &bodyB;
    desc.linkIndexA = PxSolverConstraintDesc::NO_LINK;
    desc.linkIndexB = PxSolverConstraintDesc::NO_LINK;
    // C11 records a 320-byte observation window. The captured descriptor itself
    // owns 19 * 16 bytes; the final 16 bytes belong to adjacent memory.
    desc.constraintLengthOver16 = static_cast<PxU16>(kConstraintSolveBytes / 16);
    desc.constraint = constraint;

    Dy::SolverContext context = {};
    context.doFriction = doFriction != 0;
    context.writeBackIteration = false;
    Dy::solveContactBlock(&desc, 1, context);

    std::memcpy(bodyAOutput, &bodyA, kSolverBodyBytes);
    std::memcpy(bodyBOutput, &bodyB, kSolverBodyBytes);
    std::memcpy(constraintOutput, constraint, kConstraintBytes);
    return 0;
}
