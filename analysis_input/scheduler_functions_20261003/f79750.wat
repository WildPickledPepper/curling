  (func $f79750 (type $t121) (param $p0 i32) (param $p1 f64)
    (local $l2 f32) (local $l3 f32) (local $l4 f64) (local $l5 f64) (local $l6 f64) (local $l7 i32) (local $l8 i32)
    local.get $p0
    local.get $p0
    i64.load offset=184
    i64.const 1
    i64.add
    i64.store offset=184
    local.get $p0
    local.get $p0
    i32.load offset=192
    i32.const 1
    i32.add
    i32.store offset=192
    block $B0
      local.get $p0
      i32.load8_u offset=232
      br_if $B0
      f32.const 0x1.4f8b58p-17 (;=1e-05;)
      local.set $l2
      local.get $p0
      local.get $p1
      local.get $p0
      f64.load offset=216
      f64.sub
      local.tee $l4
      local.get $p0
      f64.load offset=96
      f64.sub
      f32.demote_f64
      local.tee $l3
      f32.const 0x1.4f8b58p-17 (;=1e-05;)
      f32.lt
      if $I1 (result f32)
        local.get $l2
      else
        local.get $p0
        local.get $l4
        f64.store offset=96
        local.get $l3
      end
      f32.store offset=108
      block $B2
        local.get $p0
        f32.load offset=200
        local.tee $l2
        f32.const 0x0p+0 (;=0;)
        f32.gt
        if $I3
          local.get $p0
          f64.load offset=80
          local.tee $l5
          local.get $l2
          local.get $p0
          f32.load offset=236
          f32.mul
          f64.promote_f32
          f64.add
          local.set $l4
          local.get $p0
          i32.load8_u offset=177
          i32.eqz
          local.set $l8
          br $B2
        end
        local.get $p0
        i32.load8_u offset=176
        if $I4
          local.get $p0
          i32.const 0
          i32.store8 offset=176
          return
        end
        local.get $p0
        f64.load offset=80
        local.set $l5
        local.get $p0
        i32.load8_u offset=177
        if $I5
          local.get $l5
          local.get $p0
          f32.load offset=236
          f32.const 0x1.47ae14p-6 (;=0.02;)
          f32.mul
          f64.promote_f32
          f64.add
          local.set $l4
          br $B2
        end
        local.get $p1
        local.get $p0
        f64.load offset=208
        f64.sub
        local.tee $l4
        local.get $l5
        f64.sub
        local.tee $l6
        local.get $p0
        f32.load offset=240
        local.tee $l2
        f64.promote_f32
        f64.gt
        if $I6
          local.get $l5
          local.get $l2
          local.get $p0
          f32.load offset=236
          f32.mul
          f64.promote_f32
          f64.add
          local.set $l4
          i32.const 1
          local.set $l8
          br $B2
        end
        local.get $p0
        f32.load offset=236
        local.set $l2
        local.get $l6
        f64.const 0x1.4f8b58p-17 (;=1e-05;)
        f64.lt
        if $I7
          local.get $l5
          local.get $l2
          f32.const 0x1.4f8b58p-17 (;=1e-05;)
          f32.mul
          f64.promote_f32
          f64.add
          local.set $l4
          i32.const 1
          local.set $l8
          br $B2
        end
        i32.const 1
        local.set $l8
        local.get $l2
        f32.const -0x1p+0 (;=-1;)
        f32.add
        local.tee $l3
        f32.neg
        local.get $l3
        local.get $l3
        f32.const 0x0p+0 (;=0;)
        f32.lt
        select
        f32.const 0x1.0c6f7ap-20 (;=1e-06;)
        f32.le
        br_if $B2
        local.get $l5
        local.get $l2
        local.get $l6
        f32.demote_f64
        f32.mul
        f64.promote_f32
        f64.add
        local.set $l4
      end
      local.get $p0
      local.get $l4
      f64.store offset=80
      local.get $p0
      local.get $l5
      f64.store offset=88
      local.get $p0
      local.get $l4
      local.get $l5
      f64.sub
      f32.demote_f64
      local.tee $l2
      f32.store offset=104
      local.get $p0
      f32.const 0x1p+0 (;=1;)
      local.get $l2
      f32.div
      f32.const 0x1p+0 (;=1;)
      local.get $l2
      f32.const 0x1.4f8b58p-17 (;=1e-05;)
      f32.gt
      select
      f32.store offset=120
      local.get $p0
      i32.const 116
      i32.add
      local.tee $l7
      local.get $l7
      f32.load
      f32.const 0x1.99999ap-1 (;=0.8;)
      f32.mul
      f32.const 0x1.99999ap-3 (;=0.2;)
      f32.add
      local.tee $l3
      f32.store
      local.get $p0
      i32.const 112
      i32.add
      local.tee $l7
      local.get $l2
      f32.const 0x1.99999ap-3 (;=0.2;)
      local.get $l3
      f32.div
      local.tee $l3
      f32.mul
      local.get $l7
      f32.load
      f32.const 0x1p+0 (;=1;)
      local.get $l3
      f32.sub
      f32.mul
      f32.add
      f32.store
      local.get $p0
      local.get $p0
      i32.const 80
      i32.add
      local.tee $l7
      i64.load
      i64.store offset=128
      local.get $p0
      local.get $l7
      i64.load offset=8
      i64.store offset=136
      local.get $p0
      local.get $l7
      i64.load offset=16
      i64.store offset=144
      local.get $p0
      local.get $l7
      i64.load offset=24
      i64.store offset=152
      local.get $p0
      local.get $l7
      i64.load offset=32
      i64.store offset=160
      local.get $p0
      local.get $l7
      i32.load offset=40
      i32.store offset=168
      local.get $p0
      local.get $p1
      local.get $l4
      f64.sub
      f64.store offset=208
      local.get $l8
      br_if $B0
      local.get $p0
      i32.const 0
      i32.store offset=116
      local.get $p0
      i32.const 0
      i32.store8 offset=177
    end)
