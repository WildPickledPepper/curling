  (func $f72666 (type $t21) (param $p0 i32) (param $p1 f32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32)
    local.get $p0
    i32.const 48
    i32.add
    local.set $l2
    block $B0
      block $B1
        block $B2
          local.get $p0
          i32.load offset=52
          local.tee $l4
          i32.const 30
          i32.shr_u
          i32.const 2
          i32.sub
          br_table $B2 $B0 $B1
        end
        local.get $l2
        i32.load
        i32.load8_u offset=4785
        br_if $B0
      end
      local.get $p0
      local.get $p1
      f32.store offset=140
      return
    end
    local.get $p0
    i32.load offset=56
    local.tee $l3
    i32.eqz
    if $I3
      local.get $p0
      local.get $p0
      i32.load offset=48
      local.get $l4
      i32.const 24
      i32.shr_u
      i32.const 15
      i32.and
      call $f71984
      local.tee $l3
      i32.store offset=56
    end
    local.get $l3
    local.get $p1
    f32.store offset=128
    local.get $p0
    i32.load offset=48
    local.get $l2
    call $f71985
    local.get $p0
    i32.const 316
    i32.add
    local.tee $p0
    local.get $p0
    i32.load
    i32.const 128
    i32.or
    i32.store)
