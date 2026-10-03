  (func $f71661 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32)
    local.get $p0
    i32.load offset=28
    if $I0
      loop $L1
        local.get $p0
        i32.load offset=24
        local.get $l2
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.get $p1
        call $f71557
        local.get $l2
        i32.const 1
        i32.add
        local.tee $l2
        local.get $p0
        i32.load offset=28
        i32.lt_u
        br_if $L1
      end
    end)