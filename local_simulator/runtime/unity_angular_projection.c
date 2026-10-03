/* Exact operation tree of the existing Unity f73035 projection.
 * No fast-math, reassociation, FMA or float64 intermediate operations.
 * Normalization mirrors the existing four-element numpy float32 reduction.
 */
#include <math.h>

__declspec(dllexport) void unity_angular_projection(
    float x, float y, float z, float w, float vy, int normalize, float *out) {
    if (normalize) {
        float xx=x*x, yy=y*y, zz=z*z, ww=w*w;
        float sum=((xx+yy)+zz)+ww;
        float norm=sqrtf(sum);
        x=x/norm; y=y/norm; z=z/norm; w=w/norm;
    }
    float vx2=0.0f, vy2=vy+vy, vz2=0.0f;
    float dot=z*vz2+(x*vx2+y*vy2);
    float half=w*w+(-0.5f);
    float local_y=y*dot+(vy2*half-w*(z*vx2-vz2*x));
    local_y=local_y+local_y;
    float local_x=0.0f, local_z=0.0f;
    dot=z*local_z+(x*local_x+y*local_y);
    out[0]=x*dot+(local_x*half+w*(y*local_z-local_y*z));
    out[1]=y*dot+(local_y*half+w*(z*local_x-local_z*x));
    out[2]=z*dot+(local_z*half+w*(x*local_y-local_x*y));
}
