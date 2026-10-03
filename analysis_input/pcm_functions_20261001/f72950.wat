  (func $f72950 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 f32) (local $l13 f32)
    global.get $g0
    i32.const 208
    i32.sub
    local.tee $l3
    global.set $g0
    block $B0
      local.get $p0
      i32.load offset=84
      local.tee $l5
      i32.eqz
      br_if $B0
      local.get $l3
      local.get $l5
      i32.store offset=104
      block $B1
        block $B2
          i32.const 4782060
          i32.load
          local.tee $l5
          i32.eqz
          br_if $B2
          local.get $l3
          i32.const 144
          i32.add
          local.get $l5
          local.get $l3
          i32.const 104
          i32.add
          call $f66830
          local.get $l3
          i32.load offset=144
          local.tee $l4
          i32.const 4782060
          i32.load
          local.tee $l5
          i32.load
          local.get $l5
          i32.load offset=4
          i32.const 3
          i32.mul
          i32.add
          i32.const 12
          i32.add
          i32.eq
          br_if $B2
          local.get $l4
          i32.load offset=8
          local.tee $l5
          br_if $B1
        end
        local.get $p0
        i32.load offset=84
        call $f80110
        local.tee $l5
        br_if $B1
        i32.const 0
        local.set $l4
        br $B0
      end
      local.get $p0
      i32.load offset=28
      i32.const 4131408
      call $f80185
      local.tee $l4
      call $f78152
      local.set $l10
      local.get $l3
      i32.const 104
      i32.add
      local.get $l4
      call $f78119
      block $B3
        local.get $p0
        i32.load offset=40
        local.tee $l6
        i32.eqz
        br_if $B3
        local.get $p0
        i32.load8_u offset=81
        br_if $B3
        local.get $l6
        local.get $l6
        i32.load
        i32.load offset=32
        call_indirect $__indirect_function_table (type $t5)
        i32.const 4
        i32.eq
        if $I4
          local.get $l3
          i64.const 4575657221408423936
          i64.store offset=168
          local.get $l3
          i64.const 0
          i64.store offset=160
          local.get $l3
          i64.const 4575657222473777152
          i64.store offset=152
          local.get $l3
          i32.const 0
          i32.store8 offset=183
          local.get $l3
          i32.const 0
          i32.store16 offset=181 align=1
          local.get $l3
          i32.const 1
          i32.store8 offset=180
          local.get $l3
          i32.const 0
          i32.store offset=176
          local.get $l3
          i64.const 4575657221408423940
          i64.store offset=144
          local.get $p0
          i32.load offset=40
          local.tee $l8
          local.get $l3
          i32.const 144
          i32.add
          local.get $l8
          i32.load
          i32.load offset=60
          call_indirect $__indirect_function_table (type $t0)
          drop
          local.get $l3
          i32.load offset=176
          local.set $l8
          br $B3
        end
        local.get $l3
        i32.const 1065353216
        i32.store offset=172
        local.get $l3
        i64.const 0
        i64.store offset=164 align=4
        local.get $l3
        i64.const 1065353216
        i64.store offset=156 align=4
        local.get $l3
        i64.const 0
        i64.store offset=176
        local.get $l3
        i64.const 4575657222473777152
        i64.store offset=148 align=4
        local.get $l3
        i32.const 5
        i32.store offset=144
        local.get $p0
        i32.load offset=40
        local.tee $l8
        local.get $l3
        i32.const 144
        i32.add
        local.get $l8
        i32.load
        i32.load offset=64
        call_indirect $__indirect_function_table (type $t0)
        drop
        local.get $l3
        i32.load offset=180
        local.set $l8
      end
      block $B5
        block $B6
          local.get $p0
          i32.load offset=144
          local.get $l5
          i32.const 180
          i32.add
          local.tee $l6
          i32.load offset=12
          i32.xor
          i32.const 31
          i32.and
          br_if $B6
          global.get $g0
          i32.const 48
          i32.sub
          local.tee $l7
          global.set $g0
          local.get $p0
          i32.load offset=28
          i32.const 4131408
          call $f80185
          local.tee $l9
          call $f78152
          local.set $l11
          local.get $l7
          i32.const 8
          i32.add
          local.get $l9
          call $f78119
          block $B7
            local.get $p0
            i32.load8_u offset=80
            if $I8
              i32.const 1
              local.set $l9
              local.get $l7
              f32.load offset=8
              f32.const 0x0p+0 (;=0;)
              f32.lt
              br_if $B7
              local.get $l7
              f32.load offset=24
              f32.const 0x0p+0 (;=0;)
              f32.lt
              br_if $B7
              local.get $l7
              f32.load offset=40
              f32.const 0x0p+0 (;=0;)
              f32.lt
              br_if $B7
            end
            i32.const 0
            local.set $l9
            local.get $l11
            i32.const 2
            i32.and
            i32.eqz
            br_if $B7
            block $B9
              local.get $l7
              f32.load offset=20
              local.tee $l12
              f32.neg
              local.get $l12
              local.get $l12
              f32.const 0x0p+0 (;=0;)
              f32.lt
              select
              f32.const 0x1.47ae14p-7 (;=0.01;)
              f32.le
              i32.eqz
              br_if $B9
              local.get $l7
              f32.load offset=32
              local.tee $l12
              f32.neg
              local.get $l12
              local.get $l12
              f32.const 0x0p+0 (;=0;)
              f32.lt
              select
              f32.const 0x1.47ae14p-7 (;=0.01;)
              f32.le
              i32.eqz
              br_if $B9
              local.get $l7
              f32.load offset=12
              local.tee $l12
              f32.neg
              local.get $l12
              local.get $l12
              f32.const 0x0p+0 (;=0;)
              f32.lt
              select
              f32.const 0x1.47ae14p-7 (;=0.01;)
              f32.le
              i32.eqz
              br_if $B9
              local.get $l7
              f32.load offset=36
              local.tee $l12
              f32.neg
              local.get $l12
              local.get $l12
              f32.const 0x0p+0 (;=0;)
              f32.lt
              select
              f32.const 0x1.47ae14p-7 (;=0.01;)
              f32.le
              i32.eqz
              br_if $B9
              local.get $l7
              f32.load offset=16
              local.tee $l12
              f32.neg
              local.get $l12
              local.get $l12
              f32.const 0x0p+0 (;=0;)
              f32.lt
              select
              f32.const 0x1.47ae14p-7 (;=0.01;)
              f32.le
              i32.eqz
              br_if $B9
              local.get $l7
              f32.load offset=28
              local.tee $l12
              f32.neg
              local.get $l12
              local.get $l12
              f32.const 0x0p+0 (;=0;)
              f32.lt
              select
              f32.const 0x1.47ae14p-7 (;=0.01;)
              f32.le
              br_if $B7
            end
            i32.const 1
            local.set $l9
          end
          local.get $l7
          i32.const 48
          i32.add
          global.set $g0
          local.get $l9
          br_if $B6
          local.get $l5
          i32.load8_u offset=188
          br_if $B6
          local.get $l3
          f32.load offset=104
          local.set $l12
          local.get $l3
          f32.load offset=120
          local.set $l13
          local.get $p1
          local.get $l3
          f32.load offset=136
          f32.store offset=8
          local.get $p1
          local.get $l13
          f32.store offset=4
          local.get $p1
          local.get $l12
          f32.store
          local.get $p0
          i32.load offset=144
          local.set $p1
          local.get $p0
          i32.load8_u offset=80
          local.set $l4
          global.get $g0
          i32.const -64
          i32.add
          local.tee $l7
          global.set $g0
          block $B10 (result i32)
            local.get $l6
            i32.const 0
            i32.const 4
            local.get $l4
            select
            i32.add
            i32.load
            local.tee $p0
            if $I11
              local.get $l6
              i32.load offset=12
              br $B10
            end
            local.get $l7
            call $f78467
            local.get $l6
            local.get $l6
            i32.const 4
            i32.add
            local.get $l4
            select
            i32.const 4679096
            i32.load
            local.tee $p0
            local.get $l5
            local.get $l4
            local.get $p1
            local.get $l7
            i32.const 0
            local.get $p0
            i32.load
            i32.load offset=44
            call_indirect $__indirect_function_table (type $t10)
            local.tee $p0
            i32.store
            local.get $l6
            local.get $p1
            i32.store offset=12
            local.get $p1
          end
          local.set $l6
          local.get $l7
          i32.const -64
          i32.sub
          global.set $g0
          i32.const 0
          local.get $p0
          local.get $p1
          local.get $l6
          i32.xor
          i32.const 31
          i32.and
          select
          local.set $l4
          local.get $p2
          i32.const 1
          i32.store8
          br $B5
        end
        local.get $l5
        i32.load offset=32
        local.tee $l6
        i32.load offset=120
        i32.eqz
        if $I12
          local.get $l3
          i32.const 72
          i32.add
          local.get $l4
          i32.const 0
          call $f78179
          local.get $l3
          i32.load offset=72
          local.set $p1
          local.get $l3
          i32.load8_u offset=92
          local.set $p2
          local.get $l5
          local.get $l5
          i32.load
          i32.load offset=40
          call_indirect $__indirect_function_table (type $t5)
          local.set $l8
          local.get $l4
          call $f78136
          local.tee $l5
          i32.load8_u offset=60
          local.set $l4
          local.get $l5
          i32.load offset=40
          local.set $l6
          local.get $l3
          local.get $l8
          i32.store offset=4
          local.get $l3
          local.get $l3
          i32.const 72
          i32.add
          local.get $p1
          local.get $p2
          i32.const 1
          i32.eq
          select
          i32.store
          local.get $l3
          local.get $l5
          i32.const 40
          i32.add
          local.get $l6
          local.get $l4
          i32.const 1
          i32.eq
          select
          i32.store offset=8
          local.get $l3
          i32.const 40
          i32.add
          i32.const 249157
          local.get $l3
          call $f569
          local.get $p0
          i32.load offset=4
          local.set $p0
          local.get $l3
          i32.const 403047
          i32.store offset=204
          local.get $l3
          i32.const 403047
          i32.store offset=200
          local.get $l3
          i64.const 0
          i64.store offset=192
          local.get $l3
          i32.const 1
          i32.store8 offset=188
          local.get $l3
          i32.const 403047
          i32.store offset=156
          local.get $l3
          i32.const 403047
          i32.store offset=152
          local.get $l3
          i32.const 403047
          i32.store offset=148
          local.get $l3
          i64.const 0
          i64.store offset=180 align=4
          local.get $l3
          local.get $p0
          i32.store offset=176
          local.get $l3
          i32.const 1
          i32.store offset=172
          local.get $l3
          i64.const -4294966985
          i64.store offset=164 align=4
          local.get $l3
          i32.const 403047
          i32.store offset=160
          local.get $l3
          local.get $l3
          i32.const 40
          i32.add
          local.get $l3
          i32.load offset=40
          local.get $l3
          i32.load8_u offset=60
          i32.const 1
          i32.eq
          select
          i32.store offset=144
          local.get $l3
          i32.const 144
          i32.add
          call $f83275
          local.get $l3
          i32.load8_u offset=60
          i32.eqz
          if $I13
            local.get $l3
            i32.load offset=40
            local.get $l3
            i32.load offset=64
            i32.const 403047
            i32.const 518
            call $f83342
          end
          local.get $l3
          i32.load8_u offset=92
          i32.eqz
          if $I14
            local.get $l3
            i32.load offset=72
            local.get $l3
            i32.load offset=96
            i32.const 403047
            i32.const 518
            call $f83342
          end
          i32.const 0
          local.set $l4
          br $B0
        end
        local.get $l6
        i32.load offset=144
        i32.eqz
        if $I15
          local.get $l3
          i32.const 72
          i32.add
          local.get $l4
          i32.const 0
          call $f78179
          local.get $l3
          i32.load offset=72
          local.set $p1
          local.get $l3
          i32.load8_u offset=92
          local.set $p2
          local.get $l5
          local.get $l5
          i32.load
          i32.load offset=40
          call_indirect $__indirect_function_table (type $t5)
          local.set $l8
          local.get $l4
          call $f78136
          local.tee $l5
          i32.load8_u offset=60
          local.set $l4
          local.get $l5
          i32.load offset=40
          local.set $l6
          local.get $l3
          local.get $l8
          i32.store offset=20
          local.get $l3
          local.get $l3
          i32.const 72
          i32.add
          local.get $p1
          local.get $p2
          i32.const 1
          i32.eq
          select
          i32.store offset=16
          local.get $l3
          local.get $l5
          i32.const 40
          i32.add
          local.get $l6
          local.get $l4
          i32.const 1
          i32.eq
          select
          i32.store offset=24
          local.get $l3
          i32.const 40
          i32.add
          i32.const 275671
          local.get $l3
          i32.const 16
          i32.add
          call $f569
          local.get $p0
          i32.load offset=4
          local.set $p0
          local.get $l3
          i32.const 403047
          i32.store offset=204
          local.get $l3
          i32.const 403047
          i32.store offset=200
          local.get $l3
          i64.const 0
          i64.store offset=192
          local.get $l3
          i32.const 1
          i32.store8 offset=188
          local.get $l3
          i32.const 403047
          i32.store offset=156
          local.get $l3
          i32.const 403047
          i32.store offset=152
          local.get $l3
          i32.const 403047
          i32.store offset=148
          local.get $l3
          i64.const 0
          i64.store offset=180 align=4
          local.get $l3
          local.get $p0
          i32.store offset=176
          local.get $l3
          i32.const 1
          i32.store offset=172
          local.get $l3
          i64.const -4294966975
          i64.store offset=164 align=4
          local.get $l3
          i32.const 403047
          i32.store offset=160
          local.get $l3
          local.get $l3
          i32.const 40
          i32.add
          local.get $l3
          i32.load offset=40
          local.get $l3
          i32.load8_u offset=60
          i32.const 1
          i32.eq
          select
          i32.store offset=144
          local.get $l3
          i32.const 144
          i32.add
          call $f83275
          local.get $l3
          i32.load8_u offset=60
          i32.eqz
          if $I16
            local.get $l3
            i32.load offset=40
            local.get $l3
            i32.load offset=64
            i32.const 403047
            i32.const 518
            call $f83342
          end
          local.get $l3
          i32.load8_u offset=92
          i32.eqz
          if $I17
            local.get $l3
            i32.load offset=72
            local.get $l3
            i32.load offset=96
            i32.const 403047
            i32.const 518
            call $f83342
          end
          i32.const 0
          local.set $l4
          br $B0
        end
        i32.const 4679096
        i32.load
        local.tee $l4
        local.get $l5
        local.get $p0
        i32.load8_u offset=80
        local.get $p0
        i32.load offset=144
        local.get $l3
        i32.const 144
        i32.add
        local.get $l3
        i32.const 104
        i32.add
        call $f78462
        local.get $l10
        local.get $l4
        i32.load
        i32.load offset=44
        call_indirect $__indirect_function_table (type $t10)
        local.set $l4
        local.get $l5
        local.get $p0
        i32.load offset=144
        i32.store offset=192
        local.get $p2
        i32.const 0
        i32.store8
        local.get $p1
        i32.const 1065353216
        i32.store offset=8
        local.get $p1
        i64.const 4575657222473777152
        i64.store align=4
      end
      local.get $l8
      i32.eqz
      br_if $B0
      local.get $l4
      i32.eqz
      br_if $B0
      local.get $l8
      local.get $l8
      i32.load
      i32.load
      call_indirect $__indirect_function_table (type $t7)
    end
    local.get $l3
    i32.const 208
    i32.add
    global.set $g0
    local.get $l4)