  (func $f71253 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i32) (local $l34 i32) (local $l35 i32) (local $l36 i32) (local $l37 i32) (local $l38 i32) (local $l39 i32) (local $l40 i32) (local $l41 i32) (local $l42 i32) (local $l43 i32) (local $l44 i32) (local $l45 i32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32)
    local.get $p0
    i32.load offset=100
    local.get $p0
    i32.load offset=96
    i32.add
    local.set $l32
    local.get $p0
    i32.load offset=28
    local.tee $l26
    i32.load offset=336
    call $f69738
    local.tee $l18
    i32.eqz
    if $I0
      call $f69753
      local.tee $l18
      i32.const 12195
      i32.const 3152658
      i32.const 3150980
      i32.const 4700888
      i32.load
      local.tee $l1
      local.get $l1
      i32.load
      i32.load offset=20
      call_indirect $__indirect_function_table (type $t5)
      select
      i32.const 3152590
      i32.const 82
      local.get $l18
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
      local.tee $l1
      i32.const 19
      i32.add
      i32.const -16
      i32.and
      local.tee $l18
      i32.const 4
      i32.sub
      local.get $l18
      local.get $l1
      i32.sub
      i32.store
      local.get $l18
      local.get $l26
      i32.load offset=340
      call $f71150
      local.set $l18
    end
    local.get $l18
    i32.const 11856
    i32.add
    i64.const 0
    i64.store align=4
    local.get $l32
    local.get $p0
    i32.load offset=96
    local.tee $l26
    i32.gt_u
    if $I1
      loop $L2
        local.get $p0
        i32.load offset=32
        i32.load offset=12000
        local.get $l26
        i32.const 36
        i32.mul
        i32.add
        local.set $l27
        i32.const 0
        local.set $l22
        i32.const 0
        local.set $l29
        i32.const 0
        local.set $l16
        global.get $g0
        i32.const 1552
        i32.sub
        local.tee $l7
        global.set $g0
        local.get $l27
        i32.load16_u offset=4
        local.tee $l1
        if $I3
          loop $L4
            local.get $p0
            i32.load offset=108
            local.tee $l2
            i32.load offset=32
            local.get $l2
            local.get $p0
            i32.load offset=32
            i32.load offset=12012
            local.get $l27
            i32.load
            local.get $l16
            i32.add
            i32.const 2
            i32.shl
            i32.add
            i32.load
            i32.load offset=12
            i32.load offset=68
            local.tee $l5
            i32.const 7
            i32.and
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.get $l5
            i32.const 3
            i32.shr_u
            i32.add
            i32.const 4
            i32.shl
            i32.add
            local.tee $l2
            i32.load8_u offset=13
            local.set $l4
            local.get $l2
            i32.load8_u offset=12
            local.set $l11
            local.get $l2
            i32.load offset=8
            local.set $l6
            local.get $l2
            i32.load offset=4
            local.set $l3
            local.get $l2
            i32.load
            local.set $l5
            i32.const 0
            local.set $l9
            local.get $l7
            i32.const 0
            i32.store offset=88
            local.get $l7
            i64.const 0
            i64.store offset=80
            i32.const 0
            local.set $l8
            i32.const 1
            local.set $l2
            i32.const 0
            local.set $l14
            local.get $l5
            if $I5
              local.get $l5
              i32.load8_u offset=43
              local.set $l2
              local.get $l7
              local.get $l3
              i32.store offset=96
              local.get $l7
              local.get $l5
              i32.store offset=92
              local.get $l7
              local.get $l6
              local.get $l11
              i32.const 2
              i32.shl
              i32.add
              i32.store offset=100
              i32.const 2
              local.get $l2
              i32.const 2
              i32.and
              local.tee $l5
              i32.const 1
              i32.shr_u
              local.get $l2
              i32.const 128
              i32.and
              local.tee $l6
              select
              local.set $l14
              local.get $l2
              i32.const 1
              i32.and
              local.set $l8
              local.get $l2
              i32.const 2
              i32.shr_u
              i32.const 1
              i32.and
              local.set $l2
              i32.const 32
              i32.const 64
              i32.const 16
              local.get $l5
              select
              local.get $l6
              select
              local.set $l9
            end
            local.get $l7
            local.get $l8
            i32.store offset=140
            local.get $l7
            local.get $l14
            i32.store offset=128
            local.get $l7
            local.get $l2
            i32.store offset=132
            local.get $l7
            local.get $l9
            i32.store offset=124
            local.get $l7
            i32.const 48
            i32.store offset=120
            local.get $l7
            local.get $l11
            i32.store offset=108
            local.get $l7
            local.get $l4
            i32.store offset=104
            block $B6
              local.get $l2
              br_if $B6
              i32.const 0
              local.set $l2
              i32.const 0
              local.set $l3
              i32.const 0
              local.set $l25
              local.get $l4
              i32.eqz
              br_if $B6
              loop $L7
                local.get $l7
                i32.load offset=92
                local.set $l5
                local.get $l25
                if $I8
                  local.get $l5
                  i32.load8_u offset=41
                  local.tee $l11
                  local.get $l3
                  i32.gt_u
                  if $I9
                    local.get $l7
                    local.get $l7
                    i32.load offset=96
                    local.get $l11
                    local.get $l3
                    i32.sub
                    local.get $l9
                    i32.mul
                    i32.add
                    i32.store offset=96
                  end
                  local.get $l7
                  local.get $l5
                  i32.const 48
                  i32.add
                  local.tee $l5
                  i32.store offset=92
                end
                local.get $l7
                local.get $l25
                i32.const 1
                i32.add
                local.tee $l25
                i32.store offset=116
                block $B10
                  local.get $l5
                  i32.load8_u offset=41
                  i32.eqz
                  if $I11
                    i32.const 0
                    local.set $l3
                    br $B10
                  end
                  local.get $l2
                  i32.const 255
                  i32.and
                  i32.eqz
                  local.set $l2
                  i32.const 0
                  local.set $l3
                  loop $L12 (result i32)
                    local.get $l2
                    i32.const 1
                    i32.and
                    i32.eqz
                    if $I13
                      local.get $l7
                      local.get $l7
                      i32.load offset=96
                      local.get $l9
                      i32.add
                      i32.store offset=96
                      local.get $l7
                      local.get $l7
                      i32.load offset=100
                      i32.const 4
                      i32.add
                      i32.store offset=100
                    end
                    local.get $l7
                    i32.const 1
                    i32.store8 offset=136
                    local.get $l7
                    local.get $l3
                    i32.const 1
                    i32.add
                    local.tee $l3
                    i32.store offset=112
                    local.get $l18
                    local.get $l22
                    i32.const 6
                    i32.shl
                    i32.add
                    local.tee $l2
                    local.get $l5
                    f32.load offset=32
                    f32.store offset=72
                    local.get $l2
                    local.get $l5
                    f32.load offset=36
                    f32.store offset=60
                    local.get $l2
                    local.get $l5
                    f32.load offset=28
                    f32.store offset=76
                    local.get $l2
                    local.get $l8
                    if $I14 (result i32)
                      local.get $l7
                      i32.load offset=100
                      i32.load
                    else
                      i32.const -1
                    end
                    i32.store offset=68
                    local.get $l2
                    i32.const -64
                    i32.sub
                    local.get $l5
                    i32.load8_u offset=42
                    i32.store8
                    local.get $l22
                    i32.const 1
                    i32.add
                    local.set $l1
                    local.get $l2
                    block $B15 (result f32)
                      local.get $l14
                      if $I16
                        local.get $l7
                        i32.load offset=96
                        local.tee $l11
                        i32.const 16
                        i32.add
                        local.set $l6
                        local.get $l11
                        f32.load offset=28
                        br $B15
                      end
                      local.get $l7
                      i32.load offset=96
                      local.set $l11
                      local.get $l7
                      i32.const 80
                      i32.add
                      local.set $l6
                      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                    end
                    f32.store offset=44
                    local.get $l2
                    local.get $l6
                    f32.load
                    f32.store offset=48
                    local.get $l2
                    local.get $l6
                    f32.load offset=4
                    f32.store offset=52
                    local.get $l2
                    local.get $l6
                    f32.load offset=8
                    f32.store offset=56
                    local.get $l2
                    local.get $l5
                    f32.load offset=16
                    f32.store offset=16
                    local.get $l2
                    local.get $l5
                    f32.load offset=20
                    f32.store offset=20
                    local.get $l2
                    local.get $l5
                    f32.load offset=24
                    f32.store offset=24
                    local.get $l2
                    local.get $l11
                    f32.load
                    f32.store offset=32
                    local.get $l2
                    local.get $l11
                    f32.load offset=4
                    f32.store offset=36
                    local.get $l2
                    local.get $l11
                    f32.load offset=8
                    f32.store offset=40
                    local.get $l2
                    local.get $l11
                    f32.load offset=12
                    f32.store offset=28
                    local.get $l7
                    i32.const 1296
                    i32.add
                    local.get $l22
                    i32.const 2
                    i32.shl
                    i32.add
                    local.tee $l2
                    local.get $l5
                    i32.load16_u offset=44
                    i32.store16
                    local.get $l2
                    local.get $l5
                    i32.load16_u offset=46
                    i32.store16 offset=2
                    local.get $l5
                    i32.load8_u offset=41
                    local.get $l3
                    i32.le_u
                    if $I17 (result i32)
                      i32.const 1
                      local.set $l2
                      local.get $l1
                    else
                      i32.const 0
                      local.set $l2
                      local.get $l1
                      local.set $l22
                      br $L12
                    end
                  end
                  local.set $l22
                end
                local.get $l4
                local.get $l25
                i32.gt_u
                br_if $L7
              end
              local.get $l27
              i32.load16_u offset=4
              local.set $l1
            end
            local.get $l16
            i32.const 1
            i32.add
            local.tee $l16
            local.get $l1
            i32.const 65535
            i32.and
            i32.lt_u
            br_if $L4
          end
        end
        local.get $l7
        local.get $l22
        i32.store offset=1288
        local.get $l7
        i32.const 0
        i32.store offset=1276
        local.get $l7
        i32.const 0
        i32.store offset=248
        local.get $l7
        local.get $l18
        i32.const 16
        i32.add
        local.tee $l25
        i32.store offset=1280
        local.get $l7
        local.get $l7
        i32.const 1296
        i32.add
        i32.store offset=1284
        i32.const 0
        local.set $l11
        i32.const 0
        local.set $l31
        global.get $g0
        i32.const 128
        i32.sub
        local.tee $l10
        global.set $g0
        local.get $l7
        i32.const 80
        i32.add
        local.tee $l15
        local.get $l15
        i32.load offset=1200
        local.tee $l19
        f32.load
        f32.store offset=172
        local.get $l15
        local.get $l19
        f32.load offset=4
        f32.store offset=176
        local.get $l15
        local.get $l19
        f32.load offset=8
        f32.store offset=180
        local.get $l15
        i32.const 0
        i32.store offset=184
        local.get $l15
        i32.const 0
        i32.store16 offset=192
        local.get $l15
        i32.const 0
        i32.store16 offset=196
        local.get $l15
        local.get $l19
        f32.load offset=12
        f32.store offset=188
        local.get $l15
        i32.const 0
        i32.store16 offset=198
        i32.const 1
        local.set $l20
        block $B18
          local.get $l15
          i32.load offset=1208
          local.tee $l30
          i32.const 2
          i32.lt_u
          if $I19
            i32.const 1
            local.set $l12
            i32.const 1
            local.set $l5
            br $B18
          end
          i32.const 1
          local.set $l5
          i32.const 1
          local.set $l12
          loop $L20
            i32.const -1
            local.set $l1
            block $B21
              local.get $l5
              i32.const 65535
              i32.and
              local.tee $l14
              i32.eqz
              br_if $B21
              local.get $l19
              local.get $l20
              i32.const 6
              i32.shl
              i32.add
              local.tee $l2
              i32.const 8
              i32.add
              local.set $l13
              local.get $l2
              i32.const 4
              i32.add
              local.set $l17
              local.get $l15
              i32.load offset=1204
              local.tee $l4
              local.get $l20
              i32.const 2
              i32.shl
              i32.add
              local.tee $l1
              i32.const 2
              i32.add
              local.set $l6
              local.get $l1
              i32.load16_u
              local.set $l9
              local.get $l14
              local.set $l1
              loop $L22
                block $B23
                  local.get $l4
                  local.get $l15
                  local.get $l1
                  i32.const 1
                  i32.sub
                  local.tee $l1
                  i32.const 28
                  i32.mul
                  i32.add
                  local.tee $l8
                  i32.load16_u offset=192
                  i32.const 2
                  i32.shl
                  i32.add
                  local.tee $l3
                  i32.load16_u
                  local.get $l9
                  i32.const 65535
                  i32.and
                  i32.ne
                  br_if $B23
                  local.get $l3
                  i32.load16_u offset=2
                  local.get $l6
                  i32.load16_u
                  i32.ne
                  br_if $B23
                  local.get $l8
                  f32.load offset=172
                  local.get $l2
                  f32.load
                  f32.mul
                  local.get $l8
                  f32.load offset=176
                  local.get $l17
                  f32.load
                  f32.mul
                  f32.add
                  local.get $l8
                  f32.load offset=180
                  local.get $l13
                  f32.load
                  f32.mul
                  f32.add
                  f32.const 0x1.fd70a4p-1 (;=0.995;)
                  f32.ge
                  br_if $B21
                end
                local.get $l1
                br_if $L22
              end
              i32.const -1
              local.set $l1
            end
            local.get $l14
            i32.const 1
            i32.sub
            local.tee $l8
            local.get $l1
            i32.ne
            if $I24
              local.get $l15
              local.get $l8
              i32.const 28
              i32.mul
              i32.add
              local.tee $l8
              local.get $l12
              local.get $l8
              i32.load16_u offset=192
              i32.sub
              i32.store16 offset=194
              local.get $l5
              i32.const 65535
              i32.and
              i32.const 32
              i32.eq
              if $I25
                i32.const 32
                local.set $l5
                br $B18
              end
              local.get $l15
              local.get $l14
              i32.const 28
              i32.mul
              local.tee $l6
              i32.add
              local.tee $l8
              i32.const 0
              i32.store offset=184
              local.get $l8
              local.get $l12
              i32.store16 offset=192
              local.get $l8
              i32.const 172
              i32.add
              local.set $l3
              block $B26
                local.get $l1
                i32.const -1
                i32.eq
                if $I27
                  local.get $l8
                  local.get $l5
                  i32.store16 offset=196
                  local.get $l3
                  local.get $l15
                  i32.load offset=1200
                  local.tee $l19
                  local.get $l20
                  i32.const 6
                  i32.shl
                  i32.add
                  local.tee $l1
                  f32.load
                  f32.store
                  local.get $l8
                  local.get $l1
                  f32.load offset=4
                  f32.store offset=176
                  local.get $l8
                  local.get $l1
                  f32.load offset=8
                  f32.store offset=180
                  local.get $l8
                  local.get $l1
                  f32.load offset=12
                  f32.store offset=188
                  br $B26
                end
                local.get $l15
                i32.const 172
                i32.add
                local.tee $l4
                local.get $l1
                i32.const 28
                i32.mul
                i32.add
                local.tee $l1
                local.get $l3
                i32.store offset=12
                local.get $l1
                i32.load16_u offset=24
                local.set $l9
                local.get $l3
                local.get $l1
                f32.load
                f32.store
                local.get $l4
                local.get $l6
                i32.add
                local.tee $l3
                local.get $l1
                f32.load offset=4
                f32.store offset=4
                local.get $l3
                local.get $l1
                f32.load offset=8
                f32.store offset=8
                local.get $l3
                local.get $l4
                local.get $l9
                i32.const 28
                i32.mul
                i32.add
                local.tee $l1
                f32.load offset=16
                local.tee $l46
                local.get $l15
                i32.load offset=1200
                local.tee $l19
                local.get $l20
                i32.const 6
                i32.shl
                i32.add
                f32.load offset=12
                local.tee $l48
                local.get $l46
                local.get $l48
                f32.lt
                select
                local.tee $l46
                f32.store offset=16
                local.get $l1
                local.get $l46
                f32.store offset=16
                local.get $l3
                local.get $l9
                i32.store16 offset=24
              end
              local.get $l8
              local.get $l5
              i32.store16 offset=198
              local.get $l15
              i32.load offset=1208
              local.set $l30
              local.get $l5
              i32.const 1
              i32.add
              local.set $l5
            end
            local.get $l30
            local.get $l12
            i32.const 1
            i32.add
            local.tee $l12
            i32.const 65535
            i32.and
            local.tee $l20
            i32.gt_u
            br_if $L20
          end
        end
        local.get $l5
        i32.const 65535
        i32.and
        local.tee $l24
        i32.const 28
        i32.mul
        local.get $l15
        i32.add
        local.tee $l1
        local.get $l12
        local.get $l1
        i32.load16_u offset=164
        i32.sub
        i32.store16 offset=166
        block $B28
          local.get $l24
          i32.eqz
          br_if $B28
          local.get $l24
          i32.const 3
          i32.and
          local.set $l4
          i32.const 0
          local.set $l1
          local.get $l24
          i32.const 1
          i32.sub
          i32.const 3
          i32.ge_u
          if $I29
            local.get $l24
            i32.const 65532
            i32.and
            local.set $l9
            local.get $l15
            i32.const 172
            i32.add
            local.set $l8
            local.get $l15
            i32.const 1068
            i32.add
            local.set $l3
            loop $L30
              local.get $l3
              local.get $l1
              i32.const 2
              i32.shl
              i32.add
              local.get $l8
              local.get $l1
              i32.const 28
              i32.mul
              i32.add
              i32.store
              local.get $l3
              local.get $l1
              i32.const 1
              i32.or
              local.tee $l6
              i32.const 2
              i32.shl
              i32.add
              local.get $l8
              local.get $l6
              i32.const 28
              i32.mul
              i32.add
              i32.store
              local.get $l3
              local.get $l1
              i32.const 2
              i32.or
              local.tee $l6
              i32.const 2
              i32.shl
              i32.add
              local.get $l8
              local.get $l6
              i32.const 28
              i32.mul
              i32.add
              i32.store
              local.get $l3
              local.get $l1
              i32.const 3
              i32.or
              local.tee $l6
              i32.const 2
              i32.shl
              i32.add
              local.get $l8
              local.get $l6
              i32.const 28
              i32.mul
              i32.add
              i32.store
              local.get $l1
              i32.const 4
              i32.add
              local.set $l1
              local.get $l9
              i32.const 4
              i32.sub
              local.tee $l9
              br_if $L30
            end
          end
          local.get $l4
          i32.eqz
          br_if $B28
          loop $L31
            local.get $l15
            local.get $l1
            i32.const 2
            i32.shl
            i32.add
            i32.const 1068
            i32.add
            local.get $l15
            local.get $l1
            i32.const 28
            i32.mul
            i32.add
            i32.const 172
            i32.add
            i32.store
            local.get $l1
            i32.const 1
            i32.add
            local.set $l1
            local.get $l4
            i32.const 1
            i32.sub
            local.tee $l4
            br_if $L31
          end
        end
        local.get $l15
        i32.const 1068
        i32.add
        local.set $l17
        i32.const 0
        local.set $l3
        i32.const 0
        local.set $l6
        i32.const 0
        local.set $l20
        i32.const 32
        local.set $l19
        global.get $g0
        i32.const 16
        i32.sub
        local.tee $l4
        global.set $g0
        local.get $l4
        local.tee $l5
        i32.const 0
        i32.store8 offset=12
        local.get $l5
        i32.const 128
        i32.sub
        local.tee $l16
        global.set $g0
        local.get $l5
        local.get $l16
        i32.store offset=8
        block $B32
          local.get $l24
          i32.const 1
          i32.sub
          local.tee $l12
          i32.const 0
          i32.le_s
          br_if $B32
          loop $L33
            block $B34
              local.get $l3
              local.get $l12
              i32.ge_s
              br_if $B34
              loop $L35
                local.get $l12
                local.get $l3
                i32.sub
                i32.const 4
                i32.le_u
                if $I36
                  loop $L37
                    local.get $l3
                    local.tee $l9
                    i32.const 1
                    i32.add
                    local.tee $l3
                    local.set $l1
                    local.get $l9
                    local.set $l4
                    loop $L38
                      local.get $l1
                      local.get $l4
                      local.get $l17
                      local.get $l1
                      i32.const 2
                      i32.shl
                      i32.add
                      i32.load
                      f32.load offset=16
                      local.get $l17
                      local.get $l4
                      i32.const 2
                      i32.shl
                      i32.add
                      i32.load
                      f32.load offset=16
                      f32.lt
                      select
                      local.set $l4
                      local.get $l1
                      local.get $l12
                      i32.lt_s
                      local.set $l14
                      local.get $l1
                      i32.const 1
                      i32.add
                      local.set $l1
                      local.get $l14
                      br_if $L38
                    end
                    local.get $l4
                    local.get $l9
                    i32.ne
                    if $I39
                      local.get $l17
                      local.get $l4
                      i32.const 2
                      i32.shl
                      i32.add
                      local.tee $l1
                      i32.load
                      local.set $l4
                      local.get $l1
                      local.get $l17
                      local.get $l9
                      i32.const 2
                      i32.shl
                      i32.add
                      local.tee $l14
                      i32.load
                      i32.store
                      local.get $l14
                      local.get $l4
                      i32.store
                    end
                    local.get $l3
                    local.get $l12
                    i32.ne
                    br_if $L37
                    br $B34
                  end
                  unreachable
                end
                block $B40
                  local.get $l17
                  local.get $l3
                  i32.const 2
                  i32.shl
                  i32.add
                  local.tee $l14
                  i32.load
                  local.tee $l9
                  f32.load offset=16
                  local.tee $l46
                  local.get $l17
                  local.get $l3
                  local.get $l12
                  i32.add
                  i32.const 2
                  i32.div_s
                  i32.const 2
                  i32.shl
                  i32.add
                  local.tee $l1
                  i32.load
                  local.tee $l13
                  f32.load offset=16
                  f32.gt
                  i32.eqz
                  if $I41
                    local.get $l9
                    local.set $l4
                    br $B40
                  end
                  local.get $l14
                  local.get $l13
                  i32.store
                  local.get $l1
                  local.get $l9
                  i32.store
                  local.get $l14
                  i32.load
                  local.tee $l4
                  f32.load offset=16
                  local.set $l46
                  local.get $l9
                  local.set $l13
                end
                block $B42
                  local.get $l46
                  local.get $l17
                  local.get $l12
                  i32.const 2
                  i32.shl
                  i32.add
                  local.tee $l9
                  i32.load
                  local.tee $l2
                  f32.load offset=16
                  local.tee $l46
                  f32.gt
                  i32.eqz
                  if $I43
                    local.get $l2
                    local.set $l4
                    br $B42
                  end
                  local.get $l14
                  local.get $l2
                  i32.store
                  local.get $l9
                  local.get $l4
                  i32.store
                  local.get $l4
                  f32.load offset=16
                  local.set $l46
                  local.get $l1
                  i32.load
                  local.set $l13
                end
                local.get $l13
                f32.load offset=16
                local.get $l46
                f32.gt
                if $I44
                  local.get $l1
                  local.get $l4
                  i32.store
                  local.get $l9
                  local.get $l13
                  i32.store
                  local.get $l1
                  i32.load
                  local.set $l13
                end
                local.get $l1
                local.get $l17
                local.get $l12
                i32.const 1
                i32.sub
                local.tee $l4
                i32.const 2
                i32.shl
                i32.add
                local.tee $l21
                i32.load
                i32.store
                local.get $l21
                local.get $l13
                i32.store
                local.get $l3
                local.set $l1
                loop $L45
                  local.get $l13
                  f32.load offset=16
                  local.set $l46
                  loop $L46
                    local.get $l17
                    local.get $l1
                    local.tee $l8
                    i32.const 1
                    i32.add
                    local.tee $l1
                    i32.const 2
                    i32.shl
                    i32.add
                    local.tee $l14
                    i32.load
                    local.tee $l9
                    f32.load offset=16
                    local.get $l46
                    f32.lt
                    br_if $L46
                  end
                  loop $L47
                    local.get $l46
                    local.get $l17
                    local.get $l4
                    i32.const 1
                    i32.sub
                    local.tee $l4
                    i32.const 2
                    i32.shl
                    i32.add
                    local.tee $l2
                    i32.load
                    local.tee $l23
                    f32.load offset=16
                    f32.lt
                    br_if $L47
                  end
                  local.get $l1
                  local.get $l4
                  i32.lt_s
                  if $I48
                    local.get $l14
                    local.get $l23
                    i32.store
                    local.get $l2
                    local.get $l9
                    i32.store
                    local.get $l21
                    i32.load
                    local.set $l13
                    br $L45
                  end
                end
                local.get $l14
                local.get $l13
                i32.store
                local.get $l21
                local.get $l9
                i32.store
                block $B49
                  local.get $l1
                  local.get $l3
                  i32.sub
                  local.get $l12
                  local.get $l1
                  i32.sub
                  i32.lt_s
                  if $I50
                    block $B51
                      local.get $l19
                      i32.const 1
                      i32.sub
                      local.get $l6
                      i32.gt_u
                      if $I52
                        local.get $l16
                        local.set $l1
                        br $B51
                      end
                      local.get $l19
                      i32.const 3
                      i32.shl
                      local.tee $l1
                      if $I53 (result i32)
                        call $f69753
                        local.tee $l4
                        local.get $l1
                        i32.const 3151812
                        i32.const 3150980
                        i32.const 4700888
                        i32.load
                        local.tee $l14
                        local.get $l14
                        i32.load
                        i32.load offset=20
                        call_indirect $__indirect_function_table (type $t5)
                        select
                        i32.const 3151117
                        i32.const 155
                        local.get $l4
                        i32.load
                        i32.load offset=8
                        call_indirect $__indirect_function_table (type $t9)
                      else
                        i32.const 0
                      end
                      local.tee $l1
                      local.get $l16
                      local.get $l6
                      i32.const 2
                      i32.shl
                      call $f483
                      local.set $l4
                      block $B54
                        local.get $l16
                        i32.eqz
                        br_if $B54
                        local.get $l20
                        i32.eqz
                        br_if $B54
                        call $f69753
                        local.tee $l14
                        local.get $l16
                        local.get $l14
                        i32.load
                        i32.load offset=12
                        call_indirect $__indirect_function_table (type $t1)
                      end
                      local.get $l19
                      i32.const 1
                      i32.shl
                      local.set $l19
                      i32.const 1
                      local.set $l20
                      local.get $l4
                      local.set $l16
                    end
                    local.get $l1
                    local.get $l6
                    i32.const 2
                    i32.shl
                    i32.add
                    local.tee $l1
                    local.get $l3
                    i32.store
                    local.get $l1
                    local.get $l8
                    i32.store offset=4
                    local.get $l8
                    i32.const 2
                    i32.add
                    local.set $l3
                    br $B49
                  end
                  local.get $l8
                  i32.const 2
                  i32.add
                  local.set $l4
                  block $B55
                    local.get $l19
                    i32.const 1
                    i32.sub
                    local.get $l6
                    i32.gt_u
                    if $I56
                      local.get $l16
                      local.set $l1
                      br $B55
                    end
                    local.get $l19
                    i32.const 3
                    i32.shl
                    local.tee $l1
                    if $I57 (result i32)
                      call $f69753
                      local.tee $l14
                      local.get $l1
                      i32.const 3151812
                      i32.const 3150980
                      i32.const 4700888
                      i32.load
                      local.tee $l9
                      local.get $l9
                      i32.load
                      i32.load offset=20
                      call_indirect $__indirect_function_table (type $t5)
                      select
                      i32.const 3151117
                      i32.const 155
                      local.get $l14
                      i32.load
                      i32.load offset=8
                      call_indirect $__indirect_function_table (type $t9)
                    else
                      i32.const 0
                    end
                    local.tee $l1
                    local.get $l16
                    local.get $l6
                    i32.const 2
                    i32.shl
                    call $f483
                    local.set $l14
                    block $B58
                      local.get $l16
                      i32.eqz
                      br_if $B58
                      local.get $l20
                      i32.eqz
                      br_if $B58
                      call $f69753
                      local.tee $l9
                      local.get $l16
                      local.get $l9
                      i32.load
                      i32.load offset=12
                      call_indirect $__indirect_function_table (type $t1)
                    end
                    local.get $l19
                    i32.const 1
                    i32.shl
                    local.set $l19
                    i32.const 1
                    local.set $l20
                    local.get $l14
                    local.set $l16
                  end
                  local.get $l1
                  local.get $l6
                  i32.const 2
                  i32.shl
                  i32.add
                  local.tee $l1
                  local.get $l4
                  i32.store
                  local.get $l1
                  local.get $l12
                  i32.store offset=4
                  local.get $l8
                  local.set $l12
                end
                local.get $l6
                i32.const 2
                i32.add
                local.set $l6
                local.get $l3
                local.get $l12
                i32.lt_s
                br_if $L35
              end
            end
            local.get $l6
            if $I59
              local.get $l16
              local.get $l6
              i32.const 2
              i32.sub
              local.tee $l1
              i32.const 2
              i32.shl
              i32.add
              i32.load
              local.set $l3
              local.get $l6
              i32.const 2
              i32.shl
              local.get $l16
              i32.add
              i32.const 4
              i32.sub
              i32.load
              local.set $l12
              local.get $l1
              local.set $l6
              br $L33
            end
          end
          local.get $l16
          i32.eqz
          br_if $B32
          local.get $l20
          i32.eqz
          br_if $B32
          call $f69753
          local.tee $l17
          local.get $l16
          local.get $l17
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l5
        i32.load8_u offset=12
        if $I60
          local.get $l5
          i32.load offset=8
          call $f70044
        end
        local.get $l5
        i32.const 16
        i32.add
        global.set $g0
        block $B61
          local.get $l24
          i32.eqz
          br_if $B61
          local.get $l10
          i32.const 116
          i32.add
          local.set $l14
          local.get $l10
          i32.const 112
          i32.add
          local.set $l5
          local.get $l15
          i32.const 20
          i32.add
          local.set $l34
          local.get $l10
          i32.const 56
          i32.add
          local.set $l35
          local.get $l10
          i32.const 48
          i32.add
          local.set $l36
          local.get $l10
          i32.const 40
          i32.add
          local.set $l37
          local.get $l10
          i32.const 32
          i32.add
          local.set $l38
          loop $L62
            local.get $l11
            local.set $l16
            block $B63
              local.get $l15
              local.get $l31
              i32.const 2
              i32.shl
              i32.add
              i32.const 1068
              i32.add
              local.tee $l28
              i32.load
              local.tee $l4
              i32.load16_u offset=24
              local.get $l4
              i32.load16_u offset=26
              i32.ne
              br_if $B63
              i32.const 6
              local.set $l11
              local.get $l16
              i32.const 6
              i32.eq
              br_if $B61
              local.get $l16
              i32.const 1
              i32.add
              local.set $l11
              local.get $l15
              local.get $l16
              i32.const 28
              i32.mul
              i32.add
              local.set $l17
              i32.const 0
              local.set $l3
              local.get $l4
              local.set $l1
              loop $L64
                local.get $l3
                local.get $l1
                i32.load16_u offset=22
                i32.add
                local.set $l3
                local.get $l1
                i32.load offset=12
                local.tee $l1
                br_if $L64
              end
              f32.const 0x0p+0 (;=0;)
              local.set $l46
              i32.const 0
              local.set $l1
              local.get $l3
              i32.const 6
              i32.le_u
              if $I65
                loop $L66
                  i32.const 0
                  local.set $l8
                  local.get $l4
                  i32.load16_u offset=22
                  if $I67
                    loop $L68
                      local.get $l17
                      local.get $l1
                      i32.const 2
                      i32.shl
                      i32.add
                      local.get $l8
                      local.get $l4
                      i32.load16_u offset=20
                      i32.add
                      i32.store offset=4
                      local.get $l1
                      i32.const 1
                      i32.add
                      local.set $l1
                      local.get $l8
                      i32.const 1
                      i32.add
                      local.tee $l8
                      local.get $l4
                      i32.load16_u offset=22
                      i32.lt_u
                      br_if $L68
                    end
                  end
                  local.get $l4
                  i32.load offset=12
                  local.tee $l4
                  br_if $L66
                end
                local.get $l17
                local.get $l3
                i32.store
                br $B63
              end
              loop $L69
                local.get $l4
                i32.load16_u offset=22
                local.tee $l6
                if $I70
                  local.get $l4
                  i32.load16_u offset=20
                  local.set $l2
                  local.get $l15
                  i32.load offset=1200
                  local.set $l13
                  i32.const 0
                  local.set $l8
                  loop $L71
                    local.get $l13
                    local.get $l2
                    local.get $l8
                    i32.add
                    local.tee $l9
                    i32.const 6
                    i32.shl
                    i32.add
                    local.tee $l3
                    f32.load offset=16
                    local.tee $l48
                    local.get $l48
                    f32.mul
                    local.get $l3
                    f32.load offset=20
                    local.tee $l48
                    local.get $l48
                    f32.mul
                    f32.add
                    local.get $l3
                    f32.load offset=24
                    local.tee $l48
                    local.get $l48
                    f32.mul
                    f32.add
                    local.tee $l48
                    local.get $l46
                    local.get $l46
                    local.get $l48
                    f32.lt
                    local.tee $l3
                    select
                    local.set $l46
                    local.get $l9
                    local.get $l1
                    local.get $l3
                    select
                    local.set $l1
                    local.get $l8
                    i32.const 1
                    i32.add
                    local.tee $l8
                    local.get $l6
                    i32.ne
                    br_if $L71
                  end
                end
                local.get $l4
                i32.load offset=12
                local.tee $l4
                br_if $L69
              end
              local.get $l17
              local.get $l1
              i32.store offset=4
              local.get $l15
              i32.load offset=1200
              local.tee $l8
              local.get $l1
              i32.const 6
              i32.shl
              i32.add
              local.tee $l21
              f32.load offset=16
              local.set $l48
              local.get $l21
              i32.const 24
              i32.add
              local.tee $l20
              f32.load
              local.set $l50
              local.get $l21
              i32.const 20
              i32.add
              local.tee $l30
              f32.load
              local.set $l49
              f32.const 0x0p+0 (;=0;)
              local.set $l46
              local.get $l28
              i32.load
              local.tee $l13
              if $I72
                loop $L73
                  local.get $l13
                  i32.load16_u offset=22
                  local.tee $l6
                  if $I74
                    local.get $l13
                    i32.load16_u offset=20
                    local.set $l2
                    i32.const 0
                    local.set $l3
                    loop $L75
                      local.get $l48
                      local.get $l8
                      local.get $l2
                      local.get $l3
                      i32.add
                      local.tee $l9
                      i32.const 6
                      i32.shl
                      i32.add
                      local.tee $l4
                      f32.load offset=16
                      f32.sub
                      local.tee $l47
                      local.get $l47
                      f32.mul
                      local.get $l49
                      local.get $l4
                      f32.load offset=20
                      f32.sub
                      local.tee $l47
                      local.get $l47
                      f32.mul
                      f32.add
                      local.get $l50
                      local.get $l4
                      f32.load offset=24
                      f32.sub
                      local.tee $l47
                      local.get $l47
                      f32.mul
                      f32.add
                      local.tee $l47
                      local.get $l46
                      local.get $l46
                      local.get $l47
                      f32.lt
                      local.tee $l4
                      select
                      local.set $l46
                      local.get $l9
                      local.get $l1
                      local.get $l4
                      select
                      local.set $l1
                      local.get $l3
                      i32.const 1
                      i32.add
                      local.tee $l3
                      local.get $l6
                      i32.ne
                      br_if $L75
                    end
                  end
                  local.get $l13
                  i32.load offset=12
                  local.tee $l13
                  br_if $L73
                end
              end
              local.get $l21
              i32.const 16
              i32.add
              local.set $l19
              local.get $l17
              local.get $l1
              i32.store offset=8
              local.get $l48
              local.get $l8
              local.get $l1
              i32.const 6
              i32.shl
              i32.add
              local.tee $l23
              f32.load offset=16
              f32.sub
              local.tee $l46
              local.get $l28
              i32.load
              local.tee $l13
              f32.load offset=4
              local.tee $l47
              f32.mul
              local.get $l49
              local.get $l23
              i32.const 20
              i32.add
              local.tee $l39
              f32.load
              f32.sub
              local.tee $l52
              local.get $l13
              f32.load
              local.tee $l51
              f32.mul
              f32.sub
              local.set $l53
              local.get $l50
              local.get $l23
              i32.const 24
              i32.add
              local.tee $l40
              f32.load
              f32.sub
              local.tee $l54
              local.get $l51
              f32.mul
              local.get $l46
              local.get $l13
              f32.load offset=8
              local.tee $l55
              f32.mul
              f32.sub
              local.set $l51
              local.get $l52
              local.get $l55
              f32.mul
              local.get $l54
              local.get $l47
              f32.mul
              f32.sub
              local.set $l52
              f32.const 0x0p+0 (;=0;)
              local.set $l46
              loop $L76
                local.get $l13
                i32.load16_u offset=22
                local.tee $l6
                if $I77
                  local.get $l13
                  i32.load16_u offset=20
                  local.set $l2
                  i32.const 0
                  local.set $l3
                  loop $L78
                    local.get $l52
                    local.get $l8
                    local.get $l2
                    local.get $l3
                    i32.add
                    local.tee $l9
                    i32.const 6
                    i32.shl
                    i32.add
                    local.tee $l4
                    f32.load offset=16
                    local.get $l48
                    f32.sub
                    f32.mul
                    local.get $l51
                    local.get $l4
                    f32.load offset=20
                    local.get $l49
                    f32.sub
                    f32.mul
                    f32.add
                    local.get $l53
                    local.get $l4
                    f32.load offset=24
                    local.get $l50
                    f32.sub
                    f32.mul
                    f32.add
                    local.tee $l47
                    local.get $l46
                    local.get $l46
                    local.get $l47
                    f32.lt
                    local.tee $l4
                    select
                    local.set $l46
                    local.get $l9
                    local.get $l1
                    local.get $l4
                    select
                    local.set $l1
                    local.get $l3
                    i32.const 1
                    i32.add
                    local.tee $l3
                    local.get $l6
                    i32.ne
                    br_if $L78
                  end
                end
                local.get $l13
                i32.load offset=12
                local.tee $l13
                br_if $L76
              end
              local.get $l17
              local.get $l1
              i32.store offset=12
              local.get $l1
              local.set $l9
              local.get $l28
              i32.load
              local.tee $l12
              if $I79
                local.get $l51
                f32.neg
                local.set $l51
                f32.const 0x0p+0 (;=0;)
                local.set $l46
                loop $L80
                  local.get $l12
                  i32.load16_u offset=22
                  local.tee $l2
                  if $I81
                    local.get $l12
                    i32.load16_u offset=20
                    local.set $l13
                    i32.const 0
                    local.set $l3
                    loop $L82
                      local.get $l8
                      local.get $l3
                      local.get $l13
                      i32.add
                      local.tee $l6
                      i32.const 6
                      i32.shl
                      i32.add
                      local.tee $l4
                      f32.load offset=20
                      local.get $l49
                      f32.sub
                      local.get $l51
                      f32.mul
                      local.get $l52
                      local.get $l4
                      f32.load offset=16
                      local.get $l48
                      f32.sub
                      f32.mul
                      f32.sub
                      local.get $l53
                      local.get $l4
                      f32.load offset=24
                      local.get $l50
                      f32.sub
                      f32.mul
                      f32.sub
                      local.tee $l47
                      local.get $l46
                      local.get $l46
                      local.get $l47
                      f32.lt
                      local.tee $l4
                      select
                      local.set $l46
                      local.get $l6
                      local.get $l9
                      local.get $l4
                      select
                      local.set $l9
                      local.get $l3
                      i32.const 1
                      i32.add
                      local.tee $l3
                      local.get $l2
                      i32.ne
                      br_if $L82
                    end
                  end
                  local.get $l12
                  i32.load offset=12
                  local.tee $l12
                  br_if $L80
                end
              end
              local.get $l23
              i32.const 16
              i32.add
              local.set $l41
              local.get $l17
              local.get $l9
              i32.store offset=16
              local.get $l10
              local.get $l15
              local.get $l16
              i32.const 7
              i32.mul
              i32.const 2
              i32.shl
              local.tee $l42
              i32.add
              local.tee $l3
              i64.load offset=12 align=4
              i64.store offset=72
              local.get $l10
              local.get $l3
              i32.const 4
              i32.add
              local.tee $l33
              i64.load align=4
              i64.store offset=64
              local.get $l10
              local.get $l21
              f32.load offset=12
              f32.const -0x1.0624dep-10 (;=-0.001;)
              f32.add
              f32.store offset=96
              local.get $l10
              local.get $l23
              f32.load offset=12
              f32.const -0x1.0624dep-10 (;=-0.001;)
              f32.add
              f32.store offset=100
              local.get $l10
              local.get $l8
              local.get $l1
              i32.const 6
              i32.shl
              i32.add
              local.tee $l1
              f32.load offset=12
              f32.const -0x1.0624dep-10 (;=-0.001;)
              f32.add
              f32.store offset=104
              local.get $l10
              local.get $l8
              local.get $l9
              i32.const 6
              i32.shl
              i32.add
              local.tee $l3
              f32.load offset=12
              f32.const -0x1.0624dep-10 (;=-0.001;)
              f32.add
              f32.store offset=108
              local.get $l28
              i32.load
              local.tee $l12
              if $I83
                local.get $l3
                i32.const 24
                i32.add
                local.set $l16
                local.get $l3
                i32.const 20
                i32.add
                local.set $l21
                local.get $l3
                i32.const 16
                i32.add
                local.set $l23
                local.get $l1
                i32.const 24
                i32.add
                local.set $l43
                local.get $l1
                i32.const 20
                i32.add
                local.set $l44
                local.get $l1
                i32.const 16
                i32.add
                local.set $l45
                loop $L84
                  local.get $l12
                  i32.load16_u offset=22
                  local.tee $l2
                  if $I85
                    local.get $l16
                    f32.load
                    local.set $l53
                    local.get $l21
                    f32.load
                    local.set $l52
                    local.get $l23
                    f32.load
                    local.set $l51
                    local.get $l43
                    f32.load
                    local.set $l54
                    local.get $l44
                    f32.load
                    local.set $l55
                    local.get $l45
                    f32.load
                    local.set $l56
                    local.get $l40
                    f32.load
                    local.set $l57
                    local.get $l39
                    f32.load
                    local.set $l58
                    local.get $l41
                    f32.load
                    local.set $l59
                    local.get $l20
                    f32.load
                    local.set $l60
                    local.get $l30
                    f32.load
                    local.set $l61
                    local.get $l19
                    f32.load
                    local.set $l62
                    local.get $l12
                    i32.load16_u offset=20
                    local.set $l13
                    i32.const 0
                    local.set $l3
                    loop $L86
                      i32.const 3
                      i32.const 2
                      local.get $l62
                      local.get $l8
                      local.get $l3
                      local.get $l13
                      i32.add
                      local.tee $l9
                      i32.const 6
                      i32.shl
                      i32.add
                      local.tee $l1
                      f32.load offset=16
                      local.tee $l46
                      f32.sub
                      local.tee $l48
                      local.get $l48
                      f32.mul
                      local.get $l61
                      local.get $l1
                      f32.load offset=20
                      local.tee $l48
                      f32.sub
                      local.tee $l50
                      local.get $l50
                      f32.mul
                      f32.add
                      local.get $l60
                      local.get $l1
                      f32.load offset=24
                      local.tee $l50
                      f32.sub
                      local.tee $l49
                      local.get $l49
                      f32.mul
                      f32.add
                      local.tee $l49
                      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                      local.get $l49
                      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                      f32.lt
                      select
                      local.tee $l49
                      local.get $l59
                      local.get $l46
                      f32.sub
                      local.tee $l47
                      local.get $l47
                      f32.mul
                      local.get $l58
                      local.get $l48
                      f32.sub
                      local.tee $l47
                      local.get $l47
                      f32.mul
                      f32.add
                      local.get $l57
                      local.get $l50
                      f32.sub
                      local.tee $l47
                      local.get $l47
                      f32.mul
                      f32.add
                      local.tee $l47
                      f32.gt
                      local.tee $l4
                      local.get $l47
                      local.get $l49
                      local.get $l4
                      select
                      local.tee $l49
                      local.get $l56
                      local.get $l46
                      f32.sub
                      local.tee $l47
                      local.get $l47
                      f32.mul
                      local.get $l55
                      local.get $l48
                      f32.sub
                      local.tee $l47
                      local.get $l47
                      f32.mul
                      f32.add
                      local.get $l54
                      local.get $l50
                      f32.sub
                      local.tee $l47
                      local.get $l47
                      f32.mul
                      f32.add
                      local.tee $l47
                      f32.gt
                      local.tee $l4
                      select
                      local.get $l51
                      local.get $l46
                      f32.sub
                      local.tee $l46
                      local.get $l46
                      f32.mul
                      local.get $l52
                      local.get $l48
                      f32.sub
                      local.tee $l46
                      local.get $l46
                      f32.mul
                      f32.add
                      local.get $l53
                      local.get $l50
                      f32.sub
                      local.tee $l46
                      local.get $l46
                      f32.mul
                      f32.add
                      local.get $l47
                      local.get $l49
                      local.get $l4
                      select
                      f32.lt
                      select
                      i32.const 2
                      i32.shl
                      local.tee $l4
                      local.get $l10
                      i32.const 96
                      i32.add
                      i32.or
                      local.tee $l6
                      f32.load
                      local.get $l1
                      f32.load offset=12
                      local.tee $l46
                      f32.gt
                      if $I87
                        local.get $l10
                        i32.const -64
                        i32.sub
                        local.get $l4
                        i32.or
                        local.get $l9
                        i32.store
                        local.get $l6
                        local.get $l46
                        f32.store
                      end
                      local.get $l3
                      i32.const 1
                      i32.add
                      local.tee $l3
                      local.get $l2
                      i32.ne
                      br_if $L86
                    end
                  end
                  local.get $l12
                  i32.load offset=12
                  local.tee $l12
                  br_if $L84
                end
              end
              local.get $l35
              i64.const 0
              i64.store
              local.get $l36
              i64.const 0
              i64.store
              local.get $l37
              i64.const 0
              i64.store
              local.get $l38
              i64.const 0
              i64.store
              local.get $l10
              i64.const 0
              i64.store offset=24
              local.get $l10
              i64.const 0
              i64.store offset=16
              local.get $l10
              i64.const 0
              i64.store offset=8
              local.get $l10
              i64.const 0
              i64.store
              local.get $l33
              local.get $l10
              i64.load offset=72
              i64.store offset=8 align=4
              local.get $l33
              local.get $l10
              i64.load offset=64
              i64.store align=4
              local.get $l10
              local.get $l10
              i32.load offset=64
              i32.add
              i32.const 1
              i32.store8
              local.get $l10
              local.get $l10
              i32.load offset=68
              i32.add
              i32.const 1
              i32.store8
              local.get $l10
              local.get $l10
              i32.load offset=72
              i32.add
              i32.const 1
              i32.store8
              local.get $l10
              local.get $l10
              i32.load offset=76
              i32.add
              i32.const 1
              i32.store8
              local.get $l10
              i64.const 0
              i64.store offset=80
              local.get $l10
              i64.const 9187343237679939583
              i64.store offset=112
              local.get $l28
              i32.load
              local.tee $l12
              if $I88
                loop $L89
                  local.get $l12
                  i32.load16_u offset=22
                  local.tee $l4
                  if $I90
                    local.get $l12
                    i32.load16_u offset=20
                    local.set $l9
                    i32.const 0
                    local.set $l1
                    loop $L91
                      block $B92
                        local.get $l10
                        local.get $l1
                        local.get $l9
                        i32.add
                        local.tee $l3
                        i32.add
                        i32.load8_u
                        br_if $B92
                        block $B93 (result i32)
                          local.get $l8
                          local.get $l3
                          i32.const 6
                          i32.shl
                          i32.add
                          f32.load offset=12
                          local.tee $l46
                          local.get $l10
                          f32.load offset=112
                          local.tee $l48
                          f32.lt
                          if $I94
                            local.get $l10
                            i32.const 80
                            i32.add
                            local.set $l6
                            local.get $l10
                            i32.load offset=80
                            local.set $l2
                            local.get $l5
                            br $B93
                          end
                          local.get $l46
                          local.get $l10
                          f32.load offset=116
                          local.tee $l48
                          f32.lt
                          i32.eqz
                          br_if $B92
                          local.get $l10
                          i32.const 84
                          i32.add
                          local.set $l6
                          local.get $l10
                          i32.load offset=84
                          local.set $l2
                          local.get $l14
                        end
                        local.set $l13
                        local.get $l10
                        local.get $l2
                        i32.store offset=84
                        local.get $l10
                        local.get $l48
                        f32.store offset=116
                        local.get $l13
                        local.get $l46
                        f32.store
                        local.get $l6
                        local.get $l3
                        i32.store
                      end
                      local.get $l1
                      i32.const 1
                      i32.add
                      local.tee $l1
                      local.get $l4
                      i32.ne
                      br_if $L91
                    end
                  end
                  local.get $l12
                  i32.load offset=12
                  local.tee $l12
                  br_if $L89
                end
              end
              local.get $l34
              local.get $l42
              i32.add
              local.get $l10
              i64.load offset=80
              i64.store align=4
              local.get $l17
              i32.const 6
              i32.store
            end
            local.get $l31
            i32.const 1
            i32.add
            local.tee $l31
            local.get $l24
            i32.ne
            br_if $L62
          end
        end
        local.get $l15
        local.get $l11
        i32.store offset=168
        local.get $l10
        i32.const 128
        i32.add
        global.set $g0
        local.get $l7
        i64.const 0
        i64.store offset=72
        local.get $l7
        i32.const -64
        i32.sub
        i64.const 0
        i64.store
        local.get $l7
        i64.const 0
        i64.store offset=56
        local.get $l7
        i64.const 0
        i64.store offset=48
        local.get $l7
        i64.const 0
        i64.store offset=40
        local.get $l7
        i64.const 0
        i64.store offset=32
        local.get $l7
        i64.const 0
        i64.store offset=24
        local.get $l7
        i64.const 0
        i64.store offset=16
        block $B95
          block $B96 (result i32)
            local.get $l7
            i32.load offset=248
            local.tee $l9
            if $I97
              i32.const 0
              local.set $l14
              loop $L98
                local.get $l7
                i32.const 80
                i32.add
                local.get $l14
                i32.const 28
                i32.mul
                i32.add
                local.tee $l3
                i32.load
                local.tee $l8
                if $I99
                  local.get $l8
                  i32.const 3
                  i32.and
                  local.set $l6
                  i32.const 0
                  local.set $l2
                  local.get $l8
                  i32.const 1
                  i32.sub
                  i32.const 3
                  i32.ge_u
                  if $I100
                    local.get $l8
                    i32.const -4
                    i32.and
                    local.set $l1
                    loop $L101
                      local.get $l3
                      i32.const 4
                      i32.add
                      local.tee $l5
                      local.get $l2
                      i32.const 2
                      i32.shl
                      local.tee $l11
                      i32.add
                      i32.load
                      local.get $l7
                      i32.const 16
                      i32.add
                      i32.add
                      i32.const 1
                      i32.store8
                      local.get $l5
                      local.get $l11
                      i32.const 4
                      i32.or
                      i32.add
                      i32.load
                      local.get $l7
                      i32.const 16
                      i32.add
                      i32.add
                      i32.const 1
                      i32.store8
                      local.get $l5
                      local.get $l11
                      i32.const 8
                      i32.or
                      i32.add
                      i32.load
                      local.get $l7
                      i32.const 16
                      i32.add
                      i32.add
                      i32.const 1
                      i32.store8
                      local.get $l5
                      local.get $l11
                      i32.const 12
                      i32.or
                      i32.add
                      i32.load
                      local.get $l7
                      i32.const 16
                      i32.add
                      i32.add
                      i32.const 1
                      i32.store8
                      local.get $l2
                      i32.const 4
                      i32.add
                      local.set $l2
                      local.get $l1
                      i32.const 4
                      i32.sub
                      local.tee $l1
                      br_if $L101
                    end
                  end
                  local.get $l6
                  if $I102
                    loop $L103
                      local.get $l3
                      local.get $l2
                      i32.const 2
                      i32.shl
                      i32.add
                      i32.load offset=4
                      local.get $l7
                      i32.const 16
                      i32.add
                      i32.add
                      i32.const 1
                      i32.store8
                      local.get $l2
                      i32.const 1
                      i32.add
                      local.set $l2
                      local.get $l6
                      i32.const 1
                      i32.sub
                      local.tee $l6
                      br_if $L103
                    end
                  end
                  local.get $l8
                  local.get $l29
                  i32.add
                  local.set $l29
                end
                local.get $l14
                i32.const 1
                i32.add
                local.tee $l14
                local.get $l9
                i32.ne
                br_if $L98
              end
              local.get $l18
              i32.const 11852
              i32.add
              local.tee $l8
              local.get $l29
              i32.const 1
              i32.shl
              i32.const 15
              i32.add
              i32.const -16
              i32.and
              local.tee $l2
              i32.const 16385
              i32.lt_u
              br_if $B96
              drop
              local.get $l8
              i32.load
              local.get $l2
              call $f70598
              local.set $l3
              br $B95
            end
            i32.const 0
            local.set $l2
            local.get $l18
            i32.const 11852
            i32.add
          end
          local.set $l8
          local.get $p0
          i32.load offset=32
          local.set $l5
          block $B104
            local.get $l18
            i32.const 11856
            i32.add
            i32.load
            local.tee $l11
            if $I105
              local.get $l18
              i32.const 11860
              i32.add
              i32.load
              local.tee $l6
              local.get $l2
              i32.add
              local.tee $l3
              i32.const 16385
              i32.lt_u
              br_if $B104
            end
            local.get $l18
            i32.load offset=11852
            local.get $l5
            i32.const 11836
            i32.add
            call $f70606
            local.set $l3
            local.get $l18
            i32.const 11860
            i32.add
            local.get $l2
            i32.store
            local.get $l18
            local.get $l3
            i32.store offset=11856
            br $B95
          end
          local.get $l18
          local.get $l3
          i32.store offset=11860
          local.get $l6
          local.get $l11
          i32.add
          local.set $l3
        end
        local.get $l27
        local.get $l3
        i32.store offset=32
        i32.const 0
        local.set $l6
        local.get $l22
        if $I106
          local.get $l18
          i32.const 16
          i32.add
          local.set $l1
          i32.const 0
          local.set $l2
          loop $L107
            local.get $l7
            i32.const 16
            i32.add
            local.get $l2
            i32.add
            i32.load8_u
            if $I108
              local.get $l2
              local.get $l6
              i32.ne
              if $I109
                local.get $l1
                local.get $l6
                i32.const 6
                i32.shl
                i32.add
                local.tee $l5
                local.get $l1
                local.get $l2
                i32.const 6
                i32.shl
                i32.add
                local.tee $l11
                f32.load
                f32.store
                local.get $l5
                local.get $l11
                f32.load offset=4
                f32.store offset=4
                local.get $l5
                local.get $l11
                f32.load offset=8
                f32.store offset=8
                local.get $l5
                local.get $l11
                f32.load offset=12
                f32.store offset=12
                local.get $l5
                local.get $l11
                f32.load offset=16
                f32.store offset=16
                local.get $l5
                local.get $l11
                f32.load offset=20
                f32.store offset=20
                local.get $l5
                local.get $l11
                f32.load offset=24
                f32.store offset=24
                local.get $l5
                local.get $l11
                f32.load offset=28
                f32.store offset=28
                local.get $l5
                local.get $l11
                f32.load offset=32
                f32.store offset=32
                local.get $l5
                local.get $l11
                f32.load offset=36
                f32.store offset=36
                local.get $l5
                local.get $l11
                f32.load offset=40
                f32.store offset=40
                local.get $l5
                local.get $l11
                i64.load offset=44 align=4
                i64.store offset=44 align=4
                local.get $l5
                local.get $l11
                i64.load offset=52 align=4
                i64.store offset=52 align=4
                local.get $l5
                local.get $l11
                i32.load offset=60
                i32.store offset=60
                local.get $l7
                i32.const 1296
                i32.add
                local.get $l6
                i32.const 2
                i32.shl
                i32.add
                local.get $l7
                i32.const 1296
                i32.add
                local.get $l2
                i32.const 2
                i32.shl
                i32.add
                i32.load
                i32.store
              end
              local.get $l3
              local.get $l6
              i32.const 1
              i32.shl
              i32.add
              local.get $l2
              i32.store16
              local.get $l6
              i32.const 1
              i32.add
              local.set $l6
            end
            local.get $l2
            i32.const 1
            i32.add
            local.tee $l2
            local.get $l22
            i32.ne
            br_if $L107
          end
        end
        local.get $l25
        local.get $l6
        i32.const 0
        local.get $p0
        i32.load offset=108
        local.tee $l2
        i32.load offset=32
        local.get $l2
        local.get $l27
        i32.load offset=8
        i32.load offset=52
        local.tee $l5
        i32.const 7
        i32.and
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.get $l5
        i32.const 3
        i32.shr_u
        i32.add
        i32.const 4
        i32.shl
        i32.add
        local.tee $l2
        i32.const 12
        i32.add
        local.get $l2
        local.get $l2
        i32.const 4
        i32.add
        local.get $l7
        i32.const 14
        i32.add
        local.get $l2
        i32.const 8
        i32.add
        local.get $l6
        i32.const 2
        i32.shl
        local.get $p0
        i32.load offset=104
        i32.const 0
        i32.const 0
        local.get $l7
        i32.const 1296
        i32.add
        local.get $l2
        i32.const 13
        i32.add
        i32.const 0
        local.get $p0
        i32.load offset=32
        i32.const 11836
        i32.add
        local.get $l8
        i32.const 0
        i32.const 0
        i32.const 0
        i32.const 0
        i32.const 0
        call $f70597
        drop
        local.get $l7
        i32.const 1552
        i32.add
        global.set $g0
        local.get $l26
        i32.const 1
        i32.add
        local.tee $l26
        local.get $l32
        i32.ne
        br_if $L2
      end
    end
    local.get $p0
    i32.load offset=28
    i32.load offset=336
    local.get $l18
    call $f69737)