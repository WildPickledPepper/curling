  (func $f70153 (type $t8) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (result i32)
    (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32)
    global.get $g0
    i32.const 160
    i32.sub
    local.tee $l4
    global.set $g0
    local.get $l4
    i64.const 0
    i64.store offset=120
    local.get $l4
    i64.const 0
    i64.store offset=128
    local.get $l4
    i64.const 0
    i64.store offset=112
    local.get $l4
    i32.const 0
    i32.store16 offset=108
    local.get $l4
    i32.const -1
    i32.store offset=104
    local.get $l4
    i64.const 0
    i64.store offset=96
    local.get $l4
    i32.const 0
    i32.store offset=144
    local.get $l4
    i64.const 2139095039
    i64.store offset=136
    block $B0
      local.get $p1
      i32.eqz
      br_if $B0
      local.get $p0
      i32.const 108
      i32.add
      local.set $l10
      local.get $p0
      i32.const -64
      i32.sub
      local.set $l16
      local.get $p0
      i32.const 224
      i32.add
      local.set $l11
      local.get $p0
      i32.const 208
      i32.add
      local.set $l12
      local.get $l4
      i32.const 140
      i32.add
      local.set $l13
      i32.const 1
      local.set $l17
      loop $L1
        local.get $p2
        local.get $l14
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l5
        i32.const 5
        i32.shr_u
        local.set $l19
        local.get $l5
        i32.const 1
        i32.shr_u
        i32.const 15
        i32.and
        local.set $l20
        i32.const 0
        local.set $l9
        loop $L2
          local.get $l9
          local.get $l19
          i32.add
          local.set $l15
          block $B3 (result i32)
            local.get $p0
            i32.load offset=12
            if $I4
              local.get $p0
              i32.load offset=16
              local.get $l15
              i32.const 6
              i32.mul
              i32.add
              local.tee $l5
              i32.load16_u offset=4
              local.set $l6
              local.get $l5
              i32.load16_u
              local.set $l8
              local.get $l5
              i32.load16_u offset=2
              br $B3
            end
            local.get $p0
            i32.load offset=16
            local.get $l15
            i32.const 12
            i32.mul
            i32.add
            local.tee $l5
            i32.load offset=8
            local.set $l6
            local.get $l5
            i32.load
            local.set $l8
            local.get $l5
            i32.load offset=4
          end
          local.set $l7
          local.get $p0
          i32.load offset=20
          local.set $l5
          local.get $l4
          local.get $l6
          i32.store offset=92
          local.get $l4
          local.get $l8
          i32.store offset=84
          local.get $l4
          local.get $l7
          i32.store offset=88
          local.get $l5
          local.get $l6
          i32.const 12
          i32.mul
          i32.add
          local.tee $l6
          f32.load
          local.set $l22
          local.get $l5
          local.get $l7
          i32.const 12
          i32.mul
          i32.add
          local.tee $l7
          f32.load
          local.set $l23
          local.get $l5
          local.get $l8
          i32.const 12
          i32.mul
          i32.add
          local.tee $l5
          f32.load
          local.set $l27
          local.get $l6
          f32.load offset=4
          local.set $l28
          local.get $l7
          f32.load offset=4
          local.set $l24
          local.get $l5
          f32.load offset=4
          local.set $l29
          local.get $l6
          f32.load offset=8
          local.set $l30
          local.get $l7
          f32.load offset=8
          local.set $l25
          local.get $l5
          f32.load offset=8
          local.set $l31
          local.get $p0
          f32.load offset=60
          local.set $l32
          local.get $p0
          f32.load offset=192
          local.set $l33
          local.get $p0
          f32.load offset=196
          local.set $l34
          local.get $p0
          f32.load offset=200
          local.set $l35
          local.get $l4
          i32.const 0
          i32.store offset=44
          local.get $l4
          local.get $l31
          local.get $l25
          local.get $l25
          local.get $l31
          f32.gt
          select
          local.tee $l26
          local.get $l30
          local.get $l26
          local.get $l30
          f32.lt
          select
          local.get $l35
          f32.sub
          f32.store offset=40
          local.get $l4
          local.get $l29
          local.get $l24
          local.get $l24
          local.get $l29
          f32.gt
          select
          local.tee $l26
          local.get $l28
          local.get $l26
          local.get $l28
          f32.lt
          select
          local.get $l34
          f32.sub
          f32.store offset=36
          local.get $l4
          local.get $l27
          local.get $l23
          local.get $l23
          local.get $l27
          f32.gt
          select
          local.tee $l26
          local.get $l22
          local.get $l22
          local.get $l26
          f32.gt
          select
          local.get $l33
          f32.sub
          f32.store offset=32
          local.get $l4
          i32.const 0
          i32.store offset=28
          local.get $l4
          local.get $l35
          local.get $l31
          local.get $l25
          local.get $l25
          local.get $l31
          f32.lt
          select
          local.tee $l25
          local.get $l30
          local.get $l25
          local.get $l30
          f32.gt
          select
          f32.add
          f32.store offset=24
          local.get $l4
          local.get $l34
          local.get $l29
          local.get $l24
          local.get $l24
          local.get $l29
          f32.lt
          select
          local.tee $l24
          local.get $l28
          local.get $l24
          local.get $l28
          f32.gt
          select
          f32.add
          f32.store offset=20
          local.get $l4
          local.get $l33
          local.get $l27
          local.get $l23
          local.get $l23
          local.get $l27
          f32.lt
          select
          local.tee $l23
          local.get $l22
          local.get $l22
          local.get $l23
          f32.lt
          select
          f32.add
          f32.store offset=16
          local.get $l4
          local.get $l32
          local.get $l32
          f32.const 0x1p+0 (;=1;)
          f32.max
          f32.const 0x1.0624dep-10 (;=0.001;)
          f32.mul
          f32.add
          f32.store
          local.get $l4
          i32.const -64
          i32.sub
          local.tee $l21
          f32.const 0x1p+0 (;=1;)
          local.get $l11
          f32.load
          local.tee $l22
          local.get $l22
          f32.neg
          local.tee $l24
          local.get $l22
          local.get $l24
          f32.gt
          select
          local.tee $l24
          f32.const 0x1.12e0bep-30 (;=1e-09;)
          local.get $l24
          f32.const 0x1.12e0bep-30 (;=1e-09;)
          f32.gt
          select
          local.tee $l24
          local.get $l24
          f32.neg
          local.get $l22
          f32.const 0x0p+0 (;=0;)
          f32.ge
          select
          f32.div
          local.tee $l24
          local.get $l4
          i32.const 16
          i32.add
          local.tee $l8
          f32.load
          local.get $l12
          f32.load
          local.tee $l23
          f32.sub
          f32.mul
          local.tee $l22
          local.get $l24
          local.get $l4
          i32.const 32
          i32.add
          local.tee $l18
          f32.load
          local.get $l23
          f32.sub
          f32.mul
          local.tee $l24
          local.get $l22
          local.get $l24
          f32.lt
          select
          local.tee $l28
          f32.const 0x1p+0 (;=1;)
          local.get $l11
          f32.load offset=4
          local.tee $l23
          local.get $l23
          f32.neg
          local.tee $l25
          local.get $l23
          local.get $l25
          f32.gt
          select
          local.tee $l25
          f32.const 0x1.12e0bep-30 (;=1e-09;)
          local.get $l25
          f32.const 0x1.12e0bep-30 (;=1e-09;)
          f32.gt
          select
          local.tee $l25
          local.get $l25
          f32.neg
          local.get $l23
          f32.const 0x0p+0 (;=0;)
          f32.ge
          select
          f32.div
          local.tee $l25
          local.get $l8
          f32.load offset=4
          local.get $l12
          f32.load offset=4
          local.tee $l26
          f32.sub
          f32.mul
          local.tee $l23
          local.get $l25
          local.get $l18
          f32.load offset=4
          local.get $l26
          f32.sub
          f32.mul
          local.tee $l25
          local.get $l23
          local.get $l25
          f32.lt
          select
          local.tee $l29
          f32.const 0x1p+0 (;=1;)
          local.get $l11
          f32.load offset=8
          local.tee $l26
          local.get $l26
          f32.neg
          local.tee $l27
          local.get $l26
          local.get $l27
          f32.gt
          select
          local.tee $l27
          f32.const 0x1.12e0bep-30 (;=1e-09;)
          local.get $l27
          f32.const 0x1.12e0bep-30 (;=1e-09;)
          f32.gt
          select
          local.tee $l27
          local.get $l27
          f32.neg
          local.get $l26
          f32.const 0x0p+0 (;=0;)
          f32.ge
          select
          f32.div
          local.tee $l27
          local.get $l8
          f32.load offset=8
          local.get $l12
          f32.load offset=8
          local.tee $l30
          f32.sub
          f32.mul
          local.tee $l26
          local.get $l27
          local.get $l18
          f32.load offset=8
          local.get $l30
          f32.sub
          f32.mul
          local.tee $l27
          local.get $l26
          local.get $l27
          f32.lt
          select
          local.tee $l30
          local.get $l29
          local.get $l30
          f32.gt
          select
          local.tee $l29
          local.get $l28
          local.get $l29
          f32.gt
          select
          local.tee $l28
          f32.const 0x0p+0 (;=0;)
          local.get $l28
          f32.const 0x0p+0 (;=0;)
          f32.gt
          select
          f32.store
          local.get $l4
          i32.const 48
          i32.add
          local.get $l4
          f32.load
          local.tee $l28
          local.get $l26
          local.get $l27
          local.get $l26
          local.get $l27
          f32.gt
          select
          local.tee $l26
          local.get $l23
          local.get $l25
          local.get $l23
          local.get $l25
          f32.gt
          select
          local.tee $l23
          local.get $l23
          local.get $l26
          f32.gt
          select
          local.tee $l23
          local.get $l22
          local.get $l24
          local.get $l22
          local.get $l24
          f32.gt
          select
          local.tee $l22
          local.get $l22
          local.get $l23
          f32.gt
          select
          local.tee $l22
          local.get $l22
          local.get $l28
          f32.gt
          select
          local.tee $l22
          f32.store
          local.get $l22
          local.get $l21
          f32.load
          f32.gt
          if $I5
            local.get $l4
            local.get $p0
            f32.load offset=60
            local.tee $l22
            f32.store offset=136
            local.get $l4
            i64.const 0
            i64.store offset=140 align=4
            local.get $l4
            i32.const 1
            i32.store16 offset=108
            local.get $l4
            local.get $l15
            i32.store offset=104
            block $B6
              local.get $p0
              i32.load8_u offset=177
              if $I7
                local.get $l22
                local.get $p0
                f32.load offset=104
                f32.lt
                i32.eqz
                br_if $B6
                local.get $l16
                local.get $l4
                i64.load offset=96
                i64.store align=4
                local.get $l16
                local.get $l4
                i32.load offset=104
                i32.store offset=8
                local.get $p0
                i32.const 1
                i32.store16 offset=76
                local.get $p0
                local.get $l4
                f32.load offset=112
                f32.store offset=80
                local.get $p0
                local.get $l4
                f32.load offset=116
                f32.store offset=84
                local.get $p0
                local.get $l4
                f32.load offset=120
                f32.store offset=88
                local.get $p0
                local.get $l4
                f32.load offset=124
                f32.store offset=92
                local.get $p0
                local.get $l4
                f32.load offset=128
                f32.store offset=96
                local.get $l4
                f32.load offset=132
                local.set $l23
                local.get $p0
                local.get $l22
                f32.store offset=104
                local.get $p0
                local.get $l23
                f32.store offset=100
                local.get $l10
                local.get $l13
                i32.load offset=16
                i32.store offset=16
                local.get $l10
                local.get $l13
                i64.load offset=8 align=4
                i64.store offset=8 align=4
                local.get $l10
                local.get $l13
                i64.load align=4
                i64.store align=4
                local.get $p3
                local.get $l22
                local.get $p3
                f32.load
                local.tee $l23
                local.get $l22
                local.get $l23
                f32.lt
                select
                f32.store
                local.get $p0
                local.get $l5
                f32.load
                f32.store offset=128
                local.get $p0
                local.get $l5
                f32.load offset=4
                f32.store offset=132
                local.get $p0
                local.get $l5
                f32.load offset=8
                f32.store offset=136
                local.get $p0
                local.get $l7
                f32.load
                f32.store offset=140
                local.get $p0
                local.get $l7
                f32.load offset=4
                f32.store offset=144
                local.get $p0
                local.get $l7
                f32.load offset=8
                f32.store offset=148
                local.get $p0
                local.get $l6
                f32.load
                f32.store offset=152
                local.get $p0
                local.get $l6
                f32.load offset=4
                f32.store offset=156
                local.get $p0
                local.get $l6
                f32.load offset=8
                f32.store offset=160
                local.get $p0
                local.get $l4
                i32.load offset=84
                i32.store offset=164
                local.get $p0
                local.get $l4
                i32.load offset=88
                i32.store offset=168
                local.get $l4
                i32.load offset=92
                local.set $l5
                local.get $p0
                i32.const 1
                i32.store8 offset=176
                local.get $p0
                local.get $l5
                i32.store offset=172
                br $B6
              end
              local.get $l4
              local.get $p3
              f32.load
              f32.store offset=64
              local.get $p0
              i32.load offset=8
              local.tee $l8
              local.get $l4
              i32.const 96
              i32.add
              local.get $l5
              local.get $l7
              local.get $l6
              local.get $l4
              i32.const -64
              i32.sub
              local.get $l4
              i32.const 84
              i32.add
              local.get $l8
              i32.load
              i32.load
              call_indirect $__indirect_function_table (type $t14)
              i32.eqz
              br_if $B0
              local.get $l4
              f32.load offset=64
              local.tee $l22
              local.get $p3
              f32.load
              f32.lt
              i32.eqz
              br_if $B6
              local.get $p3
              local.get $l22
              f32.store
              local.get $p0
              local.get $l22
              f32.store offset=60
            end
            local.get $p0
            i32.load offset=8
            i32.load offset=4
            i32.eqz
            br_if $B0
          end
          local.get $l9
          local.get $l20
          i32.eq
          local.set $l5
          local.get $l9
          i32.const 1
          i32.add
          local.set $l9
          local.get $l5
          i32.eqz
          br_if $L2
        end
        local.get $l14
        i32.const 1
        i32.add
        local.tee $l14
        local.get $p1
        i32.lt_u
        local.set $l17
        local.get $p1
        local.get $l14
        i32.ne
        br_if $L1
      end
    end
    local.get $l4
    i32.const 160
    i32.add
    global.set $g0
    local.get $l17
    i32.const -1
    i32.xor
    i32.const 1
    i32.and)
