  (func $f73032 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32)
    global.get $g0
    i32.const -64
    i32.add
    local.tee $l2
    global.set $g0
    i32.const 9
    call $f80140
    call $f73714
    block $B0
      block $B1
        local.get $p1
        f32.load
        f32.const 0x0p+0 (;=0;)
        f32.ge
        i32.eqz
        br_if $B1
        local.get $p1
        f32.load offset=4
        f32.const 0x0p+0 (;=0;)
        f32.ge
        i32.eqz
        br_if $B1
        local.get $p1
        f32.load offset=8
        f32.const 0x0p+0 (;=0;)
        f32.ge
        i32.eqz
        br_if $B1
        local.get $p0
        i32.const 0
        i32.store8 offset=100
        local.get $p0
        local.get $p1
        i64.load align=4
        i64.store offset=104 align=4
        local.get $p0
        local.get $p1
        i32.load offset=8
        i32.store offset=112
        local.get $p0
        i32.load offset=52
        local.tee $l3
        i32.eqz
        br_if $B0
        local.get $l3
        local.get $p1
        local.get $l3
        i32.load
        i32.load offset=128
        call_indirect $__indirect_function_table (type $t1)
        local.get $p0
        call $f73060
        br $B0
      end
      local.get $p0
      i32.load offset=4
      local.set $p1
      local.get $l2
      i32.const 403047
      i32.store offset=60
      local.get $l2
      i32.const 403047
      i32.store offset=56
      local.get $l2
      i64.const 0
      i64.store offset=48
      local.get $l2
      i32.const 1
      i32.store8 offset=44
      local.get $l2
      i32.const 403047
      i32.store offset=12
      local.get $l2
      i32.const 403047
      i32.store offset=8
      local.get $l2
      i32.const 403047
      i32.store offset=4
      local.get $l2
      i64.const 0
      i64.store offset=36 align=4
      local.get $l2
      local.get $p1
      i32.store offset=32
      local.get $l2
      i32.const 1
      i32.store offset=28
      local.get $l2
      i64.const -4294966195
      i64.store offset=20 align=4
      local.get $l2
      i32.const 403047
      i32.store offset=16
      local.get $l2
      i32.const 247419
      i32.store
      local.get $l2
      call $f83275
    end
    local.get $l2
    i32.const -64
    i32.sub
    global.set $g0)