/* Original WebGL f82200/f82202: uint32 shifts and explicit f32 grouping.
 * The friction helper also preserves the existing iterator's f32 add followed
 * by f64 subtraction. One call consumes one random word; no prefetching.
 */
#include <stdint.h>

__declspec(dllexport) uint32_t unity_rng_step(uint32_t *state) {
    uint32_t old0=state[0], old3=state[3];
    state[0]=state[1]; state[1]=state[2]; state[2]=old3;
    uint32_t x=old0^(old0<<11);
    state[3]=old3^((x>>8)^x)^(old3>>19);
    return state[3];
}

__declspec(dllexport) float unity_rng_range(uint32_t *state, float minimum, float maximum) {
    float t=(float)(unity_rng_step(state)&UINT32_C(8388607))*0x1.000002p-23f;
    float left=minimum*t;
    float right=(1.0f-t)*maximum;
    return left+right;
}

__declspec(dllexport) double unity_rng_friction_noise(uint32_t *state, float base, float amplitude) {
    float noise=unity_rng_range(state,-amplitude,amplitude);
    float friction=base+noise;
    return (double)friction-(double)base;
}
