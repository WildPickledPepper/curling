// Compile the actual PhysX 4.1 unconstrained-velocity helper to Wasm.
// Diagnostic only: production does not call this kernel until its recurrence
// matches the Unity bridge trace.

#include "DyBodyCoreIntegrator.h"

extern "C" float a11_apply_physx_unconstrained_angular(
    float angularVelocity,
    float angularDamping,
    float dt
) {
    physx::PxVec3 linearVelocity(0.0f);
    physx::PxVec3 angular(0.0f, angularVelocity, 0.0f);
    physx::Dy::bodyCoreComputeUnconstrainedVelocity(
        physx::PxVec3(0.0f),
        dt,
        0.0f,
        angularDamping,
        1.0f,
        1.0e30f,
        1.0e30f,
        linearVelocity,
        angular,
        true
    );
    return angular.y;
}

extern "C" float a11_rotate_angular_y(
    float qx,
    float qy,
    float qz,
    float qw,
    float angularVelocity
) {
    const physx::PxQuat rotation(qx, qy, qz, qw);
    return rotation.rotate(physx::PxVec3(0.0f, angularVelocity, 0.0f)).y;
}
