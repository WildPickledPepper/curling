  (func $f72776 (type $t8) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (result i32)
    (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32)
    global.get $g0
    i32.const 304
    i32.sub
    local.tee $l4
    global.set $g0
    local.get $l4
    i32.const 1
    i32.store8 offset=248
    local.get $l4
    i64.const 68719476736
    i64.store offset=256
    local.get $l4
    local.get $l4
    i32.const 184
    i32.add
    i32.store offset=252
    local.get $p0
    local.get $p0
    i32.load
    i32.load offset=92
    call_indirect $__indirect_function_table (type $t5)
    local.set $l5
    local.get $l4
    i32.const 0
    i32.store offset=128
    local.get $l4
    i32.const 128
    i32.add
    local.set $l9
    local.get $l5
    local.tee $l8
    local.get $l4
    i32.const 184
    i32.add
    local.tee $l10
    i32.load offset=76
    i32.const 2147483647
    i32.and
    i32.gt_u
    if $I0
      local.get $l10
      local.set $l5
      block $B1 (result i32)
        i32.const 0
        local.get $l8
        i32.eqz
        br_if $B1
        drop
        block $B2
          local.get $l8
          i32.const 2
          i32.shl
          local.tee $l7
          i32.const 64
          i32.gt_u
          br_if $B2
          local.get $l5
          i32.load8_u offset=64
          br_if $B2
          local.get $l5
          i32.const 1
          i32.store8 offset=64
          local.get $l5
          br $B1
        end
        i32.const 0
        local.get $l7
        i32.eqz
        br_if $B1
        drop
        call $f69753
        local.tee $l6
        local.get $l7
        i32.const 3209624
        i32.const 3209596
        i32.const 4700888
        i32.load
        local.tee $l13
        local.get $l13
        i32.load
        i32.load offset=20
        call_indirect $__indirect_function_table (type $t5)
        select
        i32.const 3209554
        i32.const 553
        local.get $l6
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
      end
      local.set $l11
      local.get $l5
      i32.load offset=72
      local.tee $l7
      i32.const 0
      i32.gt_s
      if $I3
        local.get $l11
        local.get $l7
        i32.const 2
        i32.shl
        i32.add
        local.set $l13
        local.get $l5
        i32.load offset=68
        local.set $l7
        local.get $l11
        local.set $l6
        loop $L4
          local.get $l6
          local.get $l7
          i32.load
          i32.store
          local.get $l7
          i32.const 4
          i32.add
          local.set $l7
          local.get $l6
          i32.const 4
          i32.add
          local.tee $l6
          local.get $l13
          i32.lt_u
          br_if $L4
        end
      end
      block $B5
        local.get $l5
        i32.load offset=76
        i32.const 0
        i32.lt_s
        br_if $B5
        local.get $l5
        i32.load offset=68
        local.tee $l7
        local.get $l5
        i32.eq
        if $I6
          local.get $l5
          i32.const 0
          i32.store8 offset=64
          br $B5
        end
        local.get $l7
        i32.eqz
        br_if $B5
        call $f69753
        local.tee $l6
        local.get $l7
        local.get $l6
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $l5
      local.get $l8
      i32.store offset=76
      local.get $l5
      local.get $l11
      i32.store offset=68
    end
    local.get $l8
    local.get $l10
    i32.load offset=72
    local.tee $l6
    i32.gt_s
    if $I7
      local.get $l10
      i32.load offset=68
      local.tee $l11
      local.get $l8
      i32.const 2
      i32.shl
      i32.add
      local.set $l5
      local.get $l11
      local.get $l6
      i32.const 2
      i32.shl
      i32.add
      local.set $l6
      loop $L8
        local.get $l6
        local.get $l9
        i32.load
        i32.store
        local.get $l6
        i32.const 4
        i32.add
        local.tee $l6
        local.get $l5
        i32.lt_u
        br_if $L8
      end
    end
    local.get $l10
    local.get $l8
    i32.store offset=72
    local.get $p0
    local.get $l4
    i32.load offset=252
    local.get $l4
    i32.load offset=256
    i32.const 0
    local.get $p0
    i32.load
    i32.load offset=96
    call_indirect $__indirect_function_table (type $t8)
    drop
    block $B9 (result i32)
      block $B10
        block $B11
          block $B12
            local.get $p1
            local.get $p2
            local.get $p1
            select
            f32.load
            local.tee $l24
            i32.reinterpret_f32
            i32.const 2139095040
            i32.and
            i32.const 2139095040
            i32.ne
            if $I13
              local.get $l4
              i32.load offset=256
              br_if $B12
              br $B11
            end
            i32.const 4700888
            i32.load
            i32.const 4
            i32.const 3210117
            i32.const 128
            i32.const 3210321
            i32.const 0
            call $f69760
            i32.const 0
            br $B9
          end
          local.get $l4
          i32.const 280
          i32.add
          local.set $l6
          local.get $l4
          i32.const 16
          i32.add
          local.set $l11
          local.get $l4
          i32.const 104
          i32.add
          local.set $l9
          local.get $l4
          i32.const 88
          i32.add
          i32.const 4
          i32.or
          local.set $l8
          local.get $l4
          i32.const 125
          i32.add
          local.set $l10
          loop $L14
            local.get $l4
            i32.const 128
            i32.add
            local.get $l12
            i32.const 2
            i32.shl
            local.tee $p0
            local.get $l4
            i32.load offset=252
            i32.add
            i32.load
            local.tee $l5
            local.get $l5
            i32.load
            i32.load offset=156
            call_indirect $__indirect_function_table (type $t1)
            block $B15
              local.get $l4
              i32.load8_u offset=128
              i32.const 1
              i32.and
              i32.eqz
              if $I16
                local.get $l28
                local.set $l16
                br $B15
              end
              block $B17
                block $B18
                  block $B19
                    block $B20
                      block $B21
                        local.get $l4
                        i32.load offset=252
                        local.get $p0
                        i32.add
                        i32.load
                        local.tee $l5
                        local.get $l5
                        i32.load
                        i32.load offset=32
                        call_indirect $__indirect_function_table (type $t5)
                        i32.const 1
                        i32.add
                        br_table $B10 $B21 $B10 $B19 $B20 $B18 $B10 $B10 $B10 $B17
                      end
                      local.get $l4
                      i64.const 0
                      i64.store offset=48
                      local.get $l4
                      i32.load offset=252
                      local.get $p0
                      i32.add
                      i32.load
                      local.tee $l5
                      local.get $l4
                      i32.const 48
                      i32.add
                      local.get $l5
                      i32.load
                      i32.load offset=48
                      call_indirect $__indirect_function_table (type $t0)
                      drop
                      local.get $l4
                      i32.const 264
                      i32.add
                      local.get $l4
                      i32.load offset=252
                      local.get $p0
                      i32.add
                      i32.load
                      local.tee $p0
                      local.get $p0
                      i32.load
                      i32.load offset=80
                      call_indirect $__indirect_function_table (type $t1)
                      local.get $l4
                      i32.const 0
                      i32.store offset=172
                      local.get $l4
                      i64.const 0
                      i64.store offset=164 align=4
                      local.get $l4
                      i32.const 0
                      i32.store offset=156
                      local.get $l4
                      i64.const 0
                      i64.store offset=148 align=4
                      local.get $l4
                      i32.const 0
                      i32.store offset=140
                      local.get $l4
                      i64.const 0
                      i64.store offset=132 align=4
                      local.get $l4
                      local.get $l4
                      f32.load offset=52
                      local.tee $l15
                      local.get $l15
                      local.get $l15
                      f32.const 0x1.0c1524p+2 (;=4.18879;)
                      f32.mul
                      f32.mul
                      f32.mul
                      local.tee $l16
                      f32.store offset=176
                      local.get $l4
                      local.get $l15
                      local.get $l15
                      local.get $l16
                      f32.mul
                      f32.mul
                      f32.const 0x1.99999ap-2 (;=0.4;)
                      f32.mul
                      local.tee $l15
                      f32.store offset=160
                      local.get $l4
                      local.get $l15
                      f32.store offset=144
                      local.get $l4
                      local.get $l15
                      f32.store offset=128
                      local.get $l4
                      f32.const 0x1p+0 (;=1;)
                      local.get $l4
                      f32.load offset=264
                      local.tee $l15
                      local.get $l15
                      local.get $l15
                      f32.add
                      local.tee $l16
                      f32.mul
                      f32.sub
                      local.tee $l20
                      local.get $l4
                      f32.load offset=268
                      local.tee $l18
                      local.get $l18
                      local.get $l18
                      f32.add
                      local.tee $l17
                      f32.mul
                      local.tee $l22
                      f32.sub
                      f32.store offset=120
                      local.get $l4
                      local.get $l17
                      local.get $l4
                      f32.load offset=272
                      local.tee $l15
                      f32.mul
                      local.tee $l19
                      local.get $l16
                      local.get $l4
                      f32.load offset=276
                      local.tee $l21
                      f32.mul
                      local.tee $l23
                      f32.sub
                      f32.store offset=116
                      local.get $l4
                      local.get $l16
                      local.get $l15
                      f32.mul
                      local.tee $l25
                      local.get $l17
                      local.get $l21
                      f32.mul
                      local.tee $l17
                      f32.add
                      f32.store offset=112
                      local.get $l4
                      local.get $l19
                      local.get $l23
                      f32.add
                      f32.store offset=108
                      local.get $l4
                      local.get $l20
                      local.get $l15
                      local.get $l15
                      local.get $l15
                      f32.add
                      local.tee $l19
                      f32.mul
                      local.tee $l15
                      f32.sub
                      f32.store offset=104
                      local.get $l4
                      local.get $l16
                      local.get $l18
                      f32.mul
                      local.tee $l16
                      local.get $l19
                      local.get $l21
                      f32.mul
                      local.tee $l18
                      f32.sub
                      f32.store offset=100
                      local.get $l4
                      local.get $l25
                      local.get $l17
                      f32.sub
                      f32.store offset=96
                      local.get $l4
                      local.get $l16
                      local.get $l18
                      f32.add
                      f32.store offset=92
                      local.get $l4
                      f32.const 0x1p+0 (;=1;)
                      local.get $l22
                      f32.sub
                      local.get $l15
                      f32.sub
                      f32.store offset=88
                      local.get $l4
                      i32.const 128
                      i32.add
                      local.get $l4
                      i32.const 88
                      i32.add
                      call $f72798
                      local.get $l4
                      i32.const 128
                      i32.add
                      local.get $l6
                      call $f72775
                      br $B17
                    end
                    local.get $l4
                    i32.const 0
                    i32.store offset=60
                    local.get $l4
                    i64.const 0
                    i64.store offset=52 align=4
                    local.get $l4
                    i32.const 3
                    i32.store offset=48
                    local.get $l4
                    i32.load offset=252
                    local.get $p0
                    i32.add
                    i32.load
                    local.tee $l5
                    local.get $l4
                    i32.const 48
                    i32.add
                    local.get $l5
                    i32.load
                    i32.load offset=44
                    call_indirect $__indirect_function_table (type $t0)
                    drop
                    local.get $l4
                    i32.const 264
                    i32.add
                    local.get $l4
                    i32.load offset=252
                    local.get $p0
                    i32.add
                    i32.load
                    local.tee $p0
                    local.get $p0
                    i32.load
                    i32.load offset=80
                    call_indirect $__indirect_function_table (type $t1)
                    local.get $l4
                    i32.const 0
                    i32.store offset=172
                    local.get $l4
                    i64.const 0
                    i64.store offset=164 align=4
                    local.get $l4
                    i32.const 0
                    i32.store offset=156
                    local.get $l4
                    i64.const 0
                    i64.store offset=148 align=4
                    local.get $l4
                    i32.const 0
                    i32.store offset=140
                    local.get $l4
                    i64.const 0
                    i64.store offset=132 align=4
                    local.get $l4
                    local.get $l4
                    f32.load offset=60
                    local.tee $l15
                    local.get $l4
                    f32.load offset=56
                    local.tee $l16
                    local.get $l4
                    f32.load offset=52
                    local.tee $l18
                    f32.const 0x1p+0 (;=1;)
                    local.get $l18
                    f32.const 0x0p+0 (;=0;)
                    f32.ne
                    select
                    local.tee $l17
                    f32.mul
                    local.get $l17
                    local.get $l16
                    f32.const 0x0p+0 (;=0;)
                    f32.ne
                    select
                    local.tee $l17
                    f32.mul
                    local.get $l17
                    local.get $l15
                    f32.const 0x0p+0 (;=0;)
                    f32.ne
                    select
                    f32.const 0x1p+3 (;=8;)
                    f32.mul
                    local.tee $l17
                    f32.store offset=176
                    local.get $l4
                    local.get $l18
                    local.get $l18
                    f32.mul
                    local.tee $l18
                    local.get $l16
                    local.get $l16
                    f32.mul
                    local.tee $l21
                    f32.add
                    local.get $l17
                    f32.const 0x1.555556p-2 (;=0.333333;)
                    f32.mul
                    local.tee $l16
                    f32.mul
                    f32.store offset=160
                    local.get $l4
                    local.get $l18
                    local.get $l15
                    local.get $l15
                    f32.mul
                    local.tee $l15
                    f32.add
                    local.get $l16
                    f32.mul
                    f32.store offset=144
                    local.get $l4
                    local.get $l21
                    local.get $l15
                    f32.add
                    local.get $l16
                    f32.mul
                    f32.store offset=128
                    local.get $l4
                    f32.const 0x1p+0 (;=1;)
                    local.get $l4
                    f32.load offset=264
                    local.tee $l15
                    local.get $l15
                    local.get $l15
                    f32.add
                    local.tee $l16
                    f32.mul
                    f32.sub
                    local.tee $l20
                    local.get $l4
                    f32.load offset=268
                    local.tee $l18
                    local.get $l18
                    local.get $l18
                    f32.add
                    local.tee $l17
                    f32.mul
                    local.tee $l22
                    f32.sub
                    f32.store offset=120
                    local.get $l4
                    local.get $l17
                    local.get $l4
                    f32.load offset=272
                    local.tee $l15
                    f32.mul
                    local.tee $l19
                    local.get $l16
                    local.get $l4
                    f32.load offset=276
                    local.tee $l21
                    f32.mul
                    local.tee $l23
                    f32.sub
                    f32.store offset=116
                    local.get $l4
                    local.get $l16
                    local.get $l15
                    f32.mul
                    local.tee $l25
                    local.get $l17
                    local.get $l21
                    f32.mul
                    local.tee $l17
                    f32.add
                    f32.store offset=112
                    local.get $l4
                    local.get $l19
                    local.get $l23
                    f32.add
                    f32.store offset=108
                    local.get $l4
                    local.get $l20
                    local.get $l15
                    local.get $l15
                    local.get $l15
                    f32.add
                    local.tee $l19
                    f32.mul
                    local.tee $l15
                    f32.sub
                    f32.store offset=104
                    local.get $l4
                    local.get $l16
                    local.get $l18
                    f32.mul
                    local.tee $l16
                    local.get $l19
                    local.get $l21
                    f32.mul
                    local.tee $l18
                    f32.sub
                    f32.store offset=100
                    local.get $l4
                    local.get $l25
                    local.get $l17
                    f32.sub
                    f32.store offset=96
                    local.get $l4
                    local.get $l16
                    local.get $l18
                    f32.add
                    f32.store offset=92
                    local.get $l4
                    f32.const 0x1p+0 (;=1;)
                    local.get $l22
                    f32.sub
                    local.get $l15
                    f32.sub
                    f32.store offset=88
                    local.get $l4
                    i32.const 128
                    i32.add
                    local.get $l4
                    i32.const 88
                    i32.add
                    call $f72798
                    local.get $l4
                    i32.const 128
                    i32.add
                    local.get $l6
                    call $f72775
                    br $B17
                  end
                  local.get $l4
                  i64.const 0
                  i64.store offset=52 align=4
                  local.get $l4
                  i32.const 2
                  i32.store offset=48
                  local.get $l4
                  i32.load offset=252
                  local.get $p0
                  i32.add
                  i32.load
                  local.tee $l5
                  local.get $l4
                  i32.const 48
                  i32.add
                  local.get $l5
                  i32.load
                  i32.load offset=52
                  call_indirect $__indirect_function_table (type $t0)
                  drop
                  local.get $l4
                  i32.const 264
                  i32.add
                  local.get $l4
                  i32.load offset=252
                  local.get $p0
                  i32.add
                  i32.load
                  local.tee $p0
                  local.get $p0
                  i32.load
                  i32.load offset=80
                  call_indirect $__indirect_function_table (type $t1)
                  local.get $l4
                  i32.const 0
                  i32.store offset=172
                  local.get $l4
                  i64.const 0
                  i64.store offset=164 align=4
                  local.get $l4
                  i32.const 0
                  i32.store offset=156
                  local.get $l4
                  i64.const 0
                  i64.store offset=148 align=4
                  local.get $l4
                  i32.const 0
                  i32.store offset=140
                  local.get $l4
                  i64.const 0
                  i64.store offset=132 align=4
                  local.get $l4
                  local.get $l4
                  f32.load offset=52
                  local.tee $l15
                  local.get $l15
                  local.get $l15
                  f32.const 0x1.0c1524p+2 (;=4.18879;)
                  f32.mul
                  f32.mul
                  f32.mul
                  local.get $l15
                  local.get $l15
                  f32.const 0x1.921fb6p+1 (;=3.14159;)
                  f32.mul
                  f32.mul
                  local.tee $l18
                  local.get $l4
                  f32.load offset=56
                  local.tee $l16
                  local.get $l16
                  f32.add
                  f32.mul
                  f32.add
                  f32.store offset=176
                  local.get $l4
                  local.get $l18
                  local.get $l15
                  local.get $l15
                  local.get $l16
                  f32.mul
                  f32.mul
                  local.tee $l17
                  local.get $l15
                  local.get $l15
                  local.get $l15
                  f32.mul
                  f32.mul
                  f32.const 0x1p+3 (;=8;)
                  f32.mul
                  f32.const 0x1.ep+3 (;=15;)
                  f32.div
                  local.tee $l21
                  f32.add
                  f32.mul
                  f32.store offset=128
                  local.get $l4
                  local.get $l18
                  local.get $l16
                  local.get $l16
                  local.get $l16
                  f32.mul
                  local.tee $l20
                  f32.mul
                  local.tee $l16
                  local.get $l16
                  f32.add
                  f32.const 0x1.8p+1 (;=3;)
                  f32.div
                  local.get $l15
                  local.get $l20
                  f32.mul
                  f32.const 0x1p+2 (;=4;)
                  f32.mul
                  f32.const 0x1.8p+1 (;=3;)
                  f32.div
                  local.get $l21
                  local.get $l17
                  f32.const 0x1.8p+1 (;=3;)
                  f32.mul
                  f32.const 0x1p-1 (;=0.5;)
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.mul
                  local.tee $l15
                  f32.store offset=160
                  local.get $l4
                  local.get $l15
                  f32.store offset=144
                  local.get $l4
                  f32.const 0x1p+0 (;=1;)
                  local.get $l4
                  f32.load offset=264
                  local.tee $l15
                  local.get $l15
                  local.get $l15
                  f32.add
                  local.tee $l16
                  f32.mul
                  f32.sub
                  local.tee $l20
                  local.get $l4
                  f32.load offset=268
                  local.tee $l18
                  local.get $l18
                  local.get $l18
                  f32.add
                  local.tee $l17
                  f32.mul
                  local.tee $l22
                  f32.sub
                  f32.store offset=120
                  local.get $l4
                  local.get $l17
                  local.get $l4
                  f32.load offset=272
                  local.tee $l15
                  f32.mul
                  local.tee $l19
                  local.get $l16
                  local.get $l4
                  f32.load offset=276
                  local.tee $l21
                  f32.mul
                  local.tee $l23
                  f32.sub
                  f32.store offset=116
                  local.get $l4
                  local.get $l16
                  local.get $l15
                  f32.mul
                  local.tee $l25
                  local.get $l17
                  local.get $l21
                  f32.mul
                  local.tee $l17
                  f32.add
                  f32.store offset=112
                  local.get $l4
                  local.get $l19
                  local.get $l23
                  f32.add
                  f32.store offset=108
                  local.get $l4
                  local.get $l20
                  local.get $l15
                  local.get $l15
                  local.get $l15
                  f32.add
                  local.tee $l19
                  f32.mul
                  local.tee $l15
                  f32.sub
                  f32.store offset=104
                  local.get $l4
                  local.get $l16
                  local.get $l18
                  f32.mul
                  local.tee $l16
                  local.get $l19
                  local.get $l21
                  f32.mul
                  local.tee $l18
                  f32.sub
                  f32.store offset=100
                  local.get $l4
                  local.get $l25
                  local.get $l17
                  f32.sub
                  f32.store offset=96
                  local.get $l4
                  local.get $l16
                  local.get $l18
                  f32.add
                  f32.store offset=92
                  local.get $l4
                  f32.const 0x1p+0 (;=1;)
                  local.get $l22
                  f32.sub
                  local.get $l15
                  f32.sub
                  f32.store offset=88
                  local.get $l4
                  i32.const 128
                  i32.add
                  local.get $l4
                  i32.const 88
                  i32.add
                  call $f72798
                  local.get $l4
                  i32.const 128
                  i32.add
                  local.get $l6
                  call $f72775
                  br $B17
                end
                local.get $l4
                i32.const 1
                i32.store8 offset=124
                local.get $l4
                i32.const 0
                i32.store offset=120
                local.get $l4
                i64.const 4575657221408423936
                i64.store offset=112
                local.get $l4
                i64.const 0
                i64.store offset=104
                local.get $l4
                i64.const 4575657222473777152
                i64.store offset=96
                local.get $l4
                i64.const 4575657221408423940
                i64.store offset=88
                local.get $l10
                i32.const 0
                i32.store8 offset=2
                local.get $l10
                i32.const 0
                i32.store16 align=1
                local.get $l4
                i32.load offset=252
                local.get $p0
                i32.add
                i32.load
                local.tee $l5
                local.get $l4
                i32.const 88
                i32.add
                local.get $l5
                i32.load
                i32.load offset=60
                call_indirect $__indirect_function_table (type $t0)
                drop
                local.get $l4
                i32.load offset=120
                local.tee $l5
                local.get $l4
                i32.const 84
                i32.add
                local.get $l4
                i32.const 48
                i32.add
                local.get $l4
                i32.const 32
                i32.add
                local.get $l5
                i32.load
                i32.load offset=52
                call_indirect $__indirect_function_table (type $t4)
                local.get $l4
                f32.load offset=100
                local.set $l22
                local.get $l4
                f32.load offset=96
                local.set $l20
                block $B22
                  block $B23
                    local.get $l4
                    f32.load offset=92
                    local.tee $l19
                    f32.const 0x1p+0 (;=1;)
                    f32.ne
                    br_if $B23
                    local.get $l20
                    f32.const 0x1p+0 (;=1;)
                    f32.ne
                    br_if $B23
                    local.get $l22
                    f32.const 0x1p+0 (;=1;)
                    f32.ne
                    br_if $B23
                    local.get $l4
                    f32.load offset=80
                    local.set $l15
                    local.get $l4
                    f32.load offset=76
                    local.set $l16
                    local.get $l4
                    f32.load offset=72
                    local.set $l18
                    local.get $l4
                    f32.load offset=68
                    local.set $l17
                    local.get $l4
                    f32.load offset=64
                    local.set $l21
                    local.get $l4
                    f32.load offset=60
                    local.set $l20
                    local.get $l4
                    f32.load offset=56
                    local.set $l22
                    local.get $l4
                    f32.load offset=52
                    local.set $l19
                    local.get $l4
                    f32.load offset=48
                    local.set $l23
                    br $B22
                  end
                  local.get $l4
                  local.get $l4
                  f32.load offset=84
                  local.get $l19
                  local.get $l20
                  f32.mul
                  local.get $l22
                  f32.mul
                  f32.mul
                  f32.store offset=84
                  local.get $l4
                  local.get $l4
                  f32.load offset=104
                  local.tee $l15
                  local.get $l4
                  f32.load offset=112
                  local.tee $l16
                  local.get $l22
                  local.get $l4
                  f32.load offset=40
                  local.tee $l18
                  local.get $l18
                  f32.add
                  local.tee $l23
                  local.get $l4
                  f32.load offset=116
                  local.tee $l18
                  local.get $l18
                  f32.mul
                  f32.const -0x1p-1 (;=-0.5;)
                  f32.add
                  local.tee $l21
                  f32.mul
                  local.get $l18
                  local.get $l15
                  local.get $l4
                  f32.load offset=36
                  local.tee $l17
                  local.get $l17
                  f32.add
                  local.tee $l25
                  f32.mul
                  local.get $l4
                  f32.load offset=32
                  local.tee $l17
                  local.get $l17
                  f32.add
                  local.tee $l26
                  local.get $l4
                  f32.load offset=108
                  local.tee $l17
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  local.get $l16
                  local.get $l26
                  local.get $l15
                  f32.mul
                  local.get $l25
                  local.get $l17
                  f32.mul
                  f32.add
                  local.get $l23
                  local.get $l16
                  f32.mul
                  f32.add
                  local.tee $l27
                  f32.mul
                  f32.add
                  f32.mul
                  local.tee $l22
                  local.get $l22
                  f32.add
                  local.tee $l22
                  f32.mul
                  local.get $l15
                  local.get $l19
                  local.get $l15
                  local.get $l27
                  f32.mul
                  local.get $l26
                  local.get $l21
                  f32.mul
                  local.get $l18
                  local.get $l23
                  local.get $l17
                  f32.mul
                  local.get $l25
                  local.get $l16
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  f32.add
                  f32.mul
                  local.tee $l19
                  local.get $l19
                  f32.add
                  local.tee $l19
                  f32.mul
                  local.get $l17
                  local.get $l20
                  local.get $l17
                  local.get $l27
                  f32.mul
                  local.get $l25
                  local.get $l21
                  f32.mul
                  local.get $l18
                  local.get $l26
                  local.get $l16
                  f32.mul
                  local.get $l23
                  local.get $l15
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  f32.add
                  f32.mul
                  local.tee $l20
                  local.get $l20
                  f32.add
                  local.tee $l20
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l23
                  f32.mul
                  local.get $l21
                  local.get $l19
                  f32.mul
                  local.get $l18
                  local.get $l17
                  local.get $l22
                  f32.mul
                  local.get $l16
                  local.get $l20
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.sub
                  f32.add
                  f32.store offset=32
                  local.get $l4
                  local.get $l17
                  local.get $l23
                  f32.mul
                  local.get $l21
                  local.get $l20
                  f32.mul
                  local.get $l18
                  local.get $l16
                  local.get $l19
                  f32.mul
                  local.get $l15
                  local.get $l22
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.sub
                  f32.add
                  f32.store offset=36
                  local.get $l4
                  local.get $l21
                  local.get $l22
                  f32.mul
                  local.get $l18
                  local.get $l15
                  local.get $l20
                  f32.mul
                  local.get $l17
                  local.get $l19
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.sub
                  local.get $l16
                  local.get $l23
                  f32.mul
                  f32.add
                  f32.store offset=40
                  global.get $g0
                  i32.const 96
                  i32.sub
                  local.tee $l5
                  global.set $g0
                  local.get $l5
                  i32.const 56
                  i32.add
                  local.get $l4
                  i32.const 48
                  i32.add
                  local.get $l9
                  call $f72779
                  local.get $l5
                  f32.load offset=88
                  local.set $l22
                  local.get $l5
                  f32.load offset=72
                  local.set $l23
                  local.get $l5
                  f32.load offset=60
                  local.set $l27
                  local.get $l5
                  f32.load offset=64
                  local.set $l16
                  local.get $l5
                  f32.load offset=56
                  local.set $l25
                  local.get $l5
                  local.get $l8
                  f32.load
                  local.tee $l17
                  local.get $l8
                  f32.load offset=4
                  local.tee $l20
                  f32.mul
                  local.get $l8
                  f32.load offset=8
                  local.tee $l21
                  f32.mul
                  local.tee $l19
                  local.get $l21
                  local.get $l20
                  local.get $l5
                  f32.load offset=76
                  f32.mul
                  f32.mul
                  f32.mul
                  local.tee $l26
                  f32.store offset=44
                  local.get $l5
                  local.get $l26
                  f32.store offset=36
                  local.get $l5
                  local.get $l19
                  local.get $l17
                  local.get $l17
                  local.get $l25
                  f32.const 0x1p-1 (;=0.5;)
                  f32.mul
                  local.get $l23
                  f32.const 0x1p-1 (;=0.5;)
                  f32.mul
                  f32.add
                  local.get $l22
                  f32.const 0x1p-1 (;=0.5;)
                  f32.mul
                  f32.add
                  local.tee $l26
                  local.get $l25
                  f32.sub
                  f32.mul
                  f32.mul
                  local.tee $l25
                  local.get $l20
                  local.get $l20
                  local.get $l26
                  local.get $l23
                  f32.sub
                  f32.mul
                  f32.mul
                  local.tee $l23
                  f32.add
                  f32.mul
                  f32.store offset=48
                  local.get $l5
                  local.get $l19
                  local.get $l21
                  local.get $l21
                  local.get $l26
                  local.get $l22
                  f32.sub
                  f32.mul
                  f32.mul
                  local.tee $l22
                  local.get $l25
                  f32.add
                  f32.mul
                  f32.store offset=32
                  local.get $l5
                  local.get $l19
                  local.get $l21
                  local.get $l17
                  local.get $l16
                  f32.mul
                  f32.mul
                  f32.mul
                  local.tee $l21
                  f32.store offset=40
                  local.get $l5
                  local.get $l19
                  local.get $l20
                  local.get $l17
                  local.get $l27
                  f32.mul
                  f32.mul
                  f32.mul
                  local.tee $l17
                  f32.store offset=28
                  local.get $l5
                  local.get $l21
                  f32.store offset=24
                  local.get $l5
                  local.get $l17
                  f32.store offset=20
                  local.get $l5
                  local.get $l19
                  local.get $l23
                  local.get $l22
                  f32.add
                  f32.mul
                  f32.store offset=16
                  local.get $l9
                  f32.load
                  local.set $l19
                  local.get $l9
                  f32.load offset=4
                  local.set $l17
                  local.get $l9
                  f32.load offset=8
                  local.set $l20
                  local.get $l5
                  local.get $l9
                  f32.load offset=12
                  f32.store offset=12
                  local.get $l5
                  local.get $l20
                  f32.neg
                  f32.store offset=8
                  local.get $l5
                  local.get $l17
                  f32.neg
                  f32.store offset=4
                  local.get $l5
                  local.get $l19
                  f32.neg
                  f32.store
                  local.get $l4
                  i32.const 264
                  i32.add
                  local.get $l5
                  i32.const 16
                  i32.add
                  local.get $l5
                  call $f72779
                  local.get $l5
                  i32.const 96
                  i32.add
                  global.set $g0
                  local.get $l4
                  local.get $l4
                  f32.load offset=264
                  local.tee $l23
                  f32.store offset=48
                  local.get $l4
                  local.get $l4
                  f32.load offset=268
                  local.tee $l19
                  f32.store offset=52
                  local.get $l4
                  local.get $l4
                  f32.load offset=272
                  local.tee $l22
                  f32.store offset=56
                  local.get $l4
                  local.get $l4
                  f32.load offset=276
                  local.tee $l20
                  f32.store offset=60
                  local.get $l4
                  local.get $l4
                  f32.load offset=280
                  local.tee $l21
                  f32.store offset=64
                  local.get $l4
                  local.get $l4
                  f32.load offset=284
                  local.tee $l17
                  f32.store offset=68
                  local.get $l4
                  local.get $l4
                  f32.load offset=288
                  local.tee $l18
                  f32.store offset=72
                  local.get $l4
                  local.get $l4
                  f32.load offset=292
                  local.tee $l16
                  f32.store offset=76
                  local.get $l4
                  local.get $l4
                  f32.load offset=296
                  local.tee $l15
                  f32.store offset=80
                end
                local.get $l4
                local.get $l4
                f32.load offset=84
                f32.store offset=176
                local.get $l4
                local.get $l4
                f32.load offset=40
                f32.store offset=172
                local.get $l4
                local.get $l4
                i64.load offset=32
                i64.store offset=164 align=4
                local.get $l4
                local.get $l15
                f32.store offset=160
                local.get $l4
                local.get $l16
                f32.store offset=156
                local.get $l4
                local.get $l18
                f32.store offset=152
                local.get $l4
                local.get $l17
                f32.store offset=148
                local.get $l4
                local.get $l21
                f32.store offset=144
                local.get $l4
                local.get $l20
                f32.store offset=140
                local.get $l4
                local.get $l22
                f32.store offset=136
                local.get $l4
                local.get $l19
                f32.store offset=132
                local.get $l4
                local.get $l23
                f32.store offset=128
                local.get $l4
                local.get $l4
                i32.load offset=252
                local.get $p0
                i32.add
                i32.load
                local.tee $p0
                local.get $p0
                i32.load
                i32.load offset=80
                call_indirect $__indirect_function_table (type $t1)
                local.get $l4
                local.get $l4
                f32.load offset=4
                local.tee $l16
                local.get $l16
                f32.add
                local.tee $l17
                local.get $l4
                f32.load offset=8
                local.tee $l15
                f32.mul
                local.tee $l22
                local.get $l4
                f32.load
                local.tee $l21
                local.get $l21
                f32.add
                local.tee $l18
                local.get $l4
                f32.load offset=12
                local.tee $l20
                f32.mul
                local.tee $l19
                f32.sub
                f32.store offset=292
                local.get $l4
                local.get $l18
                local.get $l15
                f32.mul
                local.tee $l23
                local.get $l17
                local.get $l20
                f32.mul
                local.tee $l25
                f32.add
                f32.store offset=288
                local.get $l4
                local.get $l22
                local.get $l19
                f32.add
                f32.store offset=284
                local.get $l4
                local.get $l18
                local.get $l16
                f32.mul
                local.tee $l22
                local.get $l20
                local.get $l15
                local.get $l15
                f32.add
                local.tee $l19
                f32.mul
                local.tee $l20
                f32.sub
                f32.store offset=276
                local.get $l4
                local.get $l23
                local.get $l25
                f32.sub
                f32.store offset=272
                local.get $l4
                local.get $l22
                local.get $l20
                f32.add
                f32.store offset=268
                local.get $l4
                f32.const 0x1p+0 (;=1;)
                local.get $l21
                local.get $l18
                f32.mul
                f32.sub
                local.tee $l18
                local.get $l16
                local.get $l17
                f32.mul
                local.tee $l16
                f32.sub
                f32.store offset=296
                local.get $l4
                local.get $l18
                local.get $l15
                local.get $l19
                f32.mul
                local.tee $l15
                f32.sub
                f32.store offset=280
                local.get $l4
                f32.const 0x1p+0 (;=1;)
                local.get $l16
                f32.sub
                local.get $l15
                f32.sub
                f32.store offset=264
                local.get $l4
                i32.const 128
                i32.add
                local.get $l4
                i32.const 264
                i32.add
                call $f72798
                local.get $l4
                i32.const 128
                i32.add
                local.get $l11
                call $f72775
              end
              f32.const 0x1p+0 (;=1;)
              local.get $l28
              block $B24 (result f32)
                local.get $p1
                if $I25
                  local.get $l4
                  local.get $l24
                  local.get $l4
                  f32.load offset=128
                  f32.mul
                  local.tee $l17
                  f32.store offset=128
                  local.get $l4
                  local.get $l24
                  local.get $l4
                  f32.load offset=132
                  f32.mul
                  local.tee $l21
                  f32.store offset=132
                  local.get $l4
                  local.get $l24
                  local.get $l4
                  f32.load offset=136
                  f32.mul
                  local.tee $l20
                  f32.store offset=136
                  local.get $l4
                  local.get $l24
                  local.get $l4
                  f32.load offset=140
                  f32.mul
                  local.tee $l22
                  f32.store offset=140
                  local.get $l4
                  local.get $l24
                  local.get $l4
                  f32.load offset=144
                  f32.mul
                  local.tee $l19
                  f32.store offset=144
                  local.get $l4
                  local.get $l24
                  local.get $l4
                  f32.load offset=148
                  f32.mul
                  local.tee $l23
                  f32.store offset=148
                  local.get $l4
                  local.get $l24
                  local.get $l4
                  f32.load offset=152
                  f32.mul
                  local.tee $l25
                  f32.store offset=152
                  local.get $l4
                  local.get $l24
                  local.get $l4
                  f32.load offset=156
                  f32.mul
                  local.tee $l26
                  f32.store offset=156
                  local.get $l4
                  local.get $l24
                  local.get $l4
                  f32.load offset=160
                  f32.mul
                  local.tee $l27
                  f32.store offset=160
                  local.get $l24
                  local.get $l4
                  f32.load offset=176
                  f32.mul
                  br $B24
                end
                local.get $l4
                f32.load offset=160
                local.set $l27
                local.get $l4
                f32.load offset=156
                local.set $l26
                local.get $l4
                f32.load offset=152
                local.set $l25
                local.get $l4
                f32.load offset=148
                local.set $l23
                local.get $l4
                f32.load offset=144
                local.set $l19
                local.get $l4
                f32.load offset=140
                local.set $l22
                local.get $l4
                f32.load offset=136
                local.set $l20
                local.get $l4
                f32.load offset=132
                local.set $l21
                local.get $l4
                f32.load offset=128
                local.set $l17
                local.get $l4
                f32.load offset=176
              end
              local.tee $l15
              f32.add
              local.tee $l16
              f32.div
              local.tee $l18
              local.get $l28
              local.get $l38
              f32.mul
              local.get $l15
              local.get $l4
              f32.load offset=172
              f32.mul
              f32.add
              f32.mul
              local.set $l38
              local.get $l18
              local.get $l28
              local.get $l39
              f32.mul
              local.get $l15
              local.get $l4
              f32.load offset=168
              f32.mul
              f32.add
              f32.mul
              local.set $l39
              local.get $l18
              local.get $l28
              local.get $l40
              f32.mul
              local.get $l15
              local.get $l4
              f32.load offset=164
              f32.mul
              f32.add
              f32.mul
              local.set $l40
              local.get $l14
              i32.const 1
              i32.add
              local.set $l14
              local.get $l29
              local.get $l27
              f32.add
              local.set $l29
              local.get $l30
              local.get $l26
              f32.add
              local.set $l30
              local.get $l31
              local.get $l25
              f32.add
              local.set $l31
              local.get $l32
              local.get $l23
              f32.add
              local.set $l32
              local.get $l33
              local.get $l19
              f32.add
              local.set $l33
              local.get $l34
              local.get $l22
              f32.add
              local.set $l34
              local.get $l35
              local.get $l20
              f32.add
              local.set $l35
              local.get $l36
              local.get $l21
              f32.add
              local.set $l36
              local.get $l37
              local.get $l17
              f32.add
              local.set $l37
              local.get $l16
              local.set $l28
            end
            local.get $l12
            i32.const 1
            i32.add
            local.tee $l12
            local.get $l4
            i32.load offset=256
            i32.lt_u
            br_if $L14
          end
          local.get $p2
          i32.eqz
          br_if $B11
          local.get $l14
          i32.eqz
          br_if $B11
          local.get $l16
          local.get $l24
          local.get $l16
          f32.div
          local.tee $l24
          f32.mul
          local.set $l16
          local.get $l29
          local.get $l24
          f32.mul
          local.set $l29
          local.get $l30
          local.get $l24
          f32.mul
          local.set $l30
          local.get $l31
          local.get $l24
          f32.mul
          local.set $l31
          local.get $l32
          local.get $l24
          f32.mul
          local.set $l32
          local.get $l33
          local.get $l24
          f32.mul
          local.set $l33
          local.get $l34
          local.get $l24
          f32.mul
          local.set $l34
          local.get $l35
          local.get $l24
          f32.mul
          local.set $l35
          local.get $l36
          local.get $l24
          f32.mul
          local.set $l36
          local.get $l37
          local.get $l24
          f32.mul
          local.set $l37
        end
        local.get $p3
        local.get $l16
        f32.store offset=48
        local.get $p3
        local.get $l40
        f32.store offset=36
        local.get $p3
        local.get $l31
        f32.store offset=24
        local.get $p3
        local.get $l34
        f32.store offset=12
        local.get $p3
        local.get $l35
        f32.store offset=8
        local.get $p3
        local.get $l36
        f32.store offset=4
        local.get $p3
        local.get $l37
        f32.store
        local.get $p3
        local.get $l38
        f32.store offset=44
        local.get $p3
        local.get $l39
        f32.store offset=40
        local.get $p3
        local.get $l29
        f32.store offset=32
        local.get $p3
        local.get $l30
        f32.store offset=28
        local.get $p3
        local.get $l32
        f32.store offset=20
        local.get $p3
        local.get $l33
        f32.store offset=16
        i32.const 1
        br $B9
      end
      i32.const 4700888
      i32.load
      i32.const 4
      i32.const 3210117
      i32.const 231
      i32.const 3210479
      i32.const 0
      call $f69760
      i32.const 0
    end
    local.set $l12
    block $B26
      local.get $l4
      i32.load offset=260
      local.tee $p0
      i32.const 0
      i32.lt_s
      br_if $B26
      local.get $p0
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if $B26
      local.get $l4
      i32.load offset=252
      local.tee $p0
      local.get $l4
      i32.const 184
      i32.add
      i32.eq
      br_if $B26
      local.get $p0
      i32.eqz
      br_if $B26
      call $f69753
      local.tee $l5
      local.get $p0
      local.get $l5
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $l4
    i32.const 304
    i32.add
    global.set $g0
    local.get $l12)
