  (func $f71174 (type $t523) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 f32) (param $p8 f32) (param $p9 i32) (param $p10 i32) (param $p11 i32) (param $p12 i32)
    (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32)
    global.get $g0
    i32.const 832
    i32.sub
    local.tee $l15
    global.set $g0
    block $B0
      local.get $p4
      i32.eqz
      br_if $B0
      loop $L1
        local.get $p1
        local.get $l19
        i32.const 80
        i32.mul
        i32.add
        local.set $l25
        block $B2 (result i32)
          local.get $l19
          if $I3
            local.get $l25
            i32.const 78
            i32.add
            local.set $l24
            local.get $l19
            local.set $l13
            loop $L4
              local.get $p0
              local.get $l13
              i32.const 2
              i32.shl
              i32.add
              local.get $l24
              i32.load16_u
              local.get $p0
              local.get $l13
              i32.const 1
              i32.sub
              local.tee $l14
              i32.const 2
              i32.shl
              i32.add
              i32.load
              local.tee $l16
              i32.load16_u offset=78
              i32.ge_u
              br_if $B2
              drop
              local.get $p0
              local.get $l13
              i32.const 2
              i32.shl
              i32.add
              local.get $l16
              i32.store
              local.get $l14
              local.tee $l13
              br_if $L4
            end
          end
          local.get $p0
        end
        local.get $l25
        i32.store
        local.get $l19
        i32.const 1
        i32.add
        local.tee $l19
        local.get $p4
        i32.ne
        br_if $L1
      end
      local.get $p4
      i32.eqz
      br_if $B0
      local.get $p4
      i32.const 1
      i32.and
      local.set $l24
      i32.const 0
      local.set $l13
      local.get $p4
      i32.const 1
      i32.ne
      if $I5
        local.get $p4
        i32.const -2
        i32.and
        local.set $l16
        loop $L6
          f32.const 0x0p+0 (;=0;)
          local.set $l31
          f32.const 0x0p+0 (;=0;)
          local.set $l32
          local.get $p1
          local.get $l13
          i32.const 80
          i32.mul
          i32.add
          local.tee $l14
          i32.load8_u offset=76
          i32.const 8
          i32.and
          if $I7
            local.get $l14
            f32.load offset=12
            local.set $l32
          end
          local.get $l14
          local.get $l32
          f32.store offset=72
          local.get $p1
          local.get $l13
          i32.const 1
          i32.or
          i32.const 80
          i32.mul
          i32.add
          local.tee $l14
          i32.load8_u offset=76
          i32.const 8
          i32.and
          if $I8
            local.get $l14
            f32.load offset=12
            local.set $l31
          end
          local.get $l14
          local.get $l31
          f32.store offset=72
          local.get $l13
          i32.const 2
          i32.add
          local.set $l13
          local.get $l16
          i32.const 2
          i32.sub
          local.tee $l16
          br_if $L6
        end
      end
      local.get $l24
      i32.eqz
      br_if $B0
      f32.const 0x0p+0 (;=0;)
      local.set $l31
      local.get $p1
      local.get $l13
      i32.const 80
      i32.mul
      i32.add
      local.tee $l13
      i32.load8_u offset=76
      i32.const 8
      i32.and
      if $I9
        local.get $l13
        f32.load offset=12
        local.set $l31
      end
      local.get $l13
      local.get $l31
      f32.store offset=72
    end
    local.get $p4
    if $I10
      local.get $p6
      f32.load offset=32
      local.set $l37
      local.get $p6
      f32.load offset=28
      local.set $l38
      local.get $p6
      f32.load offset=20
      local.set $l39
      local.get $p6
      f32.load offset=16
      local.set $l40
      local.get $p5
      f32.load offset=32
      local.set $l41
      local.get $p5
      f32.load offset=28
      local.set $l42
      local.get $p5
      f32.load offset=20
      local.set $l43
      local.get $p5
      f32.load offset=16
      local.set $l44
      local.get $p6
      f32.load offset=24
      local.set $l45
      local.get $p6
      f32.load offset=12
      local.set $l46
      local.get $p6
      f32.load offset=8
      local.set $l47
      local.get $p6
      f32.load offset=4
      local.set $l48
      local.get $p6
      f32.load
      local.set $l49
      local.get $p5
      f32.load offset=24
      local.set $l50
      local.get $p5
      f32.load offset=12
      local.set $l51
      local.get $p5
      f32.load offset=8
      local.set $l52
      local.get $p5
      f32.load offset=4
      local.set $l53
      local.get $p5
      f32.load
      local.set $l54
      i32.const 0
      local.set $l14
      loop $L11
        local.get $p0
        local.get $l14
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l13
        f32.load offset=56
        local.set $l31
        local.get $l13
        f32.load offset=52
        local.set $l32
        local.get $l13
        f32.load offset=48
        local.set $l33
        local.get $l13
        f32.load offset=24
        local.set $l34
        local.get $l13
        f32.load offset=20
        local.set $l35
        local.get $l13
        f32.load offset=16
        local.set $l36
        local.get $p2
        local.get $l14
        i32.const 4
        i32.shl
        local.tee $l16
        i32.add
        local.tee $l13
        i32.const 0
        i32.store offset=12
        local.get $l13
        local.get $l52
        local.get $l36
        f32.mul
        local.get $l43
        local.get $l35
        f32.mul
        f32.add
        local.get $l41
        local.get $l34
        f32.mul
        f32.add
        f32.store offset=8
        local.get $l13
        local.get $l53
        local.get $l36
        f32.mul
        local.get $l44
        local.get $l35
        f32.mul
        f32.add
        local.get $l42
        local.get $l34
        f32.mul
        f32.add
        f32.store offset=4
        local.get $l13
        local.get $l54
        local.get $l36
        f32.mul
        local.get $l51
        local.get $l35
        f32.mul
        f32.add
        local.get $l50
        local.get $l34
        f32.mul
        f32.add
        f32.store
        local.get $p3
        local.get $l16
        i32.add
        local.tee $l13
        i32.const 0
        i32.store offset=12
        local.get $l13
        local.get $l47
        local.get $l33
        f32.mul
        local.get $l39
        local.get $l32
        f32.mul
        f32.add
        local.get $l37
        local.get $l31
        f32.mul
        f32.add
        f32.store offset=8
        local.get $l13
        local.get $l48
        local.get $l33
        f32.mul
        local.get $l40
        local.get $l32
        f32.mul
        f32.add
        local.get $l38
        local.get $l31
        f32.mul
        f32.add
        f32.store offset=4
        local.get $l13
        local.get $l49
        local.get $l33
        f32.mul
        local.get $l46
        local.get $l32
        f32.mul
        f32.add
        local.get $l45
        local.get $l31
        f32.mul
        f32.add
        f32.store
        local.get $l14
        i32.const 1
        i32.add
        local.tee $l14
        local.get $p4
        i32.ne
        br_if $L11
      end
    end
    block $B12
      local.get $p10
      br_if $B12
      local.get $l15
      local.get $p9
      f32.load
      local.get $p7
      f32.mul
      f32.store
      local.get $l15
      local.get $p9
      f32.load offset=8
      local.get $p8
      f32.mul
      f32.store offset=16
      local.get $l15
      local.get $p9
      f32.load offset=4
      f32.store offset=32
      local.get $l15
      local.get $p9
      f32.load offset=12
      f32.store offset=48
      local.get $p4
      i32.eqz
      br_if $B12
      loop $L13
        local.get $p4
        local.get $l21
        local.tee $l17
        i32.const 1
        i32.add
        local.tee $l13
        local.get $p4
        local.get $l13
        i32.gt_u
        select
        local.tee $l13
        i32.const 1
        i32.sub
        local.set $l14
        local.get $p0
        local.get $l17
        i32.const 2
        i32.shl
        i32.add
        local.tee $l27
        i32.load
        local.tee $p9
        i32.load16_u offset=78
        local.tee $l16
        i32.const 8
        i32.shr_u
        local.set $l28
        loop $L14
          block $B15
            local.get $p4
            local.get $l21
            local.tee $l20
            i32.const 1
            i32.add
            local.tee $l21
            i32.le_u
            if $I16
              local.get $l14
              local.set $l20
              local.get $l13
              local.set $l21
              br $B15
            end
            local.get $p0
            local.get $l21
            i32.const 2
            i32.shl
            i32.add
            i32.load
            i32.load8_u offset=79
            local.get $l28
            i32.eq
            br_if $L14
          end
        end
        block $B17
          block $B18
            block $B19
              block $B20
                local.get $l28
                i32.const 1
                i32.sub
                br_table $B18 $B17 $B17 $B19 $B17 $B17 $B17 $B20 $B17
              end
              local.get $p12
              i32.eqz
              br_if $B17
            end
            block $B21
              local.get $l20
              local.get $l17
              local.tee $l13
              i32.lt_u
              br_if $B21
              local.get $l16
              i32.const 255
              i32.and
              br_if $B21
              local.get $l20
              i32.const 1
              i32.add
              local.set $l14
              loop $L22
                local.get $l13
                local.get $l20
                i32.eq
                if $I23
                  local.get $l14
                  local.set $l13
                  br $B21
                end
                local.get $p0
                local.get $l13
                i32.const 1
                i32.add
                local.tee $l13
                i32.const 2
                i32.shl
                i32.add
                i32.load
                i32.load8_u offset=78
                i32.eqz
                br_if $L22
              end
            end
            block $B24
              local.get $l21
              local.get $l17
              i32.sub
              local.tee $l29
              i32.eqz
              br_if $B24
              local.get $l13
              local.get $l17
              i32.sub
              local.set $l26
              local.get $p3
              local.get $l17
              i32.const 4
              i32.shl
              local.tee $l13
              i32.add
              local.set $p1
              local.get $p2
              local.get $l13
              i32.add
              local.set $p5
              i32.const 0
              local.set $p10
              loop $L25
                local.get $p9
                f32.load offset=56
                local.set $l44
                local.get $p9
                f32.load offset=52
                local.set $l45
                local.get $p9
                f32.load offset=40
                local.set $l32
                local.get $p9
                f32.load offset=36
                local.set $l33
                local.get $p9
                f32.load offset=28
                local.set $l46
                local.get $p9
                f32.load offset=24
                local.set $l47
                local.get $p9
                f32.load offset=20
                local.set $l48
                local.get $p1
                local.get $p10
                i32.const 4
                i32.shl
                local.tee $l18
                i32.add
                local.tee $l22
                f32.load offset=12
                local.set $l52
                local.get $l22
                f32.load offset=8
                local.set $l38
                local.get $l22
                f32.load offset=4
                local.set $l39
                local.get $l22
                f32.load
                local.set $l40
                local.get $p5
                local.get $l18
                i32.add
                local.tee $l23
                f32.load offset=12
                local.set $l53
                local.get $l23
                f32.load offset=8
                local.set $l41
                local.get $l23
                f32.load offset=4
                local.set $l42
                local.get $l23
                f32.load
                local.set $l43
                local.get $p9
                f32.load offset=48
                local.set $l49
                local.get $p9
                f32.load offset=32
                local.set $l34
                local.get $p9
                f32.load offset=16
                local.set $l50
                local.get $p9
                f32.load offset=12
                local.set $l51
                local.get $p9
                f32.load offset=8
                local.set $l35
                local.get $p9
                f32.load offset=4
                local.set $l36
                local.get $p9
                f32.load
                local.set $l37
                local.get $p10
                local.get $l26
                local.get $p10
                local.get $l26
                i32.lt_u
                local.tee $l30
                select
                if $I26
                  local.get $l26
                  local.get $p10
                  local.get $p10
                  local.get $l26
                  i32.gt_u
                  select
                  local.set $p6
                  i32.const 0
                  local.set $l16
                  loop $L27
                    local.get $l52
                    local.get $l34
                    local.get $l16
                    i32.const 4
                    i32.shl
                    local.tee $l13
                    local.get $l15
                    i32.const 736
                    i32.add
                    i32.add
                    local.tee $l14
                    f32.load
                    f32.mul
                    local.get $l37
                    local.get $l15
                    i32.const 352
                    i32.add
                    local.get $l13
                    i32.add
                    local.tee $l24
                    f32.load
                    f32.mul
                    f32.add
                    local.get $l40
                    local.get $l15
                    i32.const 640
                    i32.add
                    local.get $l13
                    i32.add
                    local.tee $l19
                    f32.load
                    f32.mul
                    local.get $l43
                    local.get $l15
                    i32.const 256
                    i32.add
                    local.get $l13
                    i32.add
                    local.tee $l25
                    f32.load
                    f32.mul
                    f32.add
                    f32.add
                    local.get $l33
                    local.get $l14
                    f32.load offset=4
                    f32.mul
                    local.get $l36
                    local.get $l24
                    f32.load offset=4
                    f32.mul
                    f32.add
                    local.get $l39
                    local.get $l19
                    f32.load offset=4
                    f32.mul
                    local.get $l42
                    local.get $l25
                    f32.load offset=4
                    f32.mul
                    f32.add
                    f32.add
                    f32.add
                    local.get $l32
                    local.get $l14
                    f32.load offset=8
                    f32.mul
                    local.get $l35
                    local.get $l24
                    f32.load offset=8
                    f32.mul
                    f32.add
                    local.get $l38
                    local.get $l19
                    f32.load offset=8
                    f32.mul
                    local.get $l41
                    local.get $l25
                    f32.load offset=8
                    f32.mul
                    f32.add
                    f32.add
                    f32.add
                    local.tee $l31
                    local.get $p1
                    local.get $l13
                    i32.add
                    local.tee $l14
                    f32.load offset=12
                    f32.mul
                    f32.sub
                    local.set $l52
                    local.get $l38
                    local.get $l31
                    local.get $l14
                    f32.load offset=8
                    f32.mul
                    f32.sub
                    local.set $l38
                    local.get $l39
                    local.get $l31
                    local.get $l14
                    f32.load offset=4
                    f32.mul
                    f32.sub
                    local.set $l39
                    local.get $l40
                    local.get $l31
                    local.get $l14
                    f32.load
                    f32.mul
                    f32.sub
                    local.set $l40
                    local.get $l53
                    local.get $l31
                    local.get $p5
                    local.get $l13
                    i32.add
                    local.tee $l14
                    f32.load offset=12
                    f32.mul
                    f32.sub
                    local.set $l53
                    local.get $l41
                    local.get $l31
                    local.get $l14
                    f32.load offset=8
                    f32.mul
                    f32.sub
                    local.set $l41
                    local.get $l42
                    local.get $l31
                    local.get $l14
                    f32.load offset=4
                    f32.mul
                    f32.sub
                    local.set $l42
                    local.get $l43
                    local.get $l31
                    local.get $l14
                    f32.load
                    f32.mul
                    f32.sub
                    local.set $l43
                    local.get $l44
                    local.get $l31
                    local.get $l15
                    i32.const 448
                    i32.add
                    local.get $l13
                    i32.add
                    local.tee $l14
                    f32.load offset=8
                    f32.mul
                    f32.sub
                    local.set $l44
                    local.get $l45
                    local.get $l31
                    local.get $l14
                    f32.load offset=4
                    f32.mul
                    f32.sub
                    local.set $l45
                    local.get $l49
                    local.get $l31
                    local.get $l14
                    f32.load
                    f32.mul
                    f32.sub
                    local.set $l49
                    local.get $l32
                    local.get $l31
                    local.get $l15
                    i32.const 544
                    i32.add
                    local.get $l13
                    i32.add
                    local.tee $l14
                    f32.load offset=8
                    f32.mul
                    f32.sub
                    local.set $l32
                    local.get $l33
                    local.get $l31
                    local.get $l14
                    f32.load offset=4
                    f32.mul
                    f32.sub
                    local.set $l33
                    local.get $l34
                    local.get $l31
                    local.get $l14
                    f32.load
                    f32.mul
                    f32.sub
                    local.set $l34
                    local.get $l46
                    local.get $l31
                    local.get $l15
                    i32.const -64
                    i32.sub
                    local.get $l13
                    i32.add
                    local.tee $l14
                    f32.load offset=12
                    f32.mul
                    f32.sub
                    local.set $l46
                    local.get $l47
                    local.get $l31
                    local.get $l14
                    f32.load offset=8
                    f32.mul
                    f32.sub
                    local.set $l47
                    local.get $l48
                    local.get $l31
                    local.get $l14
                    f32.load offset=4
                    f32.mul
                    f32.sub
                    local.set $l48
                    local.get $l50
                    local.get $l31
                    local.get $l14
                    f32.load
                    f32.mul
                    f32.sub
                    local.set $l50
                    local.get $l51
                    local.get $l15
                    i32.const 160
                    i32.add
                    local.get $l13
                    i32.add
                    local.tee $l13
                    f32.load offset=12
                    local.get $l31
                    f32.mul
                    f32.sub
                    local.set $l51
                    local.get $l35
                    local.get $l13
                    f32.load offset=8
                    local.get $l31
                    f32.mul
                    f32.sub
                    local.set $l35
                    local.get $l36
                    local.get $l13
                    f32.load offset=4
                    local.get $l31
                    f32.mul
                    f32.sub
                    local.set $l36
                    local.get $l37
                    local.get $l13
                    f32.load
                    local.get $l31
                    f32.mul
                    f32.sub
                    local.set $l37
                    local.get $l16
                    i32.const 1
                    i32.add
                    local.tee $l16
                    local.get $p6
                    i32.ne
                    br_if $L27
                  end
                end
                local.get $p9
                local.get $l51
                f32.store offset=12
                local.get $p9
                local.get $l35
                f32.store offset=8
                local.get $p9
                local.get $l36
                f32.store offset=4
                local.get $p9
                local.get $l37
                f32.store
                local.get $l27
                local.get $p10
                i32.const 2
                i32.shl
                i32.add
                local.tee $p6
                i32.load
                local.tee $l13
                local.get $l46
                f32.store offset=28
                local.get $l13
                local.get $l50
                f32.store offset=16
                local.get $l13
                local.get $l47
                f32.store offset=24
                local.get $l13
                local.get $l48
                f32.store offset=20
                local.get $p6
                i32.load
                local.tee $l13
                local.get $l34
                f32.store offset=32
                local.get $l13
                local.get $l32
                f32.store offset=40
                local.get $l13
                local.get $l33
                f32.store offset=36
                local.get $p6
                i32.load
                local.tee $l13
                local.get $l49
                f32.store offset=48
                local.get $l13
                local.get $l44
                f32.store offset=56
                local.get $l13
                local.get $l45
                f32.store offset=52
                local.get $l23
                local.get $l53
                f32.store offset=12
                local.get $l23
                local.get $l41
                f32.store offset=8
                local.get $l23
                local.get $l42
                f32.store offset=4
                local.get $l23
                local.get $l43
                f32.store
                local.get $l22
                local.get $l52
                f32.store offset=12
                local.get $l22
                local.get $l38
                f32.store offset=8
                local.get $l22
                local.get $l39
                f32.store offset=4
                local.get $l22
                local.get $l40
                f32.store
                local.get $l30
                if $I28
                  local.get $l15
                  i32.const 160
                  i32.add
                  local.get $l18
                  i32.add
                  local.tee $l13
                  local.get $l51
                  f32.store offset=12
                  local.get $l13
                  local.get $l35
                  f32.store offset=8
                  local.get $l13
                  local.get $l36
                  f32.store offset=4
                  local.get $l13
                  local.get $l37
                  f32.store
                  local.get $l15
                  i32.const -64
                  i32.sub
                  local.get $l18
                  i32.add
                  local.tee $l13
                  local.get $l46
                  f32.store offset=12
                  local.get $l13
                  local.get $l47
                  f32.store offset=8
                  local.get $l13
                  local.get $l48
                  f32.store offset=4
                  local.get $l13
                  local.get $l50
                  f32.store
                  local.get $l15
                  i32.const 544
                  i32.add
                  local.get $l18
                  i32.add
                  local.tee $l13
                  i32.const 0
                  i32.store offset=12
                  local.get $l13
                  local.get $l32
                  f32.store offset=8
                  local.get $l13
                  local.get $l33
                  f32.store offset=4
                  local.get $l13
                  local.get $l34
                  f32.store
                  local.get $l15
                  i32.const 448
                  i32.add
                  local.get $l18
                  i32.add
                  local.tee $l13
                  i32.const 0
                  i32.store offset=12
                  local.get $l13
                  local.get $l44
                  f32.store offset=8
                  local.get $l13
                  local.get $l45
                  f32.store offset=4
                  local.get $l13
                  local.get $l49
                  f32.store
                  local.get $l15
                  f32.load
                  local.set $l31
                  local.get $l15
                  f32.load offset=16
                  local.set $l44
                  local.get $l15
                  f32.load offset=32
                  local.set $l45
                  local.get $l15
                  f32.load offset=48
                  local.set $l46
                  local.get $l15
                  i32.const 736
                  i32.add
                  local.get $l18
                  i32.add
                  local.tee $l13
                  i32.const 0
                  i32.store offset=12
                  local.get $l15
                  i32.const 640
                  i32.add
                  local.get $l18
                  i32.add
                  local.tee $l14
                  i32.const 0
                  i32.store offset=12
                  local.get $l15
                  i32.const 352
                  i32.add
                  local.get $l18
                  i32.add
                  local.tee $l16
                  f32.const 0x1p+0 (;=1;)
                  local.get $l35
                  local.get $l35
                  local.get $l31
                  f32.mul
                  local.tee $l47
                  f32.mul
                  local.get $l32
                  local.get $l32
                  local.get $l44
                  f32.mul
                  local.tee $l35
                  f32.mul
                  f32.add
                  local.get $l41
                  local.get $l41
                  local.get $l45
                  f32.mul
                  local.tee $l32
                  f32.mul
                  local.get $l38
                  local.get $l38
                  local.get $l46
                  f32.mul
                  local.tee $l41
                  f32.mul
                  f32.add
                  f32.add
                  local.get $l37
                  local.get $l37
                  local.get $l31
                  f32.mul
                  local.tee $l38
                  f32.mul
                  local.get $l34
                  local.get $l34
                  local.get $l44
                  f32.mul
                  local.tee $l37
                  f32.mul
                  f32.add
                  local.get $l43
                  local.get $l43
                  local.get $l45
                  f32.mul
                  local.tee $l34
                  f32.mul
                  local.get $l40
                  local.get $l40
                  local.get $l46
                  f32.mul
                  local.tee $l43
                  f32.mul
                  f32.add
                  f32.add
                  local.get $l36
                  local.get $l36
                  local.get $l31
                  f32.mul
                  local.tee $l40
                  f32.mul
                  local.get $l33
                  local.get $l33
                  local.get $l44
                  f32.mul
                  local.tee $l36
                  f32.mul
                  f32.add
                  local.get $l42
                  local.get $l42
                  local.get $l45
                  f32.mul
                  local.tee $l33
                  f32.mul
                  local.get $l39
                  local.get $l39
                  local.get $l46
                  f32.mul
                  local.tee $l42
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.add
                  local.tee $l31
                  f32.div
                  f32.const 0x0p+0 (;=0;)
                  local.get $l31
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  select
                  local.tee $l31
                  f32.const 0x0p+0 (;=0;)
                  f32.mul
                  local.tee $l39
                  f32.store offset=12
                  local.get $l16
                  local.get $l47
                  local.get $l31
                  f32.mul
                  f32.store offset=8
                  local.get $l16
                  local.get $l40
                  local.get $l31
                  f32.mul
                  f32.store offset=4
                  local.get $l16
                  local.get $l38
                  local.get $l31
                  f32.mul
                  f32.store
                  local.get $l15
                  i32.const 256
                  i32.add
                  local.get $l18
                  i32.add
                  local.tee $l16
                  local.get $l34
                  local.get $l31
                  f32.mul
                  f32.store
                  local.get $l16
                  local.get $l33
                  local.get $l31
                  f32.mul
                  f32.store offset=4
                  local.get $l16
                  local.get $l32
                  local.get $l31
                  f32.mul
                  f32.store offset=8
                  local.get $l16
                  local.get $l39
                  f32.store offset=12
                  local.get $l13
                  local.get $l37
                  local.get $l31
                  f32.mul
                  f32.store
                  local.get $l13
                  local.get $l36
                  local.get $l31
                  f32.mul
                  f32.store offset=4
                  local.get $l13
                  local.get $l35
                  local.get $l31
                  f32.mul
                  f32.store offset=8
                  local.get $l14
                  local.get $l43
                  local.get $l31
                  f32.mul
                  f32.store
                  local.get $l14
                  local.get $l42
                  local.get $l31
                  f32.mul
                  f32.store offset=4
                  local.get $l14
                  local.get $l41
                  local.get $l31
                  f32.mul
                  f32.store offset=8
                end
                local.get $p10
                i32.const 1
                i32.add
                local.tee $p10
                local.get $l29
                i32.eq
                br_if $B24
                local.get $l27
                local.get $p10
                i32.const 2
                i32.shl
                i32.add
                i32.load
                local.set $p9
                br $L25
              end
              unreachable
            end
            local.get $l28
            i32.const 1
            i32.ne
            br_if $B17
          end
          local.get $p11
          i32.eqz
          br_if $B17
          block $B29
            local.get $l20
            local.get $l17
            local.tee $l13
            i32.lt_u
            br_if $B29
            local.get $l20
            i32.const 1
            i32.add
            local.set $l16
            loop $L30
              local.get $p0
              local.get $l13
              i32.const 2
              i32.shl
              i32.add
              i32.load
              i32.load8_u offset=78
              i32.const 2
              i32.eq
              br_if $B29
              local.get $l13
              local.get $l20
              i32.ne
              local.set $l14
              local.get $l13
              i32.const 1
              i32.add
              local.set $l13
              local.get $l14
              br_if $L30
            end
            local.get $l16
            local.set $l13
          end
          local.get $l20
          local.get $l13
          i32.const 2
          i32.add
          i32.eq
          if $I31
            local.get $p0
            local.get $l13
            i32.const 2
            i32.shl
            i32.add
            local.get $p2
            local.get $l13
            i32.const 4
            i32.shl
            local.tee $l13
            i32.add
            local.get $p3
            local.get $l13
            i32.add
            local.get $l15
            call $f71175
          end
          local.get $l27
          local.get $p2
          local.get $l17
          i32.const 4
          i32.shl
          local.tee $l13
          i32.add
          local.get $p3
          local.get $l13
          i32.add
          local.get $l15
          call $f71175
        end
        local.get $p4
        local.get $l21
        i32.gt_u
        br_if $L13
      end
    end
    local.get $l15
    i32.const 832
    i32.add
    global.set $g0)