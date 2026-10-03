  (func $f69971 (type $t65) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 f32)
    (local $l4 i32)
    block $B0
      local.get $p2
      i32.const 4
      i32.le_u
      if $I1
        local.get $p2
        i32.eqz
        br_if $B0
        local.get $p0
        i32.load offset=76
        local.tee $l4
        local.get $p1
        i64.load
        i64.store
        local.get $l4
        local.get $p1
        i64.load offset=8
        i64.store offset=8
        local.get $p0
        i32.load offset=76
        local.tee $l4
        local.get $p1
        i64.load offset=16
        i64.store offset=16
        local.get $l4
        local.get $p1
        i64.load offset=24
        i64.store offset=24
        local.get $p0
        i32.load offset=76
        local.tee $l4
        local.get $p1
        i64.load offset=32
        i64.store offset=32
        local.get $l4
        local.get $p1
        i64.load offset=40
        i64.store offset=40
        local.get $p2
        i32.const 1
        i32.eq
        br_if $B0
        local.get $p0
        i32.load offset=76
        local.tee $l4
        local.get $p1
        i64.load offset=48
        i64.store offset=48
        local.get $l4
        local.get $p1
        i64.load offset=56
        i64.store offset=56
        local.get $p0
        i32.load offset=76
        local.tee $l4
        i32.const -64
        i32.sub
        local.get $p1
        i32.const -64
        i32.sub
        i64.load
        i64.store
        local.get $l4
        local.get $p1
        i64.load offset=72
        i64.store offset=72
        local.get $p0
        i32.load offset=76
        local.tee $l4
        local.get $p1
        i64.load offset=80
        i64.store offset=80
        local.get $l4
        local.get $p1
        i64.load offset=88
        i64.store offset=88
        local.get $p2
        i32.const 2
        i32.eq
        br_if $B0
        local.get $p0
        i32.load offset=76
        local.tee $l4
        local.get $p1
        i64.load offset=96
        i64.store offset=96
        local.get $l4
        local.get $p1
        i64.load offset=104
        i64.store offset=104
        local.get $p0
        i32.load offset=76
        local.tee $l4
        local.get $p1
        i64.load offset=112
        i64.store offset=112
        local.get $l4
        local.get $p1
        i64.load offset=120
        i64.store offset=120
        local.get $p0
        i32.load offset=76
        local.tee $l4
        local.get $p1
        i64.load offset=128
        i64.store offset=128
        local.get $l4
        local.get $p1
        i64.load offset=136
        i64.store offset=136
        local.get $p2
        i32.const 3
        i32.eq
        br_if $B0
        local.get $p0
        i32.load offset=76
        local.tee $l4
        local.get $p1
        i64.load offset=144
        i64.store offset=144
        local.get $l4
        local.get $p1
        i64.load offset=152
        i64.store offset=152
        local.get $p0
        i32.load offset=76
        local.tee $l4
        local.get $p1
        i64.load offset=160
        i64.store offset=160
        local.get $l4
        local.get $p1
        i64.load offset=168
        i64.store offset=168
        local.get $p0
        i32.load offset=76
        local.tee $l4
        local.get $p1
        i64.load offset=176
        i64.store offset=176
        local.get $l4
        local.get $p1
        i64.load offset=184
        i64.store offset=184
        local.get $p0
        local.get $p2
        i32.store8 offset=64
        return
      end
      local.get $p0
      local.get $p1
      local.get $p2
      local.get $p3
      call $f69969
      i32.const 4
      local.set $p2
    end
    local.get $p0
    local.get $p2
    i32.store8 offset=64)