  (func $f70527 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32)
    local.get $p0
    i32.load offset=148
    local.tee $l4
    i32.load offset=20
    local.set $l9
    local.get $l4
    i32.load offset=16
    local.set $l10
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $l2
    i64.const 0
    i64.store offset=40
    local.get $l2
    i64.const 0
    i64.store offset=32
    local.get $l2
    i64.const 0
    i64.store offset=24
    local.get $l2
    i64.const 0
    i64.store offset=16
    local.get $p1
    f32.load
    local.set $l14
    local.get $p1
    f32.load offset=4
    local.set $l15
    local.get $l2
    local.get $p1
    f32.load offset=8
    local.tee $l16
    f32.store offset=8
    local.get $l2
    local.get $l15
    f32.store offset=4
    local.get $l2
    local.get $l14
    f32.store
    local.get $l16
    i32.reinterpret_f32
    i32.const 2147483647
    i32.and
    local.set $l3
    local.get $l4
    i32.load16_u
    local.set $p1
    block $B0 (result i32)
      block $B1
        local.get $l15
        i32.reinterpret_f32
        i32.const 2147483647
        i32.and
        local.tee $l5
        local.get $l14
        i32.reinterpret_f32
        i32.const 2147483647
        i32.and
        local.tee $l6
        i32.le_u
        br_if $B1
        local.get $l3
        local.get $l5
        i32.ge_u
        br_if $B1
        local.get $l2
        i32.const 8
        i32.add
        local.set $l5
        i32.const 1
        local.set $l3
        local.get $l2
        br $B0
      end
      local.get $l3
      local.get $l6
      i32.le_u
      if $I2
        local.get $l2
        i32.const 4
        i32.or
        local.set $l5
        i32.const 0
        local.set $l3
        local.get $l2
        i32.const 8
        i32.add
        br $B0
      end
      i32.const 2
      local.set $l3
      local.get $l2
      local.set $l5
      local.get $l2
      i32.const 4
      i32.or
    end
    local.set $l6
    local.get $l3
    i32.const 1
    i32.shl
    local.get $l2
    local.get $l3
    i32.const 2
    i32.shl
    i32.add
    f32.load
    local.tee $l13
    i32.reinterpret_f32
    i32.const 31
    i32.shr_u
    i32.or
    local.get $p1
    i32.mul
    block $B3 (result i32)
      local.get $p1
      i32.const 1
      i32.sub
      f32.convert_i32_u
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l17
      local.get $l5
      f32.load
      f32.const 0x1p+0 (;=1;)
      local.get $l13
      f32.abs
      f32.div
      local.tee $l18
      f32.mul
      f32.const 0x1p+0 (;=1;)
      f32.add
      f32.mul
      f32.const 0x1p-1 (;=0.5;)
      f32.add
      local.tee $l13
      f32.const 0x1p+32 (;=4.29497e+09;)
      f32.lt
      local.get $l13
      f32.const 0x0p+0 (;=0;)
      f32.ge
      i32.and
      if $I4
        local.get $l13
        i32.trunc_f32_u
        br $B3
      end
      i32.const 0
    end
    i32.add
    local.get $p1
    i32.mul
    local.set $p1
    block $B5 (result i32)
      local.get $l17
      local.get $l18
      local.get $l6
      f32.load
      f32.mul
      f32.const 0x1p+0 (;=1;)
      f32.add
      f32.mul
      f32.const 0x1p-1 (;=0.5;)
      f32.add
      local.tee $l13
      f32.const 0x1p+32 (;=4.29497e+09;)
      f32.lt
      local.get $l13
      f32.const 0x0p+0 (;=0;)
      f32.ge
      i32.and
      if $I6
        local.get $l13
        i32.trunc_f32_u
        br $B5
      end
      i32.const 0
    end
    local.set $l3
    local.get $l14
    local.get $p0
    i32.load offset=152
    local.tee $l6
    local.get $l4
    i32.load offset=4
    local.get $p1
    local.get $l3
    i32.add
    i32.add
    i32.load8_u
    local.tee $l7
    i32.const 12
    i32.mul
    i32.add
    local.tee $p1
    f32.load
    f32.mul
    local.get $l15
    local.get $p1
    f32.load offset=4
    f32.mul
    f32.add
    local.get $l16
    local.get $p1
    f32.load offset=8
    f32.mul
    f32.add
    local.set $l13
    loop $L7
      local.get $l10
      local.get $l7
      local.tee $l8
      i32.const 2
      i32.shl
      i32.add
      local.tee $p1
      i32.load16_u
      local.tee $l3
      if $I8
        local.get $p1
        i32.load16_u offset=2
        local.set $l5
        i32.const 0
        local.set $p1
        loop $L9
          block $B10
            local.get $l14
            local.get $l6
            local.get $l9
            local.get $p1
            local.get $l5
            i32.add
            i32.add
            i32.load8_u
            local.tee $p0
            i32.const 12
            i32.mul
            i32.add
            local.tee $l4
            f32.load
            f32.mul
            local.get $l15
            local.get $l4
            f32.load offset=4
            f32.mul
            f32.add
            local.get $l16
            local.get $l4
            f32.load offset=8
            f32.mul
            f32.add
            local.tee $l17
            local.get $l13
            f32.gt
            i32.eqz
            br_if $B10
            local.get $l2
            i32.const 16
            i32.add
            local.get $p0
            i32.const 3
            i32.shr_u
            i32.const 28
            i32.and
            i32.add
            local.tee $l4
            i32.load
            local.tee $l11
            i32.const 1
            local.get $p0
            i32.shl
            local.tee $l12
            i32.and
            br_if $B10
            local.get $l4
            local.get $l11
            local.get $l12
            i32.or
            i32.store
            local.get $l17
            local.set $l13
            local.get $p0
            local.set $l7
          end
          local.get $p1
          i32.const 1
          i32.add
          local.tee $p1
          local.get $l3
          i32.ne
          br_if $L9
        end
        local.get $l7
        local.get $l8
        i32.ne
        br_if $L7
      end
    end
    local.get $l8)