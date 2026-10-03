  (func $f79752 (type $t7) (param $p0 i32)
    (local $l1 f32) (local $l2 f32) (local $l3 i32)
    local.get $p0
    i32.const 56
    i32.add
    local.tee $l3
    f32.const 0x1.a36e2ep-14 (;=0.0001;)
    local.get $l3
    f32.load
    local.tee $l1
    f32.const 0x0p+0 (;=0;)
    local.get $l1
    local.get $l1
    f32.eq
    select
    local.tee $l1
    f32.const 0x1.4p+3 (;=10;)
    f32.min
    local.get $l1
    f32.const 0x1.a36e2ep-14 (;=0.0001;)
    f32.lt
    select
    local.tee $l1
    f32.store
    local.get $p0
    local.get $l1
    local.get $p0
    f32.load offset=240
    local.tee $l2
    f32.const 0x0p+0 (;=0;)
    local.get $l2
    local.get $l2
    f32.eq
    select
    local.tee $l2
    local.get $l1
    local.get $l2
    f32.gt
    select
    f32.store offset=240
    local.get $p0
    local.get $l1
    local.get $p0
    f32.load offset=244
    local.tee $l2
    f32.const 0x0p+0 (;=0;)
    local.get $l2
    local.get $l2
    f32.eq
    select
    local.tee $l2
    local.get $l1
    local.get $l2
    f32.gt
    select
    f32.store offset=244)
