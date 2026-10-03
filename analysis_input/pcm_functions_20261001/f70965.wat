  (func $f70965 (type $t262) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 f32) (param $p4 f32) (param $p5 f32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (result i32)
    (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32) (local $l64 f32) (local $l65 f32) (local $l66 f32) (local $l67 f32) (local $l68 f32) (local $l69 f32) (local $l70 f32) (local $l71 f32) (local $l72 f32) (local $l73 f32) (local $l74 f32) (local $l75 f32) (local $l76 f32) (local $l77 f32) (local $l78 f32) (local $l79 f32) (local $l80 f32) (local $l81 i64) (local $l82 i64) (local $l83 i64)
    global.get $g0
    i32.const 432
    i32.sub
    local.tee $l9
    global.set $g0
    local.get $p0
    i32.load offset=16
    local.tee $l15
    i32.const 0
    i32.store16 offset=22
    local.get $p2
    i32.const 4112
    i32.add
    i32.const 0
    i32.store
    local.get $l9
    i32.const 1065353216
    i32.store offset=28
    local.get $l9
    i32.const 1065353216
    i32.store offset=24
    local.get $l9
    i32.const 1065353216
    i32.store offset=20
    local.get $l9
    i32.const 1065353216
    i32.store offset=16
    local.get $l9
    i32.const 0
    i32.store8 offset=15
    local.get $l9
    i32.const 0
    i32.store8 offset=14
    block $B0
      local.get $p2
      i32.const 16
      i32.add
      local.tee $l25
      local.get $p1
      local.get $l9
      i32.const 15
      i32.add
      local.get $l9
      i32.const 14
      i32.add
      local.get $l9
      i32.const 28
      i32.add
      local.get $l9
      i32.const 24
      i32.add
      local.get $l9
      i32.const 20
      i32.add
      local.get $l9
      i32.const 16
      i32.add
      local.get $p0
      i32.load offset=28
      f32.load offset=76
      local.tee $l28
      local.get $p0
      i32.load offset=32
      f32.load offset=76
      local.tee $l29
      local.get $l28
      local.get $l29
      f32.lt
      select
      call $f71234
      local.tee $l24
      i32.eqz
      if $I1
        local.get $p0
        i32.const 0
        i32.store8 offset=140
        local.get $p0
        i32.const 0
        i32.store offset=136
        i32.const 1
        local.set $l16
        br $B0
      end
      local.get $p2
      i32.const 11812
      i32.add
      i64.const 0
      i64.store align=4
      local.get $p2
      i32.const 4128
      i32.add
      local.tee $l23
      local.get $l25
      local.get $p2
      i32.load offset=4112
      call $f71216
      drop
      local.get $l23
      local.get $l25
      local.get $p0
      i32.const 36
      i32.add
      local.tee $l26
      local.get $p0
      i32.const -64
      i32.sub
      local.tee $l13
      i32.const 0
      i32.const 0
      call $f71217
      drop
      i32.const 1
      local.set $l16
      i32.const 1
      i32.const 2
      local.get $p7
      i32.const 1
      i32.eq
      select
      local.set $l22
      local.get $p0
      i32.load offset=96
      local.get $p0
      i32.load offset=92
      i32.or
      i32.const 8
      i32.and
      local.set $l21
      block $B2
        block $B3
          local.get $p2
          i32.const 11816
          i32.add
          i32.load
          local.tee $l17
          i32.eqz
          br_if $B3
          i32.const 7
          i32.const 6
          local.get $l21
          select
          local.set $l19
          i32.const 112
          i32.const 48
          local.get $l21
          select
          local.set $l18
          i32.const 0
          local.set $p7
          loop $L4
            block $B5
              local.get $p2
              local.get $p7
              i32.const 2
              i32.shl
              i32.add
              i32.const 11424
              i32.add
              i32.load
              local.tee $l11
              i32.eqz
              br_if $B5
              local.get $l11
              i32.const 2
              i32.shl
              i32.const 12
              i32.add
              i32.const -16
              i32.and
              local.set $l12
              local.get $l20
              local.get $l11
              local.get $l18
              i32.mul
              i32.add
              i32.const 80
              i32.add
              local.set $l14
              local.get $p2
              local.get $p7
              i32.const 104
              i32.mul
              i32.add
              i32.const 6945
              i32.add
              i32.load8_u
              i32.const 1
              i32.and
              i32.eqz
              if $I6
                local.get $l12
                local.get $l14
                i32.add
                local.get $l11
                local.get $l22
                i32.mul
                local.get $l19
                i32.shl
                i32.add
                local.set $l20
                br $B5
              end
              local.get $l12
              local.get $l14
              i32.add
              local.set $l20
            end
            local.get $p7
            i32.const 1
            i32.add
            local.tee $p7
            local.get $l17
            i32.ne
            br_if $L4
          end
          local.get $l20
          i32.const 15
          i32.add
          i32.const -16
          i32.and
          local.tee $l27
          i32.eqz
          if $I7
            i32.const 0
            local.set $l20
            br $B3
          end
          i32.const 0
          local.get $p6
          local.get $l27
          i32.const 16
          i32.add
          local.get $p6
          i32.load
          i32.load
          call_indirect $__indirect_function_table (type $t0)
          local.tee $p7
          local.get $p7
          i32.const -1
          i32.eq
          select
          local.tee $l20
          br_if $B2
          local.get $p0
          i32.const 0
          i32.store offset=136
          local.get $l15
          i32.const 0
          i32.store16 offset=22
          local.get $l15
          i32.const 0
          i32.store offset=24
          local.get $p0
          i32.const 0
          i32.store8 offset=140
          i32.const 0
          local.set $l16
          br $B0
        end
        i32.const 0
        local.set $l27
      end
      local.get $p0
      i32.const 0
      i32.store8 offset=140
      local.get $p0
      i32.const 0
      i32.store offset=136
      local.get $l15
      local.get $l20
      i32.store offset=24
      local.get $p1
      local.get $l24
      i32.store8 offset=12
      local.get $l15
      local.get $l27
      i32.const 4
      i32.shr_u
      i32.store16 offset=22
      local.get $l20
      i32.eqz
      br_if $B0
      local.get $p0
      i32.load offset=32
      local.set $p7
      local.get $p0
      i32.load offset=28
      local.set $l11
      block $B8
        local.get $l21
        if $I9
          local.get $p0
          i32.load offset=20
          local.set $l12
          local.get $l9
          local.get $l15
          i32.load16_u offset=8
          i32.store16 offset=264
          local.get $l9
          local.get $l11
          i32.store offset=260
          local.get $l9
          local.get $l12
          i32.store offset=256
          local.get $p0
          i32.load offset=24
          local.set $l11
          local.get $l9
          local.get $l15
          i32.load16_u offset=10
          i32.store16 offset=216
          local.get $l9
          local.get $p7
          i32.store offset=212
          local.get $l9
          local.get $l11
          i32.store offset=208
          local.get $l26
          local.set $p1
          local.get $l20
          local.set $p2
          local.get $l9
          i32.const 208
          i32.add
          local.set $l14
          local.get $l22
          local.set $p6
          local.get $l9
          f32.load offset=28
          local.set $l49
          local.get $l9
          f32.load offset=20
          local.set $l47
          local.get $l9
          f32.load offset=24
          local.set $l50
          local.get $l9
          f32.load offset=16
          local.set $l48
          local.get $p0
          f32.load offset=128
          local.set $l35
          local.get $p0
          f32.load offset=132
          local.set $l30
          i32.const 0
          local.set $l16
          i32.const 0
          local.set $l22
          i32.const 0
          local.set $l26
          global.get $g0
          i32.const 480
          i32.sub
          local.tee $l10
          global.set $g0
          local.get $l10
          local.get $l30
          f32.store offset=464
          local.get $l10
          block $B10 (result f32)
            local.get $l9
            i32.const 256
            i32.add
            local.tee $l15
            i32.load16_u offset=8
            local.tee $p0
            i32.const 65535
            i32.eq
            if $I11
              local.get $l15
              i32.load offset=4
              f32.load offset=68
              br $B10
            end
            local.get $l15
            i32.load
            local.tee $l12
            local.get $p0
            local.get $l12
            i32.load
            i32.load offset=124
            call_indirect $__indirect_function_table (type $t13)
          end
          local.tee $l30
          block $B12 (result f32)
            local.get $l14
            i32.load16_u offset=8
            local.tee $p0
            i32.const 65535
            i32.eq
            if $I13
              local.get $l14
              i32.load offset=4
              f32.load offset=68
              br $B12
            end
            local.get $l14
            i32.load
            local.tee $l12
            local.get $p0
            local.get $l12
            i32.load
            i32.load offset=124
            call_indirect $__indirect_function_table (type $t13)
          end
          local.tee $l31
          local.get $l30
          local.get $l31
          f32.gt
          select
          local.get $p3
          f32.div
          f32.store offset=448
          local.get $l10
          local.get $l35
          f32.store offset=432
          local.get $l10
          local.get $p4
          f32.store offset=416
          local.get $l10
          i32.const 384
          i32.add
          local.get $l15
          call $f71171
          local.get $l10
          i32.const 352
          i32.add
          local.get $l14
          call $f71171
          local.get $l10
          local.get $p3
          f32.store offset=336
          local.get $l10
          local.get $p3
          f32.const 0x1.99999ap-1 (;=0.8;)
          f32.mul
          f32.store offset=320
          local.get $p1
          f32.load offset=24
          local.set $p3
          local.get $p1
          i64.load offset=16 align=4
          local.set $l82
          local.get $l10
          i32.const 0
          i32.store offset=316
          local.get $l10
          local.get $p3
          f32.store offset=312
          local.get $l10
          local.get $l82
          i64.store offset=304
          local.get $l13
          f32.load offset=24
          local.set $p3
          local.get $l13
          i64.load offset=16 align=4
          local.set $l82
          local.get $l10
          i32.const 0
          i32.store offset=300
          local.get $l10
          local.get $p3
          f32.store offset=296
          local.get $l10
          local.get $l82
          i64.store offset=288
          local.get $l23
          i32.load offset=7688
          local.set $l18
          local.get $l10
          local.get $l49
          f32.store offset=272
          local.get $l10
          local.get $l50
          f32.store offset=256
          local.get $l10
          local.get $l47
          f32.store offset=240
          local.get $l10
          local.get $l48
          f32.store offset=224
          local.get $p2
          local.set $p1
          local.get $l18
          if $I14
            loop $L15
              block $B16
                local.get $l23
                local.get $l16
                i32.const 2
                i32.shl
                i32.add
                local.tee $l13
                i32.const 7296
                i32.add
                i32.load
                local.tee $p0
                i32.eqz
                br_if $B16
                local.get $l25
                local.get $l23
                local.get $l13
                i32.const 7424
                i32.add
                local.tee $l12
                i32.load
                i32.const 44
                i32.mul
                i32.add
                i32.load16_u
                i32.const 6
                i32.shl
                i32.add
                local.tee $l13
                f32.load
                local.set $p3
                local.get $l13
                f32.load offset=4
                local.set $l30
                local.get $l13
                f32.load offset=8
                local.set $l31
                local.get $l10
                i32.const 0
                i32.store offset=140
                local.get $l10
                local.get $l31
                f32.store offset=136
                local.get $l10
                local.get $l30
                f32.store offset=132
                local.get $l10
                local.get $p3
                f32.store offset=128
                local.get $l10
                local.get $l13
                f32.load offset=60
                f32.store offset=96
                local.get $p1
                i32.const 3
                i32.store8
                local.get $p1
                local.get $p0
                i32.store8 offset=1
                local.get $p1
                local.get $l10
                f32.load offset=272
                f32.store offset=8
                local.get $l10
                f32.load offset=256
                local.set $p4
                local.get $p1
                i32.const 0
                i32.store8 offset=36
                local.get $p1
                local.get $l48
                f32.store offset=28
                local.get $p1
                local.get $l47
                f32.store offset=4
                local.get $p1
                local.get $p4
                f32.store offset=12
                local.get $p1
                local.get $l31
                f32.store offset=24
                local.get $p1
                local.get $l30
                f32.store offset=20
                local.get $p1
                local.get $p3
                f32.store offset=16
                local.get $p1
                i32.const 48
                i32.add
                local.set $p1
                local.get $l12
                i32.load
                local.tee $l13
                i32.const 65535
                i32.eq
                br_if $B16
                loop $L17
                  local.get $l23
                  local.get $l13
                  i32.const 44
                  i32.mul
                  i32.add
                  local.tee $l17
                  i32.load8_u offset=5
                  local.tee $p0
                  if $I18
                    local.get $l25
                    local.get $l17
                    i32.load16_u
                    i32.const 6
                    i32.shl
                    i32.add
                    local.set $l12
                    i32.const 0
                    local.set $l13
                    loop $L19
                      local.get $l10
                      i32.const -64
                      i32.sub
                      local.get $l15
                      local.get $l14
                      local.get $l10
                      i32.const 272
                      i32.add
                      local.get $l10
                      i32.const 256
                      i32.add
                      local.get $l10
                      i32.const 240
                      i32.add
                      local.get $l10
                      i32.const 224
                      i32.add
                      local.get $l10
                      i32.const 304
                      i32.add
                      local.get $l10
                      i32.const 288
                      i32.add
                      local.get $l10
                      i32.const 128
                      i32.add
                      local.get $l10
                      i32.const 336
                      i32.add
                      local.get $l10
                      i32.const 320
                      i32.add
                      local.get $l10
                      i32.const 432
                      i32.add
                      local.get $l10
                      i32.const 448
                      i32.add
                      local.get $l10
                      i32.const 96
                      i32.add
                      local.get $l10
                      i32.const 416
                      i32.add
                      local.get $l12
                      local.get $l13
                      i32.const 6
                      i32.shl
                      i32.add
                      local.get $p1
                      local.get $l10
                      i32.const 464
                      i32.add
                      local.get $p8
                      local.get $l10
                      i32.const 384
                      i32.add
                      local.get $l10
                      i32.const 352
                      i32.add
                      call $f71105
                      local.get $p1
                      i32.const 112
                      i32.add
                      local.set $p1
                      local.get $l13
                      i32.const 1
                      i32.add
                      local.tee $l13
                      local.get $p0
                      i32.ne
                      br_if $L19
                    end
                  end
                  local.get $l17
                  i32.load16_u offset=2
                  local.tee $l13
                  i32.const 65535
                  i32.ne
                  br_if $L17
                end
              end
              local.get $l16
              i32.const 1
              i32.add
              local.tee $l16
              local.get $l18
              i32.ne
              br_if $L15
            end
          end
          local.get $l18
          if $I20
            local.get $l10
            i32.const 112
            i32.add
            local.set $l17
            local.get $l10
            i32.const 144
            i32.add
            local.set $l16
            loop $L21
              local.get $l23
              local.get $l22
              i32.const 2
              i32.shl
              i32.add
              local.tee $l13
              i32.const 7296
              i32.add
              local.tee $p0
              i32.load
              if $I22
                local.get $p2
                local.get $p1
                local.get $p2
                i32.sub
                i32.store16 offset=2
                local.get $l25
                local.get $l23
                local.get $l13
                i32.const 7424
                i32.add
                local.tee $l11
                i32.load
                i32.const 44
                i32.mul
                i32.add
                i32.load16_u
                i32.const 6
                i32.shl
                i32.add
                local.tee $l13
                f32.load offset=44
                local.set $l40
                local.get $l13
                f32.load offset=8
                local.set $l31
                local.get $l13
                f32.load offset=4
                local.set $p3
                local.get $l13
                f32.load
                local.set $l30
                local.get $l13
                i32.load8_u offset=48
                local.set $l13
                local.get $p2
                i32.load8_u offset=1
                local.set $l12
                local.get $p1
                local.get $p0
                i32.load
                i32.store8 offset=1
                local.get $l13
                i32.const 1
                i32.and
                local.tee $l24
                if $I23 (result i32)
                  i32.const 0
                else
                  local.get $p0
                  i32.load
                  local.get $p6
                  i32.mul
                end
                local.set $l13
                local.get $l12
                i32.const 112
                i32.mul
                local.set $l12
                local.get $p1
                i32.const 0
                i32.store8 offset=3
                local.get $p1
                local.get $l13
                i32.store8 offset=2
                local.get $p1
                i32.const 32
                i32.add
                i32.const 0
                local.get $p0
                i32.load
                i32.const 2
                i32.shl
                local.tee $l13
                call $f484
                local.set $l19
                local.get $l10
                i32.const 128
                i32.add
                local.get $l15
                call $f71170
                local.get $l10
                i32.const 96
                i32.add
                local.get $l14
                call $f71170
                f32.const 0x0p+0 (;=0;)
                local.set $p4
                local.get $l13
                i32.const 12
                i32.add
                i32.const -16
                i32.and
                local.set $l21
                f32.const 0x0p+0 (;=0;)
                local.set $l35
                f32.const 0x0p+0 (;=0;)
                local.set $l38
                local.get $l10
                f32.load offset=136
                local.get $l10
                f32.load offset=104
                f32.sub
                local.tee $l33
                local.get $l31
                local.get $l30
                local.get $l10
                f32.load offset=128
                local.get $l10
                f32.load offset=96
                f32.sub
                local.tee $l39
                f32.mul
                local.get $p3
                local.get $l10
                f32.load offset=132
                local.get $l10
                f32.load offset=100
                f32.sub
                local.tee $l41
                f32.mul
                f32.add
                local.get $l31
                local.get $l33
                f32.mul
                f32.add
                local.tee $l33
                f32.mul
                f32.sub
                local.tee $l36
                local.get $p3
                f32.const 0x0p+0 (;=0;)
                local.get $l30
                f32.abs
                f32.const 0x1.6a09e6p-1 (;=0.707107;)
                f32.lt
                local.tee $l13
                select
                local.get $l36
                local.get $l36
                f32.mul
                local.get $l39
                local.get $l30
                local.get $l33
                f32.mul
                f32.sub
                local.tee $l36
                local.get $l36
                f32.mul
                local.get $l41
                local.get $p3
                local.get $l33
                f32.mul
                f32.sub
                local.tee $l33
                local.get $l33
                f32.mul
                f32.add
                f32.add
                f32.const 0x1.4f8b58p-17 (;=1e-05;)
                f32.gt
                local.tee $p0
                select
                local.tee $l39
                local.get $l39
                f32.mul
                local.get $l36
                f32.const 0x0p+0 (;=0;)
                local.get $p3
                f32.neg
                local.get $l13
                select
                local.get $p0
                select
                local.tee $l36
                local.get $l36
                f32.mul
                local.get $l33
                local.get $l31
                f32.neg
                local.get $l30
                local.get $l13
                select
                local.get $p0
                select
                local.tee $l33
                local.get $l33
                f32.mul
                f32.add
                f32.add
                local.tee $l41
                f32.const 0x0p+0 (;=0;)
                f32.gt
                if $I24
                  local.get $l39
                  f32.const 0x1p+0 (;=1;)
                  local.get $l41
                  f32.sqrt
                  f32.div
                  local.tee $p4
                  f32.mul
                  local.set $l38
                  local.get $l33
                  local.get $p4
                  f32.mul
                  local.set $l35
                  local.get $l36
                  local.get $p4
                  f32.mul
                  local.set $p4
                end
                local.get $p2
                local.get $l12
                i32.add
                local.set $p7
                local.get $l19
                local.get $l21
                i32.add
                local.set $p0
                local.get $l10
                local.get $l35
                f32.store offset=196
                local.get $l10
                local.get $p4
                f32.store offset=192
                local.get $l10
                local.get $p3
                local.get $p4
                f32.mul
                local.get $l30
                local.get $l35
                f32.mul
                f32.sub
                f32.store offset=212
                local.get $l10
                local.get $l38
                f32.store offset=200
                local.get $l10
                local.get $l30
                local.get $l38
                f32.mul
                local.get $l31
                local.get $p4
                f32.mul
                f32.sub
                f32.store offset=208
                local.get $l10
                local.get $l31
                local.get $l35
                f32.mul
                local.get $p3
                local.get $l38
                f32.mul
                f32.sub
                f32.store offset=204
                block $B25
                  local.get $l24
                  br_if $B25
                  local.get $p1
                  local.get $l48
                  f32.store offset=20
                  local.get $p1
                  local.get $l47
                  f32.store offset=16
                  local.get $p1
                  local.get $l50
                  f32.store offset=12
                  local.get $p1
                  local.get $l49
                  f32.store offset=8
                  local.get $p1
                  local.get $l40
                  f32.store offset=4
                  local.get $p1
                  i32.const 12
                  i32.store8
                  i32.const 0
                  local.set $l13
                  i32.const 1
                  local.set $l26
                  local.get $l11
                  i32.load
                  local.tee $p1
                  i32.const 65535
                  i32.eq
                  br_if $B25
                  loop $L26
                    local.get $l23
                    local.get $p1
                    i32.const 44
                    i32.mul
                    i32.add
                    local.tee $l21
                    i32.load8_u offset=5
                    local.tee $l24
                    if $I27
                      local.get $l25
                      local.get $l21
                      i32.load16_u
                      i32.const 6
                      i32.shl
                      i32.add
                      local.set $l19
                      i32.const 0
                      local.set $p2
                      loop $L28
                        local.get $p6
                        if $I29
                          local.get $l10
                          f32.load offset=360
                          local.get $l19
                          local.get $p2
                          i32.const 6
                          i32.shl
                          i32.add
                          local.tee $p1
                          f32.load offset=20
                          local.tee $p3
                          local.get $l10
                          f32.load offset=292
                          f32.sub
                          local.tee $l38
                          local.get $l10
                          f32.load offset=368
                          local.tee $l30
                          f32.mul
                          local.get $p1
                          f32.load offset=16
                          local.tee $l31
                          local.get $l10
                          f32.load offset=288
                          f32.sub
                          local.tee $l33
                          local.get $l10
                          f32.load offset=372
                          local.tee $p4
                          f32.mul
                          f32.sub
                          f32.add
                          local.set $l57
                          local.get $l10
                          f32.load offset=356
                          local.get $l33
                          local.get $l10
                          f32.load offset=376
                          local.tee $l35
                          f32.mul
                          local.get $p1
                          f32.load offset=24
                          local.tee $l40
                          local.get $l10
                          f32.load offset=296
                          f32.sub
                          local.tee $l36
                          local.get $l30
                          f32.mul
                          f32.sub
                          f32.add
                          local.set $l58
                          local.get $l10
                          f32.load offset=352
                          local.get $l36
                          local.get $p4
                          f32.mul
                          local.get $l38
                          local.get $l35
                          f32.mul
                          f32.sub
                          f32.add
                          local.set $l59
                          local.get $l10
                          f32.load offset=392
                          local.get $p3
                          local.get $l10
                          f32.load offset=308
                          f32.sub
                          local.tee $l39
                          local.get $l10
                          f32.load offset=400
                          local.tee $p3
                          f32.mul
                          local.get $l31
                          local.get $l10
                          f32.load offset=304
                          f32.sub
                          local.tee $l41
                          local.get $l10
                          f32.load offset=404
                          local.tee $l30
                          f32.mul
                          f32.sub
                          f32.add
                          local.set $l60
                          local.get $l10
                          f32.load offset=388
                          local.get $l41
                          local.get $l10
                          f32.load offset=408
                          local.tee $l31
                          f32.mul
                          local.get $l40
                          local.get $l10
                          f32.load offset=312
                          f32.sub
                          local.tee $l40
                          local.get $p3
                          f32.mul
                          f32.sub
                          f32.add
                          local.set $l34
                          local.get $l10
                          f32.load offset=384
                          local.get $l40
                          local.get $l30
                          f32.mul
                          local.get $l39
                          local.get $l31
                          f32.mul
                          f32.sub
                          f32.add
                          local.set $l28
                          local.get $p1
                          f32.load offset=32
                          local.set $l29
                          local.get $p1
                          f32.load offset=40
                          local.set $l43
                          local.get $p1
                          f32.load offset=36
                          local.set $l44
                          i32.const 0
                          local.set $l12
                          loop $L30
                            local.get $p0
                            local.set $p1
                            local.get $l10
                            i32.const 192
                            i32.add
                            local.get $l13
                            i32.const 12
                            i32.mul
                            i32.add
                            local.tee $p0
                            f32.load
                            local.set $p3
                            local.get $p0
                            f32.load offset=4
                            local.set $l30
                            local.get $p0
                            f32.load offset=8
                            local.set $l31
                            local.get $l10
                            i32.const 0
                            i32.store offset=188
                            local.get $l10
                            local.get $l31
                            f32.store offset=184
                            local.get $l10
                            local.get $l30
                            f32.store offset=180
                            local.get $l10
                            local.get $p3
                            f32.store offset=176
                            local.get $l10
                            i32.const 0
                            i32.store offset=172
                            local.get $l10
                            local.get $l41
                            local.get $l30
                            f32.mul
                            local.get $l39
                            local.get $p3
                            f32.mul
                            f32.sub
                            f32.store offset=168
                            local.get $l10
                            local.get $l40
                            local.get $p3
                            f32.mul
                            local.get $l41
                            local.get $l31
                            f32.mul
                            f32.sub
                            f32.store offset=164
                            local.get $l10
                            local.get $l39
                            local.get $l31
                            f32.mul
                            local.get $l40
                            local.get $l30
                            f32.mul
                            f32.sub
                            f32.store offset=160
                            local.get $l10
                            i32.const -64
                            i32.sub
                            local.get $l10
                            i32.const 176
                            i32.add
                            local.get $l10
                            i32.const 160
                            i32.add
                            local.get $l15
                            call $f71172
                            local.get $l10
                            i32.const 0
                            i32.store offset=28
                            local.get $l10
                            local.get $l10
                            f32.load offset=184
                            f32.neg
                            f32.store offset=24
                            local.get $l10
                            local.get $l10
                            f32.load offset=180
                            f32.neg
                            f32.store offset=20
                            local.get $l10
                            local.get $l10
                            f32.load offset=176
                            f32.neg
                            f32.store offset=16
                            local.get $l10
                            i32.const 0
                            i32.store offset=12
                            local.get $l10
                            local.get $l33
                            local.get $l30
                            f32.mul
                            local.get $l38
                            local.get $p3
                            f32.mul
                            f32.sub
                            f32.neg
                            f32.store offset=8
                            local.get $l10
                            local.get $l36
                            local.get $p3
                            f32.mul
                            local.get $l33
                            local.get $l31
                            f32.mul
                            f32.sub
                            f32.neg
                            f32.store offset=4
                            local.get $l10
                            local.get $l38
                            local.get $l31
                            f32.mul
                            local.get $l36
                            local.get $l30
                            f32.mul
                            f32.sub
                            f32.neg
                            f32.store
                            local.get $l10
                            i32.const 32
                            i32.add
                            local.get $l10
                            i32.const 16
                            i32.add
                            local.get $l10
                            local.get $l14
                            call $f71172
                            local.get $l10
                            i32.const 16
                            i32.add
                            local.get $l15
                            local.get $l10
                            i32.const -64
                            i32.sub
                            local.get $l10
                            i32.const 128
                            i32.add
                            local.get $l10
                            i32.const 272
                            i32.add
                            local.get $l10
                            i32.const 240
                            i32.add
                            local.get $l14
                            local.get $l10
                            i32.const 32
                            i32.add
                            local.get $l10
                            i32.const 96
                            i32.add
                            local.get $l10
                            i32.const 256
                            i32.add
                            local.get $l10
                            i32.const 224
                            i32.add
                            local.get $p8
                            call $f71173
                            local.get $l29
                            local.get $l10
                            f32.load offset=176
                            local.tee $l31
                            f32.mul
                            local.get $l44
                            local.get $l10
                            f32.load offset=180
                            local.tee $p4
                            f32.mul
                            f32.add
                            local.get $l43
                            local.get $l10
                            f32.load offset=184
                            local.tee $l35
                            f32.mul
                            f32.add
                            local.set $p3
                            block $B31
                              local.get $l15
                              i32.load16_u offset=8
                              i32.const 65535
                              i32.eq
                              if $I32
                                local.get $p3
                                local.get $l28
                                local.get $l31
                                f32.mul
                                local.get $l34
                                local.get $p4
                                f32.mul
                                f32.add
                                local.get $l60
                                local.get $l35
                                f32.mul
                                f32.add
                                f32.add
                                local.set $p3
                                br $B31
                              end
                              local.get $l14
                              i32.load16_u offset=8
                              i32.const 65535
                              i32.ne
                              br_if $B31
                              local.get $p3
                              local.get $l59
                              local.get $l31
                              f32.mul
                              local.get $l58
                              local.get $p4
                              f32.mul
                              f32.add
                              local.get $l57
                              local.get $l35
                              f32.mul
                              f32.add
                              f32.sub
                              local.set $p3
                            end
                            i32.const 1
                            local.get $l13
                            i32.sub
                            local.set $l13
                            local.get $p1
                            i32.const 128
                            i32.add
                            local.set $p0
                            local.get $l10
                            f32.load offset=16
                            local.set $l30
                            local.get $l10
                            i64.load offset=80
                            local.set $l82
                            local.get $p1
                            local.get $l10
                            f32.load offset=88
                            f32.store offset=24
                            local.get $p1
                            local.get $l82
                            i64.store offset=16
                            local.get $p1
                            f32.const 0x1p+0 (;=1;)
                            local.get $l30
                            f32.div
                            f32.const 0x0p+0 (;=0;)
                            local.get $l30
                            f32.const 0x0p+0 (;=0;)
                            f32.gt
                            select
                            f32.store offset=28
                            local.get $l10
                            f32.load offset=48
                            local.set $l30
                            local.get $l10
                            f32.load offset=52
                            local.set $l45
                            local.get $l10
                            f32.load offset=56
                            local.set $p5
                            local.get $p1
                            i32.const 0
                            i32.store offset=44
                            local.get $p1
                            local.get $p3
                            f32.store offset=48
                            local.get $p1
                            i32.const 0
                            i32.store offset=12
                            local.get $p1
                            local.get $l35
                            f32.store offset=8
                            local.get $p1
                            local.get $p4
                            f32.store offset=4
                            local.get $p1
                            local.get $l31
                            f32.store
                            local.get $p1
                            local.get $p5
                            f32.neg
                            f32.store offset=40
                            local.get $p1
                            local.get $l45
                            f32.neg
                            f32.store offset=36
                            local.get $p1
                            local.get $l30
                            f32.neg
                            f32.store offset=32
                            local.get $p1
                            local.get $l10
                            i64.load offset=128
                            i64.store offset=64
                            local.get $p1
                            local.get $l10
                            i64.load offset=136
                            i64.store offset=72
                            local.get $p1
                            local.get $l16
                            i64.load
                            i64.store offset=80
                            local.get $p1
                            local.get $l16
                            i64.load offset=8
                            i64.store offset=88
                            local.get $p1
                            local.get $l10
                            i64.load offset=96
                            i64.store offset=96
                            local.get $p1
                            local.get $l10
                            i64.load offset=104
                            i64.store offset=104
                            local.get $p1
                            local.get $l17
                            i64.load
                            i64.store offset=112
                            local.get $p1
                            local.get $l17
                            i64.load offset=8
                            i64.store offset=120
                            local.get $l12
                            i32.const 1
                            i32.add
                            local.tee $l12
                            local.get $p6
                            i32.ne
                            br_if $L30
                          end
                        end
                        local.get $p2
                        i32.const 1
                        i32.add
                        local.tee $p2
                        local.get $l24
                        i32.ne
                        br_if $L28
                      end
                    end
                    local.get $l21
                    i32.load16_u offset=2
                    local.tee $p1
                    i32.const 65535
                    i32.ne
                    br_if $L26
                  end
                end
                local.get $p7
                i32.const 48
                i32.add
                local.set $p2
                local.get $p0
                local.set $p1
              end
              local.get $l22
              i32.const 1
              i32.add
              local.tee $l22
              local.get $l18
              i32.ne
              br_if $L21
            end
          end
          local.get $l10
          i32.const 480
          i32.add
          global.set $g0
          local.get $l26
          local.set $l17
          br $B8
        end
        local.get $p0
        i32.load8_u offset=126
        local.set $l19
        local.get $p0
        i32.load offset=112
        local.set $l15
        local.get $p0
        i32.load offset=96
        local.set $l12
        local.get $p0
        f32.load offset=128
        local.set $l28
        local.get $l9
        f32.load offset=24
        local.set $l32
        local.get $l9
        f32.load offset=28
        local.set $l37
        local.get $l9
        f32.load offset=16
        local.set $l29
        local.get $l9
        f32.load offset=20
        local.set $l34
        local.get $l9
        local.get $p0
        f32.load offset=132
        f32.store offset=416
        i32.const 0
        local.set $l17
        local.get $l9
        i32.const 0
        i32.store offset=412
        local.get $l9
        local.get $p5
        f32.store offset=408
        local.get $l9
        local.get $p5
        f32.store offset=404
        local.get $l9
        local.get $p5
        f32.store offset=400
        local.get $l9
        local.get $l28
        f32.store offset=384
        local.get $p0
        i64.load offset=52 align=4
        local.set $l81
        local.get $p0
        f32.load offset=60
        local.set $l28
        local.get $l9
        i32.const 0
        i32.store offset=380
        local.get $l9
        local.get $l28
        f32.store offset=376
        local.get $l9
        local.get $l81
        i64.store offset=368
        local.get $p0
        i64.load offset=80
        local.set $l81
        local.get $p0
        f32.load offset=88
        local.set $l28
        local.get $l9
        i32.const 0
        i32.store offset=364
        local.get $l9
        local.get $l28
        f32.store offset=360
        local.get $l9
        local.get $l81
        i64.store offset=352
        local.get $p7
        f32.load offset=8
        local.set $l61
        local.get $p7
        f32.load offset=4
        local.set $l62
        local.get $p7
        f32.load
        local.set $l63
        local.get $l11
        f32.load offset=8
        local.set $l64
        local.get $l11
        f32.load offset=4
        local.set $l65
        local.get $l11
        f32.load
        local.set $l66
        local.get $p2
        i32.load offset=11816
        local.set $p1
        local.get $l11
        f32.load offset=24
        local.set $l28
        local.get $l11
        i64.load offset=16
        local.set $l81
        local.get $l9
        i32.const 0
        i32.store offset=348
        local.get $l9
        local.get $l28
        f32.store offset=344
        local.get $l9
        local.get $l81
        i64.store offset=336
        local.get $p7
        f32.load offset=24
        local.set $l28
        local.get $p7
        i64.load offset=16
        local.set $l81
        local.get $l9
        i32.const 0
        i32.store offset=332
        local.get $l9
        local.get $l28
        f32.store offset=328
        local.get $l9
        local.get $l81
        i64.store offset=320
        local.get $p7
        f32.load offset=12
        local.set $l42
        local.get $l11
        f32.load offset=12
        local.set $l46
        local.get $l9
        local.get $l11
        f32.load offset=68
        local.tee $l28
        local.get $p7
        f32.load offset=68
        local.tee $p5
        local.get $p5
        local.get $l28
        f32.lt
        select
        f32.store offset=304
        local.get $l11
        f32.load offset=40
        local.set $l28
        local.get $l11
        i64.load offset=44 align=4
        local.set $l81
        local.get $l11
        i64.load offset=56
        local.set $l83
        local.get $l11
        i32.const -64
        i32.sub
        f32.load
        local.set $p5
        local.get $l11
        i64.load offset=32
        local.set $l82
        local.get $l9
        local.get $l11
        f32.load offset=52
        f32.store offset=280
        local.get $l9
        i32.const 0
        i32.store offset=284
        local.get $l9
        i32.const 0
        i32.store offset=300
        local.get $l9
        local.get $p5
        f32.store offset=296
        local.get $l9
        i32.const 0
        i32.store offset=268
        local.get $l9
        local.get $l82
        i64.store offset=256
        local.get $l9
        local.get $l83
        i64.store offset=288
        local.get $l9
        local.get $l81
        i64.store offset=272
        local.get $l9
        local.get $l28
        f32.store offset=264
        local.get $p7
        f32.load offset=40
        local.set $l28
        local.get $p7
        i64.load offset=44 align=4
        local.set $l81
        local.get $p7
        i64.load offset=56
        local.set $l83
        local.get $p7
        i32.const -64
        i32.sub
        f32.load
        local.set $p5
        local.get $p7
        i64.load offset=32
        local.set $l82
        local.get $l9
        local.get $p7
        f32.load offset=52
        f32.store offset=232
        local.get $l9
        i32.const 0
        i32.store offset=236
        local.get $l9
        i32.const 0
        i32.store offset=252
        local.get $l9
        local.get $p5
        f32.store offset=248
        local.get $l9
        i32.const 0
        i32.store offset=220
        local.get $l9
        local.get $l82
        i64.store offset=208
        local.get $l9
        local.get $l83
        i64.store offset=240
        local.get $l9
        local.get $l81
        i64.store offset=224
        local.get $l9
        local.get $l28
        f32.store offset=216
        local.get $l9
        local.get $p3
        f32.store offset=192
        local.get $l9
        local.get $p4
        f32.store offset=176
        local.get $l9
        local.get $p3
        f32.const 0x1.99999ap-1 (;=0.8;)
        f32.mul
        f32.store offset=160
        local.get $l9
        local.get $l34
        f32.store offset=144
        local.get $l9
        local.get $l29
        f32.store offset=128
        block $B33
          local.get $p1
          i32.eqz
          if $I34
            local.get $l20
            local.set $l11
            br $B33
          end
          i32.const 11
          i32.const 10
          local.get $l12
          i32.const 2
          i32.eq
          local.tee $p7
          select
          local.set $l24
          i32.const 5
          i32.const 1
          local.get $p7
          select
          local.set $l16
          local.get $l37
          local.get $l46
          f32.mul
          local.set $l51
          local.get $l42
          local.get $l32
          f32.neg
          f32.mul
          local.tee $l67
          f32.neg
          local.set $l68
          local.get $p2
          i32.const 4128
          i32.add
          local.set $l18
          local.get $l20
          local.set $l11
          loop $L35
            block $B36
              local.get $p2
              local.get $l17
              i32.const 2
              i32.shl
              local.tee $p7
              i32.add
              i32.const 11424
              i32.add
              i32.load
              local.tee $l12
              i32.eqz
              br_if $B36
              local.get $p2
              local.get $l18
              local.get $p7
              local.get $l18
              i32.add
              i32.const 7424
              i32.add
              local.tee $l14
              i32.load
              i32.const 44
              i32.mul
              i32.add
              i32.load16_u
              i32.const 6
              i32.shl
              i32.add
              local.tee $p7
              f32.load offset=24
              local.set $l28
              local.get $p7
              f32.load offset=16
              local.set $l29
              local.get $l9
              local.get $p7
              f32.load offset=20
              local.tee $p3
              f32.store offset=116
              local.get $l9
              local.get $l29
              f32.store offset=112
              local.get $l9
              i32.const 0
              i32.store offset=124
              local.get $l9
              local.get $l28
              f32.store offset=120
              local.get $l9
              local.get $l9
              i64.load offset=120
              i64.store offset=104
              local.get $l9
              local.get $l9
              i64.load offset=112
              i64.store offset=96
              local.get $l9
              local.get $p7
              f32.load offset=76
              f32.store offset=80
              local.get $l9
              local.get $l66
              local.get $l29
              f32.mul
              local.get $l63
              local.get $l29
              f32.mul
              f32.sub
              local.get $l65
              local.get $p3
              f32.mul
              local.get $l62
              local.get $p3
              f32.mul
              f32.sub
              f32.add
              local.get $l64
              local.get $l28
              f32.mul
              local.get $l61
              local.get $l28
              f32.mul
              f32.sub
              f32.add
              f32.store offset=64
              local.get $l9
              local.get $l51
              local.get $l29
              local.get $l29
              f32.mul
              local.get $p3
              local.get $p3
              f32.mul
              f32.add
              local.get $l28
              local.get $l28
              f32.mul
              f32.add
              local.tee $l28
              f32.mul
              f32.store offset=48
              local.get $l9
              local.get $l67
              local.get $l28
              f32.mul
              f32.store offset=32
              local.get $l11
              local.get $l68
              f32.store offset=12
              local.get $l11
              local.get $l51
              f32.store offset=8
              local.get $l11
              local.get $l16
              i32.store8
              local.get $l11
              local.get $l12
              i32.store8 offset=1
              local.get $l11
              local.get $l9
              f32.load offset=144
              f32.store offset=4
              local.get $l11
              local.get $l9
              f32.load offset=128
              f32.store offset=28
              local.get $l9
              i64.load offset=112
              local.set $l81
              local.get $l9
              f32.load offset=120
              local.set $l28
              local.get $l11
              local.get $l19
              i32.store8 offset=36
              local.get $l11
              local.get $l28
              f32.store offset=24
              local.get $l11
              local.get $l81
              i64.store offset=16 align=4
              local.get $l11
              local.get $l15
              i32.store offset=32
              local.get $l11
              i32.const 48
              i32.add
              local.set $l11
              local.get $l14
              i32.load
              local.tee $p7
              i32.const 65535
              i32.eq
              br_if $B36
              loop $L37
                local.get $p2
                local.get $p7
                i32.const 44
                i32.mul
                i32.add
                local.tee $p0
                i32.const 4133
                i32.add
                i32.load8_u
                local.tee $l12
                if $I38
                  local.get $p2
                  local.get $p0
                  i32.const 4128
                  i32.add
                  i32.load16_u
                  i32.const 6
                  i32.shl
                  i32.add
                  i32.const 16
                  i32.add
                  local.set $l14
                  i32.const 0
                  local.set $p7
                  loop $L39
                    local.get $l9
                    i32.const 256
                    i32.add
                    local.get $l9
                    i32.const 208
                    i32.add
                    local.get $l9
                    i32.const 48
                    i32.add
                    local.get $l9
                    i32.const 32
                    i32.add
                    local.get $l9
                    i32.const 144
                    i32.add
                    local.get $l9
                    i32.const 128
                    i32.add
                    local.get $l9
                    i32.const 368
                    i32.add
                    local.get $l9
                    i32.const 352
                    i32.add
                    local.get $l9
                    i32.const 112
                    i32.add
                    local.get $l9
                    i32.const -64
                    i32.sub
                    local.get $l9
                    i32.const 96
                    i32.add
                    local.get $l9
                    i32.const 336
                    i32.add
                    local.get $l9
                    i32.const 320
                    i32.add
                    local.get $l9
                    i32.const 192
                    i32.add
                    local.get $l9
                    i32.const 160
                    i32.add
                    local.get $l9
                    i32.const 384
                    i32.add
                    local.get $l9
                    i32.const 304
                    i32.add
                    local.get $l9
                    i32.const 80
                    i32.add
                    local.get $l9
                    i32.const 176
                    i32.add
                    local.get $l14
                    local.get $p7
                    i32.const 6
                    i32.shl
                    i32.add
                    local.get $l11
                    local.get $l9
                    i32.const 416
                    i32.add
                    local.get $l9
                    i32.const 400
                    i32.add
                    call $f71104
                    local.get $l11
                    i32.const 48
                    i32.add
                    local.set $l11
                    local.get $p7
                    i32.const 1
                    i32.add
                    local.tee $p7
                    local.get $l12
                    i32.ne
                    br_if $L39
                  end
                end
                local.get $p0
                i32.const 4130
                i32.add
                i32.load16_u
                local.tee $p7
                i32.const 65535
                i32.ne
                br_if $L37
              end
            end
            local.get $l17
            i32.const 1
            i32.add
            local.tee $l17
            local.get $p1
            i32.ne
            br_if $L35
          end
          local.get $l64
          local.get $l61
          f32.sub
          local.set $l69
          local.get $l65
          local.get $l62
          f32.sub
          local.set $l70
          local.get $l66
          local.get $l63
          f32.sub
          local.set $l71
          local.get $l22
          i32.const 2
          i32.shl
          local.set $l21
          local.get $p2
          i32.const 4128
          i32.add
          local.set $l16
          local.get $l20
          local.set $l19
          i32.const 0
          local.set $l17
          i32.const 0
          local.set $l15
          loop $L40
            local.get $p2
            local.get $l15
            i32.const 2
            i32.shl
            local.tee $l12
            i32.add
            i32.const 11424
            i32.add
            local.tee $p7
            i32.load
            local.tee $l14
            if $I41
              local.get $l16
              local.get $l12
              local.get $l16
              i32.add
              i32.const 7424
              i32.add
              local.tee $l12
              i32.load
              i32.const 44
              i32.mul
              i32.add
              i32.load16_u
              local.set $p0
              local.get $l19
              local.get $l11
              local.get $l19
              i32.sub
              i32.store16 offset=2
              local.get $p2
              local.get $p0
              i32.const 6
              i32.shl
              i32.add
              local.tee $p0
              f32.load offset=60
              local.set $l28
              local.get $p0
              i32.const -64
              i32.sub
              i32.load8_u
              local.set $p0
              local.get $l19
              i32.load8_u offset=1
              local.set $l18
              local.get $l11
              local.get $p7
              i32.load
              i32.store8 offset=1
              local.get $l18
              i32.const 48
              i32.mul
              local.get $l19
              i32.add
              i32.const 48
              i32.add
              local.set $l19
              local.get $l11
              local.get $p0
              i32.const 1
              i32.and
              local.tee $p0
              if $I42 (result i32)
                i32.const 0
              else
                local.get $p7
                i32.load
                local.get $l22
                i32.mul
              end
              i32.store8 offset=2
              local.get $p7
              i32.load
              local.set $p7
              local.get $l11
              i32.const 32
              i32.add
              i32.const 0
              local.get $l14
              local.get $l21
              i32.mul
              call $f484
              local.get $p7
              i32.const 2
              i32.shl
              i32.const 12
              i32.add
              i32.const -16
              i32.and
              i32.add
              local.set $p7
              block $B43
                local.get $p0
                br_if $B43
                local.get $p2
                local.get $p2
                local.get $l12
                i32.load
                i32.const 44
                i32.mul
                i32.add
                i32.const 4128
                i32.add
                i32.load16_u
                i32.const 6
                i32.shl
                i32.add
                local.tee $l14
                f32.load offset=16
                local.set $l29
                local.get $l14
                f32.load offset=24
                local.set $l32
                local.get $l14
                f32.load offset=20
                local.set $p3
                local.get $l11
                local.get $l68
                f32.store offset=12
                local.get $l11
                local.get $l51
                f32.store offset=8
                local.get $l11
                local.get $l28
                f32.store offset=4
                local.get $l11
                local.get $l9
                f32.load offset=144
                f32.store offset=16
                local.get $l9
                f32.load offset=128
                local.set $l28
                local.get $l11
                local.get $l24
                i32.store8
                local.get $l11
                local.get $l28
                f32.store offset=20
                local.get $l12
                i32.load
                local.tee $l11
                i32.const 65535
                i32.eq
                br_if $B43
                local.get $p3
                local.get $l71
                local.get $l29
                local.get $l71
                local.get $l29
                f32.mul
                local.get $l70
                local.get $p3
                f32.mul
                f32.add
                local.get $l69
                local.get $l32
                f32.mul
                f32.add
                local.tee $l28
                f32.mul
                f32.sub
                local.tee $p5
                f32.const 0x0p+0 (;=0;)
                local.get $p3
                f32.neg
                local.get $l29
                f32.abs
                f32.const 0x1.6a09e6p-1 (;=0.707107;)
                f32.lt
                local.tee $l12
                select
                local.get $l69
                local.get $l32
                local.get $l28
                f32.mul
                f32.sub
                local.tee $p4
                local.get $p4
                f32.mul
                local.get $p5
                local.get $p5
                f32.mul
                local.get $l70
                local.get $p3
                local.get $l28
                f32.mul
                f32.sub
                local.tee $l28
                local.get $l28
                f32.mul
                f32.add
                f32.add
                f32.const 0x1.4f8b58p-17 (;=1e-05;)
                f32.gt
                local.tee $l14
                select
                local.tee $p5
                f32.const 0x1p+0 (;=1;)
                local.get $p4
                local.get $p3
                f32.const 0x0p+0 (;=0;)
                local.get $l12
                select
                local.get $l14
                select
                local.tee $l34
                local.get $l34
                f32.mul
                local.get $p5
                local.get $p5
                f32.mul
                local.get $l28
                local.get $l32
                f32.neg
                local.get $l29
                local.get $l12
                select
                local.get $l14
                select
                local.tee $l28
                local.get $l28
                f32.mul
                f32.add
                f32.add
                f32.sqrt
                f32.div
                local.tee $l37
                f32.mul
                local.tee $p5
                f32.mul
                local.get $l29
                local.get $l28
                local.get $l37
                f32.mul
                local.tee $p4
                f32.mul
                f32.sub
                local.set $l28
                local.get $l29
                local.get $l34
                local.get $l37
                f32.mul
                local.tee $l34
                f32.mul
                local.get $l32
                local.get $p5
                f32.mul
                f32.sub
                local.set $l29
                local.get $l32
                local.get $p4
                f32.mul
                local.get $p3
                local.get $l34
                f32.mul
                f32.sub
                local.set $p3
                loop $L44
                  local.get $p2
                  local.get $l11
                  i32.const 44
                  i32.mul
                  i32.add
                  local.tee $l18
                  i32.const 4133
                  i32.add
                  i32.load8_u
                  local.tee $l14
                  if $I45
                    local.get $p2
                    local.get $l18
                    i32.const 4128
                    i32.add
                    i32.load16_u
                    i32.const 6
                    i32.shl
                    i32.add
                    i32.const 16
                    i32.add
                    local.set $p0
                    i32.const 0
                    local.set $l12
                    local.get $l28
                    local.set $l43
                    local.get $l29
                    local.set $l44
                    local.get $p3
                    local.set $l45
                    loop $L46
                      f32.const 0x0p+0 (;=0;)
                      local.get $p0
                      local.get $l12
                      i32.const 6
                      i32.shl
                      i32.add
                      local.tee $l11
                      f32.load offset=16
                      local.tee $l29
                      local.get $l9
                      f32.load offset=352
                      f32.sub
                      local.tee $l28
                      local.get $l9
                      f32.load offset=400
                      local.tee $p3
                      local.get $l28
                      local.get $l28
                      f32.neg
                      local.tee $l32
                      local.get $l28
                      local.get $l32
                      f32.gt
                      select
                      f32.gt
                      select
                      local.set $l72
                      f32.const 0x0p+0 (;=0;)
                      local.get $l29
                      local.get $l9
                      f32.load offset=368
                      f32.sub
                      local.tee $l28
                      local.get $p3
                      local.get $l28
                      local.get $l28
                      f32.neg
                      local.tee $l29
                      local.get $l28
                      local.get $l29
                      f32.gt
                      select
                      f32.gt
                      select
                      local.set $l73
                      f32.const 0x0p+0 (;=0;)
                      local.get $l11
                      f32.load offset=24
                      local.tee $l29
                      local.get $l9
                      f32.load offset=360
                      f32.sub
                      local.tee $l28
                      local.get $l9
                      f32.load offset=408
                      local.tee $p3
                      local.get $l28
                      local.get $l28
                      f32.neg
                      local.tee $l32
                      local.get $l28
                      local.get $l32
                      f32.gt
                      select
                      f32.gt
                      select
                      local.set $l74
                      f32.const 0x0p+0 (;=0;)
                      local.get $l11
                      f32.load offset=20
                      local.tee $l32
                      local.get $l9
                      f32.load offset=356
                      f32.sub
                      local.tee $l28
                      local.get $l9
                      f32.load offset=404
                      local.tee $l37
                      local.get $l28
                      local.get $l28
                      f32.neg
                      local.tee $l42
                      local.get $l28
                      local.get $l42
                      f32.gt
                      select
                      f32.gt
                      select
                      local.set $l75
                      f32.const 0x0p+0 (;=0;)
                      local.get $l29
                      local.get $l9
                      f32.load offset=376
                      f32.sub
                      local.tee $l28
                      local.get $p3
                      local.get $l28
                      local.get $l28
                      f32.neg
                      local.tee $l29
                      local.get $l28
                      local.get $l29
                      f32.gt
                      select
                      f32.gt
                      select
                      local.set $l76
                      f32.const 0x0p+0 (;=0;)
                      local.get $l32
                      local.get $l9
                      f32.load offset=372
                      f32.sub
                      local.tee $l28
                      local.get $l37
                      local.get $l28
                      local.get $l28
                      f32.neg
                      local.tee $l29
                      local.get $l28
                      local.get $l29
                      f32.gt
                      select
                      f32.gt
                      select
                      local.set $l77
                      local.get $l11
                      f32.load offset=32
                      local.set $l78
                      local.get $l11
                      f32.load offset=40
                      local.set $l79
                      local.get $l11
                      f32.load offset=36
                      local.set $l80
                      i32.const 1
                      local.set $l11
                      loop $L47
                        local.get $l9
                        f32.load offset=144
                        local.set $l30
                        local.get $l9
                        f32.load offset=128
                        local.set $l31
                        local.get $l9
                        f32.load offset=344
                        local.set $l33
                        local.get $l9
                        f32.load offset=336
                        local.set $l36
                        local.get $l9
                        f32.load offset=340
                        local.set $l35
                        local.get $l9
                        f32.load offset=328
                        local.set $l38
                        local.get $l9
                        f32.load offset=320
                        local.set $l39
                        local.get $l9
                        f32.load offset=324
                        local.set $l40
                        local.get $l9
                        f32.load offset=288
                        local.set $l52
                        local.get $l9
                        f32.load offset=256
                        local.set $l41
                        local.get $l9
                        f32.load offset=272
                        local.set $l47
                        local.get $l9
                        f32.load offset=292
                        local.set $l53
                        local.get $l9
                        f32.load offset=260
                        local.set $l48
                        local.get $l9
                        f32.load offset=276
                        local.set $l49
                        local.get $l9
                        f32.load offset=296
                        local.set $l54
                        local.get $l9
                        f32.load offset=264
                        local.set $l37
                        local.get $l9
                        f32.load offset=280
                        local.set $l42
                        local.get $l9
                        f32.load offset=240
                        local.set $l32
                        local.get $l9
                        f32.load offset=208
                        local.set $l55
                        local.get $l9
                        f32.load offset=224
                        local.set $l50
                        local.get $l9
                        f32.load offset=244
                        local.set $l56
                        local.get $l9
                        f32.load offset=212
                        local.set $l57
                        local.get $l9
                        f32.load offset=228
                        local.set $l58
                        local.get $l9
                        f32.load offset=248
                        local.set $l46
                        local.get $l9
                        f32.load offset=216
                        local.set $l59
                        local.get $l9
                        f32.load offset=232
                        local.set $l60
                        local.get $p7
                        i32.const 0
                        i32.store offset=44
                        local.get $p7
                        i32.const 0
                        i32.store offset=12
                        local.get $p7
                        local.get $l34
                        local.tee $l28
                        f32.store offset=8
                        local.get $p7
                        local.get $p4
                        local.tee $l29
                        f32.store offset=4
                        local.get $p7
                        local.get $p5
                        local.tee $p3
                        f32.store
                        local.get $p7
                        local.get $l59
                        local.get $l75
                        local.get $l28
                        f32.mul
                        local.get $l74
                        local.get $l29
                        f32.mul
                        f32.sub
                        local.tee $p5
                        f32.mul
                        local.get $l60
                        local.get $l74
                        local.get $p3
                        f32.mul
                        local.get $l72
                        local.get $l28
                        f32.mul
                        f32.sub
                        local.tee $p4
                        f32.mul
                        f32.add
                        local.get $l46
                        local.get $l72
                        local.get $l29
                        f32.mul
                        local.get $l75
                        local.get $p3
                        f32.mul
                        f32.sub
                        local.tee $l34
                        f32.mul
                        f32.add
                        local.tee $l46
                        f32.store offset=40
                        local.get $p7
                        local.get $p5
                        local.get $l57
                        f32.mul
                        local.get $p4
                        local.get $l58
                        f32.mul
                        f32.add
                        local.get $l34
                        local.get $l56
                        f32.mul
                        f32.add
                        local.tee $l56
                        f32.store offset=36
                        local.get $p7
                        local.get $p5
                        local.get $l55
                        f32.mul
                        local.get $p4
                        local.get $l50
                        f32.mul
                        f32.add
                        local.get $l34
                        local.get $l32
                        f32.mul
                        f32.add
                        local.tee $l55
                        f32.store offset=32
                        local.get $p7
                        local.get $l37
                        local.get $l77
                        local.get $l28
                        f32.mul
                        local.get $l76
                        local.get $l29
                        f32.mul
                        f32.sub
                        local.tee $l32
                        f32.mul
                        local.get $l42
                        local.get $l76
                        local.get $p3
                        f32.mul
                        local.get $l73
                        local.get $l28
                        f32.mul
                        f32.sub
                        local.tee $l37
                        f32.mul
                        f32.add
                        local.get $l54
                        local.get $l73
                        local.get $l29
                        f32.mul
                        local.get $l77
                        local.get $p3
                        f32.mul
                        f32.sub
                        local.tee $l42
                        f32.mul
                        f32.add
                        local.tee $l54
                        f32.store offset=24
                        local.get $p7
                        local.get $l32
                        local.get $l48
                        f32.mul
                        local.get $l37
                        local.get $l49
                        f32.mul
                        f32.add
                        local.get $l42
                        local.get $l53
                        f32.mul
                        f32.add
                        local.tee $l53
                        f32.store offset=20
                        local.get $p7
                        local.get $l32
                        local.get $l41
                        f32.mul
                        local.get $l37
                        local.get $l47
                        f32.mul
                        f32.add
                        local.get $l42
                        local.get $l52
                        f32.mul
                        f32.add
                        local.tee $l52
                        f32.store offset=16
                        local.get $p7
                        local.get $l79
                        local.get $l28
                        f32.mul
                        local.get $l80
                        local.get $l29
                        f32.mul
                        local.get $l78
                        local.get $p3
                        f32.mul
                        f32.add
                        f32.add
                        local.get $l64
                        local.get $l28
                        f32.mul
                        local.get $l65
                        local.get $l29
                        f32.mul
                        local.get $l66
                        local.get $p3
                        f32.mul
                        f32.add
                        f32.add
                        local.get $l32
                        local.get $l36
                        f32.mul
                        local.get $l37
                        local.get $l35
                        f32.mul
                        f32.add
                        local.get $l42
                        local.get $l33
                        f32.mul
                        f32.add
                        f32.add
                        local.get $l61
                        local.get $l28
                        f32.mul
                        local.get $l62
                        local.get $l29
                        f32.mul
                        local.get $l63
                        local.get $p3
                        f32.mul
                        f32.add
                        f32.add
                        local.get $p5
                        local.get $l39
                        f32.mul
                        local.get $p4
                        local.get $l40
                        f32.mul
                        f32.add
                        local.get $l34
                        local.get $l38
                        f32.mul
                        f32.add
                        f32.add
                        f32.sub
                        f32.sub
                        f32.store offset=48
                        local.get $p7
                        f32.const 0x1p+0 (;=1;)
                        local.get $l51
                        local.get $l30
                        local.get $l52
                        local.get $l52
                        f32.mul
                        local.get $l53
                        local.get $l53
                        f32.mul
                        f32.add
                        local.get $l54
                        local.get $l54
                        f32.mul
                        f32.add
                        f32.mul
                        f32.add
                        local.get $l31
                        local.get $l55
                        local.get $l55
                        f32.mul
                        local.get $l56
                        local.get $l56
                        f32.mul
                        f32.add
                        local.get $l46
                        local.get $l46
                        f32.mul
                        f32.add
                        f32.mul
                        local.get $l67
                        f32.sub
                        f32.add
                        local.tee $p5
                        f32.div
                        f32.const 0x0p+0 (;=0;)
                        local.get $p5
                        f32.const 0x0p+0 (;=0;)
                        f32.gt
                        select
                        f32.neg
                        f32.store offset=28
                        local.get $p7
                        i32.const -64
                        i32.sub
                        local.set $p7
                        local.get $l11
                        local.get $l22
                        i32.ne
                        if $I48
                          local.get $l11
                          i32.const 1
                          i32.add
                          local.set $l11
                          local.get $l43
                          local.set $l34
                          local.get $l44
                          local.set $p4
                          local.get $l45
                          local.set $p5
                          local.get $l28
                          local.set $l43
                          local.get $l29
                          local.set $l44
                          local.get $p3
                          local.set $l45
                          br $L47
                        end
                      end
                      i32.const 1
                      local.set $l17
                      local.get $l45
                      local.set $p5
                      local.get $l44
                      local.set $p4
                      local.get $l43
                      local.set $l34
                      local.get $l28
                      local.set $l43
                      local.get $l29
                      local.set $l44
                      local.get $p3
                      local.set $l45
                      local.get $l12
                      i32.const 1
                      i32.add
                      local.tee $l12
                      local.get $l14
                      i32.ne
                      br_if $L46
                    end
                  end
                  local.get $l18
                  i32.const 4130
                  i32.add
                  i32.load16_u
                  local.tee $l11
                  i32.const 65535
                  i32.ne
                  br_if $L44
                end
              end
              local.get $p7
              local.set $l11
            end
            local.get $l15
            i32.const 1
            i32.add
            local.tee $l15
            local.get $p1
            i32.ne
            br_if $L40
          end
        end
        local.get $l11
        i32.const 0
        i32.store8
      end
      local.get $l20
      local.get $l27
      i32.add
      local.tee $p7
      i32.const 0
      i32.store
      i32.const 1
      local.set $l16
      local.get $p7
      i32.const 0
      local.get $l17
      i32.const 1
      i32.and
      i32.sub
      i32.store offset=4
    end
    local.get $l9
    i32.const 432
    i32.add
    global.set $g0
    local.get $l16)
