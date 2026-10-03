  (func $f69098 (type $t4) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32)
    (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i32) (local $l34 i32) (local $l35 i32) (local $l36 i32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32) (local $l64 f32) (local $l65 f32) (local $l66 f32) (local $l67 f32) (local $l68 f32) (local $l69 f32) (local $l70 f32) (local $l71 f32) (local $l72 f32) (local $l73 f32) (local $l74 f32) (local $l75 f32) (local $l76 f32) (local $l77 f32) (local $l78 f32) (local $l79 f32) (local $l80 f32) (local $l81 f32) (local $l82 f32) (local $l83 f32) (local $l84 f32) (local $l85 f32) (local $l86 f32) (local $l87 f32) (local $l88 f32) (local $l89 f32) (local $l90 f32) (local $l91 f32) (local $l92 f32) (local $l93 f32) (local $l94 f32) (local $l95 f32) (local $l96 f32) (local $l97 f32) (local $l98 f32) (local $l99 f32) (local $l100 f32) (local $l101 f32) (local $l102 f32) (local $l103 f32) (local $l104 f32) (local $l105 f32) (local $l106 f32) (local $l107 i64) (local $l108 i64) (local $l109 f64)
    global.get $g0
    i32.const 96
    i32.sub
    local.tee $l12
    global.set $g0
    local.get $p0
    i32.load offset=8
    local.tee $l23
    if $I0 (result f64)
      local.get $p0
      i32.load
      i32.load
      i32.load offset=20
      f64.load offset=40
    else
      f64.const 0x0p+0 (;=0;)
    end
    local.set $l109
    i32.const 7
    call $f80140
    f32.load offset=108
    local.set $l106
    local.get $l109
    f32.demote_f64
    local.set $l100
    local.get $p1
    if $I1
      local.get $p0
      i32.load offset=8
      if $I2
        local.get $p0
        i32.load
        local.set $l10
        loop $L3
          local.get $l10
          i32.load
          local.tee $l14
          i32.load offset=108
          local.set $p1
          local.get $l14
          call $f68200
          local.set $l14
          block $B4
            local.get $p1
            i32.eqz
            br_if $B4
            local.get $l14
            br_if $B4
            local.get $p1
            i32.load8_u offset=216
            i32.eqz
            if $I5
              local.get $p1
              call $f69053
            end
            local.get $p1
            i32.load offset=236
            i32.eqz
            br_if $B4
            local.get $p1
            i32.load offset=932
            local.tee $l14
            i32.eqz
            br_if $B4
            local.get $l14
            i32.load offset=192
            local.tee $l14
            i32.eqz
            br_if $B4
            local.get $l14
            local.get $p1
            f32.load offset=720
            f32.store
          end
          local.get $l10
          i32.const 4
          i32.add
          local.tee $l10
          local.get $p0
          i32.load
          local.get $p0
          i32.load offset=8
          i32.const 2
          i32.shl
          i32.add
          i32.ne
          br_if $L3
        end
      end
      local.get $l12
      i64.const 4294967296
      i64.store offset=88
      local.get $l12
      i64.const 4294967296
      i64.store offset=80
      local.get $l12
      i64.const 4294967296
      i64.store offset=72
      local.get $l12
      i64.const 4294967296
      i64.store offset=64
      local.get $l12
      i64.const 4294967296
      i64.store offset=56
      local.get $l12
      i64.const 4294967296
      i64.store offset=48
      local.get $l12
      i64.const 4294967296
      i64.store offset=40
      local.get $l12
      i64.const 4294967296
      i64.store offset=32
      local.get $l23
      local.get $l23
      if $I6 (result i32)
        local.get $l12
        i32.const 80
        i32.add
        local.get $l23
        i32.const 72
        i32.const 8
        call $f545
        local.get $l12
        i32.load offset=76
      else
        i32.const 1
      end
      i32.const 1
      i32.shr_u
      i32.gt_u
      if $I7
        local.get $l12
        i32.const -64
        i32.sub
        local.get $l23
        i32.const 1
        i32.const 1
        call $f545
      end
      local.get $l23
      local.get $l12
      i32.load offset=60
      i32.const 1
      i32.shr_u
      i32.gt_u
      if $I8
        local.get $l12
        i32.const 48
        i32.add
        local.get $l23
        i32.const 1
        i32.const 1
        call $f545
      end
      local.get $p0
      local.get $l12
      i32.const 80
      i32.add
      i32.const 0
      local.get $l12
      i32.const -64
      i32.sub
      local.get $l12
      i32.const 48
      i32.add
      local.get $l12
      i32.const 32
      i32.add
      i32.const 1
      local.get $p3
      call $f69099
      local.get $l12
      i32.load offset=88
      if $I9
        i32.const 0
        local.set $l14
        loop $L10
          block $B11 (result f32)
            local.get $l12
            i32.load offset=80
            local.get $l14
            i32.const 72
            i32.mul
            i32.add
            local.tee $l10
            i32.load offset=16
            local.tee $p1
            i32.load offset=224
            i32.const 2
            i32.eq
            if $I12
              local.get $l106
              i32.const 4129880
              i32.load8_u
              br_if $B11
              drop
            end
            local.get $l100
          end
          local.set $l37
          block $B13
            block $B14
              local.get $p1
              i32.load offset=900
              i32.const 2
              i32.ne
              br_if $B14
              local.get $p1
              f32.load offset=720
              f32.const 0x0p+0 (;=0;)
              f32.lt
              i32.eqz
              br_if $B14
              local.get $l37
              local.get $p1
              i32.const 856
              i32.add
              local.tee $l7
              i32.load offset=32
              local.tee $l8
              i32.const -1
              i32.eq
              if $I15 (result f32)
                f32.const -0x1p+0 (;=-1;)
              else
                local.get $l7
                i32.load offset=4
                local.get $l8
                i32.const 12
                i32.mul
                i32.add
                f32.load offset=8
              end
              f32.add
              local.set $l37
              global.get $g0
              i32.const 96
              i32.sub
              local.tee $l7
              global.set $g0
              local.get $l7
              i32.const 0
              i32.store offset=12
              local.get $l7
              i32.const 0
              i32.store offset=8
              block $B16 (result f32)
                local.get $l7
                i32.const 12
                i32.add
                local.set $l20
                local.get $l7
                i32.const 8
                i32.add
                local.set $l15
                i32.const 0
                local.set $l17
                f32.const 0x0p+0 (;=0;)
                local.get $p1
                i32.const 856
                i32.add
                local.tee $l8
                i32.load offset=24
                local.tee $l4
                i32.const -1
                i32.eq
                br_if $B16
                drop
                local.get $l8
                i32.load offset=28
                local.tee $l19
                i32.const 1
                i32.add
                local.set $l5
                local.get $l8
                i32.load offset=20
                local.tee $l9
                i32.const 0
                i32.le_s
                local.tee $l18
                i32.eqz
                if $I17
                  local.get $l5
                  local.get $l9
                  i32.rem_s
                  local.set $l5
                end
                local.get $l8
                i32.load offset=4
                local.set $l13
                local.get $l4
                local.set $l11
                loop $L18
                  local.get $l13
                  local.get $l4
                  local.tee $l6
                  i32.const 12
                  i32.mul
                  i32.add
                  f32.load offset=8
                  local.get $l37
                  f32.gt
                  local.set $l16
                  local.get $l4
                  i32.const 1
                  i32.add
                  local.set $l4
                  local.get $l11
                  local.get $l19
                  local.get $l16
                  select
                  local.set $l19
                  local.get $l18
                  i32.eqz
                  if $I19
                    local.get $l4
                    local.get $l9
                    i32.rem_s
                    local.set $l4
                  end
                  local.get $l4
                  local.get $l5
                  i32.ne
                  if $I20
                    local.get $l6
                    local.set $l11
                    local.get $l16
                    local.get $l17
                    i32.or
                    local.tee $l17
                    i32.const 1
                    i32.xor
                    i32.const 1
                    i32.and
                    br_if $L18
                  end
                end
                local.get $l8
                local.get $l19
                i32.store offset=32
                local.get $l20
                local.get $l13
                local.get $l19
                i32.const 12
                i32.mul
                local.tee $l16
                i32.add
                i32.load
                i32.store
                local.get $l15
                local.get $l8
                i32.load offset=4
                local.get $l16
                i32.add
                i32.load offset=4
                local.tee $l4
                i32.store
                local.get $l4
                i32.load
                if $I21
                  i32.const 0
                  local.set $l6
                  loop $L22
                    local.get $l4
                    i32.load offset=4
                    local.get $l4
                    i32.const 4
                    i32.add
                    i32.add
                    local.get $l6
                    i32.const 2
                    i32.shl
                    i32.add
                    local.tee $l4
                    i32.load
                    local.get $l4
                    i32.add
                    i32.const 1
                    i32.store8 offset=114
                    local.get $l6
                    i32.const 1
                    i32.add
                    local.tee $l6
                    local.get $l15
                    i32.load
                    local.tee $l4
                    i32.load
                    i32.lt_u
                    br_if $L22
                  end
                end
                local.get $l8
                i32.load offset=4
                local.get $l16
                i32.add
                f32.load offset=8
              end
              local.set $l38
              block $B23
                block $B24
                  local.get $l7
                  i32.load offset=12
                  if $I25
                    local.get $l37
                    local.get $l38
                    f32.lt
                    i32.eqz
                    if $I26
                      local.get $l8
                      i32.load offset=32
                      i32.const -1
                      i32.ne
                      if $I27
                        local.get $l8
                        i32.load offset=4
                        local.get $l8
                        i32.load offset=28
                        i32.const 12
                        i32.mul
                        i32.add
                        f32.load offset=8
                        drop
                      end
                    end
                    global.get $g0
                    i32.const 80
                    i32.sub
                    local.tee $l4
                    global.set $g0
                    block $B28
                      local.get $p1
                      local.tee $l8
                      i32.load offset=236
                      i32.eqz
                      br_if $B28
                      local.get $l8
                      i32.load offset=932
                      local.tee $l6
                      i32.eqz
                      br_if $B28
                      block $B29
                        local.get $l8
                        i32.load offset=264
                        local.tee $l11
                        i32.eqz
                        br_if $B29
                        local.get $l8
                        i32.load offset=276
                        br_if $B29
                        local.get $l4
                        i64.const 4294967296
                        i64.store offset=72
                        local.get $l4
                        i64.const 322122547200
                        i64.store offset=64
                        local.get $l4
                        local.get $l4
                        i32.const -64
                        i32.sub
                        call $f68356
                        local.tee $l6
                        i32.const 0
                        i32.store8 offset=41
                        local.get $l6
                        local.get $l11
                        call $f69105
                        local.get $l8
                        i32.const 240
                        i32.add
                        local.tee $l19
                        local.get $l4
                        i32.load offset=72
                        i32.const 16
                        local.get $l8
                        i32.load offset=240
                        i32.load
                        call_indirect $__indirect_function_table (type $t3)
                        local.tee $l16
                        if $I30
                          local.get $l16
                          local.get $l4
                          i32.load offset=64
                          local.get $l4
                          i32.load offset=72
                          call $f483
                          drop
                        end
                        local.get $l8
                        local.get $l4
                        i32.load offset=72
                        i32.store offset=276
                        local.get $l6
                        i32.const 44
                        i32.add
                        call $f554
                        drop
                        local.get $l4
                        i32.const -64
                        i32.sub
                        call $f554
                        drop
                        local.get $l8
                        local.get $l16
                        i32.store offset=264
                        local.get $l11
                        local.get $l19
                        call $f68324
                        local.get $l8
                        i32.load offset=932
                        local.set $l6
                      end
                      local.get $l8
                      i32.const 240
                      i32.add
                      local.set $l11
                      global.get $g0
                      i32.const 80
                      i32.sub
                      local.tee $l8
                      global.set $g0
                      block $B31
                        local.get $l6
                        i32.load offset=196
                        local.tee $l5
                        i32.eqz
                        br_if $B31
                        local.get $l6
                        i32.load offset=204
                        br_if $B31
                        local.get $l8
                        i64.const 4294967296
                        i64.store offset=72
                        local.get $l8
                        i64.const 322122547200
                        i64.store offset=64
                        local.get $l8
                        local.get $l8
                        i32.const -64
                        i32.sub
                        call $f68356
                        local.tee $l16
                        i32.const 0
                        i32.store8 offset=41
                        local.get $l16
                        local.get $l5
                        call $f68813
                        local.get $l11
                        local.get $l8
                        i32.load offset=72
                        i32.const 16
                        local.get $l11
                        i32.load
                        i32.load
                        call_indirect $__indirect_function_table (type $t3)
                        local.tee $l19
                        if $I32
                          local.get $l19
                          local.get $l8
                          i32.load offset=64
                          local.get $l8
                          i32.load offset=72
                          call $f483
                          drop
                        end
                        local.get $l6
                        local.get $l8
                        i32.load offset=72
                        i32.store offset=204
                        local.get $l16
                        i32.const 44
                        i32.add
                        call $f554
                        drop
                        local.get $l8
                        i32.const -64
                        i32.sub
                        call $f554
                        drop
                        local.get $l6
                        local.get $l19
                        i32.store offset=196
                        local.get $l5
                        local.get $l11
                        call $f68577
                      end
                      local.get $l8
                      i32.const 80
                      i32.add
                      global.set $g0
                    end
                    local.get $l4
                    i32.const 80
                    i32.add
                    global.set $g0
                    local.get $p1
                    local.get $l37
                    f32.store offset=908
                    local.get $p1
                    i32.load offset=264
                    local.set $l4
                    local.get $p1
                    i32.load offset=276
                    local.set $l16
                    local.get $l7
                    i32.load offset=12
                    local.set $l8
                    local.get $l7
                    i64.const 4294967296
                    i64.store offset=88
                    local.get $l7
                    i64.const 322122547200
                    i64.store offset=80
                    local.get $l7
                    i32.const 16
                    i32.add
                    local.get $l7
                    i32.const 80
                    i32.add
                    call $f68356
                    local.tee $l6
                    i32.const 0
                    i32.store8 offset=41
                    local.get $l6
                    local.get $l8
                    call $f69105
                    local.get $l7
                    i32.load offset=88
                    local.set $l11
                    block $B33
                      block $B34
                        local.get $l4
                        i32.const 0
                        local.get $l4
                        i32.sub
                        i32.const 15
                        i32.and
                        i32.add
                        local.tee $l8
                        i32.eqz
                        br_if $B34
                        local.get $l8
                        local.get $l11
                        i32.add
                        local.get $l4
                        local.get $l16
                        i32.add
                        i32.gt_u
                        br_if $B34
                        local.get $l8
                        local.get $l7
                        i32.load offset=80
                        local.get $l11
                        call $f483
                        drop
                        local.get $p1
                        local.get $l7
                        i32.load offset=88
                        i32.store offset=276
                        local.get $l6
                        i32.const 44
                        i32.add
                        call $f554
                        drop
                        local.get $l7
                        i32.const 80
                        i32.add
                        call $f554
                        drop
                        br $B33
                      end
                      local.get $p1
                      local.get $l11
                      i32.store offset=276
                      local.get $l6
                      i32.const 44
                      i32.add
                      call $f554
                      drop
                      local.get $l7
                      i32.const 80
                      i32.add
                      call $f554
                      drop
                      local.get $p1
                      i32.load offset=264
                      local.get $p1
                      i32.const 240
                      i32.add
                      call $f68324
                      local.get $p1
                      i32.load offset=276
                      i32.const 4
                      local.get $p1
                      i32.load offset=244
                      i32.const 0
                      i32.const 403047
                      i32.const 30
                      call $f83341
                      local.set $l4
                      local.get $p1
                      i32.load offset=276
                      local.set $l16
                      local.get $l7
                      i32.load offset=12
                      local.set $l8
                      local.get $l7
                      i64.const 4294967296
                      i64.store offset=88
                      local.get $l7
                      i64.const 322122547200
                      i64.store offset=80
                      local.get $l7
                      i32.const 16
                      i32.add
                      local.get $l7
                      i32.const 80
                      i32.add
                      call $f68356
                      local.tee $l6
                      i32.const 0
                      i32.store8 offset=41
                      local.get $l6
                      local.get $l8
                      call $f69105
                      local.get $l7
                      i32.load offset=88
                      local.set $l11
                      local.get $l4
                      i32.const 0
                      local.get $l4
                      i32.sub
                      i32.const 15
                      i32.and
                      i32.add
                      local.tee $l8
                      i32.eqz
                      br_if $B24
                      local.get $l8
                      local.get $l11
                      i32.add
                      local.get $l4
                      local.get $l16
                      i32.add
                      i32.gt_u
                      br_if $B24
                      local.get $l8
                      local.get $l7
                      i32.load offset=80
                      local.get $l11
                      call $f483
                      drop
                      local.get $p1
                      local.get $l7
                      i32.load offset=88
                      i32.store offset=276
                      local.get $l6
                      i32.const 44
                      i32.add
                      call $f554
                      drop
                      local.get $l7
                      i32.const 80
                      i32.add
                      call $f554
                      drop
                    end
                    local.get $p1
                    local.get $l8
                    i32.store offset=264
                    local.get $p1
                    local.get $l37
                    local.get $l38
                    f32.sub
                    f32.store offset=904
                    local.get $p1
                    i32.load offset=932
                    local.set $l16
                    local.get $l7
                    i32.load offset=8
                    local.set $l9
                    local.get $p1
                    i32.const 240
                    i32.add
                    local.set $l8
                    global.get $g0
                    i32.const 80
                    i32.sub
                    local.tee $l6
                    global.set $g0
                    local.get $l16
                    i32.load offset=204
                    local.set $l13
                    local.get $l16
                    i32.load offset=196
                    local.set $l5
                    local.get $l6
                    i64.const 4294967296
                    i64.store offset=72
                    local.get $l6
                    i64.const 322122547200
                    i64.store offset=64
                    local.get $l6
                    local.get $l6
                    i32.const -64
                    i32.sub
                    call $f68356
                    local.tee $l4
                    i32.const 0
                    i32.store8 offset=41
                    local.get $l4
                    local.get $l9
                    call $f68813
                    local.get $l6
                    i32.load offset=72
                    local.set $l11
                    block $B35
                      block $B36
                        local.get $l5
                        i32.const 0
                        local.get $l5
                        i32.sub
                        i32.const 15
                        i32.and
                        i32.add
                        local.tee $l19
                        i32.eqz
                        br_if $B36
                        local.get $l11
                        local.get $l19
                        i32.add
                        local.get $l5
                        local.get $l13
                        i32.add
                        i32.gt_u
                        br_if $B36
                        local.get $l19
                        local.get $l6
                        i32.load offset=64
                        local.get $l11
                        call $f483
                        drop
                        local.get $l16
                        local.get $l6
                        i32.load offset=72
                        i32.store offset=204
                        local.get $l4
                        i32.const 44
                        i32.add
                        call $f554
                        drop
                        local.get $l6
                        i32.const -64
                        i32.sub
                        call $f554
                        drop
                        br $B35
                      end
                      local.get $l16
                      local.get $l11
                      i32.store offset=204
                      local.get $l4
                      i32.const 44
                      i32.add
                      call $f554
                      drop
                      local.get $l6
                      i32.const -64
                      i32.sub
                      call $f554
                      drop
                      local.get $l16
                      i32.load offset=196
                      local.get $l8
                      call $f68577
                      local.get $l8
                      local.get $l16
                      i32.load offset=204
                      i32.const 4
                      local.get $l8
                      i32.load
                      i32.load
                      call_indirect $__indirect_function_table (type $t3)
                      local.set $l5
                      local.get $l16
                      i32.load offset=204
                      local.set $l8
                      local.get $l6
                      i64.const 4294967296
                      i64.store offset=72
                      local.get $l6
                      i64.const 322122547200
                      i64.store offset=64
                      local.get $l6
                      local.get $l6
                      i32.const -64
                      i32.sub
                      call $f68356
                      local.tee $l11
                      i32.const 0
                      i32.store8 offset=41
                      local.get $l11
                      local.get $l9
                      call $f68813
                      local.get $l6
                      i32.load offset=72
                      local.set $l4
                      block $B37
                        local.get $l5
                        i32.const 0
                        local.get $l5
                        i32.sub
                        i32.const 15
                        i32.and
                        i32.add
                        local.tee $l19
                        i32.eqz
                        if $I38
                          i32.const 0
                          local.set $l19
                          br $B37
                        end
                        local.get $l4
                        local.get $l19
                        i32.add
                        local.get $l5
                        local.get $l8
                        i32.add
                        i32.gt_u
                        if $I39
                          i32.const 0
                          local.set $l19
                          br $B37
                        end
                        local.get $l19
                        local.get $l6
                        i32.load offset=64
                        local.get $l4
                        call $f483
                        drop
                        local.get $l6
                        i32.load offset=72
                        local.set $l4
                      end
                      local.get $l16
                      local.get $l4
                      i32.store offset=204
                      local.get $l11
                      i32.const 44
                      i32.add
                      call $f554
                      drop
                      local.get $l6
                      i32.const -64
                      i32.sub
                      call $f554
                      drop
                    end
                    local.get $l16
                    local.get $l19
                    i32.store offset=196
                    local.get $l19
                    i32.const 1
                    i32.store8 offset=24
                    local.get $l16
                    i32.load offset=188
                    local.tee $l5
                    i32.load
                    if $I40
                      local.get $l5
                      i32.const 4
                      i32.add
                      local.set $l9
                      i32.const 0
                      local.set $l19
                      loop $L41
                        local.get $l16
                        i32.load offset=264
                        local.get $l5
                        i32.load offset=4
                        local.get $l9
                        i32.add
                        local.get $l19
                        i32.const 2
                        i32.shl
                        i32.add
                        local.tee $l4
                        i32.load
                        local.get $l4
                        i32.add
                        local.tee $l4
                        i32.load
                        local.tee $l11
                        i32.const 3
                        i32.shl
                        i32.add
                        i32.load
                        local.get $l4
                        i32.load offset=4
                        i32.const 2
                        i32.shl
                        i32.add
                        i32.load
                        local.set $l8
                        local.get $l16
                        i32.load offset=196
                        local.tee $l4
                        i32.load offset=4
                        local.get $l4
                        i32.const 4
                        i32.add
                        i32.add
                        local.get $l11
                        i32.const 2
                        i32.shl
                        local.tee $l4
                        i32.add
                        local.tee $l11
                        i32.load
                        local.get $l11
                        i32.add
                        i32.load8_u offset=108
                        local.set $l11
                        local.get $l16
                        i32.load offset=200
                        i32.load offset=4
                        local.get $l4
                        i32.add
                        i32.load
                        i32.load8_u offset=16
                        local.set $l15
                        block $B42
                          block $B43
                            local.get $l8
                            i32.load offset=220
                            local.tee $l4
                            br_if $B43
                            local.get $l11
                            br_if $B43
                            local.get $l8
                            call $f68675
                            br $B42
                          end
                          block $B44
                            local.get $l4
                            i32.eqz
                            br_if $B44
                            local.get $l11
                            i32.eqz
                            br_if $B44
                            local.get $l8
                            i32.load offset=24
                            i32.load offset=16
                            local.tee $l13
                            local.get $l4
                            i32.const 12
                            i32.mul
                            i32.add
                            i32.load
                            local.set $l11
                            local.get $l13
                            i32.load
                            local.set $l4
                            local.get $l8
                            i32.const 0
                            i32.store8 offset=224
                            local.get $l11
                            local.get $l15
                            i32.store8 offset=183
                            local.get $l8
                            i32.const 0
                            call $f68177
                            local.get $l8
                            i32.const 0
                            i32.store8 offset=164
                            local.get $l8
                            local.get $l8
                            i32.load offset=220
                            call $f68177
                            local.get $l8
                            i32.const 0
                            i32.store8 offset=164
                            local.get $l11
                            local.get $l8
                            i32.const -1
                            i32.const 0
                            call $f68180
                            local.get $l8
                            i32.const 0
                            i32.store8 offset=164
                            local.get $l11
                            i32.const 0
                            i32.store8 offset=164
                            local.get $l4
                            local.get $l8
                            i32.const -1
                            i32.const 2
                            call $f68180
                            local.get $l8
                            i32.const 0
                            i32.store8 offset=164
                            local.get $l4
                            i32.const 0
                            i32.store8 offset=164
                            local.get $l8
                            i32.const 2
                            f32.const 0x0p+0 (;=0;)
                            local.get $l8
                            i32.load
                            i32.load offset=12
                            call_indirect $__indirect_function_table (type $t31)
                            local.get $l8
                            i32.const 0
                            i32.store offset=220
                          end
                        end
                        local.get $l19
                        i32.const 1
                        i32.add
                        local.tee $l19
                        local.get $l5
                        i32.load
                        i32.lt_u
                        br_if $L41
                      end
                    end
                    local.get $l6
                    i32.const 80
                    i32.add
                    global.set $g0
                    br $B23
                  end
                  local.get $p1
                  i64.const 0
                  i64.store offset=904
                  br $B23
                end
                local.get $p1
                local.get $l11
                i32.store offset=276
                local.get $l6
                i32.const 44
                i32.add
                call $f554
                drop
                local.get $l7
                i32.const 80
                i32.add
                call $f554
                drop
                local.get $p1
                i64.const 0
                i64.store offset=904
                local.get $p1
                i32.const 0
                i32.store offset=264
              end
              local.get $l7
              i32.const 96
              i32.add
              global.set $g0
              br $B13
            end
            local.get $l10
            i32.load offset=56
            i32.load offset=4
            local.get $l37
            f32.store
          end
          block $B45
            local.get $p1
            i32.load offset=900
            local.tee $l8
            i32.const 1
            i32.ne
            if $I46
              local.get $l8
              i32.const 2
              i32.ne
              br_if $B45
              local.get $p1
              f32.load offset=720
              f32.const 0x0p+0 (;=0;)
              f32.lt
              i32.eqz
              br_if $B45
            end
            local.get $l10
            i32.load offset=56
            i32.load offset=4
            local.get $p1
            f32.load offset=904
            f32.store
            local.get $p1
            i32.const 0
            i32.store offset=904
          end
          local.get $l10
          i32.load offset=56
          i32.load offset=4
          local.get $p1
          i32.load8_u offset=715
          i32.store8 offset=18
          local.get $l10
          i32.load offset=56
          i32.load offset=4
          local.get $p1
          i32.load8_u offset=716
          i32.store8 offset=16
          local.get $p1
          i32.const 36
          i32.add
          local.tee $l6
          i32.load offset=40
          local.tee $l8
          if $I47
            local.get $l6
            i32.load offset=32
            local.tee $l4
            local.set $l7
            loop $L48
              local.get $l7
              i32.load offset=24
              i32.const 5
              i32.ge_u
              if $I49
                local.get $l7
                i32.const 20
                i32.add
                local.set $l8
                local.get $l7
                block $B50 (result f32)
                  local.get $l7
                  i32.load8_u offset=17
                  if $I51
                    local.get $l8
                    call $f69020
                    f32.convert_i32_s
                    br $B50
                  end
                  local.get $l8
                  call $f69022
                end
                f32.store offset=40
                local.get $l6
                i32.load offset=40
                local.set $l8
                local.get $l6
                i32.load offset=32
                local.set $l4
              end
              local.get $l7
              i32.const 44
              i32.add
              local.tee $l7
              local.get $l4
              local.get $l8
              i32.const 44
              i32.mul
              i32.add
              i32.ne
              br_if $L48
            end
          end
          local.get $l10
          i32.const 56
          i32.add
          local.set $l10
          local.get $p1
          i64.load offset=320
          i64.eqz
          i32.eqz
          if $I52
            local.get $p1
            i32.const 320
            i32.add
            local.tee $l8
            call $f79912
            local.get $l8
            call $f79911
          end
          local.get $l10
          i32.load
          i32.load offset=12
          i32.const 0
          i32.store8 offset=137
          block $B53
            local.get $p1
            i32.load offset=900
            local.tee $l8
            i32.const 1
            i32.ne
            if $I54
              local.get $l8
              i32.const 2
              i32.ne
              br_if $B53
              local.get $p1
              f32.load offset=720
              f32.const 0x0p+0 (;=0;)
              f32.lt
              i32.eqz
              br_if $B53
            end
            local.get $p1
            i32.load offset=932
            local.tee $l8
            i32.eqz
            br_if $B53
            local.get $l10
            i32.load
            i32.load offset=4
            f32.load
            local.set $l37
            local.get $l8
            local.get $l8
            i32.load
            i32.load offset=156
            call_indirect $__indirect_function_table (type $t5)
            i32.eqz
            br_if $B53
            block $B55
              local.get $p1
              i32.load offset=932
              i32.load offset=196
              local.tee $l10
              i32.load offset=20
              br_if $B55
              local.get $l37
              f32.const 0x0p+0 (;=0;)
              f32.eq
              if $I56 (result i32)
                local.get $p1
                local.get $p1
                i32.load
                i32.load offset=104
                call_indirect $__indirect_function_table (type $t5)
                br_if $B55
                local.get $p1
                i32.load offset=932
                i32.load offset=196
              else
                local.get $l10
              end
              i32.const 1
              i32.store offset=20
            end
            local.get $p1
            i32.load offset=932
            local.get $l37
            call $f68593
          end
          local.get $l14
          i32.const 1
          i32.add
          local.tee $l14
          local.get $l12
          i32.load offset=88
          i32.lt_u
          br_if $L10
        end
      end
      i32.const 0
      local.set $p1
      local.get $l12
      i32.const 0
      i32.store offset=24
      local.get $l12
      i64.const 0
      i64.store offset=16
      local.get $l12
      i32.const 16
      i32.add
      local.get $l12
      i32.load offset=32
      local.get $l12
      i32.load offset=40
      call $f78319
      local.get $l12
      i32.load offset=88
      local.tee $l10
      if $I57
        local.get $l12
        i32.load offset=80
        local.set $l14
        loop $L58
          global.get $g0
          i32.const 16
          i32.sub
          local.tee $l19
          global.set $g0
          block $B59
            local.get $l14
            local.tee $l7
            local.get $p1
            local.tee $l8
            i32.const 72
            i32.mul
            i32.add
            local.tee $l4
            i32.load offset=56
            local.tee $l11
            i32.load8_u offset=29
            i32.eqz
            br_if $B59
            local.get $l4
            i32.load offset=60
            i32.load
            i32.eqz
            br_if $B59
            block $B60
              local.get $l4
              i32.const 16
              i32.add
              local.tee $l16
              i32.load
              local.tee $l6
              i32.load offset=900
              local.tee $l5
              i32.const 1
              i32.eq
              br_if $B60
              local.get $l5
              i32.const 2
              i32.eq
              if $I61
                local.get $l6
                f32.load offset=720
                f32.const 0x0p+0 (;=0;)
                f32.lt
                br_if $B60
              end
              local.get $l19
              local.get $l4
              i64.load
              local.tee $l107
              i64.store offset=8
              local.get $l11
              i32.load offset=12
              local.set $l11
              local.get $l19
              local.get $l107
              i64.store
              local.get $l19
              local.get $l11
              call $f69091
              local.get $l16
              i32.load
              local.set $l6
            end
            f32.const 0x0p+0 (;=0;)
            local.set $l65
            global.get $g0
            i32.const 80
            i32.sub
            local.tee $l18
            global.set $g0
            local.get $l6
            i32.const 4748488
            i64.load align=4
            i64.store offset=568 align=4
            i32.const 4748496
            i32.load
            local.set $l9
            local.get $l6
            i64.const 4575657221408423936
            i64.store offset=588 align=4
            local.get $l6
            i64.const 0
            i64.store offset=580 align=4
            local.get $l6
            local.get $l9
            i32.store offset=576
            local.get $l6
            i32.const 4748496
            i32.load
            i32.store offset=604
            local.get $l6
            i32.const 4748488
            i64.load align=4
            i64.store offset=596 align=4
            local.get $l6
            i32.const 4748496
            i32.load
            i32.store offset=616
            local.get $l6
            i32.const 4748488
            i64.load align=4
            i64.store offset=608 align=4
            i32.const 1
            local.set $l13
            local.get $l4
            i32.load offset=16
            local.tee $l5
            i32.load8_u offset=714
            i32.eqz
            if $I62
              local.get $l5
              call $f69106
              local.set $l13
            end
            local.get $l4
            i64.load
            local.set $l107
            local.get $l4
            i32.load offset=56
            local.set $l17
            local.get $l4
            i32.load offset=64
            local.set $l9
            local.get $l4
            i32.load offset=68
            local.tee $l5
            i32.load offset=4
            i32.const 0
            call $f68309
            local.get $l9
            i32.load offset=64
            local.get $l9
            i32.load offset=68
            local.get $l9
            i32.load offset=72
            local.get $l5
            i32.load offset=4
            i32.const 1
            call $f68330
            local.get $l5
            i32.const 0
            i32.store8
            local.get $l9
            i32.load offset=56
            local.tee $l9
            i32.const -1
            i32.ne
            if $I63
              local.get $l9
              local.get $l5
              i32.load offset=4
              local.tee $l9
              i32.load offset=28
              local.get $l9
              i32.const 28
              i32.add
              i32.add
              i32.add
              i32.const 1
              i32.store8
              local.get $l5
              i32.const 1
              i32.store8
            end
            local.get $l17
            i32.load offset=4
            local.set $l9
            local.get $l5
            i32.const 0
            i32.store8 offset=12
            local.get $l5
            local.get $l9
            i32.store offset=8
            local.get $l18
            i32.const 40
            i32.add
            call $f68288
            local.get $l5
            i32.load offset=16
            local.tee $l9
            local.get $l18
            i64.load offset=40
            i64.store align=4
            local.get $l9
            local.get $l18
            i32.load offset=48
            i32.store offset=8
            local.get $l5
            local.get $l107
            i64.store offset=36 align=4
            local.get $l5
            i32.const 0
            i32.store offset=32
            local.get $l5
            i32.const 0
            i32.store offset=24
            local.get $l5
            i32.const 0
            i32.store8 offset=21
            local.get $l5
            local.get $l13
            i32.store8 offset=20
            local.get $l18
            i32.const 1
            i32.store8 offset=78
            local.get $l18
            i32.const 0
            i32.store16 offset=76
            local.get $l18
            i32.const -64
            i32.sub
            i32.const 0
            i32.store8
            local.get $l18
            i32.const 0
            i32.store8 offset=52
            local.get $l18
            local.get $l4
            i32.load offset=56
            local.tee $l5
            i32.load offset=8
            local.tee $l9
            i32.load
            i32.store offset=40
            local.get $l18
            local.get $l9
            i32.load offset=4
            i32.store offset=44
            local.get $l18
            local.get $l9
            i32.load offset=16
            i32.store offset=48
            local.get $l18
            local.get $l5
            i32.load offset=8
            i32.load offset=24
            i32.store offset=56
            local.get $l18
            local.get $l5
            i32.load offset=4
            i32.load8_u offset=17
            if $I64 (result i32)
              i32.const 0
            else
              local.get $l5
              i32.load offset=8
              i32.load offset=20
            end
            i32.store offset=60
            local.get $l18
            local.get $l18
            i32.const 40
            i32.add
            i32.store offset=72
            local.get $l18
            i32.const 40
            i32.add
            call $f68367
            local.get $l18
            i32.load offset=44
            i32.const 0
            call $f68309
            local.get $l4
            i32.load offset=68
            local.set $l5
            local.get $l4
            i32.load offset=64
            local.set $l9
            local.get $l18
            i64.const 4294967360
            i64.store offset=32
            local.get $l18
            i64.const 4294967360
            i64.store offset=8
            local.get $l4
            local.get $l9
            local.get $l5
            local.get $l18
            i32.const 72
            i32.add
            i32.const 118906
            i32.const 118907
            i32.const 118908
            i32.const 118909
            local.get $l18
            i32.const 8
            i32.add
            call $f68953
            local.get $l4
            i32.load offset=68
            local.tee $l5
            i32.load8_u offset=20
            if $I65
              local.get $l4
              i32.load offset=64
              i32.load8_u offset=78
              local.set $l9
              local.get $l18
              i32.load offset=72
              i32.load offset=8
              local.get $l5
              i32.load offset=8
              f32.load
              f32.store
              local.get $l4
              i32.load offset=56
              local.tee $l5
              i32.load
              local.set $l15
              local.get $l5
              i32.load offset=4
              local.set $l20
              local.get $l5
              i32.load offset=12
              local.set $l17
              local.get $l5
              i32.load offset=16
              local.set $l24
              local.get $l5
              i32.load offset=8
              local.set $l25
              global.get $g0
              i32.const 48
              i32.sub
              local.tee $l13
              global.set $g0
              block $B66
                local.get $l15
                i32.load offset=20
                local.tee $l21
                i32.eqz
                br_if $B66
                local.get $l21
                local.get $l15
                i32.const 20
                i32.add
                local.tee $l26
                i32.add
                local.tee $l15
                i32.load offset=40
                local.get $l15
                i32.const 40
                i32.add
                i32.add
                i32.load
                i32.eqz
                br_if $B66
                local.get $l13
                i32.const 8
                i32.add
                local.get $l25
                i32.load offset=16
                call $f68340
                local.get $l25
                i32.load offset=16
                local.tee $l15
                f32.load offset=40
                local.set $l75
                local.get $l15
                f32.load offset=44
                local.set $l76
                local.get $l15
                f32.load offset=36
                local.set $l77
                local.get $l15
                f32.load offset=76
                local.set $l88
                local.get $l15
                f32.load offset=84
                local.set $l93
                local.get $l15
                f32.load offset=80
                local.set $l64
                local.get $l17
                i32.load8_u offset=136
                i32.eqz
                if $I67
                  local.get $l13
                  local.get $l13
                  f32.load offset=16
                  local.tee $l86
                  local.get $l13
                  f32.load offset=44
                  local.tee $l70
                  local.get $l17
                  f32.load offset=128
                  local.get $l86
                  local.get $l76
                  local.get $l70
                  f32.mul
                  local.tee $l66
                  local.get $l77
                  local.get $l13
                  f32.load offset=36
                  local.tee $l89
                  f32.mul
                  local.tee $l68
                  local.get $l13
                  f32.load offset=24
                  local.tee $l49
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l78
                  local.get $l13
                  f32.load offset=32
                  local.tee $l61
                  f32.mul
                  local.tee $l101
                  local.get $l13
                  f32.load offset=20
                  local.tee $l50
                  local.get $l13
                  f32.load offset=28
                  local.tee $l57
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l79
                  f32.mul
                  f32.sub
                  local.tee $l84
                  f32.mul
                  f32.add
                  local.get $l66
                  local.get $l50
                  local.get $l50
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l90
                  f32.mul
                  local.get $l49
                  local.get $l49
                  local.get $l49
                  f32.add
                  local.tee $l102
                  f32.mul
                  f32.sub
                  local.tee $l91
                  f32.mul
                  local.get $l75
                  local.get $l13
                  f32.load offset=40
                  local.tee $l48
                  f32.mul
                  local.tee $l103
                  local.get $l49
                  local.get $l57
                  local.get $l57
                  f32.add
                  local.tee $l104
                  f32.mul
                  local.get $l61
                  local.get $l90
                  f32.mul
                  local.tee $l105
                  f32.sub
                  local.tee $l95
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  local.get $l70
                  local.get $l15
                  f32.load offset=72
                  f32.mul
                  local.tee $l53
                  f32.const 0x0p+0 (;=0;)
                  f32.const 0x1p+0 (;=1;)
                  local.get $l53
                  f32.div
                  local.get $l53
                  f32.abs
                  f32.const 0x1.12e0bep-30 (;=1e-09;)
                  f32.lt
                  select
                  local.get $l15
                  f32.load offset=140
                  local.tee $l82
                  local.get $l15
                  i32.load offset=132
                  i32.const -2147483648
                  i32.xor
                  f32.reinterpret_i32
                  local.tee $l53
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l58
                  f32.mul
                  local.tee $l71
                  local.get $l15
                  i32.load offset=136
                  i32.const -2147483648
                  i32.xor
                  f32.reinterpret_i32
                  local.tee $l60
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l62
                  local.get $l15
                  i32.load offset=128
                  i32.const -2147483648
                  i32.xor
                  f32.reinterpret_i32
                  local.tee $l67
                  f32.mul
                  f32.sub
                  local.get $l15
                  f32.load offset=116
                  local.tee $l55
                  f32.neg
                  local.tee $l87
                  f32.mul
                  local.get $l15
                  f32.load offset=124
                  local.tee $l83
                  f32.sub
                  local.get $l67
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l63
                  local.get $l67
                  f32.mul
                  local.get $l53
                  local.get $l53
                  f32.add
                  local.tee $l72
                  local.get $l53
                  f32.mul
                  f32.sub
                  local.get $l83
                  f32.neg
                  local.tee $l94
                  f32.mul
                  local.get $l15
                  f32.load offset=120
                  local.tee $l85
                  local.get $l60
                  local.get $l60
                  f32.add
                  local.tee $l56
                  local.get $l53
                  f32.mul
                  local.get $l82
                  local.get $l63
                  f32.mul
                  local.tee $l73
                  f32.sub
                  f32.mul
                  f32.sub
                  f32.add
                  f32.mul
                  f32.mul
                  local.tee $l96
                  local.get $l15
                  f32.load offset=60
                  local.tee $l80
                  local.get $l61
                  f32.mul
                  local.get $l15
                  f32.load offset=48
                  local.tee $l69
                  local.get $l50
                  f32.mul
                  f32.sub
                  local.get $l15
                  f32.load offset=56
                  local.tee $l81
                  local.get $l57
                  f32.mul
                  f32.sub
                  local.get $l15
                  f32.load offset=52
                  local.tee $l74
                  local.get $l49
                  f32.mul
                  f32.sub
                  local.tee $l97
                  local.get $l81
                  local.get $l50
                  f32.mul
                  local.get $l69
                  local.get $l57
                  f32.mul
                  f32.sub
                  local.get $l74
                  local.get $l61
                  f32.mul
                  f32.sub
                  local.get $l80
                  local.get $l49
                  f32.mul
                  f32.sub
                  i32.reinterpret_f32
                  i32.const -2147483648
                  i32.xor
                  f32.reinterpret_i32
                  local.tee $l83
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l41
                  f32.mul
                  local.tee $l43
                  local.get $l69
                  local.get $l49
                  f32.mul
                  local.get $l81
                  local.get $l61
                  f32.mul
                  f32.sub
                  local.get $l80
                  local.get $l57
                  f32.mul
                  f32.sub
                  local.get $l74
                  local.get $l50
                  f32.mul
                  f32.sub
                  i32.reinterpret_f32
                  i32.const -2147483648
                  i32.xor
                  f32.reinterpret_i32
                  local.tee $l92
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l45
                  local.get $l74
                  local.get $l57
                  f32.mul
                  local.get $l81
                  local.get $l49
                  f32.mul
                  f32.sub
                  local.get $l69
                  local.get $l61
                  f32.mul
                  f32.sub
                  local.get $l80
                  local.get $l50
                  f32.mul
                  f32.sub
                  i32.reinterpret_f32
                  i32.const -2147483648
                  i32.xor
                  f32.reinterpret_i32
                  local.tee $l80
                  f32.mul
                  f32.sub
                  local.get $l15
                  i32.const -64
                  i32.sub
                  f32.load
                  local.get $l89
                  f32.mul
                  local.tee $l69
                  f32.const 0x0p+0 (;=0;)
                  f32.const 0x1p+0 (;=1;)
                  local.get $l69
                  f32.div
                  local.get $l69
                  f32.abs
                  f32.const 0x1.12e0bep-30 (;=1e-09;)
                  f32.lt
                  select
                  local.get $l58
                  local.get $l53
                  f32.mul
                  local.get $l56
                  local.get $l60
                  f32.mul
                  f32.sub
                  local.get $l87
                  f32.mul
                  local.get $l55
                  f32.sub
                  local.get $l67
                  local.get $l67
                  f32.add
                  local.tee $l69
                  local.get $l60
                  f32.mul
                  local.get $l71
                  f32.sub
                  local.get $l94
                  f32.mul
                  local.get $l85
                  local.get $l82
                  local.get $l62
                  f32.mul
                  local.tee $l81
                  local.get $l63
                  local.get $l53
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.sub
                  f32.add
                  f32.mul
                  f32.mul
                  local.tee $l63
                  f32.mul
                  f32.add
                  local.get $l80
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l71
                  local.get $l80
                  f32.mul
                  local.get $l83
                  local.get $l83
                  f32.add
                  local.get $l83
                  f32.mul
                  f32.sub
                  local.get $l96
                  f32.mul
                  local.get $l92
                  local.get $l92
                  f32.add
                  local.tee $l46
                  local.get $l83
                  f32.mul
                  local.get $l97
                  local.get $l71
                  f32.mul
                  f32.sub
                  local.get $l15
                  f32.load offset=68
                  local.get $l48
                  f32.mul
                  local.tee $l53
                  f32.const 0x0p+0 (;=0;)
                  f32.const 0x1p+0 (;=1;)
                  local.get $l53
                  f32.div
                  local.get $l53
                  f32.abs
                  f32.const 0x1.12e0bep-30 (;=1e-09;)
                  f32.lt
                  select
                  local.get $l72
                  local.get $l67
                  f32.mul
                  local.get $l81
                  f32.sub
                  local.get $l87
                  f32.mul
                  local.get $l85
                  f32.sub
                  local.get $l73
                  local.get $l58
                  local.get $l60
                  f32.mul
                  f32.sub
                  local.get $l94
                  f32.mul
                  local.get $l85
                  local.get $l62
                  local.get $l60
                  f32.mul
                  local.get $l69
                  local.get $l67
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.sub
                  f32.add
                  f32.mul
                  f32.mul
                  local.tee $l47
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  local.tee $l51
                  local.get $l86
                  local.get $l93
                  local.get $l70
                  f32.mul
                  local.tee $l58
                  local.get $l88
                  local.get $l89
                  f32.mul
                  local.tee $l62
                  local.get $l84
                  f32.mul
                  f32.add
                  local.get $l58
                  local.get $l91
                  f32.mul
                  local.get $l64
                  local.get $l48
                  f32.mul
                  local.tee $l52
                  local.get $l95
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  local.get $l70
                  local.get $l15
                  f32.load offset=112
                  f32.mul
                  local.tee $l53
                  f32.const 0x0p+0 (;=0;)
                  f32.const 0x1p+0 (;=1;)
                  local.get $l53
                  f32.div
                  local.get $l53
                  f32.abs
                  f32.const 0x1.12e0bep-30 (;=1e-09;)
                  f32.lt
                  select
                  local.get $l15
                  f32.load offset=180
                  local.tee $l87
                  local.get $l15
                  i32.load offset=172
                  i32.const -2147483648
                  i32.xor
                  f32.reinterpret_i32
                  local.tee $l53
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l94
                  f32.mul
                  local.tee $l54
                  local.get $l15
                  i32.load offset=176
                  i32.const -2147483648
                  i32.xor
                  f32.reinterpret_i32
                  local.tee $l60
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l55
                  local.get $l15
                  i32.load offset=168
                  i32.const -2147483648
                  i32.xor
                  f32.reinterpret_i32
                  local.tee $l67
                  f32.mul
                  f32.sub
                  local.get $l15
                  f32.load offset=156
                  local.tee $l59
                  f32.neg
                  local.tee $l72
                  f32.mul
                  local.get $l15
                  f32.load offset=164
                  local.tee $l70
                  f32.sub
                  local.get $l67
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l56
                  local.get $l67
                  f32.mul
                  local.get $l53
                  local.get $l53
                  f32.add
                  local.tee $l37
                  local.get $l53
                  f32.mul
                  f32.sub
                  local.get $l70
                  f32.neg
                  local.tee $l73
                  f32.mul
                  local.get $l15
                  f32.load offset=160
                  local.tee $l81
                  local.get $l60
                  local.get $l60
                  f32.add
                  local.tee $l38
                  local.get $l53
                  f32.mul
                  local.get $l87
                  local.get $l56
                  f32.mul
                  local.tee $l39
                  f32.sub
                  f32.mul
                  f32.sub
                  f32.add
                  f32.mul
                  f32.mul
                  local.tee $l98
                  local.get $l15
                  f32.load offset=100
                  local.tee $l69
                  local.get $l61
                  f32.mul
                  local.get $l15
                  f32.load offset=88
                  local.tee $l74
                  local.get $l50
                  f32.mul
                  f32.sub
                  local.get $l15
                  f32.load offset=96
                  local.tee $l86
                  local.get $l57
                  f32.mul
                  f32.sub
                  local.get $l15
                  f32.load offset=92
                  local.tee $l82
                  local.get $l49
                  f32.mul
                  f32.sub
                  local.tee $l99
                  local.get $l86
                  local.get $l50
                  f32.mul
                  local.get $l74
                  local.get $l57
                  f32.mul
                  f32.sub
                  local.get $l82
                  local.get $l61
                  f32.mul
                  f32.sub
                  local.get $l69
                  local.get $l49
                  f32.mul
                  f32.sub
                  i32.reinterpret_f32
                  i32.const -2147483648
                  i32.xor
                  f32.reinterpret_i32
                  local.tee $l70
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l40
                  f32.mul
                  local.tee $l42
                  local.get $l74
                  local.get $l49
                  f32.mul
                  local.get $l86
                  local.get $l61
                  f32.mul
                  f32.sub
                  local.get $l69
                  local.get $l57
                  f32.mul
                  f32.sub
                  local.get $l82
                  local.get $l50
                  f32.mul
                  f32.sub
                  i32.reinterpret_f32
                  i32.const -2147483648
                  i32.xor
                  f32.reinterpret_i32
                  local.tee $l85
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l44
                  local.get $l82
                  local.get $l57
                  f32.mul
                  local.get $l86
                  local.get $l49
                  f32.mul
                  f32.sub
                  local.get $l74
                  local.get $l61
                  f32.mul
                  f32.sub
                  local.get $l69
                  local.get $l50
                  f32.mul
                  f32.sub
                  i32.reinterpret_f32
                  i32.const -2147483648
                  i32.xor
                  f32.reinterpret_i32
                  local.tee $l69
                  f32.mul
                  f32.sub
                  local.get $l15
                  f32.load offset=104
                  local.get $l89
                  f32.mul
                  local.tee $l74
                  f32.const 0x0p+0 (;=0;)
                  f32.const 0x1p+0 (;=1;)
                  local.get $l74
                  f32.div
                  local.get $l74
                  f32.abs
                  f32.const 0x1.12e0bep-30 (;=1e-09;)
                  f32.lt
                  select
                  local.get $l94
                  local.get $l53
                  f32.mul
                  local.get $l38
                  local.get $l60
                  f32.mul
                  f32.sub
                  local.get $l72
                  f32.mul
                  local.get $l59
                  f32.sub
                  local.get $l67
                  local.get $l67
                  f32.add
                  local.tee $l82
                  local.get $l60
                  f32.mul
                  local.get $l54
                  f32.sub
                  local.get $l73
                  f32.mul
                  local.get $l81
                  local.get $l87
                  local.get $l55
                  f32.mul
                  local.tee $l87
                  local.get $l56
                  local.get $l53
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.sub
                  f32.add
                  f32.mul
                  f32.mul
                  local.tee $l74
                  f32.mul
                  f32.add
                  local.get $l69
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l86
                  local.get $l69
                  f32.mul
                  local.get $l70
                  local.get $l70
                  f32.add
                  local.get $l70
                  f32.mul
                  f32.sub
                  local.get $l98
                  f32.mul
                  local.get $l85
                  local.get $l85
                  f32.add
                  local.tee $l56
                  local.get $l70
                  f32.mul
                  local.get $l99
                  local.get $l86
                  f32.mul
                  f32.sub
                  local.get $l15
                  f32.load offset=108
                  local.get $l48
                  f32.mul
                  local.tee $l53
                  f32.const 0x0p+0 (;=0;)
                  f32.const 0x1p+0 (;=1;)
                  local.get $l53
                  f32.div
                  local.get $l53
                  f32.abs
                  f32.const 0x1.12e0bep-30 (;=1e-09;)
                  f32.lt
                  select
                  local.get $l37
                  local.get $l67
                  f32.mul
                  local.get $l87
                  f32.sub
                  local.get $l72
                  f32.mul
                  local.get $l81
                  f32.sub
                  local.get $l39
                  local.get $l94
                  local.get $l60
                  f32.mul
                  f32.sub
                  local.get $l73
                  f32.mul
                  local.get $l81
                  local.get $l55
                  local.get $l60
                  f32.mul
                  local.get $l82
                  local.get $l67
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.sub
                  f32.add
                  f32.mul
                  f32.mul
                  local.tee $l87
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  local.get $l51
                  f32.sub
                  local.get $l17
                  f32.load offset=132
                  local.tee $l94
                  f32.mul
                  f32.add
                  f32.sub
                  local.get $l20
                  f32.load offset=12
                  local.get $l15
                  f32.load offset=196
                  f32.mul
                  local.tee $l55
                  f32.mul
                  f32.mul
                  local.tee $l53
                  local.get $l84
                  local.get $l89
                  local.get $l17
                  f32.load offset=120
                  local.get $l13
                  f32.load offset=8
                  local.tee $l60
                  local.get $l68
                  local.get $l68
                  local.get $l49
                  local.get $l78
                  f32.mul
                  local.get $l57
                  local.get $l104
                  f32.mul
                  f32.sub
                  local.tee $l67
                  f32.mul
                  f32.add
                  local.get $l66
                  local.get $l50
                  local.get $l50
                  f32.add
                  local.tee $l68
                  local.get $l57
                  f32.mul
                  local.get $l101
                  f32.sub
                  local.tee $l81
                  f32.mul
                  local.get $l103
                  local.get $l61
                  local.get $l79
                  f32.mul
                  local.tee $l66
                  local.get $l49
                  local.get $l90
                  f32.mul
                  f32.sub
                  local.tee $l82
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  local.get $l63
                  local.get $l63
                  local.get $l41
                  local.get $l83
                  f32.mul
                  local.get $l46
                  local.get $l92
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  local.get $l80
                  local.get $l80
                  f32.add
                  local.get $l92
                  f32.mul
                  local.get $l43
                  f32.sub
                  local.get $l96
                  f32.mul
                  local.get $l97
                  local.get $l45
                  f32.mul
                  local.get $l71
                  local.get $l83
                  f32.mul
                  f32.sub
                  local.get $l47
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  local.tee $l49
                  local.get $l60
                  local.get $l62
                  local.get $l62
                  local.get $l67
                  f32.mul
                  f32.add
                  local.get $l58
                  local.get $l81
                  f32.mul
                  local.get $l52
                  local.get $l82
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  local.get $l74
                  local.get $l74
                  local.get $l40
                  local.get $l70
                  f32.mul
                  local.get $l56
                  local.get $l85
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  local.get $l69
                  local.get $l69
                  f32.add
                  local.get $l85
                  f32.mul
                  local.get $l42
                  f32.sub
                  local.get $l98
                  f32.mul
                  local.get $l99
                  local.get $l44
                  f32.mul
                  local.get $l86
                  local.get $l70
                  f32.mul
                  f32.sub
                  local.get $l87
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  local.get $l49
                  f32.sub
                  local.get $l94
                  f32.mul
                  f32.add
                  f32.sub
                  local.get $l55
                  f32.mul
                  f32.mul
                  local.tee $l49
                  f32.mul
                  f32.add
                  local.get $l48
                  f32.const 0x0p+0 (;=0;)
                  f32.mul
                  local.tee $l61
                  local.get $l95
                  f32.mul
                  local.get $l91
                  local.get $l53
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.store offset=16
                  local.get $l13
                  local.get $l13
                  f32.load offset=12
                  local.get $l61
                  local.get $l50
                  local.get $l102
                  f32.mul
                  local.get $l66
                  f32.sub
                  local.get $l49
                  f32.mul
                  f32.add
                  local.get $l61
                  local.get $l57
                  local.get $l79
                  f32.mul
                  local.get $l50
                  local.get $l68
                  f32.mul
                  f32.sub
                  f32.mul
                  local.get $l105
                  local.get $l78
                  local.get $l57
                  f32.mul
                  f32.sub
                  local.get $l53
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.store offset=12
                  local.get $l13
                  local.get $l60
                  local.get $l49
                  local.get $l67
                  local.get $l49
                  f32.mul
                  f32.add
                  local.get $l61
                  local.get $l82
                  f32.mul
                  local.get $l81
                  local.get $l53
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.store offset=8
                  local.get $l13
                  i32.const 8
                  i32.add
                  local.tee $l20
                  i64.load align=4
                  local.set $l107
                  local.get $l15
                  local.get $l20
                  f32.load offset=8
                  f32.store offset=12
                  local.get $l15
                  local.get $l107
                  i64.store offset=4 align=4
                end
                block $B68
                  local.get $l25
                  i32.load offset=16
                  local.tee $l15
                  f32.load
                  f32.const 0x0p+0 (;=0;)
                  f32.eq
                  if $I69
                    local.get $l17
                    f32.load offset=132
                    local.set $l49
                    br $B68
                  end
                  f32.const 0x0p+0 (;=0;)
                  local.set $l49
                  local.get $l15
                  f32.load offset=116
                  local.tee $l50
                  local.get $l50
                  f32.mul
                  local.get $l15
                  f32.load offset=120
                  local.tee $l50
                  local.get $l50
                  f32.mul
                  f32.add
                  local.get $l15
                  f32.load offset=124
                  local.tee $l50
                  local.get $l50
                  f32.mul
                  f32.const 0x0p+0 (;=0;)
                  f32.add
                  f32.add
                  f32.sqrt
                  local.tee $l57
                  local.get $l15
                  f32.load offset=156
                  local.tee $l50
                  local.get $l50
                  f32.mul
                  local.get $l15
                  f32.load offset=160
                  local.tee $l50
                  local.get $l50
                  f32.mul
                  f32.add
                  local.get $l15
                  f32.load offset=164
                  local.tee $l50
                  local.get $l50
                  f32.mul
                  f32.const 0x0p+0 (;=0;)
                  f32.add
                  f32.add
                  f32.sqrt
                  f32.add
                  local.tee $l50
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  if $I70
                    local.get $l57
                    local.get $l50
                    f32.div
                    f32.const 0x0p+0 (;=0;)
                    call $f65475
                    f32.const 0x1p+0 (;=1;)
                    call $f65476
                    f32.const -0x1p-1 (;=-0.5;)
                    f32.add
                    local.set $l49
                  end
                  local.get $l17
                  local.get $l15
                  f32.load offset=196
                  local.get $l49
                  f32.mul
                  f32.const 0x1p-1 (;=0.5;)
                  f32.add
                  local.tee $l49
                  f32.store offset=132
                end
                local.get $l17
                local.get $l76
                local.get $l93
                local.get $l76
                f32.sub
                local.get $l49
                f32.mul
                f32.add
                f32.store offset=128
                local.get $l17
                local.get $l75
                local.get $l64
                local.get $l75
                f32.sub
                local.get $l49
                f32.mul
                f32.add
                f32.store offset=124
                local.get $l17
                local.get $l77
                local.get $l88
                local.get $l77
                f32.sub
                local.get $l49
                f32.mul
                f32.add
                f32.store offset=120
                f32.const 0x1p+0 (;=1;)
                local.set $l60
                block $B71
                  local.get $l26
                  i32.load
                  local.tee $l15
                  i32.eqz
                  br_if $B71
                  local.get $l15
                  local.get $l26
                  i32.add
                  local.tee $l15
                  i32.load offset=40
                  local.get $l15
                  i32.const 40
                  i32.add
                  i32.add
                  i32.load
                  i32.eqz
                  br_if $B71
                  local.get $l15
                  f32.load offset=256
                  local.set $l60
                end
                local.get $l17
                f32.load
                local.set $l67
                local.get $l17
                f32.load offset=4
                local.set $l83
                local.get $l24
                i32.const 20
                i32.add
                local.tee $l15
                local.get $l17
                f32.load offset=8
                local.tee $l64
                f32.store
                local.get $l24
                i32.const 16
                i32.add
                local.tee $l25
                local.get $l83
                f32.store
                local.get $l24
                local.get $l67
                f32.store offset=12
                local.get $l17
                f32.load offset=16
                local.set $l49
                local.get $l17
                f32.load offset=20
                local.set $l50
                local.get $l17
                f32.load offset=12
                local.set $l57
                local.get $l24
                i32.const 36
                i32.add
                local.tee $l21
                local.get $l17
                f32.load offset=24
                local.tee $l61
                f32.store
                local.get $l24
                i32.const 32
                i32.add
                local.tee $l26
                local.get $l50
                f32.store
                local.get $l24
                i32.const 28
                i32.add
                local.tee $l20
                local.get $l49
                f32.store
                local.get $l24
                i32.const 24
                i32.add
                local.tee $l11
                local.get $l57
                f32.store
                local.get $l17
                f32.load offset=32
                local.set $l70
                local.get $l17
                f32.load offset=28
                local.set $l88
                local.get $l13
                f32.load offset=8
                local.set $l89
                local.get $l13
                f32.load offset=12
                local.set $l48
                local.get $l13
                f32.load offset=16
                local.set $l92
                local.get $l13
                f32.load offset=24
                local.set $l75
                local.get $l13
                f32.load offset=28
                local.set $l76
                local.get $l13
                f32.load offset=32
                local.set $l77
                local.get $l13
                f32.load offset=20
                local.set $l53
                local.get $l13
                f32.load offset=36
                local.set $l93
                local.get $l13
                f32.load offset=40
                local.set $l80
                local.get $l24
                local.get $l17
                f32.load offset=36
                local.tee $l85
                local.get $l13
                f32.load offset=44
                f32.mul
                f32.store offset=48
                local.get $l24
                local.get $l70
                local.get $l80
                f32.mul
                f32.store offset=44
                local.get $l24
                local.get $l88
                local.get $l93
                f32.mul
                f32.store offset=40
                local.get $l21
                local.get $l61
                local.get $l77
                f32.mul
                local.get $l57
                local.get $l53
                f32.mul
                f32.sub
                local.get $l50
                local.get $l76
                f32.mul
                f32.sub
                local.get $l49
                local.get $l75
                f32.mul
                f32.sub
                f32.store
                local.get $l26
                local.get $l49
                local.get $l53
                f32.mul
                local.get $l61
                local.get $l76
                f32.mul
                f32.sub
                local.get $l50
                local.get $l77
                f32.mul
                f32.sub
                local.get $l57
                local.get $l75
                f32.mul
                f32.sub
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                i32.store
                local.get $l20
                local.get $l57
                local.get $l76
                f32.mul
                local.get $l50
                local.get $l53
                f32.mul
                f32.sub
                local.get $l61
                local.get $l75
                f32.mul
                f32.sub
                local.get $l49
                local.get $l77
                f32.mul
                f32.sub
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                i32.store
                local.get $l11
                local.get $l50
                local.get $l75
                f32.mul
                local.get $l49
                local.get $l76
                f32.mul
                f32.sub
                local.get $l61
                local.get $l53
                f32.mul
                f32.sub
                local.get $l57
                local.get $l77
                f32.mul
                f32.sub
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                i32.store
                local.get $l15
                local.get $l64
                local.get $l61
                local.get $l49
                f32.const -0x1p+1 (;=-2;)
                f32.mul
                local.tee $l53
                f32.mul
                local.tee $l80
                local.get $l57
                local.get $l50
                f32.const -0x1p+1 (;=-2;)
                f32.mul
                local.tee $l93
                f32.mul
                f32.sub
                local.get $l88
                local.get $l60
                local.get $l89
                f32.mul
                f32.mul
                local.tee $l75
                f32.mul
                local.get $l85
                local.get $l60
                local.get $l92
                f32.mul
                f32.mul
                local.tee $l76
                f32.add
                local.get $l49
                local.get $l50
                local.get $l50
                f32.add
                local.tee $l89
                f32.mul
                local.get $l61
                local.get $l57
                f32.const -0x1p+1 (;=-2;)
                f32.mul
                local.tee $l88
                f32.mul
                local.tee $l92
                f32.sub
                local.get $l70
                local.get $l60
                local.get $l48
                f32.mul
                f32.mul
                local.tee $l77
                f32.mul
                local.get $l57
                local.get $l88
                f32.mul
                local.get $l49
                local.get $l49
                local.get $l49
                f32.add
                local.tee $l60
                f32.mul
                f32.sub
                local.get $l76
                f32.mul
                f32.add
                f32.add
                f32.add
                f32.store
                local.get $l25
                local.get $l83
                local.get $l77
                local.get $l57
                local.get $l60
                f32.mul
                local.get $l61
                local.get $l93
                f32.mul
                local.tee $l61
                f32.sub
                local.get $l75
                f32.mul
                f32.add
                local.get $l50
                local.get $l93
                f32.mul
                local.get $l57
                local.get $l57
                local.get $l57
                f32.add
                local.tee $l60
                f32.mul
                f32.sub
                local.get $l77
                f32.mul
                local.get $l92
                local.get $l53
                local.get $l50
                f32.mul
                f32.sub
                local.get $l76
                f32.mul
                f32.add
                f32.add
                f32.add
                f32.store
                local.get $l24
                local.get $l67
                local.get $l75
                local.get $l75
                local.get $l49
                local.get $l53
                f32.mul
                local.get $l50
                local.get $l89
                f32.mul
                f32.sub
                f32.mul
                f32.add
                local.get $l61
                local.get $l49
                local.get $l88
                f32.mul
                f32.sub
                local.get $l77
                f32.mul
                local.get $l60
                local.get $l50
                f32.mul
                local.get $l80
                f32.sub
                local.get $l76
                f32.mul
                f32.add
                f32.add
                f32.add
                f32.store offset=12
              end
              local.get $l13
              i32.const 48
              i32.add
              global.set $g0
              local.get $l4
              i32.load offset=56
              local.set $l5
              f32.const 0x1p+0 (;=1;)
              local.set $l62
              local.get $l9
              if $I72
                local.get $l5
                i32.load
                local.tee $l9
                i32.load offset=20
                local.get $l9
                i32.const 20
                i32.add
                i32.add
                f32.load offset=256
                local.set $l62
              end
              local.get $l5
              i32.load offset=8
              i32.load offset=16
              local.tee $l5
              local.get $l62
              local.get $l5
              f32.load offset=216
              f32.mul
              f32.store offset=216
              local.get $l5
              i32.const 224
              i32.add
              local.tee $l9
              local.get $l62
              local.get $l9
              f32.load
              f32.mul
              f32.store
              local.get $l5
              i32.const 220
              i32.add
              local.tee $l5
              local.get $l62
              local.get $l5
              f32.load
              f32.mul
              f32.store
              global.get $g0
              i32.const 128
              i32.sub
              local.tee $l5
              global.set $g0
              block $B73
                local.get $l6
                f32.load offset=660
                f32.const 0x0p+0 (;=0;)
                f32.ge
                i32.eqz
                br_if $B73
                local.get $l6
                i32.load offset=932
                local.tee $l21
                i32.load offset=196
                local.tee $l11
                i32.load offset=4
                local.get $l11
                i32.const 4
                i32.add
                i32.add
                local.get $l21
                i32.load offset=188
                local.tee $l21
                i32.load offset=4
                local.get $l21
                i32.const 4
                i32.add
                i32.add
                local.tee $l21
                i32.load
                local.get $l21
                i32.add
                i32.load
                i32.const 2
                i32.shl
                i32.add
                local.tee $l21
                i32.load
                local.tee $l11
                local.get $l21
                i32.add
                i32.const 0
                local.get $l11
                select
                i32.load8_u offset=109
                i32.eqz
                if $I74
                  i32.const 0
                  local.set $l21
                  block $B75
                    local.get $l6
                    local.tee $l11
                    i32.load8_u offset=216
                    i32.eqz
                    br_if $B75
                    local.get $l11
                    i32.load offset=28
                    local.tee $l20
                    i32.eqz
                    br_if $B75
                    local.get $l20
                    call $f80180
                    i32.eqz
                    br_if $B75
                    local.get $l11
                    i32.load offset=236
                    i32.eqz
                    br_if $B75
                    local.get $l11
                    i32.load offset=932
                    local.tee $l20
                    i32.eqz
                    br_if $B75
                    local.get $l20
                    i32.const 0
                    call $f68616
                    i32.eqz
                    br_if $B75
                    local.get $l11
                    i32.load offset=932
                    local.tee $l25
                    i32.load offset=188
                    local.tee $l20
                    i32.load offset=12
                    local.get $l20
                    i32.const 12
                    i32.add
                    i32.add
                    local.get $l20
                    i32.load offset=4
                    local.get $l20
                    i32.const 4
                    i32.add
                    i32.add
                    local.tee $l20
                    local.get $l20
                    i32.load
                    i32.add
                    i32.load
                    i32.const 2
                    i32.shl
                    i32.add
                    local.tee $l20
                    i32.load
                    local.tee $l26
                    local.get $l20
                    i32.add
                    i32.const 0
                    local.get $l26
                    select
                    local.tee $l20
                    i32.load
                    i32.eqz
                    br_if $B75
                    i32.const 1
                    local.set $l21
                    local.get $l11
                    i32.load offset=664
                    local.tee $l11
                    local.get $l20
                    i32.load offset=4
                    local.get $l20
                    i32.const 4
                    i32.add
                    i32.add
                    local.get $l25
                    i32.load offset=196
                    local.tee $l20
                    i32.load offset=4
                    local.get $l20
                    i32.const 4
                    i32.add
                    i32.add
                    local.get $l25
                    i32.load offset=188
                    local.tee $l25
                    i32.load offset=4
                    local.get $l25
                    i32.const 4
                    i32.add
                    i32.add
                    local.tee $l25
                    i32.load
                    local.get $l25
                    i32.add
                    i32.load
                    i32.const 2
                    i32.shl
                    i32.add
                    local.tee $l25
                    i32.load
                    local.tee $l20
                    local.get $l25
                    i32.add
                    i32.const 0
                    local.get $l20
                    select
                    i32.load offset=12
                    i32.const 2
                    i32.shl
                    i32.add
                    local.tee $l20
                    i32.load
                    local.tee $l26
                    local.get $l20
                    i32.add
                    i32.const 0
                    local.get $l26
                    select
                    local.tee $l20
                    i32.load offset=32
                    i32.eq
                    br_if $B75
                    local.get $l20
                    i32.load offset=28
                    local.get $l11
                    i32.eq
                    br_if $B75
                    local.get $l20
                    i32.load offset=24
                    local.get $l11
                    i32.eq
                    local.set $l21
                  end
                  local.get $l21
                  br_if $B73
                end
                local.get $l6
                i32.load8_u offset=713
                if $I76
                  local.get $l6
                  i32.const 1
                  i32.store8 offset=712
                  br $B73
                end
                local.get $l6
                i64.const -1082130432
                i64.store offset=660 align=4
              end
              block $B77
                local.get $l6
                i32.load8_u offset=216
                i32.eqz
                br_if $B77
                local.get $l6
                f32.load offset=660
                f32.const 0x0p+0 (;=0;)
                f32.ge
                i32.eqz
                br_if $B77
                local.get $l6
                i32.load offset=260
                i32.load offset=16
                local.tee $l13
                i32.eqz
                br_if $B77
                local.get $l6
                i32.load offset=264
                local.tee $l9
                i32.const 36
                i32.add
                local.set $l17
                local.get $l9
                i32.const 32
                i32.add
                local.set $l24
                local.get $l9
                i32.const 24
                i32.add
                local.set $l25
                local.get $l9
                i32.const 20
                i32.add
                local.set $l26
                local.get $l9
                i32.const 16
                i32.add
                local.set $l21
                f32.const 0x1p+0 (;=1;)
                local.set $l71
                block $B78 (result f32)
                  f32.const 0x1p+0 (;=1;)
                  local.get $l6
                  i32.load offset=252
                  local.tee $l20
                  i32.load offset=20
                  local.tee $l11
                  i32.eqz
                  br_if $B78
                  drop
                  f32.const 0x1p+0 (;=1;)
                  local.get $l11
                  local.get $l20
                  i32.const 20
                  i32.add
                  i32.add
                  local.tee $l20
                  i32.load offset=40
                  local.get $l20
                  i32.const 40
                  i32.add
                  i32.add
                  i32.load
                  i32.eqz
                  br_if $B78
                  drop
                  local.get $l20
                  f32.load offset=256
                end
                local.set $l56
                local.get $l9
                f32.load offset=12
                local.set $l48
                local.get $l26
                f32.load
                local.set $l41
                local.get $l21
                f32.load
                local.set $l43
                local.get $l25
                f32.load
                local.set $l45
                local.get $l9
                f32.load offset=28
                local.set $l40
                local.get $l17
                f32.load
                local.set $l64
                local.get $l24
                f32.load
                local.set $l37
                local.get $l9
                f32.load offset=8
                local.set $l38
                local.get $l9
                f32.load offset=4
                local.set $l68
                local.get $l9
                f32.load
                local.set $l72
                local.get $l5
                i32.const 88
                i32.add
                local.get $l13
                call $f68340
                local.get $l5
                local.get $l5
                f32.load offset=88
                local.tee $l58
                f32.store offset=48
                local.get $l5
                f32.load offset=96
                local.set $l55
                local.get $l5
                f32.load offset=92
                local.set $l63
                local.get $l5
                f32.load offset=100
                local.set $l47
                local.get $l5
                f32.load offset=108
                local.set $l51
                local.get $l5
                f32.load offset=104
                local.set $l46
                local.get $l5
                f32.load offset=112
                local.set $l39
                local.get $l5
                f32.load offset=124
                local.set $l66
                local.get $l5
                f32.load offset=120
                local.set $l84
                local.get $l5
                f32.load offset=116
                local.set $l78
                local.get $l6
                i32.load offset=932
                local.tee $l9
                i32.load offset=188
                i32.load
                if $I79 (result f32)
                  local.get $l5
                  i32.const 0
                  i32.store offset=40
                  local.get $l5
                  i64.const 0
                  i64.store offset=32
                  local.get $l5
                  i32.const 24
                  i32.add
                  local.tee $l13
                  i64.const 0
                  i64.store
                  local.get $l5
                  i64.const 0
                  i64.store offset=16
                  local.get $l5
                  i64.const 0
                  i64.store offset=8
                  local.get $l9
                  i32.const 0
                  i32.const 0
                  local.get $l5
                  i32.const 8
                  i32.add
                  call $f68618
                  drop
                  local.get $l13
                  f32.load
                  local.set $l71
                  local.get $l5
                  f32.load offset=20
                else
                  f32.const 0x0p+0 (;=0;)
                end
                local.set $l52
                local.get $l52
                local.get $l6
                f32.load offset=660
                f32.ge
                i32.eqz
                br_if $B77
                local.get $l38
                local.get $l43
                f32.const -0x1p+1 (;=-2;)
                f32.mul
                local.tee $l90
                local.get $l45
                f32.mul
                local.tee $l42
                local.get $l48
                local.get $l41
                f32.const -0x1p+1 (;=-2;)
                f32.mul
                local.tee $l79
                f32.mul
                f32.sub
                local.get $l40
                local.get $l56
                local.get $l58
                f32.mul
                f32.mul
                local.tee $l58
                f32.mul
                local.get $l64
                local.get $l56
                local.get $l55
                f32.mul
                f32.mul
                local.tee $l55
                f32.add
                local.get $l43
                local.get $l41
                local.get $l41
                f32.add
                local.tee $l44
                f32.mul
                local.get $l48
                f32.const -0x1p+1 (;=-2;)
                f32.mul
                local.tee $l73
                local.get $l45
                f32.mul
                local.tee $l54
                f32.sub
                local.get $l37
                local.get $l56
                local.get $l63
                f32.mul
                f32.mul
                local.tee $l63
                f32.mul
                local.get $l48
                local.get $l73
                f32.mul
                local.get $l43
                local.get $l43
                local.get $l43
                f32.add
                local.tee $l59
                f32.mul
                f32.sub
                local.get $l55
                f32.mul
                f32.add
                f32.add
                f32.add
                local.set $l91
                local.get $l68
                local.get $l63
                local.get $l48
                local.get $l59
                f32.mul
                local.get $l45
                local.get $l79
                f32.mul
                local.tee $l38
                f32.sub
                local.get $l58
                f32.mul
                f32.add
                local.get $l41
                local.get $l79
                f32.mul
                local.get $l48
                local.get $l48
                local.get $l48
                f32.add
                local.tee $l79
                f32.mul
                f32.sub
                local.get $l63
                f32.mul
                local.get $l54
                local.get $l90
                local.get $l41
                f32.mul
                f32.sub
                local.get $l55
                f32.mul
                f32.add
                f32.add
                f32.add
                local.set $l95
                local.get $l72
                local.get $l58
                local.get $l58
                local.get $l43
                local.get $l90
                f32.mul
                local.get $l41
                local.get $l44
                f32.mul
                f32.sub
                f32.mul
                f32.add
                local.get $l38
                local.get $l43
                local.get $l73
                f32.mul
                f32.sub
                local.get $l63
                f32.mul
                local.get $l79
                local.get $l41
                f32.mul
                local.get $l42
                f32.sub
                local.get $l55
                f32.mul
                f32.add
                f32.add
                f32.add
                local.set $l73
                local.get $l48
                local.get $l51
                f32.mul
                local.get $l41
                local.get $l47
                f32.mul
                f32.sub
                local.get $l45
                local.get $l46
                f32.mul
                f32.sub
                local.get $l43
                local.get $l39
                f32.mul
                f32.sub
                local.set $l58
                local.get $l41
                local.get $l46
                f32.mul
                local.get $l43
                local.get $l51
                f32.mul
                f32.sub
                local.get $l45
                local.get $l47
                f32.mul
                f32.sub
                local.get $l48
                local.get $l39
                f32.mul
                f32.sub
                local.set $l55
                local.get $l45
                local.get $l39
                f32.mul
                local.get $l48
                local.get $l47
                f32.mul
                f32.sub
                local.get $l41
                local.get $l51
                f32.mul
                f32.sub
                local.get $l43
                local.get $l46
                f32.mul
                f32.sub
                local.set $l63
                local.get $l43
                local.get $l47
                f32.mul
                local.get $l45
                local.get $l51
                f32.mul
                f32.sub
                local.get $l41
                local.get $l39
                f32.mul
                f32.sub
                local.get $l48
                local.get $l46
                f32.mul
                f32.sub
                local.set $l48
                local.get $l64
                local.get $l66
                f32.mul
                local.set $l64
                local.get $l37
                local.get $l84
                f32.mul
                local.set $l72
                local.get $l40
                local.get $l78
                f32.mul
                local.set $l68
                f32.const 0x0p+0 (;=0;)
                local.set $l38
                f32.const 0x1p+0 (;=1;)
                local.set $l51
                local.get $l6
                i32.load offset=256
                local.tee $l13
                i32.load offset=4
                local.set $l17
                local.get $l6
                i32.load offset=260
                local.tee $l24
                i32.load offset=16
                local.tee $l9
                f32.load offset=240
                local.set $l41
                local.get $l9
                f32.load offset=236
                local.set $l43
                local.get $l9
                f32.load offset=232
                local.set $l45
                local.get $l9
                f32.load offset=228
                local.set $l47
                local.get $l9
                f32.load offset=224
                local.set $l39
                local.get $l9
                f32.load offset=220
                local.set $l40
                local.get $l9
                f32.load offset=216
                local.set $l37
                local.get $l6
                i32.load8_u offset=712
                local.set $l9
                local.get $l13
                f32.load
                local.get $l71
                f32.div
                local.tee $l46
                local.get $l13
                f32.load offset=8
                local.get $l52
                local.get $l46
                f32.sub
                f32.sub
                local.tee $l46
                f32.const 0x0p+0 (;=0;)
                local.get $l46
                f32.const 0x0p+0 (;=0;)
                f32.gt
                select
                local.tee $l46
                f32.div
                f32.const 0x1p+0 (;=1;)
                local.get $l46
                f32.const 0x0p+0 (;=0;)
                f32.ne
                select
                f32.const 0x0p+0 (;=0;)
                call $f65475
                f32.const 0x1p+0 (;=1;)
                call $f65476
                local.set $l52
                block $B80
                  block $B81
                    local.get $l9
                    if $I82
                      f32.const 0x0p+0 (;=0;)
                      local.set $l44
                      f32.const 0x0p+0 (;=0;)
                      local.set $l42
                      f32.const 0x0p+0 (;=0;)
                      local.set $l54
                      f32.const 0x0p+0 (;=0;)
                      local.set $l59
                      f32.const 0x1p+0 (;=1;)
                      local.set $l46
                      block $B83
                        block $B84
                          local.get $l17
                          br_table $B80 $B84 $B83
                        end
                        local.get $l24
                        i32.load offset=24
                        local.tee $l9
                        f32.load offset=24
                        local.set $l46
                        local.get $l9
                        f32.load offset=20
                        local.set $l65
                        local.get $l9
                        f32.load offset=16
                        local.set $l59
                        local.get $l9
                        f32.load offset=12
                        local.set $l54
                        local.get $l9
                        f32.load offset=8
                        local.set $l38
                        local.get $l9
                        f32.load offset=4
                        local.set $l44
                        local.get $l9
                        f32.load
                        local.set $l42
                        br $B80
                      end
                      local.get $l39
                      local.set $l38
                      local.get $l40
                      local.set $l44
                      local.get $l37
                      local.set $l42
                      local.get $l47
                      local.set $l54
                      local.get $l45
                      local.set $l59
                      local.get $l43
                      local.set $l65
                      local.get $l41
                      local.set $l46
                      local.get $l17
                      i32.const 5
                      i32.gt_u
                      br_if $B80
                      local.get $l24
                      i32.load offset=24
                      local.get $l17
                      i32.const 2
                      i32.sub
                      local.tee $l9
                      i32.const 6
                      i32.shl
                      i32.add
                      local.tee $l13
                      f32.load offset=92
                      local.set $l41
                      local.get $l13
                      f32.load offset=88
                      local.set $l43
                      local.get $l13
                      f32.load offset=84
                      local.set $l45
                      local.get $l13
                      f32.load offset=80
                      local.set $l47
                      local.get $l13
                      f32.load offset=76
                      local.set $l39
                      local.get $l13
                      f32.load offset=72
                      local.set $l40
                      local.get $l13
                      f32.load offset=68
                      local.set $l37
                      f32.const 0x1p+0 (;=1;)
                      local.set $l52
                      br $B81
                    end
                    local.get $l52
                    local.set $l51
                    local.get $l39
                    local.set $l38
                    local.get $l40
                    local.set $l44
                    local.get $l37
                    local.set $l42
                    local.get $l47
                    local.set $l54
                    local.get $l45
                    local.set $l59
                    local.get $l43
                    local.set $l65
                    local.get $l41
                    local.set $l46
                    local.get $l17
                    i32.const 2
                    i32.sub
                    local.tee $l9
                    i32.const 3
                    i32.gt_u
                    br_if $B80
                  end
                  global.get $g0
                  i32.const -64
                  i32.add
                  local.tee $l21
                  i64.const 4554552057058557952
                  i64.store offset=56
                  local.get $l21
                  i64.const 1060439287
                  i64.store offset=40
                  local.get $l21
                  i64.const 4539628425446424576
                  i64.store offset=24
                  local.get $l21
                  i64.const 4554552057058557952
                  i64.store offset=48
                  local.get $l21
                  i64.const 1060439287
                  i64.store offset=32
                  local.get $l21
                  i64.const -4683743611408351232
                  i64.store offset=16
                  local.get $l21
                  i64.const 4539628425446424576
                  i64.store offset=8
                  local.get $l21
                  i64.const -4683743611408351232
                  i64.store
                  local.get $l5
                  i32.const 8
                  i32.add
                  local.tee $l11
                  local.get $l21
                  local.get $l9
                  i32.const 4
                  i32.shl
                  i32.add
                  local.tee $l21
                  i64.load align=4
                  i64.store align=4
                  local.get $l11
                  local.get $l21
                  i64.load offset=8 align=4
                  i64.store offset=8 align=4
                  local.get $l41
                  local.get $l5
                  f32.load offset=20
                  local.tee $l51
                  f32.mul
                  local.get $l47
                  local.get $l5
                  f32.load offset=8
                  local.tee $l46
                  f32.mul
                  f32.sub
                  local.get $l43
                  local.get $l5
                  f32.load offset=16
                  local.tee $l71
                  f32.mul
                  f32.sub
                  local.get $l45
                  local.get $l5
                  f32.load offset=12
                  local.tee $l38
                  f32.mul
                  f32.sub
                  local.tee $l66
                  f32.const 0x1p+0 (;=1;)
                  local.get $l43
                  local.get $l38
                  f32.mul
                  local.get $l45
                  local.get $l71
                  f32.mul
                  f32.sub
                  local.get $l41
                  local.get $l46
                  f32.mul
                  f32.sub
                  local.get $l47
                  local.get $l51
                  f32.mul
                  f32.sub
                  i32.reinterpret_f32
                  i32.const -2147483648
                  i32.xor
                  f32.reinterpret_i32
                  local.tee $l84
                  local.get $l84
                  f32.mul
                  local.get $l47
                  local.get $l71
                  f32.mul
                  local.get $l43
                  local.get $l46
                  f32.mul
                  f32.sub
                  local.get $l41
                  local.get $l38
                  f32.mul
                  f32.sub
                  local.get $l45
                  local.get $l51
                  f32.mul
                  f32.sub
                  i32.reinterpret_f32
                  i32.const -2147483648
                  i32.xor
                  f32.reinterpret_i32
                  local.tee $l78
                  local.get $l78
                  f32.mul
                  f32.add
                  local.get $l66
                  local.get $l66
                  f32.mul
                  local.get $l45
                  local.get $l46
                  f32.mul
                  local.get $l41
                  local.get $l71
                  f32.mul
                  f32.sub
                  local.get $l43
                  local.get $l51
                  f32.mul
                  f32.sub
                  local.get $l47
                  local.get $l38
                  f32.mul
                  f32.sub
                  i32.reinterpret_f32
                  i32.const -2147483648
                  i32.xor
                  f32.reinterpret_i32
                  local.tee $l43
                  local.get $l43
                  f32.mul
                  f32.add
                  f32.add
                  f32.sqrt
                  f32.div
                  local.tee $l41
                  f32.mul
                  local.set $l46
                  local.get $l41
                  local.get $l43
                  f32.mul
                  local.set $l65
                  local.get $l41
                  local.get $l78
                  f32.mul
                  local.set $l59
                  local.get $l41
                  local.get $l84
                  f32.mul
                  local.set $l54
                  local.get $l52
                  local.set $l51
                  local.get $l39
                  local.set $l38
                  local.get $l40
                  local.set $l44
                  local.get $l37
                  local.set $l42
                end
                local.get $l6
                f32.load offset=708
                local.set $l101
                local.get $l6
                f32.load offset=684
                local.set $l39
                local.get $l6
                f32.load offset=688
                local.set $l52
                local.get $l6
                f32.load offset=692
                local.set $l71
                local.get $l6
                f32.load offset=704
                local.set $l96
                local.get $l6
                f32.load offset=700
                local.set $l102
                local.get $l6
                f32.load offset=672
                local.set $l37
                local.get $l6
                f32.load offset=676
                local.set $l97
                local.get $l6
                f32.load offset=680
                local.set $l40
                local.get $l6
                f32.load offset=696
                local.set $l98
                local.get $l6
                f32.load offset=668
                local.set $l99
                local.get $l5
                f32.load offset=88
                local.set $l103
                local.get $l5
                f32.load offset=92
                local.set $l104
                local.get $l5
                f32.load offset=96
                local.set $l78
                local.get $l5
                f32.load offset=104
                local.set $l41
                local.get $l5
                f32.load offset=108
                local.set $l43
                local.get $l5
                f32.load offset=112
                local.set $l47
                local.get $l5
                f32.load offset=100
                local.set $l45
                local.get $l5
                f32.load offset=116
                local.set $l66
                local.get $l5
                f32.load offset=120
                local.set $l84
                local.get $l5
                local.get $l5
                f32.load offset=124
                local.tee $l79
                f32.store offset=84
                local.get $l5
                local.get $l84
                f32.store offset=80
                local.get $l5
                local.get $l66
                f32.store offset=76
                local.get $l5
                local.get $l78
                local.get $l79
                f32.const 0x1p+0 (;=1;)
                local.get $l56
                f32.div
                local.tee $l78
                f32.const 0x0p+0 (;=0;)
                f32.const 0x1p+0 (;=1;)
                local.get $l64
                f32.div
                local.get $l64
                f32.abs
                f32.const 0x1.12e0bep-30 (;=1e-09;)
                f32.lt
                select
                local.get $l63
                local.get $l58
                f32.const -0x1p+1 (;=-2;)
                f32.mul
                local.tee $l90
                f32.mul
                local.tee $l105
                local.get $l55
                local.get $l48
                f32.const -0x1p+1 (;=-2;)
                f32.mul
                local.tee $l79
                f32.mul
                f32.sub
                local.get $l99
                local.get $l73
                f32.sub
                local.tee $l56
                f32.mul
                local.get $l97
                local.get $l91
                f32.sub
                local.tee $l64
                f32.add
                local.get $l58
                local.get $l48
                local.get $l48
                f32.add
                local.tee $l91
                f32.mul
                local.get $l63
                local.get $l55
                f32.const -0x1p+1 (;=-2;)
                f32.mul
                local.tee $l73
                f32.mul
                local.tee $l97
                f32.sub
                local.get $l37
                local.get $l95
                f32.sub
                local.tee $l37
                f32.mul
                local.get $l55
                local.get $l73
                f32.mul
                local.get $l58
                local.get $l58
                local.get $l58
                f32.add
                local.tee $l95
                f32.mul
                f32.sub
                local.get $l64
                f32.mul
                f32.add
                f32.add
                f32.mul
                local.get $l38
                f32.sub
                f32.mul
                local.get $l51
                local.get $l96
                f32.mul
                f32.mul
                f32.mul
                local.tee $l38
                local.get $l66
                local.get $l51
                local.get $l98
                f32.mul
                local.get $l78
                f32.const 0x0p+0 (;=0;)
                f32.const 0x1p+0 (;=1;)
                local.get $l68
                f32.div
                local.get $l68
                f32.abs
                f32.const 0x1.12e0bep-30 (;=1e-09;)
                f32.lt
                select
                local.get $l56
                local.get $l56
                local.get $l58
                local.get $l90
                f32.mul
                local.get $l48
                local.get $l91
                f32.mul
                f32.sub
                f32.mul
                f32.add
                local.get $l63
                local.get $l79
                f32.mul
                local.tee $l91
                local.get $l58
                local.get $l73
                f32.mul
                f32.sub
                local.get $l37
                f32.mul
                local.get $l48
                local.get $l55
                local.get $l55
                f32.add
                local.tee $l96
                f32.mul
                local.get $l105
                f32.sub
                local.get $l64
                f32.mul
                f32.add
                f32.add
                f32.mul
                local.get $l42
                f32.sub
                f32.mul
                f32.mul
                f32.mul
                local.tee $l68
                local.get $l47
                local.get $l41
                f32.const -0x1p+1 (;=-2;)
                f32.mul
                local.tee $l66
                f32.mul
                local.tee $l98
                local.get $l45
                local.get $l43
                f32.const -0x1p+1 (;=-2;)
                f32.mul
                local.tee $l73
                f32.mul
                f32.sub
                f32.mul
                f32.add
                local.get $l38
                local.get $l45
                local.get $l45
                f32.const -0x1p+1 (;=-2;)
                f32.mul
                local.tee $l42
                f32.mul
                local.get $l41
                local.get $l41
                local.get $l41
                f32.add
                local.tee $l99
                f32.mul
                f32.sub
                f32.mul
                local.get $l84
                local.get $l78
                f32.const 0x0p+0 (;=0;)
                f32.const 0x1p+0 (;=1;)
                local.get $l72
                f32.div
                local.get $l72
                f32.abs
                f32.const 0x1.12e0bep-30 (;=1e-09;)
                f32.lt
                select
                local.get $l37
                local.get $l55
                local.get $l95
                f32.mul
                local.get $l91
                f32.sub
                local.get $l56
                f32.mul
                f32.add
                local.get $l48
                local.get $l79
                f32.mul
                local.get $l55
                local.get $l96
                f32.mul
                f32.sub
                local.get $l37
                f32.mul
                local.get $l97
                local.get $l48
                local.get $l90
                f32.mul
                f32.sub
                local.get $l64
                f32.mul
                f32.add
                f32.add
                f32.mul
                local.get $l44
                f32.sub
                f32.mul
                local.get $l51
                local.get $l102
                f32.mul
                f32.mul
                f32.mul
                local.tee $l56
                local.get $l41
                local.get $l43
                local.get $l43
                f32.add
                local.tee $l64
                f32.mul
                local.get $l47
                local.get $l42
                f32.mul
                local.tee $l37
                f32.sub
                f32.mul
                f32.add
                f32.add
                f32.add
                f32.store offset=56
                local.get $l5
                local.get $l104
                local.get $l56
                local.get $l68
                local.get $l45
                local.get $l99
                f32.mul
                local.get $l47
                local.get $l73
                f32.mul
                local.tee $l72
                f32.sub
                f32.mul
                f32.add
                local.get $l38
                local.get $l37
                local.get $l66
                local.get $l43
                f32.mul
                f32.sub
                f32.mul
                local.get $l56
                local.get $l43
                local.get $l73
                f32.mul
                local.get $l45
                local.get $l45
                local.get $l45
                f32.add
                local.tee $l37
                f32.mul
                f32.sub
                f32.mul
                f32.add
                f32.add
                f32.add
                f32.store offset=52
                local.get $l5
                local.get $l103
                local.get $l68
                local.get $l68
                local.get $l41
                local.get $l66
                f32.mul
                local.get $l43
                local.get $l64
                f32.mul
                f32.sub
                f32.mul
                f32.add
                local.get $l38
                local.get $l37
                local.get $l43
                f32.mul
                local.get $l98
                f32.sub
                f32.mul
                local.get $l56
                local.get $l72
                local.get $l41
                local.get $l42
                f32.mul
                f32.sub
                f32.mul
                f32.add
                f32.add
                f32.add
                f32.store offset=48
                local.get $l5
                local.get $l47
                local.get $l51
                local.get $l101
                f32.mul
                local.tee $l56
                local.get $l59
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                f32.reinterpret_i32
                local.tee $l64
                local.get $l58
                local.get $l40
                f32.mul
                local.get $l63
                local.get $l52
                f32.mul
                f32.sub
                local.get $l48
                local.get $l71
                f32.mul
                f32.sub
                local.get $l55
                local.get $l39
                f32.mul
                f32.sub
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                f32.reinterpret_i32
                local.tee $l37
                f32.mul
                local.get $l65
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                f32.reinterpret_i32
                local.tee $l38
                local.get $l55
                local.get $l52
                f32.mul
                local.get $l48
                local.get $l40
                f32.mul
                f32.sub
                local.get $l63
                local.get $l39
                f32.mul
                f32.sub
                local.get $l58
                local.get $l71
                f32.mul
                f32.sub
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                f32.reinterpret_i32
                local.tee $l68
                f32.mul
                f32.sub
                local.get $l63
                local.get $l71
                f32.mul
                local.get $l55
                local.get $l40
                f32.mul
                f32.sub
                local.get $l48
                local.get $l52
                f32.mul
                f32.sub
                local.get $l58
                local.get $l39
                f32.mul
                f32.sub
                local.tee $l72
                local.get $l54
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                f32.reinterpret_i32
                local.tee $l66
                f32.mul
                f32.sub
                local.get $l46
                local.get $l48
                local.get $l39
                f32.mul
                local.get $l58
                local.get $l52
                f32.mul
                f32.sub
                local.get $l63
                local.get $l40
                f32.mul
                f32.sub
                local.get $l55
                local.get $l71
                f32.mul
                f32.sub
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                f32.reinterpret_i32
                local.tee $l48
                f32.mul
                f32.sub
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                local.tee $l13
                f32.reinterpret_i32
                f32.const 0x0p+0 (;=0;)
                f32.mul
                local.get $l38
                local.get $l48
                f32.mul
                local.get $l66
                local.get $l37
                f32.mul
                f32.sub
                local.get $l72
                local.get $l64
                f32.mul
                f32.sub
                local.get $l46
                local.get $l68
                f32.mul
                f32.sub
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                local.tee $l17
                f32.reinterpret_i32
                f32.const 0x0p+0 (;=0;)
                f32.mul
                f32.add
                local.get $l46
                local.get $l72
                f32.mul
                local.get $l66
                local.get $l48
                f32.mul
                f32.sub
                local.get $l38
                local.get $l37
                f32.mul
                f32.sub
                local.get $l64
                local.get $l68
                f32.mul
                f32.sub
                local.tee $l58
                local.get $l66
                local.get $l68
                f32.mul
                local.get $l72
                local.get $l38
                f32.mul
                f32.sub
                local.get $l46
                local.get $l37
                f32.mul
                f32.sub
                local.get $l64
                local.get $l48
                f32.mul
                f32.sub
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                local.tee $l24
                f32.reinterpret_i32
                f32.const 0x0p+0 (;=0;)
                f32.mul
                f32.add
                f32.add
                i32.reinterpret_f32
                i32.const -2147483648
                i32.and
                local.tee $l9
                local.get $l58
                i32.reinterpret_f32
                i32.xor
                f32.reinterpret_i32
                f32.const -0x1p+0 (;=-1;)
                f32.add
                f32.mul
                f32.const 0x1p+0 (;=1;)
                f32.add
                local.tee $l48
                f32.const 0x1p+0 (;=1;)
                local.get $l56
                local.get $l9
                local.get $l13
                i32.xor
                f32.reinterpret_i32
                f32.mul
                f32.const 0x0p+0 (;=0;)
                f32.add
                local.tee $l55
                local.get $l55
                f32.mul
                local.get $l56
                local.get $l9
                local.get $l17
                i32.xor
                f32.reinterpret_i32
                f32.mul
                f32.const 0x0p+0 (;=0;)
                f32.add
                local.tee $l63
                local.get $l63
                f32.mul
                f32.add
                local.get $l56
                local.get $l9
                local.get $l24
                i32.xor
                f32.reinterpret_i32
                f32.mul
                f32.const 0x0p+0 (;=0;)
                f32.add
                local.tee $l56
                local.get $l56
                f32.mul
                local.get $l48
                local.get $l48
                f32.mul
                f32.add
                f32.add
                f32.sqrt
                f32.div
                local.tee $l48
                f32.mul
                local.tee $l58
                f32.mul
                local.get $l45
                local.get $l55
                local.get $l48
                f32.mul
                local.tee $l55
                f32.mul
                f32.sub
                local.get $l43
                local.get $l56
                local.get $l48
                f32.mul
                local.tee $l56
                f32.mul
                f32.sub
                local.get $l41
                local.get $l63
                local.get $l48
                f32.mul
                local.tee $l48
                f32.mul
                f32.sub
                f32.store offset=72
                local.get $l5
                local.get $l41
                local.get $l55
                f32.mul
                local.get $l47
                local.get $l56
                f32.mul
                f32.sub
                local.get $l43
                local.get $l58
                f32.mul
                f32.sub
                local.get $l45
                local.get $l48
                f32.mul
                f32.sub
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                i32.store offset=68
                local.get $l5
                local.get $l45
                local.get $l56
                f32.mul
                local.get $l43
                local.get $l55
                f32.mul
                f32.sub
                local.get $l47
                local.get $l48
                f32.mul
                f32.sub
                local.get $l41
                local.get $l58
                f32.mul
                f32.sub
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                i32.store offset=64
                local.get $l5
                local.get $l43
                local.get $l48
                f32.mul
                local.get $l41
                local.get $l56
                f32.mul
                f32.sub
                local.get $l47
                local.get $l55
                f32.mul
                f32.sub
                local.get $l45
                local.get $l58
                f32.mul
                f32.sub
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                i32.store offset=60
                local.get $l5
                i32.const 48
                i32.add
                local.tee $l21
                i64.load align=4
                local.set $l107
                local.get $l6
                i32.load offset=260
                i32.load offset=16
                local.tee $l11
                local.get $l21
                f32.load offset=8
                f32.store offset=12
                local.get $l11
                local.get $l107
                i64.store offset=4 align=4
                local.get $l21
                i64.load offset=12 align=4
                local.set $l107
                local.get $l11
                local.get $l21
                i64.load offset=20 align=4
                i64.store offset=24 align=4
                local.get $l11
                local.get $l107
                i64.store offset=16 align=4
                local.get $l51
                f32.const 0x1p+0 (;=1;)
                f32.ge
                i32.eqz
                br_if $B77
                local.get $l6
                i64.const -1082130432
                i64.store offset=660 align=4
              end
              local.get $l5
              i32.const 128
              i32.add
              global.set $g0
              local.get $l6
              i32.const 0
              i32.store8 offset=712
              local.get $l4
              i32.load offset=56
              local.tee $l9
              i32.load offset=12
              local.set $l5
              local.get $l18
              i32.const 16
              i32.add
              local.tee $l13
              local.get $l9
              i32.load offset=8
              i32.load offset=16
              local.tee $l9
              i64.load offset=4 align=4
              i64.store align=4
              local.get $l13
              local.get $l9
              i32.load offset=12
              i32.store offset=8
              local.get $l6
              local.get $l62
              local.get $l18
              f32.load offset=24
              local.get $l4
              i32.load offset=56
              i32.load offset=12
              local.tee $l9
              f32.load offset=36
              f32.mul
              f32.mul
              local.tee $l40
              local.get $l62
              local.get $l18
              f32.load offset=16
              local.get $l9
              f32.load offset=28
              f32.mul
              f32.mul
              local.tee $l42
              local.get $l5
              f32.load offset=16
              local.tee $l37
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l45
              local.get $l5
              f32.load offset=24
              local.tee $l44
              f32.mul
              local.tee $l47
              local.get $l5
              f32.load offset=12
              local.tee $l38
              local.get $l5
              f32.load offset=20
              local.tee $l39
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l41
              f32.mul
              f32.sub
              f32.mul
              f32.add
              local.get $l40
              local.get $l38
              local.get $l38
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l46
              f32.mul
              local.get $l37
              local.get $l37
              local.get $l37
              f32.add
              local.tee $l51
              f32.mul
              f32.sub
              f32.mul
              local.get $l62
              local.get $l18
              f32.load offset=20
              local.get $l9
              f32.load offset=32
              f32.mul
              f32.mul
              local.tee $l43
              local.get $l37
              local.get $l39
              local.get $l39
              f32.add
              local.tee $l52
              f32.mul
              local.get $l44
              local.get $l46
              f32.mul
              local.tee $l54
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.store offset=576
              local.get $l6
              local.get $l43
              local.get $l42
              local.get $l38
              local.get $l51
              f32.mul
              local.get $l44
              local.get $l41
              f32.mul
              local.tee $l44
              f32.sub
              f32.mul
              f32.add
              local.get $l40
              local.get $l54
              local.get $l45
              local.get $l39
              f32.mul
              f32.sub
              f32.mul
              local.get $l43
              local.get $l39
              local.get $l41
              f32.mul
              local.get $l38
              local.get $l38
              local.get $l38
              f32.add
              local.tee $l41
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.store offset=572
              local.get $l6
              local.get $l42
              local.get $l42
              local.get $l37
              local.get $l45
              f32.mul
              local.get $l39
              local.get $l52
              f32.mul
              f32.sub
              f32.mul
              f32.add
              local.get $l40
              local.get $l41
              local.get $l39
              f32.mul
              local.get $l47
              f32.sub
              f32.mul
              local.get $l43
              local.get $l44
              local.get $l37
              local.get $l46
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.store offset=568
              local.get $l18
              i32.const 16
              i32.add
              local.tee $l5
              local.get $l4
              i32.load offset=56
              i32.load offset=8
              i32.load offset=16
              local.tee $l9
              i64.load offset=16 align=4
              i64.store align=4
              local.get $l5
              local.get $l9
              i64.load offset=24 align=4
              i64.store offset=8 align=4
              local.get $l6
              local.get $l18
              f32.load offset=28
              local.tee $l37
              local.get $l18
              f32.load offset=16
              local.tee $l38
              local.get $l38
              f32.mul
              local.get $l18
              f32.load offset=20
              local.tee $l39
              local.get $l39
              f32.mul
              f32.add
              local.get $l18
              f32.load offset=24
              local.tee $l40
              local.get $l40
              f32.mul
              local.get $l37
              local.get $l37
              f32.mul
              f32.add
              f32.add
              local.tee $l42
              f32.sqrt
              local.tee $l37
              f32.div
              f32.const 0x1p+0 (;=1;)
              local.get $l42
              f32.const 0x1.4484cp-100 (;=1e-30;)
              f32.gt
              local.tee $l5
              select
              f32.store offset=592
              local.get $l6
              local.get $l40
              local.get $l37
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l5
              select
              f32.store offset=588
              local.get $l6
              local.get $l39
              local.get $l37
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l5
              select
              f32.store offset=584
              local.get $l6
              local.get $l38
              local.get $l37
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l5
              select
              f32.store offset=580
              local.get $l4
              i32.load offset=56
              local.tee $l9
              i32.load offset=12
              local.set $l5
              local.get $l9
              i32.load offset=8
              i32.load offset=16
              local.tee $l9
              f32.load offset=8
              local.set $l38
              local.get $l9
              f32.load offset=12
              local.set $l39
              local.get $l18
              i32.const 16
              i32.add
              local.tee $l13
              local.get $l9
              f32.load offset=4
              local.get $l9
              f32.load
              local.tee $l37
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l37
              f32.const 0x0p+0 (;=0;)
              f32.ne
              local.tee $l9
              select
              f32.store
              local.get $l13
              local.get $l39
              local.get $l37
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l9
              select
              f32.store offset=8
              local.get $l13
              local.get $l38
              local.get $l37
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l9
              select
              f32.store offset=4
              local.get $l6
              local.get $l62
              local.get $l18
              f32.load offset=24
              local.get $l4
              i32.load offset=56
              i32.load offset=12
              local.tee $l9
              f32.load offset=36
              f32.mul
              f32.mul
              local.tee $l40
              local.get $l62
              local.get $l18
              f32.load offset=16
              local.get $l9
              f32.load offset=28
              f32.mul
              f32.mul
              local.tee $l42
              local.get $l5
              f32.load offset=16
              local.tee $l37
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l45
              local.get $l5
              f32.load offset=24
              local.tee $l44
              f32.mul
              local.tee $l47
              local.get $l5
              f32.load offset=12
              local.tee $l38
              local.get $l5
              f32.load offset=20
              local.tee $l39
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l41
              f32.mul
              f32.sub
              f32.mul
              f32.add
              local.get $l40
              local.get $l38
              local.get $l38
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l46
              f32.mul
              local.get $l37
              local.get $l37
              local.get $l37
              f32.add
              local.tee $l51
              f32.mul
              f32.sub
              f32.mul
              local.get $l62
              local.get $l18
              f32.load offset=20
              local.get $l9
              f32.load offset=32
              f32.mul
              f32.mul
              local.tee $l43
              local.get $l37
              local.get $l39
              local.get $l39
              f32.add
              local.tee $l52
              f32.mul
              local.get $l44
              local.get $l46
              f32.mul
              local.tee $l54
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.store offset=604
              local.get $l6
              local.get $l43
              local.get $l42
              local.get $l38
              local.get $l51
              f32.mul
              local.get $l44
              local.get $l41
              f32.mul
              local.tee $l44
              f32.sub
              f32.mul
              f32.add
              local.get $l40
              local.get $l54
              local.get $l45
              local.get $l39
              f32.mul
              f32.sub
              f32.mul
              local.get $l43
              local.get $l39
              local.get $l41
              f32.mul
              local.get $l38
              local.get $l38
              local.get $l38
              f32.add
              local.tee $l41
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.store offset=600
              local.get $l6
              local.get $l42
              local.get $l42
              local.get $l37
              local.get $l45
              f32.mul
              local.get $l39
              local.get $l52
              f32.mul
              f32.sub
              f32.mul
              f32.add
              local.get $l40
              local.get $l41
              local.get $l39
              f32.mul
              local.get $l47
              f32.sub
              f32.mul
              local.get $l43
              local.get $l44
              local.get $l37
              local.get $l46
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.store offset=596
              local.get $l4
              i32.load offset=56
              local.tee $l9
              i32.load offset=12
              local.set $l5
              local.get $l18
              i32.const 16
              i32.add
              local.tee $l13
              f32.const 0x0p+0 (;=0;)
              local.get $l9
              i32.load offset=8
              i32.load offset=16
              local.tee $l9
              f32.load offset=16
              local.tee $l37
              f32.const 0x1p+0 (;=1;)
              local.get $l37
              local.get $l37
              f32.mul
              local.get $l9
              f32.load offset=20
              local.tee $l37
              local.get $l37
              f32.mul
              f32.add
              local.get $l9
              f32.load offset=24
              local.tee $l38
              local.get $l38
              f32.mul
              local.get $l9
              f32.load offset=28
              local.tee $l39
              local.get $l39
              f32.mul
              f32.add
              f32.add
              f32.sqrt
              f32.div
              local.tee $l39
              f32.mul
              local.tee $l40
              local.get $l40
              f32.mul
              local.get $l37
              local.get $l39
              f32.mul
              local.tee $l42
              local.get $l42
              f32.mul
              f32.add
              local.get $l38
              local.get $l39
              f32.mul
              local.tee $l38
              local.get $l38
              f32.mul
              f32.const 0x0p+0 (;=0;)
              f32.add
              f32.add
              f32.sqrt
              local.tee $l37
              call $f65711
              local.tee $l39
              local.get $l39
              f32.add
              local.tee $l39
              local.get $l38
              f32.mul
              local.get $l37
              f32.div
              local.get $l37
              f32.const 0x0p+0 (;=0;)
              f32.eq
              local.tee $l17
              select
              local.get $l9
              f32.load
              local.tee $l38
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l38
              f32.const 0x0p+0 (;=0;)
              f32.ne
              local.tee $l9
              select
              f32.store offset=8
              local.get $l13
              f32.const 0x0p+0 (;=0;)
              local.get $l39
              local.get $l42
              f32.mul
              local.get $l37
              f32.div
              local.get $l17
              select
              local.get $l38
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l9
              select
              f32.store offset=4
              local.get $l13
              f32.const 0x0p+0 (;=0;)
              local.get $l39
              local.get $l40
              f32.mul
              local.get $l37
              f32.div
              local.get $l17
              select
              local.get $l38
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l9
              select
              f32.store
              local.get $l6
              local.get $l18
              f32.load offset=24
              local.tee $l40
              local.get $l18
              f32.load offset=16
              local.tee $l42
              local.get $l5
              f32.load offset=16
              local.tee $l37
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l45
              local.get $l5
              f32.load offset=24
              local.tee $l44
              f32.mul
              local.tee $l47
              local.get $l5
              f32.load offset=12
              local.tee $l38
              local.get $l5
              f32.load offset=20
              local.tee $l39
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l41
              f32.mul
              f32.sub
              f32.mul
              f32.add
              local.get $l18
              f32.load offset=20
              local.tee $l43
              local.get $l37
              local.get $l39
              local.get $l39
              f32.add
              local.tee $l51
              f32.mul
              local.get $l44
              local.get $l38
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l46
              f32.mul
              local.tee $l52
              f32.sub
              f32.mul
              local.get $l38
              local.get $l46
              f32.mul
              local.get $l37
              local.get $l37
              local.get $l37
              f32.add
              local.tee $l54
              f32.mul
              f32.sub
              local.get $l40
              f32.mul
              f32.add
              f32.add
              f32.store offset=616
              local.get $l6
              local.get $l43
              local.get $l42
              local.get $l38
              local.get $l54
              f32.mul
              local.get $l44
              local.get $l41
              f32.mul
              local.tee $l44
              f32.sub
              f32.mul
              f32.add
              local.get $l43
              local.get $l39
              local.get $l41
              f32.mul
              local.get $l38
              local.get $l38
              local.get $l38
              f32.add
              local.tee $l41
              f32.mul
              f32.sub
              f32.mul
              local.get $l40
              local.get $l52
              local.get $l45
              local.get $l39
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.store offset=612
              local.get $l6
              local.get $l42
              local.get $l42
              local.get $l37
              local.get $l45
              f32.mul
              local.get $l39
              local.get $l51
              f32.mul
              f32.sub
              f32.mul
              f32.add
              local.get $l43
              local.get $l44
              local.get $l37
              local.get $l46
              f32.mul
              f32.sub
              f32.mul
              local.get $l40
              local.get $l41
              local.get $l39
              f32.mul
              local.get $l47
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.store offset=608
              local.get $l4
              i32.load offset=56
              local.tee $l5
              i32.load
              local.set $l17
              local.get $l5
              i32.load offset=4
              drop
              local.get $l5
              i32.load offset=8
              local.set $l24
              local.get $l5
              i32.load offset=12
              local.set $l9
              local.get $l5
              i32.load offset=16
              drop
              global.get $g0
              i32.const 48
              i32.sub
              local.tee $l5
              global.set $g0
              block $B85
                local.get $l17
                i32.load offset=20
                local.tee $l13
                i32.eqz
                if $I86
                  local.get $l5
                  i32.const 8
                  i32.add
                  local.get $l24
                  i32.load offset=16
                  call $f68340
                  br $B85
                end
                local.get $l13
                local.get $l17
                i32.const 20
                i32.add
                local.tee $l17
                i32.add
                local.tee $l13
                i32.load offset=40
                local.get $l13
                i32.const 40
                i32.add
                i32.add
                i32.load
                local.set $l13
                local.get $l5
                i32.const 8
                i32.add
                local.get $l24
                i32.load offset=16
                call $f68340
                local.get $l13
                i32.eqz
                br_if $B85
                local.get $l5
                local.get $l17
                i32.load
                local.get $l17
                i32.add
                f32.load offset=256
                local.tee $l37
                local.get $l5
                f32.load offset=16
                f32.mul
                f32.store offset=16
                local.get $l5
                local.get $l37
                local.get $l5
                f32.load offset=12
                f32.mul
                f32.store offset=12
                local.get $l5
                local.get $l37
                local.get $l5
                f32.load offset=8
                f32.mul
                f32.store offset=8
              end
              local.get $l9
              i32.const 16
              i32.add
              local.tee $l17
              f32.load
              local.set $l37
              local.get $l9
              i32.const 20
              i32.add
              local.tee $l24
              f32.load
              local.set $l38
              local.get $l9
              i32.const 24
              i32.add
              local.tee $l13
              f32.load
              local.set $l40
              local.get $l9
              i32.const 32
              i32.add
              local.tee $l20
              f32.load
              local.set $l46
              local.get $l9
              i32.const 36
              i32.add
              local.tee $l25
              f32.load
              local.set $l43
              local.get $l9
              f32.load
              local.set $l59
              local.get $l9
              f32.load offset=4
              local.set $l65
              local.get $l9
              f32.load offset=8
              local.set $l48
              local.get $l5
              f32.load offset=24
              local.set $l42
              local.get $l5
              f32.load offset=28
              local.set $l44
              local.get $l5
              f32.load offset=32
              local.set $l41
              local.get $l9
              f32.load offset=12
              local.set $l39
              local.get $l5
              f32.load offset=40
              local.set $l47
              local.get $l5
              f32.load offset=44
              local.set $l51
              local.get $l5
              f32.load offset=8
              local.set $l52
              local.get $l5
              f32.load offset=16
              local.set $l54
              local.get $l5
              f32.load offset=12
              local.set $l55
              local.get $l5
              f32.load offset=20
              local.set $l45
              local.get $l9
              local.get $l9
              f32.load offset=28
              local.tee $l56
              local.get $l5
              f32.load offset=36
              f32.mul
              f32.store offset=28
              local.get $l25
              local.get $l43
              local.get $l51
              f32.mul
              f32.store
              local.get $l20
              local.get $l46
              local.get $l47
              f32.mul
              f32.store
              local.get $l13
              local.get $l40
              local.get $l41
              f32.mul
              local.get $l39
              local.get $l45
              f32.mul
              f32.sub
              local.get $l38
              local.get $l44
              f32.mul
              f32.sub
              local.get $l37
              local.get $l42
              f32.mul
              f32.sub
              f32.store
              local.get $l24
              local.get $l37
              local.get $l45
              f32.mul
              local.get $l40
              local.get $l44
              f32.mul
              f32.sub
              local.get $l38
              local.get $l41
              f32.mul
              f32.sub
              local.get $l39
              local.get $l42
              f32.mul
              f32.sub
              i32.reinterpret_f32
              i32.const -2147483648
              i32.xor
              i32.store
              local.get $l17
              local.get $l39
              local.get $l44
              f32.mul
              local.get $l38
              local.get $l45
              f32.mul
              f32.sub
              local.get $l40
              local.get $l42
              f32.mul
              f32.sub
              local.get $l37
              local.get $l41
              f32.mul
              f32.sub
              i32.reinterpret_f32
              i32.const -2147483648
              i32.xor
              i32.store
              local.get $l9
              local.get $l38
              local.get $l42
              f32.mul
              local.get $l37
              local.get $l44
              f32.mul
              f32.sub
              local.get $l40
              local.get $l45
              f32.mul
              f32.sub
              local.get $l39
              local.get $l41
              f32.mul
              f32.sub
              i32.reinterpret_f32
              i32.const -2147483648
              i32.xor
              i32.store offset=12
              local.get $l9
              local.get $l48
              local.get $l54
              local.get $l43
              f32.mul
              local.tee $l42
              local.get $l52
              local.get $l56
              f32.mul
              local.tee $l44
              local.get $l40
              local.get $l37
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l45
              f32.mul
              local.tee $l51
              local.get $l39
              local.get $l38
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l43
              f32.mul
              f32.sub
              f32.mul
              f32.add
              local.get $l42
              local.get $l39
              local.get $l39
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l47
              f32.mul
              local.get $l37
              local.get $l37
              local.get $l37
              f32.add
              local.tee $l52
              f32.mul
              f32.sub
              f32.mul
              local.get $l55
              local.get $l46
              f32.mul
              local.tee $l41
              local.get $l37
              local.get $l38
              local.get $l38
              f32.add
              local.tee $l46
              f32.mul
              local.get $l40
              local.get $l47
              f32.mul
              local.tee $l54
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.add
              f32.store offset=8
              local.get $l9
              local.get $l65
              local.get $l41
              local.get $l44
              local.get $l39
              local.get $l52
              f32.mul
              local.get $l40
              local.get $l43
              f32.mul
              local.tee $l40
              f32.sub
              f32.mul
              f32.add
              local.get $l42
              local.get $l54
              local.get $l45
              local.get $l38
              f32.mul
              f32.sub
              f32.mul
              local.get $l41
              local.get $l38
              local.get $l43
              f32.mul
              local.get $l39
              local.get $l39
              local.get $l39
              f32.add
              local.tee $l43
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.add
              f32.store offset=4
              local.get $l9
              local.get $l59
              local.get $l44
              local.get $l44
              local.get $l37
              local.get $l45
              f32.mul
              local.get $l38
              local.get $l46
              f32.mul
              f32.sub
              f32.mul
              f32.add
              local.get $l42
              local.get $l43
              local.get $l38
              f32.mul
              local.get $l51
              f32.sub
              f32.mul
              local.get $l41
              local.get $l40
              local.get $l37
              local.get $l47
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.add
              f32.store
              local.get $l5
              i32.const 48
              i32.add
              global.set $g0
              local.get $l4
              i32.load offset=56
              local.tee $l9
              i32.load offset=12
              local.tee $l5
              f32.load
              local.set $l47
              local.get $l5
              f32.load offset=4
              local.set $l51
              local.get $l6
              local.get $l5
              f32.load offset=8
              local.get $l9
              i32.load offset=8
              i32.load offset=16
              local.tee $l9
              f32.load offset=224
              local.get $l5
              f32.load offset=36
              f32.mul
              local.tee $l40
              local.get $l9
              f32.load offset=216
              local.get $l5
              f32.load offset=28
              f32.mul
              local.tee $l42
              local.get $l5
              f32.load offset=16
              local.tee $l37
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l45
              local.get $l5
              f32.load offset=24
              local.tee $l44
              f32.mul
              local.tee $l52
              local.get $l5
              f32.load offset=12
              local.tee $l38
              local.get $l5
              f32.load offset=20
              local.tee $l39
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l41
              f32.mul
              f32.sub
              f32.mul
              f32.add
              local.get $l40
              local.get $l38
              local.get $l38
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l46
              f32.mul
              local.get $l37
              local.get $l37
              local.get $l37
              f32.add
              local.tee $l54
              f32.mul
              f32.sub
              f32.mul
              local.get $l9
              f32.load offset=220
              local.get $l5
              f32.load offset=32
              f32.mul
              local.tee $l43
              local.get $l37
              local.get $l39
              local.get $l39
              f32.add
              local.tee $l59
              f32.mul
              local.get $l44
              local.get $l46
              f32.mul
              local.tee $l65
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.add
              f32.store offset=640
              local.get $l6
              local.get $l51
              local.get $l43
              local.get $l42
              local.get $l38
              local.get $l54
              f32.mul
              local.get $l44
              local.get $l41
              f32.mul
              local.tee $l44
              f32.sub
              f32.mul
              f32.add
              local.get $l40
              local.get $l65
              local.get $l45
              local.get $l39
              f32.mul
              f32.sub
              f32.mul
              local.get $l43
              local.get $l39
              local.get $l41
              f32.mul
              local.get $l38
              local.get $l38
              local.get $l38
              f32.add
              local.tee $l41
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.add
              f32.store offset=636
              local.get $l6
              local.get $l47
              local.get $l42
              local.get $l42
              local.get $l37
              local.get $l45
              f32.mul
              local.get $l39
              local.get $l59
              f32.mul
              f32.sub
              f32.mul
              f32.add
              local.get $l40
              local.get $l41
              local.get $l39
              f32.mul
              local.get $l52
              f32.sub
              f32.mul
              local.get $l43
              local.get $l44
              local.get $l37
              local.get $l46
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.add
              f32.store offset=632
              local.get $l6
              local.get $l4
              i32.load offset=56
              local.tee $l9
              i32.load offset=12
              local.tee $l5
              f32.load offset=24
              local.tee $l37
              local.get $l9
              i32.load offset=8
              i32.load offset=16
              local.tee $l9
              f32.load offset=240
              local.tee $l38
              f32.mul
              local.get $l9
              f32.load offset=228
              local.tee $l39
              local.get $l5
              f32.load offset=12
              local.tee $l40
              f32.mul
              f32.sub
              local.get $l5
              f32.load offset=20
              local.tee $l42
              local.get $l9
              f32.load offset=236
              local.tee $l43
              f32.mul
              f32.sub
              local.get $l5
              f32.load offset=16
              local.tee $l45
              local.get $l9
              f32.load offset=232
              local.tee $l44
              f32.mul
              f32.sub
              local.tee $l41
              f32.const 0x1p+0 (;=1;)
              local.get $l42
              local.get $l44
              f32.mul
              local.get $l45
              local.get $l43
              f32.mul
              f32.sub
              local.get $l39
              local.get $l37
              f32.mul
              f32.sub
              local.get $l38
              local.get $l40
              f32.mul
              f32.sub
              i32.reinterpret_f32
              i32.const -2147483648
              i32.xor
              f32.reinterpret_i32
              local.tee $l46
              local.get $l46
              f32.mul
              local.get $l40
              local.get $l43
              f32.mul
              local.get $l39
              local.get $l42
              f32.mul
              f32.sub
              local.get $l37
              local.get $l44
              f32.mul
              f32.sub
              local.get $l45
              local.get $l38
              f32.mul
              f32.sub
              i32.reinterpret_f32
              i32.const -2147483648
              i32.xor
              f32.reinterpret_i32
              local.tee $l47
              local.get $l47
              f32.mul
              f32.add
              local.get $l41
              local.get $l41
              f32.mul
              local.get $l45
              local.get $l39
              f32.mul
              local.get $l37
              local.get $l43
              f32.mul
              f32.sub
              local.get $l38
              local.get $l42
              f32.mul
              f32.sub
              local.get $l44
              local.get $l40
              f32.mul
              f32.sub
              i32.reinterpret_f32
              i32.const -2147483648
              i32.xor
              f32.reinterpret_i32
              local.tee $l38
              local.get $l38
              f32.mul
              f32.add
              f32.add
              f32.sqrt
              f32.div
              local.tee $l37
              f32.mul
              local.tee $l39
              local.get $l37
              local.get $l46
              f32.mul
              local.tee $l40
              local.get $l40
              f32.mul
              local.get $l37
              local.get $l47
              f32.mul
              local.tee $l42
              local.get $l42
              f32.mul
              f32.add
              local.get $l37
              local.get $l38
              f32.mul
              local.tee $l38
              local.get $l38
              f32.mul
              local.get $l39
              local.get $l39
              f32.mul
              f32.add
              f32.add
              local.tee $l39
              f32.sqrt
              local.tee $l37
              f32.div
              f32.const 0x1p+0 (;=1;)
              local.get $l39
              f32.const 0x1.4484cp-100 (;=1e-30;)
              f32.gt
              local.tee $l5
              select
              f32.store offset=656
              local.get $l6
              local.get $l38
              local.get $l37
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l5
              select
              f32.store offset=652
              local.get $l6
              local.get $l42
              local.get $l37
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l5
              select
              f32.store offset=648
              local.get $l6
              local.get $l40
              local.get $l37
              f32.div
              f32.const 0x0p+0 (;=0;)
              local.get $l5
              select
              f32.store offset=644
              local.get $l4
              i32.load offset=56
              i32.load offset=12
              local.tee $l4
              f32.load
              local.set $l46
              local.get $l4
              f32.load offset=4
              local.set $l47
              local.get $l6
              local.get $l4
              f32.load offset=8
              local.get $l62
              local.get $l4
              f32.load offset=128
              f32.mul
              local.get $l4
              f32.load offset=36
              f32.mul
              local.tee $l40
              local.get $l62
              local.get $l4
              f32.load offset=120
              f32.mul
              local.get $l4
              f32.load offset=28
              f32.mul
              local.tee $l42
              local.get $l4
              f32.load offset=16
              local.tee $l37
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l43
              local.get $l4
              f32.load offset=24
              local.tee $l45
              f32.mul
              local.tee $l51
              local.get $l4
              f32.load offset=12
              local.tee $l38
              local.get $l4
              f32.load offset=20
              local.tee $l39
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l44
              f32.mul
              f32.sub
              f32.mul
              f32.add
              local.get $l40
              local.get $l38
              local.get $l38
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l41
              f32.mul
              local.get $l37
              local.get $l37
              local.get $l37
              f32.add
              local.tee $l52
              f32.mul
              f32.sub
              f32.mul
              local.get $l62
              local.get $l4
              f32.load offset=124
              f32.mul
              local.get $l4
              f32.load offset=32
              f32.mul
              local.tee $l62
              local.get $l37
              local.get $l39
              local.get $l39
              f32.add
              local.tee $l54
              f32.mul
              local.get $l45
              local.get $l41
              f32.mul
              local.tee $l59
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.add
              f32.store offset=628
              local.get $l6
              local.get $l47
              local.get $l62
              local.get $l42
              local.get $l38
              local.get $l52
              f32.mul
              local.get $l45
              local.get $l44
              f32.mul
              local.tee $l45
              f32.sub
              f32.mul
              f32.add
              local.get $l40
              local.get $l59
              local.get $l43
              local.get $l39
              f32.mul
              f32.sub
              f32.mul
              local.get $l62
              local.get $l39
              local.get $l44
              f32.mul
              local.get $l38
              local.get $l38
              local.get $l38
              f32.add
              local.tee $l44
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.add
              f32.store offset=624
              local.get $l6
              local.get $l46
              local.get $l42
              local.get $l42
              local.get $l37
              local.get $l43
              f32.mul
              local.get $l39
              local.get $l54
              f32.mul
              f32.sub
              f32.mul
              f32.add
              local.get $l40
              local.get $l44
              local.get $l39
              f32.mul
              local.get $l51
              f32.sub
              f32.mul
              local.get $l62
              local.get $l45
              local.get $l37
              local.get $l41
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.add
              f32.store offset=620
            end
            local.get $l18
            i32.const 80
            i32.add
            global.set $g0
            local.get $l16
            i32.load
            i32.load8_u offset=228
            i32.const 8
            i32.and
            br_if $B59
            local.get $l7
            local.get $l8
            i32.const 72
            i32.mul
            i32.add
            local.tee $l4
            i32.const 32
            i32.add
            local.tee $l6
            i32.load
            local.tee $l8
            i32.eqz
            br_if $B59
            local.get $l4
            i32.const 40
            i32.add
            local.set $l16
            local.get $l4
            i32.const 24
            i32.add
            local.tee $l5
            i32.load
            local.tee $l11
            local.set $l4
            loop $L87
              block $B88
                local.get $l4
                i32.load offset=8
                local.tee $l7
                i32.eqz
                br_if $B88
                local.get $l7
                i32.load offset=16
                local.get $l4
                i32.load offset=12
                i32.const -2
                i32.and
                i32.ne
                br_if $B88
                local.get $l7
                i32.load offset=20
                local.tee $l7
                i32.eqz
                br_if $B88
                local.get $l7
                f32.const 0x1p+0 (;=1;)
                local.get $l16
                local.get $l7
                i32.load
                i32.load offset=80
                call_indirect $__indirect_function_table (type $t17)
                local.get $l6
                i32.load
                local.set $l8
                local.get $l5
                i32.load
                local.set $l11
              end
              local.get $l4
              i32.const 20
              i32.add
              local.tee $l4
              local.get $l11
              local.get $l8
              i32.const 20
              i32.mul
              i32.add
              i32.ne
              br_if $L87
            end
          end
          local.get $l19
          i32.const 16
          i32.add
          global.set $g0
          local.get $p1
          i32.const 1
          i32.add
          local.tee $p1
          local.get $l10
          i32.ne
          br_if $L58
        end
      end
      i32.const 4782136
      i32.load
      i32.const 1
      i32.or
      call $f80130
      local.set $l14
      local.get $l12
      i32.load offset=88
      if $I89
        i32.const 0
        local.set $p1
        loop $L90
          local.get $l12
          i32.load offset=80
          local.get $p1
          i32.const 72
          i32.mul
          i32.add
          local.set $l10
          block $B91
            local.get $l12
            i32.load offset=64
            local.get $p1
            i32.add
            i32.load8_u
            i32.eqz
            br_if $B91
            local.get $l10
            i32.load offset=56
            i32.load8_u offset=29
            i32.eqz
            br_if $B91
            local.get $l10
            i32.load offset=60
            i32.load
            i32.eqz
            br_if $B91
            local.get $l10
            i32.load offset=16
            local.tee $l8
            i32.load offset=228
            local.tee $l7
            i32.const 8
            i32.and
            i32.eqz
            if $I92
              local.get $l8
              local.get $l7
              i32.const 8
              i32.or
              i32.store offset=228
              block $B93
                local.get $l8
                i32.load8_u offset=725
                i32.eqz
                br_if $B93
                local.get $l10
                i32.load offset=48
                local.tee $l4
                i32.eqz
                br_if $B93
                local.get $l10
                i32.load offset=40
                local.tee $l6
                local.set $l7
                loop $L94
                  block $B95
                    local.get $l10
                    i32.load offset=56
                    i32.load8_u offset=29
                    i32.eqz
                    br_if $B95
                    local.get $l10
                    i32.load offset=60
                    i32.load
                    i32.eqz
                    br_if $B95
                    local.get $l7
                    i32.load
                    local.set $l19
                    i32.const 0
                    local.set $l9
                    local.get $l7
                    local.tee $l6
                    i32.load offset=56
                    local.set $l4
                    local.get $l6
                    f32.load offset=4
                    local.set $l37
                    local.get $l6
                    f32.load offset=8
                    local.set $l40
                    block $B96 (result i32)
                      local.get $l6
                      i32.load8_u offset=61
                      if $I97
                        local.get $l6
                        i32.load8_u offset=62
                        i32.const 0
                        i32.ne
                        br $B96
                      end
                      local.get $l19
                      local.get $l19
                      i32.load
                      i32.load offset=104
                      call_indirect $__indirect_function_table (type $t5)
                    end
                    local.set $l16
                    block $B98
                      local.get $l37
                      local.get $l40
                      f32.eq
                      br_if $B98
                      local.get $l6
                      i32.const 48
                      i32.add
                      local.set $l13
                      local.get $l6
                      i32.const 12
                      i32.add
                      local.set $l15
                      local.get $l19
                      i32.load offset=216
                      local.set $l11
                      block $B99
                        local.get $l4
                        i32.const -2147483648
                        i32.and
                        i32.const 1065353216
                        i32.or
                        f32.reinterpret_i32
                        f32.const 0x0p+0 (;=0;)
                        f32.lt
                        br_if $B99
                        local.get $l37
                        local.get $l40
                        f32.gt
                        i32.eqz
                        br_if $B99
                        i32.const 1
                        local.set $l5
                        block $B100
                          local.get $l37
                          local.get $l19
                          local.get $l19
                          i32.load
                          i32.load offset=84
                          call_indirect $__indirect_function_table (type $t23)
                          local.tee $l39
                          f32.ge
                          i32.eqz
                          br_if $B100
                          local.get $l16
                          local.get $l39
                          f32.const 0x0p+0 (;=0;)
                          f32.ne
                          i32.and
                          i32.eqz
                          br_if $B100
                          block $B101 (result i32)
                            local.get $l37
                            local.get $l39
                            f32.div
                            f32.floor
                            f32.const 0x1p+0 (;=1;)
                            f32.add
                            local.tee $l38
                            f32.abs
                            f32.const 0x1p+31 (;=2.14748e+09;)
                            f32.lt
                            if $I102
                              local.get $l38
                              i32.trunc_f32_s
                              br $B101
                            end
                            i32.const -2147483648
                          end
                          local.tee $l5
                          i32.const 0
                          i32.le_s
                          br_if $B98
                        end
                        local.get $l5
                        i32.const 1
                        i32.sub
                        local.set $l17
                        local.get $l11
                        i32.const 0
                        i32.le_s
                        local.set $l18
                        loop $L103
                          block $B104
                            local.get $l18
                            br_if $B104
                            local.get $l9
                            f32.convert_i32_s
                            local.set $l42
                            i32.const 0
                            local.set $l4
                            loop $L105
                              local.get $l19
                              i32.load offset=208
                              local.set $l16
                              block $B106
                                block $B107
                                  local.get $l6
                                  i32.load8_u offset=60
                                  br_if $B107
                                  local.get $l5
                                  i32.const 1
                                  i32.eq
                                  br_if $B107
                                  local.get $l9
                                  local.get $l17
                                  i32.ne
                                  br_if $B107
                                  local.get $l16
                                  local.get $l4
                                  i32.const 88
                                  i32.mul
                                  i32.add
                                  f32.load
                                  f32.const 0x0p+0 (;=0;)
                                  f32.eq
                                  br_if $B106
                                end
                                block $B108
                                  local.get $l40
                                  local.get $l42
                                  local.get $l39
                                  f32.mul
                                  local.get $l16
                                  local.get $l4
                                  i32.const 88
                                  i32.mul
                                  i32.add
                                  local.tee $l16
                                  f32.load
                                  f32.add
                                  local.tee $l38
                                  f32.lt
                                  i32.eqz
                                  br_if $B108
                                  local.get $l37
                                  local.get $l38
                                  f32.ge
                                  i32.eqz
                                  br_if $B108
                                  local.get $l16
                                  local.get $l8
                                  i32.const 0
                                  local.get $l15
                                  local.get $l13
                                  call $f68818
                                end
                                local.get $l37
                                local.get $l38
                                f32.lt
                                br_if $B104
                                local.get $l4
                                i32.const 1
                                i32.add
                                local.tee $l4
                                local.get $l11
                                i32.lt_s
                                br_if $L105
                                br $B104
                              end
                              local.get $l4
                              i32.const 1
                              i32.add
                              local.tee $l4
                              local.get $l11
                              i32.lt_s
                              br_if $L105
                            end
                          end
                          local.get $l9
                          i32.const 1
                          i32.add
                          local.tee $l9
                          local.get $l5
                          i32.ne
                          br_if $L103
                        end
                        br $B98
                      end
                      local.get $l37
                      local.get $l40
                      f32.lt
                      i32.eqz
                      br_if $B98
                      local.get $l19
                      local.get $l19
                      i32.load
                      i32.load offset=84
                      call_indirect $__indirect_function_table (type $t23)
                      local.set $l39
                      i32.const 1
                      local.set $l5
                      block $B109
                        local.get $l37
                        f32.const 0x0p+0 (;=0;)
                        f32.le
                        i32.eqz
                        br_if $B109
                        local.get $l16
                        i32.const 1
                        i32.xor
                        br_if $B109
                        block $B110 (result i32)
                          local.get $l39
                          local.get $l37
                          f32.sub
                          local.get $l39
                          f32.div
                          f32.floor
                          f32.const 0x1p+0 (;=1;)
                          f32.add
                          local.tee $l38
                          f32.abs
                          f32.const 0x1p+31 (;=2.14748e+09;)
                          f32.lt
                          if $I111
                            local.get $l38
                            i32.trunc_f32_s
                            br $B110
                          end
                          i32.const -2147483648
                        end
                        local.tee $l5
                        i32.const 0
                        i32.le_s
                        br_if $B98
                      end
                      i32.const 0
                      local.set $l6
                      loop $L112
                        local.get $l6
                        f32.convert_i32_s
                        f32.neg
                        local.set $l42
                        local.get $l11
                        local.set $l4
                        loop $L113
                          local.get $l4
                          i32.const 0
                          i32.gt_s
                          if $I114
                            block $B115
                              local.get $l40
                              local.get $l42
                              local.get $l39
                              f32.mul
                              local.get $l19
                              i32.load offset=208
                              local.get $l4
                              i32.const 1
                              i32.sub
                              local.tee $l4
                              i32.const 88
                              i32.mul
                              i32.add
                              local.tee $l16
                              f32.load
                              f32.add
                              local.tee $l38
                              f32.gt
                              i32.eqz
                              br_if $B115
                              local.get $l37
                              local.get $l38
                              f32.le
                              i32.eqz
                              br_if $B115
                              local.get $l16
                              local.get $l8
                              i32.const 0
                              local.get $l15
                              local.get $l13
                              call $f68818
                            end
                            local.get $l37
                            local.get $l38
                            f32.ge
                            i32.eqz
                            br_if $L113
                          end
                        end
                        local.get $l6
                        i32.const 1
                        i32.add
                        local.tee $l6
                        local.get $l5
                        i32.ne
                        br_if $L112
                      end
                    end
                    local.get $l10
                    i32.load offset=48
                    local.set $l4
                    local.get $l10
                    i32.load offset=40
                    local.set $l6
                  end
                  local.get $l7
                  i32.const -64
                  i32.sub
                  local.tee $l7
                  local.get $l6
                  local.get $l4
                  i32.const 6
                  i32.shl
                  i32.add
                  i32.ne
                  br_if $L94
                end
              end
              block $B116
                local.get $l10
                i32.load offset=40
                local.tee $l7
                i32.eqz
                br_if $B116
                local.get $l10
                i32.load8_u offset=52
                i32.const 1
                i32.and
                br_if $B116
                local.get $l7
                local.get $l10
                i32.load offset=44
                i32.const 403047
                i32.const 774
                call $f83342
              end
              local.get $l10
              i32.const 0
              i32.store offset=40
              local.get $l10
              i64.const 4294967296
              i64.store offset=48
              local.get $l8
              local.get $l8
              i32.load offset=228
              i32.const -9
              i32.and
              i32.store offset=228
            end
          end
          block $B117
            local.get $l12
            i32.load offset=48
            local.get $p1
            i32.add
            i32.load8_u
            i32.eqz
            br_if $B117
            local.get $l10
            i32.load offset=56
            i32.load8_u offset=29
            i32.eqz
            br_if $B117
            local.get $l10
            i32.load offset=60
            i32.load
            i32.eqz
            br_if $B117
            local.get $l10
            i32.load offset=16
            i32.const 7
            local.get $l10
            i32.const -1
            call $f69095
            drop
          end
          local.get $p1
          i32.const 1
          i32.add
          local.tee $p1
          local.get $l12
          i32.load offset=88
          i32.lt_u
          br_if $L90
        end
      end
      local.get $l14
      call $f80130
      drop
      local.get $l12
      i32.load offset=88
      if $I118
        loop $L119
          local.get $l22
          i32.const 72
          i32.mul
          local.tee $l6
          local.get $l12
          i32.load offset=80
          i32.add
          local.tee $l7
          i32.load offset=16
          local.tee $l4
          i32.load offset=740
          local.tee $l14
          if $I120
            local.get $l4
            i32.load offset=732
            local.tee $l8
            local.set $p1
            loop $L121
              block $B122
                local.get $p1
                i32.load
                local.tee $l10
                i32.eqz
                br_if $B122
                local.get $l10
                i32.load offset=16
                local.get $p1
                i32.load offset=4
                i32.const -2
                i32.and
                i32.ne
                br_if $B122
                block $B123
                  local.get $l10
                  i32.load offset=20
                  local.tee $l10
                  local.get $l10
                  i32.load
                  i32.load offset=156
                  call_indirect $__indirect_function_table (type $t5)
                  i32.eqz
                  br_if $B123
                  local.get $l10
                  i32.load offset=196
                  local.tee $l10
                  i32.load offset=20
                  i32.const 1
                  i32.ne
                  br_if $B123
                  local.get $l10
                  i32.const 2
                  i32.store offset=20
                end
                local.get $l4
                i32.load offset=740
                local.set $l14
                local.get $l4
                i32.load offset=732
                local.set $l8
              end
              local.get $p1
              i32.const 8
              i32.add
              local.tee $p1
              local.get $l8
              local.get $l14
              i32.const 3
              i32.shl
              i32.add
              i32.ne
              br_if $L121
            end
          end
          block $B124
            local.get $l7
            i32.load offset=56
            i32.load8_u offset=29
            i32.eqz
            br_if $B124
            local.get $l7
            i32.load offset=60
            i32.load
            i32.eqz
            br_if $B124
            local.get $l12
            i32.load offset=80
            local.get $l6
            i32.add
            local.set $l7
            i32.const 0
            local.set $l14
            i32.const 0
            local.set $l10
            f32.const 0x0p+0 (;=0;)
            local.set $l42
            global.get $g0
            i32.const 32
            i32.sub
            local.tee $l11
            global.set $g0
            local.get $l4
            local.get $l4
            i32.load offset=228
            i32.const 2
            i32.or
            i32.store offset=228
            local.get $l4
            i32.load offset=28
            i32.const 4131408
            call $f80185
            local.set $l19
            block $B125
              block $B126
                block $B127
                  local.get $l4
                  i32.load offset=900
                  local.tee $l6
                  i32.const 1
                  i32.eq
                  br_if $B127
                  local.get $l6
                  i32.const 2
                  i32.eq
                  if $I128
                    local.get $l4
                    f32.load offset=720
                    f32.const 0x0p+0 (;=0;)
                    f32.lt
                    br_if $B127
                  end
                  block $B129
                    local.get $l4
                    i32.load offset=28
                    i32.load offset=56
                    i32.const 1
                    i32.const 4676660
                    i32.load
                    i32.shl
                    i32.const 4676656
                    i32.load
                    i32.const 28
                    i32.shl
                    i32.const 31
                    i32.shr_s
                    i32.and
                    i32.and
                    i32.eqz
                    br_if $B129
                    local.get $l4
                    i32.load8_u offset=228
                    i32.const 32
                    i32.and
                    br_if $B129
                    local.get $l11
                    i32.const 0
                    i32.store offset=24
                    local.get $l11
                    i64.const 0
                    i64.store offset=16
                    local.get $l4
                    i32.const 4676644
                    local.get $l11
                    i32.const 16
                    i32.add
                    call $f80200
                    i32.const 1
                    local.set $l14
                  end
                  i32.const 4782136
                  i32.load
                  i32.const 1
                  i32.or
                  call $f80130
                  local.set $l6
                  local.get $l4
                  i32.const 8
                  local.get $l7
                  i32.const -1
                  call $f69095
                  local.set $p1
                  local.get $l6
                  call $f80130
                  drop
                  local.get $l7
                  i32.load offset=56
                  local.tee $l6
                  i32.load8_u offset=29
                  i32.eqz
                  br_if $B125
                  local.get $l7
                  i32.load offset=60
                  i32.load
                  local.tee $l10
                  i32.eqz
                  br_if $B125
                  local.get $l6
                  i32.load offset=8
                  local.set $l16
                  block $B130
                    local.get $p1
                    local.get $l14
                    i32.or
                    local.tee $l14
                    br_if $B130
                    local.get $l4
                    i32.load8_u offset=714
                    i32.eqz
                    br_if $B130
                    global.get $g0
                    i32.const 80
                    i32.sub
                    local.tee $p1
                    global.set $g0
                    block $B131
                      local.get $l4
                      i32.load offset=900
                      local.tee $l8
                      i32.const 1
                      i32.eq
                      br_if $B131
                      local.get $l8
                      i32.const 2
                      i32.eq
                      if $I132
                        local.get $l4
                        f32.load offset=720
                        f32.const 0x0p+0 (;=0;)
                        f32.lt
                        br_if $B131
                      end
                      local.get $l4
                      i32.load8_u offset=228
                      i32.const 2
                      i32.and
                      i32.eqz
                      br_if $B131
                      local.get $l6
                      i32.load8_u offset=29
                      i32.eqz
                      br_if $B131
                      local.get $l4
                      i64.load offset=568
                      local.set $l107
                      local.get $p1
                      local.get $l4
                      f32.load offset=576
                      f32.store offset=32
                      local.get $p1
                      local.get $l107
                      i64.store offset=24
                      local.get $p1
                      local.get $l6
                      i32.load offset=12
                      local.tee $l8
                      f32.load offset=20
                      local.tee $l37
                      local.get $l8
                      f32.load offset=12
                      local.tee $l38
                      local.get $l38
                      f32.mul
                      local.get $l8
                      f32.load offset=16
                      local.tee $l39
                      local.get $l39
                      f32.mul
                      f32.add
                      local.get $l37
                      local.get $l37
                      f32.mul
                      local.get $l8
                      f32.load offset=24
                      local.tee $l40
                      local.get $l40
                      f32.mul
                      f32.add
                      f32.add
                      local.tee $l44
                      f32.sqrt
                      local.tee $l37
                      f32.div
                      f32.const 0x0p+0 (;=0;)
                      local.get $l44
                      f32.const 0x1.4484cp-100 (;=1e-30;)
                      f32.gt
                      local.tee $l8
                      select
                      f32.store offset=44
                      local.get $p1
                      local.get $l39
                      local.get $l37
                      f32.div
                      f32.const 0x0p+0 (;=0;)
                      local.get $l8
                      select
                      f32.store offset=40
                      local.get $p1
                      local.get $l40
                      local.get $l37
                      f32.div
                      f32.const 0x1p+0 (;=1;)
                      local.get $l8
                      select
                      f32.store offset=48
                      local.get $p1
                      local.get $l38
                      local.get $l37
                      f32.div
                      f32.const 0x0p+0 (;=0;)
                      local.get $l8
                      select
                      f32.store offset=36
                      block $B133
                        local.get $l4
                        i32.load8_u offset=281
                        i32.eqz
                        br_if $B133
                        local.get $l4
                        i32.load offset=260
                        local.tee $l8
                        i32.eqz
                        br_if $B133
                        local.get $l8
                        i32.load offset=16
                        local.tee $l8
                        i32.eqz
                        br_if $B133
                        local.get $l8
                        f32.load offset=32
                        local.set $l42
                      end
                      local.get $p1
                      i32.const 0
                      i32.store8 offset=56
                      local.get $p1
                      local.get $l42
                      f32.store offset=52
                      local.get $p1
                      local.get $l4
                      i32.load offset=224
                      i32.const 1
                      i32.ne
                      i32.store8 offset=57
                      local.get $p1
                      i32.const 0
                      i32.store offset=72
                      local.get $p1
                      i32.const 4108868
                      i32.store offset=64
                      local.get $p1
                      local.get $p1
                      i32.const 24
                      i32.add
                      i32.store offset=68
                      local.get $l4
                      i32.const 4676692
                      local.get $p1
                      i32.const -64
                      i32.sub
                      call $f80200
                      local.get $p1
                      i32.load8_u offset=56
                      br_if $B131
                      local.get $p1
                      i32.const 16
                      i32.add
                      local.get $l4
                      i32.load offset=28
                      i32.const 4131408
                      call $f80185
                      call $f78084
                      local.get $l6
                      i32.load offset=12
                      local.set $l8
                      i64.const 0
                      local.set $l107
                      local.get $l4
                      i32.load offset=224
                      i32.const 1
                      i32.eq
                      if $I134
                        i32.const 4745992
                        i32.load
                        i32.const 64
                        call $f78118
                        local.set $l107
                      end
                      local.get $p1
                      local.get $p1
                      i64.load offset=16
                      i64.store offset=8
                      local.get $p1
                      i32.const 8
                      i32.add
                      local.get $l8
                      local.get $l107
                      call $f69096
                      i32.eqz
                      br_if $B131
                      local.get $l4
                      i32.load offset=28
                      i32.const 4131408
                      call $f80185
                      call $f78085
                    end
                    local.get $p1
                    i32.const 80
                    i32.add
                    global.set $g0
                    local.get $l7
                    i32.load offset=56
                    i32.load8_u offset=29
                    i32.eqz
                    br_if $B125
                  end
                  local.get $l7
                  i32.load offset=60
                  i32.load
                  i32.eqz
                  br_if $B125
                  local.get $l4
                  i32.load8_u offset=714
                  local.set $l6
                  local.get $l11
                  i32.const 16
                  i32.add
                  local.get $l4
                  i32.load offset=28
                  i32.const 4131408
                  call $f80185
                  call $f78084
                  local.get $l7
                  local.get $l11
                  i64.load offset=16
                  i64.store
                  local.get $l10
                  local.get $l16
                  i32.load
                  local.get $l7
                  local.get $l6
                  local.get $l14
                  i32.or
                  i32.const 0
                  i32.ne
                  local.get $l7
                  i64.load offset=8
                  call $f68809
                  br_if $B126
                  br $B125
                end
                local.get $l7
                i32.load offset=56
                i32.load offset=8
                local.set $l6
                local.get $l7
                i32.load offset=60
                i32.load
                local.set $l14
                local.get $l4
                i32.load8_u offset=714
                if $I135 (result i32)
                  local.get $l11
                  local.get $l7
                  i64.load
                  local.tee $l107
                  i64.store offset=8
                  local.get $l7
                  i32.load offset=16
                  i32.load offset=264
                  local.set $p1
                  local.get $l7
                  i64.load offset=8
                  local.set $l108
                  local.get $l11
                  local.get $l107
                  i64.store
                  local.get $l11
                  local.get $p1
                  local.get $l108
                  call $f69096
                  local.set $l10
                  local.get $l4
                  i32.load8_u offset=714
                  i32.const 0
                  i32.ne
                else
                  i32.const 0
                end
                local.set $p1
                local.get $l14
                local.get $l6
                i32.load
                local.get $l7
                local.get $p1
                local.get $l7
                i64.load offset=8
                call $f68809
                local.get $l10
                i32.or
                i32.eqz
                br_if $B125
              end
              local.get $l19
              call $f78085
            end
            local.get $l4
            local.get $l4
            i32.load offset=228
            i32.const -3
            i32.and
            i32.store offset=228
            local.get $l11
            i32.const 32
            i32.add
            global.set $g0
            local.get $l4
            i32.load8_u offset=217
            br_if $B124
            local.get $l4
            i32.load offset=264
            local.get $l100
            call $f68374
          end
          local.get $l22
          i32.const 1
          i32.add
          local.tee $l22
          local.get $l12
          i32.load offset=88
          i32.lt_u
          br_if $L119
        end
      end
      local.get $l12
      i32.const 32
      i32.add
      call $f554
      drop
      local.get $l12
      i32.const 48
      i32.add
      call $f554
      drop
      local.get $l12
      i32.const -64
      i32.sub
      call $f554
      drop
      local.get $l12
      i32.const 80
      i32.add
      call $f69094
    end
    local.get $p2
    if $I136
      local.get $l12
      i64.const 4294967296
      i64.store offset=88
      local.get $l12
      i64.const 4294967296
      i64.store offset=80
      block $B137
        local.get $l23
        i32.eqz
        if $I138
          local.get $l12
          i64.const 4294967296
          i64.store offset=72
          local.get $l12
          i64.const 4294967296
          i64.store offset=64
          br $B137
        end
        local.get $l12
        i32.const 80
        i32.add
        local.get $l23
        i32.const 72
        i32.const 8
        call $f545
        local.get $l12
        i64.const 4294967296
        i64.store offset=72
        local.get $l12
        i64.const 4294967296
        i64.store offset=64
        local.get $l12
        i32.const -64
        i32.sub
        local.get $l23
        i32.const 72
        i32.const 8
        call $f545
      end
      i32.const 0
      local.set $p1
      local.get $p0
      local.get $l12
      i32.const 80
      i32.add
      local.get $l12
      i32.const -64
      i32.sub
      i32.const 0
      i32.const 0
      i32.const 0
      i32.const 0
      local.get $p3
      call $f69099
      local.get $l12
      i64.const 4294967296
      i64.store offset=56
      local.get $l12
      i64.const 4294967296
      i64.store offset=48
      local.get $l12
      i64.const 4294967296
      i64.store offset=40
      local.get $l12
      i64.const 4294967296
      i64.store offset=32
      local.get $l12
      i32.const 80
      i32.add
      local.get $l12
      i32.const 48
      i32.add
      call $f69100
      local.get $l12
      i32.const -64
      i32.sub
      local.get $l12
      i32.const 32
      i32.add
      call $f69100
      i32.const 0
      local.set $p3
      block $B139
        local.get $l12
        i32.load offset=88
        local.tee $l4
        i32.eqz
        br_if $B139
        local.get $l12
        i32.load offset=80
        local.set $l22
        i32.const 0
        local.set $l10
        loop $L140
          block $B141
            local.get $l22
            local.get $l10
            i32.const 72
            i32.mul
            i32.add
            local.tee $l14
            i32.load offset=56
            local.tee $l8
            i32.load8_u offset=29
            i32.eqz
            br_if $B141
            local.get $l14
            i32.load offset=60
            i32.load
            i32.eqz
            br_if $B141
            local.get $l12
            local.get $l14
            i64.load
            local.tee $l107
            i64.store offset=16
            local.get $l8
            i32.load offset=12
            local.set $l8
            local.get $l12
            local.get $l107
            i64.store offset=8
            local.get $l12
            i32.const 8
            i32.add
            local.get $l8
            call $f69091
            local.get $l14
            i32.load offset=16
            drop
            global.get $g0
            i32.const -64
            i32.add
            local.tee $p0
            global.set $g0
            i32.const 1
            local.set $l8
            local.get $l14
            i32.load offset=16
            local.tee $p2
            i32.load8_u offset=714
            i32.eqz
            if $I142
              local.get $p2
              call $f69106
              local.set $l8
            end
            local.get $l14
            i64.load
            local.set $l107
            local.get $l14
            i32.load offset=56
            local.set $l23
            local.get $l14
            i32.load offset=64
            local.set $l7
            local.get $l14
            i32.load offset=68
            local.tee $p2
            i32.load offset=4
            i32.const 1
            call $f68309
            local.get $l7
            i32.load offset=64
            local.get $l7
            i32.load offset=68
            local.get $l7
            i32.load offset=72
            local.get $p2
            i32.load offset=4
            i32.const 0
            call $f68330
            local.get $p2
            i32.const 0
            i32.store8
            local.get $l7
            i32.load offset=56
            local.tee $l7
            i32.const -1
            i32.ne
            if $I143
              local.get $l7
              local.get $p2
              i32.load offset=4
              local.tee $l7
              i32.load offset=28
              local.get $l7
              i32.const 28
              i32.add
              i32.add
              i32.add
              i32.const 0
              i32.store8
              local.get $p2
              i32.const 0
              i32.store8
            end
            local.get $l23
            i32.load offset=4
            local.set $l7
            local.get $p2
            i32.const 0
            i32.store8 offset=12
            local.get $p2
            local.get $l7
            i32.store offset=8
            local.get $p0
            i32.const 24
            i32.add
            call $f68288
            local.get $p2
            i32.load offset=16
            local.tee $l7
            local.get $p0
            i64.load offset=24
            i64.store align=4
            local.get $l7
            local.get $p0
            i32.load offset=32
            i32.store offset=8
            local.get $p2
            local.get $l107
            i64.store offset=36 align=4
            local.get $p2
            i32.const 0
            i32.store offset=32
            local.get $p2
            i32.const 0
            i32.store offset=24
            local.get $p2
            i32.const 0
            i32.store8 offset=21
            local.get $p2
            local.get $l8
            i32.store8 offset=20
            local.get $p0
            i32.const 1
            i32.store8 offset=62
            local.get $p0
            i32.const 0
            i32.store16 offset=60
            local.get $p0
            i32.const 0
            i32.store8 offset=48
            local.get $p0
            i32.const 0
            i32.store8 offset=36
            local.get $p0
            local.get $l14
            i32.load offset=56
            local.tee $p2
            i32.load offset=8
            local.tee $l7
            i32.load
            i32.store offset=24
            local.get $p0
            local.get $l7
            i32.load offset=4
            i32.store offset=28
            local.get $p0
            local.get $l7
            i32.load offset=16
            i32.store offset=32
            local.get $p0
            local.get $p2
            i32.load offset=8
            i32.load offset=24
            i32.store offset=40
            local.get $p0
            local.get $p2
            i32.load offset=4
            i32.load8_u offset=17
            if $I144 (result i32)
              i32.const 0
            else
              local.get $p2
              i32.load offset=8
              i32.load offset=20
            end
            i32.store offset=44
            local.get $p0
            local.get $p0
            i32.const 24
            i32.add
            i32.store offset=56
            local.get $l14
            i32.load offset=68
            local.set $p2
            local.get $l14
            i32.load offset=64
            local.set $l7
            local.get $p0
            i64.const 4294967364
            i64.store offset=16
            local.get $p0
            i64.const 4294967364
            i64.store offset=8
            local.get $l14
            local.get $l7
            local.get $p2
            local.get $p0
            i32.const 56
            i32.add
            i32.const 118910
            i32.const 118911
            i32.const 118912
            i32.const 118913
            local.get $p0
            i32.const 8
            i32.add
            call $f68953
            local.get $l14
            i32.load offset=64
            i32.load8_u offset=78
            if $I145
              local.get $l14
              i32.load offset=56
              i32.load offset=4
              local.get $p0
              i32.load8_u offset=60
              i32.store8 offset=19
              local.get $l14
              i32.load offset=56
              i32.load offset=4
              local.get $p0
              i32.load8_u offset=61
              i32.store8 offset=20
              local.get $l14
              i32.load offset=56
              i32.load offset=4
              local.get $p0
              i32.load8_u offset=62
              i32.store8 offset=21
            end
            local.get $p0
            i32.const -64
            i32.sub
            global.set $g0
          end
          local.get $l10
          i32.const 1
          i32.add
          local.tee $l10
          local.get $l4
          i32.ne
          br_if $L140
        end
        local.get $l12
        i32.load offset=88
        local.tee $l14
        i32.eqz
        br_if $B139
        local.get $l12
        i32.load offset=80
        local.set $l10
        local.get $l14
        i32.const 72
        i32.mul
        i32.const 72
        i32.sub
        local.tee $l14
        i32.const 72
        i32.div_u
        i32.const 1
        i32.add
        local.tee $l8
        i32.const 1
        i32.and
        local.set $p0
        local.get $l14
        i32.const 72
        i32.ge_u
        if $I146
          local.get $l8
          i32.const 134217726
          i32.and
          local.set $l7
          i32.const 0
          local.set $l22
          loop $L147
            local.get $l10
            i32.load offset=16
            local.tee $l8
            i32.load offset=748
            local.tee $l14
            i32.eqz
            if $I148
              local.get $l8
              i32.load offset=256
              i32.load8_u offset=20
              local.set $l14
            end
            local.get $l8
            i32.load offset=268
            i32.const 1
            i32.store8 offset=54
            local.get $l14
            local.get $p3
            local.get $p3
            local.get $l14
            i32.lt_s
            select
            local.set $l8
            local.get $l10
            i32.load offset=88
            local.tee $l4
            i32.load offset=748
            local.tee $l14
            i32.eqz
            if $I149
              local.get $l4
              i32.load offset=256
              i32.load8_u offset=20
              local.set $l14
            end
            local.get $l4
            i32.load offset=268
            i32.const 1
            i32.store8 offset=54
            local.get $l14
            local.get $l8
            local.get $l8
            local.get $l14
            i32.lt_s
            select
            local.set $p3
            local.get $l10
            i32.const 144
            i32.add
            local.set $l10
            local.get $l22
            i32.const 2
            i32.add
            local.tee $l22
            local.get $l7
            i32.ne
            br_if $L147
          end
        end
        local.get $p0
        i32.eqz
        br_if $B139
        local.get $l10
        i32.load offset=16
        local.tee $l14
        i32.load offset=748
        local.tee $l10
        i32.eqz
        if $I150
          local.get $l14
          i32.load offset=256
          i32.load8_u offset=20
          local.set $l10
        end
        local.get $l14
        i32.load offset=268
        i32.const 1
        i32.store8 offset=54
        local.get $l10
        local.get $p3
        local.get $p3
        local.get $l10
        i32.lt_s
        select
        local.set $p3
      end
      block $B151
        local.get $l12
        i32.load offset=72
        local.tee $l14
        i32.eqz
        br_if $B151
        local.get $l12
        i32.load offset=64
        local.set $l8
        loop $L152
          block $B153
            local.get $l8
            local.get $p1
            i32.const 72
            i32.mul
            i32.add
            local.tee $l10
            i32.load offset=56
            i32.load8_u offset=29
            i32.eqz
            br_if $B153
            local.get $l10
            i32.load offset=60
            i32.load
            i32.eqz
            br_if $B153
            local.get $l10
            i32.load offset=16
            local.set $l7
            i32.const 0
            local.set $p2
            i32.const 0
            local.set $l22
            block $B154
              local.get $l10
              i32.load offset=56
              local.tee $p0
              i32.load offset=4
              local.tee $l23
              i32.load8_u offset=17
              if $I155
                i32.const 1
                local.set $p2
                br $B154
              end
              local.get $l7
              i32.load offset=740
              local.tee $l4
              i32.eqz
              br_if $B154
              local.get $l4
              local.get $l7
              i32.load offset=208
              i32.ne
              br_if $B154
              local.get $l7
              i32.load offset=732
              local.tee $l23
              local.set $p0
              loop $L156
                block $B157
                  local.get $p0
                  i32.load
                  local.tee $p2
                  i32.eqz
                  br_if $B157
                  local.get $p2
                  i32.load offset=16
                  local.get $p0
                  i32.load offset=4
                  i32.const -2
                  i32.and
                  i32.ne
                  br_if $B157
                  local.get $l22
                  local.get $p2
                  i32.load offset=20
                  call $f68617
                  i32.const 1
                  i32.gt_s
                  i32.or
                  local.set $l22
                  local.get $l7
                  i32.load offset=740
                  local.set $l4
                  local.get $l7
                  i32.load offset=732
                  local.set $l23
                end
                local.get $p0
                i32.const 8
                i32.add
                local.tee $p0
                local.get $l23
                local.get $l4
                i32.const 3
                i32.shl
                i32.add
                i32.ne
                br_if $L156
              end
              local.get $l22
              i32.const 1
              i32.xor
              local.set $p2
              local.get $l10
              i32.load offset=56
              local.tee $p0
              i32.load offset=4
              local.set $l23
            end
            local.get $p0
            i32.load
            local.set $l24
            local.get $p0
            i32.load offset=8
            local.set $l11
            local.get $p0
            i32.load offset=12
            local.set $l15
            local.get $p0
            i32.load offset=16
            local.set $l25
            local.get $p2
            i32.const 1
            i32.and
            local.set $l27
            global.get $g0
            i32.const 1120
            i32.sub
            local.tee $l13
            global.set $g0
            block $B158
              local.get $l24
              i32.load offset=20
              local.tee $l16
              i32.eqz
              br_if $B158
              local.get $l16
              local.get $l24
              i32.const 20
              i32.add
              local.tee $l26
              i32.add
              local.tee $l16
              i32.load offset=40
              local.get $l16
              i32.const 40
              i32.add
              i32.add
              i32.load
              i32.eqz
              br_if $B158
              local.get $l15
              i64.load align=4
              local.set $l107
              local.get $l13
              local.get $l15
              f32.load offset=8
              f32.store offset=1088
              local.get $l13
              local.get $l107
              i64.store offset=1080
              local.get $l15
              i64.load offset=12 align=4
              local.set $l107
              local.get $l13
              i32.const 1100
              i32.add
              local.get $l15
              i64.load offset=20 align=4
              i64.store align=4
              local.get $l13
              local.get $l107
              i64.store offset=1092 align=4
              local.get $l15
              i64.load offset=28 align=4
              local.set $l107
              local.get $l13
              i32.const 1116
              i32.add
              local.get $l15
              f32.load offset=36
              f32.store
              local.get $l13
              local.get $l107
              i64.store offset=1108 align=4
              local.get $l13
              i32.const 8
              i32.add
              call $f68289
              local.tee $l16
              local.set $l5
              local.get $l27
              if $I159 (result i32)
                i32.const 0
                local.set $l5
                local.get $l11
                i32.load offset=20
              else
                local.get $l16
              end
              local.get $l11
              i32.load offset=24
              call $f68296
              local.get $l26
              i32.load
              local.tee $l16
              local.get $l26
              i32.add
              i32.const 0
              local.get $l16
              select
              local.set $l6
              local.get $l11
              i32.load offset=20
              local.set $p2
              local.get $l11
              i32.load offset=28
              local.set $l7
              local.get $l25
              i32.load
              local.set $l19
              local.get $l25
              i32.load offset=4
              local.set $l9
              local.get $l23
              i32.load8_u offset=21
              local.set $l29
              global.get $g0
              i32.const 16
              i32.sub
              local.tee $l22
              global.set $g0
              local.get $l6
              i32.load offset=56
              local.set $l30
              local.get $l6
              f32.load offset=256
              local.set $l59
              local.get $p2
              f32.load
              local.set $l37
              local.get $p2
              f32.load offset=4
              local.set $l38
              local.get $l7
              local.get $p2
              f32.load offset=8
              local.tee $l39
              f32.store offset=8
              local.get $l7
              local.get $l38
              f32.store offset=4
              local.get $l7
              local.get $l37
              f32.store
              local.get $p2
              i64.load offset=12 align=4
              local.set $l107
              local.get $l7
              i32.const 20
              i32.add
              local.tee $l4
              local.get $p2
              i64.load offset=20 align=4
              i64.store align=4
              local.get $l7
              local.get $l107
              i64.store offset=12 align=4
              local.get $p2
              f32.load offset=36
              local.set $l42
              local.get $l7
              local.get $p2
              i64.load offset=28 align=4
              i64.store offset=28 align=4
              local.get $l7
              i32.const 36
              i32.add
              local.tee $l10
              local.get $l42
              f32.store
              local.get $p2
              f32.load offset=48
              local.set $l42
              local.get $l7
              local.get $p2
              i64.load offset=40 align=4
              i64.store offset=40 align=4
              local.get $l7
              local.get $l42
              f32.store offset=48
              local.get $p2
              i64.load offset=52 align=4
              local.set $l107
              local.get $l7
              local.get $p2
              i64.load offset=60 align=4
              i64.store offset=60 align=4
              local.get $l7
              local.get $l107
              i64.store offset=52 align=4
              local.get $l7
              i32.const 68
              i32.add
              local.get $p2
              i32.const 68
              i32.add
              i32.const 256
              call $f483
              drop
              local.get $l7
              i32.const 596
              i32.add
              local.get $p2
              i32.const 596
              i32.add
              i32.const 220
              call $f483
              local.set $l31
              local.get $l7
              i32.const 364
              i32.add
              local.get $p2
              i32.const 364
              i32.add
              i32.const 80
              call $f483
              local.set $l32
              local.get $l7
              i32.const 500
              i32.add
              local.get $p2
              i32.const 500
              i32.add
              i32.const 80
              call $f483
              local.set $l16
              local.get $l7
              i32.const 816
              i32.add
              local.get $p2
              i32.const 816
              i32.add
              i32.const 252
              call $f483
              local.set $l26
              local.get $l7
              local.get $l59
              local.get $l39
              f32.mul
              local.tee $l47
              f32.store offset=8
              local.get $l7
              local.get $l59
              local.get $l38
              f32.mul
              local.tee $l54
              f32.store offset=4
              local.get $l7
              local.get $l59
              local.get $l37
              f32.mul
              local.tee $l51
              f32.store
              local.get $l7
              i32.const 16
              i32.add
              local.tee $l17
              f32.load
              local.set $l40
              local.get $l13
              i32.const 1080
              i32.add
              local.tee $p0
              f32.load offset=16
              local.set $l37
              local.get $l7
              i32.const 24
              i32.add
              local.tee $l18
              f32.load
              local.set $l44
              local.get $p0
              f32.load offset=24
              local.set $l42
              local.get $l4
              f32.load
              local.set $l41
              local.get $p0
              f32.load offset=20
              local.set $l38
              local.get $l7
              i32.const 32
              i32.add
              local.tee $l20
              f32.load
              local.set $l52
              local.get $p0
              f32.load offset=32
              local.set $l46
              local.get $p0
              f32.load
              local.set $l65
              local.get $p0
              f32.load offset=4
              local.set $l48
              local.get $p0
              f32.load offset=8
              local.set $l49
              local.get $l7
              f32.load offset=12
              local.set $l43
              local.get $p0
              f32.load offset=12
              local.set $l39
              local.get $l7
              f32.load offset=28
              local.set $l50
              local.get $p0
              f32.load offset=28
              local.set $l45
              local.get $l10
              local.get $p0
              f32.load offset=36
              local.tee $l53
              local.get $l10
              f32.load
              f32.mul
              f32.store
              local.get $l20
              local.get $l46
              local.get $l52
              f32.mul
              f32.store
              local.get $l7
              local.get $l45
              local.get $l50
              f32.mul
              f32.store offset=28
              local.get $l18
              local.get $l42
              local.get $l44
              f32.mul
              local.get $l39
              local.get $l43
              f32.mul
              f32.sub
              local.get $l38
              local.get $l41
              f32.mul
              f32.sub
              local.get $l37
              local.get $l40
              f32.mul
              f32.sub
              f32.store
              local.get $l4
              local.get $l37
              local.get $l43
              f32.mul
              local.get $l42
              local.get $l41
              f32.mul
              f32.sub
              local.get $l38
              local.get $l44
              f32.mul
              f32.sub
              local.get $l39
              local.get $l40
              f32.mul
              f32.sub
              i32.reinterpret_f32
              i32.const -2147483648
              i32.xor
              i32.store
              local.get $l17
              local.get $l39
              local.get $l41
              f32.mul
              local.get $l38
              local.get $l43
              f32.mul
              f32.sub
              local.get $l42
              local.get $l40
              f32.mul
              f32.sub
              local.get $l37
              local.get $l44
              f32.mul
              f32.sub
              i32.reinterpret_f32
              i32.const -2147483648
              i32.xor
              i32.store
              local.get $l7
              local.get $l38
              local.get $l40
              f32.mul
              local.get $l37
              local.get $l41
              f32.mul
              f32.sub
              local.get $l42
              local.get $l43
              f32.mul
              f32.sub
              local.get $l39
              local.get $l44
              f32.mul
              f32.sub
              i32.reinterpret_f32
              i32.const -2147483648
              i32.xor
              i32.store offset=12
              local.get $l7
              local.get $l49
              local.get $l47
              local.get $l53
              f32.mul
              local.tee $l40
              local.get $l51
              local.get $l45
              f32.mul
              local.tee $l44
              local.get $l42
              local.get $l37
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l43
              f32.mul
              local.tee $l51
              local.get $l39
              local.get $l38
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l45
              f32.mul
              f32.sub
              f32.mul
              f32.add
              local.get $l40
              local.get $l39
              local.get $l39
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l47
              f32.mul
              local.get $l37
              local.get $l37
              local.get $l37
              f32.add
              local.tee $l52
              f32.mul
              f32.sub
              f32.mul
              local.get $l54
              local.get $l46
              f32.mul
              local.tee $l41
              local.get $l37
              local.get $l38
              local.get $l38
              f32.add
              local.tee $l46
              f32.mul
              local.get $l42
              local.get $l47
              f32.mul
              local.tee $l54
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.add
              f32.store offset=8
              local.get $l7
              local.get $l48
              local.get $l41
              local.get $l44
              local.get $l39
              local.get $l52
              f32.mul
              local.get $l42
              local.get $l45
              f32.mul
              local.tee $l42
              f32.sub
              f32.mul
              f32.add
              local.get $l40
              local.get $l54
              local.get $l43
              local.get $l38
              f32.mul
              f32.sub
              f32.mul
              local.get $l41
              local.get $l38
              local.get $l45
              f32.mul
              local.get $l39
              local.get $l39
              local.get $l39
              f32.add
              local.tee $l45
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.add
              f32.store offset=4
              local.get $l7
              local.get $l65
              local.get $l44
              local.get $l44
              local.get $l37
              local.get $l43
              f32.mul
              local.get $l38
              local.get $l46
              f32.mul
              f32.sub
              f32.mul
              f32.add
              local.get $l40
              local.get $l45
              local.get $l38
              f32.mul
              local.get $l51
              f32.sub
              f32.mul
              local.get $l41
              local.get $l42
              local.get $l37
              local.get $l47
              f32.mul
              f32.sub
              f32.mul
              f32.add
              f32.add
              f32.add
              f32.store
              local.get $l6
              i32.const 40
              i32.add
              local.set $l28
              local.get $l5
              local.get $p2
              local.get $l5
              select
              local.set $l27
              i32.const 0
              local.set $l10
              loop $L160
                local.get $l27
                local.get $l10
                i32.const 6
                i32.shl
                local.tee $l4
                i32.add
                local.tee $p2
                f32.load offset=68
                local.set $l37
                local.get $p2
                f32.load offset=72
                local.set $l38
                local.get $l4
                local.get $l7
                i32.add
                local.tee $l4
                i32.const 76
                i32.add
                local.tee $l17
                local.get $p2
                f32.load offset=76
                local.tee $l39
                f32.store
                local.get $l4
                i32.const 72
                i32.add
                local.tee $l18
                local.get $l38
                f32.store
                local.get $l4
                i32.const 68
                i32.add
                local.tee $l20
                local.get $l37
                f32.store
                local.get $p2
                f32.load offset=80
                local.set $l40
                local.get $p2
                f32.load offset=84
                local.set $l44
                local.get $p2
                f32.load offset=88
                local.set $l41
                local.get $l4
                i32.const 92
                i32.add
                local.tee $l21
                local.get $p2
                f32.load offset=92
                local.tee $l43
                f32.store
                local.get $l4
                i32.const 88
                i32.add
                local.tee $l33
                local.get $l41
                f32.store
                local.get $l4
                i32.const 84
                i32.add
                local.tee $l34
                local.get $l44
                f32.store
                local.get $l4
                i32.const 80
                i32.add
                local.tee $l35
                local.get $l40
                f32.store
                local.get $p2
                f32.load offset=96
                local.set $l46
                local.get $p2
                f32.load offset=100
                local.set $l45
                local.get $l4
                i32.const 104
                i32.add
                local.tee $l36
                local.get $p2
                f32.load offset=104
                local.tee $l51
                f32.store
                local.get $l4
                i32.const 100
                i32.add
                local.tee $p2
                local.get $l45
                f32.store
                local.get $l4
                i32.const 96
                i32.add
                local.tee $l4
                local.get $l46
                f32.store
                local.get $l17
                local.get $l59
                local.get $l39
                f32.mul
                local.tee $l52
                f32.store
                local.get $l18
                local.get $l59
                local.get $l38
                f32.mul
                local.tee $l65
                f32.store
                local.get $l20
                local.get $l59
                local.get $l37
                f32.mul
                local.tee $l48
                f32.store
                local.get $p0
                f32.load
                local.set $l49
                local.get $p0
                f32.load offset=4
                local.set $l50
                local.get $p0
                f32.load offset=8
                local.set $l53
                local.get $p0
                f32.load offset=16
                local.set $l37
                local.get $p0
                f32.load offset=20
                local.set $l38
                local.get $p0
                f32.load offset=24
                local.set $l42
                local.get $p0
                f32.load offset=12
                local.set $l39
                local.get $p0
                f32.load offset=28
                local.set $l47
                local.get $p0
                f32.load offset=32
                local.set $l54
                local.get $l36
                local.get $l51
                local.get $p0
                f32.load offset=36
                local.tee $l55
                f32.mul
                local.tee $l56
                f32.store
                local.get $p2
                local.get $l45
                local.get $l54
                f32.mul
                local.tee $l57
                f32.store
                local.get $l4
                local.get $l46
                local.get $l47
                f32.mul
                local.tee $l58
                f32.store
                local.get $l21
                local.get $l43
                local.get $l42
                f32.mul
                local.get $l40
                local.get $l39
                f32.mul
                f32.sub
                local.get $l41
                local.get $l38
                f32.mul
                f32.sub
                local.get $l44
                local.get $l37
                f32.mul
                f32.sub
                local.tee $l51
                f32.store
                local.get $l33
                local.get $l40
                local.get $l37
                f32.mul
                local.get $l41
                local.get $l42
                f32.mul
                f32.sub
                local.get $l43
                local.get $l38
                f32.mul
                f32.sub
                local.get $l44
                local.get $l39
                f32.mul
                f32.sub
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                local.tee $p2
                i32.store
                local.get $l34
                local.get $l41
                local.get $l39
                f32.mul
                local.get $l40
                local.get $l38
                f32.mul
                f32.sub
                local.get $l44
                local.get $l42
                f32.mul
                f32.sub
                local.get $l43
                local.get $l37
                f32.mul
                f32.sub
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                local.tee $l4
                i32.store
                local.get $l35
                local.get $l44
                local.get $l38
                f32.mul
                local.get $l41
                local.get $l37
                f32.mul
                f32.sub
                local.get $l40
                local.get $l42
                f32.mul
                f32.sub
                local.get $l43
                local.get $l39
                f32.mul
                f32.sub
                i32.reinterpret_f32
                i32.const -2147483648
                i32.xor
                local.tee $l21
                i32.store
                local.get $l17
                local.get $l53
                local.get $l52
                local.get $l55
                f32.mul
                local.tee $l40
                local.get $l48
                local.get $l47
                f32.mul
                local.tee $l44
                local.get $l42
                local.get $l37
                f32.const -0x1p+1 (;=-2;)
                f32.mul
                local.tee $l43
                f32.mul
                local.tee $l47
                local.get $l39
                local.get $l38
                f32.const -0x1p+1 (;=-2;)
                f32.mul
                local.tee $l46
                f32.mul
                f32.sub
                f32.mul
                f32.add
                local.get $l40
                local.get $l39
                local.get $l39
                f32.const -0x1p+1 (;=-2;)
                f32.mul
                local.tee $l45
                f32.mul
                local.get $l37
                local.get $l37
                local.get $l37
                f32.add
                local.tee $l52
                f32.mul
                f32.sub
                f32.mul
                local.get $l65
                local.get $l54
                f32.mul
                local.tee $l41
                local.get $l37
                local.get $l38
                local.get $l38
                f32.add
                local.tee $l54
                f32.mul
                local.get $l42
                local.get $l45
                f32.mul
                local.tee $l65
                f32.sub
                f32.mul
                f32.add
                f32.add
                f32.add
                local.tee $l48
                f32.store
                local.get $l18
                local.get $l50
                local.get $l41
                local.get $l44
                local.get $l39
                local.get $l52
                f32.mul
                local.get $l42
                local.get $l46
                f32.mul
                local.tee $l42
                f32.sub
                f32.mul
                f32.add
                local.get $l40
                local.get $l65
                local.get $l43
                local.get $l38
                f32.mul
                f32.sub
                f32.mul
                local.get $l41
                local.get $l38
                local.get $l46
                f32.mul
                local.get $l39
                local.get $l39
                local.get $l39
                f32.add
                local.tee $l46
                f32.mul
                f32.sub
                f32.mul
                f32.add
                f32.add
                f32.add
                local.tee $l52
                f32.store
                local.get $l20
                local.get $l49
                local.get $l44
                local.get $l44
                local.get $l37
                local.get $l43
                f32.mul
                local.get $l38
                local.get $l54
                f32.mul
                f32.sub
                f32.mul
                f32.add
                local.get $l40
                local.get $l46
                local.get $l38
                f32.mul
                local.get $l47
                f32.sub
                f32.mul
                local.get $l41
                local.get $l42
                local.get $l37
                local.get $l45
                f32.mul
                f32.sub
                f32.mul
                f32.add
                f32.add
                f32.add
                local.tee $l41
                f32.store
                local.get $l10
                i32.const 1
                i32.le_u
                if $I161
                  local.get $l20
                  local.get $l41
                  local.get $l56
                  f32.const -0x0p+0 (;=-0;)
                  f32.mul
                  local.tee $l42
                  local.get $l21
                  f32.reinterpret_i32
                  local.tee $l37
                  local.get $l37
                  f32.add
                  local.tee $l47
                  local.get $p2
                  f32.reinterpret_i32
                  local.tee $l38
                  f32.mul
                  local.get $l51
                  local.get $l4
                  f32.reinterpret_i32
                  local.tee $l39
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l43
                  f32.mul
                  local.tee $l54
                  f32.sub
                  f32.mul
                  local.get $l57
                  f32.const -0x0p+0 (;=-0;)
                  f32.mul
                  local.tee $l40
                  local.get $l51
                  local.get $l38
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l46
                  f32.mul
                  local.tee $l65
                  local.get $l37
                  f32.const -0x1p+1 (;=-2;)
                  f32.mul
                  local.tee $l45
                  local.get $l39
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  local.get $l58
                  local.get $l6
                  i32.load offset=40
                  local.get $l28
                  i32.add
                  local.tee $p2
                  i32.load offset=16
                  local.get $p2
                  i32.const 16
                  i32.add
                  i32.add
                  local.get $p2
                  i32.load offset=4
                  local.get $p2
                  i32.const 4
                  i32.add
                  i32.add
                  local.get $l6
                  i32.const 24
                  i32.const 20
                  local.get $l10
                  select
                  i32.add
                  i32.load offset=56
                  i32.const 3
                  i32.shl
                  i32.add
                  i32.load offset=4
                  i32.const 76
                  i32.mul
                  i32.add
                  f32.load offset=68
                  f32.neg
                  f32.mul
                  local.tee $l44
                  local.get $l44
                  local.get $l43
                  local.get $l39
                  f32.mul
                  local.get $l38
                  local.get $l38
                  f32.add
                  local.tee $l49
                  local.get $l38
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.store
                  local.get $l18
                  local.get $l52
                  local.get $l42
                  local.get $l51
                  local.get $l45
                  f32.mul
                  local.tee $l41
                  local.get $l43
                  local.get $l38
                  f32.mul
                  f32.sub
                  f32.mul
                  local.get $l40
                  local.get $l46
                  local.get $l38
                  f32.mul
                  local.get $l47
                  local.get $l37
                  f32.mul
                  f32.sub
                  f32.mul
                  f32.add
                  local.get $l40
                  local.get $l39
                  local.get $l39
                  f32.add
                  local.tee $l38
                  local.get $l37
                  f32.mul
                  local.get $l65
                  f32.sub
                  local.get $l44
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.store
                  local.get $l17
                  local.get $l48
                  local.get $l42
                  local.get $l45
                  local.get $l37
                  f32.mul
                  local.get $l38
                  local.get $l39
                  f32.mul
                  f32.sub
                  f32.mul
                  local.get $l40
                  local.get $l49
                  local.get $l39
                  f32.mul
                  local.get $l41
                  f32.sub
                  f32.mul
                  f32.add
                  local.get $l42
                  local.get $l54
                  local.get $l46
                  local.get $l37
                  f32.mul
                  f32.sub
                  local.get $l44
                  f32.mul
                  f32.add
                  f32.add
                  f32.add
                  f32.store
                end
                local.get $l10
                i32.const 1
                i32.add
                local.tee $l10
                i32.const 4
                i32.ne
                br_if $L160
              end
              local.get $l6
              i32.load offset=44
              local.tee $p0
              local.get $l6
              i32.const 44
              i32.add
              local.tee $l10
              i32.add
              i32.const 0
              local.get $p0
              select
              local.get $l19
              call $f68263
              local.get $l29
              if $I162
                local.get $l6
                local.get $l7
                call $f68292
              end
              local.get $l6
              local.get $l7
              local.get $l19
              call $f68293
              local.get $l6
              i32.load8_u offset=290
              if $I163
                local.get $l6
                local.get $l7
                local.get $l6
                i32.load offset=44
                local.tee $p0
                local.get $l10
                i32.add
                i32.const 0
                local.get $p0
                select
                local.get $l19
                local.get $l9
                call $f68306
              end
              local.get $l28
              i32.load
              local.tee $p0
              local.get $l28
              i32.add
              i32.const 0
              local.get $p0
              select
              local.get $l19
              local.get $l9
              call $f68265
              f32.const 0x0p+0 (;=0;)
              local.set $l38
              i32.const 0
              local.set $p0
              f32.const 0x0p+0 (;=0;)
              local.set $l39
              f32.const 0x0p+0 (;=0;)
              local.set $l42
              f32.const 0x0p+0 (;=0;)
              local.set $l40
              loop $L164
                local.get $l6
                local.get $p0
                i32.const 2
                i32.shl
                i32.add
                local.tee $p2
                i32.load offset=56
                i32.const 0
                i32.ge_s
                if $I165
                  local.get $p2
                  f32.load offset=156
                  local.set $l37
                  local.get $l22
                  local.get $l6
                  local.get $l9
                  local.get $p0
                  call $f68290
                  local.get $l39
                  local.get $l37
                  local.get $l22
                  f32.load offset=8
                  f32.mul
                  f32.add
                  local.set $l39
                  local.get $l40
                  local.get $l37
                  local.get $l22
                  f32.load
                  f32.mul
                  f32.add
                  local.set $l40
                  local.get $l42
                  local.get $l37
                  local.get $l22
                  f32.load offset=4
                  f32.mul
                  f32.add
                  local.set $l42
                  local.get $l38
                  local.get $l37
                  f32.add
                  local.set $l38
                end
                local.get $p0
                i32.const 1
                i32.add
                local.tee $p0
                i32.const 25
                i32.ne
                br_if $L164
              end
              local.get $l22
              local.get $l6
              local.get $l9
              call $f68291
              local.get $l22
              f32.load offset=12
              local.set $l41
              local.get $l22
              i32.load offset=8
              local.set $l17
              local.get $l22
              i32.load
              local.set $l18
              local.get $l22
              i32.load offset=4
              local.set $l20
              local.get $l30
              i32.const 40
              i32.mul
              local.tee $p2
              local.get $l9
              i32.const 4
              i32.add
              local.tee $l21
              local.get $l9
              i32.load offset=4
              i32.add
              i32.add
              local.tee $p0
              f32.load offset=16
              local.set $l43
              local.get $p0
              f32.load offset=20
              local.set $l59
              local.get $p0
              f32.load offset=24
              local.set $l46
              local.get $p0
              f32.load offset=12
              local.set $l45
              local.get $p0
              f32.load
              local.set $l37
              local.get $p0
              f32.load offset=4
              local.set $l65
              local.get $p0
              f32.load offset=8
              local.set $l52
              local.get $l19
              i32.const 4
              i32.add
              local.tee $l4
              local.get $l19
              i32.load offset=4
              i32.add
              local.get $p2
              i32.add
              local.tee $p0
              i32.const 1065353216
              i32.store offset=36
              local.get $p0
              i64.const 4575657222473777152
              i64.store offset=28 align=4
              local.get $p0
              local.get $l37
              local.get $l40
              local.get $l38
              f32.div
              f32.sub
              local.tee $l47
              local.get $l41
              local.get $l20
              i32.const -2147483648
              i32.xor
              f32.reinterpret_i32
              local.tee $l37
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l54
              f32.mul
              local.tee $l48
              local.get $l17
              i32.const -2147483648
              i32.xor
              f32.reinterpret_i32
              local.tee $l40
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l51
              local.get $l18
              i32.const -2147483648
              i32.xor
              f32.reinterpret_i32
              local.tee $l44
              f32.mul
              f32.sub
              f32.mul
              local.get $l52
              local.get $l39
              local.get $l38
              f32.div
              f32.sub
              local.tee $l39
              f32.add
              local.get $l40
              local.get $l40
              f32.add
              local.tee $l49
              local.get $l37
              f32.mul
              local.get $l41
              local.get $l44
              f32.const -0x1p+1 (;=-2;)
              f32.mul
              local.tee $l52
              f32.mul
              local.tee $l50
              f32.sub
              local.get $l65
              local.get $l42
              local.get $l38
              f32.div
              f32.sub
              local.tee $l38
              f32.mul
              local.get $l52
              local.get $l44
              f32.mul
              local.get $l37
              local.get $l37
              f32.add
              local.tee $l42
              local.get $l37
              f32.mul
              f32.sub
              local.get $l39
              f32.mul
              f32.add
              f32.add
              f32.store offset=8
              local.get $p0
              local.get $l38
              local.get $l47
              local.get $l42
              local.get $l44
              f32.mul
              local.get $l41
              local.get $l51
              f32.mul
              local.tee $l42
              f32.sub
              f32.mul
              f32.add
              local.get $l51
              local.get $l40
              f32.mul
              local.get $l44
              local.get $l44
              f32.add
              local.tee $l51
              local.get $l44
              f32.mul
              f32.sub
              local.get $l38
              f32.mul
              local.get $l50
              local.get $l54
              local.get $l40
              f32.mul
              f32.sub
              local.get $l39
              f32.mul
              f32.add
              f32.add
              f32.store offset=4
              local.get $p0
              local.get $l47
              local.get $l47
              local.get $l54
              local.get $l37
              f32.mul
              local.get $l49
              local.get $l40
              f32.mul
              f32.sub
              f32.mul
              f32.add
              local.get $l42
              local.get $l52
              local.get $l37
              f32.mul
              f32.sub
              local.get $l38
              f32.mul
              local.get $l51
              local.get $l40
              f32.mul
              local.get $l48
              f32.sub
              local.get $l39
              f32.mul
              f32.add
              f32.add
              f32.store
              local.get $p0
              local.get $l41
              local.get $l46
              f32.mul
              local.get $l45
              local.get $l44
              f32.mul
              f32.sub
              local.get $l59
              local.get $l40
              f32.mul
              f32.sub
              local.get $l43
              local.get $l37
              f32.mul
              f32.sub
              f32.store offset=24
              local.get $p0
              local.get $l45
              local.get $l37
              f32.mul
              local.get $l41
              local.get $l59
              f32.mul
              f32.sub
              local.get $l46
              local.get $l40
              f32.mul
              f32.sub
              local.get $l43
              local.get $l44
              f32.mul
              f32.sub
              i32.reinterpret_f32
              i32.const -2147483648
              i32.xor
              i32.store offset=20
              local.get $p0
              local.get $l59
              local.get $l44
              f32.mul
              local.get $l45
              local.get $l40
              f32.mul
              f32.sub
              local.get $l41
              local.get $l43
              f32.mul
              f32.sub
              local.get $l46
              local.get $l37
              f32.mul
              f32.sub
              i32.reinterpret_f32
              i32.const -2147483648
              i32.xor
              i32.store offset=16
              local.get $p0
              local.get $l43
              local.get $l40
              f32.mul
              local.get $l59
              local.get $l37
              f32.mul
              f32.sub
              local.get $l41
              local.get $l45
              f32.mul
              f32.sub
              local.get $l46
              local.get $l44
              f32.mul
              f32.sub
              i32.reinterpret_f32
              i32.const -2147483648
              i32.xor
              i32.store offset=12
              local.get $l9
              i32.load offset=4
              local.get $l21
              i32.add
              local.get $p2
              i32.add
              local.tee $p0
              i64.load offset=28 align=4
              local.set $l107
              local.get $l19
              i32.load offset=4
              local.get $l4
              i32.add
              local.get $p2
              i32.add
              local.tee $p2
              local.get $p0
              f32.load offset=36
              f32.store offset=36
              local.get $p2
              local.get $l107
              i64.store offset=28 align=4
              block $B166
                local.get $l5
                i32.eqz
                br_if $B166
                local.get $l31
                local.get $l5
                i32.const 596
                i32.add
                i32.const 220
                call $f483
                drop
                local.get $l32
                local.get $l5
                i32.const 364
                i32.add
                i32.const 80
                call $f483
                drop
                local.get $l16
                local.get $l5
                i32.const 500
                i32.add
                i32.const 80
                call $f483
                drop
                local.get $l26
                local.get $l5
                i32.const 816
                i32.add
                i32.const 252
                call $f483
                drop
                local.get $l29
                if $I167
                  local.get $l6
                  local.get $l7
                  call $f68292
                end
                local.get $l6
                local.get $l7
                local.get $l19
                call $f68293
                local.get $l6
                i32.load8_u offset=290
                i32.eqz
                br_if $B166
                local.get $l6
                local.get $l7
                local.get $l6
                i32.load offset=44
                local.tee $p0
                local.get $l10
                i32.add
                i32.const 0
                local.get $p0
                select
                local.get $l19
                local.get $l9
                call $f68306
              end
              local.get $l7
              i64.load align=4
              local.set $l107
              local.get $l4
              i32.load
              local.get $l4
              i32.add
              local.tee $p0
              local.get $l7
              f32.load offset=8
              f32.store offset=8
              local.get $p0
              local.get $l107
              i64.store align=4
              local.get $l7
              i64.load offset=12 align=4
              local.set $l107
              local.get $p0
              local.get $l7
              i64.load offset=20 align=4
              i64.store offset=20 align=4
              local.get $p0
              local.get $l107
              i64.store offset=12 align=4
              local.get $l7
              f32.load offset=36
              local.set $l37
              local.get $p0
              local.get $l7
              i64.load offset=28 align=4
              i64.store offset=28 align=4
              local.get $p0
              local.get $l37
              f32.store offset=36
              local.get $l22
              i32.const 16
              i32.add
              global.set $g0
              local.get $l11
              i32.load offset=28
              i32.const 0
              i32.store offset=108
              local.get $l11
              i32.load offset=28
              i32.const 0
              i32.store offset=112
              local.get $l11
              i32.load offset=28
              i32.const 0
              i32.store offset=128
              local.get $l11
              i32.load offset=28
              i32.const 0
              i32.store offset=172
              local.get $l11
              i32.load offset=28
              i32.const 0
              i32.store offset=176
              local.get $l11
              i32.load offset=28
              i32.const 0
              i32.store offset=192
              local.get $l11
              i32.load offset=28
              i32.const 0
              i32.store offset=236
              local.get $l11
              i32.load offset=28
              i32.const 0
              i32.store offset=240
              local.get $l11
              i32.load offset=28
              i32.const 0
              i32.store offset=256
              local.get $l11
              i32.load offset=28
              i32.const 0
              i32.store offset=300
              local.get $l11
              i32.load offset=28
              i32.const 0
              i32.store offset=304
              local.get $l11
              i32.load offset=28
              i32.const 0
              i32.store offset=320
              local.get $l11
              i32.load offset=28
              local.tee $l16
              i64.const 0
              i64.store offset=52 align=4
              local.get $l16
              i64.const 0
              i64.store offset=60 align=4
              local.get $l23
              i32.load8_u offset=19
              i32.eqz
              br_if $B158
              i32.const 1
              local.get $l24
              local.get $l23
              local.get $l15
              local.get $l25
              local.get $l11
              call $f68369
              i32.const 0
              local.get $l24
              local.get $l23
              local.get $l15
              local.get $l25
              local.get $l11
              call $f68369
            end
            local.get $l13
            i32.const 1120
            i32.add
            global.set $g0
          end
          local.get $p1
          i32.const 1
          i32.add
          local.tee $p1
          local.get $l14
          i32.ne
          br_if $L152
        end
        local.get $l12
        i32.load offset=72
        local.tee $l10
        i32.eqz
        br_if $B151
        i32.const 0
        local.set $p1
        local.get $l12
        i32.load offset=64
        local.set $l14
        loop $L168
          local.get $l14
          local.get $p1
          call $f69092
          local.get $p1
          i32.const 1
          i32.add
          local.tee $p1
          local.get $l10
          i32.ne
          br_if $L168
        end
      end
      local.get $l12
      i32.load offset=40
      local.tee $l22
      i32.const 0
      i32.gt_s
      if $I169
        i32.const 0
        local.set $l4
        local.get $l12
        i32.load offset=32
        local.set $l7
        loop $L170
          local.get $l7
          local.get $l4
          i32.const 4
          i32.shl
          i32.add
          local.tee $l14
          i32.load offset=8
          local.tee $l8
          i32.const 0
          i32.gt_s
          if $I171
            i32.const 0
            local.set $p1
            loop $L172
              block $B173
                local.get $l14
                i32.load
                local.get $p1
                i32.const 72
                i32.mul
                i32.add
                local.tee $l10
                i32.load offset=56
                i32.load8_u offset=29
                i32.eqz
                br_if $B173
                local.get $l10
                i32.load offset=60
                i32.load
                i32.eqz
                br_if $B173
                local.get $l10
                i32.load offset=16
                local.get $l10
                call $f69093
              end
              local.get $p1
              i32.const 1
              i32.add
              local.tee $p1
              local.get $l8
              i32.ne
              br_if $L172
            end
          end
          local.get $l4
          i32.const 1
          i32.add
          local.tee $l4
          local.get $l22
          i32.ne
          br_if $L170
        end
      end
      i32.const 0
      local.set $p0
      local.get $p3
      i32.const 0
      i32.gt_s
      if $I174
        loop $L175
          block $B176
            local.get $l12
            i32.load offset=72
            i32.eqz
            br_if $B176
            i32.const 0
            local.set $l6
            loop $L177
              local.get $l12
              i32.load offset=64
              local.get $l6
              i32.const 72
              i32.mul
              i32.add
              local.tee $l7
              i32.const 60
              i32.add
              local.set $l8
              local.get $l7
              i32.const 56
              i32.add
              local.set $l14
              i32.const 0
              local.set $l22
              block $B178
                local.get $l7
                i32.load offset=16
                local.tee $l23
                i32.load offset=740
                i32.eqz
                br_if $B178
                local.get $l7
                i32.const 16
                i32.add
                local.set $l4
                local.get $l23
                i32.load offset=732
                local.set $p1
                loop $L179
                  local.get $l14
                  i32.load
                  i32.load8_u offset=29
                  i32.eqz
                  br_if $B178
                  local.get $l8
                  i32.load
                  i32.load
                  i32.eqz
                  br_if $B178
                  block $B180
                    local.get $p1
                    i32.load
                    local.tee $l10
                    i32.eqz
                    br_if $B180
                    local.get $l10
                    i32.load offset=16
                    local.get $p1
                    i32.load offset=4
                    i32.const -2
                    i32.and
                    i32.ne
                    br_if $B180
                    local.get $l10
                    i32.load offset=20
                    local.tee $l10
                    local.get $l10
                    i32.load
                    i32.load offset=156
                    call_indirect $__indirect_function_table (type $t5)
                    i32.eqz
                    br_if $B180
                    local.get $p0
                    local.get $p1
                    i32.load
                    i32.load offset=20
                    i32.load offset=188
                    local.tee $p2
                    i32.load
                    i32.lt_s
                    if $I181 (result i32)
                      local.get $p2
                      i32.load offset=4
                      local.get $p2
                      i32.const 4
                      i32.add
                      i32.add
                      local.get $p0
                      i32.const 2
                      i32.shl
                      i32.add
                      local.tee $l10
                      i32.load
                      local.get $l10
                      i32.add
                      i32.load8_u offset=36
                      i32.const 0
                      i32.ne
                    else
                      i32.const 0
                    end
                    local.get $l22
                    i32.or
                    local.set $l22
                  end
                  local.get $p1
                  i32.const 8
                  i32.add
                  local.tee $p1
                  local.get $l4
                  i32.load
                  local.tee $l10
                  i32.load offset=732
                  local.get $l10
                  i32.load offset=740
                  i32.const 3
                  i32.shl
                  i32.add
                  i32.ne
                  br_if $L179
                end
              end
              local.get $p0
              i32.eqz
              local.get $l14
              i32.load
              local.tee $p1
              i32.load offset=4
              i32.load8_u offset=20
              i32.const 0
              i32.ne
              i32.and
              local.get $l22
              i32.or
              i32.const 1
              i32.and
              local.tee $l10
              if $I182
                global.get $g0
                i32.const 16
                i32.sub
                local.tee $p1
                global.set $g0
                local.get $l23
                local.get $l23
                i32.load offset=228
                i32.const 4
                i32.or
                i32.store offset=228
                local.get $l23
                i32.load offset=28
                i32.load offset=56
                i32.const 1
                i32.const 4676756
                i32.load
                i32.shl
                i32.const 4676752
                i32.load
                i32.const 28
                i32.shl
                i32.const 31
                i32.shr_s
                i32.and
                i32.and
                if $I183
                  local.get $p1
                  i32.const 0
                  i32.store offset=8
                  local.get $p1
                  i32.const 4131744
                  i32.store
                  local.get $p1
                  local.get $p0
                  i32.store offset=4
                  local.get $l23
                  i32.const 4676740
                  local.get $p1
                  call $f80200
                end
                i32.const 4782136
                i32.load
                i32.const 1
                i32.or
                call $f80130
                local.set $p2
                local.get $l23
                i32.const 16
                local.get $l7
                local.get $p0
                call $f69095
                drop
                local.get $p2
                call $f80130
                drop
                local.get $l23
                local.get $l23
                i32.load offset=228
                i32.const -5
                i32.and
                i32.store offset=228
                local.get $p1
                i32.const 16
                i32.add
                global.set $g0
                local.get $l14
                i32.load
                local.set $p1
              end
              block $B184
                local.get $p1
                i32.load8_u offset=29
                i32.eqz
                br_if $B184
                local.get $l8
                i32.load
                i32.load
                i32.eqz
                br_if $B184
                local.get $p1
                i32.load offset=16
                i32.const 0
                i32.store8 offset=52
                local.get $l14
                i32.load
                i32.load offset=16
                local.get $l10
                i32.store8 offset=53
                local.get $l14
                i32.load
                i32.load offset=16
                local.get $l10
                i32.store8 offset=54
              end
              local.get $l6
              i32.const 1
              i32.add
              local.tee $l6
              local.get $l12
              i32.load offset=72
              local.tee $l10
              i32.lt_u
              br_if $L177
            end
            local.get $l10
            i32.eqz
            br_if $B176
            i32.const 0
            local.set $p1
            local.get $l12
            i32.load offset=64
            local.set $l14
            loop $L185
              local.get $l14
              local.get $p1
              call $f69092
              local.get $p1
              i32.const 1
              i32.add
              local.tee $p1
              local.get $l10
              i32.ne
              br_if $L185
            end
          end
          local.get $l12
          i32.load offset=40
          local.tee $l22
          i32.const 0
          i32.gt_s
          if $I186
            i32.const 0
            local.set $l4
            local.get $l12
            i32.load offset=32
            local.set $l7
            loop $L187
              local.get $l7
              local.get $l4
              i32.const 4
              i32.shl
              i32.add
              local.tee $l14
              i32.load offset=8
              local.tee $l8
              i32.const 0
              i32.gt_s
              if $I188
                i32.const 0
                local.set $p1
                loop $L189
                  block $B190
                    local.get $l14
                    i32.load
                    local.get $p1
                    i32.const 72
                    i32.mul
                    i32.add
                    local.tee $l10
                    i32.load offset=56
                    i32.load8_u offset=29
                    i32.eqz
                    br_if $B190
                    local.get $l10
                    i32.load offset=60
                    i32.load
                    i32.eqz
                    br_if $B190
                    local.get $l10
                    i32.load offset=16
                    local.get $l10
                    call $f69093
                  end
                  local.get $p1
                  i32.const 1
                  i32.add
                  local.tee $p1
                  local.get $l8
                  i32.ne
                  br_if $L189
                end
              end
              local.get $l4
              i32.const 1
              i32.add
              local.tee $l4
              local.get $l22
              i32.ne
              br_if $L187
            end
          end
          local.get $p0
          i32.const 1
          i32.add
          local.tee $p0
          local.get $p3
          i32.ne
          br_if $L175
        end
      end
      local.get $l12
      i32.load offset=56
      local.tee $l22
      i32.const 0
      i32.gt_s
      if $I191
        i32.const 0
        local.set $l4
        local.get $l12
        i32.load offset=48
        local.set $l7
        loop $L192
          local.get $l7
          local.get $l4
          i32.const 4
          i32.shl
          i32.add
          local.tee $l14
          i32.load offset=8
          local.tee $l8
          i32.const 0
          i32.gt_s
          if $I193
            i32.const 0
            local.set $p1
            loop $L194
              block $B195
                local.get $l14
                i32.load
                local.get $p1
                i32.const 72
                i32.mul
                i32.add
                local.tee $l10
                i32.load offset=56
                i32.load8_u offset=29
                i32.eqz
                br_if $B195
                local.get $l10
                i32.load offset=60
                i32.load
                i32.eqz
                br_if $B195
                local.get $l10
                i32.load offset=16
                local.get $l10
                call $f69093
              end
              local.get $p1
              i32.const 1
              i32.add
              local.tee $p1
              local.get $l8
              i32.ne
              br_if $L194
            end
          end
          local.get $l4
          i32.const 1
          i32.add
          local.tee $l4
          local.get $l22
          i32.ne
          br_if $L192
        end
      end
      i32.const 4782136
      i32.load
      i32.const 1
      i32.or
      call $f80130
      local.set $l10
      local.get $l12
      i32.load offset=88
      if $I196
        i32.const 0
        local.set $p1
        loop $L197
          local.get $l106
          local.set $l37
          block $B198
            local.get $l12
            i32.load offset=80
            local.get $p1
            i32.const 72
            i32.mul
            i32.add
            i32.load offset=16
            local.tee $p0
            i32.load offset=28
            local.tee $p2
            i32.eqz
            br_if $B198
            local.get $p2
            call $f80180
            i32.eqz
            br_if $B198
            local.get $p0
            i32.load8_u offset=216
            i32.eqz
            br_if $B198
            local.get $p0
            local.get $p0
            i32.load offset=228
            i32.const 16
            i32.or
            i32.store offset=228
            local.get $p0
            i32.load offset=292
            local.get $p0
            i32.load offset=260
            i32.load
            call $f68808
            local.get $p0
            i32.load8_u offset=216
            if $I199
              local.get $p0
              i32.load offset=292
              local.get $p0
              i32.load offset=260
              i32.load
              call $f68806
              local.get $p0
              i32.load offset=292
              local.get $p0
              i32.load offset=260
              i32.load
              call $f68807
              local.get $p0
              i32.load offset=28
              i32.const 4131408
              call $f80185
              call $f78085
              block $B200
                local.get $p0
                i32.load offset=224
                i32.const 2
                i32.eq
                if $I201
                  i32.const 4129880
                  i32.load8_u
                  br_if $B200
                end
                local.get $l100
                local.set $l37
              end
              block $B202
                local.get $p0
                i32.load offset=236
                i32.eqz
                br_if $B202
                local.get $p0
                i32.load offset=932
                local.tee $p2
                i32.eqz
                br_if $B202
                local.get $p0
                i32.load offset=900
                i32.const 2
                i32.ne
                br_if $B202
                local.get $p0
                f32.load offset=720
                local.tee $l38
                f32.const 0x0p+0 (;=0;)
                f32.ge
                i32.eqz
                br_if $B202
                local.get $l37
                local.get $l38
                f32.mul
                local.set $l37
                local.get $p0
                i32.load offset=264
                local.set $l6
                local.get $p2
                i32.load offset=196
                local.set $l8
                i32.const 0
                local.set $l11
                global.get $g0
                i32.const 80
                i32.sub
                local.tee $p3
                global.set $g0
                block $B203
                  local.get $p0
                  i32.const 856
                  i32.add
                  local.tee $p2
                  i32.load offset=20
                  i32.const -1
                  i32.eq
                  if $I204
                    local.get $p3
                    i32.const 403047
                    i32.store offset=60
                    local.get $p3
                    i32.const 403047
                    i32.store offset=56
                    local.get $p3
                    i64.const 0
                    i64.store offset=48
                    local.get $p3
                    i32.const 1
                    i32.store8 offset=44
                    local.get $p3
                    i32.const 403047
                    i32.store offset=12
                    local.get $p3
                    i32.const 403047
                    i32.store offset=8
                    local.get $p3
                    i32.const 403047
                    i32.store offset=4
                    local.get $p3
                    i64.const 0
                    i64.store offset=36 align=4
                    local.get $p3
                    i64.const 512
                    i64.store offset=28 align=4
                    local.get $p3
                    i64.const -4294967194
                    i64.store offset=20 align=4
                    local.get $p3
                    i32.const 403047
                    i32.store offset=16
                    local.get $p3
                    i32.const 275533
                    i32.store
                    local.get $p3
                    call $f83275
                    br $B203
                  end
                  local.get $p2
                  i32.load offset=24
                  i32.const -1
                  i32.eq
                  if $I205 (result f32)
                    f32.const 0x0p+0 (;=0;)
                  else
                    local.get $p2
                    i32.load offset=4
                    local.get $p2
                    i32.load offset=32
                    i32.const 12
                    i32.mul
                    i32.add
                    f32.load offset=8
                    local.get $l37
                    f32.add
                  end
                  local.set $l37
                  local.get $p3
                  i64.const 4294967296
                  i64.store offset=72
                  local.get $p3
                  i64.const 322122547200
                  i64.store offset=64
                  local.get $p3
                  local.get $p3
                  i32.const -64
                  i32.sub
                  call $f68356
                  local.tee $l7
                  i32.const 0
                  i32.store8 offset=41
                  local.get $l7
                  local.get $l6
                  call $f69105
                  local.get $p2
                  i32.const 36
                  i32.add
                  local.tee $l4
                  local.get $p3
                  i32.load offset=72
                  i32.const 16
                  local.get $p2
                  i32.load offset=36
                  i32.load
                  call_indirect $__indirect_function_table (type $t3)
                  local.tee $l6
                  if $I206
                    local.get $l6
                    local.get $p3
                    i32.load offset=64
                    local.get $p3
                    i32.load offset=72
                    call $f483
                    drop
                  end
                  local.get $l7
                  i32.const 44
                  i32.add
                  call $f554
                  drop
                  local.get $p3
                  i32.const -64
                  i32.sub
                  call $f554
                  drop
                  local.get $l8
                  if $I207
                    local.get $p3
                    i64.const 4294967296
                    i64.store offset=72
                    local.get $p3
                    i64.const 322122547200
                    i64.store offset=64
                    local.get $p3
                    local.get $p3
                    i32.const -64
                    i32.sub
                    call $f68356
                    local.tee $l7
                    i32.const 0
                    i32.store8 offset=41
                    local.get $l7
                    local.get $l8
                    call $f68813
                    local.get $l4
                    local.get $p3
                    i32.load offset=72
                    i32.const 16
                    local.get $l4
                    i32.load
                    i32.load
                    call_indirect $__indirect_function_table (type $t3)
                    local.tee $l11
                    if $I208
                      local.get $l11
                      local.get $p3
                      i32.load offset=64
                      local.get $p3
                      i32.load offset=72
                      call $f483
                      drop
                    end
                    local.get $l7
                    i32.const 44
                    i32.add
                    call $f554
                    drop
                    local.get $p3
                    i32.const -64
                    i32.sub
                    call $f554
                    drop
                  end
                  local.get $p2
                  i32.load offset=32
                  i32.const 1
                  i32.add
                  local.set $l8
                  local.get $p2
                  i32.load offset=20
                  local.tee $l7
                  i32.const 0
                  i32.gt_s
                  if $I209
                    local.get $p2
                    local.get $l8
                    local.get $l7
                    i32.rem_s
                    local.tee $l8
                    i32.store offset=32
                    local.get $l8
                    local.get $p2
                    i32.load offset=24
                    local.tee $l4
                    i32.ne
                    local.get $l4
                    i32.const -1
                    i32.ne
                    i32.and
                    i32.eqz
                    if $I210
                      local.get $p2
                      local.get $l4
                      i32.const 1
                      i32.add
                      local.get $l7
                      i32.rem_s
                      i32.store offset=24
                    end
                    local.get $p2
                    local.get $l8
                    i32.store offset=28
                    local.get $p2
                    i32.load offset=4
                    local.get $l8
                    i32.const 12
                    i32.mul
                    i32.add
                    i32.load
                    local.get $p2
                    i32.const 40
                    i32.add
                    local.tee $l8
                    i32.load
                    i32.const 403047
                    i32.const 36
                    call $f83342
                    local.get $p2
                    i32.load offset=4
                    local.get $p2
                    i32.load offset=32
                    i32.const 12
                    i32.mul
                    i32.add
                    i32.load offset=4
                    local.get $l8
                    i32.load
                    i32.const 403047
                    i32.const 36
                    call $f83342
                    local.get $p2
                    i32.load offset=4
                    local.get $p2
                    i32.load offset=32
                    i32.const 12
                    i32.mul
                    i32.add
                    local.tee $p2
                    local.get $l37
                    f32.store offset=8
                    local.get $p2
                    local.get $l11
                    i32.store offset=4
                    local.get $p2
                    local.get $l6
                    i32.store
                    br $B203
                  end
                  local.get $p2
                  local.get $l8
                  i32.store offset=32
                  local.get $l8
                  local.get $p2
                  i32.load offset=24
                  local.tee $l7
                  i32.ne
                  local.get $l7
                  i32.const -1
                  i32.ne
                  i32.and
                  i32.eqz
                  if $I211
                    local.get $p2
                    local.get $l7
                    i32.const 1
                    i32.add
                    i32.store offset=24
                  end
                  local.get $p2
                  local.get $l8
                  i32.store offset=28
                  local.get $p2
                  i32.load offset=12
                  local.tee $l8
                  i32.const 1
                  i32.add
                  local.tee $l7
                  local.get $p2
                  i32.load offset=16
                  i32.const 1
                  i32.shr_u
                  i32.gt_u
                  if $I212
                    local.get $p2
                    i32.const 4
                    i32.add
                    call $f65727
                  end
                  local.get $p2
                  local.get $l7
                  i32.store offset=12
                  local.get $p2
                  i32.load offset=4
                  local.get $l8
                  i32.const 12
                  i32.mul
                  i32.add
                  local.tee $p2
                  local.get $l37
                  f32.store offset=8
                  local.get $p2
                  local.get $l11
                  i32.store offset=4
                  local.get $p2
                  local.get $l6
                  i32.store
                end
                local.get $p3
                i32.const 80
                i32.add
                global.set $g0
              end
              local.get $p0
              i32.load offset=264
              local.get $l100
              call $f68374
            end
            local.get $p0
            local.get $p0
            i32.load offset=228
            i32.const -17
            i32.and
            i32.store offset=228
          end
          local.get $p1
          i32.const 1
          i32.add
          local.tee $p1
          local.get $l12
          i32.load offset=88
          i32.lt_u
          br_if $L197
        end
      end
      local.get $l10
      call $f80130
      drop
      local.get $l12
      i32.const 32
      i32.add
      call $f69101
      local.get $l12
      i32.const 48
      i32.add
      call $f69101
      local.get $l12
      i32.const -64
      i32.sub
      call $f69094
      local.get $l12
      i32.const 80
      i32.add
      call $f69094
    end
    local.get $l12
    i32.const 96
    i32.add
    global.set $g0)
