/* Bridge to the existing, hash-verified CP39 kernel, not a new physics solver.
 * Method slots and the motion entry are traced from its Python bindings.
 * Keep getters/setters (including wake/cache side effects) and their order.
 */
#include <stdint.h>
#include <stdbool.h>
#include "unity_angular_projection.c"
#include "unity_random.c"

typedef struct { float x,y,z; } Vec3;
typedef struct { float x,y,z,w,px,py,pz; } Pose;
typedef struct { double x,y,angle; } Motion;
typedef Motion *(*MotionFn)(Motion *,double,double,double,double,double,int);
typedef Vec3 *(*GetVec)(void *,Vec3 *);
typedef Pose *(*GetPose)(void *,Pose *);
typedef void (*SetVec)(void *,const Vec3 *,bool);
typedef void (*SetPose)(void *,const Pose *,bool);
typedef bool (*Sleeping)(void *);
typedef struct {
    void *motion;
    void *actors[16];
    double positions[32];
    void *scene;
    void *simulate;
} Context;

static void **methods(void *actor) { return *(void ***)actor; }
static void position(Context *context,int index) {
    void *actor=context->actors[index];
    Pose pose;
    ((GetPose)methods(actor)[18])(actor,&pose);
    context->positions[index*2]=56.525001525878906-(double)pose.pz;
    context->positions[index*2+1]=-64.377398-(double)pose.px;
}

__declspec(dllexport) void unity_bridge_prepare(
    Context *context,int index,uint32_t enabled,int normalize,double noise,uint32_t *rng) {
    /* Recreate the prior lazy iterator's f32 add, f64 subtract and final f32
     * mapping. No draw before the controller's eligibility gate, no prefetch.
     */
    const float base=0x1.0624dep-10f;
    if (rng) noise=unity_rng_friction_noise(rng,base,(float)0.0002);
    double sum=(double)base+noise;
    double friction=(double)(float)sum;
    void *actor=context->actors[index];
    void **vtable=methods(actor);
    Vec3 linear,angular,set_linear,set_angular;
    Motion output;
    Pose pose;
    float projected[3];
    ((GetVec)vtable[38])(actor,&linear);
    ((GetVec)vtable[40])(actor,&angular);
    ((MotionFn)context->motion)(&output,friction,-(double)linear.z,
        -(double)linear.x,(double)angular.y,0x1.0624dep-10,0);
    set_linear.x=(float)(-output.y);
    set_linear.y=0.0f;
    set_linear.z=(float)(-output.x);
    ((SetVec)vtable[39])(actor,&set_linear,true);
    ((GetPose)vtable[18])(actor,&pose);
    unity_angular_projection(pose.x,pose.y,pose.z,pose.w,(float)output.angle,
        normalize,projected);
    set_angular.x=projected[0];
    set_angular.y=projected[1];
    set_angular.z=projected[2];
    ((SetVec)vtable[41])(actor,&set_angular,true);
    /* Keep the original pre-sim getter order: active, then other enabled
     * slots. Python retains its math.hypot PCM threshold comparison.
     */
    position(context,index);
    for (int k=0;k<16;++k)
        if (k!=index && (enabled&(UINT32_C(1)<<k))) position(context,k);
}

__declspec(dllexport) void unity_bridge_writeback(Context *context,uint32_t enabled) {
    for (int k=0;k<16;++k) {
        if (!(enabled&(UINT32_C(1)<<k))) continue;
        void *actor=context->actors[k];
        void **vtable=methods(actor);
        if (((Sleeping)vtable[63])(actor)) continue;
        Pose pose;
        ((GetPose)vtable[18])(actor,&pose);
        /* Never skip equal poses: the real setter invalidates caches. */
        ((SetPose)vtable[19])(actor,&pose,false);
    }
}

/* The actual SceneWrapper::simulate binding entry clears its saved reports,
 * calls simulate/fetchResults, and adds the promoted f32 dt to scene time.
 * Reuse that complete entry; do not reproduce its internal physical work.
 */
__declspec(dllexport) int unity_bridge_simulate_writeback(
    Context *context,float dt,uint32_t enabled) {
    ((void (*)(void *,float))context->simulate)(context->scene,dt);
    void *begin=*(void **)((char *)context->scene+0x38);
    void *end=*(void **)((char *)context->scene+0x40);
    if (begin!=end) return 0;
    /* No saved records means the original callback loops are empty. On a
     * nonempty step Python performs callbacks before calling writeback.
     */
    unity_bridge_writeback(context,enabled);
    return 1;
}
