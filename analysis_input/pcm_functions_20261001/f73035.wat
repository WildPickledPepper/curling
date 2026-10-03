  (func $f73035 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 f32) (local $l4 f32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32)
    global.get $g0
    i32.const 112
    i32.sub
    local.tee $l2
    global.set $g0
    block $B0
      local.get $p0
      i32.load offset=52
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load8_u offset=133
      if $I1
        local.get $p0
        i32.load offset=4
        local.set $p0
        local.get $l2
        i32.const 403047
        i32.store offset=108
        local.get $l2
        i32.const 403047
        i32.store offset=104
        local.get $l2
        i64.const 0
        i64.store offset=96
        local.get $l2
        i32.const 1
        i32.store8 offset=92
        local.get $l2
        i32.const 403047
        i32.store offset=60
        local.get $l2
        i32.const 403047
        i32.store offset=56
        local.get $l2
        i32.const 403047
        i32.store offset=52
        local.get $l2
        i64.const 0
        i64.store offset=84 align=4
        local.get $l2
        local.get $p0
        i32.store offset=80
        local.get $l2
        i32.const 512
        i32.store offset=76
        local.get $l2
        i64.const -4294966121
        i64.store offset=68 align=4
        local.get $l2
        i32.const 403047
        i32.store offset=64
        local.get $l2
        i32.const 269392
        i32.store offset=48
        local.get $l2
        i32.const 48
        i32.add
        call $f83275
        br $B0
      end
      i32.const 9
      call $f80140
      call $f73714
      local.get $p1
      f32.load
      local.set $l3
      local.get $p1
      f32.load offset=4
      local.set $l4
      local.get $l2
      local.get $p1
      f32.load offset=8
      local.tee $l5
      f32.store offset=40
      local.get $l2
      local.get $l4
      f32.store offset=36
      local.get $l2
      local.get $l3
      f32.store offset=32
      local.get $p0
      i32.load8_u offset=136
      i32.const 112
      i32.and
      if $I2
        local.get $l2
        i32.const 16
        i32.add
        local.get $p0
        i32.load offset=28
        i32.const 4131408
        call $f80185
        local.tee $p1
        call $f78093
        local.get $l2
        local.get $p1
        call $f78150
        local.get $l2
        f32.load offset=4
        local.set $l6
        local.get $l2
        f32.load
        local.set $l7
        local.get $l2
        f32.load offset=12
        local.set $l8
        local.get $l2
        f32.load offset=8
        local.set $l9
        local.get $l2
        i32.const 48
        i32.add
        local.get $p0
        i32.load offset=52
        local.tee $p1
        local.get $p1
        i32.load
        i32.load offset=112
        call_indirect $__indirect_function_table (type $t1)
        local.get $l2
        local.get $l7
        local.get $l2
        f32.load offset=52
        local.tee $l11
        f32.mul
        local.get $l8
        local.get $l2
        f32.load offset=56
        local.tee $l12
        f32.mul
        local.get $l9
        local.get $l2
        f32.load offset=60
        local.tee $l13
        f32.mul
        f32.add
        f32.add
        local.get $l6
        local.get $l2
        f32.load offset=48
        local.tee $l14
        f32.mul
        f32.sub
        local.tee $l10
        local.get $l10
        f32.const 0x0p+0 (;=0;)
        local.get $l10
        local.get $l10
        local.get $l5
        local.get $l5
        f32.add
        local.tee $l15
        f32.mul
        local.get $l6
        local.get $l12
        f32.mul
        local.get $l8
        local.get $l14
        f32.mul
        local.get $l7
        local.get $l13
        f32.mul
        f32.add
        f32.add
        local.get $l11
        local.get $l9
        f32.mul
        f32.sub
        local.tee $l5
        local.get $l3
        local.get $l3
        f32.add
        local.tee $l16
        f32.mul
        local.get $l9
        local.get $l14
        f32.mul
        local.get $l8
        local.get $l11
        f32.mul
        local.get $l6
        local.get $l13
        f32.mul
        f32.add
        f32.add
        local.get $l12
        local.get $l7
        f32.mul
        f32.sub
        local.tee $l3
        local.get $l4
        local.get $l4
        f32.add
        local.tee $l17
        f32.mul
        f32.add
        f32.add
        local.tee $l18
        f32.mul
        local.get $l15
        local.get $l8
        local.get $l13
        f32.mul
        local.get $l14
        local.get $l7
        f32.mul
        f32.sub
        local.get $l6
        local.get $l11
        f32.mul
        f32.sub
        local.get $l9
        local.get $l12
        f32.mul
        f32.sub
        local.tee $l4
        local.get $l4
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.tee $l6
        f32.mul
        local.get $l4
        local.get $l5
        local.get $l17
        f32.mul
        local.get $l16
        local.get $l3
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        local.tee $l7
        local.get $l7
        f32.add
        local.get $p0
        i32.load offset=136
        local.tee $p1
        i32.const 64
        i32.and
        select
        local.tee $l7
        f32.mul
        local.get $l5
        f32.const 0x0p+0 (;=0;)
        local.get $l5
        local.get $l18
        f32.mul
        local.get $l16
        local.get $l6
        f32.mul
        local.get $l4
        local.get $l3
        local.get $l15
        f32.mul
        local.get $l17
        local.get $l10
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        local.tee $l8
        local.get $l8
        f32.add
        local.get $p1
        i32.const 16
        i32.and
        select
        local.tee $l8
        f32.mul
        local.get $l3
        f32.const 0x0p+0 (;=0;)
        local.get $l3
        local.get $l18
        f32.mul
        local.get $l17
        local.get $l6
        f32.mul
        local.get $l4
        local.get $l10
        local.get $l16
        f32.mul
        local.get $l15
        local.get $l5
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        local.tee $l9
        local.get $l9
        f32.add
        local.get $p1
        i32.const 32
        i32.and
        select
        local.tee $l9
        f32.mul
        f32.add
        f32.add
        local.tee $l11
        f32.mul
        local.get $l7
        local.get $l6
        f32.mul
        local.get $l4
        local.get $l5
        local.get $l9
        f32.mul
        local.get $l8
        local.get $l3
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        f32.store offset=40
        local.get $l2
        local.get $l3
        local.get $l11
        f32.mul
        local.get $l9
        local.get $l6
        f32.mul
        local.get $l4
        local.get $l10
        local.get $l8
        f32.mul
        local.get $l7
        local.get $l5
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        f32.store offset=36
        local.get $l2
        local.get $l5
        local.get $l11
        f32.mul
        local.get $l8
        local.get $l6
        f32.mul
        local.get $l4
        local.get $l3
        local.get $l7
        f32.mul
        local.get $l9
        local.get $l10
        f32.mul
        f32.sub
        f32.mul
        f32.add
        f32.add
        f32.store offset=32
      end
      local.get $p0
      i32.load offset=52
      local.tee $p0
      local.get $l2
      i32.const 32
      i32.add
      i32.const 1
      local.get $p0
      i32.load
      i32.load offset=168
      call_indirect $__indirect_function_table (type $t2)
    end
    local.get $l2
    i32.const 112
    i32.add
    global.set $g0)