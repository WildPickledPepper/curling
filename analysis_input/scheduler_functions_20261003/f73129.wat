  (func $f73129 (type $t148) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 f32)
    (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 i64) (local $l23 f64) (local $l24 f64) (local $l25 f64)
    global.get $g0
    i32.const 80
    i32.sub
    local.tee $l6
    global.set $g0
    local.get $l6
    local.get $p1
    i32.store offset=76
    block $B0
      local.get $p0
      i32.load offset=176
      i32.const -1
      i32.eq
      br_if $B0
      local.get $l6
      i32.const 32
      i32.add
      local.tee $l12
      i64.const 0
      i64.store
      local.get $l6
      i64.const 0
      i64.store offset=40
      local.get $l6
      i64.const 0
      i64.store offset=24
      local.get $l6
      i32.const 0
      i32.store16 offset=20
      local.get $l6
      i32.const -1
      i32.store offset=16
      local.get $l6
      i64.const 0
      i64.store offset=8
      local.get $l6
      i32.const 0
      i32.store offset=56
      local.get $l6
      i64.const 2139095039
      i64.store offset=48
      local.get $l6
      i32.const 8
      i32.add
      local.set $l9
      global.get $g0
      i32.const -64
      i32.add
      local.tee $p1
      global.set $g0
      block $B1
        local.get $l6
        i32.load offset=76
        local.tee $l13
        i32.const 65535
        i32.and
        local.tee $l7
        local.get $p2
        i32.load offset=36
        local.tee $l8
        i32.ge_u
        br_if $B1
        local.get $p2
        i32.load offset=40
        local.get $l7
        i32.const 1
        i32.shl
        i32.add
        i32.load16_u
        local.tee $l10
        i32.const 65535
        i32.eq
        br_if $B1
        local.get $l8
        local.get $l10
        i32.le_u
        br_if $B1
        local.get $p2
        i32.load offset=48
        local.get $l7
        i32.const 1
        i32.shl
        i32.add
        i32.load16_u
        local.get $l13
        i32.const 16
        i32.shr_u
        i32.ne
        br_if $B1
        local.get $p2
        i32.load offset=28
        local.get $l10
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l7
        i32.eqz
        br_if $B1
        local.get $l7
        i32.const 16
        i32.shr_u
        local.set $l8
        local.get $l7
        i32.const 65535
        i32.and
        i32.const 4
        i32.eq
        if $I2
          i32.const 4117116
          i32.load
          local.set $l7
          local.get $p2
          i32.load offset=4
          local.get $l8
          i32.const 72
          i32.mul
          i32.add
          local.tee $p2
          i64.load offset=56 align=4
          local.set $l22
          local.get $p1
          local.get $p2
          i32.const -64
          i32.sub
          f32.load
          f32.store offset=60
          local.get $p1
          local.get $l22
          i64.store offset=52 align=4
          local.get $p1
          i32.const 3
          i32.store offset=48
          local.get $p2
          f64.load offset=16
          local.set $l23
          local.get $p2
          f64.load offset=24
          local.set $l24
          local.get $p2
          f64.load offset=32
          local.set $l25
          local.get $p1
          local.get $p2
          f32.load offset=40
          f32.store offset=16
          local.get $p1
          local.get $p2
          f32.load offset=44
          f32.store offset=20
          local.get $p1
          local.get $p2
          f32.load offset=48
          f32.store offset=24
          local.get $p2
          f32.load offset=52
          local.set $l14
          local.get $p1
          local.get $l25
          f32.demote_f64
          f32.store offset=40
          local.get $p1
          local.get $l24
          f32.demote_f64
          f32.store offset=36
          local.get $p1
          local.get $l23
          f32.demote_f64
          f32.store offset=32
          local.get $p1
          local.get $l14
          f32.store offset=28
          local.get $p1
          i32.const 0
          i32.store16 offset=8
          local.get $p1
          i32.const 48
          i32.add
          local.get $p1
          i32.const 16
          i32.add
          local.get $p3
          local.get $p4
          local.get $p5
          local.get $p1
          i32.const 8
          i32.add
          i32.const 1
          local.get $l9
          local.get $l7
          call_indirect $__indirect_function_table (type $t108)
          i32.eqz
          br_if $B1
          local.get $p2
          i32.const 8
          i32.add
          local.set $l11
          br $B1
        end
        i32.const 4117112
        i32.load
        local.set $l7
        local.get $p2
        i32.load offset=16
        local.get $l8
        i32.const 6
        i32.shl
        i32.add
        local.tee $p2
        i64.load offset=56
        local.set $l22
        local.get $p1
        i32.const 2
        i32.store offset=48
        local.get $p1
        local.get $l22
        i64.const 32
        i64.rotl
        i64.store offset=52 align=4
        local.get $p2
        f64.load offset=16
        local.set $l23
        local.get $p2
        f64.load offset=24
        local.set $l24
        local.get $p2
        f64.load offset=32
        local.set $l25
        local.get $p1
        local.get $p2
        f32.load offset=40
        f32.store offset=16
        local.get $p1
        local.get $p2
        f32.load offset=44
        f32.store offset=20
        local.get $p1
        local.get $p2
        f32.load offset=48
        f32.store offset=24
        local.get $p2
        f32.load offset=52
        local.set $l14
        local.get $p1
        local.get $l25
        f32.demote_f64
        f32.store offset=40
        local.get $p1
        local.get $l24
        f32.demote_f64
        f32.store offset=36
        local.get $p1
        local.get $l23
        f32.demote_f64
        f32.store offset=32
        local.get $p1
        local.get $l14
        f32.store offset=28
        local.get $p1
        i32.const 0
        i32.store16
        local.get $p1
        i32.const 48
        i32.add
        local.get $p1
        i32.const 16
        i32.add
        local.get $p3
        local.get $p4
        local.get $p5
        local.get $p1
        i32.const 1
        local.get $l9
        local.get $l7
        call_indirect $__indirect_function_table (type $t108)
        i32.eqz
        br_if $B1
        local.get $p2
        i32.const 8
        i32.add
        local.set $l11
      end
      local.get $p1
      i32.const -64
      i32.sub
      global.set $g0
      local.get $l11
      local.tee $p1
      i32.eqz
      br_if $B0
      local.get $l6
      f32.load offset=24
      local.tee $p5
      local.get $p4
      f32.load
      local.tee $l16
      f32.mul
      local.get $l6
      f32.load offset=28
      local.tee $l14
      local.get $p4
      f32.load offset=4
      local.tee $l17
      f32.mul
      f32.add
      local.get $l12
      f32.load
      local.tee $l15
      local.get $p4
      f32.load offset=8
      local.tee $l18
      f32.mul
      f32.add
      local.get $l16
      local.get $p0
      f32.load offset=228
      f32.mul
      local.get $l17
      local.get $p0
      f32.load offset=232
      f32.mul
      f32.add
      local.get $l18
      local.get $p0
      f32.load offset=236
      f32.mul
      f32.add
      f32.lt
      i32.eqz
      br_if $B0
      local.get $l6
      i32.load offset=76
      local.set $p4
      local.get $p0
      local.get $l15
      f32.store offset=236
      local.get $p0
      local.get $l14
      f32.store offset=232
      local.get $p0
      local.get $p5
      f32.store offset=228
      local.get $p0
      local.get $p4
      i32.store offset=176
      local.get $p0
      local.get $p1
      f32.load offset=40
      local.tee $l16
      local.get $p1
      f32.load offset=32
      local.tee $l17
      local.get $p5
      local.get $p1
      f64.load offset=8
      f32.demote_f64
      f32.sub
      local.tee $p5
      local.get $p5
      f32.add
      local.tee $l18
      f32.mul
      local.get $p1
      f32.load offset=36
      local.tee $l19
      local.get $l14
      local.get $p1
      f64.load offset=16
      f32.demote_f64
      f32.sub
      local.tee $p5
      local.get $p5
      f32.add
      local.tee $l14
      f32.mul
      f32.add
      local.get $l16
      local.get $l15
      local.get $p1
      f64.load offset=24
      f32.demote_f64
      f32.sub
      local.tee $p5
      local.get $p5
      f32.add
      local.tee $l15
      f32.mul
      f32.add
      local.tee $l20
      f32.mul
      local.get $l15
      local.get $p1
      f32.load offset=44
      local.tee $p5
      local.get $p5
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l21
      f32.mul
      local.get $p5
      local.get $l17
      local.get $l14
      f32.mul
      local.get $l18
      local.get $l19
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      f32.store offset=224
      local.get $p0
      local.get $l19
      local.get $l20
      f32.mul
      local.get $l14
      local.get $l21
      f32.mul
      local.get $p5
      local.get $l18
      local.get $l16
      f32.mul
      local.get $l17
      local.get $l15
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      f32.store offset=220
      local.get $p0
      local.get $l17
      local.get $l20
      f32.mul
      local.get $l18
      local.get $l21
      f32.mul
      local.get $p5
      local.get $l19
      local.get $l15
      f32.mul
      local.get $l14
      local.get $l16
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      f32.store offset=216
    end
    local.get $l6
    i32.const 80
    i32.add
    global.set $g0)
