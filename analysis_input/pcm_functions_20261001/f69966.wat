  (func $f69966 (type $t436) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 f32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (param $p9 i32) (param $p10 i32) (result i32)
    (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32) (local $l64 f32) (local $l65 f32) (local $l66 f32) (local $l67 i64)
    global.get $g0
    i32.const 560
    i32.sub
    local.tee $l11
    global.set $g0
    block $B0
      local.get $p0
      i32.eqz
      if $I1
        i32.const 0
        local.set $p8
        br $B0
      end
      local.get $p8
      i32.load16_u
      local.tee $p8
      i32.const 16
      i32.and
      local.set $l17
      local.get $p8
      i32.const 64
      i32.and
      local.set $l18
      local.get $p8
      i32.const 128
      i32.and
      local.set $p8
      local.get $p2
      f32.load
      local.tee $l24
      local.get $p2
      f32.load offset=12
      local.tee $l25
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l50
      local.get $l50
      f32.mul
      local.get $p2
      f32.load offset=4
      local.tee $l28
      local.get $p2
      f32.load offset=16
      local.tee $l27
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l51
      local.get $l51
      f32.mul
      f32.add
      local.get $p2
      f32.load offset=8
      local.tee $l29
      local.get $p2
      f32.load offset=20
      local.tee $l33
      f32.sub
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l48
      local.get $l48
      f32.mul
      f32.add
      f32.sqrt
      local.tee $l26
      f32.const 0x0p+0 (;=0;)
      f32.eq
      if $I2
        local.get $p0
        local.get $p1
        local.get $p2
        local.get $p2
        f32.load offset=24
        local.get $p3
        local.get $p4
        local.get $p5
        local.get $p6
        local.get $p7
        local.get $p9
        local.get $p8
        i32.const 0
        i32.ne
        local.get $l18
        i32.const 0
        i32.ne
        local.get $l17
        i32.eqz
        call $f69963
        local.set $p8
        br $B0
      end
      local.get $p8
      i32.const 7
      i32.shr_u
      local.get $p9
      i32.or
      local.set $l19
      local.get $p8
      i32.eqz
      local.set $l22
      local.get $p3
      f32.load offset=8
      local.set $l46
      local.get $p3
      f32.load
      local.set $l57
      local.get $p3
      f32.load offset=4
      local.set $l54
      local.get $l11
      local.get $l29
      local.get $l33
      f32.add
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l31
      f32.store offset=552
      local.get $l11
      local.get $l28
      local.get $l27
      f32.add
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l34
      f32.store offset=548
      local.get $l11
      local.get $l24
      local.get $l25
      f32.add
      f32.const 0x1p-1 (;=0.5;)
      f32.mul
      local.tee $l39
      f32.store offset=544
      local.get $l57
      local.get $l50
      f32.const 0x1p+0 (;=1;)
      local.get $l26
      f32.div
      local.tee $l30
      f32.mul
      f32.mul
      local.get $l54
      local.get $l51
      local.get $l30
      f32.mul
      f32.mul
      f32.add
      local.get $l46
      local.get $l48
      local.get $l30
      f32.mul
      f32.mul
      f32.add
      f32.abs
      f32.const 0x1.fffebp-1 (;=0.99999;)
      f32.lt
      i32.eqz
      if $I3
        local.get $l11
        local.get $l27
        local.get $l28
        f32.sub
        local.tee $l28
        f32.store offset=292
        local.get $l11
        local.get $l25
        local.get $l24
        f32.sub
        local.tee $l24
        f32.store offset=288
        local.get $l11
        local.get $l33
        local.get $l29
        f32.sub
        local.tee $l25
        f32.store offset=296
        local.get $l11
        local.get $l24
        local.get $l24
        f32.mul
        local.get $l28
        local.get $l28
        f32.mul
        f32.add
        local.get $l25
        local.get $l25
        f32.mul
        f32.add
        local.tee $l24
        f32.store offset=300
        local.get $l11
        f32.const 0x1p+0 (;=1;)
        local.get $l24
        f32.div
        f32.const 0x0p+0 (;=0;)
        local.get $l24
        f32.const 0x0p+0 (;=0;)
        f32.ne
        select
        f32.store offset=304
        local.get $l11
        local.get $l26
        local.get $l46
        f32.mul
        local.get $l31
        f32.add
        local.tee $l24
        f32.store offset=136
        local.get $l11
        local.get $l26
        local.get $l54
        f32.mul
        local.get $l34
        f32.add
        local.tee $l25
        f32.store offset=132
        local.get $l11
        local.get $l26
        local.get $l57
        f32.mul
        local.get $l39
        f32.add
        local.tee $l26
        f32.store offset=128
        local.get $p5
        if $I4
          local.get $p5
          i32.load
          local.set $l12
        end
        local.get $l57
        local.get $l26
        f32.mul
        local.get $l54
        local.get $l25
        f32.mul
        f32.add
        local.get $l46
        local.get $l24
        f32.mul
        f32.add
        local.set $l57
        f32.const 0x1p+1 (;=2;)
        local.set $l35
        i32.const -1
        local.set $l13
        local.get $p4
        local.set $l26
        i32.const 0
        local.set $p5
        f32.const 0x0p+0 (;=0;)
        local.set $l48
        block $B5
          block $B6
            loop $L7
              block $B8
                block $B9
                  local.get $l11
                  i32.const 128
                  i32.add
                  local.get $p3
                  local.get $l26
                  local.get $p2
                  f32.load offset=24
                  local.tee $l27
                  local.get $p1
                  i32.const 0
                  local.get $p5
                  local.get $p5
                  local.get $l12
                  i32.eq
                  select
                  local.get $l12
                  local.get $p5
                  select
                  local.tee $l14
                  i32.const 36
                  i32.mul
                  i32.add
                  local.tee $p8
                  call $f69964
                  i32.eqz
                  br_if $B9
                  local.get $l57
                  local.get $l26
                  f32.add
                  local.get $l27
                  f32.const 0x1.0624dep-9 (;=0.002;)
                  f32.add
                  local.tee $l27
                  f32.add
                  local.get $p8
                  f32.load
                  local.tee $l54
                  local.get $p3
                  f32.load
                  local.tee $l24
                  f32.mul
                  local.get $p8
                  f32.load offset=4
                  local.tee $l31
                  local.get $p3
                  f32.load offset=4
                  local.tee $l25
                  f32.mul
                  f32.add
                  local.get $p8
                  f32.load offset=8
                  local.tee $l34
                  local.get $p3
                  f32.load offset=8
                  local.tee $l28
                  f32.mul
                  f32.add
                  local.tee $l29
                  local.get $l24
                  local.get $p8
                  f32.load offset=12
                  local.tee $l39
                  f32.mul
                  local.get $l25
                  local.get $p8
                  f32.load offset=16
                  local.tee $l40
                  f32.mul
                  f32.add
                  local.get $l28
                  local.get $p8
                  f32.load offset=20
                  local.tee $l41
                  f32.mul
                  f32.add
                  local.tee $l33
                  local.get $l29
                  local.get $l33
                  f32.lt
                  select
                  local.tee $l46
                  local.get $l24
                  local.get $p8
                  f32.load offset=24
                  local.tee $l42
                  f32.mul
                  local.get $l25
                  local.get $p8
                  f32.load offset=28
                  local.tee $l50
                  f32.mul
                  f32.add
                  local.get $l28
                  local.get $p8
                  f32.load offset=32
                  local.tee $l51
                  f32.mul
                  f32.add
                  local.tee $l30
                  local.get $l30
                  local.get $l46
                  f32.gt
                  select
                  f32.lt
                  br_if $B9
                  block $B10
                    local.get $l29
                    local.get $l57
                    local.get $l27
                    f32.sub
                    local.tee $l27
                    f32.lt
                    i32.eqz
                    br_if $B10
                    local.get $l27
                    local.get $l33
                    f32.gt
                    i32.eqz
                    br_if $B10
                    local.get $l27
                    local.get $l30
                    f32.gt
                    br_if $B9
                  end
                  local.get $l11
                  local.get $l39
                  local.get $l54
                  f32.sub
                  local.tee $l29
                  local.get $l50
                  local.get $l31
                  f32.sub
                  local.tee $l33
                  f32.mul
                  local.get $l40
                  local.get $l31
                  f32.sub
                  local.tee $l30
                  local.get $l42
                  local.get $l54
                  f32.sub
                  local.tee $l46
                  f32.mul
                  f32.sub
                  local.tee $l27
                  f32.store offset=200
                  local.get $l11
                  local.get $l41
                  local.get $l34
                  f32.sub
                  local.tee $l54
                  local.get $l46
                  f32.mul
                  local.get $l29
                  local.get $l51
                  local.get $l34
                  f32.sub
                  local.tee $l46
                  f32.mul
                  f32.sub
                  local.tee $l29
                  f32.store offset=196
                  local.get $l11
                  local.get $l30
                  local.get $l46
                  f32.mul
                  local.get $l54
                  local.get $l33
                  f32.mul
                  f32.sub
                  local.tee $l33
                  f32.store offset=192
                  local.get $l19
                  i32.eqz
                  if $I11
                    local.get $l33
                    local.get $l24
                    f32.mul
                    local.get $l29
                    local.get $l25
                    f32.mul
                    f32.add
                    local.get $l27
                    local.get $l28
                    f32.mul
                    f32.add
                    f32.const 0x0p+0 (;=0;)
                    f32.gt
                    br_if $B9
                  end
                  local.get $l17
                  i32.eqz
                  if $I12
                    local.get $l11
                    i32.const 192
                    i32.add
                    local.get $p8
                    local.get $p8
                    i32.const 12
                    i32.add
                    local.get $p8
                    i32.const 24
                    i32.add
                    local.get $p2
                    local.get $l11
                    i32.const 288
                    i32.add
                    call $f69907
                    br_if $B8
                    local.get $l11
                    f32.load offset=196
                    local.set $l29
                    local.get $l11
                    f32.load offset=192
                    local.set $l33
                    local.get $l11
                    f32.load offset=200
                    local.set $l27
                  end
                  local.get $l33
                  local.get $l33
                  f32.mul
                  local.get $l29
                  local.get $l29
                  f32.mul
                  f32.add
                  local.get $l27
                  local.get $l27
                  f32.mul
                  f32.add
                  f32.sqrt
                  local.tee $l24
                  f32.const 0x0p+0 (;=0;)
                  f32.eq
                  br_if $B9
                  local.get $l11
                  local.get $l27
                  f32.const 0x1p+0 (;=1;)
                  local.get $l24
                  f32.div
                  local.tee $l24
                  f32.mul
                  f32.store offset=200
                  local.get $l11
                  local.get $l29
                  local.get $l24
                  f32.mul
                  f32.store offset=196
                  local.get $l11
                  local.get $l33
                  local.get $l24
                  f32.mul
                  f32.store offset=192
                  local.get $p8
                  local.get $l11
                  i32.const 192
                  i32.add
                  local.get $l11
                  i32.const 128
                  i32.add
                  local.get $p2
                  f32.load offset=24
                  local.get $p3
                  local.get $l11
                  i32.const 152
                  i32.add
                  local.get $l11
                  i32.const 112
                  i32.add
                  i32.const 0
                  call $f69960
                  i32.eqz
                  br_if $B9
                  local.get $l11
                  f32.load offset=152
                  local.tee $l24
                  local.get $p4
                  f32.gt
                  br_if $B9
                  local.get $l11
                  f32.load offset=192
                  local.tee $l28
                  local.get $p3
                  f32.load
                  f32.mul
                  local.get $l11
                  f32.load offset=196
                  local.tee $l27
                  local.get $p3
                  f32.load offset=4
                  f32.mul
                  f32.add
                  local.get $l11
                  f32.load offset=200
                  local.tee $l29
                  local.get $p3
                  f32.load offset=8
                  f32.mul
                  f32.add
                  f32.abs
                  f32.neg
                  local.set $l25
                  block $B13
                    local.get $l26
                    local.get $l24
                    local.get $l26
                    local.get $l24
                    local.get $l26
                    f32.gt
                    select
                    f32.const 0x1p+0 (;=1;)
                    f32.max
                    f32.const 0x1.0624dep-10 (;=0.001;)
                    f32.mul
                    local.tee $l33
                    f32.sub
                    local.get $l24
                    f32.gt
                    br_if $B13
                    local.get $l25
                    local.get $l35
                    f32.lt
                    local.get $l26
                    local.get $l33
                    f32.add
                    local.get $l24
                    f32.gt
                    i32.and
                    br_if $B13
                    local.get $l24
                    f32.const 0x0p+0 (;=0;)
                    f32.eq
                    br_if $B13
                    local.get $l25
                    local.get $l35
                    f32.eq
                    local.get $l24
                    local.get $l26
                    f32.lt
                    i32.and
                    i32.eqz
                    br_if $B9
                  end
                  local.get $l18
                  br_if $B6
                  local.get $l28
                  local.set $l36
                  local.get $l27
                  local.set $l44
                  local.get $l29
                  local.set $l48
                  local.get $l25
                  local.set $l35
                  local.get $l24
                  local.set $l26
                  local.get $l14
                  local.set $l13
                end
                local.get $p5
                i32.const 1
                i32.add
                local.tee $p5
                local.get $p0
                i32.ne
                br_if $L7
                br $B5
              end
            end
            local.get $p3
            f32.load
            local.set $l26
            local.get $p3
            f32.load offset=4
            local.set $l24
            local.get $p7
            local.get $p3
            f32.load offset=8
            f32.neg
            f32.store offset=8
            local.get $p7
            local.get $l24
            f32.neg
            f32.store offset=4
            local.get $p7
            local.get $l26
            f32.neg
            f32.store
            local.get $p6
            i32.const 1026
            i32.store16 offset=12
            local.get $p6
            local.get $l14
            i32.store offset=8
            local.get $p3
            f32.load
            local.set $l26
            local.get $p3
            f32.load offset=4
            local.set $l24
            local.get $p3
            f32.load offset=8
            local.set $l25
            local.get $p6
            i32.const 0
            i32.store offset=40
            local.get $p6
            local.get $l25
            f32.neg
            f32.store offset=36
            local.get $p6
            local.get $l24
            f32.neg
            f32.store offset=32
            local.get $p6
            local.get $l26
            f32.neg
            f32.store offset=28
            i32.const 1
            local.set $p8
            br $B0
          end
          local.get $l28
          local.set $l36
          local.get $l27
          local.set $l44
          local.get $l29
          local.set $l48
          local.get $l24
          local.set $l26
          local.get $l14
          local.set $l13
        end
        local.get $l13
        i32.const -1
        i32.ne
        if $I14
          local.get $l11
          i32.const 192
          i32.add
          local.get $l11
          i32.const 152
          i32.add
          local.get $l11
          i32.const 128
          i32.add
          local.get $p3
          local.get $l26
          local.get $p1
          local.get $l13
          i32.const 36
          i32.mul
          i32.add
          call $f69957
          block $B15
            local.get $p9
            local.get $l22
            i32.or
            br_if $B15
            local.get $l36
            local.get $p3
            f32.load
            f32.mul
            local.get $l44
            local.get $p3
            f32.load offset=4
            f32.mul
            f32.add
            local.get $l48
            local.get $p3
            f32.load offset=8
            f32.mul
            f32.add
            f32.const 0x0p+0 (;=0;)
            f32.gt
            i32.eqz
            br_if $B15
            local.get $l11
            local.get $l11
            f32.load offset=160
            f32.neg
            f32.store offset=160
            local.get $l11
            local.get $l11
            f32.load offset=156
            f32.neg
            f32.store offset=156
            local.get $l11
            local.get $l11
            f32.load offset=152
            f32.neg
            f32.store offset=152
          end
          local.get $p6
          local.get $l11
          f32.load offset=192
          f32.store offset=16
          local.get $p6
          local.get $l11
          f32.load offset=196
          f32.store offset=20
          local.get $p6
          local.get $l11
          f32.load offset=200
          f32.store offset=24
          local.get $p6
          local.get $l11
          f32.load offset=152
          f32.store offset=28
          local.get $p6
          local.get $l11
          f32.load offset=156
          f32.store offset=32
          local.get $l11
          f32.load offset=160
          local.set $l24
          local.get $p6
          local.get $l26
          f32.store offset=40
          local.get $p6
          local.get $l24
          f32.store offset=36
          local.get $p6
          i32.const 3
          i32.store16 offset=12
          local.get $p6
          local.get $l13
          i32.store offset=8
          local.get $p7
          local.get $l48
          f32.store offset=8
          local.get $p7
          local.get $l44
          f32.store offset=4
          local.get $p7
          local.get $l36
          f32.store
        end
        local.get $l13
        i32.const -1
        i32.ne
        local.set $p8
        br $B0
      end
      local.get $p6
      i32.const -1
      i32.store offset=8
      local.get $p5
      if $I16
        local.get $p5
        i32.load
        local.set $l16
      end
      local.get $p2
      f32.load offset=24
      local.set $l33
      local.get $p3
      f32.load offset=8
      local.set $l28
      local.get $p3
      f32.load
      local.set $l27
      local.get $p3
      f32.load offset=4
      local.set $l29
      local.get $p2
      f32.load offset=8
      local.set $l25
      local.get $p2
      f32.load offset=20
      local.set $l30
      local.get $p2
      f32.load
      local.set $l24
      local.get $p2
      f32.load offset=12
      local.set $l46
      local.get $l11
      local.get $p2
      f32.load offset=16
      local.get $p2
      f32.load offset=4
      f32.sub
      local.tee $l26
      f32.store offset=132
      local.get $l11
      local.get $l46
      local.get $l24
      f32.sub
      local.tee $l24
      f32.store offset=128
      local.get $l11
      local.get $l30
      local.get $l25
      f32.sub
      local.tee $l25
      f32.store offset=136
      local.get $l11
      local.get $l24
      local.get $l24
      f32.mul
      local.get $l26
      local.get $l26
      f32.mul
      f32.add
      local.get $l25
      local.get $l25
      f32.mul
      f32.add
      local.tee $l26
      f32.store offset=140
      local.get $l11
      f32.const 0x1p+0 (;=1;)
      local.get $l26
      f32.div
      f32.const 0x0p+0 (;=0;)
      local.get $l26
      f32.const 0x0p+0 (;=0;)
      f32.ne
      select
      f32.store offset=144
      local.get $l39
      local.get $l27
      f32.mul
      local.get $l34
      local.get $l29
      f32.mul
      f32.add
      local.get $l31
      local.get $l28
      f32.mul
      f32.add
      local.tee $l57
      local.get $l33
      f32.const 0x1.0624dep-9 (;=0.002;)
      f32.add
      local.tee $l54
      f32.sub
      local.set $l46
      f32.const 0x1p+1 (;=2;)
      local.set $l63
      local.get $p4
      local.set $l26
      block $B17
        loop $L18
          block $B19
            local.get $p1
            i32.const 0
            local.get $l15
            local.get $l15
            local.get $l16
            i32.eq
            select
            local.get $l16
            local.get $l15
            select
            local.tee $l23
            i32.const 36
            i32.mul
            i32.add
            local.tee $p8
            i32.const 20
            i32.add
            local.tee $l14
            f32.load
            local.set $l25
            local.get $p8
            f32.load offset=8
            local.set $l24
            local.get $p8
            i32.const 32
            i32.add
            local.tee $l13
            f32.load
            local.set $l28
            local.get $l11
            local.get $p8
            f32.load offset=12
            local.get $p8
            f32.load
            local.tee $l27
            f32.sub
            local.tee $l29
            local.get $p8
            i32.const 28
            i32.add
            local.tee $l20
            f32.load
            local.get $p8
            f32.load offset=4
            local.tee $l30
            f32.sub
            local.tee $l31
            f32.mul
            local.get $p8
            i32.const 16
            i32.add
            local.tee $l21
            f32.load
            local.get $l30
            f32.sub
            local.tee $l30
            local.get $p8
            f32.load offset=24
            local.get $l27
            f32.sub
            local.tee $l27
            f32.mul
            f32.sub
            local.tee $l34
            f32.store offset=120
            local.get $l11
            local.get $l25
            local.get $l24
            f32.sub
            local.tee $l25
            local.get $l27
            f32.mul
            local.get $l29
            local.get $l28
            local.get $l24
            f32.sub
            local.tee $l24
            f32.mul
            f32.sub
            local.tee $l28
            f32.store offset=116
            local.get $l11
            local.get $l30
            local.get $l24
            f32.mul
            local.get $l25
            local.get $l31
            f32.mul
            f32.sub
            local.tee $l24
            f32.store offset=112
            block $B20
              local.get $l19
              i32.eqz
              if $I21
                local.get $l24
                local.get $p3
                f32.load
                f32.mul
                local.get $l28
                local.get $p3
                f32.load offset=4
                f32.mul
                f32.add
                local.get $l34
                local.get $p3
                f32.load offset=8
                f32.mul
                f32.add
                f32.const 0x0p+0 (;=0;)
                f32.gt
                br_if $B20
              end
              local.get $p8
              i32.const 24
              i32.add
              local.set $p5
              local.get $p8
              i32.const 12
              i32.add
              local.set $l12
              local.get $p10
              if $I22
                local.get $p10
                local.get $p8
                local.get $l12
                local.get $p5
                call $f69916
                i32.eqz
                br_if $B20
              end
              block $B23
                local.get $l17
                br_if $B23
                local.get $l11
                i32.const 112
                i32.add
                local.get $p8
                local.get $l12
                local.get $p5
                local.get $p2
                local.get $l11
                i32.const 128
                i32.add
                call $f69907
                i32.eqz
                br_if $B23
                local.get $p3
                f32.load
                local.set $l26
                local.get $p3
                f32.load offset=4
                local.set $l24
                local.get $p7
                local.get $p3
                f32.load offset=8
                f32.neg
                f32.store offset=8
                local.get $p7
                local.get $l24
                f32.neg
                f32.store offset=4
                local.get $p7
                local.get $l26
                f32.neg
                f32.store
                local.get $p6
                i32.const 1026
                i32.store16 offset=12
                local.get $p6
                local.get $l23
                i32.store offset=8
                local.get $p3
                f32.load
                local.set $l26
                local.get $p3
                f32.load offset=4
                local.set $l24
                local.get $p3
                f32.load offset=8
                local.set $l25
                local.get $p6
                i32.const 0
                i32.store offset=40
                local.get $p6
                local.get $l25
                f32.neg
                f32.store offset=36
                local.get $p6
                local.get $l24
                f32.neg
                f32.store offset=32
                local.get $p6
                local.get $l26
                f32.neg
                f32.store offset=28
                i32.const 1
                local.set $p8
                br $B0
              end
              local.get $l48
              local.get $l13
              f32.load
              local.tee $l24
              f32.add
              local.set $l40
              local.get $l51
              local.get $l20
              f32.load
              local.tee $l25
              f32.add
              local.set $l41
              local.get $l50
              local.get $p5
              f32.load
              local.tee $l28
              f32.add
              local.set $l42
              local.get $l48
              local.get $l14
              f32.load
              local.tee $l31
              f32.add
              local.set $l55
              local.get $l51
              local.get $l21
              f32.load
              local.tee $l34
              f32.add
              local.set $l56
              local.get $l50
              local.get $l12
              f32.load
              local.tee $l39
              f32.add
              local.set $l58
              local.get $l48
              local.get $p8
              f32.load offset=8
              local.tee $l44
              f32.add
              local.set $l27
              local.get $l51
              local.get $p8
              f32.load offset=4
              local.tee $l36
              f32.add
              local.set $l29
              local.get $l50
              local.get $p8
              f32.load
              local.tee $l35
              f32.add
              local.set $l30
              local.get $l24
              local.get $l48
              f32.sub
              local.set $l45
              local.get $l25
              local.get $l51
              f32.sub
              local.set $l32
              local.get $l28
              local.get $l50
              f32.sub
              local.set $l37
              local.get $l31
              local.get $l48
              f32.sub
              local.set $l24
              local.get $l34
              local.get $l51
              f32.sub
              local.set $l25
              local.get $l39
              local.get $l50
              f32.sub
              local.set $l28
              local.get $l44
              local.get $l48
              f32.sub
              local.set $l31
              local.get $l36
              local.get $l51
              f32.sub
              local.set $l34
              local.get $l35
              local.get $l50
              f32.sub
              local.set $l39
              block $B24 (result f32)
                local.get $l50
                local.get $l11
                f32.load offset=112
                local.tee $l59
                f32.mul
                local.get $l51
                local.get $l11
                f32.load offset=116
                local.tee $l60
                f32.mul
                f32.add
                local.get $l48
                local.get $l11
                f32.load offset=120
                local.tee $l61
                f32.mul
                f32.add
                f32.const 0x0p+0 (;=0;)
                f32.ge
                if $I25
                  local.get $l11
                  local.get $l30
                  f32.store offset=288
                  local.get $l11
                  local.get $l42
                  f32.store offset=312
                  local.get $l11
                  local.get $l29
                  f32.store offset=292
                  local.get $l11
                  local.get $l56
                  f32.store offset=304
                  local.get $l11
                  local.get $l41
                  f32.store offset=316
                  local.get $l11
                  local.get $l58
                  f32.store offset=300
                  local.get $l58
                  local.get $l30
                  f32.sub
                  local.tee $l36
                  local.get $l41
                  local.get $l29
                  f32.sub
                  local.tee $l35
                  f32.mul
                  local.get $l56
                  local.get $l29
                  f32.sub
                  local.tee $l43
                  local.get $l42
                  local.get $l30
                  f32.sub
                  local.tee $l38
                  f32.mul
                  f32.sub
                  local.set $l44
                  local.get $l11
                  local.get $l27
                  f32.store offset=296
                  local.get $l11
                  local.get $l40
                  f32.store offset=320
                  local.get $l11
                  local.get $l55
                  f32.store offset=308
                  local.get $l55
                  local.get $l27
                  f32.sub
                  local.tee $l52
                  local.get $l38
                  f32.mul
                  local.get $l36
                  local.get $l40
                  local.get $l27
                  f32.sub
                  local.tee $l38
                  f32.mul
                  f32.sub
                  local.set $l36
                  local.get $l43
                  local.get $l38
                  f32.mul
                  local.get $l52
                  local.get $l35
                  f32.mul
                  f32.sub
                  br $B24
                end
                local.get $l11
                local.get $l39
                f32.store offset=288
                local.get $l11
                local.get $l37
                f32.store offset=312
                local.get $l11
                local.get $l34
                f32.store offset=292
                local.get $l11
                local.get $l25
                f32.store offset=304
                local.get $l11
                local.get $l32
                f32.store offset=316
                local.get $l11
                local.get $l28
                f32.store offset=300
                local.get $l28
                local.get $l39
                f32.sub
                local.tee $l36
                local.get $l32
                local.get $l34
                f32.sub
                local.tee $l35
                f32.mul
                local.get $l25
                local.get $l34
                f32.sub
                local.tee $l43
                local.get $l37
                local.get $l39
                f32.sub
                local.tee $l38
                f32.mul
                f32.sub
                local.set $l44
                local.get $l11
                local.get $l31
                f32.store offset=296
                local.get $l11
                local.get $l45
                f32.store offset=320
                local.get $l11
                local.get $l24
                f32.store offset=308
                local.get $l24
                local.get $l31
                f32.sub
                local.tee $l52
                local.get $l38
                f32.mul
                local.get $l36
                local.get $l45
                local.get $l31
                f32.sub
                local.tee $l38
                f32.mul
                f32.sub
                local.set $l36
                local.get $l43
                local.get $l38
                f32.mul
                local.get $l52
                local.get $l35
                f32.mul
                f32.sub
              end
              local.set $l35
              local.get $l11
              local.get $l44
              f32.store offset=200
              local.get $l11
              local.get $l36
              f32.store offset=196
              local.get $l11
              local.get $l35
              f32.store offset=192
              local.get $l11
              local.get $l24
              f32.store offset=332
              local.get $l11
              local.get $l40
              f32.store offset=356
              local.get $l11
              local.get $l28
              f32.store offset=324
              local.get $l11
              local.get $l58
              f32.store offset=336
              local.get $l11
              local.get $l42
              f32.store offset=348
              local.get $l11
              local.get $l55
              f32.store offset=344
              local.get $l11
              local.get $l56
              f32.store offset=340
              local.get $l11
              local.get $l41
              f32.store offset=352
              local.get $l11
              local.get $l25
              f32.store offset=328
              local.get $l58
              local.get $l28
              f32.sub
              local.tee $l47
              local.get $l41
              local.get $l25
              f32.sub
              local.tee $l43
              f32.mul
              local.get $l56
              local.get $l25
              f32.sub
              local.tee $l35
              local.get $l42
              local.get $l28
              f32.sub
              local.tee $l38
              f32.mul
              f32.sub
              local.tee $l49
              local.get $p3
              f32.load offset=8
              local.tee $l44
              f32.mul
              local.get $p3
              f32.load
              local.tee $l36
              local.get $l35
              local.get $l40
              local.get $l24
              f32.sub
              local.tee $l52
              f32.mul
              local.get $l55
              local.get $l24
              f32.sub
              local.tee $l62
              local.get $l43
              f32.mul
              f32.sub
              local.tee $l53
              f32.mul
              local.get $p3
              f32.load offset=4
              local.tee $l35
              local.get $l62
              local.get $l38
              f32.mul
              local.get $l47
              local.get $l52
              f32.mul
              f32.sub
              local.tee $l47
              f32.mul
              f32.add
              f32.add
              f32.const 0x0p+0 (;=0;)
              f32.gt
              if $I26
                local.get $l11
                local.get $l55
                f32.store offset=356
                local.get $l11
                local.get $l56
                f32.store offset=352
                local.get $l11
                local.get $l58
                f32.store offset=348
                local.get $l11
                local.get $l40
                f32.store offset=344
                local.get $l11
                local.get $l41
                f32.store offset=340
                local.get $l11
                local.get $l42
                f32.store offset=336
                local.get $l49
                f32.neg
                local.set $l49
                local.get $l53
                f32.neg
                local.set $l53
                local.get $l47
                f32.neg
                local.set $l47
              end
              local.get $l11
              local.get $l49
              f32.store offset=212
              local.get $l11
              local.get $l47
              f32.store offset=208
              local.get $l11
              local.get $l53
              f32.store offset=204
              local.get $l11
              local.get $l40
              f32.store offset=380
              local.get $l11
              local.get $l41
              f32.store offset=376
              local.get $l11
              local.get $l42
              f32.store offset=372
              local.get $l11
              local.get $l24
              f32.store offset=368
              local.get $l11
              local.get $l45
              f32.store offset=392
              local.get $l11
              local.get $l28
              f32.store offset=360
              local.get $l11
              local.get $l37
              f32.store offset=384
              local.get $l11
              local.get $l25
              f32.store offset=364
              local.get $l11
              local.get $l32
              f32.store offset=388
              local.get $l44
              local.get $l38
              local.get $l32
              local.get $l25
              f32.sub
              local.tee $l53
              f32.mul
              local.get $l43
              local.get $l37
              local.get $l28
              f32.sub
              local.tee $l47
              f32.mul
              f32.sub
              local.tee $l49
              f32.mul
              local.get $l36
              local.get $l43
              local.get $l45
              local.get $l24
              f32.sub
              local.tee $l62
              f32.mul
              local.get $l52
              local.get $l53
              f32.mul
              f32.sub
              local.tee $l43
              f32.mul
              local.get $l35
              local.get $l52
              local.get $l47
              f32.mul
              local.get $l38
              local.get $l62
              f32.mul
              f32.sub
              local.tee $l38
              f32.mul
              f32.add
              f32.add
              f32.const 0x0p+0 (;=0;)
              f32.gt
              if $I27
                local.get $l11
                local.get $l40
                f32.store offset=392
                local.get $l11
                local.get $l41
                f32.store offset=388
                local.get $l11
                local.get $l42
                f32.store offset=384
                local.get $l11
                local.get $l45
                f32.store offset=380
                local.get $l11
                local.get $l32
                f32.store offset=376
                local.get $l11
                local.get $l37
                f32.store offset=372
                local.get $l49
                f32.neg
                local.set $l49
                local.get $l43
                f32.neg
                local.set $l43
                local.get $l38
                f32.neg
                local.set $l38
              end
              local.get $l11
              local.get $l49
              f32.store offset=224
              local.get $l11
              local.get $l38
              f32.store offset=220
              local.get $l11
              local.get $l43
              f32.store offset=216
              local.get $l11
              local.get $l31
              f32.store offset=404
              local.get $l11
              local.get $l40
              f32.store offset=428
              local.get $l11
              local.get $l39
              f32.store offset=396
              local.get $l11
              local.get $l37
              f32.store offset=408
              local.get $l11
              local.get $l42
              f32.store offset=420
              local.get $l11
              local.get $l45
              f32.store offset=416
              local.get $l11
              local.get $l34
              f32.store offset=400
              local.get $l11
              local.get $l41
              f32.store offset=424
              local.get $l11
              local.get $l32
              f32.store offset=412
              local.get $l44
              local.get $l37
              local.get $l39
              f32.sub
              local.tee $l47
              local.get $l41
              local.get $l34
              f32.sub
              local.tee $l43
              f32.mul
              local.get $l32
              local.get $l34
              f32.sub
              local.tee $l53
              local.get $l42
              local.get $l39
              f32.sub
              local.tee $l38
              f32.mul
              f32.sub
              local.tee $l49
              f32.mul
              local.get $l36
              local.get $l53
              local.get $l40
              local.get $l31
              f32.sub
              local.tee $l52
              f32.mul
              local.get $l45
              local.get $l31
              f32.sub
              local.tee $l62
              local.get $l43
              f32.mul
              f32.sub
              local.tee $l53
              f32.mul
              local.get $l35
              local.get $l62
              local.get $l38
              f32.mul
              local.get $l47
              local.get $l52
              f32.mul
              f32.sub
              local.tee $l47
              f32.mul
              f32.add
              f32.add
              f32.const 0x0p+0 (;=0;)
              f32.gt
              if $I28
                local.get $l11
                local.get $l45
                f32.store offset=428
                local.get $l11
                local.get $l32
                f32.store offset=424
                local.get $l11
                local.get $l37
                f32.store offset=420
                local.get $l11
                local.get $l40
                f32.store offset=416
                local.get $l11
                local.get $l41
                f32.store offset=412
                local.get $l11
                local.get $l42
                f32.store offset=408
                local.get $l49
                f32.neg
                local.set $l49
                local.get $l53
                f32.neg
                local.set $l53
                local.get $l47
                f32.neg
                local.set $l47
              end
              local.get $l11
              local.get $l49
              f32.store offset=236
              local.get $l11
              local.get $l47
              f32.store offset=232
              local.get $l11
              local.get $l53
              f32.store offset=228
              local.get $l11
              local.get $l40
              f32.store offset=452
              local.get $l11
              local.get $l41
              f32.store offset=448
              local.get $l11
              local.get $l42
              f32.store offset=444
              local.get $l11
              local.get $l31
              f32.store offset=440
              local.get $l11
              local.get $l27
              f32.store offset=464
              local.get $l11
              local.get $l39
              f32.store offset=432
              local.get $l11
              local.get $l30
              f32.store offset=456
              local.get $l11
              local.get $l34
              f32.store offset=436
              local.get $l11
              local.get $l29
              f32.store offset=460
              local.get $l44
              local.get $l38
              local.get $l29
              local.get $l34
              f32.sub
              local.tee $l32
              f32.mul
              local.get $l43
              local.get $l30
              local.get $l39
              f32.sub
              local.tee $l37
              f32.mul
              f32.sub
              local.tee $l45
              f32.mul
              local.get $l36
              local.get $l43
              local.get $l27
              local.get $l31
              f32.sub
              local.tee $l49
              f32.mul
              local.get $l52
              local.get $l32
              f32.mul
              f32.sub
              local.tee $l32
              f32.mul
              local.get $l35
              local.get $l52
              local.get $l37
              f32.mul
              local.get $l38
              local.get $l49
              f32.mul
              f32.sub
              local.tee $l37
              f32.mul
              f32.add
              f32.add
              f32.const 0x0p+0 (;=0;)
              f32.gt
              if $I29
                local.get $l11
                local.get $l40
                f32.store offset=464
                local.get $l11
                local.get $l41
                f32.store offset=460
                local.get $l11
                local.get $l42
                f32.store offset=456
                local.get $l11
                local.get $l27
                f32.store offset=452
                local.get $l11
                local.get $l29
                f32.store offset=448
                local.get $l11
                local.get $l30
                f32.store offset=444
                local.get $l45
                f32.neg
                local.set $l45
                local.get $l37
                f32.neg
                local.set $l37
                local.get $l32
                f32.neg
                local.set $l32
              end
              local.get $l11
              local.get $l45
              f32.store offset=248
              local.get $l11
              local.get $l37
              f32.store offset=244
              local.get $l11
              local.get $l32
              f32.store offset=240
              local.get $l11
              local.get $l27
              f32.store offset=476
              local.get $l11
              local.get $l24
              f32.store offset=500
              local.get $l11
              local.get $l30
              f32.store offset=468
              local.get $l11
              local.get $l58
              f32.store offset=480
              local.get $l11
              local.get $l28
              f32.store offset=492
              local.get $l11
              local.get $l55
              f32.store offset=488
              local.get $l11
              local.get $l29
              f32.store offset=472
              local.get $l11
              local.get $l25
              f32.store offset=496
              local.get $l11
              local.get $l56
              f32.store offset=484
              local.get $l58
              local.get $l30
              f32.sub
              local.tee $l37
              local.get $l25
              local.get $l29
              f32.sub
              local.tee $l40
              f32.mul
              local.get $l56
              local.get $l29
              f32.sub
              local.tee $l32
              local.get $l28
              local.get $l30
              f32.sub
              local.tee $l41
              f32.mul
              f32.sub
              local.tee $l45
              local.get $l44
              f32.mul
              local.get $l36
              local.get $l32
              local.get $l24
              local.get $l27
              f32.sub
              local.tee $l42
              f32.mul
              local.get $l55
              local.get $l27
              f32.sub
              local.tee $l43
              local.get $l40
              f32.mul
              f32.sub
              local.tee $l32
              f32.mul
              local.get $l35
              local.get $l43
              local.get $l41
              f32.mul
              local.get $l37
              local.get $l42
              f32.mul
              f32.sub
              local.tee $l37
              f32.mul
              f32.add
              f32.add
              f32.const 0x0p+0 (;=0;)
              f32.gt
              if $I30
                local.get $l11
                local.get $l55
                f32.store offset=500
                local.get $l11
                local.get $l56
                f32.store offset=496
                local.get $l11
                local.get $l58
                f32.store offset=492
                local.get $l11
                local.get $l24
                f32.store offset=488
                local.get $l11
                local.get $l25
                f32.store offset=484
                local.get $l11
                local.get $l28
                f32.store offset=480
                local.get $l45
                f32.neg
                local.set $l45
                local.get $l37
                f32.neg
                local.set $l37
                local.get $l32
                f32.neg
                local.set $l32
              end
              local.get $l11
              local.get $l45
              f32.store offset=260
              local.get $l11
              local.get $l37
              f32.store offset=256
              local.get $l11
              local.get $l32
              f32.store offset=252
              local.get $l11
              local.get $l24
              f32.store offset=524
              local.get $l11
              local.get $l25
              f32.store offset=520
              local.get $l11
              local.get $l28
              f32.store offset=516
              local.get $l11
              local.get $l27
              f32.store offset=512
              local.get $l11
              local.get $l31
              f32.store offset=536
              local.get $l11
              local.get $l30
              f32.store offset=504
              local.get $l11
              local.get $l39
              f32.store offset=528
              local.get $l11
              local.get $l29
              f32.store offset=508
              local.get $l11
              local.get $l34
              f32.store offset=532
              local.get $l44
              local.get $l41
              local.get $l34
              local.get $l29
              f32.sub
              local.tee $l55
              f32.mul
              local.get $l40
              local.get $l39
              local.get $l30
              f32.sub
              local.tee $l30
              f32.mul
              f32.sub
              local.tee $l29
              f32.mul
              local.get $l36
              local.get $l40
              local.get $l31
              local.get $l27
              f32.sub
              local.tee $l56
              f32.mul
              local.get $l42
              local.get $l55
              f32.mul
              f32.sub
              local.tee $l27
              f32.mul
              local.get $l35
              local.get $l42
              local.get $l30
              f32.mul
              local.get $l41
              local.get $l56
              f32.mul
              f32.sub
              local.tee $l30
              f32.mul
              f32.add
              f32.add
              f32.const 0x0p+0 (;=0;)
              f32.gt
              if $I31
                local.get $l11
                local.get $l24
                f32.store offset=536
                local.get $l11
                local.get $l25
                f32.store offset=532
                local.get $l11
                local.get $l28
                f32.store offset=528
                local.get $l11
                local.get $l31
                f32.store offset=524
                local.get $l11
                local.get $l34
                f32.store offset=520
                local.get $l11
                local.get $l39
                f32.store offset=516
                local.get $l29
                f32.neg
                local.set $l29
                local.get $l30
                f32.neg
                local.set $l30
                local.get $l27
                f32.neg
                local.set $l27
              end
              local.get $l11
              local.get $l29
              f32.store offset=272
              local.get $l11
              local.get $l30
              f32.store offset=268
              local.get $l11
              local.get $l27
              f32.store offset=264
              local.get $l59
              local.get $l59
              f32.mul
              local.get $l60
              local.get $l60
              f32.mul
              f32.add
              local.get $l61
              local.get $l61
              f32.mul
              f32.add
              f32.sqrt
              local.tee $l24
              f32.const 0x0p+0 (;=0;)
              f32.gt
              if $I32
                local.get $l11
                local.get $l61
                f32.const 0x1p+0 (;=1;)
                local.get $l24
                f32.div
                local.tee $l24
                f32.mul
                local.tee $l61
                f32.store offset=120
                local.get $l11
                local.get $l60
                local.get $l24
                f32.mul
                local.tee $l60
                f32.store offset=116
                local.get $l11
                local.get $l59
                local.get $l24
                f32.mul
                local.tee $l59
                f32.store offset=112
              end
              local.get $l36
              local.get $l59
              f32.mul
              local.get $l35
              local.get $l60
              f32.mul
              f32.add
              local.get $l44
              local.get $l61
              f32.mul
              f32.add
              f32.abs
              f32.neg
              local.set $l31
              i32.const 0
              local.set $p5
              loop $L33
                local.get $l11
                i32.const 192
                i32.add
                local.get $p5
                i32.const 12
                i32.mul
                i32.add
                local.set $l12
                block $B34
                  local.get $l19
                  i32.eqz
                  if $I35
                    local.get $l12
                    f32.load
                    local.get $p3
                    f32.load
                    f32.mul
                    local.get $l12
                    f32.load offset=4
                    local.get $p3
                    f32.load offset=4
                    f32.mul
                    f32.add
                    local.get $l12
                    f32.load offset=8
                    local.get $p3
                    f32.load offset=8
                    f32.mul
                    f32.add
                    f32.const 0x0p+0 (;=0;)
                    f32.gt
                    br_if $B34
                  end
                  local.get $l11
                  i32.const 544
                  i32.add
                  local.get $p3
                  local.get $l26
                  local.get $l33
                  local.get $l11
                  i32.const 288
                  i32.add
                  local.get $p5
                  i32.const 36
                  i32.mul
                  i32.add
                  local.tee $p8
                  call $f69964
                  i32.eqz
                  br_if $B34
                  local.get $l54
                  local.get $l57
                  local.get $l26
                  f32.add
                  f32.add
                  local.get $p8
                  f32.load
                  local.get $p3
                  f32.load
                  local.tee $l24
                  f32.mul
                  local.get $p8
                  f32.load offset=4
                  local.get $p3
                  f32.load offset=4
                  local.tee $l25
                  f32.mul
                  f32.add
                  local.get $p8
                  f32.load offset=8
                  local.get $p3
                  f32.load offset=8
                  local.tee $l28
                  f32.mul
                  f32.add
                  local.tee $l27
                  local.get $l24
                  local.get $p8
                  f32.load offset=12
                  f32.mul
                  local.get $l25
                  local.get $p8
                  i32.const 16
                  i32.add
                  local.tee $l14
                  f32.load
                  f32.mul
                  f32.add
                  local.get $l28
                  local.get $p8
                  i32.const 20
                  i32.add
                  local.tee $l13
                  f32.load
                  f32.mul
                  f32.add
                  local.tee $l29
                  local.get $l27
                  local.get $l29
                  f32.lt
                  select
                  local.tee $l30
                  local.get $l24
                  local.get $p8
                  f32.load offset=24
                  f32.mul
                  local.get $l25
                  local.get $p8
                  i32.const 28
                  i32.add
                  local.tee $l20
                  f32.load
                  f32.mul
                  f32.add
                  local.get $l28
                  local.get $p8
                  i32.const 32
                  i32.add
                  local.tee $l21
                  f32.load
                  f32.mul
                  f32.add
                  local.tee $l24
                  local.get $l24
                  local.get $l30
                  f32.gt
                  select
                  f32.lt
                  br_if $B34
                  block $B36
                    local.get $l27
                    local.get $l46
                    f32.lt
                    i32.eqz
                    br_if $B36
                    local.get $l29
                    local.get $l46
                    f32.lt
                    i32.eqz
                    br_if $B36
                    local.get $l24
                    local.get $l46
                    f32.lt
                    br_if $B34
                  end
                  local.get $l12
                  f32.load
                  local.tee $l24
                  local.get $l24
                  f32.mul
                  local.get $l12
                  f32.load offset=4
                  local.tee $l25
                  local.get $l25
                  f32.mul
                  f32.add
                  local.get $l12
                  f32.load offset=8
                  local.tee $l28
                  local.get $l28
                  f32.mul
                  f32.add
                  f32.sqrt
                  local.tee $l27
                  f32.const 0x0p+0 (;=0;)
                  f32.eq
                  br_if $B34
                  local.get $l12
                  local.get $l24
                  f32.const 0x1p+0 (;=1;)
                  local.get $l27
                  f32.div
                  local.tee $l27
                  f32.mul
                  f32.store
                  local.get $l12
                  local.get $l25
                  local.get $l27
                  f32.mul
                  f32.store offset=4
                  local.get $l12
                  local.get $l28
                  local.get $l27
                  f32.mul
                  f32.store offset=8
                  local.get $p8
                  local.get $l12
                  local.get $l11
                  i32.const 544
                  i32.add
                  local.get $l33
                  local.get $p3
                  local.get $l11
                  i32.const 96
                  i32.add
                  local.get $l11
                  i32.const 80
                  i32.add
                  i32.const 0
                  call $f69960
                  i32.eqz
                  br_if $B34
                  local.get $l11
                  f32.load offset=96
                  local.tee $l24
                  local.get $p4
                  f32.gt
                  br_if $B34
                  block $B37
                    local.get $l26
                    local.get $l24
                    local.get $l26
                    local.get $l24
                    local.get $l26
                    f32.gt
                    select
                    f32.const 0x1p+0 (;=1;)
                    f32.max
                    f32.const 0x1.0624dep-10 (;=0.001;)
                    f32.mul
                    local.tee $l25
                    f32.sub
                    local.get $l24
                    f32.gt
                    br_if $B37
                    local.get $l31
                    local.get $l63
                    f32.lt
                    local.get $l26
                    local.get $l25
                    f32.add
                    local.get $l24
                    f32.gt
                    i32.and
                    br_if $B37
                    local.get $l24
                    f32.const 0x0p+0 (;=0;)
                    f32.eq
                    br_if $B37
                    local.get $l31
                    local.get $l63
                    f32.eq
                    local.get $l24
                    local.get $l26
                    f32.lt
                    i32.and
                    i32.eqz
                    br_if $B34
                  end
                  local.get $p6
                  local.get $l23
                  i32.store offset=8
                  local.get $l11
                  local.get $p8
                  f32.load
                  f32.store offset=152
                  local.get $l11
                  local.get $p8
                  f32.load offset=4
                  f32.store offset=156
                  local.get $l11
                  local.get $p8
                  f32.load offset=8
                  f32.store offset=160
                  local.get $l11
                  local.get $p8
                  f32.load offset=12
                  f32.store offset=164
                  local.get $l11
                  local.get $l14
                  f32.load
                  f32.store offset=168
                  local.get $l11
                  local.get $l13
                  f32.load
                  f32.store offset=172
                  local.get $l11
                  local.get $p8
                  f32.load offset=24
                  f32.store offset=176
                  local.get $l11
                  local.get $l20
                  f32.load
                  f32.store offset=180
                  local.get $l11
                  local.get $l21
                  f32.load
                  f32.store offset=184
                  local.get $l11
                  f32.load offset=120
                  local.set $l64
                  local.get $l11
                  f32.load offset=116
                  local.set $l65
                  local.get $l11
                  f32.load offset=112
                  local.set $l66
                  local.get $l18
                  br_if $B19
                  local.get $l31
                  local.set $l63
                  local.get $l24
                  local.set $l26
                end
                local.get $p5
                i32.const 1
                i32.add
                local.tee $p5
                i32.const 7
                i32.ne
                br_if $L33
              end
            end
            local.get $l15
            i32.const 1
            i32.add
            local.tee $l15
            local.get $p0
            i32.ne
            br_if $L18
            br $B17
          end
        end
        local.get $l24
        local.set $l26
      end
      local.get $p6
      i32.load offset=8
      i32.const -1
      i32.eq
      if $I38
        i32.const 0
        local.set $p8
        br $B0
      end
      local.get $p6
      local.get $l26
      f32.store offset=40
      local.get $p7
      local.get $l64
      f32.store offset=8
      local.get $p7
      local.get $l65
      f32.store offset=4
      local.get $p7
      local.get $l66
      f32.store
      local.get $p6
      i32.const 16
      i32.add
      local.get $p6
      i32.const 28
      i32.add
      local.get $l11
      i32.const 544
      i32.add
      local.get $p3
      local.get $p6
      f32.load offset=40
      local.get $l11
      i32.const 152
      i32.add
      call $f69957
      block $B39
        local.get $p9
        local.get $l22
        i32.or
        br_if $B39
        local.get $l66
        local.get $p3
        f32.load
        f32.mul
        local.get $l65
        local.get $p3
        f32.load offset=4
        f32.mul
        f32.add
        local.get $l64
        local.get $p3
        f32.load offset=8
        f32.mul
        f32.add
        f32.const 0x0p+0 (;=0;)
        f32.gt
        i32.eqz
        br_if $B39
        local.get $p6
        local.get $p6
        f32.load offset=28
        f32.neg
        f32.store offset=28
        local.get $p6
        i32.const 36
        i32.add
        local.tee $p8
        local.get $p8
        f32.load
        f32.neg
        f32.store
        local.get $p6
        i32.const 32
        i32.add
        local.tee $p8
        local.get $p8
        f32.load
        f32.neg
        f32.store
      end
      i32.const 1
      local.set $p8
      local.get $p6
      i32.load offset=8
      local.tee $p5
      i32.const -1
      i32.eq
      br_if $B0
      local.get $p3
      f32.load
      local.set $l24
      local.get $p3
      f32.load offset=4
      local.set $l25
      local.get $p3
      f32.load offset=8
      local.set $l28
      local.get $p6
      f32.load offset=40
      local.set $l26
      local.get $p2
      f32.load
      local.set $l27
      local.get $p2
      f32.load offset=4
      local.set $l29
      local.get $p2
      f32.load offset=8
      local.set $l33
      local.get $l11
      i32.const 0
      i32.store offset=92
      local.get $l11
      local.get $l33
      local.get $l26
      local.get $l28
      f32.mul
      local.tee $l28
      f32.add
      f32.store offset=88
      local.get $l11
      local.get $l29
      local.get $l26
      local.get $l25
      f32.mul
      local.tee $l25
      f32.add
      f32.store offset=84
      local.get $l11
      local.get $l27
      local.get $l26
      local.get $l24
      f32.mul
      local.tee $l26
      f32.add
      f32.store offset=80
      local.get $p2
      f32.load offset=12
      local.set $l24
      local.get $p2
      f32.load offset=16
      local.set $l27
      local.get $p2
      f32.load offset=20
      local.set $l29
      local.get $l11
      i32.const 0
      i32.store offset=76
      local.get $l11
      local.get $l28
      local.get $l29
      f32.add
      f32.store offset=72
      local.get $l11
      local.get $l25
      local.get $l27
      f32.add
      f32.store offset=68
      local.get $l11
      local.get $l26
      local.get $l24
      f32.add
      f32.store offset=64
      local.get $p1
      local.get $p5
      i32.const 36
      i32.mul
      i32.add
      local.tee $p3
      i64.load align=4
      local.set $l67
      local.get $p3
      f32.load offset=8
      local.set $l26
      local.get $l11
      i32.const 0
      i32.store offset=60
      local.get $l11
      local.get $l26
      f32.store offset=56
      local.get $l11
      local.get $l67
      i64.store offset=48
      local.get $p3
      i64.load offset=12 align=4
      local.set $l67
      local.get $p3
      f32.load offset=20
      local.set $l26
      local.get $l11
      i32.const 0
      i32.store offset=44
      local.get $l11
      local.get $l26
      f32.store offset=40
      local.get $l11
      local.get $l67
      i64.store offset=32
      local.get $p3
      i64.load offset=24 align=4
      local.set $l67
      local.get $p3
      f32.load offset=32
      local.set $l26
      local.get $l11
      i32.const 0
      i32.store offset=28
      local.get $l11
      local.get $l26
      f32.store offset=24
      local.get $l11
      local.get $l67
      i64.store offset=16
      local.get $l11
      local.get $l11
      i32.const 80
      i32.add
      local.get $l11
      i32.const -64
      i32.sub
      local.get $l11
      i32.const 48
      i32.add
      local.get $l11
      i32.const 32
      i32.add
      local.get $l11
      i32.const 16
      i32.add
      local.get $l11
      i32.const 112
      i32.add
      local.get $l11
      i32.const 96
      i32.add
      call $f69895
      local.get $l11
      i64.load offset=96
      local.set $l67
      local.get $p6
      local.get $l11
      f32.load offset=104
      f32.store offset=24
      local.get $p6
      local.get $l67
      i64.store offset=16 align=4
      local.get $p6
      i32.const 3
      i32.store16 offset=12
    end
    local.get $l11
    i32.const 560
    i32.add
    global.set $g0
    local.get $p8)
