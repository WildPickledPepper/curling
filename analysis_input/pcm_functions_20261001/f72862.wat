  (func $f72862 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32)
    local.get $p0
    i32.const 0
    i32.store offset=112
    local.get $p0
    i32.const 104
    i32.add
    local.tee $l2
    local.get $p0
    i32.load offset=12
    local.tee $l3
    i32.load offset=12
    i32.store
    local.get $p0
    local.get $l3
    i32.load offset=68
    i32.store offset=116
    block $B0 (result i32)
      local.get $l3
      i32.load8_u offset=8
      i32.const 2
      i32.and
      if $I1
        local.get $l3
        i32.load offset=72
        br $B0
      end
      local.get $l3
      i32.load offset=72
      local.set $l1
      i32.const 0
    end
    local.set $l4
    local.get $l3
    i32.load offset=16
    local.set $l3
    local.get $p0
    local.get $l4
    i32.store offset=124
    local.get $p0
    local.get $l1
    i32.store offset=120
    local.get $p0
    local.get $l3
    i32.store offset=108
    local.get $p0
    i32.const 128
    i32.add
    local.set $l5
    local.get $p0
    i32.load offset=8
    local.tee $l1
    i32.load offset=40
    i32.const 1
    i32.eq
    if $I2 (result i32)
      local.get $l1
      i32.load offset=32
    else
      i32.const 4
    end
    local.set $l3
    i32.const 0
    local.set $l4
    global.get $g0
    i32.const 176
    i32.sub
    local.tee $l1
    global.set $g0
    local.get $l2
    i32.load offset=12
    local.set $l6
    local.get $l1
    i32.const 0
    i32.store offset=96
    local.get $l1
    i64.const 0
    i64.store offset=88
    block $B3
      local.get $l1
      i32.const 88
      i32.add
      local.get $l2
      local.get $l3
      call $f70246
      i32.eqz
      br_if $B3
      local.get $l6
      i32.const 2
      i32.shl
      local.tee $l7
      if $I4
        call $f69753
        local.tee $l4
        local.get $l7
        i32.const 3126265
        i32.const 3126218
        i32.const 1483
        local.get $l4
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.set $l4
      end
      local.get $l1
      i64.const 0
      i64.store offset=24
      local.get $l1
      i64.const 0
      i64.store offset=32
      local.get $l1
      i64.const 0
      i64.store offset=40
      local.get $l1
      i64.const 0
      i64.store offset=48
      local.get $l1
      i64.const 0
      i64.store offset=56
      local.get $l1
      i32.const -64
      i32.sub
      i64.const 0
      i64.store
      local.get $l1
      i64.const 0
      i64.store offset=72
      local.get $l1
      i64.const 0
      i64.store offset=16
      local.get $l1
      local.get $l6
      i32.store offset=12
      local.get $l1
      i32.const 0
      i32.store offset=8
      local.get $l1
      local.get $l3
      i32.store offset=4
      local.get $l1
      local.get $l4
      i32.store
      local.get $l1
      local.get $l2
      i32.store offset=80
      local.get $l1
      i32.const 0
      i32.store offset=152
      local.get $l1
      i32.const 0
      i32.store offset=136
      local.get $l1
      i32.load offset=92
      local.get $l1
      i32.const 152
      i32.add
      local.get $l1
      i32.const 136
      i32.add
      i32.const 119827
      local.get $l1
      call $f70248
      local.get $l2
      local.get $l4
      call $f70242
      local.get $l4
      if $I5
        call $f69753
        local.tee $l7
        local.get $l4
        local.get $l7
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $l3
      local.get $l2
      i32.load offset=12
      local.tee $l4
      i32.ge_u
      if $I6
        local.get $l5
        local.get $l2
        local.get $l1
        i32.load offset=92
        call $f70243
        local.set $l7
        br $B3
      end
      local.get $l1
      i32.load offset=92
      local.set $l3
      local.get $l4
      i32.const 4
      i32.le_u
      if $I7
        local.get $l5
        local.get $l2
        local.get $l3
        call $f70243
        local.set $l7
        br $B3
      end
      local.get $l3
      call $f70251
      local.get $l1
      i32.const 12
      i32.add
      local.tee $l4
      i64.const 0
      i64.store align=4
      i32.const 0
      local.set $l6
      local.get $l1
      i32.const 0
      i32.store offset=24
      local.get $l1
      f32.const 0x1.a36e2ep-13 (;=0.0002;)
      f32.store offset=20
      local.get $l1
      i64.const 0
      i64.store offset=4 align=4
      local.get $l1
      i32.const 1
      i32.store
      local.get $l1
      i32.const 88
      i32.add
      local.get $l1
      call $f70249
      local.tee $l3
      local.get $l1
      i32.load offset=92
      local.get $l1
      call $f70252
      local.get $l5
      local.get $l2
      local.get $l1
      i32.load offset=92
      call $f70243
      local.tee $l7
      if $I8
        local.get $l5
        i32.const 1
        i32.store8 offset=57
        local.get $l3
        i32.load offset=68
        i32.const -1
        i32.ne
        local.get $l3
        i32.load offset=32
        i32.const -1
        i32.ne
        i32.add
        local.get $l3
        i32.load offset=104
        i32.const -1
        i32.ne
        i32.add
        local.get $l3
        i32.load offset=140
        i32.const -1
        i32.ne
        i32.add
        local.set $l2
        local.get $l1
        i32.load offset=16
        local.get $l4
        i32.load
        local.get $l1
        i32.load offset=8
        local.get $l1
        i32.load offset=4
        i32.add
        i32.add
        i32.add
        local.tee $l8
        i32.const 6
        i32.shl
        local.tee $l11
        if $I9
          call $f69753
          local.tee $l4
          local.get $l11
          i32.const 3126265
          i32.const 3126218
          i32.const 1090
          local.get $l4
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
          local.set $l6
        end
        local.get $l1
        i32.const 4
        i32.store offset=172
        local.get $l5
        local.get $l2
        i32.const 2
        i32.sub
        local.tee $l2
        i32.const 1
        i32.shl
        i32.const -1
        local.get $l2
        i32.const 3
        i32.lt_u
        select
        i32.store offset=28
        local.get $l1
        i32.const 0
        i32.store offset=168
        local.get $l1
        i32.const 0
        i32.store offset=164
        local.get $l5
        i32.load8_u offset=57
        if $I10
          local.get $l1
          i32.const -8388609
          i32.store offset=128
          local.get $l1
          i64.const -36028797027352577
          i64.store offset=120
          local.get $l1
          i32.const -8388609
          i32.store offset=112
          local.get $l1
          i64.const -36028797027352577
          i64.store offset=104
          local.get $l3
          local.get $l1
          i32.const 120
          i32.add
          local.get $l1
          i32.const 104
          i32.add
          call $f70253
          local.get $l1
          f32.load offset=120
          local.set $l12
          local.get $l1
          f32.load offset=124
          local.set $l13
          local.get $l1
          f32.load offset=128
          local.set $l14
          local.get $l1
          f32.load offset=104
          local.set $l15
          local.get $l1
          f32.load offset=108
          local.set $l16
          local.get $l5
          local.get $l1
          f32.load offset=112
          local.tee $l17
          f32.const 0x1.fffcp+14 (;=32767;)
          f32.div
          f32.store offset=52
          local.get $l5
          local.get $l16
          f32.const 0x1.fffcp+14 (;=32767;)
          f32.div
          f32.store offset=48
          local.get $l5
          local.get $l15
          f32.const 0x1.fffcp+14 (;=32767;)
          f32.div
          f32.store offset=44
          local.get $l5
          local.get $l14
          f32.const 0x1.fffcp+14 (;=32767;)
          f32.div
          f32.store offset=40
          local.get $l5
          local.get $l13
          f32.const 0x1.fffcp+14 (;=32767;)
          f32.div
          f32.store offset=36
          local.get $l5
          local.get $l12
          f32.const 0x1.fffcp+14 (;=32767;)
          f32.div
          f32.store offset=32
          local.get $l1
          f32.const 0x1.fffcp+14 (;=32767;)
          local.get $l14
          f32.div
          f32.const 0x0p+0 (;=0;)
          local.get $l14
          f32.const 0x0p+0 (;=0;)
          f32.ne
          select
          f32.store offset=160
          local.get $l1
          f32.const 0x1.fffcp+14 (;=32767;)
          local.get $l13
          f32.div
          f32.const 0x0p+0 (;=0;)
          local.get $l13
          f32.const 0x0p+0 (;=0;)
          f32.ne
          select
          f32.store offset=156
          local.get $l1
          f32.const 0x1.fffcp+14 (;=32767;)
          local.get $l12
          f32.div
          f32.const 0x0p+0 (;=0;)
          local.get $l12
          f32.const 0x0p+0 (;=0;)
          f32.ne
          select
          f32.store offset=152
          local.get $l1
          f32.const 0x1.fffcp+14 (;=32767;)
          local.get $l17
          f32.div
          f32.const 0x0p+0 (;=0;)
          local.get $l17
          f32.const 0x0p+0 (;=0;)
          f32.ne
          select
          f32.store offset=144
          local.get $l1
          f32.const 0x1.fffcp+14 (;=32767;)
          local.get $l16
          f32.div
          f32.const 0x0p+0 (;=0;)
          local.get $l16
          f32.const 0x0p+0 (;=0;)
          f32.ne
          select
          f32.store offset=140
          local.get $l1
          f32.const 0x1.fffcp+14 (;=32767;)
          local.get $l15
          f32.div
          f32.const 0x0p+0 (;=0;)
          local.get $l15
          f32.const 0x0p+0 (;=0;)
          f32.ne
          select
          f32.store offset=136
          local.get $l6
          i32.const 0
          local.get $l1
          i32.const 172
          i32.add
          local.get $l3
          local.get $l1
          i32.const 168
          i32.add
          local.get $l1
          i32.const 164
          i32.add
          local.get $l1
          i32.const 152
          i32.add
          local.get $l1
          i32.const 136
          i32.add
          local.get $l5
          i32.const 32
          i32.add
          local.get $l5
          i32.const 44
          i32.add
          call $f70254
        end
        local.get $l1
        i32.load offset=24
        local.tee $l2
        if $I11
          loop $L12
            local.get $l2
            i32.load offset=37896
            local.set $l3
            call $f69753
            local.tee $l4
            local.get $l2
            local.get $l4
            i32.load
            i32.load offset=12
            call_indirect $__indirect_function_table (type $t1)
            local.get $l3
            local.tee $l2
            br_if $L12
          end
        end
        local.get $l8
        i32.const 2
        i32.shl
        local.set $l9
        local.get $l1
        i32.const 0
        i32.store offset=24
        block $B13
          local.get $l5
          i32.load8_u offset=57
          i32.eqz
          br_if $B13
          block $B14
            block $B15
              i32.const -1
              local.get $l9
              i32.const 4
              i32.shl
              local.get $l9
              i32.const 268435455
              i32.and
              local.get $l9
              i32.ne
              select
              local.tee $l2
              if $I16
                call $f69753
                local.tee $l3
                local.get $l2
                i32.const 3126309
                i32.const 3126281
                i32.const 4700888
                i32.load
                local.tee $l4
                local.get $l4
                i32.load
                i32.load offset=20
                call_indirect $__indirect_function_table (type $t5)
                select
                i32.const 3126218
                i32.const 1218
                local.get $l3
                i32.load
                i32.load offset=8
                call_indirect $__indirect_function_table (type $t9)
                local.tee $l10
                local.get $l6
                local.get $l11
                call $f483
                local.set $l2
                local.get $l8
                i32.const 1073741823
                i32.and
                local.tee $l8
                br_if $B15
                local.get $l2
                br_if $B14
                br $B13
              end
              i32.const 0
              local.get $l6
              local.get $l11
              call $f483
              drop
              local.get $l8
              i32.const 1073741823
              i32.and
              local.tee $l8
              i32.eqz
              br_if $B13
            end
            i32.const 0
            local.set $l4
            loop $L17
              local.get $l6
              local.get $l4
              i32.const 6
              i32.shl
              local.tee $l3
              i32.add
              local.tee $l2
              local.get $l3
              local.get $l10
              i32.add
              local.tee $l3
              i32.load16_u offset=2
              i32.store16
              local.get $l2
              local.get $l3
              i32.load16_u offset=6
              i32.store16 offset=16
              local.get $l2
              local.get $l3
              i32.load16_u offset=10
              i32.store16 offset=32
              local.get $l2
              local.get $l3
              i32.load16_u
              i32.store16 offset=2
              local.get $l2
              local.get $l3
              i32.load16_u offset=4
              i32.store16 offset=18
              local.get $l2
              local.get $l3
              i32.load16_u offset=8
              i32.store16 offset=34
              local.get $l2
              local.get $l3
              i32.load offset=12
              i32.store offset=48
              local.get $l2
              local.get $l3
              i32.load16_u offset=18
              i32.store16 offset=4
              local.get $l2
              local.get $l3
              i32.load16_u offset=22
              i32.store16 offset=20
              local.get $l2
              local.get $l3
              i32.load16_u offset=26
              i32.store16 offset=36
              local.get $l2
              local.get $l3
              i32.load16_u offset=16
              i32.store16 offset=6
              local.get $l2
              local.get $l3
              i32.load16_u offset=20
              i32.store16 offset=22
              local.get $l2
              local.get $l3
              i32.load16_u offset=24
              i32.store16 offset=38
              local.get $l2
              local.get $l3
              i32.load offset=28
              i32.store offset=52
              local.get $l2
              local.get $l3
              i32.load16_u offset=34
              i32.store16 offset=8
              local.get $l2
              local.get $l3
              i32.load16_u offset=38
              i32.store16 offset=24
              local.get $l2
              local.get $l3
              i32.load16_u offset=42
              i32.store16 offset=40
              local.get $l2
              local.get $l3
              i32.load16_u offset=32
              i32.store16 offset=10
              local.get $l2
              local.get $l3
              i32.load16_u offset=36
              i32.store16 offset=26
              local.get $l2
              local.get $l3
              i32.load16_u offset=40
              i32.store16 offset=42
              local.get $l2
              local.get $l3
              i32.load offset=44
              i32.store offset=56
              local.get $l2
              local.get $l3
              i32.load16_u offset=50
              i32.store16 offset=12
              local.get $l2
              local.get $l3
              i32.load16_u offset=54
              i32.store16 offset=28
              local.get $l2
              local.get $l3
              i32.load16_u offset=58
              i32.store16 offset=44
              local.get $l2
              local.get $l3
              i32.load16_u offset=48
              i32.store16 offset=14
              local.get $l2
              local.get $l3
              i32.load16_u offset=52
              i32.store16 offset=30
              local.get $l2
              local.get $l3
              i32.load16_u offset=56
              i32.store16 offset=46
              local.get $l2
              local.get $l3
              i32.load offset=60
              i32.store offset=60
              local.get $l4
              i32.const 1
              i32.add
              local.tee $l4
              local.get $l8
              i32.ne
              br_if $L17
            end
          end
          call $f69753
          local.tee $l2
          local.get $l10
          local.get $l2
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l5
        local.get $l6
        i32.store offset=24
        local.get $l5
        local.get $l9
        i32.store offset=20
      end
      local.get $l1
      i32.load offset=24
      local.tee $l2
      i32.eqz
      br_if $B3
      loop $L18
        local.get $l2
        i32.load offset=37896
        local.set $l3
        call $f69753
        local.tee $l4
        local.get $l2
        local.get $l4
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
        local.get $l3
        local.tee $l2
        br_if $L18
      end
    end
    local.get $l1
    i32.load offset=92
    local.tee $l4
    if $I19
      block $B20
        local.get $l4
        i32.const 4
        i32.sub
        local.tee $l5
        i32.load
        local.tee $l2
        i32.eqz
        br_if $B20
        local.get $l4
        local.get $l2
        i32.const 36
        i32.mul
        local.tee $l3
        i32.add
        local.set $l2
        local.get $l3
        i32.const 36
        i32.sub
        local.tee $l6
        i32.const 36
        i32.div_u
        i32.const 1
        i32.add
        i32.const 3
        i32.and
        local.tee $l3
        if $I21
          loop $L22
            local.get $l2
            i32.const 4
            i32.sub
            i32.const 0
            i32.store
            local.get $l2
            i32.const 12
            i32.sub
            i64.const 0
            i64.store align=4
            local.get $l2
            i32.const 36
            i32.sub
            local.set $l2
            local.get $l3
            i32.const 1
            i32.sub
            local.tee $l3
            br_if $L22
          end
        end
        local.get $l6
        i32.const 108
        i32.lt_u
        br_if $B20
        loop $L23
          local.get $l2
          i32.const 4
          i32.sub
          i32.const 0
          i32.store
          local.get $l2
          i32.const 12
          i32.sub
          i64.const 0
          i64.store align=4
          local.get $l2
          i32.const 40
          i32.sub
          i32.const 0
          i32.store
          local.get $l2
          i32.const 48
          i32.sub
          i64.const 0
          i64.store align=4
          local.get $l2
          i32.const 76
          i32.sub
          i32.const 0
          i32.store
          local.get $l2
          i32.const 84
          i32.sub
          i64.const 0
          i64.store align=4
          local.get $l2
          i32.const 112
          i32.sub
          i32.const 0
          i32.store
          local.get $l2
          i32.const 120
          i32.sub
          i64.const 0
          i64.store align=4
          local.get $l2
          i32.const 144
          i32.sub
          local.tee $l2
          local.get $l4
          i32.ne
          br_if $L23
        end
      end
      call $f69753
      local.tee $l2
      local.get $l5
      local.get $l2
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
      local.get $l1
      i32.const 0
      i32.store offset=92
    end
    local.get $l1
    i32.load offset=88
    local.tee $l2
    if $I24
      call $f69753
      local.tee $l3
      local.get $l2
      local.get $l3
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $l1
    i32.const 176
    i32.add
    global.set $g0
    local.get $l7
    i32.eqz
    if $I25
      i32.const 4700888
      i32.load
      i32.const 32
      i32.const 3212696
      i32.const 1150
      i32.const 3213124
      i32.const 0
      call $f69760
      return
    end
    local.get $p0
    i32.load offset=112
    local.set $l6
    local.get $p0
    i32.load offset=12
    local.tee $l1
    i32.load offset=80
    if $I26
      i32.const 0
      local.set $l3
      i32.const 0
      local.set $l2
      i32.const -1
      local.get $l1
      i32.load offset=68
      local.tee $l4
      local.get $l4
      i32.add
      local.tee $l5
      local.get $l4
      local.get $l5
      i32.gt_u
      select
      local.tee $l5
      if $I27 (result i32)
        call $f69753
        local.tee $l1
        local.get $l5
        i32.const 3213686
        i32.const 3213424
        i32.const 4700888
        i32.load
        local.tee $l2
        local.get $l2
        i32.load
        i32.load offset=20
        call_indirect $__indirect_function_table (type $t5)
        select
        i32.const 3212696
        i32.const 1159
        local.get $l1
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.set $l2
        local.get $p0
        i32.load offset=12
        local.tee $l1
        i32.load offset=68
      else
        local.get $l4
      end
      if $I28
        loop $L29
          local.get $l2
          local.get $l3
          i32.const 1
          i32.shl
          i32.add
          local.get $l1
          i32.load offset=80
          local.get $l6
          local.get $l3
          i32.const 2
          i32.shl
          i32.add
          i32.load
          i32.const 1
          i32.shl
          i32.add
          i32.load16_u
          i32.store16
          local.get $l3
          i32.const 1
          i32.add
          local.tee $l3
          local.get $p0
          i32.load offset=12
          local.tee $l1
          i32.load offset=68
          i32.lt_u
          br_if $L29
        end
      end
      local.get $l1
      i32.load offset=80
      local.tee $l3
      if $I30 (result i32)
        call $f69753
        local.tee $l1
        local.get $l3
        local.get $l1
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
        local.get $p0
        i32.load offset=12
      else
        local.get $l1
      end
      i32.const 0
      i32.store offset=80
      local.get $p0
      i32.load offset=12
      local.get $l2
      i32.store offset=80
    end
    block $B31
      local.get $p0
      i32.load offset=8
      local.tee $l3
      i32.load8_u offset=12
      if $I32
        local.get $l3
        i32.load8_u offset=14
        i32.eqz
        br_if $B31
      end
      i32.const 0
      local.set $l1
      i32.const 0
      local.set $l5
      i32.const -1
      local.get $p0
      i32.load offset=12
      local.tee $l2
      i32.load offset=68
      local.tee $l3
      i32.const 2
      i32.shl
      local.get $l3
      i32.const 1073741823
      i32.and
      local.get $l3
      i32.ne
      select
      local.tee $l4
      if $I33 (result i32)
        call $f69753
        local.tee $l3
        local.get $l4
        i32.const 3213588
        i32.const 3213424
        i32.const 4700888
        i32.load
        local.tee $l2
        local.get $l2
        i32.load
        i32.load offset=20
        call_indirect $__indirect_function_table (type $t5)
        select
        i32.const 3212696
        i32.const 1168
        local.get $l3
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.set $l5
        local.get $p0
        i32.load offset=12
        local.tee $l2
        i32.load offset=68
      else
        local.get $l3
      end
      if $I34
        loop $L35
          local.get $l6
          local.get $l1
          i32.const 2
          i32.shl
          local.tee $l4
          i32.add
          local.set $l3
          local.get $l4
          local.get $l5
          i32.add
          local.get $l2
          i32.load offset=48
          local.tee $l2
          if $I36 (result i32)
            local.get $l2
            local.get $l3
            i32.load
            i32.const 2
            i32.shl
            i32.add
          else
            local.get $l3
          end
          i32.load
          i32.store
          local.get $l1
          i32.const 1
          i32.add
          local.tee $l1
          local.get $p0
          i32.load offset=12
          local.tee $l2
          i32.load offset=68
          i32.lt_u
          br_if $L35
        end
      end
      local.get $l2
      i32.load offset=48
      local.tee $l3
      if $I37 (result i32)
        call $f69753
        local.tee $l1
        local.get $l3
        local.get $l1
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
        local.get $p0
        i32.load offset=12
      else
        local.get $l2
      end
      i32.const 0
      i32.store offset=48
      local.get $p0
      i32.load offset=12
      local.get $l5
      i32.store offset=48
    end
    local.get $p0
    i32.load offset=112
    local.tee $l3
    if $I38
      call $f69753
      local.tee $l1
      local.get $l3
      local.get $l1
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $p0
    i32.const 0
    i32.store offset=112)
