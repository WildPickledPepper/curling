  (func $f70358 (type $t80) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 f32) (param $p7 i32) (param $p8 i32) (param $p9 f32) (result i32)
    (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 i32) (local $l47 i32) (local $l48 i32) (local $l49 i32) (local $l50 i32) (local $l51 i32) (local $l52 i32) (local $l53 i32) (local $l54 i32) (local $l55 i32)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $p2
    global.set $g0
    local.get $p1
    f32.load offset=20
    local.set $l10
    local.get $p1
    f32.load offset=16
    local.set $l11
    local.get $p2
    local.get $p1
    f32.load offset=24
    local.tee $l18
    local.get $p0
    f32.load offset=8
    local.tee $l13
    local.get $p1
    f32.load
    local.tee $l14
    local.get $l14
    f32.add
    local.tee $l15
    local.get $p1
    f32.load offset=8
    local.tee $l12
    f32.mul
    local.get $p1
    f32.load offset=12
    local.tee $l16
    local.get $l16
    f32.add
    local.tee $l17
    local.get $p1
    f32.load offset=4
    local.tee $l19
    f32.mul
    f32.sub
    f32.mul
    local.tee $l20
    f32.sub
    f32.store offset=36
    local.get $p2
    local.get $l10
    local.get $l13
    local.get $l12
    local.get $l17
    f32.mul
    local.get $l15
    local.get $l19
    f32.mul
    f32.add
    f32.mul
    local.tee $l12
    f32.sub
    f32.store offset=32
    local.get $p2
    local.get $l20
    local.get $l18
    f32.add
    f32.store offset=24
    local.get $p2
    local.get $l10
    local.get $l12
    f32.add
    f32.store offset=20
    local.get $p2
    local.get $l11
    local.get $l13
    local.get $l14
    local.get $l15
    f32.mul
    local.get $l16
    local.get $l17
    f32.mul
    f32.const -0x1p+0 (;=-1;)
    f32.add
    f32.add
    f32.mul
    local.tee $l10
    f32.sub
    f32.store offset=28
    local.get $p2
    local.get $l11
    local.get $l10
    f32.add
    f32.store offset=16
    local.get $p2
    local.get $p0
    f32.load offset=4
    local.get $p9
    f32.add
    f32.store offset=40
    local.get $p8
    i32.load16_u
    local.set $p0
    local.get $p5
    f32.load
    local.set $l10
    local.get $p5
    f32.load offset=4
    local.set $l11
    local.get $p2
    local.get $p5
    f32.load offset=8
    f32.neg
    f32.store offset=8
    local.get $p2
    local.get $l11
    f32.neg
    f32.store offset=4
    local.get $p2
    local.get $l10
    f32.neg
    f32.store
    i32.const 0
    local.set $p1
    local.get $p7
    i32.const 40
    i32.add
    local.set $l53
    local.get $p7
    i32.const 16
    i32.add
    local.set $l50
    local.get $p7
    i32.const 28
    i32.add
    local.set $p8
    local.get $p2
    i32.const 14
    i32.add
    local.set $l46
    global.get $g0
    i32.const 208
    i32.sub
    local.tee $p3
    global.set $g0
    local.get $p4
    f32.load offset=24
    local.get $p2
    i32.const 16
    i32.add
    local.tee $p5
    f32.load offset=24
    f32.add
    local.set $l13
    block $B0 (result i32)
      block $B1
        block $B2 (result f32)
          block $B3
            block $B4
              block $B5
                local.get $p0
                i32.const 16
                i32.and
                br_if $B5
                block $B6
                  local.get $p4
                  f32.load
                  local.tee $l11
                  local.get $p4
                  f32.load offset=12
                  local.tee $p9
                  f32.ne
                  br_if $B6
                  local.get $p4
                  f32.load offset=4
                  local.tee $l10
                  local.get $p4
                  f32.load offset=16
                  f32.ne
                  br_if $B6
                  local.get $p4
                  f32.load offset=8
                  local.tee $l12
                  local.get $p4
                  f32.load offset=20
                  f32.ne
                  br_if $B6
                  block $B7
                    local.get $p5
                    f32.load offset=12
                    local.get $p5
                    f32.load
                    local.tee $p9
                    f32.sub
                    local.tee $l14
                    local.get $l11
                    local.get $p9
                    f32.sub
                    local.tee $l11
                    f32.mul
                    local.get $p5
                    f32.load offset=16
                    local.get $p5
                    f32.load offset=4
                    local.tee $p9
                    f32.sub
                    local.tee $l15
                    local.get $l10
                    local.get $p9
                    f32.sub
                    local.tee $p9
                    f32.mul
                    f32.add
                    local.get $p5
                    f32.load offset=20
                    local.get $p5
                    f32.load offset=8
                    local.tee $l10
                    f32.sub
                    local.tee $l16
                    local.get $l12
                    local.get $l10
                    f32.sub
                    local.tee $l10
                    f32.mul
                    f32.add
                    local.tee $l12
                    f32.const 0x0p+0 (;=0;)
                    f32.le
                    br_if $B7
                    local.get $l14
                    local.get $l14
                    f32.mul
                    local.get $l15
                    local.get $l15
                    f32.mul
                    f32.add
                    local.get $l16
                    local.get $l16
                    f32.mul
                    f32.add
                    local.tee $l17
                    local.get $l12
                    f32.le
                    if $I8
                      local.get $l10
                      local.get $l16
                      f32.sub
                      local.set $l10
                      local.get $p9
                      local.get $l15
                      f32.sub
                      local.set $p9
                      local.get $l11
                      local.get $l14
                      f32.sub
                      local.set $l11
                      br $B7
                    end
                    local.get $l10
                    local.get $l16
                    local.get $l12
                    local.get $l17
                    f32.div
                    local.tee $l12
                    f32.mul
                    f32.sub
                    local.set $l10
                    local.get $p9
                    local.get $l15
                    local.get $l12
                    f32.mul
                    f32.sub
                    local.set $p9
                    local.get $l11
                    local.get $l14
                    local.get $l12
                    f32.mul
                    f32.sub
                    local.set $l11
                  end
                  local.get $l11
                  local.get $l11
                  f32.mul
                  local.get $p9
                  local.get $p9
                  f32.mul
                  f32.add
                  local.get $l10
                  local.get $l10
                  f32.mul
                  f32.add
                  local.get $l13
                  local.get $l13
                  f32.mul
                  f32.lt
                  i32.eqz
                  br_if $B5
                  br $B4
                end
                block $B9
                  local.get $p5
                  f32.load
                  local.tee $l10
                  local.get $p5
                  f32.load offset=12
                  local.tee $l14
                  f32.ne
                  if $I10
                    local.get $p5
                    f32.load offset=16
                    local.set $l15
                    local.get $p5
                    f32.load offset=4
                    local.set $l12
                    br $B9
                  end
                  local.get $p5
                  f32.load offset=4
                  local.tee $l12
                  local.get $p5
                  f32.load offset=16
                  local.tee $l15
                  f32.ne
                  br_if $B9
                  local.get $p5
                  f32.load offset=8
                  local.tee $l16
                  local.get $p5
                  f32.load offset=20
                  f32.ne
                  br_if $B9
                  block $B11
                    local.get $p9
                    local.get $l11
                    f32.sub
                    local.tee $l14
                    local.get $l10
                    local.get $l11
                    f32.sub
                    local.tee $l11
                    f32.mul
                    local.get $p4
                    f32.load offset=16
                    local.get $p4
                    f32.load offset=4
                    local.tee $p9
                    f32.sub
                    local.tee $l15
                    local.get $l12
                    local.get $p9
                    f32.sub
                    local.tee $p9
                    f32.mul
                    f32.add
                    local.get $p4
                    f32.load offset=20
                    local.get $p4
                    f32.load offset=8
                    local.tee $l10
                    f32.sub
                    local.tee $l12
                    local.get $l16
                    local.get $l10
                    f32.sub
                    local.tee $l10
                    f32.mul
                    f32.add
                    local.tee $l16
                    f32.const 0x0p+0 (;=0;)
                    f32.le
                    br_if $B11
                    local.get $l14
                    local.get $l14
                    f32.mul
                    local.get $l15
                    local.get $l15
                    f32.mul
                    f32.add
                    local.get $l12
                    local.get $l12
                    f32.mul
                    f32.add
                    local.tee $l17
                    local.get $l16
                    f32.le
                    if $I12
                      local.get $l10
                      local.get $l12
                      f32.sub
                      local.set $l10
                      local.get $p9
                      local.get $l15
                      f32.sub
                      local.set $p9
                      local.get $l11
                      local.get $l14
                      f32.sub
                      local.set $l11
                      br $B11
                    end
                    local.get $l10
                    local.get $l12
                    local.get $l16
                    local.get $l17
                    f32.div
                    local.tee $l16
                    f32.mul
                    f32.sub
                    local.set $l10
                    local.get $p9
                    local.get $l15
                    local.get $l16
                    f32.mul
                    f32.sub
                    local.set $p9
                    local.get $l11
                    local.get $l14
                    local.get $l16
                    f32.mul
                    f32.sub
                    local.set $l11
                  end
                  local.get $l11
                  local.get $l11
                  f32.mul
                  local.get $p9
                  local.get $p9
                  f32.mul
                  f32.add
                  local.get $l10
                  local.get $l10
                  f32.mul
                  f32.add
                  local.get $l13
                  local.get $l13
                  f32.mul
                  f32.lt
                  i32.eqz
                  br_if $B5
                  br $B4
                end
                local.get $p4
                f32.load offset=16
                local.set $l16
                local.get $p4
                f32.load offset=20
                local.set $l17
                local.get $p4
                f32.load offset=4
                local.set $l19
                local.get $p4
                f32.load offset=8
                local.set $l22
                local.get $p3
                local.get $p9
                local.get $l11
                f32.sub
                f32.store offset=80
                local.get $p3
                local.get $l17
                local.get $l22
                f32.sub
                f32.store offset=88
                local.get $p3
                local.get $l16
                local.get $l19
                f32.sub
                f32.store offset=84
                local.get $p5
                f32.load offset=20
                local.set $l11
                local.get $p5
                f32.load offset=8
                local.set $p9
                local.get $p3
                local.get $l15
                local.get $l12
                f32.sub
                f32.store offset=196
                local.get $p3
                local.get $l14
                local.get $l10
                f32.sub
                f32.store offset=192
                local.get $p3
                local.get $l11
                local.get $p9
                f32.sub
                f32.store offset=200
                local.get $p4
                local.get $p3
                i32.const 80
                i32.add
                local.get $p5
                local.get $p3
                i32.const 192
                i32.add
                i32.const 0
                i32.const 0
                call $f69892
                local.get $l13
                local.get $l13
                f32.mul
                f32.lt
                br_if $B4
              end
              local.get $p5
              f32.load offset=12
              local.tee $l26
              local.get $p5
              f32.load
              local.tee $l20
              f32.sub
              local.tee $l38
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              local.tee $l12
              local.get $p4
              f32.load offset=12
              local.tee $l11
              f32.add
              local.tee $l22
              local.get $l12
              local.get $p4
              f32.load
              local.tee $l23
              f32.add
              local.tee $l16
              f32.sub
              local.tee $l10
              local.get $p4
              f32.load offset=16
              local.tee $p9
              local.get $p5
              f32.load offset=16
              local.tee $l39
              local.get $p5
              f32.load offset=4
              local.tee $l31
              f32.sub
              local.tee $l40
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              local.tee $l14
              f32.sub
              local.tee $l32
              local.get $l14
              local.get $p4
              f32.load offset=4
              local.tee $l24
              f32.add
              local.tee $l17
              f32.sub
              local.tee $l18
              f32.mul
              local.get $l11
              local.get $l12
              f32.sub
              local.tee $l33
              local.get $l16
              f32.sub
              local.tee $l27
              local.get $l14
              local.get $p9
              f32.add
              local.tee $l34
              local.get $l17
              f32.sub
              local.tee $p9
              f32.mul
              f32.sub
              local.tee $l11
              local.get $l11
              f32.mul
              local.get $p9
              local.get $p4
              f32.load offset=20
              local.tee $l25
              local.get $p5
              f32.load offset=20
              local.tee $l41
              local.get $p5
              f32.load offset=8
              local.tee $l42
              f32.sub
              local.tee $l43
              f32.const 0x1p-1 (;=0.5;)
              f32.mul
              local.tee $l15
              f32.sub
              local.tee $l35
              local.get $l15
              local.get $p4
              f32.load offset=8
              local.tee $l28
              f32.add
              local.tee $l19
              f32.sub
              local.tee $l29
              f32.mul
              local.get $l18
              local.get $l15
              local.get $l25
              f32.add
              local.tee $l25
              local.get $l19
              f32.sub
              local.tee $l21
              f32.mul
              f32.sub
              local.tee $p9
              local.get $p9
              f32.mul
              local.get $l27
              local.get $l21
              f32.mul
              local.get $l10
              local.get $l29
              f32.mul
              f32.sub
              local.tee $l10
              local.get $l10
              f32.mul
              f32.add
              f32.add
              f32.sqrt
              local.tee $l18
              f32.const 0x0p+0 (;=0;)
              f32.gt
              if $I13
                local.get $l11
                f32.const 0x1p+0 (;=1;)
                local.get $l18
                f32.div
                local.tee $l18
                f32.mul
                local.set $l11
                local.get $l10
                local.get $l18
                f32.mul
                local.set $l10
                local.get $p9
                local.get $l18
                f32.mul
                local.set $p9
              end
              local.get $l23
              local.get $l12
              f32.sub
              local.set $l23
              local.get $l28
              local.get $l15
              f32.sub
              local.set $l18
              local.get $l24
              local.get $l14
              f32.sub
              local.set $l24
              local.get $l13
              local.get $l11
              f32.mul
              local.set $l12
              local.get $l13
              local.get $l10
              f32.mul
              local.set $l14
              local.get $l13
              local.get $p9
              f32.mul
              local.set $l15
              local.get $p9
              local.get $p2
              f32.load
              local.tee $l27
              f32.mul
              local.get $l10
              local.get $p2
              f32.load offset=4
              local.tee $l28
              f32.mul
              f32.add
              local.get $l11
              local.get $p2
              f32.load offset=8
              local.tee $l29
              f32.mul
              f32.add
              f32.const 0x0p+0 (;=0;)
              f32.ge
              i32.eqz
              br_if $B3
              local.get $l25
              local.get $l12
              f32.sub
              local.set $l21
              local.get $l34
              local.get $l14
              f32.sub
              local.set $l30
              local.get $l22
              local.get $l15
              f32.sub
              local.set $l36
              local.get $l35
              local.get $l12
              f32.sub
              local.set $l11
              local.get $l33
              local.get $l15
              f32.sub
              local.set $l10
              local.get $l18
              local.get $l12
              f32.sub
              local.set $l37
              local.get $l24
              local.get $l14
              f32.sub
              local.set $l44
              local.get $l23
              local.get $l15
              f32.sub
              local.set $l45
              local.get $l32
              local.get $l14
              f32.sub
              br $B2
            end
            local.get $l53
            i32.const 0
            i32.store
            local.get $p2
            f32.load
            local.set $l13
            local.get $p2
            f32.load offset=4
            local.set $l11
            local.get $p8
            local.get $p2
            f32.load offset=8
            f32.neg
            f32.store offset=8
            local.get $p8
            local.get $l11
            f32.neg
            f32.store offset=4
            local.get $p8
            local.get $l13
            f32.neg
            f32.store
            local.get $l46
            i32.const 2
            i32.store16
            br $B1
          end
          local.get $l25
          local.get $l12
          f32.add
          local.set $l37
          local.get $l34
          local.get $l14
          f32.add
          local.set $l44
          local.get $l22
          local.get $l15
          f32.add
          local.set $l45
          local.get $l35
          local.get $l12
          f32.add
          local.set $l11
          local.get $l33
          local.get $l15
          f32.add
          local.set $l10
          local.get $l18
          local.get $l12
          f32.add
          local.set $l21
          local.get $l24
          local.get $l14
          f32.add
          local.set $l30
          local.get $l23
          local.get $l15
          f32.add
          local.set $l36
          local.get $l32
          local.get $l14
          f32.add
        end
        local.set $p9
        local.get $p3
        local.get $l42
        local.get $l41
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l41
        f32.store offset=200
        local.get $p3
        local.get $l31
        local.get $l39
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l39
        f32.store offset=196
        local.get $p3
        local.get $l20
        local.get $l26
        f32.add
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l20
        f32.store offset=192
        block $B14
          block $B15
            local.get $l21
            local.get $l11
            f32.sub
            local.tee $l31
            local.get $l27
            local.get $l44
            local.get $p9
            f32.sub
            local.tee $l12
            f32.mul
            local.get $l28
            local.get $l45
            local.get $l10
            f32.sub
            local.tee $l14
            f32.mul
            f32.sub
            local.tee $l42
            f32.mul
            local.get $l36
            local.get $l10
            f32.sub
            local.tee $l21
            local.get $l28
            local.get $l37
            local.get $l11
            f32.sub
            local.tee $l15
            f32.mul
            local.get $l29
            local.get $l12
            f32.mul
            f32.sub
            local.tee $l36
            f32.mul
            local.get $l30
            local.get $p9
            f32.sub
            local.tee $l30
            local.get $l29
            local.get $l14
            f32.mul
            local.get $l27
            local.get $l15
            f32.mul
            f32.sub
            local.tee $l37
            f32.mul
            f32.add
            f32.add
            local.tee $l26
            f32.const 0x1.4f8b58p-17 (;=1e-05;)
            f32.lt
            br_if $B15
            local.get $l36
            local.get $l20
            local.get $l10
            f32.sub
            local.tee $l10
            f32.mul
            local.get $l37
            local.get $l39
            local.get $p9
            f32.sub
            local.tee $p9
            f32.mul
            f32.add
            local.get $l42
            local.get $l41
            local.get $l11
            f32.sub
            local.tee $l11
            f32.mul
            f32.add
            local.tee $l20
            f32.const 0x0p+0 (;=0;)
            f32.lt
            br_if $B15
            local.get $l20
            local.get $l26
            f32.gt
            br_if $B15
            local.get $l29
            local.get $l30
            local.get $l10
            f32.mul
            local.get $l21
            local.get $p9
            f32.mul
            f32.sub
            local.tee $l20
            f32.mul
            local.get $l27
            local.get $l31
            local.get $p9
            f32.mul
            local.get $l30
            local.get $l11
            f32.mul
            f32.sub
            local.tee $p9
            f32.mul
            local.get $l28
            local.get $l21
            local.get $l11
            f32.mul
            local.get $l31
            local.get $l10
            f32.mul
            f32.sub
            local.tee $l10
            f32.mul
            f32.add
            f32.add
            local.tee $l11
            f32.const 0x0p+0 (;=0;)
            f32.lt
            br_if $B15
            local.get $l11
            local.get $l26
            f32.gt
            br_if $B15
            f32.const 0x1p+0 (;=1;)
            local.get $l26
            f32.div
            local.get $l15
            local.get $l20
            f32.mul
            local.get $l14
            local.get $p9
            f32.mul
            local.get $l12
            local.get $l10
            f32.mul
            f32.add
            f32.add
            f32.mul
            local.tee $l11
            f32.const 0x0p+0 (;=0;)
            f32.ge
            i32.eqz
            br_if $B15
            local.get $p6
            local.get $l11
            f32.gt
            br_if $B14
          end
          local.get $p3
          i32.const 188
          i32.add
          local.tee $l47
          local.get $l13
          f32.store
          local.get $p3
          local.get $l19
          f32.store offset=184
          local.get $p3
          local.get $l17
          f32.store offset=180
          local.get $p3
          i32.const 176
          i32.add
          local.tee $l51
          local.get $l16
          f32.store
          local.get $p3
          local.get $l18
          f32.store offset=172
          local.get $p3
          local.get $l24
          f32.store offset=168
          local.get $p3
          i32.const 160
          i32.add
          local.tee $l48
          local.get $l13
          f32.store
          local.get $p3
          local.get $l19
          f32.store offset=156
          local.get $p3
          local.get $l17
          f32.store offset=152
          local.get $p3
          i32.const 148
          i32.add
          local.tee $l52
          local.get $l16
          f32.store
          local.get $p3
          local.get $l25
          f32.store offset=144
          local.get $p3
          local.get $l34
          f32.store offset=140
          local.get $p3
          i32.const 132
          i32.add
          local.tee $l49
          local.get $l13
          f32.store
          local.get $p3
          local.get $l25
          f32.store offset=128
          local.get $p3
          local.get $l34
          f32.store offset=124
          local.get $p3
          i32.const 120
          i32.add
          local.tee $l54
          local.get $l22
          f32.store
          local.get $p3
          local.get $l35
          f32.store offset=116
          local.get $p3
          local.get $l32
          f32.store offset=112
          local.get $p3
          local.get $l35
          f32.store offset=100
          local.get $p3
          local.get $l32
          f32.store offset=96
          local.get $p3
          local.get $l23
          f32.store offset=164
          local.get $p3
          local.get $l22
          f32.store offset=136
          local.get $p3
          local.get $l33
          f32.store offset=108
          local.get $p3
          local.get $l13
          f32.store offset=104
          local.get $p3
          local.get $l33
          f32.store offset=92
          local.get $p3
          local.get $l18
          f32.store offset=88
          local.get $p3
          local.get $l24
          f32.store offset=84
          local.get $p3
          local.get $l23
          f32.store offset=80
          local.get $p3
          i32.const 192
          i32.add
          local.get $p2
          local.get $p3
          i32.const 80
          i32.add
          local.get $p3
          i32.const 80
          i32.add
          i32.const 12
          i32.or
          local.get $l13
          local.get $p3
          i32.const -64
          i32.sub
          call $f70336
          local.set $l55
          local.get $p3
          f32.load offset=64
          local.set $l13
          local.get $p3
          i32.const 192
          i32.add
          local.get $p2
          local.get $p3
          i32.const 108
          i32.add
          local.get $l54
          local.get $l49
          f32.load
          local.get $p3
          i32.const -64
          i32.sub
          call $f70336
          local.set $l49
          local.get $p3
          f32.load offset=64
          local.set $l11
          local.get $p3
          i32.const 192
          i32.add
          local.get $p2
          local.get $p3
          i32.const 136
          i32.add
          local.get $l52
          local.get $l48
          f32.load
          local.get $p3
          i32.const -64
          i32.sub
          call $f70336
          local.set $l48
          local.get $p3
          f32.load offset=64
          local.set $p9
          local.get $p3
          i32.const 192
          i32.add
          local.get $p2
          local.get $p3
          i32.const 164
          i32.add
          local.get $l51
          local.get $l47
          f32.load
          local.get $p3
          i32.const -64
          i32.sub
          call $f70336
          local.set $l47
          local.get $p6
          local.get $l13
          local.get $p6
          local.get $l13
          f32.ge
          i32.eqz
          local.get $l13
          f32.const 0x0p+0 (;=0;)
          f32.ge
          i32.eqz
          local.get $l55
          i32.const 1
          i32.xor
          i32.or
          i32.or
          local.tee $l51
          select
          local.tee $l13
          local.get $l11
          local.get $l11
          local.get $l13
          f32.le
          i32.eqz
          local.get $l11
          f32.const 0x0p+0 (;=0;)
          f32.ge
          i32.eqz
          local.get $l49
          i32.const 1
          i32.xor
          i32.or
          i32.or
          local.tee $l52
          select
          local.tee $l13
          local.get $p9
          local.get $p9
          local.get $l13
          f32.le
          i32.eqz
          local.get $p9
          f32.const 0x0p+0 (;=0;)
          f32.ge
          i32.eqz
          local.get $l48
          i32.const 1
          i32.xor
          i32.or
          i32.or
          local.tee $l48
          select
          local.tee $l11
          local.get $p3
          f32.load offset=64
          local.tee $l13
          local.get $l11
          local.get $l13
          f32.ge
          i32.eqz
          local.get $l13
          f32.const 0x0p+0 (;=0;)
          f32.ge
          i32.eqz
          local.get $l47
          i32.const 1
          i32.xor
          i32.or
          i32.or
          local.tee $l49
          select
          local.set $l11
          local.get $l51
          i32.const 1
          i32.ne
          br_if $B14
          local.get $l52
          i32.eqz
          br_if $B14
          local.get $l48
          i32.eqz
          br_if $B14
          i32.const 0
          local.get $l49
          br_if $B0
          drop
        end
        local.get $l46
        i32.const 0
        i32.store16
        block $B16
          local.get $p0
          i32.const 3
          i32.and
          i32.eqz
          br_if $B16
          local.get $p4
          f32.load offset=8
          local.set $l13
          local.get $p2
          f32.load offset=8
          local.set $p9
          local.get $p4
          f32.load offset=4
          local.set $l10
          local.get $p2
          f32.load offset=4
          local.set $l12
          local.get $p3
          local.get $p4
          f32.load
          local.get $l11
          local.get $p2
          f32.load
          f32.mul
          local.tee $l14
          f32.sub
          local.tee $l15
          f32.store offset=80
          local.get $p3
          local.get $l10
          local.get $l11
          local.get $l12
          f32.mul
          local.tee $l12
          f32.sub
          local.tee $l10
          f32.store offset=84
          local.get $p3
          local.get $l13
          local.get $l11
          local.get $p9
          f32.mul
          local.tee $p9
          f32.sub
          local.tee $l13
          f32.store offset=88
          local.get $p4
          f32.load offset=12
          local.set $l16
          local.get $p4
          f32.load offset=16
          local.set $l17
          local.get $p3
          local.get $p4
          f32.load offset=20
          local.get $p9
          f32.sub
          local.get $l13
          f32.sub
          local.tee $l19
          f32.store offset=72
          local.get $p3
          local.get $l17
          local.get $l12
          f32.sub
          local.get $l10
          f32.sub
          local.tee $l12
          f32.store offset=68
          local.get $p3
          local.get $l16
          local.get $l14
          f32.sub
          local.get $l15
          f32.sub
          local.tee $l14
          f32.store offset=64
          local.get $p3
          local.get $l43
          f32.store offset=56
          local.get $p3
          local.get $l40
          f32.store offset=52
          local.get $p3
          local.get $l38
          f32.store offset=48
          local.get $p3
          i32.const 32
          i32.add
          local.get $p3
          i32.const 16
          i32.add
          local.get $p3
          i32.const 80
          i32.add
          local.get $p3
          i32.const -64
          i32.sub
          local.get $p5
          local.get $p3
          i32.const 48
          i32.add
          call $f70240
          local.get $p0
          i32.const 2
          i32.and
          if $I17
            local.get $p3
            f32.load offset=16
            local.set $l10
            local.get $p3
            f32.load offset=32
            local.set $l15
            local.get $p3
            f32.load offset=20
            local.set $p9
            local.get $p3
            f32.load offset=36
            local.set $l16
            local.get $p8
            local.get $p3
            f32.load offset=40
            local.get $p3
            f32.load offset=24
            f32.sub
            local.tee $l13
            f32.store offset=8
            local.get $p8
            local.get $l16
            local.get $p9
            f32.sub
            local.tee $p9
            f32.store offset=4
            local.get $p8
            local.get $l15
            local.get $l10
            f32.sub
            local.tee $l10
            f32.store
            local.get $l10
            local.get $l10
            f32.mul
            local.get $p9
            local.get $p9
            f32.mul
            f32.add
            local.get $l13
            local.get $l13
            f32.mul
            f32.add
            f32.sqrt
            local.tee $l15
            f32.const 0x0p+0 (;=0;)
            f32.gt
            if $I18
              local.get $p8
              local.get $l13
              f32.const 0x1p+0 (;=1;)
              local.get $l15
              f32.div
              local.tee $l16
              f32.mul
              f32.store offset=8
              local.get $p8
              local.get $p9
              local.get $l16
              f32.mul
              f32.store offset=4
              local.get $p8
              local.get $l10
              local.get $l16
              f32.mul
              f32.store
            end
            block $B19
              local.get $l15
              f32.const 0x1.0624dep-10 (;=0.001;)
              f32.lt
              i32.eqz
              br_if $B19
              local.get $p8
              local.get $l38
              local.get $l12
              f32.mul
              local.get $l40
              local.get $l14
              f32.mul
              f32.sub
              local.tee $l13
              f32.store offset=8
              local.get $p8
              local.get $l43
              local.get $l14
              f32.mul
              local.get $l38
              local.get $l19
              f32.mul
              f32.sub
              local.tee $p9
              f32.store offset=4
              local.get $p8
              local.get $l40
              local.get $l19
              f32.mul
              local.get $l43
              local.get $l12
              f32.mul
              f32.sub
              local.tee $l10
              f32.store
              local.get $l13
              local.get $l13
              f32.mul
              local.get $l10
              local.get $l10
              f32.mul
              local.get $p9
              local.get $p9
              f32.mul
              f32.add
              f32.add
              f32.sqrt
              local.tee $l12
              f32.const 0x0p+0 (;=0;)
              f32.gt
              if $I20
                local.get $p8
                local.get $l13
                f32.const 0x1p+0 (;=1;)
                local.get $l12
                f32.div
                local.tee $l14
                f32.mul
                f32.store offset=8
                local.get $p8
                local.get $p9
                local.get $l14
                f32.mul
                f32.store offset=4
                local.get $p8
                local.get $l10
                local.get $l14
                f32.mul
                f32.store
              end
              local.get $l12
              f32.const 0x1.0624dep-10 (;=0.001;)
              f32.lt
              i32.eqz
              br_if $B19
              local.get $p4
              f32.load
              local.set $l13
              local.get $p4
              f32.load offset=12
              local.set $p9
              local.get $p4
              f32.load offset=4
              local.set $l10
              local.get $p4
              f32.load offset=16
              local.set $l12
              local.get $p3
              local.get $p4
              f32.load offset=20
              local.get $p4
              f32.load offset=8
              f32.sub
              f32.store offset=8
              local.get $p3
              local.get $l12
              local.get $l10
              f32.sub
              f32.store offset=4
              local.get $p3
              local.get $p9
              local.get $l13
              f32.sub
              f32.store
              local.get $p3
              i32.const 32
              i32.add
              local.get $p3
              i32.const 16
              i32.add
              local.get $p4
              local.get $p3
              local.get $p5
              local.get $p3
              i32.const 48
              i32.add
              call $f70240
              local.get $p3
              f32.load offset=16
              local.set $l10
              local.get $p3
              f32.load offset=32
              local.set $l12
              local.get $p3
              f32.load offset=20
              local.set $p9
              local.get $p3
              f32.load offset=36
              local.set $l14
              local.get $p8
              local.get $p3
              f32.load offset=40
              local.get $p3
              f32.load offset=24
              f32.sub
              local.tee $l13
              f32.store offset=8
              local.get $p8
              local.get $l14
              local.get $p9
              f32.sub
              local.tee $p9
              f32.store offset=4
              local.get $p8
              local.get $l12
              local.get $l10
              f32.sub
              local.tee $l10
              f32.store
              local.get $l10
              local.get $l10
              f32.mul
              local.get $p9
              local.get $p9
              f32.mul
              f32.add
              local.get $l13
              local.get $l13
              f32.mul
              f32.add
              f32.sqrt
              local.tee $l12
              f32.const 0x0p+0 (;=0;)
              f32.gt
              i32.eqz
              br_if $B19
              local.get $p8
              local.get $l13
              f32.const 0x1p+0 (;=1;)
              local.get $l12
              f32.div
              local.tee $l12
              f32.mul
              f32.store offset=8
              local.get $p8
              local.get $p9
              local.get $l12
              f32.mul
              f32.store offset=4
              local.get $p8
              local.get $l10
              local.get $l12
              f32.mul
              f32.store
            end
            local.get $l46
            local.get $l46
            i32.load16_u
            i32.const 2
            i32.or
            i32.store16
          end
          local.get $p0
          i32.const 1
          i32.and
          i32.eqz
          br_if $B16
          local.get $p3
          f32.load offset=32
          local.set $l12
          local.get $p3
          f32.load offset=16
          local.set $l14
          local.get $p3
          f32.load offset=36
          local.set $l15
          local.get $p3
          f32.load offset=20
          local.set $l16
          local.get $l50
          f32.const 0x1p+0 (;=1;)
          local.get $p5
          f32.load offset=24
          local.tee $l13
          local.get $p4
          f32.load offset=24
          local.tee $p9
          f32.add
          f32.div
          local.tee $l10
          local.get $l13
          local.get $p3
          f32.load offset=40
          f32.mul
          local.get $p9
          local.get $p3
          f32.load offset=24
          f32.mul
          f32.add
          f32.mul
          f32.store offset=8
          local.get $l50
          local.get $l10
          local.get $l13
          local.get $l15
          f32.mul
          local.get $p9
          local.get $l16
          f32.mul
          f32.add
          f32.mul
          f32.store offset=4
          local.get $l50
          local.get $l10
          local.get $l13
          local.get $l12
          f32.mul
          local.get $p9
          local.get $l14
          f32.mul
          f32.add
          f32.mul
          f32.store
          local.get $l46
          local.get $l46
          i32.load16_u
          i32.const 1
          i32.or
          i32.store16
        end
        local.get $l53
        local.get $l11
        f32.store
      end
      i32.const 1
    end
    local.set $l47
    local.get $p3
    i32.const 208
    i32.add
    global.set $g0
    block $B21
      local.get $l47
      i32.eqz
      br_if $B21
      local.get $p7
      local.get $p2
      i32.load16_u offset=14
      local.tee $p5
      i32.store16 offset=12
      i32.const 1
      local.set $p1
      local.get $p0
      i32.const 512
      i32.and
      i32.eqz
      br_if $B21
      local.get $p7
      f32.load offset=40
      f32.const 0x0p+0 (;=0;)
      f32.ne
      br_if $B21
      local.get $p7
      local.get $p5
      i32.const 1
      i32.or
      i32.store16 offset=12
      global.get $g0
      i32.const 48
      i32.sub
      local.tee $p0
      global.set $g0
      local.get $p4
      i32.const 16
      i32.add
      local.tee $p3
      f32.load
      local.set $p6
      local.get $p4
      f32.load
      local.set $p9
      local.get $p4
      f32.load offset=12
      local.set $l10
      local.get $p4
      f32.load offset=4
      local.set $l11
      local.get $p0
      local.get $p4
      i32.const 20
      i32.add
      local.tee $p5
      f32.load
      local.get $p4
      f32.load offset=8
      f32.sub
      f32.store offset=40
      local.get $p0
      local.get $p6
      local.get $l11
      f32.sub
      f32.store offset=36
      local.get $p0
      local.get $l10
      local.get $p9
      f32.sub
      f32.store offset=32
      local.get $p2
      i32.const 16
      i32.add
      local.tee $p1
      i32.const 16
      i32.add
      local.tee $p8
      f32.load
      local.set $p6
      local.get $p1
      f32.load
      local.set $p9
      local.get $p1
      f32.load offset=12
      local.set $l10
      local.get $p1
      f32.load offset=4
      local.set $l11
      local.get $p0
      local.get $p1
      i32.const 20
      i32.add
      local.tee $l46
      f32.load
      local.get $p1
      f32.load offset=8
      f32.sub
      f32.store offset=24
      local.get $p0
      local.get $p6
      local.get $l11
      f32.sub
      f32.store offset=20
      local.get $p0
      local.get $l10
      local.get $p9
      f32.sub
      f32.store offset=16
      local.get $p4
      local.get $p0
      i32.const 32
      i32.add
      local.get $p1
      local.get $p0
      i32.const 16
      i32.add
      local.get $p0
      i32.const 12
      i32.add
      local.get $p0
      i32.const 8
      i32.add
      call $f69892
      drop
      local.get $p4
      f32.load
      local.tee $p9
      local.get $p0
      f32.load offset=12
      local.tee $p6
      local.get $p4
      f32.load offset=12
      local.get $p9
      f32.sub
      f32.mul
      f32.add
      local.get $p1
      f32.load
      local.tee $l10
      local.get $p0
      f32.load offset=8
      local.tee $p9
      local.get $p1
      f32.load offset=12
      local.get $l10
      f32.sub
      f32.mul
      f32.add
      local.tee $l14
      f32.sub
      local.tee $l11
      local.get $l11
      f32.mul
      local.get $p4
      f32.load offset=4
      local.tee $l10
      local.get $p6
      local.get $p3
      f32.load
      local.get $l10
      f32.sub
      f32.mul
      f32.add
      local.get $p1
      f32.load offset=4
      local.tee $l10
      local.get $p9
      local.get $p8
      f32.load
      local.get $l10
      f32.sub
      f32.mul
      f32.add
      local.tee $l15
      f32.sub
      local.tee $l12
      local.get $l12
      f32.mul
      f32.add
      local.get $p4
      f32.load offset=8
      local.tee $l10
      local.get $p6
      local.get $p5
      f32.load
      local.get $l10
      f32.sub
      f32.mul
      f32.add
      local.get $p1
      f32.load offset=8
      local.tee $p6
      local.get $p9
      local.get $l46
      f32.load
      local.get $p6
      f32.sub
      f32.mul
      f32.add
      local.tee $l16
      f32.sub
      local.tee $p6
      local.get $p6
      f32.mul
      f32.add
      local.tee $p9
      f32.sqrt
      local.set $l13
      local.get $p1
      f32.load offset=24
      local.set $l17
      local.get $p4
      f32.load offset=24
      local.set $l18
      local.get $p7
      block $B22 (result f32)
        local.get $p9
        f32.const 0x1.0c6f7ap-20 (;=1e-06;)
        f32.lt
        if $I23
          f32.const 0x0p+0 (;=0;)
          local.set $p6
          f32.const 0x0p+0 (;=0;)
          local.set $l10
          f32.const 0x1p+0 (;=1;)
          br $B22
        end
        local.get $p6
        f32.const 0x1p+0 (;=1;)
        local.get $l13
        f32.div
        local.tee $p9
        f32.mul
        local.set $l10
        local.get $l12
        local.get $p9
        f32.mul
        local.set $p6
        local.get $l11
        local.get $p9
        f32.mul
      end
      local.tee $p9
      f32.store offset=28
      local.get $p7
      local.get $l10
      f32.store offset=36
      local.get $p7
      local.get $p6
      f32.store offset=32
      local.get $p7
      local.get $l13
      local.get $l18
      local.get $l17
      f32.add
      f32.sub
      f32.store offset=40
      local.get $p7
      local.get $l16
      local.get $l10
      local.get $p1
      f32.load offset=24
      local.tee $l11
      f32.mul
      f32.add
      f32.store offset=24
      local.get $p7
      local.get $l15
      local.get $p6
      local.get $l11
      f32.mul
      f32.add
      f32.store offset=20
      local.get $p7
      local.get $l14
      local.get $p9
      local.get $l11
      f32.mul
      f32.add
      f32.store offset=16
      local.get $p0
      i32.const 48
      i32.add
      global.set $g0
      i32.const 1
      local.set $p1
    end
    local.get $p2
    i32.const 48
    i32.add
    global.set $g0
    local.get $p1)
