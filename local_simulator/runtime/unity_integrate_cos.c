/* Unity wasm cbbd1ad2..., f33062 -> f18889/f18888/f18176.
 * Build with build_unity_integrate_cos.py: SSE2, no reassociation or FMA.
 * Only the two verified PhysX integrateCore call sites use this function.
 * The original angular cap is 1e7; at the simulator's dt=.01 the largest
 * half-angle is 50000. The original moderate reduction covers much more.
 * Large finite argument reduction (f5976) is outside this integration contract.
 */
#include <stdint.h>
#include <string.h>

static float cos_kernel(double x) {
    double z = x*x, zz = z*z;
    double high = (z*zz) * (z*0x1.99342e0ee5069p-16 - 0x1.6c087e80f1e27p-10);
    double low = zz*0x1.55553e1053a42p-5 + (z*(-0x1.ffffffd0c5e81p-2) + 1.0);
    return (float)(high + low);
}

static float sin_kernel(double x) {
    double z = x*x, v = z*x;
    double high = (v*(z*z)) * (z*0x1.6cd878c3b46a7p-19 - 0x1.a00f9e2cae774p-13);
    double low = v*(z*0x1.11110896efbb2p-7 - 0x1.5555554cbac77p-3) + x;
    return (float)(high + low);
}

__declspec(dllexport) float unity_integrate_cosf(float x) {
    uint32_t bits;
    memcpy(&bits, &x, 4);
    uint32_t a = bits & 0x7fffffffU;
    int negative = (bits >> 31) != 0;
    double xd = (double)x;
    if (a <= 1061752794U) {
        if (a < 964689920U) return 1.0f;
        return cos_kernel(xd);
    }
    if (a <= 1081824209U) {
        if (a >= 1075235812U)
            return -cos_kernel((negative ? 0x1.921fb54442d18p+1 : -0x1.921fb54442d18p+1) + xd);
        return negative ? sin_kernel(xd + 0x1.921fb54442d18p+0)
                        : sin_kernel(0x1.921fb54442d18p+0 - xd);
    }
    if (a <= 1088565717U) {
        if (a >= 1085271520U)
            return cos_kernel((negative ? 0x1.921fb54442d18p+2 : -0x1.921fb54442d18p+2) + xd);
        return negative ? sin_kernel(-0x1.2d97c7f3321d2p+2 - xd)
                        : sin_kernel(xd + (-0x1.2d97c7f3321d2p+2));
    }
    if (a >= 2139095040U) return x-x;
    if (a > 1305022426U) {
        /* Fail visibly outside the verified domain; never use system cosf. */
        uint32_t nan_bits = 0x7fc00000U;
        float invalid;
        memcpy(&invalid, &nan_bits, 4);
        return invalid;
    }
    double fn = (xd*0x1.45f306dc9c883p-1 + 0x1.8p+52) + (-0x1.8p+52);
    double y = (xd + fn*(-0x1.921fb5p+0)) + fn*(-0x1.110b4611a6263p-26);
    int32_t n = (int32_t)fn;
    if (y < -0x1.921fb6p-1) {
        fn = fn - 1.0;
        y = (xd + fn*(-0x1.921fb5p+0)) + fn*(-0x1.110b4611a6263p-26);
        n--;
    } else if (y > 0x1.921fb6p-1) {
        fn = fn + 1.0;
        y = (xd + fn*(-0x1.921fb5p+0)) + fn*(-0x1.110b4611a6263p-26);
        n++;
    }
    switch ((uint32_t)n & 3U) {
        case 0: return cos_kernel(y);
        case 1: return sin_kernel(-y);
        case 2: return -cos_kernel(y);
        default: return sin_kernel(y);
    }
}
