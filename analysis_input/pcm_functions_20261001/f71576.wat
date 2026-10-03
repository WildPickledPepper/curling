  (func $f71576 (type $t1) (param $p0 i32) (param $p1 i32)
    local.get $p0
    i32.load offset=32
    local.tee $p0
    if $I0
      loop $L1
        local.get $p0
        i32.const 1
        local.get $p1
        call $f71458
        local.get $p0
        call $f71456
        local.get $p0
        i32.load
        local.tee $p0
        br_if $L1
      end
    end)