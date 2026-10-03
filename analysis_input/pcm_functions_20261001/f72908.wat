  (func $f72908 (type $t5) (param $p0 i32) (result i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i32) (local $l34 i32) (local $l35 i32) (local $l36 i32) (local $l37 i32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32)
    global.get $g0
    i32.const 208
    i32.sub
    local.tee $l7
    global.set $g0
    local.get $p0
    i32.load offset=4
    local.tee $l1
    i32.load offset=8
    local.tee $l6
    i32.const 8
    local.get $l6
    i32.const 8
    i32.gt_u
    select
    i32.const 12
    i32.mul
    local.tee $l6
    if $I0
      call $f69753
      local.tee $l1
      local.get $l6
      i32.const 3217836
      i32.const 3217483
      i32.const 1845
      local.get $l1
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
      local.set $l17
      local.get $p0
      i32.load offset=4
      local.set $l1
    end
    local.get $l1
    i32.load
    local.set $l6
    local.get $l1
    i32.load offset=4
    local.set $l10
    local.get $l1
    i32.load offset=8
    local.set $l4
    block $B1
      block $B2
        local.get $l1
        i32.load8_u offset=37
        i32.const 1
        i32.and
        if $I3
          local.get $l6
          local.set $l1
          local.get $l7
          i32.const 172
          i32.add
          local.set $l2
          local.get $l7
          i32.const 192
          i32.add
          local.set $l5
          local.get $l7
          i32.const 176
          i32.add
          local.set $l9
          local.get $p0
          local.get $l4
          i32.const 12
          i32.mul
          local.tee $l6
          if $I4 (result i32)
            call $f69753
            local.tee $l8
            local.get $l6
            i32.const 3216437
            i32.const 3215482
            i32.const 137
            local.get $l8
            i32.load
            i32.load offset=8
            call_indirect $__indirect_function_table (type $t9)
          else
            i32.const 0
          end
          local.tee $l3
          i32.store offset=28
          block $B5
            local.get $l4
            i32.eqz
            if $I6
              f32.const -0x1.fffffep+125 (;=-8.50706e+37;)
              local.set $l40
              f32.const 0x1.fffffep+125 (;=8.50706e+37;)
              local.set $l38
              f32.const 0x1.fffffep+125 (;=8.50706e+37;)
              local.set $l45
              f32.const 0x1.fffffep+125 (;=8.50706e+37;)
              local.set $l44
              f32.const -0x1.fffffep+125 (;=-8.50706e+37;)
              local.set $l43
              f32.const -0x1.fffffep+125 (;=-8.50706e+37;)
              local.set $l46
              br $B5
            end
            f32.const 0x1.fffffep+125 (;=8.50706e+37;)
            local.set $l44
            f32.const -0x1.fffffep+125 (;=-8.50706e+37;)
            local.set $l46
            local.get $l10
            local.set $l6
            i32.const 1
            local.set $l8
            f32.const -0x1.fffffep+125 (;=-8.50706e+37;)
            local.set $l43
            f32.const -0x1.fffffep+125 (;=-8.50706e+37;)
            local.set $l40
            f32.const 0x1.fffffep+125 (;=8.50706e+37;)
            local.set $l45
            f32.const 0x1.fffffep+125 (;=8.50706e+37;)
            local.set $l38
            loop $L7
              local.get $l46
              local.get $l6
              f32.load offset=8
              local.tee $l39
              local.get $l39
              local.get $l46
              f32.lt
              select
              local.set $l46
              local.get $l43
              local.get $l6
              f32.load offset=4
              local.tee $l41
              local.get $l41
              local.get $l43
              f32.lt
              select
              local.set $l43
              local.get $l40
              local.get $l6
              f32.load
              local.tee $l42
              local.get $l40
              local.get $l42
              f32.gt
              select
              local.set $l40
              local.get $l44
              local.get $l39
              local.get $l39
              local.get $l44
              f32.gt
              select
              local.set $l44
              local.get $l45
              local.get $l41
              local.get $l41
              local.get $l45
              f32.gt
              select
              local.set $l45
              local.get $l38
              local.get $l42
              local.get $l38
              local.get $l42
              f32.lt
              select
              local.set $l38
              local.get $l4
              local.get $l8
              i32.eq
              br_if $B5
              local.get $l1
              local.get $l6
              i32.add
              local.set $l6
              local.get $l8
              i32.const 1
              i32.add
              local.set $l8
              br $L7
            end
            unreachable
          end
          local.get $p0
          local.get $l44
          local.get $l46
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l39
          f32.store offset=24
          local.get $p0
          local.get $l45
          local.get $l43
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l41
          f32.store offset=20
          local.get $p0
          local.get $l38
          local.get $l40
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          local.tee $l42
          f32.store offset=16
          local.get $p0
          local.get $l4
          local.get $l4
          if $I8 (result i32)
            local.get $l10
            f32.load
            local.set $l40
            local.get $l10
            f32.load offset=4
            local.set $l38
            local.get $l3
            local.get $l10
            f32.load offset=8
            local.get $l39
            f32.sub
            f32.store offset=8
            local.get $l3
            local.get $l38
            local.get $l41
            f32.sub
            f32.store offset=4
            local.get $l3
            local.get $l40
            local.get $l42
            f32.sub
            f32.store
            i32.const 1
            local.set $l6
            local.get $l4
            i32.const 1
            i32.ne
            if $I9
              loop $L10
                local.get $l1
                local.get $l10
                i32.add
                local.tee $l10
                f32.load
                local.set $l39
                local.get $l10
                f32.load offset=4
                local.set $l41
                local.get $p0
                f32.load offset=16
                local.set $l42
                local.get $p0
                f32.load offset=20
                local.set $l40
                local.get $p0
                i32.load offset=28
                local.get $l6
                i32.const 12
                i32.mul
                i32.add
                local.tee $l8
                local.get $l10
                f32.load offset=8
                local.get $p0
                f32.load offset=24
                f32.sub
                f32.store offset=8
                local.get $l8
                local.get $l41
                local.get $l40
                f32.sub
                f32.store offset=4
                local.get $l8
                local.get $l39
                local.get $l42
                f32.sub
                f32.store
                local.get $l6
                i32.const 1
                i32.add
                local.tee $l6
                local.get $l4
                i32.ne
                br_if $L10
              end
            end
            local.get $p0
            i32.load offset=28
          else
            local.get $l3
          end
          i32.const 12
          local.get $l2
          local.get $l17
          local.get $l5
          local.get $l9
          call $f72873
          br_if $B2
          i32.const 3
          local.set $l8
          local.get $l17
          i32.eqz
          br_if $B1
          call $f69753
          local.tee $l1
          local.get $l17
          local.get $l1
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
          br $B1
        end
        local.get $p0
        local.get $l4
        local.get $l10
        local.get $l6
        local.get $l7
        i32.const 172
        i32.add
        local.get $l17
        local.get $l7
        i32.const 192
        i32.add
        local.get $l7
        i32.const 176
        i32.add
        call $f72873
        br_if $B2
        i32.const 3
        local.set $l8
        local.get $l17
        i32.eqz
        br_if $B1
        call $f69753
        local.tee $l1
        local.get $l17
        local.get $l1
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
        br $B1
      end
      block $B11 (result i32)
        local.get $l7
        i32.load offset=172
        local.set $l22
        local.get $l7
        i32.const 12
        i32.add
        local.set $l27
        local.get $l7
        i32.const 8
        i32.add
        local.set $l28
        f32.const 0x0p+0 (;=0;)
        local.set $l46
        local.get $l7
        i32.const 96
        i32.add
        local.tee $l5
        local.get $l17
        local.tee $l2
        f32.load
        f32.store
        local.get $l5
        local.get $l2
        f32.load offset=4
        f32.store offset=4
        local.get $l2
        f32.load offset=8
        local.set $l38
        local.get $l5
        i32.const 0
        i32.store offset=12
        local.get $l5
        local.get $l38
        f32.store offset=8
        local.get $l7
        i32.const 16
        i32.add
        local.tee $l9
        local.get $l2
        f32.load
        f32.store
        local.get $l9
        local.get $l2
        f32.load offset=4
        f32.store offset=4
        local.get $l2
        f32.load offset=8
        local.set $l38
        local.get $l9
        i32.const 0
        i32.store offset=12
        local.get $l9
        local.get $l38
        f32.store offset=8
        local.get $l5
        local.get $l2
        f32.load
        f32.store offset=24
        local.get $l5
        i32.const 28
        i32.add
        local.tee $l15
        local.get $l2
        f32.load offset=4
        f32.store
        local.get $l2
        f32.load offset=8
        local.set $l38
        local.get $l5
        i32.const 36
        i32.add
        local.tee $l19
        i32.const 0
        i32.store
        local.get $l5
        i32.const 32
        i32.add
        local.tee $l20
        local.get $l38
        f32.store
        local.get $l9
        local.get $l2
        f32.load
        f32.store offset=24
        local.get $l9
        i32.const 28
        i32.add
        local.tee $l12
        local.get $l2
        f32.load offset=4
        f32.store
        local.get $l2
        f32.load offset=8
        local.set $l38
        local.get $l9
        i32.const 36
        i32.add
        local.tee $l13
        i32.const 0
        i32.store
        local.get $l9
        i32.const 32
        i32.add
        local.tee $l14
        local.get $l38
        f32.store
        local.get $l5
        local.get $l2
        f32.load
        f32.store offset=48
        local.get $l5
        i32.const 52
        i32.add
        local.tee $l18
        local.get $l2
        f32.load offset=4
        f32.store
        local.get $l2
        f32.load offset=8
        local.set $l38
        local.get $l5
        i32.const 60
        i32.add
        local.tee $l16
        i32.const 0
        i32.store
        local.get $l5
        i32.const 56
        i32.add
        local.tee $l21
        local.get $l38
        f32.store
        local.get $l9
        local.get $l2
        f32.load
        f32.store offset=48
        local.get $l9
        i32.const 52
        i32.add
        local.tee $l23
        local.get $l2
        f32.load offset=4
        f32.store
        local.get $l2
        f32.load offset=8
        local.set $l38
        local.get $l9
        i32.const 60
        i32.add
        local.tee $l24
        i32.const 0
        i32.store
        local.get $l9
        i32.const 56
        i32.add
        local.tee $l25
        local.get $l38
        f32.store
        i32.const 1
        local.set $l11
        local.get $l2
        f32.load offset=8
        local.set $l43
        local.get $l2
        f32.load offset=4
        local.set $l45
        local.get $l2
        f32.load
        local.set $l44
        block $B12
          local.get $l22
          i32.const 1
          i32.le_u
          if $I13
            local.get $l44
            local.set $l39
            local.get $l45
            local.set $l41
            local.get $l43
            local.set $l42
            br $B12
          end
          local.get $l9
          i32.const 48
          i32.add
          local.set $l26
          local.get $l5
          i32.const 48
          i32.add
          local.set $l29
          local.get $l9
          i32.const 24
          i32.add
          local.set $l30
          local.get $l5
          i32.const 24
          i32.add
          local.set $l31
          local.get $l9
          i32.const 12
          i32.add
          local.set $l32
          local.get $l9
          i32.const 8
          i32.add
          local.set $l33
          local.get $l9
          i32.const 4
          i32.add
          local.set $l34
          local.get $l5
          i32.const 12
          i32.add
          local.set $l35
          local.get $l5
          i32.const 8
          i32.add
          local.set $l36
          local.get $l5
          i32.const 4
          i32.add
          local.set $l37
          local.get $l43
          local.set $l42
          local.get $l45
          local.set $l41
          local.get $l44
          local.set $l39
          loop $L14
            block $B15
              block $B16
                local.get $l44
                local.get $l2
                local.get $l11
                i32.const 12
                i32.mul
                i32.add
                local.tee $l3
                f32.load
                local.tee $l38
                f32.lt
                if $I17
                  local.get $l9
                  local.set $l8
                  local.get $l34
                  local.set $l10
                  local.get $l33
                  local.set $l6
                  local.get $l32
                  local.set $l4
                  local.get $l39
                  local.set $l40
                  local.get $l38
                  local.set $l44
                  br $B16
                end
                local.get $l5
                local.set $l8
                local.get $l37
                local.set $l10
                local.get $l36
                local.set $l6
                local.get $l35
                local.set $l4
                local.get $l38
                local.set $l40
                local.get $l38
                local.get $l39
                f32.lt
                i32.eqz
                br_if $B15
              end
              local.get $l8
              local.get $l38
              f32.store
              local.get $l10
              local.get $l3
              f32.load offset=4
              f32.store
              local.get $l6
              local.get $l3
              f32.load offset=8
              f32.store
              local.get $l4
              local.get $l11
              i32.store
              local.get $l40
              local.set $l39
            end
            local.get $l3
            i32.const 4
            i32.add
            local.set $l8
            block $B18
              block $B19
                local.get $l45
                local.get $l3
                f32.load offset=4
                local.tee $l38
                f32.lt
                if $I20
                  local.get $l30
                  local.set $l10
                  local.get $l12
                  local.set $l6
                  local.get $l14
                  local.set $l4
                  local.get $l13
                  local.set $l1
                  local.get $l41
                  local.set $l40
                  local.get $l38
                  local.set $l45
                  br $B19
                end
                local.get $l31
                local.set $l10
                local.get $l15
                local.set $l6
                local.get $l20
                local.set $l4
                local.get $l19
                local.set $l1
                local.get $l38
                local.set $l40
                local.get $l38
                local.get $l41
                f32.lt
                i32.eqz
                br_if $B18
              end
              local.get $l10
              local.get $l3
              f32.load
              f32.store
              local.get $l6
              local.get $l8
              f32.load
              f32.store
              local.get $l4
              local.get $l3
              f32.load offset=8
              f32.store
              local.get $l1
              local.get $l11
              i32.store
              local.get $l40
              local.set $l41
            end
            block $B21
              block $B22
                local.get $l43
                local.get $l3
                f32.load offset=8
                local.tee $l38
                f32.lt
                if $I23
                  local.get $l26
                  local.set $l10
                  local.get $l23
                  local.set $l6
                  local.get $l25
                  local.set $l4
                  local.get $l24
                  local.set $l1
                  local.get $l42
                  local.set $l40
                  local.get $l38
                  local.set $l43
                  br $B22
                end
                local.get $l29
                local.set $l10
                local.get $l18
                local.set $l6
                local.get $l21
                local.set $l4
                local.get $l16
                local.set $l1
                local.get $l38
                local.set $l40
                local.get $l38
                local.get $l42
                f32.lt
                i32.eqz
                br_if $B21
              end
              local.get $l10
              local.get $l3
              f32.load
              f32.store
              local.get $l6
              local.get $l8
              f32.load
              f32.store
              local.get $l4
              local.get $l3
              f32.load offset=8
              f32.store
              local.get $l1
              local.get $l11
              i32.store
              local.get $l40
              local.set $l42
            end
            local.get $l11
            i32.const 1
            i32.add
            local.tee $l11
            local.get $l22
            i32.ne
            br_if $L14
          end
        end
        local.get $l27
        local.get $l43
        local.get $l44
        local.get $l39
        f32.sub
        local.get $l45
        f32.add
        local.get $l41
        f32.sub
        f32.add
        local.get $l42
        f32.sub
        f32.const 0x1p-1 (;=0.5;)
        f32.mul
        local.tee $l39
        f32.const 0x1.8p-22 (;=3.57628e-07;)
        f32.mul
        local.tee $l38
        f32.const 0x1.8p-22 (;=3.57628e-07;)
        local.get $l38
        f32.const 0x1.8p-22 (;=3.57628e-07;)
        f32.gt
        select
        f32.store
        local.get $l28
        local.get $l39
        local.get $p0
        i32.load offset=8
        f32.load offset=4
        local.tee $l38
        f32.mul
        local.tee $l39
        local.get $l38
        local.get $l38
        local.get $l39
        f32.lt
        select
        f32.store
        local.get $l5
        i32.const 2
        local.get $l9
        f32.load offset=28
        local.get $l5
        f32.load offset=28
        f32.sub
        local.tee $l38
        local.get $l9
        f32.load
        local.get $l5
        f32.load
        f32.sub
        local.tee $l39
        f32.const 0x0p+0 (;=0;)
        local.get $l39
        f32.const 0x0p+0 (;=0;)
        f32.gt
        select
        local.tee $l39
        f32.gt
        local.tee $l3
        local.get $l9
        f32.load offset=56
        local.get $l5
        f32.load offset=56
        f32.sub
        local.get $l38
        local.get $l39
        local.get $l3
        select
        f32.gt
        select
        i32.const 24
        i32.mul
        local.tee $l11
        i32.add
        local.tee $l3
        f32.load
        local.get $l9
        local.get $l11
        i32.add
        local.tee $l11
        f32.load
        local.tee $l55
        f32.sub
        local.tee $l42
        local.get $l42
        f32.mul
        local.get $l3
        f32.load offset=4
        local.get $l11
        f32.load offset=4
        local.tee $l56
        f32.sub
        local.tee $l40
        local.get $l40
        f32.mul
        f32.add
        local.get $l3
        f32.load offset=8
        local.get $l11
        f32.load offset=8
        local.tee $l57
        f32.sub
        local.tee $l43
        local.get $l43
        f32.mul
        f32.add
        f32.sqrt
        local.tee $l38
        f32.const 0x0p+0 (;=0;)
        f32.gt
        if $I24
          local.get $l43
          f32.const 0x1p+0 (;=1;)
          local.get $l38
          f32.div
          local.tee $l38
          f32.mul
          local.set $l43
          local.get $l42
          local.get $l38
          f32.mul
          local.set $l42
          local.get $l40
          local.get $l38
          f32.mul
          local.set $l40
        end
        i32.const 0
        local.set $l8
        local.get $l22
        if $I25
          i32.const 0
          local.set $l3
          loop $L26
            local.get $l48
            local.get $l42
            local.get $l2
            local.get $l3
            i32.const 12
            i32.mul
            i32.add
            local.tee $l11
            f32.load offset=4
            local.tee $l52
            local.get $l56
            f32.sub
            local.tee $l39
            f32.mul
            local.get $l40
            local.get $l11
            f32.load
            local.tee $l53
            local.get $l55
            f32.sub
            local.tee $l41
            f32.mul
            f32.sub
            local.tee $l38
            local.get $l38
            f32.mul
            local.get $l40
            local.get $l11
            f32.load offset=8
            local.tee $l54
            local.get $l57
            f32.sub
            local.tee $l45
            f32.mul
            local.get $l43
            local.get $l39
            f32.mul
            f32.sub
            local.tee $l39
            local.get $l39
            f32.mul
            local.get $l43
            local.get $l41
            f32.mul
            local.get $l42
            local.get $l45
            f32.mul
            f32.sub
            local.tee $l41
            local.get $l41
            f32.mul
            f32.add
            f32.add
            local.tee $l45
            f32.lt
            if $I27
              local.get $l53
              local.set $l49
              local.get $l52
              local.set $l50
              local.get $l54
              local.set $l51
              local.get $l41
              local.set $l46
              local.get $l38
              local.set $l47
              local.get $l45
              local.set $l48
              local.get $l3
              local.set $l8
              local.get $l39
              local.set $l44
            end
            local.get $l3
            i32.const 1
            i32.add
            local.tee $l3
            local.get $l22
            i32.ne
            br_if $L26
          end
        end
        local.get $l27
        f32.load
        local.tee $l38
        local.get $l48
        f32.sqrt
        f32.gt
        local.tee $l10
        if $I28
          local.get $l51
          local.get $l57
          f32.sub
          local.tee $l39
          local.get $l43
          local.get $l42
          local.get $l49
          local.get $l55
          f32.sub
          local.tee $l41
          f32.mul
          local.get $l40
          local.get $l50
          local.get $l56
          f32.sub
          local.tee $l48
          f32.mul
          f32.add
          local.get $l43
          local.get $l39
          f32.mul
          f32.add
          local.get $l42
          local.get $l42
          f32.mul
          local.get $l40
          local.get $l40
          f32.mul
          f32.add
          local.get $l43
          local.get $l43
          f32.mul
          f32.add
          f32.div
          local.tee $l45
          f32.mul
          f32.sub
          local.tee $l39
          local.get $l39
          f32.mul
          local.get $l41
          local.get $l42
          local.get $l45
          f32.mul
          f32.sub
          local.tee $l41
          local.get $l41
          f32.mul
          local.get $l48
          local.get $l40
          local.get $l45
          f32.mul
          f32.sub
          local.tee $l42
          local.get $l42
          f32.mul
          f32.add
          f32.add
          f32.sqrt
          local.tee $l40
          f32.const 0x0p+0 (;=0;)
          f32.gt
          if $I29
            local.get $l39
            f32.const 0x1p+0 (;=1;)
            local.get $l40
            f32.div
            local.tee $l40
            f32.mul
            local.set $l39
            local.get $l42
            local.get $l40
            f32.mul
            local.set $l42
            local.get $l41
            local.get $l40
            f32.mul
            local.set $l41
          end
          local.get $l2
          local.get $l8
          i32.const 12
          i32.mul
          i32.add
          local.tee $l3
          local.get $l51
          local.get $l38
          local.get $l39
          f32.mul
          f32.add
          local.tee $l51
          f32.store offset=8
          local.get $l3
          local.get $l50
          local.get $l38
          local.get $l42
          f32.mul
          f32.add
          local.tee $l50
          f32.store offset=4
          local.get $l3
          local.get $l49
          local.get $l38
          local.get $l41
          f32.mul
          f32.add
          local.tee $l49
          f32.store
        end
        f32.const 0x0p+0 (;=0;)
        local.set $l38
        local.get $l44
        local.get $l44
        f32.mul
        local.get $l46
        local.get $l46
        f32.mul
        f32.add
        local.get $l47
        local.get $l47
        f32.mul
        f32.add
        f32.sqrt
        local.tee $l39
        f32.const 0x0p+0 (;=0;)
        f32.gt
        if $I30
          local.get $l47
          f32.const 0x1p+0 (;=1;)
          local.get $l39
          f32.div
          local.tee $l39
          f32.mul
          local.set $l47
          local.get $l46
          local.get $l39
          f32.mul
          local.set $l46
          local.get $l44
          local.get $l39
          f32.mul
          local.set $l44
        end
        local.get $l44
        local.get $l49
        f32.mul
        local.get $l46
        local.get $l50
        f32.mul
        f32.add
        local.get $l47
        local.get $l51
        f32.mul
        f32.add
        local.set $l41
        i32.const 0
        local.set $l3
        block $B31
          local.get $l22
          i32.eqz
          if $I32
            i32.const 0
            local.set $l8
            br $B31
          end
          i32.const 0
          local.set $l8
          loop $L33
            local.get $l44
            local.get $l2
            local.get $l3
            i32.const 12
            i32.mul
            i32.add
            local.tee $l11
            f32.load
            f32.mul
            local.get $l46
            local.get $l11
            f32.load offset=4
            f32.mul
            f32.add
            local.get $l47
            local.get $l11
            f32.load offset=8
            f32.mul
            f32.add
            local.get $l41
            f32.sub
            f32.abs
            local.tee $l39
            local.get $l38
            local.get $l38
            local.get $l39
            f32.lt
            local.tee $l11
            select
            local.set $l38
            local.get $l3
            local.get $l8
            local.get $l11
            select
            local.set $l8
            local.get $l3
            i32.const 1
            i32.add
            local.tee $l3
            local.get $l22
            i32.ne
            br_if $L33
          end
        end
        local.get $l10
        i32.const 1
        i32.xor
        local.get $l38
        f32.abs
        local.get $l27
        f32.load
        local.tee $l38
        f32.lt
        i32.eqz
        br_if $B11
        drop
        local.get $l47
        local.get $l38
        f32.mul
        local.set $l39
        local.get $l46
        local.get $l38
        f32.mul
        local.set $l42
        local.get $l44
        local.get $l38
        f32.mul
        local.set $l38
        local.get $l2
        local.get $l8
        i32.const 12
        i32.mul
        i32.add
        local.tee $l3
        i32.const 8
        i32.add
        local.set $l11
        local.get $l3
        i32.const 4
        i32.add
        local.set $l2
        local.get $l3
        block $B34 (result f32)
          local.get $l44
          local.get $l3
          f32.load
          local.tee $l40
          f32.mul
          local.get $l46
          local.get $l3
          f32.load offset=4
          local.tee $l43
          f32.mul
          f32.add
          local.get $l47
          local.get $l3
          f32.load offset=8
          local.tee $l45
          f32.mul
          f32.add
          local.get $l41
          f32.sub
          f32.const 0x0p+0 (;=0;)
          f32.gt
          if $I35
            local.get $l39
            local.get $l45
            f32.add
            local.set $l39
            local.get $l42
            local.get $l43
            f32.add
            local.set $l41
            local.get $l38
            local.get $l40
            f32.add
            br $B34
          end
          local.get $l45
          local.get $l39
          f32.sub
          local.set $l39
          local.get $l43
          local.get $l42
          f32.sub
          local.set $l41
          local.get $l40
          local.get $l38
          f32.sub
        end
        f32.store
        local.get $l2
        local.get $l41
        f32.store
        local.get $l11
        local.get $l39
        f32.store
        i32.const 0
      end
      local.set $l2
      local.get $p0
      i32.load offset=32
      local.tee $l4
      local.get $l7
      i32.load offset=172
      local.tee $l3
      i32.store offset=24
      local.get $l3
      if $I36
        i32.const 0
        local.set $l1
        loop $L37
          local.get $l1
          i32.const 24
          i32.mul
          local.tee $l8
          local.get $l4
          i32.load offset=36
          i32.add
          local.tee $l6
          local.get $l17
          local.get $l1
          i32.const 12
          i32.mul
          i32.add
          local.tee $l10
          f32.load
          f32.store
          local.get $l6
          local.get $l10
          f32.load offset=4
          f32.store offset=4
          local.get $l6
          local.get $l10
          f32.load offset=8
          f32.store offset=8
          local.get $l4
          i32.load offset=36
          local.get $l8
          i32.add
          local.get $l1
          i32.store offset=12
          local.get $l1
          i32.const 1
          i32.add
          local.tee $l1
          local.get $l3
          i32.ne
          br_if $L37
        end
      end
      local.get $l2
      if $I38
        local.get $l7
        f32.load offset=12
        local.set $l40
        local.get $l7
        f32.load offset=8
        local.set $l38
        local.get $p0
        i32.load offset=32
        local.tee $l1
        local.get $l7
        f32.load offset=96
        f32.store offset=108
        local.get $l1
        local.get $l7
        f32.load offset=100
        f32.store offset=112
        local.get $l1
        local.get $l7
        f32.load offset=104
        f32.store offset=116
        local.get $l1
        local.get $l7
        i64.load offset=108 align=4
        i64.store offset=120 align=4
        local.get $l1
        local.get $l7
        i32.load offset=116
        i32.store offset=128
        local.get $l1
        local.get $l7
        f32.load offset=16
        f32.store offset=180
        local.get $l1
        local.get $l7
        f32.load offset=20
        f32.store offset=184
        local.get $l1
        local.get $l7
        f32.load offset=24
        f32.store offset=188
        local.get $l1
        local.get $l7
        i64.load offset=28 align=4
        i64.store offset=192 align=4
        local.get $l1
        local.get $l7
        i32.load offset=36
        i32.store offset=200
        local.get $l1
        local.get $l7
        f32.load offset=120
        f32.store offset=132
        local.get $l1
        local.get $l7
        f32.load offset=124
        f32.store offset=136
        local.get $l1
        local.get $l7
        f32.load offset=128
        f32.store offset=140
        local.get $l1
        local.get $l7
        i64.load offset=132 align=4
        i64.store offset=144 align=4
        local.get $l1
        local.get $l7
        i32.load offset=140
        i32.store offset=152
        local.get $l1
        local.get $l7
        f32.load offset=40
        f32.store offset=204
        local.get $l1
        local.get $l7
        f32.load offset=44
        f32.store offset=208
        local.get $l1
        local.get $l7
        f32.load offset=48
        f32.store offset=212
        local.get $l1
        local.get $l7
        i64.load offset=52 align=4
        i64.store offset=216 align=4
        local.get $l1
        local.get $l7
        i32.load offset=60
        i32.store offset=224
        local.get $l1
        local.get $l7
        f32.load offset=144
        f32.store offset=156
        local.get $l1
        local.get $l7
        f32.load offset=148
        f32.store offset=160
        local.get $l1
        local.get $l7
        f32.load offset=152
        f32.store offset=164
        local.get $l1
        local.get $l7
        i64.load offset=156 align=4
        i64.store offset=168 align=4
        local.get $l1
        local.get $l7
        i32.load offset=164
        i32.store offset=176
        local.get $l1
        local.get $l7
        f32.load offset=64
        f32.store offset=228
        local.get $l1
        local.get $l7
        f32.load offset=68
        f32.store offset=232
        local.get $l1
        local.get $l7
        f32.load offset=72
        f32.store offset=236
        local.get $l1
        local.get $l7
        i64.load offset=76 align=4
        i64.store offset=240 align=4
        local.get $l1
        local.get $l7
        i32.load offset=84
        i32.store offset=248
        local.get $l1
        local.get $l38
        f32.store offset=256
        local.get $l1
        local.get $l40
        f32.store offset=252
        local.get $l1
        i32.const 1
        i32.store8 offset=104
      end
      i32.const 3
      local.set $l8
      block $B39
        block $B40
          block $B41
            block $B42
              block $B43
                local.get $p0
                i32.load offset=32
                call $f72900
                br_table $B42 $B43 $B40 $B41 $B39
              end
              i32.const 1
              local.set $l8
              br $B39
            end
            i32.const 0
            local.set $l8
            local.get $p0
            i32.load offset=32
            local.tee $l1
            i32.load offset=92
            local.tee $l4
            i32.eqz
            br_if $B39
            i32.const 0
            local.set $l10
            loop $L44
              local.get $l1
              i32.load offset=88
              local.get $l10
              i32.const 2
              i32.shl
              i32.add
              i32.load
              local.tee $l6
              i32.load offset=48
              i32.eqz
              if $I45
                loop $L46
                  global.get $g0
                  i32.const 16
                  i32.sub
                  local.tee $l16
                  global.set $g0
                  local.get $l6
                  local.tee $l9
                  i32.load
                  local.set $l19
                  block $B47 (result i32)
                    loop $L48
                      block $B49
                        local.get $l9
                        f32.load offset=12
                        local.get $l19
                        i32.load offset=32
                        i32.load offset=36
                        local.tee $l4
                        f32.load offset=12
                        f32.mul
                        local.get $l9
                        f32.load offset=16
                        local.get $l4
                        f32.load offset=16
                        f32.mul
                        f32.add
                        local.get $l9
                        f32.load offset=20
                        local.get $l4
                        f32.load offset=20
                        f32.mul
                        f32.add
                        f32.const 0x1.ff4c5ep-1 (;=0.99863;)
                        f32.gt
                        i32.eqz
                        br_if $B49
                        local.get $l9
                        f32.load offset=24
                        local.get $l4
                        f32.load offset=24
                        f32.ge
                        i32.eqz
                        br_if $B49
                        i32.const 0
                        local.set $l3
                        i32.const 0
                        local.set $l13
                        i32.const 0
                        local.set $l23
                        global.get $g0
                        i32.const 80
                        i32.sub
                        local.tee $l4
                        global.set $g0
                        local.get $l4
                        local.tee $l5
                        local.get $l19
                        local.tee $l15
                        i32.load offset=32
                        i32.load offset=36
                        local.tee $l18
                        i32.load16_u offset=4
                        local.get $l15
                        i32.load offset=36
                        local.tee $l21
                        i32.load16_u offset=4
                        i32.add
                        i32.const 44
                        i32.mul
                        local.tee $l2
                        i32.const 1024
                        i32.gt_u
                        i32.store8 offset=76
                        block $B50
                          local.get $l2
                          i32.const 1025
                          i32.ge_u
                          if $I51
                            local.get $l2
                            i32.const 3217483
                            i32.const 1446
                            call $f70043
                            local.set $l2
                            br $B50
                          end
                          local.get $l4
                          local.get $l2
                          i32.const 15
                          i32.add
                          i32.const 16777200
                          i32.and
                          i32.sub
                          local.tee $l2
                          global.set $g0
                        end
                        local.get $l5
                        local.get $l2
                        i32.store offset=72
                        local.get $l2
                        i32.const 0
                        local.get $l18
                        i32.load16_u offset=4
                        local.get $l21
                        i32.load16_u offset=4
                        i32.add
                        i32.const 44
                        i32.mul
                        call $f484
                        drop
                        local.get $l5
                        i32.const 0
                        i32.store8 offset=68
                        local.get $l5
                        i64.const 0
                        i64.store offset=56
                        local.get $l5
                        i64.const -36028801313931264
                        i64.store offset=48
                        local.get $l5
                        i32.const 0
                        i32.store offset=32
                        local.get $l5
                        i32.const 0
                        i32.store offset=16
                        local.get $l5
                        i32.const 0
                        i32.store16 offset=12
                        local.get $l5
                        local.get $l5
                        i32.load offset=72
                        local.tee $l12
                        i32.store offset=8
                        local.get $l15
                        i32.load offset=28
                        local.get $l21
                        i32.load
                        local.tee $l2
                        local.get $l2
                        local.get $l15
                        i32.eq
                        select
                        local.tee $l20
                        local.set $l2
                        loop $L52
                          local.get $l12
                          local.get $l3
                          i32.const 44
                          i32.mul
                          local.tee $l14
                          i32.add
                          local.get $l5
                          i32.const 8
                          i32.add
                          i32.store offset=36
                          local.get $l5
                          i32.load offset=72
                          local.get $l14
                          i32.add
                          local.tee $l4
                          local.get $l2
                          f32.load
                          f32.store
                          local.get $l4
                          local.get $l2
                          f32.load offset=4
                          f32.store offset=4
                          local.get $l4
                          local.get $l2
                          f32.load offset=8
                          f32.store offset=8
                          local.get $l4
                          local.get $l2
                          i32.load offset=20
                          i32.store offset=20
                          local.get $l4
                          local.get $l2
                          i64.load offset=12 align=4
                          i64.store offset=12 align=4
                          i32.const 0
                          local.get $l3
                          i32.const 1
                          i32.add
                          local.tee $l4
                          local.get $l2
                          i32.load offset=28
                          local.get $l20
                          i32.eq
                          select
                          local.set $l25
                          local.get $l2
                          local.get $l15
                          i32.eq
                          local.set $l12
                          local.get $l5
                          i32.load offset=72
                          local.get $l14
                          i32.add
                          local.set $l24
                          local.get $l15
                          i32.load offset=32
                          local.set $l26
                          local.get $l3
                          i32.eqz
                          if $I53
                            local.get $l21
                            i32.load16_u offset=4
                            local.set $l3
                          end
                          local.get $l24
                          local.get $l23
                          local.get $l12
                          select
                          local.set $l23
                          local.get $l26
                          local.get $l13
                          local.get $l12
                          select
                          local.set $l13
                          local.get $l5
                          i32.load offset=72
                          local.tee $l12
                          local.get $l14
                          i32.add
                          local.get $l12
                          local.get $l25
                          i32.const 44
                          i32.mul
                          i32.add
                          i32.store offset=28
                          local.get $l5
                          i32.load offset=72
                          local.tee $l12
                          local.get $l14
                          i32.add
                          local.get $l3
                          i32.const 44
                          i32.mul
                          local.get $l12
                          i32.add
                          i32.const 44
                          i32.sub
                          i32.store offset=24
                          local.get $l20
                          local.get $l2
                          i32.load offset=28
                          local.tee $l2
                          i32.ne
                          if $I54
                            local.get $l5
                            i32.load offset=72
                            local.set $l12
                            local.get $l4
                            local.set $l3
                            br $L52
                          end
                        end
                        local.get $l18
                        i32.load
                        local.set $l2
                        loop $L55
                          local.get $l4
                          i32.const 44
                          i32.mul
                          local.tee $l14
                          local.get $l5
                          i32.load offset=72
                          i32.add
                          local.get $l5
                          i32.const 8
                          i32.add
                          i32.store offset=36
                          local.get $l5
                          i32.load offset=72
                          local.get $l14
                          i32.add
                          local.tee $l3
                          local.get $l2
                          f32.load
                          f32.store
                          local.get $l3
                          local.get $l2
                          f32.load offset=4
                          f32.store offset=4
                          local.get $l3
                          local.get $l2
                          f32.load offset=8
                          f32.store offset=8
                          local.get $l3
                          local.get $l2
                          i32.load offset=20
                          i32.store offset=20
                          local.get $l3
                          local.get $l2
                          i64.load offset=12 align=4
                          i64.store offset=12 align=4
                          local.get $l5
                          i32.load offset=72
                          local.set $l3
                          block $B56 (result i32)
                            local.get $l2
                            i32.load offset=28
                            local.get $l18
                            i32.load
                            i32.eq
                            if $I57
                              local.get $l21
                              i32.load16_u offset=4
                              local.tee $l24
                              br $B56
                            end
                            local.get $l21
                            i32.load16_u offset=4
                            local.set $l24
                            local.get $l4
                            i32.const 1
                            i32.add
                          end
                          local.set $l26
                          local.get $l2
                          local.get $l13
                          i32.eq
                          local.set $l25
                          local.get $l3
                          local.get $l14
                          i32.add
                          local.set $l12
                          local.get $l4
                          local.set $l20
                          local.get $l4
                          local.get $l24
                          i32.eq
                          if $I58
                            local.get $l4
                            local.get $l18
                            i32.load16_u offset=4
                            i32.add
                            local.set $l20
                          end
                          local.get $l12
                          local.get $l13
                          local.get $l25
                          select
                          local.set $l13
                          local.get $l12
                          local.get $l3
                          local.get $l26
                          i32.const 44
                          i32.mul
                          i32.add
                          i32.store offset=28
                          local.get $l5
                          i32.load offset=72
                          local.tee $l3
                          local.get $l14
                          i32.add
                          local.get $l20
                          i32.const 44
                          i32.mul
                          local.get $l3
                          i32.add
                          i32.const 44
                          i32.sub
                          i32.store offset=24
                          local.get $l4
                          i32.const 1
                          i32.add
                          local.set $l4
                          local.get $l2
                          i32.load offset=28
                          local.tee $l2
                          local.get $l18
                          i32.load
                          i32.ne
                          br_if $L55
                        end
                        local.get $l13
                        i32.load offset=28
                        local.set $l2
                        local.get $l23
                        i32.load offset=24
                        local.set $l4
                        local.get $l13
                        i32.load offset=24
                        local.tee $l3
                        local.get $l23
                        i32.load offset=28
                        local.tee $l13
                        i32.store offset=28
                        local.get $l13
                        local.get $l3
                        i32.store offset=24
                        local.get $l4
                        local.get $l2
                        i32.store offset=28
                        local.get $l2
                        local.get $l4
                        i32.store offset=24
                        local.get $l5
                        i32.const 8
                        i32.add
                        call $f72891
                        local.get $l5
                        f32.load offset=28
                        local.set $l49
                        local.get $l5
                        f32.load offset=24
                        local.set $l50
                        local.get $l5
                        f32.load offset=20
                        local.set $l51
                        block $B59
                          local.get $l1
                          i32.load offset=24
                          local.tee $l3
                          if $I60
                            local.get $l1
                            f32.load offset=256
                            local.set $l40
                            local.get $l5
                            f32.load offset=48
                            local.set $l38
                            local.get $l1
                            i32.load offset=36
                            local.set $l13
                            i32.const 0
                            local.set $l14
                            i32.const 0
                            local.set $l4
                            loop $L61
                              local.get $l13
                              local.get $l4
                              i32.const 24
                              i32.mul
                              i32.add
                              local.tee $l2
                              f32.load
                              local.get $l51
                              f32.mul
                              local.get $l2
                              f32.load offset=4
                              local.get $l50
                              f32.mul
                              f32.add
                              local.get $l2
                              f32.load offset=8
                              local.get $l49
                              f32.mul
                              f32.add
                              local.get $l38
                              f32.sub
                              local.get $l40
                              f32.gt
                              br_if $B59
                              local.get $l4
                              i32.const 1
                              i32.add
                              local.tee $l4
                              local.get $l3
                              i32.ne
                              br_if $L61
                            end
                          end
                          local.get $l5
                          i32.load offset=8
                          local.tee $l3
                          f32.load offset=8
                          local.set $l40
                          local.get $l3
                          f32.load offset=4
                          local.set $l38
                          local.get $l3
                          f32.load
                          local.set $l39
                          local.get $l1
                          f32.load offset=252
                          local.set $l54
                          local.get $l3
                          local.set $l4
                          loop $L62
                            local.get $l4
                            i32.load offset=28
                            local.tee $l4
                            f32.load
                            local.tee $l41
                            local.get $l39
                            f32.sub
                            local.tee $l44
                            local.set $l52
                            local.get $l4
                            f32.load offset=4
                            local.tee $l42
                            local.get $l38
                            f32.sub
                            local.tee $l43
                            local.set $l48
                            local.get $l4
                            f32.load offset=8
                            local.tee $l45
                            local.get $l40
                            f32.sub
                            local.tee $l47
                            local.set $l53
                            i32.const 0
                            local.set $l14
                            local.get $l4
                            local.set $l2
                            local.get $l44
                            local.get $l44
                            f32.mul
                            local.get $l43
                            local.get $l43
                            f32.mul
                            f32.add
                            local.get $l47
                            local.get $l47
                            f32.mul
                            f32.add
                            f32.sqrt
                            local.tee $l46
                            f32.const 0x0p+0 (;=0;)
                            f32.gt
                            if $I63
                              local.get $l47
                              f32.const 0x1p+0 (;=1;)
                              local.get $l46
                              f32.div
                              local.tee $l46
                              f32.mul
                              local.set $l53
                              local.get $l44
                              local.get $l46
                              f32.mul
                              local.set $l52
                              local.get $l43
                              local.get $l46
                              f32.mul
                              local.set $l48
                            end
                            local.get $l43
                            local.get $l52
                            local.get $l49
                            f32.mul
                            local.get $l53
                            local.get $l51
                            f32.mul
                            f32.sub
                            f32.neg
                            local.tee $l46
                            f32.mul
                            local.get $l53
                            local.get $l50
                            f32.mul
                            local.get $l48
                            local.get $l49
                            f32.mul
                            f32.sub
                            local.tee $l43
                            local.get $l44
                            f32.mul
                            f32.sub
                            local.get $l48
                            local.get $l51
                            f32.mul
                            local.get $l52
                            local.get $l50
                            f32.mul
                            f32.sub
                            local.tee $l44
                            local.get $l47
                            f32.mul
                            f32.sub
                            local.get $l54
                            f32.gt
                            br_if $B59
                            loop $L64
                              local.get $l4
                              local.get $l2
                              i32.load offset=28
                              local.tee $l2
                              i32.ne
                              if $I65
                                local.get $l2
                                f32.load offset=4
                                local.get $l38
                                f32.sub
                                local.get $l46
                                f32.mul
                                local.get $l43
                                local.get $l2
                                f32.load
                                local.get $l39
                                f32.sub
                                f32.mul
                                f32.sub
                                local.get $l44
                                local.get $l2
                                f32.load offset=8
                                local.get $l40
                                f32.sub
                                f32.mul
                                f32.sub
                                local.get $l54
                                f32.gt
                                i32.eqz
                                br_if $L64
                                br $B59
                              end
                            end
                            local.get $l45
                            local.set $l40
                            local.get $l42
                            local.set $l38
                            local.get $l41
                            local.set $l39
                            local.get $l3
                            local.get $l4
                            i32.ne
                            br_if $L62
                          end
                          local.get $l15
                          i32.load offset=28
                          local.set $l13
                          local.get $l15
                          i32.load offset=32
                          local.tee $l2
                          i32.load offset=24
                          local.set $l12
                          local.get $l2
                          i32.load offset=36
                          local.set $l4
                          loop $L66
                            local.get $l2
                            i32.load offset=28
                            local.set $l2
                            local.get $l15
                            i32.load offset=24
                            local.tee $l15
                            i32.load offset=32
                            i32.load offset=36
                            local.tee $l3
                            local.get $l4
                            i32.eq
                            br_if $L66
                          end
                          local.get $l4
                          local.get $l13
                          i32.load offset=32
                          i32.load offset=36
                          local.tee $l18
                          i32.eq
                          if $I67
                            loop $L68
                              local.get $l12
                              i32.load offset=24
                              local.set $l12
                              local.get $l13
                              i32.load offset=28
                              local.tee $l13
                              i32.load offset=32
                              i32.load offset=36
                              local.tee $l18
                              local.get $l4
                              i32.eq
                              br_if $L68
                            end
                          end
                          local.get $l12
                          i32.load offset=32
                          i32.load offset=36
                          local.get $l18
                          i32.eq
                          br_if $B59
                          local.get $l3
                          local.get $l2
                          i32.load offset=32
                          i32.load offset=36
                          i32.ne
                          local.set $l14
                        end
                        local.get $l5
                        i32.load8_u offset=76
                        if $I69
                          local.get $l5
                          i32.load offset=72
                          call $f70044
                        end
                        local.get $l5
                        i32.const 80
                        i32.add
                        global.set $g0
                        local.get $l14
                        i32.eqz
                        br_if $B49
                        i32.const 0
                        local.set $l4
                        local.get $l16
                        i32.const 0
                        i32.store offset=8
                        local.get $l16
                        i64.const 0
                        i64.store
                        local.get $l9
                        local.get $l19
                        local.get $l16
                        call $f72889
                        drop
                        local.get $l1
                        local.get $l1
                        i32.load offset=100
                        local.get $l16
                        i32.load offset=4
                        local.tee $l19
                        i32.sub
                        i32.store offset=100
                        local.get $l19
                        if $I70
                          loop $L71
                            local.get $l1
                            local.get $l16
                            i32.load
                            local.get $l4
                            i32.const 2
                            i32.shl
                            i32.add
                            i32.load
                            local.get $l9
                            call $f72899
                            local.get $l4
                            i32.const 1
                            i32.add
                            local.tee $l4
                            local.get $l16
                            i32.load offset=4
                            i32.lt_u
                            br_if $L71
                          end
                        end
                        block $B72
                          local.get $l16
                          i32.load offset=8
                          local.tee $l9
                          i32.const 0
                          i32.lt_s
                          br_if $B72
                          local.get $l9
                          i32.const 2147483647
                          i32.and
                          i32.eqz
                          br_if $B72
                          local.get $l16
                          i32.load
                          local.tee $l9
                          i32.eqz
                          br_if $B72
                          call $f69753
                          local.tee $l4
                          local.get $l9
                          local.get $l4
                          i32.load
                          i32.load offset=12
                          call_indirect $__indirect_function_table (type $t1)
                        end
                        i32.const 1
                        br $B47
                      end
                      local.get $l19
                      i32.load offset=28
                      local.tee $l19
                      local.get $l9
                      i32.load
                      i32.ne
                      br_if $L48
                    end
                    i32.const 0
                  end
                  local.set $l9
                  local.get $l16
                  i32.const 16
                  i32.add
                  global.set $g0
                  local.get $l9
                  br_if $L46
                end
                local.get $l1
                i32.load offset=92
                local.set $l4
              end
              local.get $l10
              i32.const 1
              i32.add
              local.tee $l10
              local.get $l4
              i32.lt_u
              br_if $L44
            end
            br $B39
          end
          i32.const 2
          local.set $l8
          local.get $p0
          i32.load offset=32
          i32.load offset=28
          local.get $p0
          i32.load offset=4
          local.tee $l1
          i32.load16_u offset=38
          i32.le_u
          br_if $B39
          local.get $l1
          i32.load8_u offset=36
          i32.const 32
          i32.and
          if $I73
            local.get $p0
            call $f72909
            drop
            br $B39
          end
          local.get $p0
          call $f72910
          br $B39
        end
        local.get $p0
        i32.load offset=4
        i32.load8_u offset=36
        i32.const 32
        i32.and
        if $I74
          local.get $p0
          call $f72909
          local.set $l8
          br $B39
        end
        local.get $p0
        call $f72910
        i32.const 0
        local.set $l8
      end
      block $B75
        local.get $p0
        i32.load offset=4
        i32.load8_u offset=36
        i32.const 128
        i32.and
        i32.eqz
        br_if $B75
        local.get $l8
        br_if $B75
        local.get $p0
        i32.load offset=36
        br_if $B75
        local.get $p0
        i32.load offset=32
        local.tee $l6
        i32.load offset=92
        local.tee $l1
        i32.eqz
        if $I76
          i32.const 0
          local.set $l8
          br $B75
        end
        local.get $l1
        i32.const 1
        i32.and
        local.set $l2
        local.get $l6
        i32.load offset=88
        local.set $l10
        block $B77
          local.get $l1
          i32.const 1
          i32.eq
          if $I78
            i32.const 0
            local.set $l6
            i32.const 0
            local.set $l1
            br $B77
          end
          local.get $l1
          i32.const -2
          i32.and
          local.set $l4
          i32.const 0
          local.set $l6
          i32.const 0
          local.set $l1
          loop $L79
            local.get $l10
            local.get $l1
            i32.const 2
            i32.shl
            local.tee $l8
            i32.add
            i32.load
            local.tee $l3
            i32.load offset=48
            i32.eqz
            if $I80
              local.get $l3
              i32.load16_u offset=4
              local.tee $l3
              local.get $l6
              local.get $l3
              local.get $l6
              i32.gt_u
              select
              local.set $l6
            end
            local.get $l10
            local.get $l8
            i32.const 4
            i32.or
            i32.add
            i32.load
            local.tee $l8
            i32.load offset=48
            i32.eqz
            if $I81
              local.get $l8
              i32.load16_u offset=4
              local.tee $l8
              local.get $l6
              local.get $l6
              local.get $l8
              i32.lt_u
              select
              local.set $l6
            end
            local.get $l1
            i32.const 2
            i32.add
            local.set $l1
            local.get $l4
            i32.const 2
            i32.sub
            local.tee $l4
            br_if $L79
          end
        end
        block $B82
          local.get $l2
          i32.eqz
          br_if $B82
          local.get $l10
          local.get $l1
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $l1
          i32.load offset=48
          br_if $B82
          local.get $l1
          i32.load16_u offset=4
          local.tee $l1
          local.get $l6
          local.get $l1
          local.get $l6
          i32.gt_u
          select
          local.set $l6
        end
        i32.const 0
        local.set $l8
        local.get $l6
        i32.const 33
        i32.lt_u
        br_if $B75
        local.get $p0
        call $f72910
      end
      local.get $l17
      i32.eqz
      br_if $B1
      call $f69753
      local.tee $l1
      local.get $l17
      local.get $l1
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $l7
    i32.const 208
    i32.add
    global.set $g0
    local.get $l8)
