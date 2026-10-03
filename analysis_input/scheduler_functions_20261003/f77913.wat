  (func $f77913 (type $t19) (result i32)
    (local $l0 i32) (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 f64) (local $l5 f64) (local $l6 f64) (local $l7 f32)
    block $B0 (result i32)
      i32.const 7
      call $f80140
      local.tee $l0
      f64.load offset=32
      local.tee $l4
      local.get $l0
      f32.load offset=56
      f64.promote_f32
      f64.add
      local.tee $l5
      local.get $l0
      f64.load offset=80
      local.tee $l6
      f64.gt
      i32.eqz
      local.get $l0
      i32.load8_u offset=178
      local.tee $l2
      i32.const 0
      i32.ne
      i32.or
      local.tee $l3
      i32.eqz
      if $I1
        local.get $l0
        i32.const 0
        i32.store8 offset=233
        local.get $l0
        local.get $l0
        i64.load offset=80
        i64.store offset=128
        local.get $l0
        local.get $l0
        i32.load offset=120
        i32.store offset=168
        local.get $l0
        local.get $l0
        i64.load offset=112
        i64.store offset=160
        local.get $l0
        local.get $l0
        i64.load offset=104
        i64.store offset=152
        local.get $l0
        local.get $l0
        i64.load offset=96
        i64.store offset=144
        local.get $l0
        local.get $l0
        i64.load offset=88
        i64.store offset=136
        local.get $l3
        br $B0
      end
      local.get $l0
      local.get $l4
      f64.store offset=40
      local.get $l0
      i32.const 32
      i32.add
      local.set $l1
      local.get $l2
      i32.eqz
      if $I2
        local.get $l1
        local.get $l5
        f64.store
        local.get $l5
        local.set $l4
      end
      local.get $l0
      f32.load offset=236
      local.tee $l7
      f32.const 0x0p+0 (;=0;)
      f32.ne
      if $I3
        local.get $l0
        i32.const 48
        i32.add
        local.tee $l2
        f64.load
        local.set $l5
        local.get $l2
        local.get $l0
        f64.load offset=96
        local.get $l4
        local.get $l6
        f64.sub
        local.get $l7
        f64.promote_f32
        f64.div
        f64.add
        local.tee $l4
        f64.store
        local.get $l0
        local.get $l4
        local.get $l5
        f64.sub
        f32.demote_f64
        f32.store offset=60
      end
      local.get $l0
      local.get $l1
      i64.load
      i64.store offset=128
      local.get $l0
      local.get $l1
      i32.load offset=40
      i32.store offset=168
      local.get $l0
      local.get $l1
      i64.load offset=32
      i64.store offset=160
      local.get $l0
      local.get $l1
      i64.load offset=24
      i64.store offset=152
      local.get $l0
      local.get $l1
      i64.load offset=16
      i64.store offset=144
      local.get $l0
      local.get $l1
      i64.load offset=8
      i64.store offset=136
      local.get $l0
      i32.const 1
      i32.store8 offset=233
      local.get $l0
      i32.const 0
      i32.store8 offset=178
      local.get $l3
    end)
