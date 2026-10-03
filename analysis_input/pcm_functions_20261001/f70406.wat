  (func $f70406 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l8
    global.set $g0
    block $B0
      block $B1
        block $B2
          block $B3
            local.get $p1
            i32.load offset=4
            br_table $B3 $B2 $B0
          end
          call $f69753
          local.tee $l2
          i32.const 208
          i32.const 3130972
          i32.const 3129657
          i32.const 4700888
          i32.load
          local.tee $l6
          local.get $l6
          i32.load
          i32.load offset=20
          call_indirect $__indirect_function_table (type $t5)
          select
          i32.const 3129364
          i32.const 115
          local.get $l2
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t9)
          local.set $l2
          local.get $p1
          i32.load offset=4
          local.set $l3
          local.get $l2
          i32.const 1
          i32.store offset=12
          local.get $l2
          i32.const 3
          i32.store16 offset=6
          local.get $l2
          i32.const 3127060
          i32.store offset=8
          local.get $l2
          i32.const 3126964
          i32.store
          local.get $l2
          local.get $l3
          i32.const 2
          i32.shl
          i32.const 3126948
          i32.add
          i32.load
          i32.store16 offset=4
          local.get $l2
          local.get $p1
          i32.load offset=12
          i32.store offset=16
          local.get $l2
          local.get $p1
          i32.load offset=68
          i32.store offset=20
          local.get $l2
          local.get $p1
          i32.load offset=16
          i32.store offset=24
          local.get $l2
          local.get $p1
          i32.load offset=72
          i32.store offset=28
          local.get $p1
          i32.const 32
          i32.add
          local.tee $l3
          f32.load
          local.set $l10
          local.get $p1
          i32.const 36
          i32.add
          local.tee $l4
          f32.load
          local.set $l11
          local.get $p1
          i32.const 24
          i32.add
          local.tee $l6
          f32.load
          local.set $l12
          local.get $p1
          f32.load offset=20
          local.set $l13
          local.get $l2
          local.get $p1
          i32.const 28
          i32.add
          local.tee $l5
          f32.load
          local.get $p1
          i32.const 40
          i32.add
          local.tee $l7
          f32.load
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=40
          local.get $l2
          local.get $l12
          local.get $l11
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=36
          local.get $l2
          local.get $l13
          local.get $l10
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=32
          local.get $l3
          f32.load
          local.set $l10
          local.get $l6
          f32.load
          local.set $l11
          local.get $l4
          f32.load
          local.set $l12
          local.get $p1
          f32.load offset=20
          local.set $l13
          local.get $l2
          local.get $l7
          f32.load
          local.get $l5
          f32.load
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=52
          local.get $l2
          local.get $l12
          local.get $l11
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=48
          local.get $l2
          local.get $l10
          local.get $l13
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=44
          local.get $l2
          local.get $p1
          i32.load offset=76
          i32.store offset=56
          local.get $l2
          local.get $p1
          f32.load offset=44
          f32.store offset=60
          local.get $l2
          local.get $p1
          i32.load8_u offset=8
          i32.store8 offset=64
          local.get $l2
          local.get $p1
          i32.const 80
          i32.add
          local.tee $l3
          i32.load
          i32.store offset=68
          local.get $l2
          local.get $p1
          i32.load offset=48
          i32.store offset=72
          local.get $p1
          i32.load offset=52
          local.set $l4
          local.get $l2
          local.get $p0
          i32.store offset=80
          local.get $l2
          local.get $l4
          i32.store offset=76
          local.get $l2
          local.get $p1
          i32.const 56
          i32.add
          local.tee $l6
          i32.load
          i32.store offset=84
          local.get $l2
          local.get $p1
          i32.load offset=60
          i32.store offset=88
          local.get $l2
          local.get $p1
          i32.const -64
          i32.sub
          local.tee $l4
          i32.load
          i32.store offset=92
          local.get $l2
          local.get $p1
          i32.load offset=84
          i32.store offset=96
          local.get $p1
          i64.const 0
          i64.store offset=48 align=4
          local.get $p1
          i32.const 0
          i32.store offset=16
          local.get $l6
          i64.const 0
          i64.store align=4
          local.get $l4
          i32.const 0
          i32.store
          local.get $p1
          i64.const 0
          i64.store offset=72 align=4
          local.get $l3
          i64.const 0
          i64.store align=4
          local.get $l2
          i64.const 0
          i64.store offset=196 align=4
          local.get $l2
          i32.const 3127588
          i32.store offset=8
          local.get $l2
          i32.const 3127492
          i32.store
          local.get $l2
          i32.const 184
          i32.add
          local.tee $l6
          i64.const 0
          i64.store
          local.get $l2
          i32.const 176
          i32.add
          local.tee $l3
          i32.const 4
          i32.store
          local.get $l2
          local.get $p1
          f32.load offset=96
          f32.store offset=112
          local.get $l2
          local.get $p1
          f32.load offset=100
          f32.store offset=116
          local.get $l2
          local.get $p1
          f32.load offset=104
          f32.store offset=120
          local.get $l2
          local.get $p1
          f32.load offset=108
          f32.store offset=124
          local.get $l2
          local.get $p1
          f32.load offset=112
          f32.store offset=128
          local.get $l2
          local.get $p1
          f32.load offset=116
          f32.store offset=132
          local.get $l2
          local.get $p1
          f32.load offset=120
          f32.store offset=136
          local.get $l2
          local.get $p1
          f32.load offset=124
          f32.store offset=140
          local.get $l2
          local.get $p1
          f32.load offset=128
          f32.store offset=144
          local.get $l2
          local.get $p1
          f32.load offset=132
          f32.store offset=148
          local.get $l2
          local.get $p1
          f32.load offset=136
          f32.store offset=152
          local.get $l2
          local.get $p1
          f32.load offset=140
          f32.store offset=156
          local.get $l2
          local.get $p1
          f32.load offset=144
          f32.store offset=160
          local.get $l2
          local.get $p1
          f32.load offset=148
          f32.store offset=164
          local.get $l2
          local.get $p1
          f32.load offset=152
          f32.store offset=168
          local.get $l2
          local.get $p1
          f32.load offset=156
          f32.store offset=172
          local.get $l3
          local.get $p1
          i64.load offset=160
          i64.store
          local.get $l6
          local.get $p1
          i64.load offset=168
          i64.store
          local.get $l2
          local.get $p1
          i64.load offset=176
          i64.store offset=192
          local.get $l2
          local.get $p1
          i32.const 184
          i32.add
          local.tee $p1
          i32.load
          i32.store offset=200
          local.get $p1
          i32.const 0
          i32.store
          br $B1
        end
        call $f69753
        local.tee $l2
        i32.const 184
        i32.const 3131102
        i32.const 3129657
        i32.const 4700888
        i32.load
        local.tee $l6
        local.get $l6
        i32.load
        i32.load offset=20
        call_indirect $__indirect_function_table (type $t5)
        select
        i32.const 3129364
        i32.const 119
        local.get $l2
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.tee $l2
        local.set $l3
        local.get $p1
        i32.load offset=4
        local.set $l5
        local.get $l3
        i32.const 1
        i32.store offset=12
        local.get $l3
        i32.const 3
        i32.store16 offset=6
        local.get $l3
        i32.const 3127060
        i32.store offset=8
        local.get $l3
        i32.const 3126964
        i32.store
        local.get $l3
        local.get $l5
        i32.const 2
        i32.shl
        i32.const 3126948
        i32.add
        i32.load
        i32.store16 offset=4
        local.get $l3
        local.get $p1
        i32.load offset=12
        i32.store offset=16
        local.get $l3
        local.get $p1
        i32.load offset=68
        i32.store offset=20
        local.get $l3
        local.get $p1
        i32.load offset=16
        i32.store offset=24
        local.get $l3
        local.get $p1
        i32.load offset=72
        i32.store offset=28
        local.get $p1
        i32.const 32
        i32.add
        local.tee $l5
        f32.load
        local.set $l10
        local.get $p1
        i32.const 36
        i32.add
        local.tee $l7
        f32.load
        local.set $l11
        local.get $p1
        i32.const 24
        i32.add
        local.tee $l6
        f32.load
        local.set $l12
        local.get $p1
        f32.load offset=20
        local.set $l13
        local.get $l3
        local.get $p1
        i32.const 28
        i32.add
        local.tee $l4
        f32.load
        local.get $p1
        i32.const 40
        i32.add
        local.tee $l9
        f32.load
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=40
        local.get $l3
        local.get $l12
        local.get $l11
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=36
        local.get $l3
        local.get $l13
        local.get $l10
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=32
        local.get $l5
        f32.load
        local.set $l10
        local.get $l6
        f32.load
        local.set $l11
        local.get $l7
        f32.load
        local.set $l12
        local.get $p1
        f32.load offset=20
        local.set $l13
        local.get $l3
        local.get $l9
        f32.load
        local.get $l4
        f32.load
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=52
        local.get $l3
        local.get $l12
        local.get $l11
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=48
        local.get $l3
        local.get $l10
        local.get $l13
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        f32.store offset=44
        local.get $l3
        local.get $p1
        i32.load offset=76
        i32.store offset=56
        local.get $l3
        local.get $p1
        f32.load offset=44
        f32.store offset=60
        local.get $l3
        local.get $p1
        i32.load8_u offset=8
        i32.store8 offset=64
        local.get $l3
        local.get $p1
        i32.const 80
        i32.add
        local.tee $l5
        i32.load
        i32.store offset=68
        local.get $l3
        local.get $p1
        i32.load offset=48
        i32.store offset=72
        local.get $p1
        i32.load offset=52
        local.set $l7
        local.get $l3
        local.get $p0
        i32.store offset=80
        local.get $l3
        local.get $l7
        i32.store offset=76
        local.get $l3
        local.get $p1
        i32.const 56
        i32.add
        local.tee $l6
        i32.load
        i32.store offset=84
        local.get $l3
        local.get $p1
        i32.load offset=60
        i32.store offset=88
        local.get $l3
        local.get $p1
        i32.const -64
        i32.sub
        local.tee $l7
        i32.load
        i32.store offset=92
        local.get $l3
        local.get $p1
        i32.load offset=84
        i32.store offset=96
        local.get $p1
        i64.const 0
        i64.store offset=48 align=4
        local.get $p1
        i32.const 0
        i32.store offset=16
        local.get $l6
        i64.const 0
        i64.store align=4
        local.get $l7
        i32.const 0
        i32.store
        local.get $p1
        i64.const 0
        i64.store offset=72 align=4
        local.get $l5
        i64.const 0
        i64.store align=4
        local.get $l3
        i32.const 3127472
        i32.store offset=8
        local.get $l3
        i32.const 3127376
        i32.store
        local.get $l3
        i32.const 100
        i32.add
        call $f1035
        local.set $l6
        local.get $l3
        i32.const 124
        i32.add
        call $f70244
        local.set $l5
        local.get $l6
        local.tee $l3
        local.get $p1
        i32.const 88
        i32.add
        local.tee $l4
        i32.load
        i32.store
        local.get $l3
        local.get $l4
        i32.load offset=4
        i32.store offset=4
        local.get $l3
        local.get $l4
        i32.load offset=12
        i32.store offset=12
        local.get $l3
        local.get $l4
        i32.const 16
        i32.add
        local.tee $l9
        i32.load
        i32.store offset=16
        local.get $l3
        local.get $l4
        i32.load offset=20
        i32.store offset=20
        local.get $l3
        local.get $l4
        i32.const 8
        i32.add
        local.tee $l3
        i32.load
        i32.store offset=8
        local.get $l9
        i64.const 0
        i64.store align=4
        local.get $l3
        i64.const 0
        i64.store align=4
        local.get $l4
        i64.const 0
        i64.store align=4
        local.get $l5
        local.get $p1
        i32.const 112
        i32.add
        local.tee $l4
        i32.load
        i32.store
        local.get $l5
        local.get $l4
        f32.load offset=4
        f32.store offset=4
        local.get $l5
        local.get $l4
        f32.load offset=8
        f32.store offset=8
        local.get $l5
        local.get $l4
        f32.load offset=12
        f32.store offset=12
        local.get $l5
        local.get $l4
        f32.load offset=16
        f32.store offset=16
        local.get $l5
        local.get $l4
        i32.load offset=20
        i32.store offset=20
        local.get $l5
        local.get $l4
        i32.load offset=24
        i32.store offset=24
        local.get $l5
        local.get $l4
        i32.const 28
        i32.add
        local.tee $l9
        i32.load
        i32.store offset=28
        local.get $l5
        local.get $l4
        f32.load offset=32
        f32.store offset=32
        local.get $l5
        local.get $l4
        i32.const 36
        i32.add
        local.tee $p1
        f32.load
        f32.store offset=36
        local.get $l5
        local.get $l4
        f32.load offset=40
        f32.store offset=40
        local.get $l5
        local.get $l4
        i32.const 44
        i32.add
        local.tee $l3
        f32.load
        f32.store offset=44
        local.get $l5
        local.get $l4
        f32.load offset=48
        f32.store offset=48
        local.get $l5
        local.get $l4
        f32.load offset=52
        f32.store offset=52
        local.get $l5
        local.get $l4
        i32.load8_u offset=56
        i32.store8 offset=56
        local.get $l5
        local.get $l4
        i32.load8_u offset=57
        i32.store8 offset=57
        local.get $l4
        i64.const 0
        i64.store offset=20 align=4
        local.get $l4
        i32.const 0
        i32.store
        local.get $l9
        i64.const 0
        i64.store align=4
        local.get $p1
        i64.const 0
        i64.store align=4
        local.get $l3
        i64.const 0
        i64.store align=4
        local.get $l4
        i64.const 0
        i64.store offset=50 align=2
        local.get $l5
        local.get $l6
        i32.store
      end
      local.get $l8
      local.get $l2
      i32.store offset=8
      local.get $l2
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load offset=4
      drop
      local.get $p0
      i32.const 8
      i32.add
      local.get $l8
      i32.const 8
      i32.add
      local.get $l8
      i32.const 15
      i32.add
      call $f70405
      local.set $p1
      local.get $l8
      i32.load8_u offset=15
      i32.eqz
      if $I4
        local.get $p1
        local.get $l8
        i32.load offset=8
        i32.store
      end
      local.get $p0
      i32.load offset=4
      drop
    end
    local.get $l8
    i32.const 16
    i32.add
    global.set $g0
    local.get $l2)
