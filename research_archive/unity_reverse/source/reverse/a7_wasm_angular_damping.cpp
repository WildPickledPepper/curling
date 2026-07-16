// Minimal Wasm probe for PhysX Dy::bodyCoreComputeUnconstrainedVelocity.
// This is a diagnostic kernel, not a replacement for the PhysX integration backend.

extern "C" float a7_apply_angular_damping(
    const float angular_velocity,
    const float angular_damping,
    const float dt
) {
    const float angular_damping_times_dt = angular_damping * dt;
    const float one_minus_angular_damping_times_dt = 1.0f - angular_damping_times_dt;
    const float angular_velocity_multiplier =
        one_minus_angular_damping_times_dt > 0.0f ? one_minus_angular_damping_times_dt : 0.0f;
    return angular_velocity * angular_velocity_multiplier;
}
