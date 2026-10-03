  (func $f60121 (type $t47) (param $p0 i32) (param $p1 f32) (param $p2 f32) (param $p3 i32) (result i32)
    (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i64)
    i32.const 4674458
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3752504
      call $f1661
      i32.const 3746096
      call $f1661
      i32.const 4674458
      i32.const 1
      i32.store8
    end
    i32.const 3746096
    i32.load
    i32.const 8
    call $f1052
    local.tee $l7
    i64.const 4601778100106166272
    i64.store offset=72
    local.get $l7
    i32.const -64
    i32.sub
    i64.const 4583581518741120795
    i64.store
    local.get $l7
    i64.const 4583581520888604443
    i64.store offset=56
    local.get $l7
    i64.const 4559011916738985984
    i64.store offset=48
    local.get $l7
    i64.const 1061477679
    i64.store offset=40
    local.get $l7
    i64.const 3208961327
    i64.store offset=32
    local.get $l7
    i64.const 0
    i64.store offset=24
    local.get $l7
    i64.const -4664360120115789824
    i64.store offset=16
    i32.const 0
    local.set $p3
    loop $L1
      local.get $p0
      i32.load offset=124
      i32.load offset=28
      local.get $p3
      local.tee $l9
      i32.const 3
      i32.shl
      i32.add
      f32.load offset=16
      local.set $l4
      i32.const 3752504
      i32.load
      local.tee $p3
      i32.load offset=116
      i32.eqz
      if $I2
        local.get $p3
        call $f65192
      end
      local.get $l9
      i32.const 1
      i32.shl
      local.set $p3
      block $B3
        block $B4
          local.get $l4
          f32.abs
          f32.const 0x1.0c6f7ap-20 (;=1e-06;)
          f32.gt
          if $I5
            local.get $p3
            i32.const 1
            i32.or
            local.set $l10
            br $B4
          end
          local.get $p0
          i32.load offset=124
          i32.load offset=28
          local.get $p3
          i32.const 1
          i32.or
          local.tee $l10
          i32.const 2
          i32.shl
          i32.add
          f32.load offset=16
          local.set $l4
          i32.const 3752504
          i32.load
          local.tee $l11
          i32.load offset=116
          i32.eqz
          if $I6
            local.get $l11
            call $f65192
          end
          local.get $l4
          f32.abs
          f32.const 0x1.0c6f7ap-20 (;=1e-06;)
          f32.gt
          i32.eqz
          br_if $B3
        end
        local.get $p0
        i32.load offset=124
        i32.load offset=28
        i32.const 16
        i32.add
        local.tee $l11
        local.get $l10
        i32.const 2
        i32.shl
        i32.add
        f32.load
        local.set $l4
        local.get $l11
        local.get $p3
        i32.const 2
        i32.shl
        i32.add
        f32.load
        local.set $l5
        local.get $l7
        local.get $l9
        i32.const 2
        i32.shl
        i32.add
        i64.load offset=16
        local.tee $l12
        i32.wrap_i64
        local.set $p3
        local.get $l12
        i64.const 32
        i64.shr_u
        i32.wrap_i64
        local.set $l10
        i32.const 4675188
        i32.load8_u
        i32.eqz
        if $I7
          i32.const 3752504
          call $f1661
          i32.const 4675188
          i32.const 1
          i32.store8
        end
        local.get $p3
        f32.reinterpret_i32
        local.set $l6
        i32.const 3752504
        i32.load
        local.tee $p3
        i32.load offset=116
        i32.eqz
        if $I8
          local.get $p3
          call $f65192
        end
        local.get $p1
        local.get $l5
        local.get $l6
        f32.sub
        local.tee $l5
        local.get $l5
        f32.mul
        local.get $l4
        local.get $l10
        f32.reinterpret_i32
        f32.sub
        local.tee $l4
        local.get $l4
        f32.mul
        f32.add
        f32.sqrt
        local.tee $l4
        f32.ge
        if $I9
          local.get $l8
          i32.const 2
          i32.add
          local.set $l8
          br $B3
        end
        local.get $p2
        local.get $l4
        f32.ge
        i32.eqz
        br_if $B3
        local.get $l8
        i32.const 1
        i32.add
        local.set $l8
      end
      local.get $l9
      i32.const 2
      i32.add
      local.set $p3
      local.get $l9
      i32.const 14
      i32.lt_u
      br_if $L1
    end
    local.get $l8
    i32.const 10
    local.get $l8
    i32.const 10
    i32.lt_s
    select)
