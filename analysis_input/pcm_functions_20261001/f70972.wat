  (func $f70972 (type $t518) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 f32) (param $p6 f32) (param $p7 f32) (param $p8 f32) (param $p9 i32)
    (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32) (local $l64 f32) (local $l65 f32) (local $l66 f32) (local $l67 f32) (local $l68 f32) (local $l69 f32) (local $l70 f32) (local $l71 f32) (local $l72 f32) (local $l73 f32) (local $l74 f32) (local $l75 f32) (local $l76 f32) (local $l77 f32) (local $l78 f32) (local $l79 f32) (local $l80 f32) (local $l81 f32) (local $l82 f32) (local $l83 f32) (local $l84 f32) (local $l85 f32) (local $l86 f32) (local $l87 f32) (local $l88 f32) (local $l89 f32) (local $l90 f32) (local $l91 f32) (local $l92 f32) (local $l93 f32) (local $l94 i64) (local $l95 i64) (local $l96 i64) (local $l97 i64) (local $l98 i64) (local $l99 i64)
    global.get $g0
    i32.const 1072
    i32.sub
    local.tee $p1
    global.set $g0
    local.get $p3
    i32.const 0
    i32.store offset=180
    local.get $p3
    i32.load offset=356
    local.tee $p2
    local.get $p3
    i32.load offset=184
    i32.const 2147483647
    i32.and
    i32.gt_u
    if $I0
      local.get $p3
      i32.const 176
      i32.add
      local.set $l18
      block $B1
        local.get $p2
        i32.eqz
        br_if $B1
        local.get $p2
        i32.const 176
        i32.mul
        local.tee $l13
        i32.eqz
        br_if $B1
        call $f69753
        local.tee $l12
        local.get $l13
        i32.const 3147971
        i32.const 3147006
        i32.const 4700888
        i32.load
        local.tee $l22
        local.get $l22
        i32.load
        i32.load offset=20
        call_indirect $__indirect_function_table (type $t5)
        select
        i32.const 3146964
        i32.const 553
        local.get $l12
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.set $l20
      end
      local.get $l18
      i32.load offset=4
      local.tee $l13
      i32.const 0
      i32.gt_s
      if $I2
        local.get $l20
        local.get $l13
        i32.const 176
        i32.mul
        i32.add
        local.set $l22
        local.get $l18
        i32.load
        local.set $l13
        local.get $l20
        local.set $l12
        loop $L3
          local.get $l12
          local.get $l13
          f32.load
          f32.store
          local.get $l12
          local.get $l13
          f32.load offset=4
          f32.store offset=4
          local.get $l12
          local.get $l13
          f32.load offset=8
          f32.store offset=8
          local.get $l12
          local.get $l13
          f32.load offset=12
          f32.store offset=12
          local.get $l12
          local.get $l13
          f32.load offset=16
          f32.store offset=16
          local.get $l12
          local.get $l13
          f32.load offset=20
          f32.store offset=20
          local.get $l12
          local.get $l13
          f32.load offset=24
          f32.store offset=24
          local.get $l12
          local.get $l13
          f32.load offset=28
          f32.store offset=28
          local.get $l12
          local.get $l13
          f32.load offset=32
          f32.store offset=32
          local.get $l12
          local.get $l13
          f32.load offset=36
          f32.store offset=36
          local.get $l12
          local.get $l13
          f32.load offset=40
          f32.store offset=40
          local.get $l12
          local.get $l13
          f32.load offset=44
          f32.store offset=44
          local.get $l12
          local.get $l13
          f32.load offset=48
          f32.store offset=48
          local.get $l12
          local.get $l13
          f32.load offset=52
          f32.store offset=52
          local.get $l12
          local.get $l13
          f32.load offset=56
          f32.store offset=56
          local.get $l12
          local.get $l13
          f32.load offset=60
          f32.store offset=60
          local.get $l12
          i32.const -64
          i32.sub
          local.get $l13
          i32.const -64
          i32.sub
          f32.load
          f32.store
          local.get $l12
          local.get $l13
          f32.load offset=68
          f32.store offset=68
          local.get $l12
          local.get $l13
          f32.load offset=72
          f32.store offset=72
          local.get $l12
          local.get $l13
          f32.load offset=76
          f32.store offset=76
          local.get $l12
          local.get $l13
          f32.load offset=80
          f32.store offset=80
          local.get $l12
          local.get $l13
          f32.load offset=84
          f32.store offset=84
          local.get $l12
          local.get $l13
          f32.load offset=88
          f32.store offset=88
          local.get $l12
          local.get $l13
          f32.load offset=92
          f32.store offset=92
          local.get $l12
          i32.const 96
          i32.add
          local.get $l13
          i32.const 96
          i32.add
          i32.const 80
          call $f483
          drop
          local.get $l13
          i32.const 176
          i32.add
          local.set $l13
          local.get $l12
          i32.const 176
          i32.add
          local.tee $l12
          local.get $l22
          i32.lt_u
          br_if $L3
        end
      end
      block $B4
        local.get $l18
        i32.load offset=8
        i32.const 0
        i32.lt_s
        br_if $B4
        local.get $l18
        i32.load
        local.tee $l13
        i32.eqz
        br_if $B4
        call $f69753
        local.tee $l12
        local.get $l13
        local.get $l12
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $l18
      local.get $p2
      i32.store offset=8
      local.get $l18
      local.get $l20
      i32.store
    end
    local.get $p3
    i32.const 0
    i32.store offset=192
    local.get $p3
    i32.load offset=360
    local.tee $p2
    local.get $p3
    i32.load offset=196
    i32.const 2147483647
    i32.and
    i32.gt_u
    if $I5
      local.get $p3
      i32.const 188
      i32.add
      local.set $l18
      i32.const 0
      local.set $l20
      block $B6
        local.get $p2
        i32.eqz
        br_if $B6
        local.get $p2
        i32.const 80
        i32.mul
        local.tee $l13
        i32.eqz
        br_if $B6
        call $f69753
        local.tee $l12
        local.get $l13
        i32.const 3148127
        i32.const 3147006
        i32.const 4700888
        i32.load
        local.tee $l22
        local.get $l22
        i32.load
        i32.load offset=20
        call_indirect $__indirect_function_table (type $t5)
        select
        i32.const 3146964
        i32.const 553
        local.get $l12
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.set $l20
      end
      local.get $l18
      i32.load offset=4
      local.tee $l13
      i32.const 0
      i32.gt_s
      if $I7
        local.get $l20
        local.get $l13
        i32.const 80
        i32.mul
        i32.add
        local.set $l22
        local.get $l18
        i32.load
        local.set $l13
        local.get $l20
        local.set $l12
        loop $L8
          local.get $l12
          local.get $l13
          f32.load
          f32.store
          local.get $l12
          local.get $l13
          f32.load offset=4
          f32.store offset=4
          local.get $l12
          local.get $l13
          f32.load offset=8
          f32.store offset=8
          local.get $l12
          local.get $l13
          f32.load offset=12
          f32.store offset=12
          local.get $l12
          local.get $l13
          f32.load offset=16
          f32.store offset=16
          local.get $l12
          local.get $l13
          f32.load offset=20
          f32.store offset=20
          local.get $l12
          local.get $l13
          f32.load offset=24
          f32.store offset=24
          local.get $l12
          local.get $l13
          f32.load offset=28
          f32.store offset=28
          local.get $l12
          local.get $l13
          f32.load offset=32
          f32.store offset=32
          local.get $l12
          local.get $l13
          f32.load offset=36
          f32.store offset=36
          local.get $l12
          local.get $l13
          f32.load offset=40
          f32.store offset=40
          local.get $l12
          local.get $l13
          f32.load offset=44
          f32.store offset=44
          local.get $l12
          local.get $l13
          f32.load offset=48
          f32.store offset=48
          local.get $l12
          local.get $l13
          f32.load offset=52
          f32.store offset=52
          local.get $l12
          local.get $l13
          f32.load offset=56
          f32.store offset=56
          local.get $l12
          local.get $l13
          i64.load offset=60 align=4
          i64.store offset=60 align=4
          local.get $l12
          local.get $l13
          i64.load offset=68 align=4
          i64.store offset=68 align=4
          local.get $l12
          local.get $l13
          i32.load offset=76
          i32.store offset=76
          local.get $l13
          i32.const 80
          i32.add
          local.set $l13
          local.get $l12
          i32.const 80
          i32.add
          local.tee $l12
          local.get $l22
          i32.lt_u
          br_if $L8
        end
      end
      block $B9
        local.get $l18
        i32.load offset=8
        i32.const 0
        i32.lt_s
        br_if $B9
        local.get $l18
        i32.load
        local.tee $l13
        i32.eqz
        br_if $B9
        call $f69753
        local.tee $l12
        local.get $l13
        local.get $l12
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $l18
      local.get $p2
      i32.store offset=8
      local.get $l18
      local.get $l20
      i32.store
    end
    local.get $p3
    i32.load offset=364
    i32.load8_u
    local.set $p2
    local.get $p1
    i32.const 40
    i32.add
    i32.const 0
    i32.const 1028
    call $f484
    drop
    local.get $p2
    i32.const 2
    i32.and
    local.set $l20
    local.get $p0
    i64.load offset=24
    local.set $l94
    local.get $p0
    i64.load offset=16
    local.set $l96
    local.get $p0
    i64.load offset=8
    local.set $l95
    local.get $p0
    i64.load
    local.set $l98
    local.get $p1
    i32.const 32
    i32.add
    local.set $l24
    local.get $p1
    i32.const 24
    i32.add
    local.set $l25
    local.get $p1
    i32.const 16
    i32.add
    local.set $l26
    loop $L10
      block $B11 (result i32)
        block $B12
          block $B13
            block $B14
              local.get $l95
              local.get $l98
              i64.or
              local.tee $l99
              local.get $l96
              i64.or
              i64.eqz
              if $I15
                i32.const 192
                local.set $p2
                local.get $l94
                local.set $l97
                local.get $l94
                i64.const 0
                i64.ne
                br_if $B12
                local.get $p1
                i32.load offset=1064
                local.tee $p2
                i32.eqz
                br_if $B13
                local.get $p6
                f32.const 0x1p+0 (;=1;)
                local.get $l20
                select
                local.set $p6
                local.get $p1
                i32.const 32
                i32.add
                local.set $l24
                local.get $p1
                i32.const 24
                i32.add
                local.set $l25
                local.get $p1
                i32.const 16
                i32.add
                local.set $l26
                br $B14
              end
              i32.const 192
              local.set $p2
              local.get $l94
              local.set $l97
              local.get $l94
              i64.eqz
              i32.eqz
              br_if $B12
              i32.const 128
              local.set $p2
              local.get $l96
              local.set $l97
              local.get $l96
              i64.const 0
              i64.ne
              br_if $B12
              local.get $l99
              i64.eqz
              i32.eqz
              if $I16
                local.get $l98
                local.get $l95
                local.get $l95
                i64.eqz
                select
                local.set $l97
                local.get $l95
                i64.const 0
                i64.ne
                i32.const 6
                i32.shl
                local.set $p2
                br $B12
              end
              i32.const -1
              br $B11
            end
            loop $L17
              local.get $p1
              local.get $p2
              i32.const 1
              i32.sub
              local.tee $p2
              i32.store offset=1064
              local.get $p5
              local.set $l42
              local.get $p8
              local.set $l55
              local.get $p1
              i32.const 40
              i32.add
              local.get $p2
              i32.const 2
              i32.shl
              i32.add
              i32.load
              local.set $p2
              i32.const 0
              local.set $l10
              i32.const 0
              local.set $l27
              global.get $g0
              i32.const 192
              i32.sub
              local.tee $l11
              global.set $g0
              block $B18
                local.get $p0
                local.get $p2
                i32.const 80
                i32.mul
                local.tee $l15
                i32.add
                local.tee $l16
                i32.load offset=68
                local.tee $l14
                f32.load offset=112
                f32.const 0x0p+0 (;=0;)
                f32.gt
                i32.eqz
                br_if $B18
                local.get $l14
                f32.load offset=104
                f32.const 0x0p+0 (;=0;)
                f32.gt
                i32.eqz
                if $I19
                  local.get $l14
                  f32.load offset=108
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  i32.eqz
                  br_if $B18
                end
                i32.const 1
                local.set $l10
              end
              block $B20
                local.get $l14
                f32.load offset=128
                f32.const 0x0p+0 (;=0;)
                f32.gt
                i32.eqz
                br_if $B20
                local.get $l14
                f32.load offset=120
                f32.const 0x0p+0 (;=0;)
                f32.gt
                i32.eqz
                if $I21
                  local.get $l14
                  f32.load offset=124
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  i32.eqz
                  br_if $B20
                end
                local.get $l10
                i32.const 1
                i32.add
                local.set $l10
              end
              block $B22
                local.get $l14
                f32.load offset=144
                f32.const 0x0p+0 (;=0;)
                f32.gt
                i32.eqz
                br_if $B22
                local.get $l14
                f32.load offset=136
                f32.const 0x0p+0 (;=0;)
                f32.gt
                i32.eqz
                if $I23
                  local.get $l14
                  f32.load offset=140
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  i32.eqz
                  br_if $B22
                end
                local.get $l10
                i32.const 1
                i32.add
                local.set $l10
              end
              local.get $p3
              i32.load offset=344
              local.set $l17
              block $B24
                local.get $l14
                f32.load offset=160
                f32.const 0x0p+0 (;=0;)
                f32.gt
                i32.eqz
                br_if $B24
                local.get $l14
                f32.load offset=152
                f32.const 0x0p+0 (;=0;)
                f32.gt
                i32.eqz
                if $I25
                  local.get $l14
                  f32.load offset=156
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  i32.eqz
                  br_if $B24
                end
                local.get $l10
                i32.const 1
                i32.add
                local.set $l10
              end
              local.get $l15
              local.get $l17
              i32.add
              local.set $l15
              block $B26
                local.get $l14
                f32.load offset=176
                f32.const 0x0p+0 (;=0;)
                f32.gt
                i32.eqz
                br_if $B26
                local.get $l14
                f32.load offset=168
                f32.const 0x0p+0 (;=0;)
                f32.gt
                i32.eqz
                if $I27
                  local.get $l14
                  f32.load offset=172
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  i32.eqz
                  br_if $B26
                end
                local.get $l10
                i32.const 1
                i32.add
                local.set $l10
              end
              local.get $l15
              i32.load8_u offset=79
              local.set $l21
              local.get $l15
              i32.load8_u offset=77
              local.set $l19
              local.get $l14
              f32.load offset=248
              local.set $l39
              block $B28
                local.get $l14
                f32.load offset=192
                f32.const 0x0p+0 (;=0;)
                f32.gt
                i32.eqz
                br_if $B28
                local.get $l14
                f32.load offset=184
                f32.const 0x0p+0 (;=0;)
                f32.gt
                i32.eqz
                if $I29
                  local.get $l14
                  f32.load offset=188
                  f32.const 0x0p+0 (;=0;)
                  f32.gt
                  i32.eqz
                  br_if $B28
                end
                local.get $l10
                i32.const 1
                i32.add
                local.set $l10
              end
              block $B30
                local.get $l10
                local.get $l19
                i32.const 1
                i32.shl
                i32.add
                local.get $l17
                local.get $p2
                i32.const 80
                i32.mul
                local.tee $l10
                i32.add
                local.tee $l13
                i32.load8_u offset=76
                i32.const 0
                local.get $l39
                f32.const 0x0p+0 (;=0;)
                f32.gt
                local.tee $l19
                select
                local.tee $l33
                i32.add
                i32.const 255
                i32.and
                i32.const 0
                local.get $l21
                i32.sub
                i32.const 255
                i32.and
                i32.eq
                br_if $B30
                local.get $l15
                i32.const 79
                i32.add
                local.set $l18
                local.get $l16
                i32.const 72
                i32.add
                local.set $l29
                local.get $p0
                local.get $l10
                i32.add
                local.tee $l21
                i32.load offset=64
                local.tee $l10
                f32.load offset=4
                local.tee $l36
                local.get $l14
                f32.load offset=44
                local.tee $l34
                local.get $l34
                f32.add
                local.tee $l56
                local.get $l10
                f32.load
                local.tee $l40
                f32.mul
                local.get $l36
                local.get $l14
                f32.load offset=48
                local.tee $l34
                local.get $l34
                f32.add
                local.tee $l45
                f32.mul
                f32.add
                local.get $l14
                f32.load offset=52
                local.tee $l34
                local.get $l34
                f32.add
                local.tee $l57
                local.get $l10
                f32.load offset=8
                local.tee $l37
                f32.mul
                f32.add
                local.tee $l58
                f32.mul
                local.get $l45
                local.get $l10
                f32.load offset=12
                local.tee $l34
                local.get $l34
                f32.mul
                f32.const -0x1p-1 (;=-0.5;)
                f32.add
                local.tee $l61
                f32.mul
                local.get $l34
                local.get $l56
                local.get $l37
                f32.mul
                local.get $l57
                local.get $l40
                f32.mul
                f32.sub
                f32.mul
                f32.add
                f32.add
                local.set $l63
                local.get $p0
                local.get $l16
                i32.load offset=72
                i32.const 80
                i32.mul
                i32.add
                local.tee $l16
                i32.load offset=64
                local.tee $l15
                f32.load offset=4
                local.tee $l38
                local.get $l14
                f32.load offset=16
                local.tee $l35
                local.get $l35
                f32.add
                local.tee $l59
                local.get $l15
                f32.load
                local.tee $l41
                f32.mul
                local.get $l38
                local.get $l14
                f32.load offset=20
                local.tee $l35
                local.get $l35
                f32.add
                local.tee $l44
                f32.mul
                f32.add
                local.get $l14
                f32.load offset=24
                local.tee $l35
                local.get $l35
                f32.add
                local.tee $l60
                local.get $l15
                f32.load offset=8
                local.tee $l43
                f32.mul
                f32.add
                local.tee $l54
                f32.mul
                local.get $l44
                local.get $l15
                f32.load offset=12
                local.tee $l35
                local.get $l35
                f32.mul
                f32.const -0x1p-1 (;=-0.5;)
                f32.add
                local.tee $l62
                f32.mul
                local.get $l35
                local.get $l59
                local.get $l43
                f32.mul
                local.get $l60
                local.get $l41
                f32.mul
                f32.sub
                f32.mul
                f32.add
                f32.add
                local.set $l64
                local.get $l43
                local.get $l14
                f32.load
                local.tee $l46
                f32.mul
                local.get $l38
                local.get $l14
                f32.load offset=12
                local.tee $l47
                f32.mul
                local.get $l35
                local.get $l14
                f32.load offset=4
                local.tee $l48
                f32.mul
                f32.add
                f32.add
                local.get $l41
                local.get $l14
                f32.load offset=8
                local.tee $l49
                f32.mul
                f32.sub
                local.tee $l65
                local.get $l34
                local.get $l14
                f32.load offset=28
                local.tee $l50
                f32.mul
                local.get $l40
                local.get $l14
                f32.load offset=40
                local.tee $l51
                f32.mul
                f32.add
                local.get $l36
                local.get $l14
                f32.load offset=36
                local.tee $l52
                f32.mul
                f32.add
                local.get $l37
                local.get $l14
                f32.load offset=32
                local.tee $l53
                f32.mul
                f32.sub
                local.tee $l66
                f32.mul
                local.tee $l78
                local.get $l35
                local.get $l47
                f32.mul
                local.get $l41
                local.get $l46
                f32.mul
                f32.sub
                local.get $l38
                local.get $l48
                f32.mul
                f32.sub
                local.get $l43
                local.get $l49
                f32.mul
                f32.sub
                local.tee $l67
                local.get $l40
                local.get $l53
                f32.mul
                local.get $l37
                local.get $l51
                f32.mul
                local.get $l34
                local.get $l52
                f32.mul
                f32.add
                f32.add
                local.get $l36
                local.get $l50
                f32.mul
                f32.sub
                local.tee $l68
                f32.mul
                local.tee $l79
                local.get $l41
                local.get $l48
                f32.mul
                local.get $l43
                local.get $l47
                f32.mul
                local.get $l35
                local.get $l49
                f32.mul
                f32.add
                f32.add
                local.get $l38
                local.get $l46
                f32.mul
                f32.sub
                local.tee $l69
                local.get $l34
                local.get $l51
                f32.mul
                local.get $l40
                local.get $l50
                f32.mul
                f32.sub
                local.get $l36
                local.get $l53
                f32.mul
                f32.sub
                local.get $l37
                local.get $l52
                f32.mul
                f32.sub
                local.tee $l70
                f32.mul
                local.tee $l80
                f32.sub
                local.get $l35
                local.get $l46
                f32.mul
                local.get $l41
                local.get $l47
                f32.mul
                f32.add
                local.get $l38
                local.get $l49
                f32.mul
                f32.add
                local.get $l43
                local.get $l48
                f32.mul
                f32.sub
                local.tee $l71
                local.get $l37
                local.get $l50
                f32.mul
                local.get $l36
                local.get $l51
                f32.mul
                local.get $l34
                local.get $l53
                f32.mul
                f32.add
                f32.add
                local.get $l40
                local.get $l52
                f32.mul
                f32.sub
                local.tee $l72
                f32.mul
                local.tee $l81
                f32.sub
                f32.add
                local.set $l82
                local.get $l69
                local.get $l72
                f32.mul
                local.tee $l83
                local.get $l67
                local.get $l66
                f32.mul
                local.tee $l84
                local.get $l71
                local.get $l70
                f32.mul
                local.tee $l85
                f32.sub
                local.get $l65
                local.get $l68
                f32.mul
                local.tee $l86
                f32.sub
                f32.add
                local.set $l87
                local.get $l39
                local.get $l42
                f32.mul
                local.get $p3
                i32.load offset=164
                local.get $p2
                i32.const 5
                i32.shl
                i32.add
                local.tee $l17
                f32.load
                local.tee $l39
                local.get $l39
                f32.mul
                local.get $l17
                f32.load offset=4
                local.tee $l39
                local.get $l39
                f32.mul
                f32.add
                local.get $l17
                f32.load offset=8
                local.tee $l39
                local.get $l39
                f32.mul
                f32.add
                f32.sqrt
                local.get $l17
                f32.load offset=16
                local.tee $l39
                local.get $l39
                f32.mul
                local.get $l17
                f32.load offset=20
                local.tee $l39
                local.get $l39
                f32.mul
                f32.add
                local.get $l17
                f32.load offset=24
                local.tee $l39
                local.get $l39
                f32.mul
                f32.add
                f32.sqrt
                f32.add
                f32.mul
                f32.const 0x0p+0 (;=0;)
                local.get $l19
                select
                local.set $l74
                local.get $l34
                local.get $l45
                local.get $l40
                f32.mul
                local.get $l56
                local.get $l36
                f32.mul
                f32.sub
                f32.mul
                local.set $l88
                local.get $l34
                local.get $l57
                local.get $l36
                f32.mul
                local.get $l45
                local.get $l37
                f32.mul
                f32.sub
                f32.mul
                local.set $l53
                local.get $l35
                local.get $l60
                local.get $l38
                f32.mul
                local.get $l44
                local.get $l43
                f32.mul
                f32.sub
                f32.mul
                local.set $l46
                local.get $l37
                local.get $l58
                f32.mul
                local.set $l89
                local.get $l40
                local.get $l58
                f32.mul
                local.set $l73
                local.get $l43
                local.get $l54
                f32.mul
                local.set $l49
                local.get $l41
                local.get $l54
                f32.mul
                local.set $l47
                local.get $l71
                local.get $l68
                f32.mul
                local.set $l75
                local.get $l69
                local.get $l66
                f32.mul
                local.set $l76
                local.get $l65
                local.get $l70
                f32.mul
                local.set $l77
                f32.const 0x0p+0 (;=0;)
                f32.const 0x1p+0 (;=1;)
                local.get $p9
                select
                local.set $l58
                local.get $l35
                local.get $l44
                local.get $l41
                f32.mul
                local.get $l59
                local.get $l38
                f32.mul
                f32.sub
                f32.mul
                local.set $l48
                local.get $l21
                i32.const -64
                i32.sub
                local.set $l22
                local.get $l16
                i32.const -64
                i32.sub
                local.set $l12
                local.get $l10
                f32.load offset=16
                local.set $l90
                local.get $l15
                f32.load offset=16
                local.set $l50
                local.get $l10
                f32.load offset=24
                local.set $l91
                local.get $l10
                f32.load offset=20
                local.set $l54
                local.get $l15
                f32.load offset=24
                local.set $l52
                local.get $l15
                f32.load offset=20
                local.set $l51
                local.get $p2
                i32.const 76
                i32.mul
                local.set $l30
                local.get $p3
                i32.load offset=348
                local.tee $l20
                local.get $p2
                i32.const 96
                i32.mul
                i32.add
                local.set $l31
                local.get $l33
                i32.const 255
                i32.and
                local.set $l32
                i32.const 0
                local.set $l15
                i32.const 0
                local.set $l17
                loop $L31
                  local.get $l14
                  local.get $l17
                  i32.add
                  i32.const 258
                  i32.add
                  local.tee $l16
                  i32.load8_u
                  local.tee $l10
                  if $I32
                    local.get $l14
                    local.get $l17
                    i32.const 4
                    i32.shl
                    i32.add
                    local.tee $l19
                    i32.const 116
                    i32.add
                    local.tee $l23
                    i32.load
                    local.set $l21
                    block $B33
                      block $B34
                        local.get $l10
                        i32.const 1
                        i32.eq
                        br_if $B34
                        local.get $l32
                        br_if $B34
                        local.get $l21
                        i32.const 4
                        i32.eq
                        br_if $B33
                      end
                      local.get $p3
                      i32.load offset=272
                      local.get $l30
                      i32.add
                      local.get $l15
                      i32.const 24
                      i32.mul
                      i32.add
                      local.tee $l10
                      f32.load
                      local.set $l34
                      local.get $l10
                      f32.load offset=4
                      local.set $l35
                      local.get $l10
                      f32.load offset=8
                      local.set $l36
                      local.get $l29
                      i32.load
                      local.set $l10
                      local.get $l11
                      i64.const 0
                      i64.store offset=136
                      local.get $l11
                      i64.const 0
                      i64.store offset=128
                      local.get $l11
                      i32.const 0
                      i32.store offset=156
                      local.get $l11
                      local.get $l36
                      f32.store offset=152
                      local.get $l11
                      local.get $l35
                      f32.store offset=148
                      local.get $l11
                      local.get $l34
                      f32.store offset=144
                      local.get $l11
                      i64.const 0
                      i64.store offset=104
                      local.get $l11
                      i64.const 0
                      i64.store offset=96
                      local.get $l11
                      i32.const 0
                      i32.store offset=124
                      local.get $l11
                      local.get $l36
                      f32.neg
                      f32.store offset=120
                      local.get $l11
                      local.get $l35
                      f32.neg
                      f32.store offset=116
                      local.get $l11
                      local.get $l34
                      f32.neg
                      f32.store offset=112
                      local.get $p0
                      local.get $p4
                      local.get $p3
                      local.get $l10
                      local.get $l11
                      i32.const 128
                      i32.add
                      local.get $l11
                      i32.const 48
                      i32.add
                      local.get $p2
                      local.get $l11
                      i32.const 96
                      i32.add
                      local.get $l11
                      i32.const 160
                      i32.add
                      call $f71011
                      f32.const 0x0p+0 (;=0;)
                      local.set $l37
                      local.get $l34
                      local.get $l11
                      f32.load offset=64
                      local.tee $l38
                      f32.mul
                      local.get $l35
                      local.get $l11
                      f32.load offset=68
                      local.tee $l41
                      f32.mul
                      f32.add
                      local.get $l36
                      local.get $l11
                      f32.load offset=72
                      local.tee $l43
                      f32.mul
                      f32.add
                      local.get $l34
                      local.get $l11
                      f32.load offset=176
                      local.tee $l39
                      f32.mul
                      local.get $l35
                      local.get $l11
                      f32.load offset=180
                      local.tee $l45
                      f32.mul
                      f32.add
                      local.get $l36
                      local.get $l11
                      f32.load offset=184
                      local.tee $l44
                      f32.mul
                      f32.add
                      f32.sub
                      local.tee $l40
                      f32.const 0x1.4f8b58p-17 (;=1e-05;)
                      f32.gt
                      if $I35
                        f32.const 0x1p+0 (;=1;)
                        local.get $l40
                        f32.const 0x1.a36e2ep-14 (;=0.0001;)
                        f32.add
                        f32.div
                        local.set $l37
                      end
                      local.get $p3
                      local.get $p3
                      i32.load offset=180
                      local.tee $l10
                      i32.const 1
                      i32.add
                      i32.store offset=180
                      local.get $p3
                      i32.load offset=176
                      local.get $l10
                      i32.const 176
                      i32.mul
                      i32.add
                      local.tee $l10
                      local.get $l40
                      f32.store offset=100
                      local.get $l10
                      local.get $l37
                      f32.store offset=96
                      local.get $l10
                      local.get $l38
                      f32.store offset=48
                      local.get $l10
                      i64.const 0
                      i64.store offset=24 align=4
                      local.get $l10
                      local.get $l34
                      f32.store offset=12
                      local.get $l10
                      i32.const 0
                      i32.store offset=8
                      local.get $l10
                      i64.const 0
                      i64.store align=4
                      local.get $l10
                      local.get $l43
                      f32.store offset=56
                      local.get $l10
                      local.get $l41
                      f32.store offset=52
                      local.get $l10
                      local.get $l36
                      f32.store offset=44
                      local.get $l10
                      local.get $l35
                      f32.store offset=40
                      local.get $l10
                      local.get $l34
                      f32.store offset=36
                      local.get $l10
                      i32.const 0
                      i32.store offset=32
                      local.get $l10
                      local.get $l36
                      f32.store offset=20
                      local.get $l10
                      local.get $l35
                      f32.store offset=16
                      local.get $l10
                      local.get $l11
                      f32.load offset=48
                      f32.store offset=60
                      local.get $l10
                      i32.const -64
                      i32.sub
                      local.get $l11
                      f32.load offset=52
                      f32.store
                      local.get $l11
                      f32.load offset=56
                      local.set $l34
                      local.get $l10
                      local.get $l44
                      f32.store offset=80
                      local.get $l10
                      local.get $l45
                      f32.store offset=76
                      local.get $l10
                      local.get $l39
                      f32.store offset=72
                      local.get $l10
                      local.get $l34
                      f32.store offset=68
                      local.get $l10
                      local.get $l11
                      f32.load offset=160
                      f32.store offset=84
                      local.get $l10
                      local.get $l11
                      f32.load offset=164
                      f32.store offset=88
                      local.get $l11
                      f32.load offset=168
                      local.set $l34
                      local.get $l10
                      local.get $p2
                      i32.store8 offset=169
                      local.get $l10
                      i32.const 0
                      i32.store8 offset=168
                      local.get $l10
                      local.get $l55
                      f32.store offset=120
                      local.get $l10
                      local.get $l34
                      f32.store offset=92
                      block $B36 (result f32)
                        local.get $l16
                        i32.load8_u
                        i32.const 1
                        i32.eq
                        if $I37
                          local.get $l10
                          local.get $l14
                          local.get $l17
                          i32.const 3
                          i32.shl
                          i32.add
                          local.tee $l28
                          f32.load offset=56
                          f32.store offset=104
                          local.get $l28
                          f32.load offset=60
                          br $B36
                        end
                        local.get $l10
                        i32.const -8388609
                        i32.store offset=104
                        f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                      end
                      local.set $l34
                      i32.const 1
                      local.get $l15
                      i32.shl
                      local.set $l28
                      local.get $l10
                      i32.const 0
                      i32.store offset=160
                      local.get $l10
                      i64.const 0
                      i64.store offset=112 align=4
                      local.get $l10
                      local.get $l34
                      f32.store offset=108
                      local.get $l10
                      local.get $l58
                      f32.store offset=164
                      local.get $l10
                      local.get $l74
                      f32.store offset=156
                      block $B38
                        block $B39
                          local.get $l10
                          block $B40 (result f32)
                            block $B41
                              block $B42
                                block $B43
                                  local.get $l21
                                  i32.const 4
                                  i32.ne
                                  if $I44
                                    local.get $l31
                                    local.get $l15
                                    i32.const 2
                                    i32.shl
                                    i32.add
                                    local.tee $l21
                                    f32.load offset=12
                                    local.set $l35
                                    local.get $l16
                                    i32.load8_u
                                    i32.const 1
                                    i32.eq
                                    if $I45
                                      local.get $l14
                                      local.get $l17
                                      i32.const 3
                                      i32.shl
                                      i32.add
                                      local.tee $l16
                                      f32.load offset=60
                                      local.tee $l34
                                      local.get $l16
                                      f32.load offset=56
                                      local.tee $l36
                                      local.get $l35
                                      local.get $l35
                                      local.get $l36
                                      f32.lt
                                      select
                                      local.tee $l35
                                      local.get $l34
                                      local.get $l35
                                      f32.lt
                                      select
                                      local.set $l35
                                    end
                                    local.get $l21
                                    f32.load
                                    local.tee $l38
                                    block $B46 (result f32)
                                      local.get $l23
                                      i32.load
                                      local.tee $l16
                                      i32.const 2
                                      i32.eq
                                      if $I47
                                        f32.const 0x1.08b2a2p+83 (;=1e+25;)
                                        local.set $l36
                                        f32.const 0x0p+0 (;=0;)
                                        br $B46
                                      end
                                      local.get $l16
                                      i32.const 3
                                      i32.ne
                                      br_if $B43
                                      f32.const 0x0p+0 (;=0;)
                                      local.set $l36
                                      f32.const 0x1.08b2a2p+83 (;=1e+25;)
                                    end
                                    local.tee $l34
                                    f32.mul
                                    local.get $l42
                                    f32.mul
                                    local.set $l41
                                    local.get $l34
                                    local.get $l36
                                    local.get $l42
                                    f32.mul
                                    f32.add
                                    local.get $l42
                                    f32.mul
                                    local.set $l38
                                    br $B42
                                  end
                                  local.get $l10
                                  i64.const 0
                                  i64.store offset=124 align=4
                                  local.get $l10
                                  i64.const 0
                                  i64.store offset=148 align=4
                                  local.get $l10
                                  i64.const 0
                                  i64.store offset=140 align=4
                                  local.get $l10
                                  i64.const 0
                                  i64.store offset=132 align=4
                                  br $B38
                                end
                                local.get $l38
                                local.get $l19
                                f32.load offset=108
                                local.tee $l34
                                f32.mul
                                local.get $l42
                                f32.mul
                                local.set $l41
                                local.get $l34
                                local.get $l19
                                f32.load offset=104
                                local.tee $l36
                                local.get $l42
                                f32.mul
                                f32.add
                                local.get $l42
                                f32.mul
                                local.set $l38
                                f32.const 0x0p+0 (;=0;)
                                local.set $l34
                                local.get $l16
                                br_table $B42 $B41 $B39
                              end
                              local.get $l10
                              local.get $l38
                              f32.const 0x1p+0 (;=1;)
                              local.get $l40
                              local.get $l38
                              f32.mul
                              f32.const 0x1p+0 (;=1;)
                              f32.add
                              f32.div
                              f32.const 0x0p+0 (;=0;)
                              local.get $l40
                              f32.const 0x0p+0 (;=0;)
                              f32.gt
                              select
                              local.tee $l34
                              f32.neg
                              f32.mul
                              f32.store offset=136
                              local.get $l10
                              local.get $l41
                              local.get $l34
                              f32.mul
                              f32.store offset=124
                              local.get $l36
                              local.get $l34
                              f32.mul
                              br $B40
                            end
                            local.get $l10
                            local.get $l37
                            local.get $l41
                            f32.const 0x1p+0 (;=1;)
                            local.get $l38
                            f32.const 0x1p+0 (;=1;)
                            f32.add
                            f32.div
                            local.tee $l34
                            f32.mul
                            f32.mul
                            f32.store offset=124
                            local.get $l10
                            local.get $l37
                            local.get $l38
                            local.get $l34
                            f32.neg
                            f32.mul
                            f32.mul
                            f32.store offset=136
                            local.get $l37
                            local.get $l36
                            local.get $l34
                            f32.mul
                            f32.mul
                          end
                          local.get $l42
                          f32.mul
                          f32.store offset=128
                        end
                        local.get $l10
                        f32.const 0x1p+0 (;=1;)
                        f32.const 0x1p+0 (;=1;)
                        local.get $l34
                        f32.sub
                        local.get $p9
                        select
                        f32.store offset=144
                        local.get $l10
                        local.get $l35
                        f32.store offset=132
                        local.get $l19
                        f32.load offset=112
                        local.set $l34
                        local.get $l10
                        i32.const 0
                        i32.store offset=152
                        local.get $l10
                        i32.const 0
                        i32.store offset=140
                        local.get $l10
                        local.get $l34
                        local.get $p6
                        f32.mul
                        f32.store offset=148
                      end
                      local.get $l27
                      local.get $l28
                      i32.or
                      local.set $l27
                    end
                    local.get $l15
                    i32.const 1
                    i32.add
                    local.set $l15
                  end
                  local.get $l17
                  i32.const 1
                  i32.add
                  local.tee $l17
                  i32.const 3
                  i32.ne
                  br_if $L31
                end
                local.get $l54
                local.get $l63
                f32.add
                local.set $l54
                local.get $l51
                local.get $l64
                f32.add
                local.set $l64
                local.get $l75
                local.get $l67
                local.get $l72
                f32.mul
                local.tee $l92
                local.get $l77
                f32.sub
                local.get $l76
                f32.sub
                f32.add
                local.set $l93
                local.get $l91
                local.get $l57
                local.get $l61
                f32.mul
                local.get $l88
                f32.add
                local.get $l89
                f32.add
                f32.add
                local.set $l63
                local.get $l90
                local.get $l73
                local.get $l56
                local.get $l61
                f32.mul
                local.get $l53
                f32.add
                f32.add
                f32.add
                local.set $l61
                local.get $l52
                local.get $l60
                local.get $l62
                f32.mul
                local.get $l48
                f32.add
                local.get $l49
                f32.add
                f32.add
                local.set $l73
                local.get $l50
                local.get $l47
                local.get $l59
                local.get $l62
                f32.mul
                local.get $l46
                f32.add
                f32.add
                f32.add
                local.set $l62
                local.get $p2
                i32.const 76
                i32.mul
                local.set $l32
                local.get $l20
                local.get $p2
                i32.const 96
                i32.mul
                i32.add
                local.set $l31
                local.get $l33
                i32.const 255
                i32.and
                local.set $l30
                i32.const 3
                local.set $l17
                loop $L48
                  local.get $l14
                  local.get $l17
                  i32.add
                  i32.const 258
                  i32.add
                  local.tee $l21
                  i32.load8_u
                  local.tee $l10
                  if $I49
                    i32.const 0
                    local.set $l16
                    block $B50
                      block $B51
                        local.get $l14
                        local.get $l17
                        i32.const 4
                        i32.shl
                        i32.add
                        local.tee $l19
                        i32.const 112
                        i32.add
                        local.tee $l28
                        f32.load
                        f32.const 0x0p+0 (;=0;)
                        f32.gt
                        if $I52
                          i32.const 1
                          local.set $l16
                          local.get $l19
                          f32.load offset=104
                          f32.const 0x0p+0 (;=0;)
                          f32.gt
                          br_if $B51
                          local.get $l19
                          f32.load offset=108
                          f32.const 0x0p+0 (;=0;)
                          f32.gt
                          local.set $l16
                        end
                        local.get $l10
                        i32.const 1
                        i32.eq
                        br_if $B51
                        local.get $l30
                        br_if $B51
                        local.get $l16
                        i32.eqz
                        br_if $B50
                      end
                      local.get $p3
                      i32.load offset=272
                      local.get $l32
                      i32.add
                      local.get $l15
                      i32.const 24
                      i32.mul
                      i32.add
                      local.tee $l10
                      f32.load offset=20
                      local.set $l34
                      local.get $l10
                      f32.load offset=16
                      local.set $l35
                      local.get $l10
                      f32.load offset=12
                      local.set $l36
                      local.get $l22
                      i32.load
                      local.tee $l10
                      f32.load offset=24
                      local.set $l40
                      local.get $l10
                      f32.load offset=20
                      local.set $l43
                      local.get $l12
                      i32.load
                      local.tee $l23
                      f32.load offset=24
                      local.set $l38
                      local.get $l23
                      f32.load offset=20
                      local.set $l37
                      local.get $l10
                      f32.load offset=16
                      local.set $l39
                      local.get $l23
                      f32.load offset=16
                      local.set $l41
                      local.get $l29
                      i32.load
                      local.set $l10
                      local.get $l11
                      i32.const 0
                      i32.store offset=156
                      local.get $l11
                      local.get $l35
                      local.get $l62
                      local.get $l41
                      f32.sub
                      local.tee $l41
                      f32.mul
                      local.get $l36
                      local.get $l64
                      local.get $l37
                      f32.sub
                      local.tee $l45
                      f32.mul
                      f32.sub
                      local.tee $l37
                      f32.store offset=152
                      local.get $l11
                      local.get $l36
                      local.get $l73
                      local.get $l38
                      f32.sub
                      local.tee $l44
                      f32.mul
                      local.get $l34
                      local.get $l41
                      f32.mul
                      f32.sub
                      local.tee $l38
                      f32.store offset=148
                      local.get $l11
                      local.get $l34
                      local.get $l45
                      f32.mul
                      local.get $l35
                      local.get $l44
                      f32.mul
                      f32.sub
                      local.tee $l41
                      f32.store offset=144
                      local.get $l11
                      i32.const 0
                      i32.store offset=140
                      local.get $l11
                      local.get $l34
                      f32.store offset=136
                      local.get $l11
                      local.get $l35
                      f32.store offset=132
                      local.get $l11
                      local.get $l36
                      f32.store offset=128
                      local.get $l11
                      i32.const 0
                      i32.store offset=124
                      local.get $l11
                      local.get $l35
                      local.get $l61
                      local.get $l39
                      f32.sub
                      local.tee $l39
                      f32.mul
                      local.get $l36
                      local.get $l54
                      local.get $l43
                      f32.sub
                      local.tee $l45
                      f32.mul
                      f32.sub
                      local.tee $l43
                      f32.neg
                      f32.store offset=120
                      local.get $l11
                      local.get $l36
                      local.get $l63
                      local.get $l40
                      f32.sub
                      local.tee $l40
                      f32.mul
                      local.get $l34
                      local.get $l39
                      f32.mul
                      f32.sub
                      local.tee $l39
                      f32.neg
                      f32.store offset=116
                      local.get $l11
                      local.get $l34
                      local.get $l45
                      f32.mul
                      local.get $l35
                      local.get $l40
                      f32.mul
                      f32.sub
                      local.tee $l45
                      f32.neg
                      f32.store offset=112
                      local.get $l11
                      i32.const 0
                      i32.store offset=108
                      local.get $l11
                      local.get $l34
                      f32.neg
                      f32.store offset=104
                      local.get $l11
                      local.get $l35
                      f32.neg
                      f32.store offset=100
                      local.get $l11
                      local.get $l36
                      f32.neg
                      f32.store offset=96
                      local.get $p0
                      local.get $p4
                      local.get $p3
                      local.get $l10
                      local.get $l11
                      i32.const 128
                      i32.add
                      local.get $l11
                      i32.const 48
                      i32.add
                      local.get $p2
                      local.get $l11
                      i32.const 96
                      i32.add
                      local.get $l11
                      i32.const 160
                      i32.add
                      call $f71011
                      f32.const 0x0p+0 (;=0;)
                      local.set $l44
                      local.get $l36
                      local.get $l11
                      f32.load offset=48
                      local.tee $l59
                      f32.mul
                      local.get $l35
                      local.get $l11
                      f32.load offset=52
                      local.tee $l60
                      f32.mul
                      f32.add
                      local.get $l34
                      local.get $l11
                      f32.load offset=56
                      local.tee $l56
                      f32.mul
                      f32.add
                      local.get $l41
                      local.get $l11
                      f32.load offset=64
                      local.tee $l57
                      f32.mul
                      local.get $l38
                      local.get $l11
                      f32.load offset=68
                      local.tee $l46
                      f32.mul
                      f32.add
                      local.get $l37
                      local.get $l11
                      f32.load offset=72
                      local.tee $l47
                      f32.mul
                      f32.add
                      f32.add
                      local.get $l36
                      local.get $l11
                      f32.load offset=160
                      local.tee $l48
                      f32.mul
                      local.get $l35
                      local.get $l11
                      f32.load offset=164
                      local.tee $l49
                      f32.mul
                      f32.add
                      local.get $l34
                      local.get $l11
                      f32.load offset=168
                      local.tee $l50
                      f32.mul
                      f32.add
                      local.get $l45
                      local.get $l11
                      f32.load offset=176
                      local.tee $l51
                      f32.mul
                      local.get $l39
                      local.get $l11
                      f32.load offset=180
                      local.tee $l52
                      f32.mul
                      f32.add
                      local.get $l43
                      local.get $l11
                      f32.load offset=184
                      local.tee $l53
                      f32.mul
                      f32.add
                      f32.add
                      f32.sub
                      local.tee $l40
                      f32.const 0x1.4f8b58p-17 (;=1e-05;)
                      f32.gt
                      if $I53
                        f32.const 0x1p+0 (;=1;)
                        local.get $l40
                        f32.const 0x1.a36e2ep-14 (;=0.0001;)
                        f32.add
                        f32.div
                        local.set $l44
                      end
                      local.get $p3
                      local.get $p3
                      i32.load offset=180
                      local.tee $l10
                      i32.const 1
                      i32.add
                      i32.store offset=180
                      local.get $p3
                      i32.load offset=176
                      local.get $l10
                      i32.const 176
                      i32.mul
                      i32.add
                      local.tee $l10
                      local.get $l44
                      f32.store offset=96
                      local.get $l10
                      local.get $l40
                      f32.store offset=100
                      local.get $l10
                      local.get $p2
                      i32.store8 offset=169
                      local.get $l10
                      i32.const 1
                      i32.store8 offset=168
                      local.get $l10
                      local.get $l55
                      f32.store offset=120
                      local.get $l10
                      local.get $l51
                      f32.store offset=72
                      local.get $l10
                      local.get $l57
                      f32.store offset=48
                      local.get $l10
                      local.get $l36
                      f32.store offset=24
                      local.get $l10
                      local.get $l41
                      f32.store offset=12
                      local.get $l10
                      local.get $l34
                      f32.store offset=8
                      local.get $l10
                      local.get $l35
                      f32.store offset=4
                      local.get $l10
                      local.get $l36
                      f32.store
                      local.get $l10
                      local.get $l50
                      f32.store offset=92
                      local.get $l10
                      local.get $l49
                      f32.store offset=88
                      local.get $l10
                      local.get $l48
                      f32.store offset=84
                      local.get $l10
                      local.get $l53
                      f32.store offset=80
                      local.get $l10
                      local.get $l52
                      f32.store offset=76
                      local.get $l10
                      local.get $l56
                      f32.store offset=68
                      local.get $l10
                      i32.const -64
                      i32.sub
                      local.get $l60
                      f32.store
                      local.get $l10
                      local.get $l59
                      f32.store offset=60
                      local.get $l10
                      local.get $l47
                      f32.store offset=56
                      local.get $l10
                      local.get $l46
                      f32.store offset=52
                      local.get $l10
                      local.get $l43
                      f32.store offset=44
                      local.get $l10
                      local.get $l39
                      f32.store offset=40
                      local.get $l10
                      local.get $l45
                      f32.store offset=36
                      local.get $l10
                      local.get $l34
                      f32.store offset=32
                      local.get $l10
                      local.get $l35
                      f32.store offset=28
                      local.get $l10
                      local.get $l37
                      f32.store offset=20
                      local.get $l10
                      local.get $l38
                      f32.store offset=16
                      local.get $l10
                      i32.const 0
                      i32.store offset=160
                      local.get $l10
                      i64.const 0
                      i64.store offset=112 align=4
                      local.get $l10
                      local.get $l74
                      f32.store offset=156
                      local.get $l10
                      local.get $l58
                      f32.store offset=164
                      block $B54 (result f32)
                        local.get $l21
                        i32.load8_u
                        i32.const 1
                        i32.eq
                        if $I55
                          local.get $l10
                          local.get $l14
                          local.get $l17
                          i32.const 3
                          i32.shl
                          i32.add
                          local.tee $l23
                          f32.load offset=56
                          f32.store offset=104
                          local.get $l23
                          f32.load offset=60
                          br $B54
                        end
                        local.get $l10
                        i32.const -8388609
                        i32.store offset=104
                        f32.const 0x1.fffffep+127 (;=3.40282e+38;)
                      end
                      local.set $l34
                      i32.const 1
                      local.get $l15
                      i32.shl
                      local.set $l23
                      local.get $l10
                      local.get $l34
                      f32.store offset=108
                      block $B56
                        block $B57
                          local.get $l10
                          block $B58 (result f32)
                            block $B59
                              block $B60
                                local.get $l16
                                if $I61
                                  local.get $l31
                                  local.get $l15
                                  i32.const 2
                                  i32.shl
                                  i32.add
                                  local.tee $l16
                                  f32.load offset=12
                                  local.set $l35
                                  local.get $l16
                                  f32.load
                                  local.set $l34
                                  local.get $l21
                                  i32.load8_u
                                  i32.const 1
                                  i32.eq
                                  if $I62
                                    local.get $l14
                                    local.get $l17
                                    i32.const 3
                                    i32.shl
                                    i32.add
                                    local.tee $l16
                                    f32.load offset=60
                                    local.tee $l36
                                    local.get $l16
                                    f32.load offset=56
                                    local.tee $l37
                                    local.get $l35
                                    local.get $l35
                                    local.get $l37
                                    f32.lt
                                    select
                                    local.tee $l35
                                    local.get $l35
                                    local.get $l36
                                    f32.gt
                                    select
                                    local.set $l35
                                  end
                                  local.get $l34
                                  f32.neg
                                  local.set $l37
                                  block $B63 (result f32)
                                    local.get $l19
                                    i32.load offset=116
                                    local.tee $l16
                                    i32.const 2
                                    i32.eq
                                    if $I64
                                      f32.const 0x1.08b2a2p+83 (;=1e+25;)
                                      local.set $l36
                                      f32.const 0x0p+0 (;=0;)
                                      br $B63
                                    end
                                    local.get $l16
                                    i32.const 3
                                    i32.ne
                                    br_if $B60
                                    f32.const 0x0p+0 (;=0;)
                                    local.set $l36
                                    f32.const 0x1.08b2a2p+83 (;=1e+25;)
                                  end
                                  local.tee $l34
                                  local.get $l37
                                  f32.mul
                                  local.get $l42
                                  f32.mul
                                  local.set $l38
                                  local.get $l36
                                  local.get $l42
                                  f32.mul
                                  local.get $l34
                                  f32.add
                                  local.get $l42
                                  f32.mul
                                  local.set $l37
                                  br $B59
                                end
                                local.get $l10
                                i64.const 0
                                i64.store offset=124 align=4
                                local.get $l10
                                i64.const 0
                                i64.store offset=148 align=4
                                local.get $l10
                                i64.const 0
                                i64.store offset=140 align=4
                                local.get $l10
                                i64.const 0
                                i64.store offset=132 align=4
                                br $B56
                              end
                              local.get $l19
                              f32.load offset=108
                              local.tee $l34
                              local.get $l37
                              f32.mul
                              local.get $l42
                              f32.mul
                              local.set $l38
                              local.get $l34
                              local.get $l19
                              f32.load offset=104
                              local.tee $l36
                              local.get $l42
                              f32.mul
                              f32.add
                              local.get $l42
                              f32.mul
                              local.set $l37
                              f32.const 0x0p+0 (;=0;)
                              local.set $l34
                              block $B65
                                local.get $l16
                                br_table $B59 $B65 $B57
                              end
                              local.get $l10
                              local.get $l44
                              local.get $l38
                              f32.const 0x1p+0 (;=1;)
                              local.get $l37
                              f32.const 0x1p+0 (;=1;)
                              f32.add
                              f32.div
                              local.tee $l34
                              f32.mul
                              f32.mul
                              f32.store offset=124
                              local.get $l10
                              local.get $l44
                              local.get $l37
                              local.get $l34
                              f32.neg
                              f32.mul
                              f32.mul
                              f32.store offset=136
                              local.get $l44
                              local.get $l36
                              local.get $l34
                              f32.mul
                              f32.mul
                              br $B58
                            end
                            local.get $l10
                            local.get $l37
                            f32.const 0x1p+0 (;=1;)
                            local.get $l40
                            local.get $l37
                            f32.mul
                            f32.const 0x1p+0 (;=1;)
                            f32.add
                            f32.div
                            f32.const 0x0p+0 (;=0;)
                            local.get $l40
                            f32.const 0x0p+0 (;=0;)
                            f32.gt
                            select
                            local.tee $l34
                            f32.neg
                            f32.mul
                            f32.store offset=136
                            local.get $l10
                            local.get $l38
                            local.get $l34
                            f32.mul
                            f32.store offset=124
                            local.get $l36
                            local.get $l34
                            f32.mul
                          end
                          local.get $l42
                          f32.mul
                          f32.store offset=128
                        end
                        local.get $l10
                        f32.const 0x1p+0 (;=1;)
                        f32.const 0x1p+0 (;=1;)
                        local.get $l34
                        f32.sub
                        local.get $p9
                        select
                        f32.store offset=144
                        local.get $l10
                        local.get $l35
                        f32.store offset=132
                        local.get $l28
                        f32.load
                        local.set $l34
                        local.get $l10
                        i32.const 0
                        i32.store offset=152
                        local.get $l10
                        i32.const 0
                        i32.store offset=140
                        local.get $l10
                        local.get $l34
                        local.get $p6
                        f32.mul
                        f32.store offset=148
                      end
                      local.get $l23
                      local.get $l27
                      i32.or
                      local.set $l27
                    end
                    local.get $l15
                    i32.const 1
                    i32.add
                    local.set $l15
                  end
                  local.get $l17
                  i32.const 1
                  i32.add
                  local.tee $l17
                  i32.const 6
                  i32.ne
                  br_if $L48
                end
                local.get $l18
                i32.load8_u
                i32.eqz
                br_if $B30
                local.get $l11
                local.get $l86
                local.get $l83
                f32.add
                local.tee $l34
                local.get $l84
                local.get $l85
                f32.add
                local.tee $l35
                f32.sub
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                f32.store offset=76
                local.get $l11
                local.get $l35
                local.get $l34
                f32.add
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                f32.store offset=68
                local.get $l11
                local.get $l69
                local.get $l68
                f32.mul
                local.tee $l34
                local.get $l34
                f32.add
                local.get $l67
                local.get $l70
                f32.mul
                local.tee $l42
                local.get $l34
                local.get $l71
                local.get $l66
                f32.mul
                local.tee $l35
                local.get $l65
                local.get $l72
                f32.mul
                local.tee $l36
                f32.add
                f32.add
                local.tee $l40
                f32.sub
                local.tee $l34
                f32.add
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                local.tee $l43
                f32.store offset=80
                local.get $l11
                i32.const -64
                i32.sub
                local.get $l36
                local.get $l36
                f32.add
                local.get $l34
                f32.add
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                local.tee $l39
                f32.store
                local.get $l11
                local.get $l76
                local.get $l75
                f32.add
                local.tee $l36
                local.get $l77
                local.get $l92
                f32.add
                local.tee $l37
                f32.add
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                f32.store offset=72
                local.get $l11
                local.get $l78
                local.get $l81
                f32.add
                local.tee $l38
                local.get $l80
                local.get $l79
                f32.add
                local.tee $l41
                f32.sub
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                f32.store offset=60
                local.get $l11
                local.get $l36
                local.get $l37
                f32.sub
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                f32.store offset=56
                local.get $l11
                local.get $l41
                local.get $l38
                f32.add
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                f32.store offset=52
                local.get $l11
                local.get $l35
                local.get $l35
                f32.add
                local.get $l34
                f32.add
                f32.const 0x1p-1 (;=0.5;)
                f32.mul
                local.tee $l34
                f32.store offset=48
                local.get $l42
                local.get $l40
                f32.add
                f32.const 0x0p+0 (;=0;)
                f32.eq
                if $I66
                  local.get $l11
                  local.get $l43
                  f32.const 0x1p-23 (;=1.19209e-07;)
                  f32.add
                  f32.store offset=80
                  local.get $l11
                  local.get $l39
                  f32.const 0x1p-23 (;=1.19209e-07;)
                  f32.add
                  f32.store offset=64
                  local.get $l11
                  local.get $l34
                  f32.const 0x1p-23 (;=1.19209e-07;)
                  f32.add
                  f32.store offset=48
                end
                local.get $l11
                local.get $l82
                f32.neg
                f32.store offset=44
                local.get $l11
                local.get $l93
                f32.neg
                f32.store offset=40
                local.get $l11
                local.get $l87
                f32.neg
                f32.store offset=36
                local.get $p7
                local.get $l55
                f32.mul
                local.set $l55
                i32.const 0
                local.set $l15
                loop $L67
                  local.get $l14
                  local.get $l15
                  i32.add
                  i32.load8_u offset=258
                  i32.eqz
                  if $I68
                    local.get $l11
                    i32.const 36
                    i32.add
                    local.get $l15
                    i32.const 2
                    i32.shl
                    i32.add
                    f32.load
                    local.set $l40
                    local.get $l11
                    i32.const 48
                    i32.add
                    local.get $l15
                    i32.const 12
                    i32.mul
                    i32.add
                    local.tee $l10
                    f32.load
                    local.set $l34
                    local.get $l10
                    f32.load offset=4
                    local.set $l35
                    local.get $l10
                    f32.load offset=8
                    local.set $l36
                    local.get $l29
                    i32.load
                    local.set $l10
                    local.get $l11
                    i64.const 0
                    i64.store offset=104
                    local.get $l11
                    i64.const 0
                    i64.store offset=96
                    local.get $l11
                    i32.const 0
                    i32.store offset=124
                    local.get $l11
                    local.get $l36
                    f32.store offset=120
                    local.get $l11
                    local.get $l35
                    f32.store offset=116
                    local.get $l11
                    local.get $l34
                    f32.store offset=112
                    local.get $l11
                    i64.const 0
                    i64.store offset=8
                    local.get $l11
                    i64.const 0
                    i64.store
                    local.get $l11
                    i32.const 0
                    i32.store offset=28
                    local.get $l11
                    local.get $l36
                    f32.neg
                    f32.store offset=24
                    local.get $l11
                    local.get $l35
                    f32.neg
                    f32.store offset=20
                    local.get $l11
                    local.get $l34
                    f32.neg
                    f32.store offset=16
                    local.get $p0
                    local.get $p4
                    local.get $p3
                    local.get $l10
                    local.get $l11
                    i32.const 96
                    i32.add
                    local.get $l11
                    i32.const 160
                    i32.add
                    local.get $p2
                    local.get $l11
                    local.get $l11
                    i32.const 128
                    i32.add
                    call $f71011
                    f32.const 0x0p+0 (;=0;)
                    local.set $l42
                    local.get $l34
                    local.get $l11
                    f32.load offset=176
                    local.tee $l37
                    f32.mul
                    local.get $l35
                    local.get $l11
                    f32.load offset=180
                    local.tee $l38
                    f32.mul
                    f32.add
                    local.get $l36
                    local.get $l11
                    f32.load offset=184
                    local.tee $l41
                    f32.mul
                    f32.add
                    local.get $l34
                    local.get $l11
                    f32.load offset=144
                    local.tee $l43
                    f32.mul
                    local.get $l35
                    local.get $l11
                    f32.load offset=148
                    local.tee $l39
                    f32.mul
                    f32.add
                    local.get $l36
                    local.get $l11
                    f32.load offset=152
                    local.tee $l45
                    f32.mul
                    f32.add
                    f32.sub
                    local.tee $l44
                    f32.const 0x1.4f8b58p-17 (;=1e-05;)
                    f32.gt
                    if $I69
                      f32.const 0x1p+0 (;=1;)
                      local.get $l44
                      f32.const 0x1.a36e2ep-14 (;=0.0001;)
                      f32.add
                      f32.div
                      local.set $l42
                    end
                    local.get $p3
                    local.get $p3
                    i32.load offset=192
                    local.tee $l10
                    i32.const 1
                    i32.add
                    i32.store offset=192
                    local.get $p3
                    i32.load offset=188
                    local.get $l10
                    i32.const 80
                    i32.mul
                    i32.add
                    local.tee $l10
                    local.get $l34
                    f32.store offset=48
                    local.get $l10
                    local.get $l41
                    f32.store offset=8
                    local.get $l10
                    local.get $l38
                    f32.store offset=4
                    local.get $l10
                    local.get $l37
                    f32.store
                    local.get $l10
                    local.get $l36
                    f32.store offset=56
                    local.get $l10
                    local.get $l35
                    f32.store offset=52
                    local.get $l10
                    local.get $l11
                    f32.load offset=160
                    f32.store offset=12
                    local.get $l10
                    local.get $l11
                    f32.load offset=164
                    f32.store offset=16
                    local.get $l11
                    f32.load offset=168
                    local.set $l34
                    local.get $l10
                    local.get $l45
                    f32.store offset=32
                    local.get $l10
                    local.get $l39
                    f32.store offset=28
                    local.get $l10
                    local.get $l43
                    f32.store offset=24
                    local.get $l10
                    local.get $l34
                    f32.store offset=20
                    local.get $l10
                    local.get $l11
                    f32.load offset=128
                    f32.store offset=36
                    local.get $l10
                    local.get $l11
                    f32.load offset=132
                    f32.store offset=40
                    local.get $l11
                    f32.load offset=136
                    local.set $l34
                    local.get $l10
                    local.get $l55
                    f32.store offset=68
                    local.get $l10
                    local.get $l40
                    f32.store offset=64
                    local.get $l10
                    local.get $l42
                    f32.store offset=60
                    local.get $l10
                    local.get $l34
                    f32.store offset=44
                  end
                  local.get $l15
                  i32.const 1
                  i32.add
                  local.tee $l15
                  i32.const 3
                  i32.ne
                  br_if $L67
                end
              end
              local.get $l13
              local.get $l27
              i32.store8 offset=78
              local.get $l11
              i32.const 192
              i32.add
              global.set $g0
              local.get $p0
              local.get $p2
              i32.const 80
              i32.mul
              i32.add
              local.tee $p2
              i64.load offset=24
              local.set $l94
              local.get $p2
              i64.load offset=16
              local.set $l96
              local.get $p2
              i64.load offset=8
              local.set $l95
              local.get $p2
              i64.load
              local.set $l98
              loop $L70
                block $B71
                  block $B72 (result i32)
                    block $B73
                      local.get $l95
                      local.get $l98
                      i64.or
                      local.tee $l99
                      local.get $l96
                      i64.or
                      i64.eqz
                      if $I74
                        i32.const 192
                        local.set $p2
                        local.get $l94
                        local.set $l97
                        local.get $l94
                        i64.eqz
                        br_if $B71
                        br $B73
                      end
                      i32.const 192
                      local.set $p2
                      local.get $l94
                      local.set $l97
                      local.get $l94
                      i64.eqz
                      i32.eqz
                      br_if $B73
                      i32.const 128
                      local.set $p2
                      local.get $l96
                      local.set $l97
                      local.get $l96
                      i64.const 0
                      i64.ne
                      br_if $B73
                      local.get $l99
                      i64.eqz
                      i32.eqz
                      if $I75
                        local.get $l98
                        local.get $l95
                        local.get $l95
                        i64.eqz
                        select
                        local.set $l97
                        local.get $l95
                        i64.const 0
                        i64.ne
                        i32.const 6
                        i32.shl
                        local.set $p2
                        br $B73
                      end
                      i32.const -1
                      br $B72
                    end
                    local.get $l97
                    i64.const 32
                    i64.shr_u
                    i32.wrap_i64
                    local.tee $l12
                    i32.clz
                    i32.const 63
                    i32.xor
                    i32.const 31
                    local.get $l97
                    i32.wrap_i64
                    i32.clz
                    i32.sub
                    local.get $l12
                    select
                    local.get $p2
                    i32.add
                  end
                  local.set $p2
                  local.get $p1
                  local.get $p1
                  i32.load offset=1064
                  local.tee $l12
                  i32.const 1
                  i32.add
                  i32.store offset=1064
                  local.get $p1
                  i32.const 40
                  i32.add
                  local.get $l12
                  i32.const 2
                  i32.shl
                  i32.add
                  local.get $p2
                  i32.store
                  local.get $l24
                  i64.const 0
                  i64.store
                  local.get $l25
                  i64.const 0
                  i64.store
                  local.get $l26
                  i64.const 0
                  i64.store
                  local.get $p1
                  i64.const 0
                  i64.store offset=8
                  local.get $p1
                  i32.const 8
                  i32.add
                  local.get $p2
                  i32.const 3
                  i32.shr_u
                  i32.const 536870904
                  i32.and
                  i32.add
                  local.tee $l12
                  local.get $l12
                  i64.load
                  i64.const 1
                  local.get $p2
                  i32.const 63
                  i32.and
                  i64.extend_i32_u
                  i64.shl
                  i64.or
                  i64.store
                  local.get $l94
                  local.get $l24
                  i64.load
                  i64.const -1
                  i64.xor
                  i64.and
                  local.set $l94
                  local.get $l96
                  local.get $l25
                  i64.load
                  i64.const -1
                  i64.xor
                  i64.and
                  local.set $l96
                  local.get $l95
                  local.get $l26
                  i64.load
                  i64.const -1
                  i64.xor
                  i64.and
                  local.set $l95
                  local.get $l98
                  local.get $p1
                  i64.load offset=8
                  i64.const -1
                  i64.xor
                  i64.and
                  local.set $l98
                  br $L70
                end
              end
              local.get $p1
              i32.load offset=1064
              local.tee $p2
              br_if $L17
            end
          end
          local.get $p1
          i32.const 1072
          i32.add
          global.set $g0
          return
        end
        local.get $l97
        i64.const 32
        i64.shr_u
        i32.wrap_i64
        local.tee $l12
        i32.clz
        i32.const 63
        i32.xor
        i32.const 31
        local.get $l97
        i32.wrap_i64
        i32.clz
        i32.sub
        local.get $l12
        select
        local.get $p2
        i32.add
      end
      local.set $p2
      local.get $p1
      local.get $p1
      i32.load offset=1064
      local.tee $l12
      i32.const 1
      i32.add
      i32.store offset=1064
      local.get $p1
      i32.const 40
      i32.add
      local.get $l12
      i32.const 2
      i32.shl
      i32.add
      local.get $p2
      i32.store
      local.get $l24
      i64.const 0
      i64.store
      local.get $l25
      i64.const 0
      i64.store
      local.get $l26
      i64.const 0
      i64.store
      local.get $p1
      i64.const 0
      i64.store offset=8
      local.get $p1
      i32.const 8
      i32.add
      local.get $p2
      i32.const 3
      i32.shr_u
      i32.const 536870904
      i32.and
      i32.add
      local.tee $l12
      local.get $l12
      i64.load
      i64.const 1
      local.get $p2
      i32.const 63
      i32.and
      i64.extend_i32_u
      i64.shl
      i64.or
      i64.store
      local.get $l94
      local.get $l24
      i64.load
      i64.const -1
      i64.xor
      i64.and
      local.set $l94
      local.get $l96
      local.get $l25
      i64.load
      i64.const -1
      i64.xor
      i64.and
      local.set $l96
      local.get $l95
      local.get $l26
      i64.load
      i64.const -1
      i64.xor
      i64.and
      local.set $l95
      local.get $l98
      local.get $p1
      i64.load offset=8
      i64.const -1
      i64.xor
      i64.and
      local.set $l98
      br $L10
    end
    unreachable)
