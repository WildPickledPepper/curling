  (func $f73131 (type $t148) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 f32)
    (local $l6 i32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32)
    global.get $g0
    i32.const 80
    i32.sub
    local.tee $l6
    global.set $g0
    local.get $p1
    local.get $p0
    i32.load offset=176
    i32.eq
    if $I0
      local.get $l6
      i64.const 0
      i64.store offset=40
      local.get $l6
      i64.const 0
      i64.store offset=48
      local.get $l6
      i64.const 0
      i64.store offset=32
      local.get $l6
      i32.const 0
      i32.store16 offset=28
      local.get $l6
      i32.const -1
      i32.store offset=24
      local.get $l6
      i64.const 0
      i64.store offset=16
      local.get $l6
      i32.const 0
      i32.store offset=64
      local.get $l6
      i64.const 2139095039
      i64.store offset=56
      local.get $l6
      i32.const -1
      i32.store offset=12
      local.get $p2
      local.get $l6
      i32.const 16
      i32.add
      local.get $p3
      local.get $p4
      local.get $p5
      local.get $l6
      i32.const 12
      i32.add
      call $f73229
      local.set $p1
      block $B1
        local.get $l6
        i32.load offset=12
        local.tee $p2
        local.get $p0
        i32.load offset=176
        i32.eq
        br_if $B1
        local.get $p1
        i32.eqz
        br_if $B1
        local.get $p0
        local.get $p2
        i32.store offset=176
        local.get $p0
        local.get $l6
        f32.load offset=32
        local.tee $p5
        f32.store offset=228
        local.get $p0
        local.get $l6
        f32.load offset=36
        local.tee $l7
        f32.store offset=232
        local.get $p0
        local.get $l6
        f32.load offset=40
        local.tee $l8
        f32.store offset=236
        local.get $p0
        local.get $p1
        f32.load offset=40
        local.tee $l9
        local.get $p1
        f32.load offset=32
        local.tee $l10
        local.get $p5
        local.get $p1
        f64.load offset=8
        f32.demote_f64
        f32.sub
        local.tee $p5
        local.get $p5
        f32.add
        local.tee $l11
        f32.mul
        local.get $p1
        f32.load offset=36
        local.tee $l12
        local.get $l7
        local.get $p1
        f64.load offset=16
        f32.demote_f64
        f32.sub
        local.tee $p5
        local.get $p5
        f32.add
        local.tee $l7
        f32.mul
        f32.add
        local.get $l9
        local.get $l8
        local.get $p1
        f64.load offset=24
        f32.demote_f64
        f32.sub
        local.tee $p5
        local.get $p5
        f32.add
        local.tee $l8
        f32.mul
        f32.add
        local.tee $l13
        f32.mul
        local.get $l8
        local.get $p1
        f32.load offset=44
        local.tee $p5
        local.get $p5
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.tee $l14
        f32.mul
        local.get $p5
        local.get $l10
        local.get $l7
        f32.mul
        local.get $l11
        local.get $l12
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        f32.store offset=224
        local.get $p0
        local.get $l12
        local.get $l13
        f32.mul
        local.get $l7
        local.get $l14
        f32.mul
        local.get $p5
        local.get $l11
        local.get $l9
        f32.mul
        local.get $l10
        local.get $l8
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        f32.store offset=220
        local.get $p0
        local.get $l10
        local.get $l13
        f32.mul
        local.get $l11
        local.get $l14
        f32.mul
        local.get $p5
        local.get $l12
        local.get $l8
        f32.mul
        local.get $l7
        local.get $l9
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
      global.set $g0
      return
    end
    local.get $l6
    i32.const 80
    i32.add
    global.set $g0)
