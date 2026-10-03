  (func $f72754 (type $t6) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32)
    (local $l5 i32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32)
    global.get $g0
    i32.const 288
    i32.sub
    local.tee $l5
    global.set $g0
    local.get $l5
    i32.const 192
    i32.add
    local.get $l5
    i32.const 160
    i32.add
    local.get $p1
    local.get $p2
    local.get $p3
    call $f72749
    local.get $p4
    i32.const 1
    i32.and
    if $I0
      local.get $p0
      local.get $l5
      i32.const 192
      i32.add
      local.get $l5
      i32.const 160
      i32.add
      local.get $p0
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t2)
    end
    block $B1
      local.get $p4
      i32.const 2
      i32.and
      i32.eqz
      br_if $B1
      local.get $l5
      f32.load offset=212
      local.set $l16
      local.get $l5
      f32.load offset=180
      local.set $l22
      local.get $l5
      f32.load offset=216
      local.set $l18
      local.get $l5
      f32.load offset=184
      local.set $l19
      local.get $l5
      f32.load offset=168
      local.set $l23
      local.get $l5
      f32.load offset=160
      local.set $l30
      local.get $l5
      f32.load offset=172
      local.set $l31
      local.get $l5
      f32.load offset=164
      local.set $l27
      local.get $l5
      f32.load offset=208
      local.set $l26
      local.get $l5
      f32.load offset=176
      local.set $l28
      local.get $l5
      local.get $l5
      f32.load offset=196
      local.tee $l7
      local.get $l7
      f32.add
      local.tee $l12
      local.get $l5
      f32.load offset=200
      local.tee $l6
      f32.mul
      local.tee $l17
      local.get $l5
      f32.load offset=192
      local.tee $l9
      local.get $l9
      f32.add
      local.tee $l10
      local.get $l5
      f32.load offset=204
      local.tee $l8
      f32.mul
      local.tee $l32
      f32.sub
      local.tee $l14
      f32.store offset=148
      local.get $l5
      local.get $l17
      local.get $l32
      f32.add
      local.tee $l15
      f32.store offset=140
      local.get $l5
      f32.const 0x1p+0 (;=1;)
      local.get $l9
      local.get $l10
      f32.mul
      f32.sub
      local.tee $l17
      local.get $l7
      local.get $l12
      f32.mul
      local.tee $l32
      f32.sub
      local.tee $l24
      f32.store offset=152
      local.get $l5
      local.get $l17
      local.get $l6
      local.get $l6
      local.get $l6
      f32.add
      local.tee $l11
      f32.mul
      local.tee $l13
      f32.sub
      local.tee $l20
      f32.store offset=136
      local.get $l5
      local.get $l10
      local.get $l6
      f32.mul
      local.tee $l17
      local.get $l12
      local.get $l8
      f32.mul
      local.tee $l12
      f32.add
      local.tee $l29
      f32.store offset=144
      local.get $l5
      local.get $l10
      local.get $l7
      f32.mul
      local.tee $l10
      local.get $l11
      local.get $l8
      f32.mul
      local.tee $l11
      f32.sub
      local.tee $l25
      f32.store offset=132
      local.get $l5
      local.get $l17
      local.get $l12
      f32.sub
      local.tee $l21
      f32.store offset=128
      local.get $l5
      local.get $l10
      local.get $l11
      f32.add
      local.tee $l11
      f32.store offset=124
      local.get $l5
      f32.const 0x1p+0 (;=1;)
      local.get $l32
      f32.sub
      local.get $l13
      f32.sub
      local.tee $l13
      f32.store offset=120
      local.get $l8
      local.get $l8
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l17
      local.get $l19
      local.get $l18
      f32.sub
      local.tee $l10
      local.get $l10
      f32.add
      local.tee $l10
      f32.mul
      local.get $l8
      local.get $l7
      local.get $l28
      local.get $l26
      f32.sub
      local.tee $l12
      local.get $l12
      f32.add
      local.tee $l12
      f32.mul
      local.get $l9
      local.get $l22
      local.get $l16
      f32.sub
      local.tee $l16
      local.get $l16
      f32.add
      local.tee $l16
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l6
      local.get $l16
      local.get $l7
      f32.neg
      f32.mul
      local.get $l9
      local.get $l12
      f32.mul
      f32.sub
      local.get $l6
      local.get $l10
      f32.mul
      f32.sub
      local.tee $l22
      f32.mul
      f32.sub
      local.set $l18
      local.get $l17
      local.get $l16
      f32.mul
      local.get $l8
      local.get $l9
      local.get $l10
      f32.mul
      local.get $l6
      local.get $l12
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l7
      local.get $l22
      f32.mul
      f32.sub
      local.set $l19
      local.get $l17
      local.get $l12
      f32.mul
      local.get $l8
      local.get $l6
      local.get $l16
      f32.mul
      local.get $l7
      local.get $l10
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l9
      local.get $l22
      f32.mul
      f32.sub
      local.set $l10
      local.get $l9
      local.get $l30
      f32.mul
      local.get $l8
      local.get $l31
      f32.mul
      f32.add
      local.set $l12
      local.get $l7
      local.get $l27
      f32.mul
      local.set $l16
      local.get $l8
      local.get $l23
      f32.mul
      local.get $l6
      local.get $l31
      f32.mul
      f32.sub
      local.set $l17
      local.get $l9
      local.get $l27
      f32.mul
      local.set $l22
      local.get $l8
      local.get $l27
      f32.mul
      local.get $l7
      local.get $l31
      f32.mul
      f32.sub
      local.set $l26
      local.get $l6
      local.get $l30
      f32.mul
      local.set $l28
      local.get $l8
      local.get $l30
      f32.mul
      local.get $l9
      local.get $l31
      f32.mul
      f32.sub
      local.get $l7
      local.get $l23
      f32.mul
      f32.sub
      local.set $l8
      local.get $l6
      local.get $l27
      f32.mul
      local.set $l32
      block $B2
        local.get $p1
        i32.load8_u offset=477
        i32.eqz
        br_if $B2
        block $B3
          block $B4
            block $B5
              block $B6
                block $B7
                  block $B8
                    block $B9
                      local.get $p1
                      i32.load offset=456
                      i32.const 1
                      i32.sub
                      br_table $B9 $B8 $B6 $B7 $B5 $B4 $B3 $B2
                    end
                    f32.const 0x0p+0 (;=0;)
                    local.set $l24
                    block $B10
                      local.get $p1
                      f32.load offset=140
                      f32.const 0x0p+0 (;=0;)
                      f32.gt
                      br_if $B10
                      local.get $p1
                      f32.load offset=136
                      f32.const 0x0p+0 (;=0;)
                      f32.gt
                      br_if $B10
                      local.get $p1
                      f32.load offset=144
                      local.set $l24
                    end
                    local.get $p1
                    f32.load offset=148
                    local.set $l14
                    local.get $l5
                    local.get $p1
                    f32.load offset=152
                    local.tee $l15
                    local.get $l21
                    f32.mul
                    local.get $l5
                    f32.load offset=216
                    local.tee $l20
                    f32.add
                    f32.store offset=80
                    local.get $l5
                    local.get $l15
                    local.get $l11
                    f32.mul
                    local.get $l5
                    f32.load offset=212
                    local.tee $l29
                    f32.add
                    f32.store offset=76
                    local.get $l5
                    local.get $l15
                    local.get $l13
                    f32.mul
                    local.get $l5
                    f32.load offset=208
                    local.tee $l25
                    f32.add
                    f32.store offset=72
                    local.get $l5
                    local.get $l20
                    local.get $l14
                    local.get $l21
                    f32.mul
                    f32.add
                    f32.store offset=48
                    local.get $l5
                    local.get $l29
                    local.get $l14
                    local.get $l11
                    f32.mul
                    f32.add
                    f32.store offset=44
                    local.get $l5
                    local.get $l25
                    local.get $l14
                    local.get $l13
                    f32.mul
                    f32.add
                    f32.store offset=40
                    local.get $p0
                    local.get $l5
                    i32.const 72
                    i32.add
                    local.get $l5
                    i32.const 40
                    i32.add
                    i32.const 16711680
                    i32.const 16711680
                    i32.const 16777215
                    local.get $l14
                    local.get $l24
                    f32.sub
                    local.get $l10
                    f32.lt
                    select
                    local.get $l24
                    local.get $l15
                    f32.add
                    local.get $l10
                    f32.gt
                    select
                    local.get $p0
                    i32.load
                    i32.load offset=28
                    call_indirect $__indirect_function_table (type $t4)
                    br $B2
                  end
                  f32.const 0x0p+0 (;=0;)
                  local.set $l14
                  block $B11
                    local.get $p1
                    f32.load offset=168
                    f32.const 0x0p+0 (;=0;)
                    f32.gt
                    br_if $B11
                    local.get $p1
                    f32.load offset=164
                    f32.const 0x0p+0 (;=0;)
                    f32.gt
                    br_if $B11
                    local.get $p1
                    f32.load offset=172
                    local.set $l14
                  end
                  local.get $p1
                  f32.load offset=176
                  local.set $l11
                  local.get $l5
                  local.get $p1
                  f32.load offset=180
                  local.tee $l13
                  local.get $l15
                  f32.mul
                  local.get $l5
                  f32.load offset=216
                  local.tee $l24
                  f32.add
                  f32.store offset=80
                  local.get $l5
                  local.get $l13
                  local.get $l20
                  f32.mul
                  local.get $l5
                  f32.load offset=212
                  local.tee $l29
                  f32.add
                  f32.store offset=76
                  local.get $l5
                  local.get $l13
                  local.get $l25
                  f32.mul
                  local.get $l5
                  f32.load offset=208
                  local.tee $l21
                  f32.add
                  f32.store offset=72
                  local.get $l5
                  local.get $l24
                  local.get $l11
                  local.get $l15
                  f32.mul
                  f32.add
                  f32.store offset=48
                  local.get $l5
                  local.get $l29
                  local.get $l11
                  local.get $l20
                  f32.mul
                  f32.add
                  f32.store offset=44
                  local.get $l5
                  local.get $l21
                  local.get $l11
                  local.get $l25
                  f32.mul
                  f32.add
                  f32.store offset=40
                  local.get $p0
                  local.get $l5
                  i32.const 72
                  i32.add
                  local.get $l5
                  i32.const 40
                  i32.add
                  i32.const 16711680
                  i32.const 16711680
                  i32.const 16777215
                  local.get $l11
                  local.get $l14
                  f32.sub
                  local.get $l19
                  f32.lt
                  select
                  local.get $l14
                  local.get $l13
                  f32.add
                  local.get $l19
                  f32.gt
                  select
                  local.get $p0
                  i32.load
                  i32.load offset=28
                  call_indirect $__indirect_function_table (type $t4)
                  br $B2
                end
                f32.const 0x0p+0 (;=0;)
                local.set $l15
                block $B12
                  local.get $p1
                  f32.load offset=196
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  br_if $B12
                  local.get $p1
                  f32.load offset=192
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  br_if $B12
                  local.get $p1
                  f32.load offset=200
                  local.set $l15
                end
                local.get $p1
                f32.load offset=204
                local.set $l11
                local.get $l5
                local.get $p1
                f32.load offset=208
                local.tee $l13
                local.get $l24
                f32.mul
                local.get $l5
                f32.load offset=216
                local.tee $l20
                f32.add
                f32.store offset=80
                local.get $l5
                local.get $l13
                local.get $l14
                f32.mul
                local.get $l5
                f32.load offset=212
                local.tee $l25
                f32.add
                f32.store offset=76
                local.get $l5
                local.get $l13
                local.get $l29
                f32.mul
                local.get $l5
                f32.load offset=208
                local.tee $l21
                f32.add
                f32.store offset=72
                local.get $l5
                local.get $l20
                local.get $l11
                local.get $l24
                f32.mul
                f32.add
                f32.store offset=48
                local.get $l5
                local.get $l25
                local.get $l11
                local.get $l14
                f32.mul
                f32.add
                f32.store offset=44
                local.get $l5
                local.get $l21
                local.get $l11
                local.get $l29
                f32.mul
                f32.add
                f32.store offset=40
                local.get $p0
                local.get $l5
                i32.const 72
                i32.add
                local.get $l5
                i32.const 40
                i32.add
                i32.const 16711680
                i32.const 16711680
                i32.const 16777215
                local.get $l11
                local.get $l15
                f32.sub
                local.get $l18
                f32.lt
                select
                local.get $l15
                local.get $l13
                f32.add
                local.get $l18
                f32.gt
                select
                local.get $p0
                i32.load
                i32.load offset=28
                call_indirect $__indirect_function_table (type $t4)
                br $B2
              end
              local.get $p0
              local.get $l5
              i32.const 208
              i32.add
              local.get $l5
              i32.const 120
              i32.add
              local.get $p1
              i32.const 128
              i32.add
              local.get $l10
              local.get $l5
              i32.const 132
              i32.add
              local.get $p1
              i32.const 156
              i32.add
              local.get $l19
              call $f72755
              br $B2
            end
            local.get $p0
            local.get $l5
            i32.const 208
            i32.add
            local.get $l5
            i32.const 120
            i32.add
            local.get $p1
            i32.const 128
            i32.add
            local.get $l10
            local.get $l5
            i32.const 144
            i32.add
            local.get $p1
            i32.const 184
            i32.add
            local.get $l18
            call $f72755
            br $B2
          end
          local.get $p0
          local.get $l5
          i32.const 208
          i32.add
          local.get $l5
          i32.const 132
          i32.add
          local.get $p1
          i32.const 156
          i32.add
          local.get $l19
          local.get $l5
          i32.const 144
          i32.add
          local.get $p1
          i32.const 184
          i32.add
          local.get $l18
          call $f72755
          br $B2
        end
        block $B13
          local.get $p1
          f32.load offset=140
          f32.const 0x0p+0 (;=0;)
          f32.gt
          br_if $B13
          local.get $p1
          f32.load offset=136
          f32.const 0x0p+0 (;=0;)
          f32.gt
          br_if $B13
          local.get $p1
          f32.load offset=144
          local.set $l39
        end
        block $B14
          local.get $p1
          f32.load offset=168
          f32.const 0x0p+0 (;=0;)
          f32.gt
          br_if $B14
          local.get $p1
          f32.load offset=164
          f32.const 0x0p+0 (;=0;)
          f32.gt
          br_if $B14
          local.get $p1
          f32.load offset=172
          local.set $l40
        end
        local.get $p1
        f32.load offset=148
        local.set $l34
        local.get $p1
        f32.load offset=152
        local.set $l35
        local.get $p1
        f32.load offset=176
        local.set $l36
        local.get $p1
        f32.load offset=180
        local.set $l37
        block $B15
          local.get $p1
          f32.load offset=196
          f32.const 0x0p+0 (;=0;)
          f32.gt
          br_if $B15
          local.get $p1
          f32.load offset=192
          f32.const 0x0p+0 (;=0;)
          f32.gt
          br_if $B15
          local.get $p1
          f32.load offset=200
          local.set $l41
        end
        local.get $p1
        f32.load offset=204
        local.set $l38
        local.get $l5
        local.get $p1
        f32.load offset=208
        local.tee $l42
        local.get $l24
        f32.mul
        local.tee $l33
        local.get $l37
        local.get $l15
        f32.mul
        local.tee $l43
        local.get $l35
        local.get $l21
        f32.mul
        local.get $l5
        f32.load offset=216
        local.tee $l44
        f32.add
        local.tee $l49
        f32.add
        local.tee $l50
        f32.add
        f32.store offset=80
        local.get $l5
        local.get $l42
        local.get $l14
        f32.mul
        local.tee $l45
        local.get $l37
        local.get $l20
        f32.mul
        local.tee $l46
        local.get $l35
        local.get $l11
        f32.mul
        local.get $l5
        f32.load offset=212
        local.tee $l47
        f32.add
        local.tee $l51
        f32.add
        local.tee $l52
        f32.add
        f32.store offset=76
        local.get $l5
        local.get $l42
        local.get $l29
        f32.mul
        local.tee $l48
        local.get $l37
        local.get $l25
        f32.mul
        local.tee $l53
        local.get $l35
        local.get $l13
        f32.mul
        local.get $l5
        f32.load offset=208
        local.tee $l54
        f32.add
        local.tee $l55
        f32.add
        local.tee $l56
        f32.add
        f32.store offset=72
        local.get $l5
        local.get $l33
        local.get $l43
        local.get $l44
        local.get $l34
        local.get $l21
        f32.mul
        f32.add
        local.tee $l21
        f32.add
        local.tee $l43
        f32.add
        f32.store offset=48
        local.get $l5
        local.get $l45
        local.get $l46
        local.get $l47
        local.get $l34
        local.get $l11
        f32.mul
        f32.add
        local.tee $l11
        f32.add
        local.tee $l44
        f32.add
        f32.store offset=44
        local.get $l5
        local.get $l48
        local.get $l53
        local.get $l54
        local.get $l34
        local.get $l13
        f32.mul
        f32.add
        local.tee $l13
        f32.add
        local.tee $l46
        f32.add
        f32.store offset=40
        local.get $l5
        local.get $l33
        local.get $l36
        local.get $l15
        f32.mul
        local.tee $l15
        local.get $l21
        f32.add
        local.tee $l21
        f32.add
        f32.store offset=16
        local.get $l5
        local.get $l45
        local.get $l36
        local.get $l20
        f32.mul
        local.tee $l20
        local.get $l11
        f32.add
        local.tee $l47
        f32.add
        f32.store offset=12
        local.get $l5
        local.get $l48
        local.get $l36
        local.get $l25
        f32.mul
        local.tee $l11
        local.get $l13
        f32.add
        local.tee $l25
        f32.add
        f32.store offset=8
        local.get $l5
        local.get $l33
        local.get $l15
        local.get $l49
        f32.add
        local.tee $l15
        f32.add
        f32.store offset=112
        local.get $l5
        local.get $l45
        local.get $l20
        local.get $l51
        f32.add
        local.tee $l20
        f32.add
        f32.store offset=108
        local.get $l5
        local.get $l48
        local.get $l11
        local.get $l55
        f32.add
        local.tee $l33
        f32.add
        f32.store offset=104
        local.get $l5
        local.get $l38
        local.get $l24
        f32.mul
        local.tee $l11
        local.get $l50
        f32.add
        f32.store offset=280
        local.get $l5
        local.get $l38
        local.get $l14
        f32.mul
        local.tee $l13
        local.get $l52
        f32.add
        f32.store offset=276
        local.get $l5
        local.get $l38
        local.get $l29
        f32.mul
        local.tee $l14
        local.get $l56
        f32.add
        f32.store offset=272
        local.get $l5
        local.get $l11
        local.get $l43
        f32.add
        f32.store offset=264
        local.get $l5
        local.get $l13
        local.get $l44
        f32.add
        f32.store offset=260
        local.get $l5
        local.get $l14
        local.get $l46
        f32.add
        f32.store offset=256
        local.get $l5
        local.get $l11
        local.get $l21
        f32.add
        f32.store offset=248
        local.get $l5
        local.get $l13
        local.get $l47
        f32.add
        f32.store offset=244
        local.get $l5
        local.get $l14
        local.get $l25
        f32.add
        f32.store offset=240
        local.get $l5
        local.get $l11
        local.get $l15
        f32.add
        f32.store offset=232
        local.get $l5
        local.get $l13
        local.get $l20
        f32.add
        f32.store offset=228
        local.get $l5
        local.get $l14
        local.get $l33
        f32.add
        f32.store offset=224
        local.get $p0
        local.get $l5
        i32.const 72
        i32.add
        local.get $l5
        i32.const 40
        i32.add
        i32.const 16711680
        i32.const 16711680
        i32.const 16711680
        i32.const 16711680
        i32.const 16711680
        i32.const 16711680
        i32.const 16777215
        local.get $l38
        local.get $l41
        f32.sub
        local.get $l18
        f32.lt
        select
        local.get $l41
        local.get $l42
        f32.add
        local.get $l18
        f32.gt
        select
        local.get $l36
        local.get $l40
        f32.sub
        local.get $l19
        f32.lt
        select
        local.get $l40
        local.get $l37
        f32.add
        local.get $l19
        f32.gt
        select
        local.get $l34
        local.get $l39
        f32.sub
        local.get $l10
        f32.lt
        select
        local.get $l39
        local.get $l35
        f32.add
        local.get $l10
        f32.gt
        select
        local.tee $p4
        local.get $p0
        i32.load
        i32.load offset=28
        call_indirect $__indirect_function_table (type $t4)
        local.get $p0
        local.get $l5
        i32.const 40
        i32.add
        local.get $l5
        i32.const 8
        i32.add
        local.get $p4
        local.get $p0
        i32.load
        i32.load offset=28
        call_indirect $__indirect_function_table (type $t4)
        local.get $p0
        local.get $l5
        i32.const 8
        i32.add
        local.get $l5
        i32.const 104
        i32.add
        local.get $p4
        local.get $p0
        i32.load
        i32.load offset=28
        call_indirect $__indirect_function_table (type $t4)
        local.get $p0
        local.get $l5
        i32.const 104
        i32.add
        local.get $l5
        i32.const 72
        i32.add
        local.get $p4
        local.get $p0
        i32.load
        i32.load offset=28
        call_indirect $__indirect_function_table (type $t4)
        local.get $p0
        local.get $l5
        i32.const 272
        i32.add
        local.get $l5
        i32.const 256
        i32.add
        local.get $p4
        local.get $p0
        i32.load
        i32.load offset=28
        call_indirect $__indirect_function_table (type $t4)
        local.get $p0
        local.get $l5
        i32.const 256
        i32.add
        local.get $l5
        i32.const 240
        i32.add
        local.get $p4
        local.get $p0
        i32.load
        i32.load offset=28
        call_indirect $__indirect_function_table (type $t4)
        local.get $p0
        local.get $l5
        i32.const 240
        i32.add
        local.get $l5
        i32.const 224
        i32.add
        local.get $p4
        local.get $p0
        i32.load
        i32.load offset=28
        call_indirect $__indirect_function_table (type $t4)
        local.get $p0
        local.get $l5
        i32.const 224
        i32.add
        local.get $l5
        i32.const 272
        i32.add
        local.get $p4
        local.get $p0
        i32.load
        i32.load offset=28
        call_indirect $__indirect_function_table (type $t4)
        local.get $p0
        local.get $l5
        i32.const 72
        i32.add
        local.get $l5
        i32.const 272
        i32.add
        local.get $p4
        local.get $p0
        i32.load
        i32.load offset=28
        call_indirect $__indirect_function_table (type $t4)
        local.get $p0
        local.get $l5
        i32.const 40
        i32.add
        local.get $l5
        i32.const 256
        i32.add
        local.get $p4
        local.get $p0
        i32.load
        i32.load offset=28
        call_indirect $__indirect_function_table (type $t4)
        local.get $p0
        local.get $l5
        i32.const 8
        i32.add
        local.get $l5
        i32.const 240
        i32.add
        local.get $p4
        local.get $p0
        i32.load
        i32.load offset=28
        call_indirect $__indirect_function_table (type $t4)
        local.get $p0
        local.get $l5
        i32.const 104
        i32.add
        local.get $l5
        i32.const 224
        i32.add
        local.get $p4
        local.get $p0
        i32.load
        i32.load offset=28
        call_indirect $__indirect_function_table (type $t4)
      end
      local.get $l12
      local.get $l16
      f32.add
      local.set $l12
      local.get $l6
      local.get $l23
      f32.mul
      local.set $l16
      local.get $l17
      local.get $l22
      f32.sub
      local.set $l17
      local.get $l7
      local.get $l30
      f32.mul
      local.set $l22
      local.get $l26
      local.get $l28
      f32.sub
      local.set $l26
      local.get $l9
      local.get $l23
      f32.mul
      local.set $l28
      local.get $l8
      local.get $l32
      f32.add
      local.set $l8
      block $B16
        local.get $p1
        i32.load8_u offset=476
        i32.eqz
        br_if $B16
        f32.const 0x0p+0 (;=0;)
        local.set $l6
        f32.const 0x0p+0 (;=0;)
        local.set $l7
        f32.const 0x0p+0 (;=0;)
        local.set $l9
        local.get $p1
        i32.load offset=456
        local.tee $p4
        i32.const 1
        i32.and
        if $I17
          local.get $l10
          local.get $l5
          f32.load offset=128
          f32.mul
          f32.const 0x0p+0 (;=0;)
          f32.add
          local.set $l9
          local.get $l10
          local.get $l5
          f32.load offset=124
          f32.mul
          f32.const 0x0p+0 (;=0;)
          f32.add
          local.set $l7
          local.get $l10
          local.get $l5
          f32.load offset=120
          f32.mul
          f32.const 0x0p+0 (;=0;)
          f32.add
          local.set $l6
        end
        local.get $p4
        i32.const 2
        i32.and
        if $I18
          local.get $l9
          local.get $l19
          local.get $l5
          f32.load offset=140
          f32.mul
          f32.add
          local.set $l9
          local.get $l7
          local.get $l19
          local.get $l5
          f32.load offset=136
          f32.mul
          f32.add
          local.set $l7
          local.get $l6
          local.get $l19
          local.get $l5
          f32.load offset=132
          f32.mul
          f32.add
          local.set $l6
        end
        local.get $p4
        i32.const 4
        i32.and
        if $I19
          local.get $l9
          local.get $l18
          local.get $l5
          f32.load offset=152
          f32.mul
          f32.add
          local.set $l9
          local.get $l7
          local.get $l18
          local.get $l5
          f32.load offset=148
          f32.mul
          f32.add
          local.set $l7
          local.get $l6
          local.get $l18
          local.get $l5
          f32.load offset=144
          f32.mul
          f32.add
          local.set $l6
        end
        local.get $l6
        local.get $l6
        f32.mul
        local.get $l7
        local.get $l7
        f32.mul
        f32.add
        local.get $l9
        local.get $l9
        f32.mul
        f32.add
        f32.sqrt
        local.tee $l6
        local.get $p1
        f32.load offset=464
        f32.gt
        i32.eqz
        br_if $B16
        local.get $p0
        local.get $l5
        i32.const 208
        i32.add
        local.get $l5
        i32.const 176
        i32.add
        i32.const 16711680
        i32.const 65280
        local.get $l6
        local.get $p1
        f32.load offset=124
        f32.gt
        select
        local.get $p0
        i32.load
        i32.load offset=28
        call_indirect $__indirect_function_table (type $t4)
      end
      local.get $l16
      local.get $l12
      f32.add
      local.set $l10
      local.get $l22
      local.get $l17
      f32.add
      local.set $l12
      local.get $l28
      local.get $l26
      f32.add
      local.set $l16
      f32.const 0x0p+0 (;=0;)
      local.set $l6
      block $B20
        local.get $l8
        f32.const 0x0p+0 (;=0;)
        f32.eq
        if $I21
          f32.const 0x1p+0 (;=1;)
          local.set $l7
          f32.const 0x0p+0 (;=0;)
          local.set $l9
          br $B20
        end
        local.get $l10
        f32.const 0x1p+0 (;=1;)
        local.get $l8
        local.get $l8
        f32.mul
        f32.const 0x0p+0 (;=0;)
        f32.add
        local.get $l10
        local.get $l10
        f32.mul
        f32.add
        f32.sqrt
        f32.div
        local.tee $l6
        f32.mul
        local.set $l7
        local.get $l6
        f32.const 0x0p+0 (;=0;)
        f32.mul
        local.set $l9
        local.get $l8
        local.get $l6
        f32.mul
        local.set $l6
      end
      local.get $l5
      local.get $l12
      local.get $l9
      f32.mul
      local.tee $l17
      local.get $l16
      local.get $l9
      f32.mul
      local.tee $l22
      local.get $l8
      local.get $l6
      f32.mul
      local.get $l10
      local.get $l7
      f32.mul
      f32.add
      f32.add
      f32.add
      local.tee $l26
      f32.store offset=116
      local.get $l5
      local.get $l16
      local.get $l6
      f32.mul
      local.get $l12
      local.get $l7
      f32.mul
      local.get $l10
      local.get $l9
      f32.mul
      local.tee $l18
      f32.sub
      local.get $l8
      local.get $l9
      f32.mul
      local.tee $l19
      f32.sub
      f32.add
      local.tee $l28
      f32.store offset=112
      local.get $l5
      local.get $l19
      local.get $l16
      local.get $l7
      f32.mul
      local.get $l18
      f32.sub
      local.get $l12
      local.get $l6
      f32.mul
      f32.sub
      f32.add
      local.tee $l12
      f32.store offset=108
      local.get $l5
      local.get $l17
      local.get $l8
      local.get $l7
      f32.mul
      local.get $l10
      local.get $l6
      f32.mul
      f32.sub
      local.get $l22
      f32.sub
      f32.add
      f32.store offset=104
      local.get $p1
      i32.load offset=456
      local.tee $p4
      i32.const 8
      i32.and
      if $I22
        local.get $l7
        local.get $l7
        f32.mul
        local.get $l9
        local.get $l9
        f32.mul
        local.tee $l8
        local.get $l8
        local.get $l6
        local.get $l6
        f32.mul
        f32.add
        f32.add
        f32.add
        f32.sqrt
        local.tee $l8
        f32.const 0x0p+0 (;=0;)
        f32.ne
        if $I23
          local.get $l7
          f32.const 0x1p+0 (;=1;)
          local.get $l8
          f32.div
          local.tee $l8
          f32.mul
          local.set $l7
          local.get $l6
          local.get $l8
          f32.mul
          local.set $l6
        end
        local.get $l7
        f32.const -0x1p+0 (;=-1;)
        f32.max
        f32.const 0x1p+0 (;=1;)
        f32.min
        call $f35882
        local.tee $l7
        local.get $l7
        f32.add
        local.tee $l7
        f32.neg
        local.get $l7
        local.get $l6
        f32.const 0x0p+0 (;=0;)
        f32.lt
        select
        local.set $l6
        local.get $p0
        local.get $l5
        i32.const 192
        i32.add
        local.get $p1
        f32.load offset=236
        local.tee $l8
        local.get $p1
        f32.load offset=232
        local.tee $l7
        local.get $l8
        block $B24 (result f32)
          block $B25
            local.get $p1
            f32.load offset=224
            f32.const 0x0p+0 (;=0;)
            f32.gt
            br_if $B25
            local.get $p1
            f32.load offset=220
            f32.const 0x0p+0 (;=0;)
            f32.gt
            br_if $B25
            local.get $p1
            f32.load offset=228
            br $B24
          end
          f32.const 0x0p+0 (;=0;)
        end
        local.tee $l9
        f32.add
        local.get $l6
        f32.gt
        local.get $l7
        local.get $l9
        f32.sub
        local.get $l6
        f32.lt
        i32.or
        local.get $p0
        i32.load
        i32.load offset=16
        call_indirect $__indirect_function_table (type $t78)
        local.get $p1
        i32.load offset=456
        local.set $p4
      end
      local.get $p4
      i32.const 48
      i32.and
      i32.const 48
      i32.eq
      if $I26
        local.get $p1
        i32.load8_u offset=478
        if $I27
          local.get $l26
          f32.const 0x1p+0 (;=1;)
          f32.add
          local.set $l7
          f32.const 0x0p+0 (;=0;)
          local.set $l6
          block $B28
            local.get $p1
            f32.load offset=252
            f32.const 0x0p+0 (;=0;)
            f32.gt
            br_if $B28
            local.get $p1
            f32.load offset=248
            f32.const 0x0p+0 (;=0;)
            f32.gt
            br_if $B28
            local.get $p1
            f32.load offset=256
            local.set $l6
          end
          local.get $l28
          local.get $l7
          call $f35884
          local.set $l8
          local.get $l12
          local.get $l7
          call $f35884
          local.set $l7
          local.get $p0
          local.get $l5
          i32.const 192
          i32.add
          local.get $p1
          f32.load offset=264
          local.tee $l9
          f32.const 0x1p-2 (;=0.25;)
          f32.mul
          call $f18177
          local.get $p1
          f32.load offset=260
          local.tee $l23
          f32.const 0x1p-2 (;=0.25;)
          f32.mul
          call $f18177
          local.get $l6
          local.get $l8
          f32.const 0x1p+2 (;=4;)
          f32.mul
          f32.abs
          f32.add
          local.get $l9
          f32.div
          local.tee $l8
          local.get $l8
          f32.mul
          local.get $l6
          local.get $l7
          f32.const 0x1p+2 (;=4;)
          f32.mul
          f32.abs
          f32.add
          local.get $l23
          f32.div
          local.tee $l6
          local.get $l6
          f32.mul
          f32.add
          f32.const 0x1p+0 (;=1;)
          f32.le
          i32.eqz
          local.get $p0
          i32.load
          i32.load offset=20
          call_indirect $__indirect_function_table (type $t78)
        end
        local.get $p1
        i32.load8_u offset=479
        i32.eqz
        br_if $B1
        local.get $p0
        local.get $p1
        local.get $l5
        i32.const 192
        i32.add
        local.get $l5
        i32.const 104
        i32.add
        i32.const 1
        i32.const 1
        call $f72756
        br $B1
      end
      local.get $p4
      i32.const 5
      i32.shr_u
      i32.const 1
      i32.and
      local.get $p4
      i32.const 16
      i32.and
      local.tee $p2
      i32.const 4
      i32.shr_u
      i32.eq
      br_if $B1
      local.get $l30
      local.get $l30
      f32.add
      local.tee $l6
      local.get $l23
      f32.mul
      local.get $l27
      local.get $l27
      f32.add
      local.tee $l7
      local.get $l31
      f32.mul
      f32.sub
      local.set $l8
      local.get $l6
      local.get $l27
      f32.mul
      local.get $l23
      local.get $l23
      f32.add
      local.tee $l6
      local.get $l31
      f32.mul
      f32.add
      local.set $l9
      f32.const 0x1p+0 (;=1;)
      local.get $l27
      local.get $l7
      f32.mul
      f32.sub
      local.get $l23
      local.get $l6
      f32.mul
      f32.sub
      local.set $l6
      local.get $l5
      i32.const 0
      i32.store offset=96
      local.get $l5
      i64.const 0
      i64.store offset=88
      local.get $l5
      i64.const 4554552043086611699
      i64.store offset=80
      local.get $l5
      i64.const -9223372034707292160
      i64.store offset=72
      local.get $l5
      i32.const -64
      i32.sub
      i32.const 0
      i32.store
      local.get $l5
      i64.const 0
      i64.store offset=56
      local.get $l5
      i64.const 4554552039878688768
      i64.store offset=48
      local.get $l5
      i64.const 4554552039878688768
      i64.store offset=40
      local.get $p1
      i32.load offset=452
      local.set $p4
      local.get $p2
      if $I29
        local.get $p1
        i32.load8_u offset=479
        local.set $p2
        local.get $p4
        i32.const 32
        i32.and
        if $I30
          local.get $p2
          i32.const 255
          i32.and
          if $I31
            local.get $p0
            local.get $p1
            local.get $l5
            i32.const 192
            i32.add
            local.get $l5
            i32.const 104
            i32.add
            i32.const 1
            i32.const 0
            call $f72756
            br $B1
          end
          local.get $l5
          i32.const 8
          i32.add
          local.get $l5
          i32.const 192
          i32.add
          local.get $l5
          i32.const 72
          i32.add
          call $f72757
          local.get $p0
          local.get $p1
          local.get $l5
          i32.const 8
          i32.add
          local.get $l12
          local.get $l26
          local.get $p1
          f32.load offset=260
          call $f72758
          br $B1
        end
        local.get $p2
        i32.const 255
        i32.and
        br_if $B1
        local.get $l5
        i32.const 8
        i32.add
        local.get $l5
        i32.const 192
        i32.add
        local.get $l5
        i32.const 40
        i32.add
        call $f72757
        local.get $p0
        local.get $p1
        local.get $l5
        i32.const 8
        i32.add
        local.get $l6
        local.get $l5
        f32.load offset=144
        f32.mul
        local.get $l9
        local.get $l5
        f32.load offset=148
        f32.mul
        f32.add
        local.get $l8
        local.get $l5
        f32.load offset=152
        f32.mul
        f32.add
        local.get $p1
        f32.load offset=260
        call $f72759
        br $B1
      end
      local.get $p1
      i32.load8_u offset=479
      local.set $p2
      local.get $p4
      i32.const 16
      i32.and
      if $I32
        local.get $p2
        i32.const 255
        i32.and
        if $I33
          local.get $p0
          local.get $p1
          local.get $l5
          i32.const 192
          i32.add
          local.get $l5
          i32.const 104
          i32.add
          i32.const 0
          i32.const 1
          call $f72756
          br $B1
        end
        local.get $l5
        i32.const 8
        i32.add
        local.get $l5
        i32.const 192
        i32.add
        local.get $l5
        i32.const 40
        i32.add
        call $f72757
        local.get $p0
        local.get $p1
        local.get $l5
        i32.const 8
        i32.add
        local.get $l28
        local.get $l26
        local.get $p1
        f32.load offset=264
        call $f72758
        br $B1
      end
      local.get $p2
      i32.const 255
      i32.and
      br_if $B1
      local.get $l5
      i32.const 8
      i32.add
      local.get $l5
      i32.const 192
      i32.add
      local.get $l5
      i32.const 72
      i32.add
      call $f72757
      local.get $p0
      local.get $p1
      local.get $l5
      i32.const 8
      i32.add
      local.get $l6
      local.get $l5
      f32.load offset=132
      f32.mul
      local.get $l9
      local.get $l5
      f32.load offset=136
      f32.mul
      f32.add
      local.get $l8
      local.get $l5
      f32.load offset=140
      f32.mul
      f32.add
      local.get $p1
      f32.load offset=264
      call $f72759
    end
    local.get $l5
    i32.const 288
    i32.add
    global.set $g0)
