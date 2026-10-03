  (func $f73138 (type $t530) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (param $p9 f32) (param $p10 i32) (param $p11 i32) (param $p12 i32) (param $p13 i32) (result i32)
    (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f64) (local $l54 f64) (local $l55 f64) (local $l56 f64) (local $l57 f64) (local $l58 f64)
    global.get $g0
    i32.const 288
    i32.sub
    local.tee $l14
    global.set $g0
    block $B0
      block $B1
        local.get $p5
        f32.load
        f32.const 0x0p+0 (;=0;)
        f32.ne
        br_if $B1
        local.get $p5
        f32.load offset=4
        f32.const 0x0p+0 (;=0;)
        f32.ne
        br_if $B1
        local.get $p5
        f32.load offset=8
        f32.const 0x0p+0 (;=0;)
        f32.eq
        br_if $B0
      end
      local.get $p0
      local.get $p0
      i32.load offset=324
      i32.const -53
      i32.and
      i32.store offset=324
      local.get $p13
      i32.const 0
      i32.store
      local.get $p12
      i32.const 0
      i32.store
      local.get $p0
      i32.const -1
      i32.store offset=176
      local.get $p2
      i32.load
      i32.load8_u offset=514
      local.set $l15
      local.get $l14
      local.get $p4
      i64.load offset=24
      i64.store offset=88
      local.get $l14
      local.get $p4
      i64.load offset=16
      i64.store offset=80
      local.get $l14
      local.get $p4
      i64.load offset=8
      i64.store offset=72
      block $B2
        local.get $p7
        i32.eqz
        if $I3
          i32.const 0
          local.set $l15
          br $B2
        end
        local.get $l14
        i32.const 224
        i32.add
        local.set $l22
        local.get $l14
        i32.const 252
        i32.add
        local.set $l23
        local.get $l14
        i32.const 36
        i32.add
        local.set $l24
        local.get $p4
        f64.load offset=8
        local.get $p5
        f32.load
        f64.promote_f32
        f64.add
        local.set $l55
        local.get $p4
        f64.load offset=16
        local.get $p5
        f32.load offset=4
        f64.promote_f32
        f64.add
        local.set $l56
        local.get $p4
        f64.load offset=24
        local.get $p5
        f32.load offset=8
        f64.promote_f32
        f64.add
        local.set $l57
        local.get $l14
        f64.load offset=88
        local.set $l53
        local.get $l14
        f64.load offset=80
        local.set $l54
        local.get $l14
        f64.load offset=72
        local.set $l58
        local.get $p11
        i32.const 3
        i32.eq
        local.set $l26
        local.get $p11
        i32.const -3
        i32.and
        i32.const 1
        i32.ne
        local.set $l28
        local.get $l15
        i32.const 255
        i32.and
        i32.const 0
        i32.ne
        local.set $l29
        i32.const 0
        local.set $l15
        loop $L4
          local.get $p0
          local.get $p0
          i32.load16_u offset=322
          i32.const 1
          i32.add
          i32.store16 offset=322
          local.get $l14
          local.get $l57
          local.get $l53
          f64.sub
          f32.demote_f64
          f32.store offset=64
          local.get $l14
          local.get $l56
          local.get $l54
          f64.sub
          f32.demote_f64
          f32.store offset=60
          local.get $l14
          local.get $l55
          local.get $l58
          f64.sub
          f32.demote_f64
          f32.store offset=56
          local.get $p4
          local.get $p0
          local.get $l14
          i32.const 216
          i32.add
          local.get $l14
          i32.const 72
          i32.add
          local.get $l14
          i32.const 56
          i32.add
          local.get $p4
          i32.load
          i32.load offset=8
          call_indirect $__indirect_function_table (type $t6)
          local.get $p0
          local.get $p1
          local.get $p3
          local.get $l14
          i32.const 216
          i32.add
          local.get $p10
          local.get $p6
          call $f73133
          local.get $l14
          f32.load offset=56
          local.tee $l32
          local.get $l32
          f32.mul
          local.get $l14
          f32.load offset=60
          local.tee $l31
          local.get $l31
          f32.mul
          f32.add
          local.get $l14
          f32.load offset=64
          local.tee $l34
          local.get $l34
          f32.mul
          f32.add
          f32.sqrt
          local.tee $l37
          local.get $p9
          f32.le
          br_if $B2
          local.get $l14
          local.get $l34
          f32.const 0x1p+0 (;=1;)
          local.get $l37
          f32.div
          local.tee $l33
          f32.mul
          local.tee $l34
          f32.store offset=64
          local.get $l14
          local.get $l32
          local.get $l33
          f32.mul
          local.tee $l32
          f32.store offset=56
          local.get $l14
          local.get $l31
          local.get $l33
          f32.mul
          local.tee $l31
          f32.store offset=60
          local.get $l32
          local.get $p5
          f32.load
          f32.mul
          local.get $l31
          local.get $p5
          f32.load offset=4
          f32.mul
          f32.add
          local.get $l34
          local.get $p5
          f32.load offset=8
          f32.mul
          f32.add
          f32.const 0x0p+0 (;=0;)
          f32.le
          br_if $B2
          local.get $l14
          local.get $l37
          local.get $p0
          f32.load offset=276
          f32.add
          f32.store offset=36
          local.get $p0
          i32.load8_u offset=298
          local.set $l21
          local.get $l14
          i32.const 0
          i32.store offset=48
          local.get $l14
          i64.const -1
          i64.store offset=40
          block $B5
            local.get $p0
            i32.load offset=36
            local.tee $l16
            if $I6
              local.get $p0
              i32.load offset=32
              local.tee $l15
              local.get $l16
              i32.const 2
              i32.shl
              i32.add
              local.set $l18
              i32.const 0
              local.set $l20
              local.get $l14
              i32.load offset=48
              local.set $l17
              local.get $l14
              f32.load offset=32
              local.set $l35
              local.get $l14
              f32.load offset=28
              local.set $l34
              local.get $l14
              f32.load offset=24
              local.set $l33
              block $B7
                block $B8
                  block $B9
                    loop $L10
                      local.get $l18
                      local.get $l15
                      local.get $p4
                      i32.load offset=36
                      i32.const 24
                      i32.mul
                      local.get $l15
                      i32.load
                      local.tee $l16
                      i32.const 2
                      i32.shl
                      i32.add
                      i32.const 3223168
                      i32.add
                      i32.load
                      local.tee $l19
                      if $I11 (result i32)
                        local.get $l14
                        i64.const -1
                        i64.store offset=256
                        local.get $l14
                        local.get $l14
                        f32.load offset=36
                        local.tee $l32
                        f32.store offset=252
                        block $B12
                          local.get $p0
                          local.get $p4
                          local.get $l15
                          local.get $l14
                          i32.const 72
                          i32.add
                          local.get $l14
                          i32.const 56
                          i32.add
                          local.get $l14
                          i32.const 216
                          i32.add
                          local.get $l19
                          call_indirect $__indirect_function_table (type $t10)
                          i32.eqz
                          br_if $B12
                          local.get $l14
                          f32.load offset=252
                          local.tee $l31
                          f32.const 0x0p+0 (;=0;)
                          f32.eq
                          if $I13
                            local.get $l21
                            i32.const 255
                            i32.and
                            i32.eqz
                            br_if $B12
                            local.get $l15
                            i32.load
                            i32.const 2
                            i32.lt_u
                            br_if $B12
                            block $B14
                              block $B15
                                local.get $l15
                                i32.load offset=8
                                local.tee $l16
                                i32.load16_u offset=4
                                i32.const 5
                                i32.sub
                                br_table $B15 $B14 $B12
                              end
                              local.get $l14
                              i32.const 184
                              i32.add
                              local.get $l16
                              local.get $l16
                              i32.load
                              i32.load offset=216
                              call_indirect $__indirect_function_table (type $t1)
                              local.get $l14
                              i32.load16_u offset=184
                              i32.const 1
                              i32.and
                              i32.eqz
                              br_if $B12
                            end
                            local.get $l14
                            local.get $l22
                            i64.load
                            i64.store offset=8
                            local.get $l14
                            local.get $l14
                            i64.load offset=232
                            i64.store offset=16
                            local.get $l14
                            local.get $l34
                            f32.store offset=28
                            local.get $l14
                            local.get $l33
                            f32.store offset=24
                            local.get $l14
                            local.get $l14
                            f32.load offset=248
                            f32.store offset=32
                            local.get $l14
                            local.get $l14
                            f32.load offset=244
                            f32.store offset=28
                            local.get $l14
                            local.get $l17
                            i32.store offset=48
                            local.get $l14
                            local.get $l14
                            i64.load offset=216
                            i64.store
                            local.get $l14
                            local.get $l14
                            f32.load offset=240
                            f32.store offset=24
                            local.get $l24
                            local.get $l23
                            i32.load offset=8
                            i32.store offset=8
                            local.get $l24
                            local.get $l23
                            i64.load align=4
                            i64.store align=4
                            br $B8
                          end
                          local.get $l31
                          local.get $l32
                          f32.lt
                          i32.eqz
                          br_if $B12
                          local.get $l14
                          local.get $l14
                          i64.load offset=232
                          i64.store offset=16
                          local.get $l14
                          local.get $l22
                          i64.load
                          i64.store offset=8
                          local.get $l14
                          local.get $l14
                          i64.load offset=216
                          i64.store
                          local.get $l14
                          f32.load offset=240
                          local.set $l33
                          local.get $l14
                          f32.load offset=244
                          local.set $l34
                          local.get $l14
                          f32.load offset=248
                          local.set $l35
                          local.get $l24
                          local.get $l23
                          i32.load offset=8
                          i32.store offset=8
                          local.get $l24
                          local.get $l23
                          i64.load align=4
                          i64.store align=4
                          local.get $l31
                          f32.const 0x0p+0 (;=0;)
                          f32.le
                          br_if $B9
                          local.get $l15
                          local.set $l17
                          local.get $l15
                          local.set $l20
                        end
                        local.get $l15
                        i32.load
                      else
                        local.get $l16
                      end
                      i32.const 2
                      i32.shl
                      i32.const 3222832
                      i32.add
                      i32.load
                      i32.add
                      local.tee $l15
                      i32.ne
                      br_if $L10
                    end
                    local.get $l14
                    local.get $l17
                    i32.store offset=48
                    local.get $l14
                    local.get $l35
                    f32.store offset=32
                    local.get $l14
                    local.get $l34
                    f32.store offset=28
                    local.get $l14
                    local.get $l33
                    f32.store offset=24
                    local.get $l20
                    local.set $l15
                    br $B7
                  end
                  local.get $l14
                  local.get $l35
                  f32.store offset=32
                  local.get $l14
                  local.get $l34
                  f32.store offset=28
                  local.get $l14
                  local.get $l33
                  f32.store offset=24
                end
                local.get $l14
                local.get $l15
                i32.store offset=48
                local.get $l15
                local.set $l20
              end
              local.get $l20
              br_if $B5
            end
            local.get $l14
            local.get $l57
            f64.store offset=88
            local.get $l14
            local.get $l56
            f64.store offset=80
            local.get $l14
            local.get $l55
            f64.store offset=72
            i32.const 1
            local.set $l15
            br $B2
          end
          local.get $l14
          f32.load offset=36
          local.set $l32
          block $B16
            local.get $p0
            i32.load8_u offset=298
            i32.eqz
            br_if $B16
            local.get $l32
            f32.const 0x0p+0 (;=0;)
            f32.ne
            br_if $B16
            local.get $l14
            f64.load offset=88
            f32.demote_f64
            local.set $l40
            local.get $l14
            f64.load offset=80
            f32.demote_f64
            local.set $l41
            local.get $l14
            f64.load offset=72
            f32.demote_f64
            local.set $l39
            local.get $p0
            f32.load offset=276
            local.set $l42
            i32.const 0
            local.set $l21
            loop $L17
              block $B18
                local.get $p0
                i32.load offset=36
                local.tee $l16
                i32.eqz
                if $I19
                  i32.const 1
                  local.set $l19
                  br $B18
                end
                local.get $p0
                i32.load offset=32
                local.tee $l15
                local.get $l16
                i32.const 2
                i32.shl
                i32.add
                local.set $l18
                i32.const 1
                local.set $l19
                loop $L20
                  block $B21
                    local.get $l15
                    i32.load
                    i32.const 2
                    i32.lt_u
                    br_if $B21
                    block $B22
                      block $B23
                        local.get $l15
                        i32.load offset=8
                        local.tee $l16
                        i32.load16_u offset=4
                        i32.const 5
                        i32.sub
                        br_table $B23 $B22 $B21
                      end
                      local.get $l14
                      i32.const 216
                      i32.add
                      local.get $l16
                      local.get $l16
                      i32.load
                      i32.load offset=216
                      call_indirect $__indirect_function_table (type $t1)
                      local.get $l14
                      i32.load16_u offset=216
                      i32.const 1
                      i32.and
                      i32.eqz
                      br_if $B21
                    end
                    local.get $l14
                    i32.const 216
                    i32.add
                    local.get $l15
                    i32.load offset=4
                    local.tee $l19
                    local.get $l19
                    i32.load
                    i32.load offset=40
                    call_indirect $__indirect_function_table (type $t1)
                    local.get $l14
                    i32.const 184
                    i32.add
                    local.get $l16
                    local.get $l16
                    i32.load
                    i32.load offset=76
                    call_indirect $__indirect_function_table (type $t1)
                    local.get $l14
                    i32.const 152
                    i32.add
                    local.get $l19
                    local.get $l19
                    i32.load
                    i32.load offset=80
                    call_indirect $__indirect_function_table (type $t1)
                    local.get $l14
                    local.get $l14
                    f32.load offset=196
                    local.tee $l32
                    local.get $l14
                    f32.load offset=164
                    local.tee $l33
                    f32.mul
                    local.get $l14
                    f32.load offset=184
                    local.tee $l31
                    local.get $l14
                    f32.load offset=152
                    local.tee $l35
                    f32.mul
                    f32.sub
                    local.get $l14
                    f32.load offset=188
                    local.tee $l37
                    local.get $l14
                    f32.load offset=156
                    local.tee $l36
                    f32.mul
                    f32.sub
                    local.get $l14
                    f32.load offset=192
                    local.tee $l34
                    local.get $l14
                    f32.load offset=160
                    local.tee $p9
                    f32.mul
                    f32.sub
                    f32.store offset=132
                    local.get $l14
                    local.get $l31
                    local.get $l36
                    f32.mul
                    local.get $l34
                    local.get $l33
                    f32.mul
                    local.get $l32
                    local.get $p9
                    f32.mul
                    f32.add
                    f32.add
                    local.get $l37
                    local.get $l35
                    f32.mul
                    f32.sub
                    f32.store offset=128
                    local.get $l14
                    local.get $l34
                    local.get $l35
                    f32.mul
                    local.get $l37
                    local.get $l33
                    f32.mul
                    local.get $l32
                    local.get $l36
                    f32.mul
                    f32.add
                    f32.add
                    local.get $l31
                    local.get $p9
                    f32.mul
                    f32.sub
                    f32.store offset=124
                    local.get $l14
                    local.get $l32
                    local.get $l35
                    f32.mul
                    local.get $l31
                    local.get $l33
                    f32.mul
                    f32.add
                    local.get $l37
                    local.get $p9
                    f32.mul
                    f32.add
                    local.get $l34
                    local.get $l36
                    f32.mul
                    f32.sub
                    f32.store offset=120
                    local.get $l14
                    local.get $l14
                    f32.load offset=208
                    local.get $l14
                    f32.load offset=176
                    local.tee $l33
                    local.get $l33
                    f32.add
                    local.tee $l33
                    local.get $l32
                    local.get $l32
                    f32.mul
                    f32.const -0x1p-1 (;=-0.5;)
                    f32.add
                    local.tee $p9
                    f32.mul
                    local.get $l32
                    local.get $l31
                    local.get $l14
                    f32.load offset=172
                    local.tee $l35
                    local.get $l35
                    f32.add
                    local.tee $l35
                    f32.mul
                    local.get $l37
                    local.get $l14
                    f32.load offset=168
                    local.tee $l36
                    local.get $l36
                    f32.add
                    local.tee $l36
                    f32.mul
                    f32.sub
                    f32.mul
                    f32.add
                    local.get $l34
                    local.get $l36
                    local.get $l31
                    f32.mul
                    local.get $l35
                    local.get $l37
                    f32.mul
                    f32.add
                    local.get $l33
                    local.get $l34
                    f32.mul
                    f32.add
                    local.tee $l38
                    f32.mul
                    f32.add
                    f32.add
                    f32.store offset=144
                    local.get $l14
                    local.get $l14
                    f32.load offset=204
                    local.get $l37
                    local.get $l38
                    f32.mul
                    local.get $l35
                    local.get $p9
                    f32.mul
                    local.get $l32
                    local.get $l36
                    local.get $l34
                    f32.mul
                    local.get $l33
                    local.get $l31
                    f32.mul
                    f32.sub
                    f32.mul
                    f32.add
                    f32.add
                    f32.add
                    f32.store offset=140
                    local.get $l14
                    local.get $l14
                    f32.load offset=200
                    local.get $l31
                    local.get $l38
                    f32.mul
                    local.get $l36
                    local.get $p9
                    f32.mul
                    local.get $l32
                    local.get $l33
                    local.get $l37
                    f32.mul
                    local.get $l35
                    local.get $l34
                    f32.mul
                    f32.sub
                    f32.mul
                    f32.add
                    f32.add
                    f32.add
                    f32.store offset=136
                    local.get $l14
                    local.get $p0
                    f32.load offset=244
                    f32.store offset=184
                    local.get $l14
                    local.get $p0
                    f32.load offset=248
                    f32.store offset=188
                    local.get $l14
                    local.get $p0
                    f32.load offset=252
                    f32.store offset=192
                    local.get $p0
                    f32.load offset=256
                    local.set $l32
                    local.get $l14
                    local.get $l40
                    f32.store offset=208
                    local.get $l14
                    local.get $l41
                    f32.store offset=204
                    local.get $l14
                    local.get $l39
                    f32.store offset=200
                    local.get $l14
                    local.get $l32
                    f32.store offset=196
                    block $B24
                      local.get $p4
                      i32.load offset=36
                      i32.const 1
                      i32.eq
                      if $I25
                        local.get $p4
                        f32.load offset=40
                        local.set $l32
                        local.get $p4
                        f32.load offset=44
                        local.set $l31
                        local.get $l14
                        i32.const 2
                        i32.store offset=152
                        local.get $l14
                        local.get $l31
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.store offset=160
                        local.get $l14
                        local.get $l42
                        local.get $l32
                        f32.add
                        f32.store offset=156
                        local.get $l14
                        local.get $l14
                        i32.const 216
                        i32.add
                        i32.store offset=104
                        i32.const 0
                        local.set $l19
                        local.get $l14
                        i32.const 104
                        i32.add
                        local.get $l14
                        i32.const 100
                        i32.add
                        local.get $l14
                        i32.const 152
                        i32.add
                        local.get $l14
                        i32.const 184
                        i32.add
                        local.get $l14
                        i32.load offset=104
                        local.get $l14
                        i32.const 120
                        i32.add
                        call $f70315
                        br_if $B24
                        br $B21
                      end
                      local.get $p4
                      f32.load offset=40
                      local.set $l32
                      local.get $p4
                      f32.load offset=44
                      local.set $l31
                      local.get $p4
                      f32.load offset=48
                      local.set $l37
                      local.get $l14
                      i32.const 3
                      i32.store offset=152
                      local.get $l14
                      local.get $l42
                      local.get $l37
                      f32.add
                      f32.store offset=164
                      local.get $l14
                      local.get $l42
                      local.get $l31
                      f32.add
                      f32.store offset=160
                      local.get $l14
                      local.get $l42
                      local.get $l32
                      f32.add
                      f32.store offset=156
                      local.get $l14
                      local.get $l14
                      i32.const 216
                      i32.add
                      i32.store offset=104
                      i32.const 0
                      local.set $l19
                      local.get $l14
                      i32.const 104
                      i32.add
                      local.get $l14
                      i32.const 100
                      i32.add
                      local.get $l14
                      i32.const 152
                      i32.add
                      local.get $l14
                      i32.const 184
                      i32.add
                      local.get $l14
                      i32.load offset=104
                      local.get $l14
                      i32.const 120
                      i32.add
                      call $f70315
                      i32.eqz
                      br_if $B21
                    end
                    i32.const 1
                    local.set $l19
                    local.get $l21
                    i32.const 1
                    i32.add
                    local.set $l21
                    local.get $l40
                    local.get $l14
                    f32.load offset=100
                    local.tee $l32
                    local.get $l14
                    f32.load offset=112
                    f32.mul
                    f32.add
                    local.set $l40
                    local.get $l41
                    local.get $l32
                    local.get $l14
                    f32.load offset=108
                    f32.mul
                    f32.add
                    local.set $l41
                    local.get $l39
                    local.get $l32
                    local.get $l14
                    f32.load offset=104
                    f32.mul
                    f32.add
                    local.set $l39
                  end
                  local.get $l18
                  local.get $l15
                  local.get $l15
                  i32.load
                  i32.const 2
                  i32.shl
                  i32.const 3222832
                  i32.add
                  i32.load
                  i32.add
                  local.tee $l15
                  i32.ne
                  br_if $L20
                end
              end
              local.get $l19
              i32.const 1
              i32.and
              local.get $l21
              i32.const 3
              i32.le_u
              i32.and
              br_if $L17
            end
            local.get $p8
            if $I26
              local.get $p8
              local.get $l25
              i32.const 1
              i32.add
              i32.store
            end
            local.get $p4
            local.get $l40
            f64.promote_f32
            f64.store offset=24
            local.get $p4
            local.get $l41
            f64.promote_f32
            f64.store offset=16
            local.get $p4
            local.get $l39
            f64.promote_f32
            f64.store offset=8
            i32.const 1
            local.set $l15
            br $B0
          end
          block $B27
            local.get $l20
            i32.load
            i32.const 1
            i32.le_u
            if $I28
              i32.const 0
              local.set $l19
              i32.const 1
              local.set $l16
              local.get $l26
              br_if $B27
              local.get $p2
              i64.const -4294967296
              i64.store offset=8 align=4
              local.get $l14
              i32.const 56
              i32.add
              local.set $l16
              i32.const 0
              local.set $l27
              global.get $g0
              i32.const 80
              i32.sub
              local.tee $l17
              global.set $g0
              local.get $l14
              local.tee $l15
              i32.load offset=48
              i32.load offset=4
              local.tee $l30
              i32.const 16
              i32.shr_u
              local.set $l21
              local.get $p2
              local.tee $l20
              i32.load
              local.set $l18
              block $B29
                block $B30
                  block $B31
                    block $B32
                      block $B33
                        local.get $l30
                        i32.const 65535
                        i32.and
                        br_table $B33 $B32 $B31 $B29
                      end
                      local.get $l18
                      i32.load offset=520
                      i32.load offset=68
                      local.get $l21
                      i32.const 2
                      i32.shl
                      i32.add
                      i32.load
                      local.set $l20
                      local.get $l17
                      local.get $l18
                      local.get $l18
                      i32.load
                      i32.load offset=16
                      call_indirect $__indirect_function_table (type $t5)
                      i32.store offset=8
                      local.get $l17
                      local.get $l15
                      i64.load offset=8
                      i64.store offset=24
                      local.get $l17
                      local.get $l15
                      i64.load offset=16
                      i64.store offset=32
                      local.get $l17
                      local.get $l15
                      i64.load
                      i64.store offset=16
                      local.get $l17
                      local.get $l15
                      f32.load offset=24
                      f32.store offset=40
                      local.get $l17
                      local.get $l15
                      f32.load offset=28
                      f32.store offset=44
                      local.get $l17
                      local.get $l15
                      f32.load offset=32
                      f32.store offset=48
                      local.get $l17
                      local.get $l16
                      f32.load
                      f32.store offset=52
                      local.get $l17
                      local.get $l16
                      f32.load offset=4
                      f32.store offset=56
                      local.get $l17
                      local.get $l16
                      f32.load offset=8
                      f32.store offset=60
                      local.get $l17
                      local.get $l37
                      f32.store offset=64
                      local.get $l17
                      local.get $l20
                      local.get $l20
                      i32.load
                      i32.load offset=16
                      call_indirect $__indirect_function_table (type $t5)
                      i32.store offset=68
                      local.get $l18
                      i32.load offset=72
                      local.tee $l15
                      if $I34
                        local.get $l15
                        local.get $l17
                        i32.const 8
                        i32.add
                        local.get $l15
                        i32.load
                        i32.load offset=4
                        call_indirect $__indirect_function_table (type $t1)
                      end
                      local.get $l18
                      i32.load offset=76
                      local.tee $l15
                      i32.eqz
                      br_if $B29
                      local.get $l17
                      i32.const 72
                      i32.add
                      local.get $l15
                      local.get $l17
                      i32.load offset=68
                      local.get $l15
                      i32.load
                      i32.load offset=4
                      call_indirect $__indirect_function_table (type $t2)
                      br $B30
                    end
                    local.get $l17
                    local.get $l18
                    local.get $l18
                    i32.load
                    i32.load offset=16
                    call_indirect $__indirect_function_table (type $t5)
                    i32.store offset=8
                    local.get $l17
                    local.get $l15
                    i64.load offset=8
                    i64.store offset=24
                    local.get $l17
                    local.get $l15
                    i64.load offset=16
                    i64.store offset=32
                    local.get $l17
                    local.get $l15
                    i64.load
                    i64.store offset=16
                    local.get $l17
                    local.get $l15
                    f32.load offset=24
                    f32.store offset=40
                    local.get $l17
                    local.get $l15
                    f32.load offset=28
                    f32.store offset=44
                    local.get $l17
                    local.get $l15
                    f32.load offset=32
                    f32.store offset=48
                    local.get $l17
                    local.get $l16
                    f32.load
                    f32.store offset=52
                    local.get $l17
                    local.get $l16
                    f32.load offset=4
                    f32.store offset=56
                    local.get $l17
                    local.get $l16
                    f32.load offset=8
                    f32.store offset=60
                    local.get $l17
                    local.get $l37
                    f32.store offset=64
                    local.get $l17
                    local.get $l20
                    i32.load offset=4
                    i32.load offset=4
                    local.get $l21
                    i32.const 72
                    i32.mul
                    i32.add
                    local.tee $l15
                    i32.load offset=12
                    i32.store offset=68
                    local.get $l20
                    local.get $l15
                    i32.const 8
                    i32.add
                    local.tee $l16
                    i32.store offset=8
                    local.get $l20
                    local.get $l15
                    i32.load
                    i32.store offset=12
                    local.get $l18
                    i32.load offset=72
                    local.tee $l15
                    if $I35
                      local.get $l15
                      local.get $l17
                      i32.const 8
                      i32.add
                      local.get $l15
                      i32.load
                      i32.load offset=8
                      call_indirect $__indirect_function_table (type $t1)
                    end
                    local.get $l18
                    i32.load offset=76
                    local.tee $l15
                    i32.eqz
                    br_if $B29
                    local.get $l17
                    i32.const 72
                    i32.add
                    local.get $l15
                    local.get $l16
                    local.get $l15
                    i32.load
                    i32.load offset=8
                    call_indirect $__indirect_function_table (type $t2)
                    br $B30
                  end
                  local.get $l17
                  local.get $l18
                  local.get $l18
                  i32.load
                  i32.load offset=16
                  call_indirect $__indirect_function_table (type $t5)
                  i32.store offset=8
                  local.get $l17
                  local.get $l15
                  i64.load offset=8
                  i64.store offset=24
                  local.get $l17
                  local.get $l15
                  i64.load offset=16
                  i64.store offset=32
                  local.get $l17
                  local.get $l15
                  i64.load
                  i64.store offset=16
                  local.get $l17
                  local.get $l15
                  f32.load offset=24
                  f32.store offset=40
                  local.get $l17
                  local.get $l15
                  f32.load offset=28
                  f32.store offset=44
                  local.get $l17
                  local.get $l15
                  f32.load offset=32
                  f32.store offset=48
                  local.get $l17
                  local.get $l16
                  f32.load
                  f32.store offset=52
                  local.get $l17
                  local.get $l16
                  f32.load offset=4
                  f32.store offset=56
                  local.get $l17
                  local.get $l16
                  f32.load offset=8
                  f32.store offset=60
                  local.get $l17
                  local.get $l37
                  f32.store offset=64
                  local.get $l17
                  local.get $l20
                  i32.load offset=4
                  i32.load offset=16
                  local.get $l21
                  i32.const 6
                  i32.shl
                  i32.add
                  local.tee $l15
                  i32.load offset=12
                  i32.store offset=68
                  local.get $l20
                  local.get $l15
                  i32.const 8
                  i32.add
                  local.tee $l16
                  i32.store offset=8
                  local.get $l20
                  local.get $l15
                  i32.load
                  i32.store offset=12
                  local.get $l18
                  i32.load offset=72
                  local.tee $l15
                  if $I36
                    local.get $l15
                    local.get $l17
                    i32.const 8
                    i32.add
                    local.get $l15
                    i32.load
                    i32.load offset=8
                    call_indirect $__indirect_function_table (type $t1)
                  end
                  local.get $l18
                  i32.load offset=76
                  local.tee $l15
                  i32.eqz
                  br_if $B29
                  local.get $l17
                  i32.const 72
                  i32.add
                  local.get $l15
                  local.get $l16
                  local.get $l15
                  i32.load
                  i32.load offset=8
                  call_indirect $__indirect_function_table (type $t2)
                end
                local.get $l17
                i32.load8_u offset=72
                local.set $l27
              end
              local.get $l17
              i32.const 80
              i32.add
              global.set $g0
              local.get $l27
              i32.const 2
              i32.and
              i32.eqz
              local.set $l16
              local.get $p11
              i32.const 2
              i32.ne
              br_if $B27
              local.get $p0
              i32.load offset=324
              local.set $l18
              local.get $p2
              i32.load offset=8
              local.tee $l15
              if $I37
                local.get $p0
                local.get $p2
                i32.load offset=12
                i32.store offset=176
                local.get $p0
                local.get $l18
                i32.const 32
                i32.or
                i32.store offset=324
                local.get $l14
                f64.load
                local.set $l53
                local.get $l14
                f64.load offset=8
                local.set $l54
                local.get $p0
                local.get $l14
                f64.load offset=16
                f32.demote_f64
                local.tee $l31
                f32.store offset=236
                local.get $p0
                local.get $l54
                f32.demote_f64
                local.tee $l36
                f32.store offset=232
                local.get $p0
                local.get $l53
                f32.demote_f64
                local.tee $l33
                f32.store offset=228
                local.get $p0
                local.get $l15
                f32.load offset=40
                local.tee $l37
                local.get $l15
                f32.load offset=32
                local.tee $l34
                local.get $l33
                local.get $l15
                f64.load offset=8
                f32.demote_f64
                f32.sub
                local.tee $l33
                local.get $l33
                f32.add
                local.tee $l33
                f32.mul
                local.get $l15
                f32.load offset=36
                local.tee $l35
                local.get $l36
                local.get $l15
                f64.load offset=16
                f32.demote_f64
                f32.sub
                local.tee $l36
                local.get $l36
                f32.add
                local.tee $l36
                f32.mul
                f32.add
                local.get $l37
                local.get $l31
                local.get $l15
                f64.load offset=24
                f32.demote_f64
                f32.sub
                local.tee $l31
                local.get $l31
                f32.add
                local.tee $l38
                f32.mul
                f32.add
                local.tee $l40
                f32.mul
                local.get $l38
                local.get $l15
                f32.load offset=44
                local.tee $l31
                local.get $l31
                f32.mul
                f32.const -0x1p-1 (;=-0.5;)
                f32.add
                local.tee $l41
                f32.mul
                local.get $l31
                local.get $l34
                local.get $l36
                f32.mul
                local.get $l33
                local.get $l35
                f32.mul
                f32.sub
                f32.mul
                f32.sub
                f32.add
                f32.store offset=224
                local.get $p0
                local.get $l35
                local.get $l40
                f32.mul
                local.get $l36
                local.get $l41
                f32.mul
                local.get $l31
                local.get $l33
                local.get $l37
                f32.mul
                local.get $l34
                local.get $l38
                f32.mul
                f32.sub
                f32.mul
                f32.sub
                f32.add
                f32.store offset=220
                local.get $p0
                local.get $l34
                local.get $l40
                f32.mul
                local.get $l33
                local.get $l41
                f32.mul
                local.get $l31
                local.get $l35
                local.get $l38
                f32.mul
                local.get $l36
                local.get $l37
                f32.mul
                f32.sub
                f32.mul
                f32.sub
                f32.add
                f32.store offset=216
                br $B27
              end
              local.get $p0
              local.get $l18
              i32.const 16
              i32.or
              i32.store offset=324
              br $B27
            end
            local.get $l20
            i32.load offset=4
            local.set $l16
            block $B38
              block $B39
                block $B40
                  block $B41
                    block $B42
                      local.get $l20
                      i32.load offset=8
                      local.tee $l19
                      i32.load16_u offset=4
                      local.tee $l18
                      i32.const 6
                      i32.ne
                      if $I43
                        local.get $l18
                        i32.const 5
                        i32.eq
                        local.get $l29
                        i32.and
                        local.set $l18
                        local.get $p11
                        i32.const 2
                        i32.eq
                        br_if $B42
                        local.get $l18
                        i32.const 1
                        i32.xor
                        local.set $l16
                        br $B39
                      end
                      local.get $p11
                      i32.const 2
                      i32.ne
                      if $I44
                        i32.const 0
                        local.set $l16
                        br $B39
                      end
                      local.get $p0
                      local.get $p0
                      i32.load offset=324
                      i32.const -49
                      i32.and
                      local.tee $l15
                      i32.store offset=324
                      br $B41
                    end
                    local.get $p0
                    local.get $p0
                    i32.load offset=324
                    i32.const -49
                    i32.and
                    local.tee $l15
                    i32.store offset=324
                    local.get $l18
                    i32.eqz
                    br_if $B40
                  end
                  local.get $l14
                  i32.load offset=40
                  local.tee $l18
                  i32.const -1
                  i32.eq
                  br_if $B40
                  local.get $p0
                  local.get $l15
                  i32.const 4
                  i32.or
                  i32.store offset=324
                  local.get $p0
                  local.get $p0
                  i32.load offset=8
                  local.get $l18
                  i32.const 36
                  i32.mul
                  i32.add
                  local.tee $l15
                  f32.load
                  local.get $p0
                  f32.load offset=260
                  local.tee $l32
                  f32.mul
                  local.get $l15
                  f32.load offset=4
                  local.get $p0
                  f32.load offset=264
                  local.tee $l31
                  f32.mul
                  f32.add
                  local.get $l15
                  f32.load offset=8
                  local.get $p0
                  f32.load offset=268
                  local.tee $l34
                  f32.mul
                  f32.add
                  local.tee $l33
                  local.get $l32
                  local.get $l15
                  f32.load offset=12
                  f32.mul
                  local.get $l31
                  local.get $l15
                  i32.const 16
                  i32.add
                  local.tee $l18
                  f32.load
                  f32.mul
                  f32.add
                  local.get $l34
                  local.get $l15
                  i32.const 20
                  i32.add
                  local.tee $l21
                  f32.load
                  f32.mul
                  f32.add
                  local.tee $l35
                  local.get $l33
                  local.get $l35
                  f32.gt
                  select
                  local.tee $l38
                  local.get $l32
                  local.get $l15
                  f32.load offset=24
                  f32.mul
                  local.get $l31
                  local.get $l15
                  i32.const 28
                  i32.add
                  local.tee $l20
                  f32.load
                  f32.mul
                  f32.add
                  local.get $l34
                  local.get $l15
                  i32.const 32
                  i32.add
                  local.tee $l17
                  f32.load
                  f32.mul
                  f32.add
                  local.tee $l36
                  local.get $l36
                  local.get $l38
                  f32.lt
                  select
                  local.get $l32
                  local.get $p0
                  f64.load offset=48
                  local.get $p0
                  f64.load offset=72
                  f64.add
                  f64.const 0x1p-1 (;=0.5;)
                  f64.mul
                  f32.demote_f64
                  f32.mul
                  local.get $l31
                  local.get $p0
                  f64.load offset=56
                  local.get $p0
                  f64.load offset=80
                  f64.add
                  f64.const 0x1p-1 (;=0.5;)
                  f64.mul
                  f32.demote_f64
                  f32.mul
                  f32.add
                  local.get $l34
                  local.get $p0
                  f64.load offset=64
                  local.get $p0
                  f64.load offset=88
                  f64.add
                  f64.const 0x1p-1 (;=0.5;)
                  f64.mul
                  f32.demote_f64
                  f32.mul
                  f32.add
                  local.tee $l32
                  f32.add
                  f32.store offset=148
                  local.get $p0
                  local.get $l33
                  local.get $l35
                  local.get $l33
                  local.get $l35
                  f32.lt
                  select
                  local.tee $l31
                  local.get $l36
                  local.get $l31
                  local.get $l36
                  f32.lt
                  select
                  local.get $l32
                  f32.add
                  f32.store offset=144
                  local.get $l21
                  f32.load
                  local.set $l34
                  local.get $l17
                  f32.load
                  local.set $l33
                  local.get $l15
                  f32.load offset=8
                  local.set $l31
                  local.get $p0
                  local.get $l15
                  f32.load offset=12
                  local.get $l15
                  f32.load
                  local.tee $l32
                  f32.sub
                  local.tee $l35
                  local.get $l20
                  f32.load
                  local.get $l15
                  f32.load offset=4
                  local.tee $l36
                  f32.sub
                  local.tee $l38
                  f32.mul
                  local.get $l18
                  f32.load
                  local.get $l36
                  f32.sub
                  local.tee $l36
                  local.get $l15
                  f32.load offset=24
                  local.get $l32
                  f32.sub
                  local.tee $l40
                  f32.mul
                  f32.sub
                  local.tee $l32
                  f32.store offset=128
                  local.get $p0
                  local.get $l34
                  local.get $l31
                  f32.sub
                  local.tee $l34
                  local.get $l40
                  f32.mul
                  local.get $l35
                  local.get $l33
                  local.get $l31
                  f32.sub
                  local.tee $l33
                  f32.mul
                  f32.sub
                  local.tee $l31
                  f32.store offset=124
                  local.get $p0
                  local.get $l36
                  local.get $l33
                  f32.mul
                  local.get $l34
                  local.get $l38
                  f32.mul
                  f32.sub
                  local.tee $l34
                  f32.store offset=120
                  local.get $l32
                  local.get $l32
                  f32.mul
                  local.get $l34
                  local.get $l34
                  f32.mul
                  local.get $l31
                  local.get $l31
                  f32.mul
                  f32.add
                  f32.add
                  f32.sqrt
                  local.tee $l33
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  i32.eqz
                  br_if $B40
                  local.get $p0
                  local.get $l32
                  f32.const 0x1p+0 (;=1;)
                  local.get $l33
                  f32.div
                  local.tee $l33
                  f32.mul
                  f32.store offset=128
                  local.get $p0
                  local.get $l31
                  local.get $l33
                  f32.mul
                  f32.store offset=124
                  local.get $p0
                  local.get $l34
                  local.get $l33
                  f32.mul
                  f32.store offset=120
                end
                local.get $p13
                local.get $l16
                i32.store
                local.get $p12
                local.get $l19
                i32.store
                local.get $l14
                i32.const 216
                i32.add
                local.get $l19
                local.get $l19
                i32.load
                i32.load offset=76
                call_indirect $__indirect_function_table (type $t1)
                local.get $l14
                i32.const 184
                i32.add
                local.get $l16
                local.get $l16
                i32.load
                i32.load offset=80
                call_indirect $__indirect_function_table (type $t1)
                local.get $l14
                f32.load offset=240
                local.set $l43
                local.get $l14
                f32.load offset=232
                local.set $l51
                local.get $l14
                f32.load offset=192
                local.set $l35
                local.get $l14
                f32.load offset=184
                local.set $l36
                local.get $l14
                f32.load offset=196
                local.set $l38
                local.get $l14
                f32.load offset=188
                local.set $l40
                local.get $l14
                f32.load offset=236
                local.set $l44
                local.get $l14
                f32.load offset=220
                local.set $l31
                local.get $l14
                f32.load offset=204
                local.set $l42
                local.get $l14
                f32.load offset=228
                local.set $l32
                local.get $l14
                f32.load offset=224
                local.set $l34
                local.get $l14
                f32.load offset=200
                local.set $l45
                local.get $l14
                f32.load offset=216
                local.set $l33
                local.get $l14
                f32.load offset=208
                local.set $l39
                local.get $l14
                f64.load
                local.set $l53
                local.get $l14
                f64.load offset=8
                local.set $l54
                local.get $p0
                local.get $l14
                f64.load offset=16
                f32.demote_f64
                local.tee $l46
                f32.store offset=212
                local.get $p0
                local.get $l54
                f32.demote_f64
                local.tee $l47
                f32.store offset=208
                local.get $p0
                local.get $l53
                f32.demote_f64
                local.tee $l52
                f32.store offset=204
                local.get $p0
                local.get $l32
                local.get $l38
                f32.mul
                local.get $l33
                local.get $l36
                f32.mul
                f32.sub
                local.get $l31
                local.get $l40
                f32.mul
                f32.sub
                local.get $l34
                local.get $l35
                f32.mul
                f32.sub
                local.tee $l41
                local.get $l41
                f32.mul
                f32.const -0x1p-1 (;=-0.5;)
                f32.add
                local.tee $l48
                local.get $l46
                local.get $l43
                local.get $l39
                local.get $l39
                f32.add
                local.tee $l39
                local.get $l32
                local.get $l32
                f32.mul
                f32.const -0x1p-1 (;=-0.5;)
                f32.add
                local.tee $l49
                f32.mul
                local.get $l32
                local.get $l33
                local.get $l42
                local.get $l42
                f32.add
                local.tee $l42
                f32.mul
                local.get $l31
                local.get $l45
                local.get $l45
                f32.add
                local.tee $l45
                f32.mul
                f32.sub
                f32.mul
                f32.add
                local.get $l34
                local.get $l45
                local.get $l33
                f32.mul
                local.get $l42
                local.get $l31
                f32.mul
                f32.add
                local.get $l39
                local.get $l34
                f32.mul
                f32.add
                local.tee $l50
                f32.mul
                f32.add
                f32.add
                f32.sub
                local.tee $l43
                local.get $l43
                f32.add
                local.tee $l43
                f32.mul
                local.get $l41
                local.get $l32
                local.get $l36
                f32.mul
                local.get $l33
                local.get $l38
                f32.mul
                f32.add
                local.get $l31
                local.get $l35
                f32.mul
                f32.add
                local.get $l34
                local.get $l40
                f32.mul
                f32.sub
                local.tee $l46
                local.get $l47
                local.get $l44
                local.get $l31
                local.get $l50
                f32.mul
                local.get $l42
                local.get $l49
                f32.mul
                local.get $l32
                local.get $l45
                local.get $l34
                f32.mul
                local.get $l39
                local.get $l33
                f32.mul
                f32.sub
                f32.mul
                f32.add
                f32.add
                f32.add
                f32.sub
                local.tee $l44
                local.get $l44
                f32.add
                local.tee $l44
                f32.mul
                local.get $l34
                local.get $l36
                f32.mul
                local.get $l31
                local.get $l38
                f32.mul
                local.get $l32
                local.get $l40
                f32.mul
                f32.add
                f32.add
                local.get $l33
                local.get $l35
                f32.mul
                f32.sub
                local.tee $l47
                local.get $l52
                local.get $l51
                local.get $l33
                local.get $l50
                f32.mul
                local.get $l45
                local.get $l49
                f32.mul
                local.get $l32
                local.get $l39
                local.get $l31
                f32.mul
                local.get $l42
                local.get $l34
                f32.mul
                f32.sub
                f32.mul
                f32.add
                f32.add
                f32.add
                f32.sub
                local.tee $l39
                local.get $l39
                f32.add
                local.tee $l39
                f32.mul
                f32.sub
                f32.mul
                f32.sub
                local.get $l33
                local.get $l40
                f32.mul
                local.get $l34
                local.get $l38
                f32.mul
                local.get $l32
                local.get $l35
                f32.mul
                f32.add
                f32.add
                local.get $l31
                local.get $l36
                f32.mul
                f32.sub
                local.tee $l32
                local.get $l46
                local.get $l39
                f32.mul
                local.get $l47
                local.get $l44
                f32.mul
                f32.add
                local.get $l32
                local.get $l43
                f32.mul
                f32.add
                local.tee $l31
                f32.mul
                f32.add
                f32.store offset=200
                local.get $p0
                local.get $l47
                local.get $l31
                f32.mul
                local.get $l48
                local.get $l44
                f32.mul
                local.get $l41
                local.get $l32
                local.get $l39
                f32.mul
                local.get $l46
                local.get $l43
                f32.mul
                f32.sub
                f32.mul
                f32.sub
                f32.add
                f32.store offset=196
                local.get $p0
                local.get $l46
                local.get $l31
                f32.mul
                local.get $l48
                local.get $l39
                f32.mul
                local.get $l41
                local.get $l47
                local.get $l43
                f32.mul
                local.get $l32
                local.get $l44
                f32.mul
                f32.sub
                f32.mul
                f32.sub
                f32.add
                f32.store offset=192
                i32.const 0
                local.set $l19
                local.get $l14
                i32.load offset=48
                local.set $l15
                br $B38
              end
              i32.const 0
              local.set $l19
              block $B45
                local.get $l28
                br_if $B45
                local.get $l16
                br_if $B45
                local.get $l14
                i32.load offset=40
                local.tee $l16
                i32.const -1
                i32.eq
                br_if $B45
                local.get $p0
                local.get $p0
                i32.load offset=324
                i32.const 8
                i32.or
                i32.store offset=324
                local.get $p0
                i32.load offset=8
                local.get $l16
                i32.const 36
                i32.mul
                i32.add
                local.tee $l16
                f32.load offset=20
                local.set $l33
                local.get $l16
                f32.load offset=32
                local.set $l35
                local.get $l16
                f32.load offset=8
                local.set $l34
                local.get $p0
                local.get $l16
                f32.load offset=12
                local.get $l16
                f32.load
                local.tee $l31
                f32.sub
                local.tee $l36
                local.get $l16
                f32.load offset=28
                local.get $l16
                f32.load offset=4
                local.tee $l38
                f32.sub
                local.tee $l40
                f32.mul
                local.get $l16
                f32.load offset=16
                local.get $l38
                f32.sub
                local.tee $l38
                local.get $l16
                f32.load offset=24
                local.get $l31
                f32.sub
                local.tee $l41
                f32.mul
                f32.sub
                local.tee $l31
                f32.store offset=140
                local.get $p0
                local.get $l33
                local.get $l34
                f32.sub
                local.tee $l33
                local.get $l41
                f32.mul
                local.get $l36
                local.get $l35
                local.get $l34
                f32.sub
                local.tee $l35
                f32.mul
                f32.sub
                local.tee $l34
                f32.store offset=136
                local.get $p0
                local.get $l38
                local.get $l35
                f32.mul
                local.get $l33
                local.get $l40
                f32.mul
                f32.sub
                local.tee $l33
                f32.store offset=132
                local.get $l31
                local.get $l31
                f32.mul
                local.get $l33
                local.get $l33
                f32.mul
                local.get $l34
                local.get $l34
                f32.mul
                f32.add
                f32.add
                f32.sqrt
                local.tee $l35
                f32.const 0x0p+0 (;=0;)
                f32.gt
                if $I46
                  local.get $p0
                  local.get $l31
                  f32.const 0x1p+0 (;=1;)
                  local.get $l35
                  f32.div
                  local.tee $l35
                  f32.mul
                  local.tee $l31
                  f32.store offset=140
                  local.get $p0
                  local.get $l34
                  local.get $l35
                  f32.mul
                  local.tee $l34
                  f32.store offset=136
                  local.get $p0
                  local.get $l33
                  local.get $l35
                  f32.mul
                  local.tee $l33
                  f32.store offset=132
                end
                local.get $p0
                i32.load8_u offset=300
                i32.eqz
                br_if $B45
                local.get $l33
                local.get $p0
                f32.load offset=260
                f32.mul
                local.get $l34
                local.get $p0
                f32.load offset=264
                f32.mul
                f32.add
                local.get $l31
                local.get $p0
                f32.load offset=268
                f32.mul
                f32.add
                f32.const 0x0p+0 (;=0;)
                f32.lt
                i32.eqz
                br_if $B45
                i32.const 1
                local.set $l19
              end
              i32.const 1
              local.set $l16
              local.get $l26
              br_if $B27
            end
            local.get $l14
            local.get $p2
            i32.load
            local.tee $l16
            local.get $l16
            i32.load
            i32.load offset=16
            call_indirect $__indirect_function_table (type $t5)
            i32.store offset=216
            local.get $l22
            local.get $l14
            i64.load offset=16
            i64.store offset=16
            local.get $l22
            local.get $l14
            i64.load offset=8
            i64.store offset=8
            local.get $l22
            local.get $l14
            i64.load
            i64.store
            local.get $l14
            local.get $l37
            f32.store offset=272
            local.get $l14
            local.get $l14
            f32.load offset=24
            f32.store offset=248
            local.get $l14
            local.get $l14
            i64.load offset=28 align=4
            i64.store offset=252 align=4
            local.get $l14
            local.get $l14
            f32.load offset=56
            f32.store offset=260
            local.get $l14
            local.get $l14
            i64.load offset=60 align=4
            i64.store offset=264
            local.get $l14
            local.get $l15
            i32.load offset=4
            i32.store offset=276
            local.get $l15
            i32.load offset=8
            local.set $l15
            local.get $l14
            local.get $l14
            i32.load offset=44
            i32.store offset=284
            local.get $l14
            local.get $l15
            i32.store offset=280
            local.get $l16
            i32.load offset=72
            local.tee $l15
            if $I47
              local.get $l15
              local.get $l14
              i32.const 216
              i32.add
              local.get $l15
              i32.load
              i32.load
              call_indirect $__indirect_function_table (type $t1)
            end
            local.get $l16
            i32.load offset=76
            local.tee $l15
            if $I48 (result i32)
              local.get $l14
              i32.const 184
              i32.add
              local.get $l15
              local.get $l14
              i32.load offset=276
              local.get $l14
              i32.load offset=280
              local.get $l15
              i32.load
              i32.load
              call_indirect $__indirect_function_table (type $t4)
              local.get $l14
              i32.load8_u offset=184
              i32.const 2
              i32.and
            else
              i32.const 0
            end
            i32.eqz
            local.set $l16
            local.get $l14
            f32.load offset=36
            local.set $l32
          end
          local.get $p0
          local.get $p0
          f32.load offset=260
          local.tee $l34
          local.get $l14
          f64.load
          f32.demote_f64
          f32.mul
          local.get $p0
          f32.load offset=264
          local.tee $l33
          local.get $l14
          f64.load offset=8
          f32.demote_f64
          f32.mul
          f32.add
          local.get $p0
          f32.load offset=268
          local.tee $l35
          local.get $l14
          f64.load offset=16
          f32.demote_f64
          f32.mul
          f32.add
          f32.store offset=308
          i32.const -1
          i32.const 8
          local.get $l16
          select
          local.set $l15
          local.get $p0
          f32.load offset=276
          local.tee $l31
          local.get $l32
          f32.lt
          if $I49
            local.get $l14
            local.get $l14
            f64.load offset=72
            local.get $l32
            local.get $l31
            f32.sub
            local.tee $l32
            local.get $l14
            f32.load offset=56
            f32.mul
            f64.promote_f32
            f64.add
            f64.store offset=72
            local.get $l14
            local.get $l14
            f64.load offset=80
            local.get $l32
            local.get $l14
            f32.load offset=60
            f32.mul
            f64.promote_f32
            f64.add
            f64.store offset=80
            local.get $l14
            local.get $l14
            f64.load offset=88
            local.get $l32
            local.get $l14
            f32.load offset=64
            f32.mul
            f64.promote_f32
            f64.add
            f64.store offset=88
          end
          i32.const -1
          local.get $l15
          local.get $l25
          select
          local.set $l15
          local.get $p11
          i32.const 2
          i32.ne
          local.set $l16
          local.get $l14
          f32.load offset=32
          local.set $l37
          local.get $l14
          f32.load offset=28
          local.set $l32
          local.get $l14
          f32.load offset=24
          local.set $l31
          block $B50
            local.get $l19
            i32.eqz
            if $I51
              local.get $p0
              i32.load8_u offset=324
              i32.const 2
              i32.and
              i32.eqz
              br_if $B50
              local.get $p0
              i32.load offset=240
              i32.const 1
              i32.eq
              br_if $B50
            end
            local.get $l37
            local.get $l35
            local.get $l34
            local.get $l31
            f32.mul
            local.get $l32
            local.get $l33
            f32.mul
            f32.add
            local.get $l37
            local.get $l35
            f32.mul
            f32.add
            local.tee $l36
            f32.mul
            f32.sub
            local.tee $l37
            local.get $l37
            f32.mul
            local.get $l31
            local.get $l34
            local.get $l36
            f32.mul
            f32.sub
            local.tee $l31
            local.get $l31
            f32.mul
            local.get $l32
            local.get $l33
            local.get $l36
            f32.mul
            f32.sub
            local.tee $l32
            local.get $l32
            f32.mul
            f32.add
            f32.add
            f32.sqrt
            local.tee $l34
            f32.const 0x0p+0 (;=0;)
            f32.gt
            i32.eqz
            br_if $B50
            local.get $l37
            f32.const 0x1p+0 (;=1;)
            local.get $l34
            f32.div
            local.tee $l34
            f32.mul
            local.set $l37
            local.get $l32
            local.get $l34
            f32.mul
            local.set $l32
            local.get $l31
            local.get $l34
            f32.mul
            local.set $l31
          end
          i32.const -1
          local.get $l15
          local.get $l16
          select
          local.set $l15
          local.get $p0
          i32.load offset=324
          i32.const 64
          i32.and
          local.set $l16
          local.get $l14
          f32.load offset=64
          local.tee $l34
          local.get $l37
          local.get $l37
          f32.add
          local.get $l31
          local.get $l14
          f32.load offset=56
          local.tee $l33
          f32.mul
          local.get $l32
          local.get $l14
          f32.load offset=60
          local.tee $l36
          f32.mul
          f32.add
          local.get $l37
          local.get $l34
          f32.mul
          f32.add
          local.tee $l35
          f32.mul
          f32.sub
          local.tee $l34
          local.get $l34
          f32.mul
          local.get $l33
          local.get $l31
          local.get $l31
          f32.add
          local.get $l35
          f32.mul
          f32.sub
          local.tee $l33
          local.get $l33
          f32.mul
          local.get $l36
          local.get $l32
          local.get $l32
          f32.add
          local.get $l35
          f32.mul
          f32.sub
          local.tee $l35
          local.get $l35
          f32.mul
          f32.add
          f32.add
          f32.sqrt
          local.tee $l36
          f32.const 0x0p+0 (;=0;)
          f32.gt
          if $I52
            local.get $l34
            f32.const 0x1p+0 (;=1;)
            local.get $l36
            f32.div
            local.tee $l36
            f32.mul
            local.set $l34
            local.get $l35
            local.get $l36
            f32.mul
            local.set $l35
            local.get $l33
            local.get $l36
            f32.mul
            local.set $l33
          end
          local.get $p7
          local.get $l15
          i32.add
          local.set $p7
          local.get $l34
          local.get $l37
          local.get $l31
          local.get $l33
          f32.mul
          local.get $l32
          local.get $l35
          f32.mul
          f32.add
          local.get $l37
          local.get $l34
          f32.mul
          f32.add
          local.tee $l36
          f32.mul
          f32.sub
          local.set $l37
          local.get $l35
          local.get $l32
          local.get $l36
          f32.mul
          f32.sub
          local.set $l34
          local.get $l33
          local.get $l31
          local.get $l36
          f32.mul
          f32.sub
          local.set $l31
          local.get $l55
          local.get $l14
          f64.load offset=72
          local.tee $l58
          f64.sub
          f32.demote_f64
          local.tee $l32
          local.get $l32
          f32.mul
          local.get $l56
          local.get $l14
          f64.load offset=80
          local.tee $l54
          f64.sub
          f32.demote_f64
          local.tee $l32
          local.get $l32
          f32.mul
          f32.add
          local.get $l57
          local.get $l14
          f64.load offset=88
          local.tee $l53
          f64.sub
          f32.demote_f64
          local.tee $l32
          local.get $l32
          f32.mul
          f32.add
          f32.sqrt
          local.set $l32
          block $B53
            local.get $l16
            i32.eqz
            br_if $B53
            local.get $l37
            local.get $l37
            f32.mul
            local.get $l31
            local.get $l31
            f32.mul
            local.get $l34
            local.get $l34
            f32.mul
            f32.add
            f32.add
            f32.sqrt
            local.tee $l33
            f32.const 0x0p+0 (;=0;)
            f32.gt
            i32.eqz
            br_if $B53
            local.get $l37
            f32.const 0x1p+0 (;=1;)
            local.get $l33
            f32.div
            local.tee $l33
            f32.mul
            local.set $l37
            local.get $l34
            local.get $l33
            f32.mul
            local.set $l34
            local.get $l31
            local.get $l33
            f32.mul
            local.set $l31
          end
          local.get $l25
          i32.const 1
          i32.add
          local.set $l25
          local.get $l53
          local.get $l32
          local.get $l37
          f32.mul
          f64.promote_f32
          f64.add
          local.set $l57
          local.get $l54
          local.get $l32
          local.get $l34
          f32.mul
          f64.promote_f32
          f64.add
          local.set $l56
          local.get $l58
          local.get $l32
          local.get $l31
          f32.mul
          f64.promote_f32
          f64.add
          local.set $l55
          i32.const 1
          local.set $l15
          local.get $p7
          br_if $L4
        end
      end
      local.get $p4
      i32.const 8
      i32.add
      local.set $l16
      local.get $p8
      if $I54
        local.get $p8
        local.get $l25
        i32.store
      end
      local.get $l16
      local.get $l14
      i64.load offset=72
      i64.store
      local.get $l16
      local.get $l14
      i64.load offset=88
      i64.store offset=16
      local.get $l16
      local.get $l14
      i64.load offset=80
      i64.store offset=8
    end
    local.get $l14
    i32.const 288
    i32.add
    global.set $g0
    local.get $l15
    i32.const 1
    i32.and)
