  (func $f71692 (type $t18) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (result i32)
    (local $l8 i32) (local $l9 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l8
    global.set $g0
    block $B0
      local.get $p1
      i32.load8_u
      i32.const 2
      i32.and
      i32.eqz
      if $I1
        local.get $p1
        i32.load16_u offset=2
        local.set $l9
        local.get $p7
        i32.eqz
        if $I2
          local.get $l8
          local.get $l9
          i32.store16 offset=8
          local.get $p0
          local.get $p2
          local.get $p3
          local.get $l8
          i32.const 8
          i32.add
          local.get $p4
          local.get $p5
          call $f71700
          local.set $p6
          br $B0
        end
        local.get $p3
        i32.load offset=40
        i32.const -64
        i32.sub
        i32.load8_u
        i32.const 4
        i32.and
        local.set $p7
        local.get $p0
        i32.const 1276
        i32.add
        i32.load
        local.tee $p6
        i32.eqz
        if $I3
          local.get $p0
          i32.const 988
          i32.add
          call $f71701
          local.get $p0
          i32.load offset=1276
          local.set $p6
        end
        local.get $p0
        local.get $p6
        i32.load
        i32.store offset=1276
        local.get $p0
        i32.const 1268
        i32.add
        local.tee $p4
        local.get $p4
        i32.load
        i32.const 1
        i32.add
        i32.store
        local.get $p6
        local.get $p3
        local.get $p2
        local.get $p7
        select
        local.get $p2
        local.get $p3
        local.get $p7
        select
        call $f71462
        local.get $p6
        local.get $p6
        i32.load16_u offset=56
        i32.const 65504
        i32.and
        local.get $l9
        i32.const 20
        i32.and
        i32.or
        i32.store16 offset=56
        br $B0
      end
      local.get $p6
      local.set $p7
      local.get $p6
      i32.eqz
      if $I4
        local.get $p0
        i32.const 1860
        i32.add
        i32.load
        local.tee $p7
        i32.eqz
        if $I5
          local.get $p0
          i32.const 1572
          i32.add
          call $f71702
          local.get $p0
          i32.load offset=1860
          local.set $p7
        end
        local.get $p0
        local.get $p7
        i32.load
        i32.store offset=1860
        local.get $p0
        i32.const 1852
        i32.add
        local.tee $p4
        local.get $p4
        i32.load
        i32.const 1
        i32.add
        i32.store
      end
      local.get $p7
      local.get $p2
      local.get $p3
      local.get $p6
      i32.const 0
      i32.ne
      call $f71703
      local.set $p6
    end
    local.get $p1
    i32.load offset=4
    i32.const -1
    i32.ne
    if $I6
      local.get $p6
      i32.const 25
      i32.add
      local.tee $p3
      local.get $p3
      i32.load8_u
      i32.const 16
      i32.or
      i32.store8
      local.get $p0
      i32.load offset=108
      i32.load
      local.get $p1
      i32.load offset=4
      i32.const 2
      i32.shl
      i32.add
      local.get $p6
      i32.store
      local.get $p6
      local.get $p1
      i32.load offset=4
      i32.store offset=36
    end
    local.get $l8
    i32.const 16
    i32.add
    global.set $g0
    local.get $p6)