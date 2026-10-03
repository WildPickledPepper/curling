  (func $f70078 (type $t100) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32) (param $p9 i32) (param $p10 i32) (param $p11 i32) (result i32)
    (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $l12
    global.set $g0
    local.get $p9
    f32.load offset=12
    local.set $l27
    local.get $p9
    f32.load offset=8
    local.set $l28
    local.get $p9
    f32.load offset=4
    local.set $l29
    local.get $p9
    f32.load
    local.set $l30
    f32.const 0x1.fffffep+127 (;=3.40282e+38;)
    local.set $l25
    block $B0 (result i32)
      block $B1
        block $B2
          local.get $p0
          i32.load offset=16
          i32.eqz
          if $I3
            br $B2
          end
          local.get $p5
          f32.load offset=56
          local.tee $l32
          local.get $p1
          f32.load
          local.tee $l15
          local.get $p5
          f32.load offset=8
          f32.mul
          local.get $p1
          f32.load offset=4
          local.tee $l16
          local.get $p5
          f32.load offset=24
          f32.mul
          f32.add
          local.get $p1
          f32.load offset=8
          local.tee $l17
          local.get $p5
          f32.load offset=40
          f32.mul
          f32.add
          f32.add
          local.set $l33
          local.get $p5
          f32.load offset=52
          local.tee $l34
          local.get $l15
          local.get $p5
          f32.load offset=4
          f32.mul
          local.get $l16
          local.get $p5
          f32.load offset=20
          f32.mul
          f32.add
          local.get $l17
          local.get $p5
          f32.load offset=36
          f32.mul
          f32.add
          f32.add
          local.set $l35
          local.get $p5
          f32.load offset=48
          local.tee $l36
          local.get $l15
          local.get $p5
          f32.load
          f32.mul
          local.get $l16
          local.get $p5
          f32.load offset=16
          f32.mul
          f32.add
          local.get $l17
          local.get $p5
          f32.load offset=32
          f32.mul
          f32.add
          f32.add
          local.set $l37
          local.get $p1
          f32.load offset=56
          local.tee $l38
          f32.neg
          local.set $l39
          local.get $p1
          f32.load offset=52
          local.tee $l40
          f32.neg
          local.set $l41
          local.get $p1
          f32.load offset=48
          local.tee $l42
          f32.neg
          local.set $l43
          local.get $p1
          f32.load offset=44
          local.set $l31
          loop $L4
            local.get $p0
            i32.load offset=24
            local.get $l13
            i32.const 20
            i32.mul
            i32.add
            local.tee $p1
            f32.load offset=12
            local.set $l44
            local.get $p0
            i32.load offset=28
            local.get $p1
            i32.load8_u offset=19
            i32.const 12
            i32.mul
            i32.add
            local.tee $p5
            f32.load offset=8
            local.set $l45
            local.get $p5
            f32.load
            local.set $l46
            local.get $p5
            f32.load offset=4
            local.set $l47
            local.get $p2
            i32.load offset=40
            local.tee $p5
            f32.load offset=36
            local.set $l22
            local.get $p5
            f32.load offset=40
            local.set $l19
            local.get $p1
            f32.load
            local.set $l15
            local.get $p5
            f32.load offset=20
            local.set $l20
            local.get $p1
            f32.load offset=4
            local.set $l16
            local.get $p5
            f32.load offset=24
            local.set $l21
            local.get $p1
            f32.load offset=8
            local.set $l17
            local.get $p5
            f32.load offset=32
            local.set $l23
            local.get $p5
            f32.load offset=8
            local.set $l18
            local.get $p5
            f32.load
            local.set $l24
            local.get $p5
            f32.load offset=4
            local.set $l26
            local.get $p5
            f32.load offset=16
            local.set $l48
            local.get $p4
            f32.load offset=40
            local.set $l49
            local.get $p4
            f32.load offset=8
            local.set $l50
            local.get $p4
            f32.load offset=24
            local.set $l51
            local.get $p4
            f32.load offset=32
            local.set $l52
            local.get $p4
            f32.load
            local.set $l53
            local.get $p4
            f32.load offset=16
            local.set $l54
            local.get $p4
            f32.load offset=36
            local.set $l55
            local.get $p4
            f32.load offset=4
            local.set $l56
            local.get $p4
            f32.load offset=20
            local.set $l57
            local.get $l12
            i32.const 0
            i32.store offset=12
            local.get $l12
            local.get $l56
            local.get $l15
            local.get $l24
            f32.mul
            local.get $l16
            local.get $l26
            f32.mul
            f32.add
            local.get $l17
            local.get $l18
            f32.mul
            f32.add
            local.tee $l18
            f32.const 0x1p+0 (;=1;)
            local.get $l18
            local.get $l18
            f32.mul
            local.get $l15
            local.get $l48
            f32.mul
            local.get $l16
            local.get $l20
            f32.mul
            f32.add
            local.get $l17
            local.get $l21
            f32.mul
            f32.add
            local.tee $l20
            local.get $l20
            f32.mul
            f32.add
            local.get $l15
            local.get $l23
            f32.mul
            local.get $l16
            local.get $l22
            f32.mul
            f32.add
            local.get $l17
            local.get $l19
            f32.mul
            f32.add
            local.tee $l19
            local.get $l19
            f32.mul
            f32.add
            f32.sqrt
            f32.div
            local.tee $l18
            f32.mul
            local.tee $l22
            f32.mul
            local.get $l57
            local.get $l20
            local.get $l18
            f32.mul
            local.tee $l20
            f32.mul
            f32.add
            local.get $l55
            local.get $l19
            local.get $l18
            f32.mul
            local.tee $l19
            f32.mul
            f32.add
            local.tee $l21
            f32.store offset=4
            local.get $l12
            local.get $l52
            local.get $l19
            f32.mul
            local.get $l53
            local.get $l22
            f32.mul
            local.get $l54
            local.get $l20
            f32.mul
            f32.add
            f32.add
            local.tee $l23
            f32.store
            local.get $l12
            local.get $l22
            local.get $l50
            f32.mul
            local.get $l20
            local.get $l51
            f32.mul
            f32.add
            local.get $l19
            local.get $l49
            f32.mul
            f32.add
            local.tee $l24
            f32.store offset=8
            block $B5
              local.get $l33
              local.get $l19
              f32.mul
              local.get $l37
              local.get $l22
              f32.mul
              local.get $l35
              local.get $l20
              f32.mul
              f32.add
              f32.add
              local.tee $l26
              local.get $l23
              local.get $l42
              local.get $l43
              local.get $l23
              f32.const 0x0p+0 (;=0;)
              f32.gt
              select
              f32.mul
              local.get $l21
              local.get $l40
              local.get $l41
              local.get $l21
              f32.const 0x0p+0 (;=0;)
              f32.gt
              select
              f32.mul
              f32.add
              local.get $l24
              local.get $l38
              local.get $l39
              local.get $l24
              f32.const 0x0p+0 (;=0;)
              f32.gt
              select
              f32.mul
              f32.add
              local.tee $l21
              local.get $l31
              local.get $l21
              local.get $l31
              f32.gt
              select
              local.tee $l23
              f32.add
              local.tee $l24
              local.get $l18
              local.get $l44
              f32.neg
              f32.mul
              local.tee $l21
              local.get $l21
              local.get $l24
              f32.gt
              select
              local.get $l46
              local.get $l15
              f32.mul
              local.get $l47
              local.get $l16
              f32.mul
              f32.add
              local.get $l45
              local.get $l17
              f32.mul
              f32.add
              local.get $l18
              f32.mul
              local.tee $l15
              local.get $l26
              local.get $l23
              f32.sub
              local.tee $l16
              local.get $l15
              local.get $l16
              f32.gt
              select
              f32.sub
              local.get $l25
              f32.gt
              br_if $B5
              local.get $p3
              local.get $l12
              local.get $l12
              i32.const 32
              i32.add
              local.get $l12
              i32.const 16
              i32.add
              local.get $p3
              i32.load
              i32.load offset=12
              call_indirect $__indirect_function_table (type $t4)
              local.get $l12
              local.get $l32
              local.get $l19
              f32.mul
              local.get $l36
              local.get $l22
              f32.mul
              local.get $l34
              local.get $l20
              f32.mul
              f32.add
              f32.add
              local.tee $l17
              local.get $l12
              f32.load offset=32
              f32.add
              local.tee $l16
              f32.store offset=32
              local.get $l12
              local.get $l17
              local.get $l12
              f32.load offset=16
              f32.add
              local.tee $l17
              f32.store offset=16
              local.get $l16
              local.get $l21
              local.get $p6
              f32.load
              local.tee $l18
              f32.add
              f32.gt
              br_if $B1
              local.get $l15
              local.get $l17
              local.get $l18
              f32.add
              f32.gt
              br_if $B1
              local.get $l25
              local.get $l21
              local.get $l16
              f32.sub
              local.tee $l15
              f32.gt
              i32.eqz
              br_if $B5
              f32.const 0x0p+0 (;=0;)
              local.set $l27
              local.get $l22
              local.set $l30
              local.get $l20
              local.set $l29
              local.get $l19
              local.set $l28
              local.get $l15
              local.set $l25
              local.get $l13
              local.set $l14
            end
            local.get $l13
            i32.const 1
            i32.add
            local.tee $l13
            local.get $p0
            i32.load offset=16
            i32.lt_u
            br_if $L4
          end
        end
        local.get $l25
        local.get $p7
        f32.load
        f32.lt
        if $I6
          local.get $p9
          local.get $l27
          f32.store offset=12
          local.get $p9
          local.get $l28
          f32.store offset=8
          local.get $p9
          local.get $l29
          f32.store offset=4
          local.get $p9
          local.get $l30
          f32.store
          local.get $p7
          local.get $l25
          f32.store
          local.get $p11
          local.get $p10
          i32.store
        end
        local.get $p8
        local.get $l14
        i32.store
        i32.const 1
        br $B0
      end
      i32.const 0
    end
    local.set $p4
    local.get $l12
    i32.const 48
    i32.add
    global.set $g0
    local.get $p4)