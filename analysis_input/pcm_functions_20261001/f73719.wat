  (func $f73719 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l2
    global.set $g0
    i32.const 9
    call $f80140
    call $f73714
    local.get $p0
    i32.load offset=40
    if $I0
      local.get $p0
      local.get $p0
      i32.load
      i32.load offset=152
      call_indirect $__indirect_function_table (type $t7)
    end
    local.get $l2
    local.get $p0
    i32.load offset=28
    i32.const 4131408
    call $f80185
    call $f78122
    local.get $l2
    local.get $l2
    f32.load offset=8
    i32.const 4748508
    f32.load
    f32.mul
    f32.store offset=24
    local.get $l2
    local.get $l2
    f32.load offset=4
    i32.const 4748504
    f32.load
    f32.mul
    f32.store offset=20
    local.get $l2
    local.get $l2
    f32.load
    i32.const 4748500
    f32.load
    f32.mul
    f32.store offset=16
    local.get $l2
    i32.const 16
    i32.add
    local.get $p0
    i32.load offset=88
    local.tee $l3
    i32.const 2
    i32.shl
    i32.add
    f32.load
    local.set $l6
    local.get $l2
    i32.const 16
    i32.add
    local.get $l3
    i32.const 1
    i32.add
    i32.const 3
    i32.rem_s
    i32.const 2
    i32.shl
    i32.add
    f32.load
    local.set $l4
    local.get $l2
    i32.const 16
    i32.add
    local.get $l3
    i32.const 2
    i32.add
    i32.const 3
    i32.rem_s
    i32.const 2
    i32.shl
    i32.add
    f32.load
    local.set $l5
    local.get $p0
    f32.load offset=84
    local.set $l7
    local.get $p0
    f32.load offset=80
    local.set $l8
    local.get $l2
    i32.const 2
    i32.store offset=16
    local.get $l2
    local.get $l8
    local.get $l5
    f32.neg
    local.get $l5
    local.get $l5
    f32.const 0x0p+0 (;=0;)
    f32.lt
    select
    local.tee $l5
    local.get $l4
    f32.neg
    local.get $l4
    local.get $l4
    f32.const 0x0p+0 (;=0;)
    f32.lt
    select
    local.tee $l4
    local.get $l4
    local.get $l5
    f32.lt
    select
    f32.mul
    local.tee $l4
    f32.const 0x1.4f8b58p-17 (;=1e-05;)
    f32.max
    f32.store offset=20
    local.get $l2
    local.get $l7
    local.get $l6
    f32.mul
    local.tee $l5
    f32.neg
    local.get $l5
    local.get $l5
    f32.const 0x0p+0 (;=0;)
    f32.lt
    select
    f32.const 0x1.4f8b58p-17 (;=1e-05;)
    f32.max
    local.get $l4
    local.get $l4
    f32.add
    f32.sub
    f32.const 0x1.4f8b58p-17 (;=1e-05;)
    f32.max
    f32.const 0x1p-1 (;=0.5;)
    f32.mul
    f32.store offset=24
    local.get $p0
    local.get $l2
    i32.const 16
    i32.add
    local.get $p1
    call $f73283
    local.get $l2
    i32.const 32
    i32.add
    global.set $g0)
