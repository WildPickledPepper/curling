  (func $f70010 (type $t9) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (result i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 i64)
    global.get $g0
    i32.const 192
    i32.sub
    local.tee $l7
    global.set $g0
    local.get $p1
    i32.const 124
    i32.add
    local.set $p1
    local.get $p3
    f32.load offset=4
    local.set $l15
    block $B0 (result i32)
      block $B1
        local.get $p3
        f32.load
        local.tee $l16
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        local.get $l15
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        f32.const 0x1p+0 (;=1;)
        local.set $l15
        local.get $p3
        f32.load offset=8
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B1
        local.get $l7
        i64.const 0
        i64.store offset=152
        local.get $l7
        i32.const 1065353216
        i32.store offset=148
        local.get $l7
        i64.const 0
        i64.store offset=160
        local.get $l7
        i64.const 0
        i64.store offset=172 align=4
        local.get $l7
        i32.const 1065353216
        i32.store offset=168
        local.get $l7
        i64.const 0
        i64.store offset=180 align=4
        local.get $l7
        i32.const 1065353216
        i32.store offset=188
        local.get $l7
        i64.const 0
        i64.store offset=132 align=4
        local.get $l7
        i32.const 1065353216
        i32.store offset=128
        local.get $l7
        i64.const 0
        i64.store offset=140 align=4
        block $B2 (result i32)
          block $B3
            local.get $p2
            i32.load
            local.tee $l5
            if $I4
              local.get $p2
              f32.load offset=4
              local.set $l16
              br $B3
            end
            local.get $p2
            i32.load offset=4
            local.tee $p3
            f32.reinterpret_i32
            local.set $l16
            local.get $p3
            br_if $B3
            local.get $p2
            i32.load offset=8
            br_if $B3
            i32.const 0
            local.get $p2
            i32.load offset=12
            i32.const 1065353216
            i32.eq
            br_if $B2
            drop
          end
          local.get $p2
          f32.load offset=8
          local.set $l15
          local.get $p2
          f32.load offset=12
          local.set $l17
          local.get $l7
          i32.const 0
          i32.store offset=156
          local.get $l7
          local.get $l15
          local.get $l16
          local.get $l16
          f32.add
          local.tee $l19
          f32.mul
          local.tee $l21
          local.get $l17
          local.get $l5
          f32.reinterpret_i32
          local.tee $l20
          local.get $l20
          f32.add
          local.tee $l18
          f32.mul
          local.tee $l25
          f32.sub
          f32.store offset=164
          local.get $l7
          i32.const 0
          i32.store offset=172
          local.get $l7
          i32.const 0
          i32.store offset=140
          local.get $l7
          local.get $l18
          local.get $l15
          f32.mul
          local.tee $l22
          local.get $l19
          local.get $l17
          f32.mul
          local.tee $l24
          f32.add
          f32.store offset=160
          local.get $l7
          local.get $l21
          local.get $l25
          f32.add
          f32.store offset=152
          local.get $l7
          local.get $l22
          local.get $l24
          f32.sub
          f32.store offset=136
          local.get $l7
          f32.const 0x1p+0 (;=1;)
          local.get $l18
          local.get $l20
          f32.mul
          f32.sub
          local.tee $l20
          local.get $l16
          local.get $l19
          f32.mul
          local.tee $l19
          f32.sub
          f32.store offset=168
          local.get $l7
          local.get $l20
          local.get $l15
          local.get $l15
          local.get $l15
          f32.add
          local.tee $l21
          f32.mul
          local.tee $l15
          f32.sub
          f32.store offset=148
          local.get $l7
          local.get $l18
          local.get $l16
          f32.mul
          local.tee $l16
          local.get $l21
          local.get $l17
          f32.mul
          local.tee $l17
          f32.sub
          f32.store offset=144
          local.get $l7
          local.get $l16
          local.get $l17
          f32.add
          f32.store offset=132
          local.get $l7
          f32.const 0x1p+0 (;=1;)
          local.get $l19
          f32.sub
          local.get $l15
          f32.sub
          f32.store offset=128
          local.get $l7
          i32.const 128
          i32.add
        end
        local.set $p3
        block $B5
          block $B6
            local.get $p2
            i32.load offset=16
            local.tee $l5
            if $I7
              local.get $p2
              f32.load offset=20
              local.set $l15
              br $B6
            end
            local.get $p2
            i32.load offset=20
            local.tee $l6
            f32.reinterpret_i32
            local.set $l15
            local.get $l6
            br_if $B6
            local.get $p2
            i32.load offset=24
            i32.eqz
            br_if $B5
          end
          local.get $l7
          local.get $l15
          f32.store offset=180
          local.get $l7
          local.get $l5
          i32.store offset=176
          local.get $l7
          local.get $p2
          f32.load offset=24
          f32.store offset=184
          local.get $l7
          i32.const 128
          i32.add
          local.set $p3
        end
        block $B8
          local.get $p4
          if $I9
            local.get $p4
            block $B10 (result i32)
              local.get $p4
              i32.load
              local.set $l9
              local.get $p4
              i32.load offset=8
              local.set $l8
              local.get $p4
              i32.const 20
              i32.add
              local.set $p2
              global.get $g0
              i32.const 1168
              i32.sub
              local.tee $l5
              global.set $g0
              local.get $p1
              i32.load
              local.set $l6
              local.get $l5
              local.get $l9
              i32.store offset=88
              local.get $l5
              local.get $l8
              i32.store offset=84
              local.get $l5
              i32.const 0
              i32.store offset=80
              local.get $l5
              local.get $p0
              local.tee $p4
              f32.load offset=12
              local.tee $l15
              local.get $l15
              f32.mul
              local.tee $l17
              f32.store offset=60
              block $B11 (result f32)
                local.get $p3
                if $I12
                  local.get $p3
                  f32.load offset=32
                  local.tee $l15
                  local.get $p4
                  f32.load
                  local.tee $l19
                  f32.mul
                  local.get $p3
                  f32.load offset=36
                  local.tee $l16
                  local.get $p4
                  f32.load offset=4
                  local.tee $l18
                  f32.mul
                  f32.add
                  local.get $p3
                  f32.load offset=40
                  local.tee $l20
                  local.get $p4
                  f32.load offset=8
                  local.tee $l21
                  f32.mul
                  f32.add
                  local.get $p3
                  f32.load offset=48
                  local.tee $l24
                  local.get $l15
                  f32.mul
                  local.get $p3
                  f32.load offset=52
                  local.tee $l22
                  local.get $l16
                  f32.mul
                  f32.add
                  local.get $p3
                  f32.load offset=56
                  local.tee $l23
                  local.get $l20
                  f32.mul
                  f32.add
                  f32.sub
                  local.set $l15
                  local.get $p3
                  f32.load offset=16
                  local.tee $l16
                  local.get $l19
                  f32.mul
                  local.get $p3
                  f32.load offset=20
                  local.tee $l20
                  local.get $l18
                  f32.mul
                  f32.add
                  local.get $p3
                  f32.load offset=24
                  local.tee $l25
                  local.get $l21
                  f32.mul
                  f32.add
                  local.get $l24
                  local.get $l16
                  f32.mul
                  local.get $l22
                  local.get $l20
                  f32.mul
                  f32.add
                  local.get $l23
                  local.get $l25
                  f32.mul
                  f32.add
                  f32.sub
                  local.set $l16
                  local.get $p3
                  f32.load
                  local.tee $l20
                  local.get $l19
                  f32.mul
                  local.get $p3
                  f32.load offset=4
                  local.tee $l19
                  local.get $l18
                  f32.mul
                  f32.add
                  local.get $p3
                  f32.load offset=8
                  local.tee $l18
                  local.get $l21
                  f32.mul
                  f32.add
                  local.get $l24
                  local.get $l20
                  f32.mul
                  local.get $l22
                  local.get $l19
                  f32.mul
                  f32.add
                  local.get $l23
                  local.get $l18
                  f32.mul
                  f32.add
                  f32.sub
                  br $B11
                end
                local.get $p4
                f32.load offset=8
                local.set $l15
                local.get $p4
                f32.load offset=4
                local.set $l16
                local.get $p4
                f32.load
              end
              local.set $l19
              local.get $l5
              local.get $l15
              local.get $l15
              f32.add
              f32.store offset=72
              local.get $l5
              local.get $l16
              local.get $l16
              f32.add
              f32.store offset=68
              local.get $l5
              local.get $l15
              f32.store offset=56
              local.get $l5
              local.get $l16
              f32.store offset=52
              local.get $l5
              local.get $l17
              f32.const 0x1p+2 (;=4;)
              f32.mul
              f32.store offset=76
              local.get $l5
              local.get $l19
              f32.store offset=48
              local.get $l5
              local.get $l19
              local.get $l19
              f32.add
              f32.store offset=64
              local.get $l5
              local.get $l6
              i32.load offset=16
              local.tee $p4
              i32.store
              local.get $l5
              local.get $l6
              i32.load offset=20
              local.tee $l8
              i32.store offset=4
              local.get $l5
              local.get $l6
              i32.load offset=4
              i32.store offset=8
              local.get $p1
              f32.load offset=40
              local.set $l15
              local.get $p1
              i64.load offset=32 align=4
              local.set $l34
              local.get $l5
              local.get $p1
              f32.load offset=44
              local.tee $l16
              f32.store offset=28
              local.get $l5
              local.get $l15
              f32.store offset=24
              local.get $l5
              local.get $l34
              i64.store offset=16
              local.get $p1
              i64.load offset=48 align=4
              local.set $l34
              local.get $l5
              local.get $p1
              f32.load offset=56
              f32.store offset=44
              local.get $l5
              local.get $l34
              i64.store offset=36 align=4
              local.get $l5
              local.get $l16
              f32.store offset=32
              local.get $p2
              block $B13 (result i32)
                local.get $p1
                i32.load offset=24
                local.tee $l12
                if $I14
                  local.get $l5
                  local.get $p1
                  i32.load offset=28
                  i32.store offset=96
                  local.get $l5
                  i32.const 48
                  i32.add
                  local.set $l11
                  i32.const 1
                  local.set $p0
                  block $B15 (result i32)
                    loop $L16
                      local.get $l12
                      local.get $l5
                      i32.const 96
                      i32.add
                      local.get $p0
                      i32.const 1
                      i32.sub
                      local.tee $p2
                      i32.const 2
                      i32.shl
                      i32.add
                      local.tee $p1
                      i32.load
                      local.tee $p4
                      i32.const 11
                      i32.shr_u
                      i32.const 4
                      i32.shl
                      i32.add
                      local.set $p3
                      block $B17
                        block $B18
                          block $B19
                            block $B20
                              local.get $p4
                              i32.const 1
                              i32.shr_u
                              i32.const 3
                              i32.and
                              local.tee $l13
                              i32.const 2
                              i32.ge_u
                              if $I21
                                local.get $l5
                                f32.load offset=76
                                local.tee $l19
                                local.get $l5
                                f32.load offset=64
                                local.tee $l15
                                local.get $l5
                                f32.load offset=16
                                local.tee $l16
                                local.get $p3
                                i32.load16_s offset=12
                                f32.convert_i32_s
                                f32.mul
                                local.tee $l21
                                local.get $l5
                                f32.load offset=32
                                local.tee $l17
                                local.get $p3
                                i32.load16_s offset=14
                                f32.convert_i32_s
                                f32.mul
                                local.tee $l24
                                f32.add
                                f32.sub
                                local.tee $l18
                                local.get $l18
                                local.get $l24
                                local.get $l21
                                f32.sub
                                local.tee $l21
                                local.get $l18
                                local.get $l21
                                f32.lt
                                select
                                local.tee $l18
                                local.get $l21
                                f32.neg
                                local.tee $l21
                                local.get $l18
                                local.get $l21
                                f32.gt
                                select
                                f32.sub
                                local.tee $l18
                                local.get $l18
                                f32.mul
                                local.get $l5
                                f32.load offset=68
                                local.tee $l18
                                local.get $l5
                                f32.load offset=20
                                local.tee $l21
                                local.get $p3
                                i32.load16_s offset=28
                                f32.convert_i32_s
                                f32.mul
                                local.tee $l23
                                local.get $l5
                                f32.load offset=36
                                local.tee $l24
                                local.get $p3
                                i32.load16_s offset=30
                                f32.convert_i32_s
                                f32.mul
                                local.tee $l20
                                f32.add
                                f32.sub
                                local.tee $l22
                                local.get $l22
                                local.get $l20
                                local.get $l23
                                f32.sub
                                local.tee $l23
                                local.get $l22
                                local.get $l23
                                f32.lt
                                select
                                local.tee $l22
                                local.get $l23
                                f32.neg
                                local.tee $l23
                                local.get $l22
                                local.get $l23
                                f32.gt
                                select
                                f32.sub
                                local.tee $l22
                                local.get $l22
                                f32.mul
                                f32.add
                                local.get $l5
                                f32.load offset=72
                                local.tee $l22
                                local.get $l5
                                f32.load offset=24
                                local.tee $l23
                                local.get $p3
                                i32.load16_s offset=44
                                f32.convert_i32_s
                                f32.mul
                                local.tee $l26
                                local.get $l5
                                f32.load offset=40
                                local.tee $l20
                                local.get $p3
                                i32.load16_s offset=46
                                f32.convert_i32_s
                                f32.mul
                                local.tee $l27
                                f32.add
                                f32.sub
                                local.tee $l25
                                local.get $l25
                                local.get $l27
                                local.get $l26
                                f32.sub
                                local.tee $l26
                                local.get $l25
                                local.get $l26
                                f32.lt
                                select
                                local.tee $l25
                                local.get $l26
                                f32.neg
                                local.tee $l26
                                local.get $l25
                                local.get $l26
                                f32.gt
                                select
                                f32.sub
                                local.tee $l25
                                local.get $l25
                                f32.mul
                                f32.add
                                f32.ge
                                i32.eqz
                                br_if $B20
                                local.get $p3
                                i32.load offset=60
                                local.tee $l8
                                i32.const 1
                                i32.and
                                i32.eqz
                                br_if $B19
                                local.get $l8
                                i32.const 5
                                i32.shr_u
                                local.set $p4
                                local.get $l8
                                i32.const 1
                                i32.shr_u
                                i32.const 15
                                i32.and
                                local.set $l8
                                loop $L22
                                  block $B23
                                    local.get $l5
                                    f32.load offset=60
                                    local.get $l5
                                    i32.load offset=8
                                    local.tee $l6
                                    block $B24 (result i32)
                                      local.get $l5
                                      i32.load
                                      local.tee $p1
                                      if $I25
                                        local.get $p1
                                        local.get $p4
                                        i32.const 12
                                        i32.mul
                                        i32.add
                                        local.tee $p1
                                        i32.load offset=8
                                        local.set $l10
                                        local.get $p1
                                        i32.load offset=4
                                        local.set $l9
                                        local.get $p1
                                        i32.load
                                        br $B24
                                      end
                                      local.get $l5
                                      i32.load offset=4
                                      local.get $p4
                                      i32.const 6
                                      i32.mul
                                      i32.add
                                      local.tee $p1
                                      i32.load16_u offset=4
                                      local.set $l10
                                      local.get $p1
                                      i32.load16_u offset=2
                                      local.set $l9
                                      local.get $p1
                                      i32.load16_u
                                    end
                                    i32.const 12
                                    i32.mul
                                    i32.add
                                    local.tee $p1
                                    f32.load
                                    local.tee $l16
                                    local.get $l5
                                    f32.load offset=48
                                    f32.sub
                                    local.tee $l15
                                    local.get $l15
                                    f32.mul
                                    local.get $p1
                                    f32.load offset=4
                                    local.tee $l19
                                    local.get $l5
                                    f32.load offset=52
                                    f32.sub
                                    local.tee $l15
                                    local.get $l15
                                    f32.mul
                                    f32.add
                                    local.get $p1
                                    f32.load offset=8
                                    local.tee $l17
                                    local.get $l5
                                    f32.load offset=56
                                    f32.sub
                                    local.tee $l15
                                    local.get $l15
                                    f32.mul
                                    f32.add
                                    f32.ge
                                    i32.eqz
                                    if $I26
                                      local.get $l6
                                      local.get $l9
                                      i32.const 12
                                      i32.mul
                                      i32.add
                                      local.tee $l9
                                      f32.load offset=4
                                      local.set $l15
                                      local.get $l9
                                      f32.load offset=8
                                      local.set $l18
                                      local.get $l5
                                      local.get $l9
                                      f32.load
                                      local.get $l16
                                      f32.sub
                                      f32.store offset=1152
                                      local.get $l5
                                      local.get $l18
                                      local.get $l17
                                      f32.sub
                                      f32.store offset=1160
                                      local.get $l5
                                      local.get $l15
                                      local.get $l19
                                      f32.sub
                                      f32.store offset=1156
                                      local.get $l6
                                      local.get $l10
                                      i32.const 12
                                      i32.mul
                                      i32.add
                                      local.tee $l6
                                      f32.load offset=4
                                      local.set $l15
                                      local.get $l6
                                      f32.load
                                      local.set $l18
                                      local.get $l5
                                      local.get $l6
                                      f32.load offset=8
                                      local.get $l17
                                      f32.sub
                                      f32.store offset=1144
                                      local.get $l5
                                      local.get $l15
                                      local.get $l19
                                      f32.sub
                                      f32.store offset=1140
                                      local.get $l5
                                      local.get $l18
                                      local.get $l16
                                      f32.sub
                                      f32.store offset=1136
                                      local.get $l5
                                      i32.const 1120
                                      i32.add
                                      local.get $l11
                                      local.get $p1
                                      local.get $l9
                                      local.get $l6
                                      local.get $l5
                                      i32.const 1152
                                      i32.add
                                      local.get $l5
                                      i32.const 1136
                                      i32.add
                                      call $f69961
                                      local.get $l5
                                      f32.load offset=60
                                      local.get $l5
                                      f32.load offset=1120
                                      local.get $l5
                                      f32.load offset=48
                                      f32.sub
                                      local.tee $l15
                                      local.get $l15
                                      f32.mul
                                      local.get $l5
                                      f32.load offset=1124
                                      local.get $l5
                                      f32.load offset=52
                                      f32.sub
                                      local.tee $l15
                                      local.get $l15
                                      f32.mul
                                      f32.add
                                      local.get $l5
                                      f32.load offset=1128
                                      local.get $l5
                                      f32.load offset=56
                                      f32.sub
                                      local.tee $l15
                                      local.get $l15
                                      f32.mul
                                      f32.add
                                      f32.ge
                                      i32.eqz
                                      br_if $B23
                                    end
                                    i32.const 1
                                    local.get $l5
                                    i32.load offset=80
                                    local.tee $p1
                                    local.get $l5
                                    i32.load offset=84
                                    i32.eq
                                    br_if $B15
                                    drop
                                    local.get $l5
                                    i32.load offset=88
                                    local.get $p1
                                    i32.const 2
                                    i32.shl
                                    i32.add
                                    local.get $p4
                                    i32.store
                                    local.get $l5
                                    local.get $l5
                                    i32.load offset=80
                                    i32.const 1
                                    i32.add
                                    i32.store offset=80
                                  end
                                  local.get $p4
                                  i32.const 1
                                  i32.add
                                  local.set $p4
                                  local.get $l8
                                  i32.const 1
                                  i32.sub
                                  local.tee $l8
                                  br_if $L22
                                end
                              end
                              local.get $l13
                              i32.eqz
                              br_if $B17
                              local.get $l5
                              f32.load offset=76
                              local.set $l19
                              local.get $l5
                              f32.load offset=72
                              local.set $l22
                              local.get $l5
                              f32.load offset=68
                              local.set $l18
                              local.get $l5
                              f32.load offset=64
                              local.set $l15
                              local.get $l5
                              f32.load offset=40
                              local.set $l20
                              local.get $l5
                              f32.load offset=36
                              local.set $l24
                              local.get $l5
                              f32.load offset=32
                              local.set $l17
                              local.get $l5
                              f32.load offset=24
                              local.set $l23
                              local.get $l5
                              f32.load offset=20
                              local.set $l21
                              local.get $l5
                              f32.load offset=16
                              local.set $l16
                            end
                            local.get $p2
                            local.set $p0
                            br $B18
                          end
                          local.get $p1
                          local.get $l8
                          i32.store
                        end
                        local.get $l19
                        local.get $l15
                        local.get $l16
                        local.get $p3
                        i32.load16_s offset=8
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l16
                        local.get $l17
                        local.get $p3
                        i32.load16_s offset=10
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l17
                        f32.add
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        local.get $l17
                        local.get $l16
                        f32.sub
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.lt
                        select
                        local.tee $l15
                        local.get $l16
                        f32.neg
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.gt
                        select
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        f32.mul
                        local.get $l18
                        local.get $l21
                        local.get $p3
                        i32.load16_s offset=24
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l16
                        local.get $l24
                        local.get $p3
                        i32.load16_s offset=26
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l17
                        f32.add
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        local.get $l17
                        local.get $l16
                        f32.sub
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.lt
                        select
                        local.tee $l15
                        local.get $l16
                        f32.neg
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.gt
                        select
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        f32.mul
                        f32.add
                        local.get $l22
                        local.get $l23
                        local.get $p3
                        i32.load16_s offset=40
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l16
                        local.get $l20
                        local.get $p3
                        i32.load16_s offset=42
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l17
                        f32.add
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        local.get $l17
                        local.get $l16
                        f32.sub
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.lt
                        select
                        local.tee $l15
                        local.get $l16
                        f32.neg
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.gt
                        select
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        f32.mul
                        f32.add
                        f32.ge
                        i32.eqz
                        if $I27
                          local.get $p0
                          local.set $p2
                          br $B17
                        end
                        local.get $p3
                        i32.load offset=56
                        local.tee $p1
                        i32.const 1
                        i32.and
                        if $I28
                          local.get $p1
                          i32.const 5
                          i32.shr_u
                          local.set $p4
                          local.get $p1
                          i32.const 1
                          i32.shr_u
                          i32.const 15
                          i32.and
                          local.set $l8
                          loop $L29
                            block $B30
                              local.get $l5
                              f32.load offset=60
                              local.get $l5
                              i32.load offset=8
                              local.tee $l6
                              block $B31 (result i32)
                                local.get $l5
                                i32.load
                                local.tee $p1
                                if $I32
                                  local.get $p1
                                  local.get $p4
                                  i32.const 12
                                  i32.mul
                                  i32.add
                                  local.tee $p1
                                  i32.load offset=8
                                  local.set $l10
                                  local.get $p1
                                  i32.load offset=4
                                  local.set $l9
                                  local.get $p1
                                  i32.load
                                  br $B31
                                end
                                local.get $l5
                                i32.load offset=4
                                local.get $p4
                                i32.const 6
                                i32.mul
                                i32.add
                                local.tee $p1
                                i32.load16_u offset=4
                                local.set $l10
                                local.get $p1
                                i32.load16_u offset=2
                                local.set $l9
                                local.get $p1
                                i32.load16_u
                              end
                              i32.const 12
                              i32.mul
                              i32.add
                              local.tee $p1
                              f32.load
                              local.tee $l15
                              local.get $l5
                              f32.load offset=48
                              f32.sub
                              local.tee $l16
                              local.get $l16
                              f32.mul
                              local.get $p1
                              f32.load offset=4
                              local.tee $l16
                              local.get $l5
                              f32.load offset=52
                              f32.sub
                              local.tee $l19
                              local.get $l19
                              f32.mul
                              f32.add
                              local.get $p1
                              f32.load offset=8
                              local.tee $l19
                              local.get $l5
                              f32.load offset=56
                              f32.sub
                              local.tee $l17
                              local.get $l17
                              f32.mul
                              f32.add
                              f32.ge
                              i32.eqz
                              if $I33
                                local.get $l6
                                local.get $l9
                                i32.const 12
                                i32.mul
                                i32.add
                                local.tee $l9
                                f32.load offset=4
                                local.set $l17
                                local.get $l9
                                f32.load offset=8
                                local.set $l18
                                local.get $l5
                                local.get $l9
                                f32.load
                                local.get $l15
                                f32.sub
                                f32.store offset=1152
                                local.get $l5
                                local.get $l18
                                local.get $l19
                                f32.sub
                                f32.store offset=1160
                                local.get $l5
                                local.get $l17
                                local.get $l16
                                f32.sub
                                f32.store offset=1156
                                local.get $l6
                                local.get $l10
                                i32.const 12
                                i32.mul
                                i32.add
                                local.tee $l6
                                f32.load offset=4
                                local.set $l17
                                local.get $l6
                                f32.load
                                local.set $l18
                                local.get $l5
                                local.get $l6
                                f32.load offset=8
                                local.get $l19
                                f32.sub
                                f32.store offset=1144
                                local.get $l5
                                local.get $l17
                                local.get $l16
                                f32.sub
                                f32.store offset=1140
                                local.get $l5
                                local.get $l18
                                local.get $l15
                                f32.sub
                                f32.store offset=1136
                                local.get $l5
                                i32.const 1120
                                i32.add
                                local.get $l11
                                local.get $p1
                                local.get $l9
                                local.get $l6
                                local.get $l5
                                i32.const 1152
                                i32.add
                                local.get $l5
                                i32.const 1136
                                i32.add
                                call $f69961
                                local.get $l5
                                f32.load offset=60
                                local.get $l5
                                f32.load offset=1120
                                local.get $l5
                                f32.load offset=48
                                f32.sub
                                local.tee $l15
                                local.get $l15
                                f32.mul
                                local.get $l5
                                f32.load offset=1124
                                local.get $l5
                                f32.load offset=52
                                f32.sub
                                local.tee $l15
                                local.get $l15
                                f32.mul
                                f32.add
                                local.get $l5
                                f32.load offset=1128
                                local.get $l5
                                f32.load offset=56
                                f32.sub
                                local.tee $l15
                                local.get $l15
                                f32.mul
                                f32.add
                                f32.ge
                                i32.eqz
                                br_if $B30
                              end
                              i32.const 1
                              local.get $l5
                              i32.load offset=80
                              local.tee $p1
                              local.get $l5
                              i32.load offset=84
                              i32.eq
                              br_if $B15
                              drop
                              local.get $l5
                              i32.load offset=88
                              local.get $p1
                              i32.const 2
                              i32.shl
                              i32.add
                              local.get $p4
                              i32.store
                              local.get $l5
                              local.get $l5
                              i32.load offset=80
                              i32.const 1
                              i32.add
                              i32.store offset=80
                            end
                            local.get $p4
                            i32.const 1
                            i32.add
                            local.set $p4
                            local.get $l8
                            i32.const 1
                            i32.sub
                            local.tee $l8
                            br_if $L29
                          end
                          local.get $p0
                          local.set $p2
                          br $B17
                        end
                        local.get $l5
                        i32.const 96
                        i32.add
                        local.get $p0
                        i32.const 2
                        i32.shl
                        i32.add
                        local.get $p1
                        i32.store
                        local.get $p0
                        i32.const 1
                        i32.add
                        local.set $p2
                      end
                      block $B34
                        local.get $l5
                        f32.load offset=76
                        local.tee $l19
                        local.get $l5
                        f32.load offset=64
                        local.tee $l17
                        local.get $l5
                        f32.load offset=16
                        local.tee $l18
                        local.get $p3
                        i32.load16_s offset=4
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l16
                        local.get $l5
                        f32.load offset=32
                        local.tee $l21
                        local.get $p3
                        i32.load16_s offset=6
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l24
                        f32.add
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        local.get $l24
                        local.get $l16
                        f32.sub
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.lt
                        select
                        local.tee $l15
                        local.get $l16
                        f32.neg
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.gt
                        select
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        f32.mul
                        local.get $l5
                        f32.load offset=68
                        local.tee $l24
                        local.get $l5
                        f32.load offset=20
                        local.tee $l22
                        local.get $p3
                        i32.load16_s offset=20
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l16
                        local.get $l5
                        f32.load offset=36
                        local.tee $l23
                        local.get $p3
                        i32.load16_s offset=22
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l20
                        f32.add
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        local.get $l20
                        local.get $l16
                        f32.sub
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.lt
                        select
                        local.tee $l15
                        local.get $l16
                        f32.neg
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.gt
                        select
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        f32.mul
                        f32.add
                        local.get $l5
                        f32.load offset=72
                        local.tee $l20
                        local.get $l5
                        f32.load offset=24
                        local.tee $l25
                        local.get $p3
                        i32.load16_s offset=36
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l16
                        local.get $l5
                        f32.load offset=40
                        local.tee $l26
                        local.get $p3
                        i32.load16_s offset=38
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l27
                        f32.add
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        local.get $l27
                        local.get $l16
                        f32.sub
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.lt
                        select
                        local.tee $l15
                        local.get $l16
                        f32.neg
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.gt
                        select
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        f32.mul
                        f32.add
                        f32.ge
                        i32.eqz
                        br_if $B34
                        local.get $p3
                        i32.load offset=52
                        local.tee $p1
                        i32.const 1
                        i32.and
                        if $I35
                          local.get $p1
                          i32.const 5
                          i32.shr_u
                          local.set $p4
                          local.get $p1
                          i32.const 1
                          i32.shr_u
                          i32.const 15
                          i32.and
                          local.set $l8
                          loop $L36
                            block $B37
                              local.get $l5
                              f32.load offset=60
                              local.get $l5
                              i32.load offset=8
                              local.tee $l6
                              block $B38 (result i32)
                                local.get $l5
                                i32.load
                                local.tee $p1
                                if $I39
                                  local.get $p1
                                  local.get $p4
                                  i32.const 12
                                  i32.mul
                                  i32.add
                                  local.tee $p1
                                  i32.load offset=8
                                  local.set $l10
                                  local.get $p1
                                  i32.load offset=4
                                  local.set $l9
                                  local.get $p1
                                  i32.load
                                  br $B38
                                end
                                local.get $l5
                                i32.load offset=4
                                local.get $p4
                                i32.const 6
                                i32.mul
                                i32.add
                                local.tee $p1
                                i32.load16_u offset=4
                                local.set $l10
                                local.get $p1
                                i32.load16_u offset=2
                                local.set $l9
                                local.get $p1
                                i32.load16_u
                              end
                              i32.const 12
                              i32.mul
                              i32.add
                              local.tee $p1
                              f32.load
                              local.tee $l15
                              local.get $l5
                              f32.load offset=48
                              f32.sub
                              local.tee $l16
                              local.get $l16
                              f32.mul
                              local.get $p1
                              f32.load offset=4
                              local.tee $l16
                              local.get $l5
                              f32.load offset=52
                              f32.sub
                              local.tee $l19
                              local.get $l19
                              f32.mul
                              f32.add
                              local.get $p1
                              f32.load offset=8
                              local.tee $l19
                              local.get $l5
                              f32.load offset=56
                              f32.sub
                              local.tee $l17
                              local.get $l17
                              f32.mul
                              f32.add
                              f32.ge
                              i32.eqz
                              if $I40
                                local.get $l6
                                local.get $l9
                                i32.const 12
                                i32.mul
                                i32.add
                                local.tee $l9
                                f32.load offset=4
                                local.set $l17
                                local.get $l9
                                f32.load offset=8
                                local.set $l18
                                local.get $l5
                                local.get $l9
                                f32.load
                                local.get $l15
                                f32.sub
                                f32.store offset=1152
                                local.get $l5
                                local.get $l18
                                local.get $l19
                                f32.sub
                                f32.store offset=1160
                                local.get $l5
                                local.get $l17
                                local.get $l16
                                f32.sub
                                f32.store offset=1156
                                local.get $l6
                                local.get $l10
                                i32.const 12
                                i32.mul
                                i32.add
                                local.tee $l6
                                f32.load offset=4
                                local.set $l17
                                local.get $l6
                                f32.load
                                local.set $l18
                                local.get $l5
                                local.get $l6
                                f32.load offset=8
                                local.get $l19
                                f32.sub
                                f32.store offset=1144
                                local.get $l5
                                local.get $l17
                                local.get $l16
                                f32.sub
                                f32.store offset=1140
                                local.get $l5
                                local.get $l18
                                local.get $l15
                                f32.sub
                                f32.store offset=1136
                                local.get $l5
                                i32.const 1120
                                i32.add
                                local.get $l11
                                local.get $p1
                                local.get $l9
                                local.get $l6
                                local.get $l5
                                i32.const 1152
                                i32.add
                                local.get $l5
                                i32.const 1136
                                i32.add
                                call $f69961
                                local.get $l5
                                f32.load offset=60
                                local.get $l5
                                f32.load offset=1120
                                local.get $l5
                                f32.load offset=48
                                f32.sub
                                local.tee $l15
                                local.get $l15
                                f32.mul
                                local.get $l5
                                f32.load offset=1124
                                local.get $l5
                                f32.load offset=52
                                f32.sub
                                local.tee $l15
                                local.get $l15
                                f32.mul
                                f32.add
                                local.get $l5
                                f32.load offset=1128
                                local.get $l5
                                f32.load offset=56
                                f32.sub
                                local.tee $l15
                                local.get $l15
                                f32.mul
                                f32.add
                                f32.ge
                                i32.eqz
                                br_if $B37
                              end
                              i32.const 1
                              local.get $l5
                              i32.load offset=80
                              local.tee $p1
                              local.get $l5
                              i32.load offset=84
                              i32.eq
                              br_if $B15
                              drop
                              local.get $l5
                              i32.load offset=88
                              local.get $p1
                              i32.const 2
                              i32.shl
                              i32.add
                              local.get $p4
                              i32.store
                              local.get $l5
                              local.get $l5
                              i32.load offset=80
                              i32.const 1
                              i32.add
                              i32.store offset=80
                            end
                            local.get $p4
                            i32.const 1
                            i32.add
                            local.set $p4
                            local.get $l8
                            i32.const 1
                            i32.sub
                            local.tee $l8
                            br_if $L36
                          end
                          local.get $l5
                          f32.load offset=76
                          local.set $l19
                          local.get $l5
                          f32.load offset=72
                          local.set $l20
                          local.get $l5
                          f32.load offset=68
                          local.set $l24
                          local.get $l5
                          f32.load offset=64
                          local.set $l17
                          local.get $l5
                          f32.load offset=40
                          local.set $l26
                          local.get $l5
                          f32.load offset=36
                          local.set $l23
                          local.get $l5
                          f32.load offset=32
                          local.set $l21
                          local.get $l5
                          f32.load offset=24
                          local.set $l25
                          local.get $l5
                          f32.load offset=20
                          local.set $l22
                          local.get $l5
                          f32.load offset=16
                          local.set $l18
                          br $B34
                        end
                        local.get $l5
                        i32.const 96
                        i32.add
                        local.get $p2
                        i32.const 2
                        i32.shl
                        i32.add
                        local.get $p1
                        i32.store
                        local.get $p2
                        i32.const 1
                        i32.add
                        local.set $p2
                      end
                      block $B41 (result i32)
                        local.get $p2
                        local.get $l19
                        local.get $l17
                        local.get $l18
                        local.get $p3
                        i32.load16_s
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l16
                        local.get $l21
                        local.get $p3
                        i32.load16_s offset=2
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l18
                        f32.add
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        local.get $l18
                        local.get $l16
                        f32.sub
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.lt
                        select
                        local.tee $l15
                        local.get $l16
                        f32.neg
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.gt
                        select
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        f32.mul
                        local.get $l24
                        local.get $l22
                        local.get $p3
                        i32.load16_s offset=16
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l16
                        local.get $l23
                        local.get $p3
                        i32.load16_s offset=18
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l17
                        f32.add
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        local.get $l17
                        local.get $l16
                        f32.sub
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.lt
                        select
                        local.tee $l15
                        local.get $l16
                        f32.neg
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.gt
                        select
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        f32.mul
                        f32.add
                        local.get $l20
                        local.get $l25
                        local.get $p3
                        i32.load16_s offset=32
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l16
                        local.get $l26
                        local.get $p3
                        i32.load16_s offset=34
                        f32.convert_i32_s
                        f32.mul
                        local.tee $l17
                        f32.add
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        local.get $l17
                        local.get $l16
                        f32.sub
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.lt
                        select
                        local.tee $l15
                        local.get $l16
                        f32.neg
                        local.tee $l16
                        local.get $l15
                        local.get $l16
                        f32.gt
                        select
                        f32.sub
                        local.tee $l15
                        local.get $l15
                        f32.mul
                        f32.add
                        f32.ge
                        i32.eqz
                        br_if $B41
                        drop
                        local.get $p3
                        i32.load offset=48
                        local.tee $p4
                        i32.const 1
                        i32.and
                        if $I42
                          local.get $p4
                          i32.const 5
                          i32.shr_u
                          local.set $p3
                          local.get $p4
                          i32.const 1
                          i32.shr_u
                          i32.const 15
                          i32.and
                          local.set $p1
                          loop $L43
                            block $B44
                              local.get $l5
                              f32.load offset=60
                              local.get $l5
                              i32.load offset=8
                              local.tee $l8
                              block $B45 (result i32)
                                local.get $l5
                                i32.load
                                local.tee $p4
                                if $I46
                                  local.get $p4
                                  local.get $p3
                                  i32.const 12
                                  i32.mul
                                  i32.add
                                  local.tee $p4
                                  i32.load offset=8
                                  local.set $l9
                                  local.get $p4
                                  i32.load offset=4
                                  local.set $l6
                                  local.get $p4
                                  i32.load
                                  br $B45
                                end
                                local.get $l5
                                i32.load offset=4
                                local.get $p3
                                i32.const 6
                                i32.mul
                                i32.add
                                local.tee $p4
                                i32.load16_u offset=4
                                local.set $l9
                                local.get $p4
                                i32.load16_u offset=2
                                local.set $l6
                                local.get $p4
                                i32.load16_u
                              end
                              i32.const 12
                              i32.mul
                              i32.add
                              local.tee $p4
                              f32.load
                              local.tee $l15
                              local.get $l5
                              f32.load offset=48
                              f32.sub
                              local.tee $l16
                              local.get $l16
                              f32.mul
                              local.get $p4
                              f32.load offset=4
                              local.tee $l16
                              local.get $l5
                              f32.load offset=52
                              f32.sub
                              local.tee $l19
                              local.get $l19
                              f32.mul
                              f32.add
                              local.get $p4
                              f32.load offset=8
                              local.tee $l19
                              local.get $l5
                              f32.load offset=56
                              f32.sub
                              local.tee $l17
                              local.get $l17
                              f32.mul
                              f32.add
                              f32.ge
                              i32.eqz
                              if $I47
                                local.get $l8
                                local.get $l6
                                i32.const 12
                                i32.mul
                                i32.add
                                local.tee $l6
                                f32.load offset=4
                                local.set $l17
                                local.get $l6
                                f32.load offset=8
                                local.set $l18
                                local.get $l5
                                local.get $l6
                                f32.load
                                local.get $l15
                                f32.sub
                                f32.store offset=1152
                                local.get $l5
                                local.get $l18
                                local.get $l19
                                f32.sub
                                f32.store offset=1160
                                local.get $l5
                                local.get $l17
                                local.get $l16
                                f32.sub
                                f32.store offset=1156
                                local.get $l8
                                local.get $l9
                                i32.const 12
                                i32.mul
                                i32.add
                                local.tee $l8
                                f32.load offset=4
                                local.set $l17
                                local.get $l8
                                f32.load
                                local.set $l18
                                local.get $l5
                                local.get $l8
                                f32.load offset=8
                                local.get $l19
                                f32.sub
                                f32.store offset=1144
                                local.get $l5
                                local.get $l17
                                local.get $l16
                                f32.sub
                                f32.store offset=1140
                                local.get $l5
                                local.get $l18
                                local.get $l15
                                f32.sub
                                f32.store offset=1136
                                local.get $l5
                                i32.const 1120
                                i32.add
                                local.get $l11
                                local.get $p4
                                local.get $l6
                                local.get $l8
                                local.get $l5
                                i32.const 1152
                                i32.add
                                local.get $l5
                                i32.const 1136
                                i32.add
                                call $f69961
                                local.get $l5
                                f32.load offset=60
                                local.get $l5
                                f32.load offset=1120
                                local.get $l5
                                f32.load offset=48
                                f32.sub
                                local.tee $l15
                                local.get $l15
                                f32.mul
                                local.get $l5
                                f32.load offset=1124
                                local.get $l5
                                f32.load offset=52
                                f32.sub
                                local.tee $l15
                                local.get $l15
                                f32.mul
                                f32.add
                                local.get $l5
                                f32.load offset=1128
                                local.get $l5
                                f32.load offset=56
                                f32.sub
                                local.tee $l15
                                local.get $l15
                                f32.mul
                                f32.add
                                f32.ge
                                i32.eqz
                                br_if $B44
                              end
                              i32.const 1
                              local.get $l5
                              i32.load offset=80
                              local.tee $p4
                              local.get $l5
                              i32.load offset=84
                              i32.eq
                              br_if $B15
                              drop
                              local.get $l5
                              i32.load offset=88
                              local.get $p4
                              i32.const 2
                              i32.shl
                              i32.add
                              local.get $p3
                              i32.store
                              local.get $l5
                              local.get $l5
                              i32.load offset=80
                              i32.const 1
                              i32.add
                              i32.store offset=80
                            end
                            local.get $p3
                            i32.const 1
                            i32.add
                            local.set $p3
                            local.get $p1
                            i32.const 1
                            i32.sub
                            local.tee $p1
                            br_if $L43
                          end
                          local.get $p2
                          br $B41
                        end
                        local.get $l5
                        i32.const 96
                        i32.add
                        local.get $p2
                        i32.const 2
                        i32.shl
                        i32.add
                        local.get $p4
                        i32.store
                        local.get $p2
                        i32.const 1
                        i32.add
                      end
                      local.tee $p0
                      br_if $L16
                    end
                    i32.const 0
                  end
                  i32.const 0
                  i32.ne
                  br $B13
                end
                local.get $l6
                i32.load offset=12
                local.tee $p1
                i32.const 4
                i32.shr_u
                local.set $p3
                local.get $p1
                i32.const 15
                i32.and
                local.set $p1
                local.get $l5
                i32.const 48
                i32.add
                local.set $l11
                loop $L48 (result i32)
                  block $B49 (result i32)
                    local.get $p4
                    if $I50
                      local.get $p4
                      local.get $p3
                      i32.const 12
                      i32.mul
                      i32.add
                      local.tee $p4
                      i32.load offset=8
                      local.set $l9
                      local.get $p4
                      i32.load offset=4
                      local.set $l6
                      local.get $p4
                      i32.load
                      br $B49
                    end
                    local.get $l8
                    local.get $p3
                    i32.const 6
                    i32.mul
                    i32.add
                    local.tee $p4
                    i32.load16_u offset=4
                    local.set $l9
                    local.get $p4
                    i32.load16_u offset=2
                    local.set $l6
                    local.get $p4
                    i32.load16_u
                  end
                  local.set $p4
                  block $B51
                    local.get $l5
                    f32.load offset=60
                    local.get $l5
                    i32.load offset=8
                    local.tee $l8
                    local.get $p4
                    i32.const 12
                    i32.mul
                    i32.add
                    local.tee $p4
                    f32.load
                    local.tee $l15
                    local.get $l5
                    f32.load offset=48
                    f32.sub
                    local.tee $l16
                    local.get $l16
                    f32.mul
                    local.get $p4
                    f32.load offset=4
                    local.tee $l16
                    local.get $l5
                    f32.load offset=52
                    f32.sub
                    local.tee $l19
                    local.get $l19
                    f32.mul
                    f32.add
                    local.get $p4
                    f32.load offset=8
                    local.tee $l19
                    local.get $l5
                    f32.load offset=56
                    f32.sub
                    local.tee $l17
                    local.get $l17
                    f32.mul
                    f32.add
                    f32.ge
                    i32.eqz
                    if $I52
                      local.get $l8
                      local.get $l6
                      i32.const 12
                      i32.mul
                      i32.add
                      local.tee $l6
                      f32.load offset=4
                      local.set $l17
                      local.get $l6
                      f32.load offset=8
                      local.set $l18
                      local.get $l5
                      local.get $l6
                      f32.load
                      local.get $l15
                      f32.sub
                      f32.store offset=96
                      local.get $l5
                      local.get $l18
                      local.get $l19
                      f32.sub
                      f32.store offset=104
                      local.get $l5
                      local.get $l17
                      local.get $l16
                      f32.sub
                      f32.store offset=100
                      local.get $l8
                      local.get $l9
                      i32.const 12
                      i32.mul
                      i32.add
                      local.tee $l8
                      f32.load offset=4
                      local.set $l17
                      local.get $l8
                      f32.load
                      local.set $l18
                      local.get $l5
                      local.get $l8
                      f32.load offset=8
                      local.get $l19
                      f32.sub
                      f32.store offset=1160
                      local.get $l5
                      local.get $l17
                      local.get $l16
                      f32.sub
                      f32.store offset=1156
                      local.get $l5
                      local.get $l18
                      local.get $l15
                      f32.sub
                      f32.store offset=1152
                      local.get $l5
                      i32.const 1136
                      i32.add
                      local.get $l11
                      local.get $p4
                      local.get $l6
                      local.get $l8
                      local.get $l5
                      i32.const 96
                      i32.add
                      local.get $l5
                      i32.const 1152
                      i32.add
                      call $f69961
                      local.get $l5
                      f32.load offset=60
                      local.get $l5
                      f32.load offset=1136
                      local.get $l5
                      f32.load offset=48
                      f32.sub
                      local.tee $l15
                      local.get $l15
                      f32.mul
                      local.get $l5
                      f32.load offset=1140
                      local.get $l5
                      f32.load offset=52
                      f32.sub
                      local.tee $l15
                      local.get $l15
                      f32.mul
                      f32.add
                      local.get $l5
                      f32.load offset=1144
                      local.get $l5
                      f32.load offset=56
                      f32.sub
                      local.tee $l15
                      local.get $l15
                      f32.mul
                      f32.add
                      f32.ge
                      i32.eqz
                      br_if $B51
                    end
                    i32.const 1
                    local.get $l5
                    i32.load offset=80
                    local.tee $p4
                    local.get $l5
                    i32.load offset=84
                    i32.eq
                    br_if $B13
                    drop
                    local.get $l5
                    i32.load offset=88
                    local.get $p4
                    i32.const 2
                    i32.shl
                    i32.add
                    local.get $p3
                    i32.store
                    local.get $l5
                    local.get $l5
                    i32.load offset=80
                    i32.const 1
                    i32.add
                    i32.store offset=80
                  end
                  local.get $p1
                  i32.const 1
                  i32.sub
                  local.tee $p1
                  if $I53 (result i32)
                    local.get $p3
                    i32.const 1
                    i32.add
                    local.set $p3
                    local.get $l5
                    i32.load offset=4
                    local.set $l8
                    local.get $l5
                    i32.load
                    local.set $p4
                    br $L48
                  else
                    i32.const 0
                  end
                end
              end
              i32.store8
              local.get $l5
              i32.load offset=80
              local.set $p3
              local.get $l5
              i32.const 1168
              i32.add
              global.set $g0
              local.get $p3
              local.tee $p2
            end
            i32.store offset=4
            br $B8
          end
          global.get $g0
          i32.const 1152
          i32.sub
          local.tee $l5
          global.set $g0
          local.get $p1
          local.tee $p2
          i32.load
          local.set $l10
          local.get $l5
          local.get $p0
          local.tee $p4
          f32.load offset=12
          local.tee $l17
          local.get $l17
          f32.mul
          local.tee $l20
          f32.store offset=60
          block $B54 (result f32)
            local.get $p3
            if $I55
              local.get $p3
              f32.load offset=32
              local.tee $l17
              local.get $p4
              f32.load
              local.tee $l18
              f32.mul
              local.get $p3
              f32.load offset=36
              local.tee $l19
              local.get $p4
              f32.load offset=4
              local.tee $l15
              f32.mul
              f32.add
              local.get $p3
              f32.load offset=40
              local.tee $l21
              local.get $p4
              f32.load offset=8
              local.tee $l16
              f32.mul
              f32.add
              local.get $p3
              f32.load offset=48
              local.tee $l22
              local.get $l17
              f32.mul
              local.get $p3
              f32.load offset=52
              local.tee $l24
              local.get $l19
              f32.mul
              f32.add
              local.get $p3
              f32.load offset=56
              local.tee $l23
              local.get $l21
              f32.mul
              f32.add
              f32.sub
              local.set $l17
              local.get $p3
              f32.load offset=16
              local.tee $l19
              local.get $l18
              f32.mul
              local.get $p3
              f32.load offset=20
              local.tee $l21
              local.get $l15
              f32.mul
              f32.add
              local.get $p3
              f32.load offset=24
              local.tee $l27
              local.get $l16
              f32.mul
              f32.add
              local.get $l22
              local.get $l19
              f32.mul
              local.get $l24
              local.get $l21
              f32.mul
              f32.add
              local.get $l23
              local.get $l27
              f32.mul
              f32.add
              f32.sub
              local.set $l19
              local.get $p3
              f32.load
              local.tee $l21
              local.get $l18
              f32.mul
              local.get $p3
              f32.load offset=4
              local.tee $l18
              local.get $l15
              f32.mul
              f32.add
              local.get $p3
              f32.load offset=8
              local.tee $l15
              local.get $l16
              f32.mul
              f32.add
              local.get $l22
              local.get $l21
              f32.mul
              local.get $l24
              local.get $l18
              f32.mul
              f32.add
              local.get $l23
              local.get $l15
              f32.mul
              f32.add
              f32.sub
              br $B54
            end
            local.get $p4
            f32.load offset=8
            local.set $l17
            local.get $p4
            f32.load offset=4
            local.set $l19
            local.get $p4
            f32.load
          end
          local.set $l18
          local.get $l5
          local.get $l17
          local.get $l17
          f32.add
          f32.store offset=72
          local.get $l5
          local.get $l19
          local.get $l19
          f32.add
          f32.store offset=68
          local.get $l5
          local.get $l17
          f32.store offset=56
          local.get $l5
          local.get $l19
          f32.store offset=52
          local.get $l5
          local.get $l20
          f32.const 0x1p+2 (;=4;)
          f32.mul
          f32.store offset=76
          local.get $l5
          local.get $l18
          f32.store offset=48
          local.get $l5
          local.get $l18
          local.get $l18
          f32.add
          f32.store offset=64
          local.get $l5
          local.get $l10
          i32.load offset=16
          local.tee $p3
          i32.store
          local.get $l5
          local.get $l10
          i32.load offset=20
          local.tee $p4
          i32.store offset=4
          local.get $l5
          local.get $l10
          i32.load offset=4
          i32.store offset=8
          local.get $p2
          f32.load offset=40
          local.set $l15
          local.get $p2
          i64.load offset=32 align=4
          local.set $l34
          local.get $l5
          local.get $p2
          f32.load offset=44
          local.tee $l16
          f32.store offset=28
          local.get $l5
          local.get $l15
          f32.store offset=24
          local.get $l5
          local.get $l34
          i64.store offset=16
          local.get $p2
          i64.load offset=48 align=4
          local.set $l34
          local.get $l5
          local.get $p2
          f32.load offset=56
          f32.store offset=44
          local.get $l5
          local.get $l34
          i64.store offset=36 align=4
          local.get $l5
          local.get $l16
          f32.store offset=32
          block $B56
            block $B57
              local.get $p2
              i32.load offset=24
              local.tee $l13
              if $I58
                local.get $l5
                local.get $p2
                i32.load offset=28
                i32.store offset=80
                local.get $l5
                i32.const 48
                i32.add
                local.set $l12
                i32.const 1
                local.set $p1
                loop $L59
                  local.get $l13
                  local.get $l5
                  i32.const 80
                  i32.add
                  local.get $p1
                  i32.const 1
                  i32.sub
                  local.tee $p0
                  i32.const 2
                  i32.shl
                  i32.add
                  local.tee $p4
                  i32.load
                  local.tee $p2
                  i32.const 11
                  i32.shr_u
                  i32.const 4
                  i32.shl
                  i32.add
                  local.set $p3
                  block $B60
                    block $B61
                      block $B62
                        block $B63
                          local.get $p2
                          i32.const 1
                          i32.shr_u
                          i32.const 3
                          i32.and
                          local.tee $l14
                          i32.const 2
                          i32.ge_u
                          if $I64
                            local.get $l5
                            f32.load offset=76
                            local.tee $l22
                            local.get $l5
                            f32.load offset=64
                            local.tee $l15
                            local.get $l5
                            f32.load offset=16
                            local.tee $l16
                            local.get $p3
                            i32.load16_s offset=12
                            f32.convert_i32_s
                            f32.mul
                            local.tee $l21
                            local.get $l5
                            f32.load offset=32
                            local.tee $l24
                            local.get $p3
                            i32.load16_s offset=14
                            f32.convert_i32_s
                            f32.mul
                            local.tee $l27
                            f32.add
                            f32.sub
                            local.tee $l23
                            local.get $l23
                            local.get $l27
                            local.get $l21
                            f32.sub
                            local.tee $l21
                            local.get $l21
                            local.get $l23
                            f32.gt
                            select
                            local.tee $l23
                            local.get $l21
                            f32.neg
                            local.tee $l21
                            local.get $l21
                            local.get $l23
                            f32.lt
                            select
                            f32.sub
                            local.tee $l23
                            local.get $l23
                            f32.mul
                            local.get $l5
                            f32.load offset=68
                            local.tee $l23
                            local.get $l5
                            f32.load offset=20
                            local.tee $l21
                            local.get $p3
                            i32.load16_s offset=28
                            f32.convert_i32_s
                            f32.mul
                            local.tee $l25
                            local.get $l5
                            f32.load offset=36
                            local.tee $l27
                            local.get $p3
                            i32.load16_s offset=30
                            f32.convert_i32_s
                            f32.mul
                            local.tee $l30
                            f32.add
                            f32.sub
                            local.tee $l26
                            local.get $l26
                            local.get $l30
                            local.get $l25
                            f32.sub
                            local.tee $l25
                            local.get $l25
                            local.get $l26
                            f32.gt
                            select
                            local.tee $l26
                            local.get $l25
                            f32.neg
                            local.tee $l25
                            local.get $l25
                            local.get $l26
                            f32.lt
                            select
                            f32.sub
                            local.tee $l26
                            local.get $l26
                            f32.mul
                            f32.add
                            local.get $l5
                            f32.load offset=72
                            local.tee $l26
                            local.get $l5
                            f32.load offset=24
                            local.tee $l25
                            local.get $p3
                            i32.load16_s offset=44
                            f32.convert_i32_s
                            f32.mul
                            local.tee $l28
                            local.get $l5
                            f32.load offset=40
                            local.tee $l30
                            local.get $p3
                            i32.load16_s offset=46
                            f32.convert_i32_s
                            f32.mul
                            local.tee $l31
                            f32.add
                            f32.sub
                            local.tee $l29
                            local.get $l29
                            local.get $l31
                            local.get $l28
                            f32.sub
                            local.tee $l28
                            local.get $l28
                            local.get $l29
                            f32.gt
                            select
                            local.tee $l29
                            local.get $l28
                            f32.neg
                            local.tee $l28
                            local.get $l28
                            local.get $l29
                            f32.lt
                            select
                            f32.sub
                            local.tee $l29
                            local.get $l29
                            f32.mul
                            f32.add
                            f32.ge
                            i32.eqz
                            br_if $B63
                            local.get $p3
                            i32.load offset=60
                            local.tee $p2
                            i32.const 1
                            i32.and
                            i32.eqz
                            br_if $B62
                            local.get $p2
                            i32.const 5
                            i32.shr_u
                            local.set $l8
                            local.get $p2
                            i32.const 1
                            i32.shr_u
                            i32.const 15
                            i32.and
                            local.set $l11
                            loop $L65
                              i32.const 1
                              local.set $l10
                              local.get $l5
                              i32.load offset=8
                              local.tee $l6
                              block $B66 (result i32)
                                local.get $l5
                                i32.load
                                local.tee $p2
                                if $I67
                                  local.get $p2
                                  local.get $l8
                                  i32.const 12
                                  i32.mul
                                  i32.add
                                  local.tee $p2
                                  i32.load offset=8
                                  local.set $l9
                                  local.get $p2
                                  i32.load offset=4
                                  local.set $p4
                                  local.get $p2
                                  i32.load
                                  br $B66
                                end
                                local.get $l5
                                i32.load offset=4
                                local.get $l8
                                i32.const 6
                                i32.mul
                                i32.add
                                local.tee $p2
                                i32.load16_u offset=4
                                local.set $l9
                                local.get $p2
                                i32.load16_u offset=2
                                local.set $p4
                                local.get $p2
                                i32.load16_u
                              end
                              i32.const 12
                              i32.mul
                              i32.add
                              local.tee $p2
                              f32.load
                              local.tee $l15
                              local.get $l18
                              f32.sub
                              local.tee $l18
                              local.get $l18
                              f32.mul
                              local.get $p2
                              f32.load offset=4
                              local.tee $l18
                              local.get $l19
                              f32.sub
                              local.tee $l19
                              local.get $l19
                              f32.mul
                              f32.add
                              local.get $p2
                              f32.load offset=8
                              local.tee $l19
                              local.get $l17
                              f32.sub
                              local.tee $l17
                              local.get $l17
                              f32.mul
                              f32.add
                              local.get $l20
                              f32.le
                              br_if $B56
                              local.get $l6
                              local.get $p4
                              i32.const 12
                              i32.mul
                              i32.add
                              local.tee $p4
                              f32.load offset=4
                              local.set $l17
                              local.get $p4
                              f32.load offset=8
                              local.set $l20
                              local.get $l5
                              local.get $p4
                              f32.load
                              local.get $l15
                              f32.sub
                              f32.store offset=1136
                              local.get $l5
                              local.get $l20
                              local.get $l19
                              f32.sub
                              f32.store offset=1144
                              local.get $l5
                              local.get $l17
                              local.get $l18
                              f32.sub
                              f32.store offset=1140
                              local.get $l6
                              local.get $l9
                              i32.const 12
                              i32.mul
                              i32.add
                              local.tee $l6
                              f32.load offset=4
                              local.set $l17
                              local.get $l6
                              f32.load
                              local.set $l20
                              local.get $l5
                              local.get $l6
                              f32.load offset=8
                              local.get $l19
                              f32.sub
                              f32.store offset=1128
                              local.get $l5
                              local.get $l17
                              local.get $l18
                              f32.sub
                              f32.store offset=1124
                              local.get $l5
                              local.get $l20
                              local.get $l15
                              f32.sub
                              f32.store offset=1120
                              local.get $l5
                              i32.const 1104
                              i32.add
                              local.get $l12
                              local.get $p2
                              local.get $p4
                              local.get $l6
                              local.get $l5
                              i32.const 1136
                              i32.add
                              local.get $l5
                              i32.const 1120
                              i32.add
                              call $f69961
                              local.get $l5
                              f32.load offset=1104
                              local.get $l5
                              f32.load offset=48
                              local.tee $l18
                              f32.sub
                              local.tee $l17
                              local.get $l17
                              f32.mul
                              local.get $l5
                              f32.load offset=1108
                              local.get $l5
                              f32.load offset=52
                              local.tee $l19
                              f32.sub
                              local.tee $l17
                              local.get $l17
                              f32.mul
                              f32.add
                              local.get $l5
                              f32.load offset=1112
                              local.get $l5
                              f32.load offset=56
                              local.tee $l17
                              f32.sub
                              local.tee $l20
                              local.get $l20
                              f32.mul
                              f32.add
                              local.get $l5
                              f32.load offset=60
                              local.tee $l20
                              f32.le
                              br_if $B56
                              local.get $l8
                              i32.const 1
                              i32.add
                              local.set $l8
                              local.get $l11
                              i32.const 1
                              i32.sub
                              local.tee $l11
                              br_if $L65
                            end
                          end
                          local.get $l14
                          i32.eqz
                          br_if $B60
                          local.get $l5
                          f32.load offset=76
                          local.set $l22
                          local.get $l5
                          f32.load offset=72
                          local.set $l26
                          local.get $l5
                          f32.load offset=68
                          local.set $l23
                          local.get $l5
                          f32.load offset=64
                          local.set $l15
                          local.get $l5
                          f32.load offset=40
                          local.set $l30
                          local.get $l5
                          f32.load offset=36
                          local.set $l27
                          local.get $l5
                          f32.load offset=32
                          local.set $l24
                          local.get $l5
                          f32.load offset=24
                          local.set $l25
                          local.get $l5
                          f32.load offset=20
                          local.set $l21
                          local.get $l5
                          f32.load offset=16
                          local.set $l16
                        end
                        local.get $p0
                        local.set $p1
                        br $B61
                      end
                      local.get $p4
                      local.get $p2
                      i32.store
                    end
                    local.get $l22
                    local.get $l15
                    local.get $l16
                    local.get $p3
                    i32.load16_s offset=8
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l16
                    local.get $l24
                    local.get $p3
                    i32.load16_s offset=10
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l24
                    f32.add
                    f32.sub
                    local.tee $l15
                    local.get $l15
                    local.get $l24
                    local.get $l16
                    f32.sub
                    local.tee $l16
                    local.get $l15
                    local.get $l16
                    f32.lt
                    select
                    local.tee $l15
                    local.get $l16
                    f32.neg
                    local.tee $l16
                    local.get $l15
                    local.get $l16
                    f32.gt
                    select
                    f32.sub
                    local.tee $l15
                    local.get $l15
                    f32.mul
                    local.get $l23
                    local.get $l21
                    local.get $p3
                    i32.load16_s offset=24
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l16
                    local.get $l27
                    local.get $p3
                    i32.load16_s offset=26
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l24
                    f32.add
                    f32.sub
                    local.tee $l15
                    local.get $l15
                    local.get $l24
                    local.get $l16
                    f32.sub
                    local.tee $l16
                    local.get $l15
                    local.get $l16
                    f32.lt
                    select
                    local.tee $l15
                    local.get $l16
                    f32.neg
                    local.tee $l16
                    local.get $l15
                    local.get $l16
                    f32.gt
                    select
                    f32.sub
                    local.tee $l15
                    local.get $l15
                    f32.mul
                    f32.add
                    local.get $l26
                    local.get $l25
                    local.get $p3
                    i32.load16_s offset=40
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l16
                    local.get $l30
                    local.get $p3
                    i32.load16_s offset=42
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l24
                    f32.add
                    f32.sub
                    local.tee $l15
                    local.get $l15
                    local.get $l24
                    local.get $l16
                    f32.sub
                    local.tee $l16
                    local.get $l15
                    local.get $l16
                    f32.lt
                    select
                    local.tee $l15
                    local.get $l16
                    f32.neg
                    local.tee $l16
                    local.get $l15
                    local.get $l16
                    f32.gt
                    select
                    f32.sub
                    local.tee $l15
                    local.get $l15
                    f32.mul
                    f32.add
                    f32.ge
                    i32.eqz
                    if $I68
                      local.get $p1
                      local.set $p0
                      br $B60
                    end
                    local.get $p3
                    i32.load offset=56
                    local.tee $p2
                    i32.const 1
                    i32.and
                    if $I69
                      local.get $p2
                      i32.const 5
                      i32.shr_u
                      local.set $l8
                      local.get $p2
                      i32.const 1
                      i32.shr_u
                      i32.const 15
                      i32.and
                      local.set $l11
                      loop $L70
                        i32.const 1
                        local.set $l10
                        local.get $l5
                        i32.load offset=8
                        local.tee $l6
                        block $B71 (result i32)
                          local.get $l5
                          i32.load
                          local.tee $p2
                          if $I72
                            local.get $p2
                            local.get $l8
                            i32.const 12
                            i32.mul
                            i32.add
                            local.tee $p2
                            i32.load offset=8
                            local.set $l9
                            local.get $p2
                            i32.load offset=4
                            local.set $p4
                            local.get $p2
                            i32.load
                            br $B71
                          end
                          local.get $l5
                          i32.load offset=4
                          local.get $l8
                          i32.const 6
                          i32.mul
                          i32.add
                          local.tee $p2
                          i32.load16_u offset=4
                          local.set $l9
                          local.get $p2
                          i32.load16_u offset=2
                          local.set $p4
                          local.get $p2
                          i32.load16_u
                        end
                        i32.const 12
                        i32.mul
                        i32.add
                        local.tee $p2
                        f32.load
                        local.tee $l15
                        local.get $l18
                        f32.sub
                        local.tee $l18
                        local.get $l18
                        f32.mul
                        local.get $p2
                        f32.load offset=4
                        local.tee $l18
                        local.get $l19
                        f32.sub
                        local.tee $l19
                        local.get $l19
                        f32.mul
                        f32.add
                        local.get $p2
                        f32.load offset=8
                        local.tee $l19
                        local.get $l17
                        f32.sub
                        local.tee $l17
                        local.get $l17
                        f32.mul
                        f32.add
                        local.get $l20
                        f32.le
                        br_if $B56
                        local.get $l6
                        local.get $p4
                        i32.const 12
                        i32.mul
                        i32.add
                        local.tee $p4
                        f32.load offset=4
                        local.set $l17
                        local.get $p4
                        f32.load offset=8
                        local.set $l20
                        local.get $l5
                        local.get $p4
                        f32.load
                        local.get $l15
                        f32.sub
                        f32.store offset=1136
                        local.get $l5
                        local.get $l20
                        local.get $l19
                        f32.sub
                        f32.store offset=1144
                        local.get $l5
                        local.get $l17
                        local.get $l18
                        f32.sub
                        f32.store offset=1140
                        local.get $l6
                        local.get $l9
                        i32.const 12
                        i32.mul
                        i32.add
                        local.tee $l6
                        f32.load offset=4
                        local.set $l17
                        local.get $l6
                        f32.load
                        local.set $l20
                        local.get $l5
                        local.get $l6
                        f32.load offset=8
                        local.get $l19
                        f32.sub
                        f32.store offset=1128
                        local.get $l5
                        local.get $l17
                        local.get $l18
                        f32.sub
                        f32.store offset=1124
                        local.get $l5
                        local.get $l20
                        local.get $l15
                        f32.sub
                        f32.store offset=1120
                        local.get $l5
                        i32.const 1104
                        i32.add
                        local.get $l12
                        local.get $p2
                        local.get $p4
                        local.get $l6
                        local.get $l5
                        i32.const 1136
                        i32.add
                        local.get $l5
                        i32.const 1120
                        i32.add
                        call $f69961
                        local.get $l5
                        f32.load offset=1104
                        local.get $l5
                        f32.load offset=48
                        local.tee $l18
                        f32.sub
                        local.tee $l17
                        local.get $l17
                        f32.mul
                        local.get $l5
                        f32.load offset=1108
                        local.get $l5
                        f32.load offset=52
                        local.tee $l19
                        f32.sub
                        local.tee $l17
                        local.get $l17
                        f32.mul
                        f32.add
                        local.get $l5
                        f32.load offset=1112
                        local.get $l5
                        f32.load offset=56
                        local.tee $l17
                        f32.sub
                        local.tee $l20
                        local.get $l20
                        f32.mul
                        f32.add
                        local.get $l5
                        f32.load offset=60
                        local.tee $l20
                        f32.le
                        br_if $B56
                        local.get $l8
                        i32.const 1
                        i32.add
                        local.set $l8
                        local.get $l11
                        i32.const 1
                        i32.sub
                        local.tee $l11
                        br_if $L70
                      end
                      local.get $p1
                      local.set $p0
                      br $B60
                    end
                    local.get $l5
                    i32.const 80
                    i32.add
                    local.get $p1
                    i32.const 2
                    i32.shl
                    i32.add
                    local.get $p2
                    i32.store
                    local.get $p1
                    i32.const 1
                    i32.add
                    local.set $p0
                  end
                  block $B73
                    local.get $l5
                    f32.load offset=76
                    local.tee $l24
                    local.get $l5
                    f32.load offset=64
                    local.tee $l23
                    local.get $l5
                    f32.load offset=16
                    local.tee $l21
                    local.get $p3
                    i32.load16_s offset=4
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l16
                    local.get $l5
                    f32.load offset=32
                    local.tee $l27
                    local.get $p3
                    i32.load16_s offset=6
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l22
                    f32.add
                    f32.sub
                    local.tee $l15
                    local.get $l15
                    local.get $l22
                    local.get $l16
                    f32.sub
                    local.tee $l16
                    local.get $l15
                    local.get $l16
                    f32.lt
                    select
                    local.tee $l15
                    local.get $l16
                    f32.neg
                    local.tee $l16
                    local.get $l15
                    local.get $l16
                    f32.gt
                    select
                    f32.sub
                    local.tee $l15
                    local.get $l15
                    f32.mul
                    local.get $l5
                    f32.load offset=68
                    local.tee $l26
                    local.get $l5
                    f32.load offset=20
                    local.tee $l25
                    local.get $p3
                    i32.load16_s offset=20
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l16
                    local.get $l5
                    f32.load offset=36
                    local.tee $l30
                    local.get $p3
                    i32.load16_s offset=22
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l22
                    f32.add
                    f32.sub
                    local.tee $l15
                    local.get $l15
                    local.get $l22
                    local.get $l16
                    f32.sub
                    local.tee $l16
                    local.get $l15
                    local.get $l16
                    f32.lt
                    select
                    local.tee $l15
                    local.get $l16
                    f32.neg
                    local.tee $l16
                    local.get $l15
                    local.get $l16
                    f32.gt
                    select
                    f32.sub
                    local.tee $l15
                    local.get $l15
                    f32.mul
                    f32.add
                    local.get $l5
                    f32.load offset=72
                    local.tee $l29
                    local.get $l5
                    f32.load offset=24
                    local.tee $l28
                    local.get $p3
                    i32.load16_s offset=36
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l16
                    local.get $l5
                    f32.load offset=40
                    local.tee $l31
                    local.get $p3
                    i32.load16_s offset=38
                    f32.convert_i32_s
                    f32.mul
                    local.tee $l22
                    f32.add
                    f32.sub
                    local.tee $l15
                    local.get $l15
                    local.get $l22
                    local.get $l16
                    f32.sub
                    local.tee $l16
                    local.get $l15
                    local.get $l16
                    f32.lt
                    select
                    local.tee $l15
                    local.get $l16
                    f32.neg
                    local.tee $l16
                    local.get $l15
                    local.get $l16
                    f32.gt
                    select
                    f32.sub
                    local.tee $l15
                    local.get $l15
                    f32.mul
                    f32.add
                    f32.ge
                    i32.eqz
                    br_if $B73
                    local.get $p3
                    i32.load offset=52
                    local.tee $p2
                    i32.const 1
                    i32.and
                    if $I74
                      local.get $p2
                      i32.const 5
                      i32.shr_u
                      local.set $l8
                      local.get $p2
                      i32.const 1
                      i32.shr_u
                      i32.const 15
                      i32.and
                      local.set $l11
                      loop $L75
                        i32.const 1
                        local.set $l10
                        local.get $l5
                        i32.load offset=8
                        local.tee $l6
                        block $B76 (result i32)
                          local.get $l5
                          i32.load
                          local.tee $p2
                          if $I77
                            local.get $p2
                            local.get $l8
                            i32.const 12
                            i32.mul
                            i32.add
                            local.tee $p2
                            i32.load offset=8
                            local.set $l9
                            local.get $p2
                            i32.load offset=4
                            local.set $p4
                            local.get $p2
                            i32.load
                            br $B76
                          end
                          local.get $l5
                          i32.load offset=4
                          local.get $l8
                          i32.const 6
                          i32.mul
                          i32.add
                          local.tee $p2
                          i32.load16_u offset=4
                          local.set $l9
                          local.get $p2
                          i32.load16_u offset=2
                          local.set $p4
                          local.get $p2
                          i32.load16_u
                        end
                        i32.const 12
                        i32.mul
                        i32.add
                        local.tee $p2
                        f32.load
                        local.tee $l15
                        local.get $l18
                        f32.sub
                        local.tee $l18
                        local.get $l18
                        f32.mul
                        local.get $p2
                        f32.load offset=4
                        local.tee $l18
                        local.get $l19
                        f32.sub
                        local.tee $l19
                        local.get $l19
                        f32.mul
                        f32.add
                        local.get $p2
                        f32.load offset=8
                        local.tee $l19
                        local.get $l17
                        f32.sub
                        local.tee $l17
                        local.get $l17
                        f32.mul
                        f32.add
                        local.get $l20
                        f32.le
                        br_if $B56
                        local.get $l6
                        local.get $p4
                        i32.const 12
                        i32.mul
                        i32.add
                        local.tee $p4
                        f32.load offset=4
                        local.set $l17
                        local.get $p4
                        f32.load offset=8
                        local.set $l20
                        local.get $l5
                        local.get $p4
                        f32.load
                        local.get $l15
                        f32.sub
                        f32.store offset=1136
                        local.get $l5
                        local.get $l20
                        local.get $l19
                        f32.sub
                        f32.store offset=1144
                        local.get $l5
                        local.get $l17
                        local.get $l18
                        f32.sub
                        f32.store offset=1140
                        local.get $l6
                        local.get $l9
                        i32.const 12
                        i32.mul
                        i32.add
                        local.tee $l6
                        f32.load offset=4
                        local.set $l17
                        local.get $l6
                        f32.load
                        local.set $l20
                        local.get $l5
                        local.get $l6
                        f32.load offset=8
                        local.get $l19
                        f32.sub
                        f32.store offset=1128
                        local.get $l5
                        local.get $l17
                        local.get $l18
                        f32.sub
                        f32.store offset=1124
                        local.get $l5
                        local.get $l20
                        local.get $l15
                        f32.sub
                        f32.store offset=1120
                        local.get $l5
                        i32.const 1104
                        i32.add
                        local.get $l12
                        local.get $p2
                        local.get $p4
                        local.get $l6
                        local.get $l5
                        i32.const 1136
                        i32.add
                        local.get $l5
                        i32.const 1120
                        i32.add
                        call $f69961
                        local.get $l5
                        f32.load offset=1104
                        local.get $l5
                        f32.load offset=48
                        local.tee $l18
                        f32.sub
                        local.tee $l17
                        local.get $l17
                        f32.mul
                        local.get $l5
                        f32.load offset=1108
                        local.get $l5
                        f32.load offset=52
                        local.tee $l19
                        f32.sub
                        local.tee $l17
                        local.get $l17
                        f32.mul
                        f32.add
                        local.get $l5
                        f32.load offset=1112
                        local.get $l5
                        f32.load offset=56
                        local.tee $l17
                        f32.sub
                        local.tee $l20
                        local.get $l20
                        f32.mul
                        f32.add
                        local.get $l5
                        f32.load offset=60
                        local.tee $l20
                        f32.le
                        br_if $B56
                        local.get $l8
                        i32.const 1
                        i32.add
                        local.set $l8
                        local.get $l11
                        i32.const 1
                        i32.sub
                        local.tee $l11
                        br_if $L75
                      end
                      local.get $l5
                      f32.load offset=76
                      local.set $l24
                      local.get $l5
                      f32.load offset=72
                      local.set $l29
                      local.get $l5
                      f32.load offset=68
                      local.set $l26
                      local.get $l5
                      f32.load offset=64
                      local.set $l23
                      local.get $l5
                      f32.load offset=40
                      local.set $l31
                      local.get $l5
                      f32.load offset=36
                      local.set $l30
                      local.get $l5
                      f32.load offset=32
                      local.set $l27
                      local.get $l5
                      f32.load offset=24
                      local.set $l28
                      local.get $l5
                      f32.load offset=20
                      local.set $l25
                      local.get $l5
                      f32.load offset=16
                      local.set $l21
                      br $B73
                    end
                    local.get $l5
                    i32.const 80
                    i32.add
                    local.get $p0
                    i32.const 2
                    i32.shl
                    i32.add
                    local.get $p2
                    i32.store
                    local.get $p0
                    i32.const 1
                    i32.add
                    local.set $p0
                  end
                  local.get $l24
                  local.get $l23
                  local.get $l21
                  local.get $p3
                  i32.load16_s
                  f32.convert_i32_s
                  f32.mul
                  local.tee $l16
                  local.get $l27
                  local.get $p3
                  i32.load16_s offset=2
                  f32.convert_i32_s
                  f32.mul
                  local.tee $l22
                  f32.add
                  f32.sub
                  local.tee $l15
                  local.get $l15
                  local.get $l22
                  local.get $l16
                  f32.sub
                  local.tee $l16
                  local.get $l15
                  local.get $l16
                  f32.lt
                  select
                  local.tee $l15
                  local.get $l16
                  f32.neg
                  local.tee $l16
                  local.get $l15
                  local.get $l16
                  f32.gt
                  select
                  f32.sub
                  local.tee $l15
                  local.get $l15
                  f32.mul
                  local.get $l26
                  local.get $l25
                  local.get $p3
                  i32.load16_s offset=16
                  f32.convert_i32_s
                  f32.mul
                  local.tee $l16
                  local.get $l30
                  local.get $p3
                  i32.load16_s offset=18
                  f32.convert_i32_s
                  f32.mul
                  local.tee $l22
                  f32.add
                  f32.sub
                  local.tee $l15
                  local.get $l15
                  local.get $l22
                  local.get $l16
                  f32.sub
                  local.tee $l16
                  local.get $l15
                  local.get $l16
                  f32.lt
                  select
                  local.tee $l15
                  local.get $l16
                  f32.neg
                  local.tee $l16
                  local.get $l15
                  local.get $l16
                  f32.gt
                  select
                  f32.sub
                  local.tee $l15
                  local.get $l15
                  f32.mul
                  f32.add
                  local.get $l29
                  local.get $l28
                  local.get $p3
                  i32.load16_s offset=32
                  f32.convert_i32_s
                  f32.mul
                  local.tee $l16
                  local.get $l31
                  local.get $p3
                  i32.load16_s offset=34
                  f32.convert_i32_s
                  f32.mul
                  local.tee $l22
                  f32.add
                  f32.sub
                  local.tee $l15
                  local.get $l15
                  local.get $l22
                  local.get $l16
                  f32.sub
                  local.tee $l16
                  local.get $l15
                  local.get $l16
                  f32.lt
                  select
                  local.tee $l15
                  local.get $l16
                  f32.neg
                  local.tee $l16
                  local.get $l15
                  local.get $l16
                  f32.gt
                  select
                  f32.sub
                  local.tee $l15
                  local.get $l15
                  f32.mul
                  f32.add
                  f32.ge
                  i32.eqz
                  if $I78
                    local.get $p0
                    local.tee $p1
                    br_if $L59
                    br $B57
                  end
                  local.get $p3
                  i32.load offset=48
                  local.tee $p3
                  i32.const 1
                  i32.and
                  if $I79
                    local.get $p3
                    i32.const 5
                    i32.shr_u
                    local.set $l6
                    local.get $p3
                    i32.const 1
                    i32.shr_u
                    i32.const 15
                    i32.and
                    local.set $l9
                    loop $L80
                      i32.const 1
                      local.set $l10
                      local.get $l5
                      i32.load offset=8
                      local.tee $p4
                      block $B81 (result i32)
                        local.get $l5
                        i32.load
                        local.tee $p3
                        if $I82
                          local.get $p3
                          local.get $l6
                          i32.const 12
                          i32.mul
                          i32.add
                          local.tee $p3
                          i32.load offset=8
                          local.set $l8
                          local.get $p3
                          i32.load offset=4
                          local.set $p2
                          local.get $p3
                          i32.load
                          br $B81
                        end
                        local.get $l5
                        i32.load offset=4
                        local.get $l6
                        i32.const 6
                        i32.mul
                        i32.add
                        local.tee $p3
                        i32.load16_u offset=4
                        local.set $l8
                        local.get $p3
                        i32.load16_u offset=2
                        local.set $p2
                        local.get $p3
                        i32.load16_u
                      end
                      i32.const 12
                      i32.mul
                      i32.add
                      local.tee $p3
                      f32.load
                      local.tee $l15
                      local.get $l18
                      f32.sub
                      local.tee $l18
                      local.get $l18
                      f32.mul
                      local.get $p3
                      f32.load offset=4
                      local.tee $l18
                      local.get $l19
                      f32.sub
                      local.tee $l19
                      local.get $l19
                      f32.mul
                      f32.add
                      local.get $p3
                      f32.load offset=8
                      local.tee $l19
                      local.get $l17
                      f32.sub
                      local.tee $l17
                      local.get $l17
                      f32.mul
                      f32.add
                      local.get $l20
                      f32.le
                      br_if $B56
                      local.get $p4
                      local.get $p2
                      i32.const 12
                      i32.mul
                      i32.add
                      local.tee $p2
                      f32.load offset=4
                      local.set $l17
                      local.get $p2
                      f32.load offset=8
                      local.set $l20
                      local.get $l5
                      local.get $p2
                      f32.load
                      local.get $l15
                      f32.sub
                      f32.store offset=1136
                      local.get $l5
                      local.get $l20
                      local.get $l19
                      f32.sub
                      f32.store offset=1144
                      local.get $l5
                      local.get $l17
                      local.get $l18
                      f32.sub
                      f32.store offset=1140
                      local.get $p4
                      local.get $l8
                      i32.const 12
                      i32.mul
                      i32.add
                      local.tee $p4
                      f32.load offset=4
                      local.set $l17
                      local.get $p4
                      f32.load
                      local.set $l20
                      local.get $l5
                      local.get $p4
                      f32.load offset=8
                      local.get $l19
                      f32.sub
                      f32.store offset=1128
                      local.get $l5
                      local.get $l17
                      local.get $l18
                      f32.sub
                      f32.store offset=1124
                      local.get $l5
                      local.get $l20
                      local.get $l15
                      f32.sub
                      f32.store offset=1120
                      local.get $l5
                      i32.const 1104
                      i32.add
                      local.get $l12
                      local.get $p3
                      local.get $p2
                      local.get $p4
                      local.get $l5
                      i32.const 1136
                      i32.add
                      local.get $l5
                      i32.const 1120
                      i32.add
                      call $f69961
                      local.get $l5
                      f32.load offset=1104
                      local.get $l5
                      f32.load offset=48
                      local.tee $l18
                      f32.sub
                      local.tee $l17
                      local.get $l17
                      f32.mul
                      local.get $l5
                      f32.load offset=1108
                      local.get $l5
                      f32.load offset=52
                      local.tee $l19
                      f32.sub
                      local.tee $l17
                      local.get $l17
                      f32.mul
                      f32.add
                      local.get $l5
                      f32.load offset=1112
                      local.get $l5
                      f32.load offset=56
                      local.tee $l17
                      f32.sub
                      local.tee $l20
                      local.get $l20
                      f32.mul
                      f32.add
                      local.get $l5
                      f32.load offset=60
                      local.tee $l20
                      f32.le
                      br_if $B56
                      local.get $l6
                      i32.const 1
                      i32.add
                      local.set $l6
                      local.get $l9
                      i32.const 1
                      i32.sub
                      local.tee $l9
                      br_if $L80
                    end
                    local.get $p0
                    local.tee $p1
                    br_if $L59
                    br $B57
                  end
                  local.get $l5
                  i32.const 80
                  i32.add
                  local.get $p0
                  i32.const 2
                  i32.shl
                  i32.add
                  local.get $p3
                  i32.store
                  local.get $p0
                  i32.const 1
                  i32.add
                  local.tee $p1
                  br_if $L59
                end
                br $B57
              end
              local.get $l10
              i32.load offset=12
              local.tee $p2
              i32.const 4
              i32.shr_u
              local.set $l6
              local.get $p2
              i32.const 15
              i32.and
              local.set $l12
              local.get $l5
              i32.const 48
              i32.add
              local.set $l9
              loop $L83
                block $B84 (result i32)
                  local.get $p3
                  if $I85
                    local.get $p3
                    local.get $l6
                    i32.const 12
                    i32.mul
                    i32.add
                    local.tee $p3
                    i32.load offset=8
                    local.set $l8
                    local.get $p3
                    i32.load offset=4
                    local.set $p2
                    local.get $p3
                    i32.load
                    br $B84
                  end
                  local.get $p4
                  local.get $l6
                  i32.const 6
                  i32.mul
                  i32.add
                  local.tee $p3
                  i32.load16_u offset=4
                  local.set $l8
                  local.get $p3
                  i32.load16_u offset=2
                  local.set $p2
                  local.get $p3
                  i32.load16_u
                end
                local.set $p3
                i32.const 1
                local.set $l10
                local.get $l5
                i32.load offset=8
                local.tee $p4
                local.get $p3
                i32.const 12
                i32.mul
                i32.add
                local.tee $p3
                f32.load
                local.tee $l15
                local.get $l18
                f32.sub
                local.tee $l18
                local.get $l18
                f32.mul
                local.get $p3
                f32.load offset=4
                local.tee $l18
                local.get $l19
                f32.sub
                local.tee $l19
                local.get $l19
                f32.mul
                f32.add
                local.get $p3
                f32.load offset=8
                local.tee $l19
                local.get $l17
                f32.sub
                local.tee $l17
                local.get $l17
                f32.mul
                f32.add
                local.get $l20
                f32.le
                br_if $B56
                local.get $p4
                local.get $p2
                i32.const 12
                i32.mul
                i32.add
                local.tee $p2
                f32.load offset=4
                local.set $l17
                local.get $p2
                f32.load offset=8
                local.set $l20
                local.get $l5
                local.get $p2
                f32.load
                local.get $l15
                f32.sub
                f32.store offset=80
                local.get $l5
                local.get $l20
                local.get $l19
                f32.sub
                f32.store offset=88
                local.get $l5
                local.get $l17
                local.get $l18
                f32.sub
                f32.store offset=84
                local.get $p4
                local.get $l8
                i32.const 12
                i32.mul
                i32.add
                local.tee $p4
                f32.load offset=4
                local.set $l17
                local.get $p4
                f32.load
                local.set $l20
                local.get $l5
                local.get $p4
                f32.load offset=8
                local.get $l19
                f32.sub
                f32.store offset=1144
                local.get $l5
                local.get $l17
                local.get $l18
                f32.sub
                f32.store offset=1140
                local.get $l5
                local.get $l20
                local.get $l15
                f32.sub
                f32.store offset=1136
                local.get $l5
                i32.const 1120
                i32.add
                local.get $l9
                local.get $p3
                local.get $p2
                local.get $p4
                local.get $l5
                i32.const 80
                i32.add
                local.get $l5
                i32.const 1136
                i32.add
                call $f69961
                local.get $l5
                f32.load offset=1120
                local.get $l5
                f32.load offset=48
                local.tee $l18
                f32.sub
                local.tee $l17
                local.get $l17
                f32.mul
                local.get $l5
                f32.load offset=1124
                local.get $l5
                f32.load offset=52
                local.tee $l19
                f32.sub
                local.tee $l17
                local.get $l17
                f32.mul
                f32.add
                local.get $l5
                f32.load offset=1128
                local.get $l5
                f32.load offset=56
                local.tee $l17
                f32.sub
                local.tee $l20
                local.get $l20
                f32.mul
                f32.add
                local.get $l5
                f32.load offset=60
                local.tee $l20
                f32.le
                br_if $B56
                local.get $l12
                i32.const 1
                i32.sub
                local.tee $l12
                i32.eqz
                br_if $B57
                local.get $l6
                i32.const 1
                i32.add
                local.set $l6
                local.get $l5
                i32.load offset=4
                local.set $p4
                local.get $l5
                i32.load
                local.set $p3
                br $L83
              end
              unreachable
            end
            i32.const 0
            local.set $l10
          end
          local.get $l5
          i32.const 1152
          i32.add
          global.set $g0
          local.get $l10
          local.set $p2
        end
        local.get $p2
        i32.const 0
        i32.ne
        br $B0
      end
      local.get $p3
      f32.load offset=8
      local.set $l17
      local.get $l7
      local.get $p4
      i32.store offset=128
      local.get $l7
      local.get $l17
      local.get $l16
      local.get $l15
      f32.mul
      f32.mul
      f32.const 0x0p+0 (;=0;)
      f32.lt
      i32.store8 offset=133
      local.get $l7
      i32.const 0
      i32.store8 offset=132
      local.get $l7
      f32.const 0x1p+0 (;=1;)
      local.get $p3
      f32.load offset=12
      local.tee $l18
      local.get $l18
      local.get $l18
      f32.add
      local.tee $l19
      f32.mul
      f32.sub
      local.tee $l27
      local.get $p3
      f32.load offset=16
      local.tee $l20
      local.get $l20
      local.get $l20
      f32.add
      local.tee $l22
      f32.mul
      local.tee $l31
      f32.sub
      local.tee $l21
      local.get $l21
      local.get $l17
      f32.mul
      local.tee $l26
      f32.mul
      local.get $l19
      local.get $p3
      f32.load offset=20
      local.tee $l18
      f32.mul
      local.tee $l32
      local.get $l22
      local.get $p3
      f32.load offset=24
      local.tee $l23
      f32.mul
      local.tee $l33
      f32.add
      local.tee $l25
      local.get $l16
      local.get $l25
      f32.mul
      local.tee $l28
      f32.mul
      local.get $l22
      local.get $l18
      f32.mul
      local.tee $l24
      local.get $l19
      local.get $l23
      f32.mul
      local.tee $l30
      f32.sub
      local.tee $l22
      local.get $l15
      local.get $l22
      f32.mul
      local.tee $l29
      f32.mul
      f32.add
      f32.add
      f32.store offset=168
      local.get $l7
      local.get $l24
      local.get $l30
      f32.add
      local.tee $l24
      local.get $l26
      f32.mul
      local.get $l19
      local.get $l20
      f32.mul
      local.tee $l30
      local.get $l23
      local.get $l18
      local.get $l18
      f32.add
      local.tee $l20
      f32.mul
      local.tee $l23
      f32.sub
      local.tee $l19
      local.get $l28
      f32.mul
      local.get $l27
      local.get $l18
      local.get $l20
      f32.mul
      local.tee $l27
      f32.sub
      local.tee $l18
      local.get $l29
      f32.mul
      f32.add
      f32.add
      f32.store offset=156
      local.get $l7
      local.get $l32
      local.get $l33
      f32.sub
      local.tee $l20
      local.get $l26
      f32.mul
      f32.const 0x1p+0 (;=1;)
      local.get $l31
      f32.sub
      local.get $l27
      f32.sub
      local.tee $l26
      local.get $l28
      f32.mul
      local.get $l30
      local.get $l23
      f32.add
      local.tee $l23
      local.get $l29
      f32.mul
      f32.add
      f32.add
      f32.store offset=144
      local.get $l7
      local.get $l21
      local.get $l24
      local.get $l17
      f32.mul
      local.tee $l28
      f32.mul
      local.get $l25
      local.get $l16
      local.get $l19
      f32.mul
      local.tee $l29
      f32.mul
      local.get $l22
      local.get $l15
      local.get $l18
      f32.mul
      local.tee $l27
      f32.mul
      f32.add
      f32.add
      f32.store offset=164
      local.get $l7
      local.get $l21
      local.get $l20
      local.get $l17
      f32.mul
      local.tee $l17
      f32.mul
      local.get $l25
      local.get $l16
      local.get $l26
      f32.mul
      local.tee $l16
      f32.mul
      local.get $l22
      local.get $l15
      local.get $l23
      f32.mul
      local.tee $l15
      f32.mul
      f32.add
      f32.add
      f32.store offset=160
      local.get $l7
      local.get $l24
      local.get $l28
      f32.mul
      local.get $l19
      local.get $l29
      f32.mul
      local.get $l18
      local.get $l27
      f32.mul
      f32.add
      f32.add
      f32.store offset=152
      local.get $l7
      local.get $l24
      local.get $l17
      f32.mul
      local.get $l19
      local.get $l16
      f32.mul
      local.get $l18
      local.get $l15
      f32.mul
      f32.add
      f32.add
      f32.store offset=148
      local.get $l7
      local.get $l20
      local.get $l28
      f32.mul
      local.get $l26
      local.get $l29
      f32.mul
      local.get $l23
      local.get $l27
      f32.mul
      f32.add
      f32.add
      f32.store offset=140
      local.get $l7
      local.get $l20
      local.get $l17
      f32.mul
      local.get $l26
      local.get $l16
      f32.mul
      local.get $l23
      local.get $l15
      f32.mul
      f32.add
      f32.add
      f32.store offset=136
      local.get $l7
      local.get $p0
      f32.load offset=8
      local.tee $l24
      local.get $p2
      f32.load offset=24
      f32.sub
      local.tee $l15
      local.get $l15
      f32.add
      local.tee $l16
      local.get $p2
      f32.load offset=12
      local.tee $l15
      local.get $l15
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l25
      f32.mul
      local.get $l15
      local.get $p0
      f32.load offset=4
      local.tee $l26
      local.get $p2
      f32.load offset=20
      f32.sub
      local.tee $l17
      local.get $l17
      f32.add
      local.tee $l17
      local.get $p2
      f32.load
      local.tee $l18
      f32.mul
      local.get $p0
      f32.load
      local.tee $l23
      local.get $p2
      f32.load offset=16
      f32.sub
      local.tee $l19
      local.get $l19
      f32.add
      local.tee $l19
      local.get $p2
      f32.load offset=4
      local.tee $l20
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      local.get $p2
      f32.load offset=8
      local.tee $l21
      local.get $l19
      local.get $l18
      f32.mul
      local.get $l17
      local.get $l20
      f32.mul
      f32.add
      local.get $l16
      local.get $l21
      f32.mul
      f32.add
      local.tee $l22
      f32.mul
      f32.add
      f32.store offset=180
      local.get $l7
      local.get $l20
      local.get $l22
      f32.mul
      local.get $l17
      local.get $l25
      f32.mul
      local.get $l15
      local.get $l19
      local.get $l21
      f32.mul
      local.get $l16
      local.get $l18
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      f32.store offset=176
      local.get $l7
      local.get $l18
      local.get $l22
      f32.mul
      local.get $l19
      local.get $l25
      f32.mul
      local.get $l15
      local.get $l16
      local.get $l20
      f32.mul
      local.get $l17
      local.get $l21
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      f32.store offset=172
      local.get $l7
      local.get $p0
      f32.load offset=12
      local.tee $l15
      local.get $l15
      f32.mul
      f32.store offset=184
      local.get $l7
      local.get $l15
      f32.store offset=120
      local.get $l7
      local.get $l15
      f32.store offset=116
      local.get $l7
      local.get $l24
      f32.store offset=108
      local.get $l7
      local.get $l26
      f32.store offset=104
      local.get $l7
      i32.const 1065353216
      i32.store offset=96
      local.get $l7
      i64.const 1065353216
      i64.store offset=80
      local.get $l7
      local.get $l15
      f32.store offset=112
      local.get $l7
      local.get $l23
      f32.store offset=100
      local.get $l7
      i64.const 0
      i64.store offset=88
      local.get $l7
      i64.const 0
      i64.store offset=72
      local.get $l7
      i64.const 1065353216
      i64.store offset=64
      local.get $l7
      local.get $l7
      i32.const -64
      i32.sub
      local.get $p2
      local.get $p3
      call $f69940
      local.get $l7
      local.get $p1
      i32.const 119661
      local.get $l7
      i32.const 128
      i32.add
      call $f69989
      local.get $l7
      i32.load8_u offset=132
      i32.const 0
      i32.ne
    end
    local.set $p2
    local.get $l7
    i32.const 192
    i32.add
    global.set $g0
    local.get $p2)
