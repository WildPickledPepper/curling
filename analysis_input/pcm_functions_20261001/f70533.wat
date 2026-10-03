  (func $f70533 (type $t28) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (result i32)
    (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32)
    global.get $g0
    i32.const 320
    i32.sub
    local.tee $l9
    global.set $g0
    local.get $p1
    i32.load offset=4
    local.tee $l10
    f32.load offset=20
    local.set $l19
    local.get $p0
    i32.load offset=4
    local.tee $l11
    f32.load offset=20
    local.set $l20
    local.get $p3
    f32.load
    local.set $l48
    local.get $l11
    i32.load8_u offset=32
    local.set $l16
    local.get $l11
    f32.load offset=16
    local.set $l49
    local.get $l10
    i32.load8_u offset=32
    local.set $l17
    local.get $l10
    f32.load offset=16
    local.set $l50
    local.get $l9
    i32.const 0
    i32.store offset=28
    local.get $l19
    local.get $l20
    local.get $l19
    local.get $l20
    f32.lt
    select
    f32.const 0x1.99999ap-4 (;=0.1;)
    f32.mul
    local.set $l47
    block $B0 (result f32)
      local.get $p7
      i32.load8_u
      local.tee $l18
      if $I1
        local.get $p0
        i32.load offset=8
        local.set $p2
        i32.const 0
        local.set $p3
        loop $L2
          local.get $p3
          i32.const 2
          i32.shl
          local.tee $l12
          local.get $l9
          i32.const 48
          i32.add
          i32.add
          local.get $p3
          local.get $p5
          i32.add
          i32.load8_u
          local.tee $l13
          i32.store
          local.get $l9
          i32.const 32
          i32.add
          local.get $l12
          i32.add
          local.get $p3
          local.get $p6
          i32.add
          i32.load8_u
          local.tee $l14
          i32.store
          local.get $l11
          i32.load offset=152
          local.get $l13
          i32.const 12
          i32.mul
          i32.add
          local.tee $l12
          f32.load offset=8
          local.set $l19
          local.get $l12
          f32.load
          local.set $l20
          local.get $l12
          f32.load offset=4
          local.set $l21
          local.get $l10
          i32.load offset=152
          local.get $l14
          i32.const 12
          i32.mul
          i32.add
          local.tee $l12
          f32.load offset=8
          local.set $l22
          local.get $l12
          f32.load
          local.set $l23
          local.get $l12
          f32.load offset=4
          local.set $l24
          local.get $p2
          f32.load offset=48
          local.set $l25
          local.get $p2
          f32.load offset=32
          local.set $l27
          local.get $p2
          f32.load
          local.set $l28
          local.get $p2
          f32.load offset=16
          local.set $l29
          local.get $p2
          f32.load offset=52
          local.set $l26
          local.get $p2
          f32.load offset=36
          local.set $l35
          local.get $p2
          f32.load offset=4
          local.set $l30
          local.get $p2
          f32.load offset=20
          local.set $l32
          local.get $p2
          f32.load offset=56
          local.set $l31
          local.get $p2
          f32.load offset=40
          local.set $l36
          local.get $l11
          f32.load offset=88
          local.set $l37
          local.get $l11
          f32.load offset=56
          local.set $l40
          local.get $l11
          f32.load offset=72
          local.set $l41
          local.get $p2
          f32.load offset=8
          local.set $l42
          local.get $l11
          f32.load offset=80
          local.set $l43
          local.get $l11
          f32.load offset=48
          local.set $l38
          local.get $l11
          f32.load offset=64
          local.set $l44
          local.get $p2
          f32.load offset=24
          local.set $l33
          local.get $l11
          f32.load offset=84
          local.set $l34
          local.get $l11
          f32.load offset=52
          local.set $l39
          local.get $l11
          f32.load offset=68
          local.set $l51
          local.get $l10
          f32.load offset=80
          local.set $l52
          local.get $l10
          f32.load offset=48
          local.set $l53
          local.get $l10
          f32.load offset=64
          local.set $l54
          local.get $l10
          f32.load offset=84
          local.set $l45
          local.get $l10
          f32.load offset=52
          local.set $l55
          local.get $l10
          f32.load offset=68
          local.set $l56
          local.get $l10
          f32.load offset=88
          local.set $l46
          local.get $l10
          f32.load offset=56
          local.set $l57
          local.get $l10
          f32.load offset=72
          local.set $l58
          local.get $l9
          i32.load offset=28
          local.tee $l15
          i32.const 4
          i32.shl
          local.tee $l14
          local.get $l9
          i32.const 128
          i32.add
          i32.add
          local.tee $l12
          i32.const 0
          i32.store offset=12
          local.get $l9
          i32.const -64
          i32.sub
          local.get $l14
          i32.add
          local.tee $l13
          i32.const 0
          i32.store offset=12
          local.get $l9
          i32.const 192
          i32.add
          local.get $l14
          i32.add
          local.tee $l14
          i32.const 0
          i32.store offset=12
          local.get $l13
          local.get $l23
          local.get $l57
          f32.mul
          local.get $l24
          local.get $l58
          f32.mul
          f32.add
          local.get $l22
          local.get $l46
          f32.mul
          f32.add
          local.tee $l46
          f32.store offset=8
          local.get $l13
          local.get $l23
          local.get $l55
          f32.mul
          local.get $l24
          local.get $l56
          f32.mul
          f32.add
          local.get $l22
          local.get $l45
          f32.mul
          f32.add
          local.tee $l45
          f32.store offset=4
          local.get $l13
          local.get $l23
          local.get $l53
          f32.mul
          local.get $l24
          local.get $l54
          f32.mul
          f32.add
          local.get $l22
          local.get $l52
          f32.mul
          f32.add
          local.tee $l24
          f32.store
          local.get $l12
          local.get $l31
          local.get $l42
          local.get $l20
          local.get $l38
          f32.mul
          local.get $l21
          local.get $l44
          f32.mul
          f32.add
          local.get $l19
          local.get $l43
          f32.mul
          f32.add
          local.tee $l22
          f32.mul
          local.get $l33
          local.get $l20
          local.get $l39
          f32.mul
          local.get $l21
          local.get $l51
          f32.mul
          f32.add
          local.get $l19
          local.get $l34
          f32.mul
          f32.add
          local.tee $l23
          f32.mul
          f32.add
          local.get $l36
          local.get $l20
          local.get $l40
          f32.mul
          local.get $l21
          local.get $l41
          f32.mul
          f32.add
          local.get $l19
          local.get $l37
          f32.mul
          f32.add
          local.tee $l19
          f32.mul
          f32.add
          f32.add
          local.tee $l20
          f32.store offset=8
          local.get $l12
          local.get $l26
          local.get $l22
          local.get $l30
          f32.mul
          local.get $l23
          local.get $l32
          f32.mul
          f32.add
          local.get $l19
          local.get $l35
          f32.mul
          f32.add
          f32.add
          local.tee $l21
          f32.store offset=4
          local.get $l12
          local.get $l25
          local.get $l22
          local.get $l28
          f32.mul
          local.get $l23
          local.get $l29
          f32.mul
          f32.add
          local.get $l19
          local.get $l27
          f32.mul
          f32.add
          f32.add
          local.tee $l19
          f32.store
          local.get $l14
          local.get $l20
          local.get $l46
          f32.sub
          local.tee $l20
          f32.store offset=8
          local.get $l14
          local.get $l21
          local.get $l45
          f32.sub
          local.tee $l21
          f32.store offset=4
          local.get $l14
          local.get $l19
          local.get $l24
          f32.sub
          local.tee $l19
          f32.store
          local.get $l9
          local.get $l15
          i32.const 1
          i32.add
          i32.store offset=28
          local.get $p3
          i32.const 1
          i32.add
          local.tee $p3
          local.get $l18
          i32.ne
          br_if $L2
        end
        block $B3
          block $B4
            block $B5
              block $B6
                block $B7
                  block $B8
                    block $B9
                      local.get $l15
                      br_table $B9 $B8 $B7 $B6 $B5
                    end
                    local.get $l9
                    i32.const 0
                    i32.store offset=316
                    br $B4
                  end
                  local.get $l9
                  f32.load offset=208
                  local.get $l9
                  f32.load offset=192
                  local.tee $l22
                  f32.sub
                  local.tee $l19
                  local.get $l19
                  f32.mul
                  local.get $l9
                  f32.load offset=212
                  local.get $l9
                  f32.load offset=196
                  local.tee $l23
                  f32.sub
                  local.tee $l20
                  local.get $l20
                  f32.mul
                  f32.add
                  local.get $l9
                  f32.load offset=216
                  local.get $l9
                  f32.load offset=200
                  local.tee $l24
                  f32.sub
                  local.tee $l21
                  local.get $l21
                  f32.mul
                  f32.add
                  local.tee $l25
                  f32.const 0x1p-23 (;=1.19209e-07;)
                  f32.le
                  if $I10
                    local.get $l9
                    i32.const 1
                    i32.store offset=28
                    local.get $l9
                    local.get $l9
                    i64.load offset=192
                    i64.store offset=304
                    local.get $l9
                    local.get $l9
                    i64.load offset=200
                    i64.store offset=312
                    br $B3
                  end
                  local.get $l9
                  i32.const 0
                  i32.store offset=316
                  local.get $l9
                  local.get $l24
                  local.get $l21
                  local.get $l20
                  local.get $l23
                  f32.neg
                  f32.mul
                  local.get $l22
                  local.get $l19
                  f32.mul
                  f32.sub
                  local.get $l24
                  local.get $l21
                  f32.mul
                  f32.sub
                  local.get $l25
                  f32.div
                  f32.const 0x1p+0 (;=1;)
                  f32.min
                  local.tee $l25
                  f32.const 0x0p+0 (;=0;)
                  local.get $l25
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  select
                  local.tee $l25
                  f32.mul
                  f32.add
                  f32.store offset=312
                  local.get $l9
                  local.get $l23
                  local.get $l20
                  local.get $l25
                  f32.mul
                  f32.add
                  f32.store offset=308
                  local.get $l9
                  local.get $l22
                  local.get $l19
                  local.get $l25
                  f32.mul
                  f32.add
                  f32.store offset=304
                  br $B3
                end
                local.get $l9
                i32.const 304
                i32.add
                local.get $l9
                i32.const 192
                i32.add
                local.get $l9
                i32.const 128
                i32.add
                local.get $l9
                i32.const -64
                i32.sub
                local.get $l9
                i32.const 48
                i32.add
                local.get $l9
                i32.const 32
                i32.add
                local.get $l9
                i32.const 28
                i32.add
                call $f70518
                br $B3
              end
              local.get $l9
              i32.const 304
              i32.add
              local.get $l9
              i32.const 192
              i32.add
              local.get $l9
              i32.const 128
              i32.add
              local.get $l9
              i32.const -64
              i32.sub
              local.get $l9
              i32.const 48
              i32.add
              local.get $l9
              i32.const 32
              i32.add
              local.get $l9
              i32.const 28
              i32.add
              call $f69905
              br $B3
            end
            local.get $l9
            i32.const 0
            i32.store offset=316
          end
          local.get $l9
          local.get $l20
          f32.store offset=312
          local.get $l9
          local.get $l21
          f32.store offset=308
          local.get $l9
          local.get $l19
          f32.store offset=304
        end
        local.get $l9
        local.get $l9
        i64.load offset=304
        i64.store offset=256
        local.get $l9
        local.get $l9
        i64.load offset=312
        i64.store offset=264
        local.get $l9
        f32.load offset=256
        local.tee $l27
        local.get $l27
        f32.mul
        local.get $l9
        f32.load offset=260
        local.tee $l28
        local.get $l28
        f32.mul
        f32.add
        local.get $l9
        f32.load offset=264
        local.tee $l29
        local.get $l29
        f32.mul
        f32.add
        f32.sqrt
        local.tee $l23
        local.get $l47
        f32.gt
        local.set $p2
        local.get $l29
        f32.const 0x1p+0 (;=1;)
        local.get $l23
        f32.div
        local.tee $l19
        f32.mul
        local.set $l30
        local.get $l27
        local.get $l19
        f32.mul
        local.set $l31
        local.get $l9
        f32.load offset=268
        local.set $l38
        local.get $l28
        local.get $l19
        f32.mul
        br $B0
      end
      local.get $p2
      f32.load offset=8
      local.set $l19
      local.get $p2
      f32.load
      local.set $l20
      local.get $p2
      f32.load offset=4
      local.set $l21
      local.get $l9
      i32.const 0
      i32.store offset=268
      local.get $l9
      local.get $l19
      f32.const 0x0p+0 (;=0;)
      local.get $l20
      local.get $l20
      f32.mul
      local.get $l21
      local.get $l21
      f32.mul
      f32.add
      local.get $l19
      local.get $l19
      f32.mul
      f32.add
      f32.const 0x0p+0 (;=0;)
      f32.gt
      local.tee $p2
      select
      local.tee $l29
      f32.store offset=264
      local.get $l9
      local.get $l21
      f32.const 0x0p+0 (;=0;)
      local.get $p2
      select
      local.tee $l28
      f32.store offset=260
      local.get $l9
      local.get $l20
      f32.const 0x1p+0 (;=1;)
      local.get $p2
      select
      local.tee $l27
      f32.store offset=256
      local.get $l29
      f32.const 0x1p+0 (;=1;)
      local.get $l29
      local.get $l29
      f32.mul
      local.get $l27
      local.get $l27
      f32.mul
      local.get $l28
      local.get $l28
      f32.mul
      f32.add
      f32.add
      f32.sqrt
      f32.div
      local.tee $l19
      f32.mul
      local.set $l30
      local.get $l27
      local.get $l19
      f32.mul
      local.set $l31
      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
      local.set $l23
      i32.const 1
      local.set $p2
      local.get $l28
      local.get $l19
      f32.mul
    end
    local.set $l32
    block $B11
      block $B12
        local.get $p2
        i32.eqz
        br_if $B12
        local.get $l48
        local.get $l49
        f32.const 0x0p+0 (;=0;)
        local.get $l16
        select
        local.tee $l33
        local.get $l50
        f32.const 0x0p+0 (;=0;)
        local.get $l17
        select
        local.tee $l34
        f32.add
        local.tee $l39
        f32.add
        local.set $l44
        local.get $p0
        i32.const 16
        i32.add
        local.set $l17
        loop $L13
          local.get $l9
          local.get $l9
          i32.load offset=296
          i32.store offset=280
          local.get $l9
          local.get $l9
          i64.load offset=288 align=4
          i64.store offset=272
          local.get $l9
          i32.const 0
          i32.store offset=12
          local.get $l9
          local.get $l29
          f32.neg
          f32.store offset=8
          local.get $l9
          local.get $l28
          f32.neg
          f32.store offset=4
          local.get $l9
          local.get $l27
          f32.neg
          f32.store
          local.get $l9
          i32.const 304
          i32.add
          local.get $p0
          i32.load offset=4
          local.get $l9
          local.get $p0
          i32.load offset=8
          local.get $l17
          local.get $l9
          i32.const 48
          i32.add
          local.get $l9
          i32.load offset=28
          i32.const 2
          i32.shl
          i32.add
          call $f70538
          local.get $l9
          f32.load offset=316
          local.set $l43
          local.get $l9
          f32.load offset=312
          local.set $l22
          local.get $l9
          f32.load offset=304
          local.set $l24
          local.get $l9
          f32.load offset=308
          local.set $l25
          local.get $l9
          i32.load offset=28
          local.set $l10
          local.get $p1
          i32.load offset=4
          local.tee $p2
          i32.const 56
          i32.add
          local.tee $l11
          f32.load
          local.set $l26
          local.get $p2
          i32.const 52
          i32.add
          local.tee $p3
          f32.load
          local.set $l35
          local.get $p2
          i32.const 72
          i32.add
          local.tee $l12
          f32.load
          local.set $l36
          local.get $p2
          i32.const -64
          i32.sub
          local.tee $l13
          f32.load
          local.set $l37
          local.get $p2
          i32.const 68
          i32.add
          local.tee $l14
          f32.load
          local.set $l40
          local.get $p2
          i32.const 88
          i32.add
          local.tee $l15
          f32.load
          local.set $l41
          local.get $p2
          i32.const 80
          i32.add
          local.tee $l18
          f32.load
          local.set $l20
          local.get $p2
          i32.const 84
          i32.add
          local.tee $l16
          f32.load
          local.set $l21
          local.get $p2
          f32.load offset=48
          local.set $l42
          local.get $l9
          i32.const 0
          i32.store offset=316
          local.get $l9
          local.get $l20
          local.get $l9
          f32.load offset=256
          local.tee $l19
          f32.mul
          local.get $l21
          local.get $l9
          f32.load offset=260
          local.tee $l20
          f32.mul
          f32.add
          local.get $l41
          local.get $l9
          f32.load offset=264
          local.tee $l21
          f32.mul
          f32.add
          f32.store offset=312
          local.get $l9
          local.get $l19
          local.get $l37
          f32.mul
          local.get $l20
          local.get $l40
          f32.mul
          f32.add
          local.get $l21
          local.get $l36
          f32.mul
          f32.add
          f32.store offset=308
          local.get $l9
          local.get $l19
          local.get $l42
          f32.mul
          local.get $l20
          local.get $l35
          f32.mul
          f32.add
          local.get $l21
          local.get $l26
          f32.mul
          f32.add
          f32.store offset=304
          local.get $l9
          i32.const 32
          i32.add
          local.get $l10
          i32.const 2
          i32.shl
          i32.add
          local.get $p2
          local.get $l9
          i32.const 304
          i32.add
          call $f70525
          local.tee $l10
          i32.store
          local.get $l44
          local.get $l31
          local.get $l24
          local.get $p2
          i32.load offset=152
          local.get $l10
          i32.const 12
          i32.mul
          i32.add
          local.tee $l10
          f32.load
          local.tee $l19
          local.get $p2
          f32.load offset=48
          f32.mul
          local.get $l10
          f32.load offset=4
          local.tee $l20
          local.get $l13
          f32.load
          f32.mul
          f32.add
          local.get $l10
          f32.load offset=8
          local.tee $l21
          local.get $l18
          f32.load
          f32.mul
          f32.add
          local.tee $l36
          f32.sub
          local.tee $l26
          f32.mul
          local.get $l32
          local.get $l25
          local.get $l19
          local.get $p3
          f32.load
          f32.mul
          local.get $l20
          local.get $l14
          f32.load
          f32.mul
          f32.add
          local.get $l21
          local.get $l16
          f32.load
          f32.mul
          f32.add
          local.tee $l37
          f32.sub
          local.tee $l35
          f32.mul
          f32.add
          local.get $l30
          local.get $l22
          local.get $l19
          local.get $l11
          f32.load
          f32.mul
          local.get $l20
          local.get $l12
          f32.load
          f32.mul
          f32.add
          local.get $l21
          local.get $l15
          f32.load
          f32.mul
          f32.add
          local.tee $l21
          f32.sub
          local.tee $l19
          f32.mul
          f32.add
          local.tee $l20
          f32.lt
          if $I14
            i32.const 0
            local.set $l12
            local.get $p5
            i32.eqz
            br_if $B11
            local.get $p7
            local.get $l9
            i32.load offset=28
            local.tee $l10
            i32.store8
            local.get $l10
            i32.eqz
            br_if $B11
            local.get $l10
            i32.const 1
            i32.and
            local.set $l13
            i32.const 0
            local.set $p2
            local.get $l10
            i32.const 1
            i32.ne
            if $I15
              local.get $l10
              i32.const -2
              i32.and
              local.set $l11
              loop $L16
                local.get $p2
                local.get $p5
                i32.add
                local.get $p2
                i32.const 2
                i32.shl
                local.tee $l10
                local.get $l9
                i32.const 48
                i32.add
                i32.add
                i32.load
                i32.store8
                local.get $p2
                local.get $p6
                i32.add
                local.get $l9
                i32.const 32
                i32.add
                local.get $l10
                i32.add
                i32.load
                i32.store8
                local.get $p5
                local.get $p2
                i32.const 1
                i32.or
                local.tee $l10
                i32.add
                local.get $l10
                i32.const 2
                i32.shl
                local.tee $p3
                local.get $l9
                i32.const 48
                i32.add
                i32.add
                i32.load
                i32.store8
                local.get $p6
                local.get $l10
                i32.add
                local.get $l9
                i32.const 32
                i32.add
                local.get $p3
                i32.add
                i32.load
                i32.store8
                local.get $p2
                i32.const 2
                i32.add
                local.set $p2
                local.get $l11
                i32.const 2
                i32.sub
                local.tee $l11
                br_if $L16
              end
            end
            local.get $l13
            i32.eqz
            br_if $B11
            local.get $p2
            local.get $p5
            i32.add
            local.get $p2
            i32.const 2
            i32.shl
            local.tee $l10
            local.get $l9
            i32.const 48
            i32.add
            i32.add
            i32.load
            i32.store8
            local.get $p2
            local.get $p6
            i32.add
            local.get $l9
            i32.const 32
            i32.add
            local.get $l10
            i32.add
            i32.load
            i32.store8
            br $B11
          end
          local.get $l9
          i32.load offset=28
          local.set $p2
          local.get $l23
          f32.const 0x1.ffe282p-1 (;=0.999775;)
          f32.mul
          local.get $l20
          f32.lt
          if $I17
            block $B18
              local.get $p5
              i32.eqz
              br_if $B18
              local.get $p7
              local.get $p2
              i32.store8
              local.get $p2
              i32.eqz
              br_if $B18
              local.get $p2
              i32.const 1
              i32.and
              local.set $l13
              i32.const 0
              local.set $l10
              local.get $p2
              i32.const 1
              i32.ne
              if $I19
                local.get $p2
                i32.const -2
                i32.and
                local.set $p3
                loop $L20
                  local.get $p5
                  local.get $l10
                  i32.add
                  local.get $l10
                  i32.const 2
                  i32.shl
                  local.tee $l11
                  local.get $l9
                  i32.const 48
                  i32.add
                  i32.add
                  i32.load
                  i32.store8
                  local.get $p6
                  local.get $l10
                  i32.add
                  local.get $l9
                  i32.const 32
                  i32.add
                  local.get $l11
                  i32.add
                  i32.load
                  i32.store8
                  local.get $p5
                  local.get $l10
                  i32.const 1
                  i32.or
                  local.tee $l11
                  i32.add
                  local.get $l11
                  i32.const 2
                  i32.shl
                  local.tee $l12
                  local.get $l9
                  i32.const 48
                  i32.add
                  i32.add
                  i32.load
                  i32.store8
                  local.get $p6
                  local.get $l11
                  i32.add
                  local.get $l9
                  i32.const 32
                  i32.add
                  local.get $l12
                  i32.add
                  i32.load
                  i32.store8
                  local.get $l10
                  i32.const 2
                  i32.add
                  local.set $l10
                  local.get $p3
                  i32.const 2
                  i32.sub
                  local.tee $p3
                  br_if $L20
                end
              end
              local.get $l13
              i32.eqz
              br_if $B18
              local.get $p5
              local.get $l10
              i32.add
              local.get $l10
              i32.const 2
              i32.shl
              local.tee $l11
              local.get $l9
              i32.const 48
              i32.add
              i32.add
              i32.load
              i32.store8
              local.get $p6
              local.get $l10
              i32.add
              local.get $l9
              i32.const 32
              i32.add
              local.get $l11
              i32.add
              i32.load
              i32.store8
            end
            local.get $p8
            local.get $l31
            f32.store offset=32
            local.get $p8
            i32.const 0
            i32.store offset=44
            local.get $p8
            local.get $l30
            f32.store offset=40
            local.get $p8
            local.get $l32
            f32.store offset=36
            local.get $l9
            i32.const 192
            i32.add
            local.get $l9
            i32.const 128
            i32.add
            local.get $l9
            i32.const -64
            i32.sub
            local.get $l9
            i32.const 256
            i32.add
            local.get $l9
            i32.const 304
            i32.add
            local.get $l9
            local.get $p2
            call $f70517
            block $B21
              local.get $p4
              if $I22
                local.get $p8
                local.get $l9
                i64.load offset=304
                i64.store
                local.get $p8
                local.get $l9
                i64.load offset=312
                i64.store offset=8
                local.get $p8
                local.get $l9
                i64.load
                i64.store offset=16
                local.get $p8
                local.get $l9
                i64.load offset=8
                i64.store offset=24
                local.get $p8
                local.get $l9
                i64.load offset=288 align=4
                i64.store offset=68 align=4
                local.get $p8
                local.get $l9
                i32.load offset=296
                i32.store offset=76
                br $B21
              end
              local.get $l9
              f32.load offset=304
              local.set $l19
              local.get $l9
              f32.load offset=308
              local.set $l20
              local.get $l9
              f32.load offset=312
              local.set $l21
              local.get $p8
              i32.const 0
              i32.store offset=12
              local.get $p8
              local.get $l21
              local.get $l33
              local.get $l30
              f32.mul
              f32.sub
              f32.store offset=8
              local.get $p8
              local.get $l20
              local.get $l33
              local.get $l32
              f32.mul
              f32.sub
              f32.store offset=4
              local.get $p8
              local.get $l19
              local.get $l33
              local.get $l31
              f32.mul
              f32.sub
              f32.store
              local.get $l9
              f32.load
              local.set $l19
              local.get $l9
              f32.load offset=4
              local.set $l20
              local.get $l9
              f32.load offset=8
              local.set $l21
              local.get $p8
              i32.const 0
              i32.store offset=28
              local.get $p8
              local.get $l21
              local.get $l34
              local.get $l30
              f32.mul
              f32.add
              f32.store offset=24
              local.get $p8
              local.get $l20
              local.get $l34
              local.get $l32
              f32.mul
              f32.add
              f32.store offset=20
              local.get $p8
              local.get $l19
              local.get $l34
              local.get $l31
              f32.mul
              f32.add
              f32.store offset=16
              local.get $l23
              local.get $l39
              f32.sub
              local.set $l23
            end
            local.get $p8
            local.get $l23
            f32.store offset=64
            i32.const 2
            local.set $l12
            br $B11
          end
          local.get $p2
          i32.const 4
          i32.shl
          local.tee $l11
          local.get $l9
          i32.const 128
          i32.add
          i32.add
          local.tee $l10
          local.get $l43
          f32.store offset=12
          local.get $l10
          local.get $l22
          f32.store offset=8
          local.get $l10
          local.get $l25
          f32.store offset=4
          local.get $l10
          local.get $l24
          f32.store
          local.get $l9
          i32.const -64
          i32.sub
          local.get $l11
          i32.add
          local.tee $l10
          i32.const 0
          i32.store offset=12
          local.get $l10
          local.get $l21
          f32.store offset=8
          local.get $l10
          local.get $l37
          f32.store offset=4
          local.get $l10
          local.get $l36
          f32.store
          local.get $l9
          i32.const 192
          i32.add
          local.get $l11
          i32.add
          local.tee $l10
          i32.const 0
          i32.store offset=12
          local.get $l10
          local.get $l19
          f32.store offset=8
          local.get $l10
          local.get $l35
          f32.store offset=4
          local.get $l10
          local.get $l26
          f32.store
          local.get $l9
          local.get $p2
          i32.const 1
          i32.add
          i32.store offset=28
          block $B23
            block $B24
              block $B25
                block $B26
                  block $B27
                    local.get $p2
                    i32.const 1
                    i32.sub
                    br_table $B27 $B26 $B25 $B24
                  end
                  local.get $l9
                  f32.load offset=208
                  local.get $l9
                  f32.load offset=192
                  local.tee $l22
                  f32.sub
                  local.tee $l19
                  local.get $l19
                  f32.mul
                  local.get $l9
                  f32.load offset=212
                  local.get $l9
                  f32.load offset=196
                  local.tee $l24
                  f32.sub
                  local.tee $l20
                  local.get $l20
                  f32.mul
                  f32.add
                  local.get $l9
                  f32.load offset=216
                  local.get $l9
                  f32.load offset=200
                  local.tee $l25
                  f32.sub
                  local.tee $l21
                  local.get $l21
                  f32.mul
                  f32.add
                  local.tee $l26
                  f32.const 0x1p-23 (;=1.19209e-07;)
                  f32.le
                  if $I28
                    local.get $l9
                    i32.const 1
                    i32.store offset=28
                    local.get $l9
                    local.get $l9
                    i64.load offset=192
                    i64.store offset=304
                    local.get $l9
                    local.get $l9
                    i64.load offset=200
                    i64.store offset=312
                    br $B23
                  end
                  local.get $l9
                  i32.const 0
                  i32.store offset=316
                  local.get $l9
                  local.get $l25
                  local.get $l21
                  local.get $l20
                  local.get $l24
                  f32.neg
                  f32.mul
                  local.get $l22
                  local.get $l19
                  f32.mul
                  f32.sub
                  local.get $l25
                  local.get $l21
                  f32.mul
                  f32.sub
                  local.get $l26
                  f32.div
                  f32.const 0x1p+0 (;=1;)
                  f32.min
                  local.tee $l26
                  f32.const 0x0p+0 (;=0;)
                  local.get $l26
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  select
                  local.tee $l26
                  f32.mul
                  f32.add
                  f32.store offset=312
                  local.get $l9
                  local.get $l24
                  local.get $l20
                  local.get $l26
                  f32.mul
                  f32.add
                  f32.store offset=308
                  local.get $l9
                  local.get $l22
                  local.get $l19
                  local.get $l26
                  f32.mul
                  f32.add
                  f32.store offset=304
                  br $B23
                end
                local.get $l9
                i32.const 304
                i32.add
                local.get $l9
                i32.const 192
                i32.add
                local.get $l9
                i32.const 128
                i32.add
                local.get $l9
                i32.const -64
                i32.sub
                local.get $l9
                i32.const 48
                i32.add
                local.get $l9
                i32.const 32
                i32.add
                local.get $l9
                i32.const 28
                i32.add
                call $f70518
                br $B23
              end
              local.get $l9
              i32.const 304
              i32.add
              local.get $l9
              i32.const 192
              i32.add
              local.get $l9
              i32.const 128
              i32.add
              local.get $l9
              i32.const -64
              i32.sub
              local.get $l9
              i32.const 48
              i32.add
              local.get $l9
              i32.const 32
              i32.add
              local.get $l9
              i32.const 28
              i32.add
              call $f69905
              br $B23
            end
            local.get $l9
            i32.const 0
            i32.store offset=316
            local.get $l9
            local.get $l19
            f32.store offset=312
            local.get $l9
            local.get $l35
            f32.store offset=308
            local.get $l9
            local.get $l26
            f32.store offset=304
          end
          local.get $l9
          local.get $l9
          i64.load offset=304
          i64.store offset=256
          local.get $l9
          local.get $l9
          i64.load offset=312
          i64.store offset=264
          local.get $l9
          f32.load offset=264
          local.tee $l20
          f32.const 0x1p+0 (;=1;)
          local.get $l9
          f32.load offset=256
          local.tee $l21
          local.get $l21
          f32.mul
          local.get $l9
          f32.load offset=260
          local.tee $l22
          local.get $l22
          f32.mul
          f32.add
          local.get $l20
          local.get $l20
          f32.mul
          f32.add
          f32.sqrt
          local.tee $l19
          f32.div
          local.tee $l24
          f32.mul
          local.set $l30
          local.get $l22
          local.get $l24
          f32.mul
          local.set $l32
          local.get $l21
          local.get $l24
          f32.mul
          local.set $l31
          block $B29
            local.get $l19
            local.get $l47
            f32.gt
            i32.eqz
            br_if $B29
            local.get $l19
            local.get $l23
            f32.lt
            i32.eqz
            br_if $B29
            local.get $l9
            f32.load offset=268
            local.set $l38
            local.get $l20
            local.set $l29
            local.get $l22
            local.set $l28
            local.get $l21
            local.set $l27
            local.get $l19
            local.set $l23
            br $L13
          end
        end
        local.get $l19
        local.get $l23
        f32.lt
        br_if $B12
        local.get $l9
        i32.load offset=28
        local.set $l12
        block $B30
          local.get $p5
          i32.eqz
          br_if $B30
          local.get $p7
          local.get $l12
          i32.const 1
          i32.sub
          local.tee $l10
          i32.store8
          local.get $l10
          i32.eqz
          br_if $B30
          local.get $l10
          i32.const 1
          i32.and
          local.set $l13
          i32.const 0
          local.set $p2
          local.get $l12
          i32.const 2
          i32.ne
          if $I31
            local.get $l10
            i32.const -2
            i32.and
            local.set $l11
            loop $L32
              local.get $p2
              local.get $p5
              i32.add
              local.get $p2
              i32.const 2
              i32.shl
              local.tee $l10
              local.get $l9
              i32.const 48
              i32.add
              i32.add
              i32.load
              i32.store8
              local.get $p2
              local.get $p6
              i32.add
              local.get $l9
              i32.const 32
              i32.add
              local.get $l10
              i32.add
              i32.load
              i32.store8
              local.get $p5
              local.get $p2
              i32.const 1
              i32.or
              local.tee $l10
              i32.add
              local.get $l10
              i32.const 2
              i32.shl
              local.tee $p3
              local.get $l9
              i32.const 48
              i32.add
              i32.add
              i32.load
              i32.store8
              local.get $p6
              local.get $l10
              i32.add
              local.get $l9
              i32.const 32
              i32.add
              local.get $p3
              i32.add
              i32.load
              i32.store8
              local.get $p2
              i32.const 2
              i32.add
              local.set $p2
              local.get $l11
              i32.const 2
              i32.sub
              local.tee $l11
              br_if $L32
            end
          end
          local.get $l13
          i32.eqz
          br_if $B30
          local.get $p2
          local.get $p5
          i32.add
          local.get $p2
          i32.const 2
          i32.shl
          local.tee $l10
          local.get $l9
          i32.const 48
          i32.add
          i32.add
          i32.load
          i32.store8
          local.get $p2
          local.get $p6
          i32.add
          local.get $l9
          i32.const 32
          i32.add
          local.get $l10
          i32.add
          i32.load
          i32.store8
        end
        local.get $l9
        local.get $l9
        i32.const 280
        i32.add
        local.tee $p2
        i32.load
        i32.store offset=296
        local.get $l9
        local.get $l9
        i64.load offset=272
        i64.store offset=288
        local.get $l9
        local.get $l38
        f32.store offset=268
        local.get $l9
        local.get $l27
        f32.store offset=256
        local.get $l9
        local.get $l28
        f32.store offset=260
        local.get $l9
        local.get $l29
        f32.store offset=264
        local.get $l9
        i32.const 192
        i32.add
        local.get $l9
        i32.const 128
        i32.add
        local.get $l9
        i32.const -64
        i32.sub
        local.get $l9
        i32.const 256
        i32.add
        local.get $l9
        i32.const 304
        i32.add
        local.get $l9
        local.get $l12
        call $f70517
        local.get $p8
        i32.const 0
        i32.store offset=60
        local.get $p8
        local.get $l30
        f32.store offset=56
        local.get $p8
        local.get $l32
        f32.store offset=52
        local.get $p8
        local.get $l31
        f32.store offset=48
        local.get $p8
        i32.const 0
        i32.store offset=44
        local.get $p8
        local.get $l29
        f32.const 0x1p+0 (;=1;)
        local.get $l23
        f32.div
        local.tee $l19
        f32.mul
        local.tee $l20
        f32.store offset=40
        local.get $p8
        local.get $l28
        local.get $l19
        f32.mul
        local.tee $l21
        f32.store offset=36
        local.get $p8
        local.get $l27
        local.get $l19
        f32.mul
        local.tee $l19
        f32.store offset=32
        local.get $p4
        if $I33
          local.get $p8
          local.get $l9
          i64.load offset=304
          i64.store
          local.get $p8
          local.get $l9
          i64.load offset=312
          i64.store offset=8
          local.get $p8
          local.get $l9
          i64.load
          i64.store offset=16
          local.get $p8
          local.get $l9
          i64.load offset=8
          i64.store offset=24
          local.get $p8
          local.get $l23
          f32.store offset=64
          local.get $p8
          local.get $l9
          i64.load offset=272
          i64.store offset=68 align=4
          local.get $p8
          local.get $p2
          i32.load
          i32.store offset=76
          i32.const 4
          local.set $l12
          br $B11
        end
        local.get $l9
        f32.load offset=304
        local.set $l22
        local.get $l9
        f32.load offset=308
        local.set $l24
        local.get $l9
        f32.load offset=312
        local.set $l25
        local.get $p8
        i32.const 0
        i32.store offset=12
        local.get $p8
        local.get $l25
        local.get $l33
        local.get $l20
        f32.mul
        f32.sub
        f32.store offset=8
        local.get $p8
        local.get $l24
        local.get $l33
        local.get $l21
        f32.mul
        f32.sub
        f32.store offset=4
        local.get $p8
        local.get $l22
        local.get $l33
        local.get $l19
        f32.mul
        f32.sub
        f32.store
        local.get $l9
        f32.load
        local.set $l22
        local.get $l9
        f32.load offset=4
        local.set $l24
        local.get $l9
        f32.load offset=8
        local.set $l25
        local.get $p8
        local.get $l23
        local.get $l39
        f32.sub
        f32.store offset=64
        local.get $p8
        i32.const 0
        i32.store offset=28
        local.get $p8
        local.get $l25
        local.get $l34
        local.get $l20
        f32.mul
        f32.add
        f32.store offset=24
        local.get $p8
        local.get $l24
        local.get $l34
        local.get $l21
        f32.mul
        f32.add
        f32.store offset=20
        local.get $p8
        local.get $l22
        local.get $l34
        local.get $l19
        f32.mul
        f32.add
        f32.store offset=16
        i32.const 2
        local.set $l12
        local.get $l23
        local.get $l39
        f32.le
        br_if $B11
        i32.const 4
        local.set $l12
        br $B11
      end
      i32.const 5
      local.set $l12
      local.get $p5
      i32.eqz
      br_if $B11
      local.get $p7
      local.get $l9
      i32.load offset=28
      local.tee $l10
      i32.store8
      local.get $l10
      i32.eqz
      br_if $B11
      local.get $l10
      i32.const 1
      i32.and
      local.set $l13
      i32.const 0
      local.set $p2
      local.get $l10
      i32.const 1
      i32.ne
      if $I34
        local.get $l10
        i32.const -2
        i32.and
        local.set $l11
        loop $L35
          local.get $p2
          local.get $p5
          i32.add
          local.get $p2
          i32.const 2
          i32.shl
          local.tee $l10
          local.get $l9
          i32.const 48
          i32.add
          i32.add
          i32.load
          i32.store8
          local.get $p2
          local.get $p6
          i32.add
          local.get $l9
          i32.const 32
          i32.add
          local.get $l10
          i32.add
          i32.load
          i32.store8
          local.get $p5
          local.get $p2
          i32.const 1
          i32.or
          local.tee $l10
          i32.add
          local.get $l10
          i32.const 2
          i32.shl
          local.tee $p3
          local.get $l9
          i32.const 48
          i32.add
          i32.add
          i32.load
          i32.store8
          local.get $p6
          local.get $l10
          i32.add
          local.get $l9
          i32.const 32
          i32.add
          local.get $p3
          i32.add
          i32.load
          i32.store8
          local.get $p2
          i32.const 2
          i32.add
          local.set $p2
          local.get $l11
          i32.const 2
          i32.sub
          local.tee $l11
          br_if $L35
        end
      end
      local.get $l13
      i32.eqz
      br_if $B11
      local.get $p2
      local.get $p5
      i32.add
      local.get $p2
      i32.const 2
      i32.shl
      local.tee $l10
      local.get $l9
      i32.const 48
      i32.add
      i32.add
      i32.load
      i32.store8
      local.get $p2
      local.get $p6
      i32.add
      local.get $l9
      i32.const 32
      i32.add
      local.get $l10
      i32.add
      i32.load
      i32.store8
    end
    local.get $l9
    i32.const 320
    i32.add
    global.set $g0
    local.get $l12)