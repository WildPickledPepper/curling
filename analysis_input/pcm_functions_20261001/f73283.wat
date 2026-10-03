  (func $f73283 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32)
    global.get $g0
    i32.const 112
    i32.sub
    local.tee $l3
    global.set $g0
    i32.const 9
    call $f80140
    drop
    local.get $p0
    local.get $p0
    i32.load offset=28
    call $f73704
    i32.store offset=32
    local.get $p0
    local.get $p2
    call $f73284
    local.set $l4
    block $B0
      local.get $p0
      local.get $p2
      call $f73285
      local.tee $p2
      if $I1
        local.get $p2
        i32.load offset=40
        local.tee $l4
        i32.eqz
        br_if $B0
        local.get $p0
        local.get $p1
        local.get $l4
        local.get $p2
        i32.load offset=292
        i32.const 0
        call $f73282
        local.get $p0
        i32.load offset=40
        i32.eqz
        br_if $B0
        local.get $p0
        local.get $p2
        i32.load offset=28
        i32.const 4131408
        call $f80185
        local.get $l3
        i32.const 48
        i32.add
        call $f73278
        if $I2
          local.get $p0
          i32.load offset=40
          local.set $p0
          local.get $l3
          i32.const 48
          i32.add
          local.get $l3
          i32.const 32
          i32.add
          call $f65718
          local.get $l3
          local.get $l3
          f32.load offset=104
          f32.store offset=24
          local.get $l3
          local.get $l3
          i64.load offset=96
          i64.store offset=16
          local.get $l3
          local.get $l3
          i64.load offset=40
          i64.store offset=8
          local.get $l3
          local.get $l3
          i64.load offset=32
          i64.store
          local.get $p0
          local.get $l3
          local.get $p0
          i32.load
          i32.load offset=76
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $p2
        call $f73700
        br $B0
      end
      local.get $l4
      if $I3
        local.get $l4
        i32.const 1
        call $f73018
        local.get $l4
        i32.load offset=52
        local.tee $p2
        if $I4
          local.get $p0
          local.get $p1
          local.get $p2
          local.get $l4
          i32.load offset=140
          local.get $l4
          i32.load8_u offset=148
          i32.const 1
          i32.xor
          call $f73282
          local.get $p0
          i32.load offset=40
          i32.eqz
          br_if $B0
          local.get $p0
          local.get $l4
          i32.load offset=28
          i32.const 4131408
          call $f80185
          local.get $l3
          i32.const 48
          i32.add
          call $f73278
          if $I5
            local.get $p0
            i32.load offset=40
            local.set $p0
            local.get $l3
            i32.const 48
            i32.add
            local.get $l3
            i32.const 32
            i32.add
            call $f65718
            local.get $l3
            local.get $l3
            f32.load offset=104
            f32.store offset=24
            local.get $l3
            local.get $l3
            i64.load offset=96
            i64.store offset=16
            local.get $l3
            local.get $l3
            i64.load offset=40
            i64.store offset=8
            local.get $l3
            local.get $l3
            i64.load offset=32
            i64.store
            local.get $p0
            local.get $l3
            local.get $p0
            i32.load
            i32.load offset=76
            call_indirect $__indirect_function_table (type $t1)
          end
          local.get $l4
          call $f73060
          local.get $l4
          i32.load offset=64
          i32.const -1
          i32.ne
          if $I6
            i32.const 4682120
            i32.load
            local.tee $p0
            local.get $l4
            i32.load offset=68
            i32.load offset=4
            local.get $l4
            i32.load offset=64
            local.get $p0
            i32.load
            i32.load offset=12
            call_indirect $__indirect_function_table (type $t2)
          end
          br $B0
        end
        local.get $p0
        i32.load offset=4
        local.set $p0
        local.get $l3
        i32.const 403047
        i32.store offset=108
        local.get $l3
        i32.const 403047
        i32.store offset=104
        local.get $l3
        i64.const 0
        i64.store offset=96
        local.get $l3
        i32.const 1
        i32.store8 offset=92
        local.get $l3
        i32.const 403047
        i32.store offset=60
        local.get $l3
        i32.const 403047
        i32.store offset=56
        local.get $l3
        i32.const 403047
        i32.store offset=52
        local.get $l3
        i64.const 0
        i64.store offset=84 align=4
        local.get $l3
        local.get $p0
        i32.store offset=80
        local.get $l3
        i32.const 1
        i32.store offset=76
        local.get $l3
        i64.const -4294966731
        i64.store offset=68 align=4
        local.get $l3
        i32.const 403047
        i32.store offset=64
        local.get $l3
        i32.const 218964
        i32.store offset=48
        local.get $l3
        i32.const 48
        i32.add
        call $f83275
        br $B0
      end
      call $f73708
      local.set $p2
      local.get $l3
      i32.const 0
      i32.store offset=72
      local.get $l3
      i64.const 0
      i64.store offset=64
      local.get $l3
      i64.const 4575657221408423936
      i64.store offset=56
      local.get $l3
      i64.const 0
      i64.store offset=48
      local.get $p2
      local.get $l3
      i32.const 48
      i32.add
      local.get $p2
      i32.load
      i32.load offset=84
      call_indirect $__indirect_function_table (type $t0)
      local.tee $p2
      if $I7
        local.get $p2
        i32.const 0
        i32.store offset=8
        local.get $p0
        local.get $p1
        local.get $p2
        i32.const 0
        i32.const 0
        call $f73282
        local.get $p0
        i32.load offset=40
        i32.eqz
        br_if $B0
        local.get $p0
        local.get $p0
        i32.load
        i32.load offset=184
        call_indirect $__indirect_function_table (type $t7)
        local.get $p0
        i32.load offset=32
        i32.load offset=8
        local.tee $l4
        local.get $p2
        i32.const 0
        local.get $l4
        i32.load
        i32.load offset=44
        call_indirect $__indirect_function_table (type $t2)
        local.get $p0
        local.get $p0
        i32.load offset=28
        i32.load offset=56
        local.get $p0
        i32.load
        i32.load offset=88
        call_indirect $__indirect_function_table (type $t1)
        br $B0
      end
      local.get $p0
      i32.load offset=4
      local.set $p0
      local.get $l3
      i32.const 403047
      i32.store offset=108
      local.get $l3
      i32.const 403047
      i32.store offset=104
      local.get $l3
      i64.const 0
      i64.store offset=96
      local.get $l3
      i32.const 1
      i32.store8 offset=92
      local.get $l3
      i32.const 403047
      i32.store offset=60
      local.get $l3
      i32.const 403047
      i32.store offset=56
      local.get $l3
      i32.const 403047
      i32.store offset=52
      local.get $l3
      i64.const 0
      i64.store offset=84 align=4
      local.get $l3
      local.get $p0
      i32.store offset=80
      local.get $l3
      i32.const 1
      i32.store offset=76
      local.get $l3
      i64.const -4294966706
      i64.store offset=68 align=4
      local.get $l3
      i32.const 403047
      i32.store offset=64
      local.get $l3
      i32.const 218964
      i32.store offset=48
      local.get $l3
      i32.const 48
      i32.add
      call $f83275
    end
    local.get $l3
    i32.const 112
    i32.add
    global.set $g0)
