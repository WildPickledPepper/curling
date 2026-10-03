  (func $f79751 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 f32)
    local.get $p0
    i32.const -64
    i32.sub
    local.get $p0
    f32.load offset=56
    local.tee $l2
    f32.store
    local.get $p0
    f32.const 0x1p+0 (;=1;)
    local.get $l2
    f32.div
    f32.store offset=72)
