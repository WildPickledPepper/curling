  (func $f70079 (type $t32) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (param $p9 i32) (result i32)
    (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32)
    global.get $g0
    i32.const 6368
    i32.sub
    local.tee $l10
    global.set $g0
    local.get $p7
    f32.load
    local.set $l36
    local.get $l10
    i32.const 6360
    i32.add
    local.tee $l15
    local.get $p7
    i32.load offset=12
    i32.store
    local.get $l10
    local.get $p7
    i64.load offset=4 align=4
    i64.store offset=6352
    local.get $p1
    f32.load offset=48
    local.set $l39
    local.get $p1
    f32.load offset=52
    local.set $l40
    local.get $p1
    f32.load offset=56
    local.set $l41
    local.get $p0
    f32.load offset=48
    local.set $l42
    local.get $p0
    f32.load offset=52
    local.set $l43
    local.get $p0
    f32.load offset=56
    local.set $l44
    local.get $p5
    i32.const 52
    i32.add
    local.tee $l12
    f32.load
    local.set $l45
    local.get $p5
    i32.const 36
    i32.add
    local.tee $l13
    f32.load
    local.set $l26
    local.get $p5
    i32.const 20
    i32.add
    local.tee $l11
    f32.load
    local.set $l30
    local.get $p5
    i32.const 56
    i32.add
    local.tee $l16
    f32.load
    local.set $l46
    local.get $p5
    i32.const 40
    i32.add
    local.tee $l17
    f32.load
    local.set $l31
    local.get $p5
    i32.const 24
    i32.add
    local.tee $l18
    f32.load
    local.set $l32
    local.get $p0
    f32.load offset=44
    local.set $l47
    local.get $p1
    f32.load offset=44
    local.set $l48
    local.get $p0
    f32.load
    local.set $l27
    local.get $p5
    f32.load offset=48
    local.set $l49
    local.get $p5
    f32.load offset=32
    local.set $l28
    local.get $p5
    f32.load
    local.set $l29
    local.get $p5
    f32.load offset=16
    local.set $l33
    local.get $p0
    f32.load offset=4
    local.set $l34
    local.get $p5
    f32.load offset=4
    local.set $l35
    local.get $p0
    f32.load offset=8
    local.set $l37
    local.get $p1
    f32.load offset=8
    local.set $l23
    local.get $p5
    f32.load offset=8
    local.set $l38
    local.get $p1
    f32.load
    local.set $l24
    local.get $p1
    f32.load offset=4
    local.set $l25
    local.get $l10
    i32.const 0
    i32.store offset=6284
    local.get $l10
    local.get $l46
    local.get $l24
    local.get $l38
    f32.mul
    local.get $l25
    local.get $l32
    f32.mul
    f32.add
    local.get $l23
    local.get $l31
    f32.mul
    f32.add
    f32.add
    local.get $l37
    f32.sub
    local.tee $l50
    f32.store offset=6280
    local.get $l10
    local.get $l45
    local.get $l24
    local.get $l35
    f32.mul
    local.get $l25
    local.get $l30
    f32.mul
    f32.add
    local.get $l23
    local.get $l26
    f32.mul
    f32.add
    f32.add
    local.get $l34
    f32.sub
    local.tee $l51
    f32.store offset=6276
    local.get $l10
    local.get $l49
    local.get $l24
    local.get $l29
    f32.mul
    local.get $l25
    local.get $l33
    f32.mul
    f32.add
    local.get $l23
    local.get $l28
    f32.mul
    f32.add
    f32.add
    local.get $l27
    f32.sub
    local.tee $l52
    f32.store offset=6272
    local.get $l10
    i32.const 6256
    i32.add
    local.get $p2
    local.get $l10
    i32.const 6272
    i32.add
    local.get $p2
    i32.load
    i32.load offset=8
    call_indirect $__indirect_function_table (type $t2)
    local.get $p4
    i32.const 36
    i32.add
    local.tee $l19
    f32.load
    local.set $l26
    local.get $p4
    i32.const 20
    i32.add
    local.tee $l20
    f32.load
    local.set $l30
    local.get $p4
    i32.const 40
    i32.add
    local.tee $l21
    f32.load
    local.set $l31
    local.get $p4
    i32.const 24
    i32.add
    local.tee $l22
    f32.load
    local.set $l24
    local.get $p4
    f32.load offset=32
    local.set $l32
    local.get $p4
    f32.load offset=16
    local.set $l27
    local.get $p4
    f32.load
    local.set $l28
    local.get $p4
    f32.load offset=4
    local.set $l29
    local.get $p4
    f32.load offset=8
    local.set $l25
    local.get $l10
    i32.const 0
    i32.store offset=6252
    local.get $l10
    local.get $l24
    local.get $l10
    f32.load offset=6276
    f32.neg
    local.tee $l23
    f32.mul
    local.get $l25
    local.get $l10
    f32.load offset=6272
    local.tee $l24
    f32.mul
    f32.sub
    local.get $l31
    local.get $l10
    f32.load offset=6280
    local.tee $l25
    f32.mul
    f32.sub
    f32.store offset=6248
    local.get $l10
    local.get $l30
    local.get $l23
    f32.mul
    local.get $l24
    local.get $l29
    f32.mul
    f32.sub
    local.get $l25
    local.get $l26
    f32.mul
    f32.sub
    f32.store offset=6244
    local.get $l10
    local.get $l27
    local.get $l23
    f32.mul
    local.get $l24
    local.get $l28
    f32.mul
    f32.sub
    local.get $l25
    local.get $l32
    f32.mul
    f32.sub
    f32.store offset=6240
    local.get $l10
    i32.const 6224
    i32.add
    local.get $p3
    local.get $l10
    i32.const 6240
    i32.add
    local.get $p3
    i32.load
    i32.load offset=8
    call_indirect $__indirect_function_table (type $t2)
    local.get $p4
    f32.load offset=52
    local.set $l26
    local.get $l19
    f32.load
    local.set $l30
    local.get $l20
    f32.load
    local.set $l31
    local.get $p4
    f32.load offset=56
    local.set $l32
    local.get $l21
    f32.load
    local.set $l27
    local.get $l22
    f32.load
    local.set $l25
    local.get $p4
    f32.load offset=48
    local.set $l28
    local.get $p4
    f32.load offset=32
    local.set $l29
    local.get $p4
    f32.load
    local.set $l33
    local.get $p4
    f32.load offset=16
    local.set $l34
    local.get $p4
    f32.load offset=4
    local.set $l35
    local.get $p4
    f32.load offset=8
    local.set $l24
    local.get $l10
    i32.const 0
    i32.store offset=6220
    local.get $l10
    local.get $l32
    local.get $l24
    local.get $l10
    f32.load offset=6256
    local.tee $l23
    f32.mul
    local.get $l25
    local.get $l10
    f32.load offset=6260
    local.tee $l24
    f32.mul
    f32.add
    local.get $l27
    local.get $l10
    f32.load offset=6264
    local.tee $l25
    f32.mul
    f32.add
    f32.add
    f32.store offset=6216
    local.get $l10
    local.get $l26
    local.get $l23
    local.get $l35
    f32.mul
    local.get $l24
    local.get $l31
    f32.mul
    f32.add
    local.get $l25
    local.get $l30
    f32.mul
    f32.add
    f32.add
    f32.store offset=6212
    local.get $l10
    local.get $l28
    local.get $l23
    local.get $l33
    f32.mul
    local.get $l24
    local.get $l34
    f32.mul
    f32.add
    local.get $l25
    local.get $l29
    f32.mul
    f32.add
    f32.add
    f32.store offset=6208
    local.get $l12
    f32.load
    local.set $l26
    local.get $l13
    f32.load
    local.set $l30
    local.get $l11
    f32.load
    local.set $l31
    local.get $l16
    f32.load
    local.set $l32
    local.get $l17
    f32.load
    local.set $l27
    local.get $l18
    f32.load
    local.set $l25
    local.get $p5
    f32.load offset=48
    local.set $l28
    local.get $p5
    f32.load offset=32
    local.set $l29
    local.get $p5
    f32.load
    local.set $l33
    local.get $p5
    f32.load offset=16
    local.set $l34
    local.get $p5
    f32.load offset=4
    local.set $l35
    local.get $p5
    f32.load offset=8
    local.set $l24
    local.get $l10
    i32.const 0
    i32.store offset=6204
    local.get $l10
    local.get $l32
    local.get $l24
    local.get $l10
    f32.load offset=6224
    local.tee $l23
    f32.mul
    local.get $l25
    local.get $l10
    f32.load offset=6228
    local.tee $l24
    f32.mul
    f32.add
    local.get $l27
    local.get $l10
    f32.load offset=6232
    local.tee $l25
    f32.mul
    f32.add
    f32.add
    f32.store offset=6200
    local.get $l10
    local.get $l26
    local.get $l23
    local.get $l35
    f32.mul
    local.get $l24
    local.get $l31
    f32.mul
    f32.add
    local.get $l25
    local.get $l30
    f32.mul
    f32.add
    f32.add
    f32.store offset=6196
    local.get $l10
    local.get $l28
    local.get $l23
    local.get $l33
    f32.mul
    local.get $l24
    local.get $l34
    f32.mul
    f32.add
    local.get $l25
    local.get $l29
    f32.mul
    f32.add
    f32.add
    f32.store offset=6192
    local.get $l10
    i32.const 0
    i32.store offset=3112
    local.get $l10
    i32.const 0
    i32.store offset=32
    local.get $p0
    local.get $p2
    local.get $l10
    i32.const 3112
    i32.add
    local.get $l10
    i32.const 6192
    i32.add
    local.get $l10
    i32.const 6272
    i32.add
    call $f70075
    local.get $p1
    local.get $p3
    local.get $l10
    i32.const 32
    i32.add
    local.get $l10
    i32.const 6208
    i32.add
    local.get $l10
    i32.const 6240
    i32.add
    call $f70075
    block $B0
      block $B1
        local.get $l10
        i32.load offset=3112
        local.tee $l13
        i32.eqz
        if $I2
          i32.const 0
          local.set $l11
          br $B1
        end
        local.get $l44
        f32.neg
        local.set $l53
        local.get $l43
        f32.neg
        local.set $l54
        local.get $l42
        f32.neg
        local.set $l55
        local.get $l41
        f32.neg
        local.set $l56
        local.get $l40
        f32.neg
        local.set $l57
        local.get $l39
        f32.neg
        local.set $l58
        i32.const 1
        local.set $l11
        local.get $l10
        i32.load offset=32
        local.set $l12
        loop $L3
          local.get $l12
          if $I4
            local.get $l10
            i32.const 3112
            i32.add
            local.get $l14
            i32.const 12
            i32.mul
            i32.add
            local.tee $p0
            f32.load offset=12
            local.set $l30
            local.get $p0
            f32.load offset=8
            local.set $l31
            local.get $p0
            f32.load offset=4
            local.set $l32
            i32.const 0
            local.set $p0
            loop $L5
              block $B6
                local.get $l32
                local.get $l10
                i32.const 32
                i32.add
                local.get $p0
                i32.const 12
                i32.mul
                i32.add
                local.tee $p1
                f32.load offset=4
                local.tee $l23
                local.get $p5
                f32.load offset=4
                f32.mul
                local.get $p1
                f32.load offset=8
                local.tee $l24
                local.get $p5
                f32.load offset=20
                f32.mul
                f32.add
                local.get $p1
                f32.load offset=12
                local.tee $l25
                local.get $p5
                f32.load offset=36
                f32.mul
                f32.add
                local.tee $l27
                f32.mul
                local.get $l31
                local.get $l23
                local.get $p5
                f32.load
                f32.mul
                local.get $l24
                local.get $p5
                f32.load offset=16
                f32.mul
                f32.add
                local.get $l25
                local.get $p5
                f32.load offset=32
                f32.mul
                f32.add
                local.tee $l28
                f32.mul
                f32.sub
                local.tee $l26
                local.get $l26
                f32.mul
                local.get $l31
                local.get $l23
                local.get $p5
                f32.load offset=8
                f32.mul
                local.get $l24
                local.get $p5
                f32.load offset=24
                f32.mul
                f32.add
                local.get $l25
                local.get $p5
                f32.load offset=40
                f32.mul
                f32.add
                local.tee $l23
                f32.mul
                local.get $l30
                local.get $l27
                f32.mul
                f32.sub
                local.tee $l24
                local.get $l24
                f32.mul
                local.get $l30
                local.get $l28
                f32.mul
                local.get $l32
                local.get $l23
                f32.mul
                f32.sub
                local.tee $l25
                local.get $l25
                f32.mul
                f32.add
                f32.add
                local.tee $l23
                f32.const 0x1p-23 (;=1.19209e-07;)
                f32.lt
                br_if $B6
                local.get $l10
                i32.const 0
                i32.store offset=28
                local.get $l10
                local.get $l26
                f32.const 0x1p+0 (;=1;)
                local.get $l23
                f32.sqrt
                f32.div
                local.tee $l27
                f32.mul
                local.tee $l23
                f32.store offset=24
                local.get $l10
                local.get $l24
                local.get $l27
                f32.mul
                local.tee $l24
                f32.store offset=16
                local.get $l10
                local.get $l25
                local.get $l27
                f32.mul
                local.tee $l25
                f32.store offset=20
                local.get $p4
                f32.load offset=40
                local.set $l28
                local.get $p4
                f32.load offset=8
                local.set $l29
                local.get $p4
                f32.load offset=24
                local.set $l33
                local.get $p4
                f32.load offset=32
                local.set $l27
                local.get $p4
                f32.load
                local.set $l34
                local.get $p4
                f32.load offset=16
                local.set $l35
                local.get $p4
                f32.load offset=36
                local.set $l26
                local.get $p4
                f32.load offset=4
                local.set $l37
                local.get $p4
                f32.load offset=20
                local.set $l38
                local.get $l10
                i32.const 0
                i32.store offset=12
                local.get $l10
                local.get $l24
                local.get $l37
                f32.mul
                local.get $l25
                local.get $l38
                f32.mul
                f32.add
                local.get $l23
                local.get $l26
                f32.mul
                f32.add
                local.tee $l26
                f32.store offset=4
                local.get $l10
                local.get $l24
                local.get $l34
                f32.mul
                local.get $l25
                local.get $l35
                f32.mul
                f32.add
                local.get $l23
                local.get $l27
                f32.mul
                f32.add
                local.tee $l27
                f32.store
                local.get $l10
                local.get $l24
                local.get $l29
                f32.mul
                local.get $l25
                local.get $l33
                f32.mul
                f32.add
                local.get $l23
                local.get $l28
                f32.mul
                f32.add
                local.tee $l28
                f32.store offset=8
                local.get $l50
                local.get $l23
                f32.mul
                local.get $l52
                local.get $l24
                f32.mul
                local.get $l51
                local.get $l25
                f32.mul
                f32.add
                f32.add
                local.tee $l29
                local.get $l27
                local.get $l39
                local.get $l58
                local.get $l27
                f32.const 0x0p+0 (;=0;)
                f32.gt
                select
                f32.mul
                local.get $l26
                local.get $l40
                local.get $l57
                local.get $l26
                f32.const 0x0p+0 (;=0;)
                f32.gt
                select
                f32.mul
                f32.add
                local.get $l28
                local.get $l41
                local.get $l56
                local.get $l28
                f32.const 0x0p+0 (;=0;)
                f32.gt
                select
                f32.mul
                f32.add
                local.tee $l26
                local.get $l48
                local.get $l26
                local.get $l48
                f32.gt
                select
                local.tee $l26
                f32.add
                local.tee $l27
                local.get $l23
                local.get $l44
                local.get $l53
                local.get $l23
                f32.const 0x0p+0 (;=0;)
                f32.gt
                select
                f32.mul
                local.get $l24
                local.get $l42
                local.get $l55
                local.get $l24
                f32.const 0x0p+0 (;=0;)
                f32.gt
                select
                f32.mul
                local.get $l25
                local.get $l43
                local.get $l54
                local.get $l25
                f32.const 0x0p+0 (;=0;)
                f32.gt
                select
                f32.mul
                f32.add
                f32.add
                local.tee $l23
                local.get $l47
                local.get $l23
                local.get $l47
                f32.gt
                select
                local.tee $l23
                local.get $l23
                local.get $l27
                f32.gt
                select
                local.get $l23
                f32.neg
                local.tee $l23
                local.get $l29
                local.get $l26
                f32.sub
                local.tee $l24
                local.get $l23
                local.get $l24
                f32.gt
                select
                f32.sub
                local.get $l36
                f32.gt
                br_if $B6
                local.get $p2
                local.get $l10
                i32.const 16
                i32.add
                local.get $l10
                i32.const 6336
                i32.add
                local.get $l10
                i32.const 6320
                i32.add
                local.get $p2
                i32.load
                i32.load offset=12
                call_indirect $__indirect_function_table (type $t4)
                local.get $l10
                f32.load offset=24
                local.set $l23
                local.get $l10
                f32.load offset=16
                local.set $l24
                local.get $l10
                f32.load offset=20
                local.set $l25
                local.get $p3
                local.get $l10
                local.get $l10
                i32.const 6304
                i32.add
                local.get $l10
                i32.const 6288
                i32.add
                local.get $p3
                i32.load
                i32.load offset=12
                call_indirect $__indirect_function_table (type $t4)
                local.get $l10
                local.get $l49
                local.get $l24
                f32.mul
                local.get $l45
                local.get $l25
                f32.mul
                f32.add
                local.get $l46
                local.get $l23
                f32.mul
                f32.add
                local.tee $l24
                local.get $l10
                f32.load offset=6304
                f32.add
                local.tee $l23
                f32.store offset=6304
                local.get $l10
                local.get $l24
                local.get $l10
                f32.load offset=6288
                f32.add
                local.tee $l24
                f32.store offset=6288
                local.get $l23
                local.get $l10
                f32.load offset=6320
                local.tee $l26
                local.get $p6
                f32.load
                local.tee $l25
                f32.add
                f32.gt
                br_if $B0
                local.get $l10
                f32.load offset=6336
                local.get $l24
                local.get $l25
                f32.add
                f32.gt
                br_if $B0
                local.get $l36
                local.get $l26
                local.get $l23
                f32.sub
                local.tee $l23
                f32.gt
                i32.eqz
                br_if $B6
                local.get $p8
                local.get $l10
                i64.load offset=16
                i64.store
                local.get $p8
                local.get $l10
                i64.load offset=24
                i64.store offset=8
                local.get $p9
                i32.const 2
                i32.store
                local.get $l23
                local.set $l36
              end
              local.get $p0
              i32.const 1
              i32.add
              local.tee $p0
              local.get $l12
              i32.ne
              br_if $L5
            end
          end
          local.get $l14
          i32.const 1
          i32.add
          local.tee $l14
          local.get $l13
          i32.lt_u
          local.set $l11
          local.get $l13
          local.get $l14
          i32.ne
          br_if $L3
        end
      end
      local.get $p7
      local.get $l36
      f32.store
      local.get $p7
      i32.const 4
      i32.add
      local.tee $p5
      local.get $l15
      i32.load
      i32.store offset=8
      local.get $p5
      local.get $l10
      i64.load offset=6352
      i64.store align=4
    end
    local.get $l10
    i32.const 6368
    i32.add
    global.set $g0
    local.get $l11
    i32.const -1
    i32.xor
    i32.const 1
    i32.and)