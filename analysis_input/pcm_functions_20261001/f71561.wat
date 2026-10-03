  (func $f71561 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32)
    local.get $p0
    i32.load offset=32
    local.tee $p0
    if $I0
      loop $L1
        local.get $p0
        local.get $p1
        i32.load offset=4
        local.get $p0
        i32.load offset=8
        i32.const 2147483647
        i32.and
        local.tee $l4
        i32.const 5
        i32.shl
        i32.add
        local.tee $l3
        call $f71453
        local.get $l3
        i32.const 0
        i32.store offset=28
        local.get $p2
        i32.load offset=4
        local.get $l4
        i32.const 24
        i32.mul
        i32.add
        local.get $p0
        i32.load offset=40
        i32.const 68
        i32.add
        local.get $l3
        f32.const 0x1p+0 (;=1;)
        call $f70384
        local.get $p0
        i32.load
        local.tee $p0
        br_if $L1
      end
    end)