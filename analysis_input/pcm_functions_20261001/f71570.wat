  (func $f71570 (type $t7) (param $p0 i32)
    block $B0
      local.get $p0
      i32.load offset=156
      i32.const -3
      i32.gt_u
      br_if $B0
      local.get $p0
      i32.load offset=44
      i32.load16_u offset=44
      i32.const 3
      i32.and
      i32.const 3
      i32.eq
      br_if $B0
      local.get $p0
      i32.load8_u offset=153
      i32.const 16
      i32.and
      br_if $B0
      local.get $p0
      i32.load offset=32
      local.tee $p0
      i32.eqz
      br_if $B0
      loop $L1
        local.get $p0
        call $f71455
        local.get $p0
        i32.load
        local.tee $p0
        br_if $L1
      end
    end)