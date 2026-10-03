  (func $f82291 (type $t193) (param $p0 f32)
    (local $l1 i32) (local $l2 i32)
    i32.const 7
    call $f80140
    local.set $l2
    global.get $g0
    i32.const 112
    i32.sub
    local.tee $l1
    global.set $g0
    block $B0
      local.get $p0
      local.get $p0
      f32.ne
      if $I1
        local.get $l1
        i32.const 16
        i32.add
        i32.const 212824
        i32.const 0
        call $f569
        local.get $l1
        i32.const 403047
        i32.store offset=108
        local.get $l1
        i32.const 403047
        i32.store offset=104
        local.get $l1
        i64.const 0
        i64.store offset=96
        local.get $l1
        i32.const 403047
        i32.store offset=60
        local.get $l1
        i32.const 403047
        i32.store offset=56
        local.get $l1
        i32.const 403047
        i32.store offset=52
        local.get $l1
        i64.const 0
        i64.store offset=84 align=4
        local.get $l1
        i64.const 1
        i64.store offset=76 align=4
        local.get $l1
        i64.const -4294966696
        i64.store offset=68 align=4
        local.get $l1
        i32.const 403047
        i32.store offset=64
        local.get $l1
        i32.const 1
        i32.store8 offset=92
        local.get $l1
        local.get $l1
        i32.const 16
        i32.add
        local.get $l1
        i32.load offset=16
        local.get $l1
        i32.load8_u offset=36
        i32.const 1
        i32.eq
        select
        i32.store offset=48
        local.get $l1
        i32.const 48
        i32.add
        call $f83275
        local.get $l1
        i32.load8_u offset=36
        br_if $B0
        local.get $l1
        i32.load offset=16
        local.get $l1
        i32.load offset=40
        i32.const 403047
        i32.const 518
        call $f83342
        br $B0
      end
      local.get $p0
      f32.const 0x0p+0 (;=0;)
      f32.lt
      if $I2
        local.get $l1
        i64.const 0
        i64.store
        local.get $l1
        i32.const 16
        i32.add
        i32.const 144252
        local.get $l1
        call $f569
        local.get $l1
        i32.const 403047
        i32.store offset=108
        local.get $l1
        i32.const 403047
        i32.store offset=104
        local.get $l1
        i64.const 0
        i64.store offset=96
        local.get $l1
        i32.const 403047
        i32.store offset=60
        local.get $l1
        i32.const 403047
        i32.store offset=56
        local.get $l1
        i32.const 403047
        i32.store offset=52
        local.get $l1
        i64.const 0
        i64.store offset=84 align=4
        local.get $l1
        i64.const 1
        i64.store offset=76 align=4
        local.get $l1
        i64.const -4294966690
        i64.store offset=68 align=4
        local.get $l1
        i32.const 403047
        i32.store offset=64
        local.get $l1
        i32.const 1
        i32.store8 offset=92
        local.get $l1
        local.get $l1
        i32.const 16
        i32.add
        local.get $l1
        i32.load offset=16
        local.get $l1
        i32.load8_u offset=36
        i32.const 1
        i32.eq
        select
        i32.store offset=48
        local.get $l1
        i32.const 48
        i32.add
        call $f83275
        local.get $l1
        i32.load8_u offset=36
        br_if $B0
        local.get $l1
        i32.load offset=16
        local.get $l1
        i32.load offset=40
        i32.const 403047
        i32.const 518
        call $f83342
        br $B0
      end
      local.get $l2
      local.get $p0
      f32.store offset=236
      i32.const 4758660
      i32.load8_u
      i32.eqz
      br_if $B0
      local.get $l2
      call $f78679
    end
    local.get $l1
    i32.const 112
    i32.add
    global.set $g0)
