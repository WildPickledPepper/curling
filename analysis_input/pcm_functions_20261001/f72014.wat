  (func $f72014 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 f32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $l3
    global.set $g0
    local.get $p0
    i32.load offset=4
    local.set $l1
    block $B0
      local.get $p0
      i32.load offset=268
      local.tee $l4
      i32.const 1048576
      i32.and
      i32.eqz
      if $I1
        local.get $p0
        local.get $p0
        f32.load offset=32
        f32.store offset=208
        local.get $p0
        local.get $p0
        i64.load offset=36 align=4
        i64.store offset=212 align=4
        local.get $p0
        local.get $p0
        i64.load offset=44 align=4
        i64.store offset=220 align=4
        local.get $p0
        local.get $p0
        i64.load offset=52 align=4
        i64.store offset=228 align=4
        br $B0
      end
      local.get $l4
      i32.const 2097152
      i32.and
      i32.eqz
      if $I2
        local.get $p0
        i32.const 16
        i32.add
        local.get $p0
        i32.const 208
        i32.add
        call $f71596
        br $B0
      end
      local.get $p0
      i32.load offset=8
      local.tee $l2
      i32.eqz
      if $I3
        local.get $p0
        local.get $p0
        i32.load
        local.get $l1
        i32.const 24
        i32.shr_u
        i32.const 15
        i32.and
        call $f71984
        local.tee $l2
        i32.store offset=8
      end
      local.get $l2
      f32.load offset=148
      local.set $l17
      local.get $l2
      f32.load offset=152
      local.set $l18
      local.get $l2
      f32.load offset=144
      local.set $l19
      local.get $l2
      f32.load offset=156
      local.set $l20
      local.get $p0
      f32.load offset=48
      local.set $l26
      local.get $p0
      f32.load offset=52
      local.set $l21
      local.get $l3
      local.get $p0
      f32.load offset=40
      local.tee $l11
      local.get $p0
      f32.load offset=32
      local.tee $l12
      local.get $p0
      f32.load offset=76
      local.tee $l6
      local.get $l6
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l15
      local.get $l2
      f32.load offset=160
      local.get $p0
      f32.load offset=80
      f32.sub
      local.tee $l5
      local.get $l5
      f32.add
      local.tee $l5
      f32.mul
      local.get $l6
      local.get $p0
      f32.load offset=72
      local.tee $l10
      local.get $l2
      f32.load offset=164
      local.get $p0
      f32.load offset=84
      f32.sub
      local.tee $l7
      local.get $l7
      f32.add
      local.tee $l13
      f32.mul
      local.get $p0
      f32.load offset=68
      local.tee $l7
      local.get $l2
      f32.load offset=168
      local.get $p0
      f32.load offset=88
      f32.sub
      local.tee $l8
      local.get $l8
      f32.add
      local.tee $l14
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $p0
      i32.const -64
      i32.sub
      f32.load
      local.tee $l8
      local.get $l13
      local.get $l7
      f32.neg
      f32.mul
      local.get $l8
      local.get $l5
      f32.mul
      f32.sub
      local.get $l10
      local.get $l14
      f32.mul
      f32.sub
      local.tee $l16
      f32.mul
      f32.sub
      local.tee $l9
      local.get $l9
      f32.add
      local.tee $l22
      f32.mul
      local.get $l15
      local.get $l13
      f32.mul
      local.get $l6
      local.get $l8
      local.get $l14
      f32.mul
      local.get $l10
      local.get $l5
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l7
      local.get $l16
      f32.mul
      f32.sub
      local.tee $l9
      local.get $l9
      f32.add
      local.tee $l23
      local.get $p0
      f32.load offset=36
      local.tee $l9
      f32.mul
      f32.add
      local.get $l11
      local.get $l15
      local.get $l14
      f32.mul
      local.get $l6
      local.get $l7
      local.get $l5
      f32.mul
      local.get $l8
      local.get $l13
      f32.mul
      f32.sub
      f32.mul
      f32.add
      local.get $l10
      local.get $l16
      f32.mul
      f32.sub
      local.tee $l5
      local.get $l5
      f32.add
      local.tee $l13
      f32.mul
      f32.add
      local.tee $l24
      f32.mul
      local.get $l12
      local.get $l23
      f32.mul
      local.get $l22
      local.get $l9
      f32.mul
      f32.sub
      local.get $p0
      f32.load offset=44
      local.tee $l5
      f32.mul
      local.get $l13
      local.get $l5
      local.get $l5
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l25
      f32.mul
      f32.add
      f32.add
      local.get $p0
      f32.load offset=56
      f32.add
      local.tee $l27
      f32.store offset=40
      local.get $l3
      local.get $l21
      local.get $l9
      local.get $l24
      f32.mul
      local.get $l5
      local.get $l22
      local.get $l11
      f32.mul
      local.get $l12
      local.get $l13
      f32.mul
      f32.sub
      f32.mul
      local.get $l23
      local.get $l25
      f32.mul
      f32.add
      f32.add
      f32.add
      local.tee $l21
      f32.store offset=36
      local.get $l3
      local.get $l5
      local.get $l10
      local.get $l18
      f32.mul
      local.get $l8
      local.get $l19
      f32.mul
      local.get $l6
      local.get $l20
      f32.mul
      f32.add
      local.get $l7
      local.get $l17
      f32.mul
      f32.add
      f32.add
      local.tee $l14
      f32.mul
      local.get $l12
      local.get $l6
      local.get $l19
      f32.mul
      local.get $l8
      local.get $l20
      f32.mul
      f32.sub
      local.get $l7
      local.get $l18
      f32.mul
      f32.sub
      local.get $l10
      local.get $l17
      f32.mul
      f32.add
      local.tee $l15
      f32.mul
      f32.sub
      local.get $l9
      local.get $l8
      local.get $l18
      f32.mul
      local.get $l6
      local.get $l17
      f32.mul
      local.get $l7
      local.get $l20
      f32.mul
      f32.sub
      local.get $l10
      local.get $l19
      f32.mul
      f32.sub
      f32.add
      local.tee $l16
      f32.mul
      f32.sub
      local.get $l11
      local.get $l7
      local.get $l19
      f32.mul
      local.get $l6
      local.get $l18
      f32.mul
      local.get $l10
      local.get $l20
      f32.mul
      f32.sub
      local.get $l8
      local.get $l17
      f32.mul
      f32.sub
      f32.add
      local.tee $l6
      f32.mul
      f32.sub
      local.tee $l10
      f32.store offset=28
      local.get $l3
      local.get $l12
      local.get $l16
      f32.mul
      local.get $l14
      local.get $l11
      f32.mul
      local.get $l6
      local.get $l5
      f32.mul
      f32.add
      f32.add
      local.get $l15
      local.get $l9
      f32.mul
      f32.sub
      local.tee $l7
      f32.store offset=24
      local.get $l3
      local.get $l15
      local.get $l11
      f32.mul
      local.get $l14
      local.get $l9
      f32.mul
      local.get $l16
      local.get $l5
      f32.mul
      f32.add
      f32.add
      local.get $l12
      local.get $l6
      f32.mul
      f32.sub
      local.tee $l8
      f32.store offset=20
      local.get $l3
      local.get $l6
      local.get $l9
      f32.mul
      local.get $l12
      local.get $l14
      f32.mul
      local.get $l15
      local.get $l5
      f32.mul
      f32.add
      f32.add
      local.get $l16
      local.get $l11
      f32.mul
      f32.sub
      local.tee $l6
      f32.store offset=16
      local.get $l3
      local.get $l26
      local.get $l12
      local.get $l24
      f32.mul
      local.get $l5
      local.get $l13
      local.get $l9
      f32.mul
      local.get $l23
      local.get $l11
      f32.mul
      f32.sub
      f32.mul
      local.get $l22
      local.get $l25
      f32.mul
      f32.add
      f32.add
      f32.add
      local.tee $l5
      f32.store offset=32
      local.get $p0
      local.get $l27
      f32.store offset=232
      local.get $p0
      local.get $l21
      f32.store offset=228
      local.get $p0
      local.get $l5
      f32.store offset=224
      local.get $p0
      local.get $l10
      f32.store offset=220
      local.get $p0
      local.get $l7
      f32.store offset=216
      local.get $p0
      local.get $l8
      f32.store offset=212
      local.get $p0
      local.get $l6
      f32.store offset=208
      local.get $p0
      i32.const 16
      i32.add
      local.get $l3
      i32.const 16
      i32.add
      call $f71596
    end
    block $B4
      local.get $l1
      i32.const 1
      i32.and
      i32.eqz
      br_if $B4
      local.get $p0
      i32.load offset=8
      local.tee $l1
      i32.eqz
      if $I5
        local.get $p0
        local.get $p0
        i32.load
        local.get $p0
        i32.load8_u offset=7
        i32.const 15
        i32.and
        call $f71984
        local.tee $l1
        i32.store offset=8
      end
      local.get $p0
      i32.load8_u offset=24
      i32.const 8
      i32.and
      local.set $l2
      block $B6
        local.get $l1
        i32.load8_u
        i32.const 8
        i32.and
        local.tee $l1
        br_if $B6
        local.get $l2
        i32.eqz
        br_if $B6
        local.get $p0
        i32.load
        local.get $p0
        i32.const 1
        call $f71995
        br $B4
      end
      local.get $l2
      br_if $B4
      local.get $l1
      i32.eqz
      br_if $B4
      local.get $p0
      i32.load
      local.get $p0
      i32.const 1
      call $f71994
    end
    block $B7
      local.get $l4
      i32.const -131072001
      i32.and
      i32.eqz
      br_if $B7
      local.get $p0
      i32.load offset=8
      local.tee $l2
      i32.eqz
      if $I8
        local.get $p0
        local.get $p0
        i32.load
        local.get $p0
        i32.load8_u offset=7
        i32.const 15
        i32.and
        call $f71984
        local.tee $l2
        i32.store offset=8
      end
      local.get $p0
      i32.load offset=268
      local.tee $l1
      i32.const 1
      i32.and
      if $I9
        local.get $p0
        i32.const 16
        i32.add
        local.get $l2
        f32.load offset=92
        call $f71607
        local.get $p0
        i32.load offset=268
        local.set $l1
      end
      local.get $l1
      i32.const 2
      i32.and
      if $I10
        local.get $p0
        i32.const 16
        i32.add
        local.get $l2
        i32.const 96
        i32.add
        call $f71609
        local.get $p0
        i32.load offset=268
        local.set $l1
      end
      local.get $l1
      i32.const 4
      i32.and
      if $I11
        local.get $p0
        i32.const 16
        i32.add
        local.get $l2
        f32.load offset=108
        call $f71610
        local.get $p0
        i32.load offset=268
        local.set $l1
      end
      local.get $l1
      i32.const 8
      i32.and
      if $I12
        local.get $p0
        i32.const 16
        i32.add
        local.get $l2
        f32.load offset=112
        call $f71611
        local.get $p0
        i32.load offset=268
        local.set $l1
      end
      local.get $l1
      i32.const 16
      i32.and
      if $I13
        local.get $p0
        i32.const 16
        i32.add
        local.get $l2
        f32.load offset=116
        call $f71612
        local.get $p0
        i32.load offset=268
        local.set $l1
      end
      local.get $l1
      i32.const 32
      i32.and
      if $I14
        local.get $p0
        i32.const 16
        i32.add
        local.get $l2
        f32.load offset=120
        call $f71613
        local.get $p0
        i32.load offset=268
        local.set $l1
      end
      local.get $l1
      i32.const 64
      i32.and
      if $I15
        local.get $p0
        i32.const 16
        i32.add
        local.get $l2
        f32.load offset=124
        call $f71619
        local.get $p0
        i32.load offset=268
        local.set $l1
      end
      local.get $l1
      i32.const 512
      i32.and
      if $I16
        local.get $p0
        i32.const 16
        i32.add
        local.get $l2
        i32.load16_u offset=136
        call $f71624
        local.get $p0
        i32.load offset=268
        local.set $l1
      end
      local.get $l1
      i32.const 256
      i32.and
      if $I17
        local.get $p0
        local.get $l2
        f32.load offset=132
        f32.store offset=124
      end
      local.get $l1
      i32.const 1024
      i32.and
      if $I18
        local.get $p0
        i32.const 16
        i32.add
        local.get $l2
        i32.const 144
        i32.add
        call $f71599
        local.get $p0
        i32.load offset=268
        local.set $l1
      end
      local.get $l1
      i32.const 4096
      i32.and
      if $I19
        local.get $p0
        i32.const 16
        i32.add
        local.get $l2
        f32.load offset=176
        call $f71620
        local.get $p0
        i32.load offset=268
        local.set $l1
      end
      local.get $l1
      i32.const 2048
      i32.and
      if $I20
        local.get $p0
        local.get $l2
        f32.load offset=172
        f32.store offset=108
      end
      local.get $l1
      i32.const 8192
      i32.and
      if $I21 (result i32)
        local.get $p0
        i32.const 16
        i32.add
        local.get $l2
        f32.load offset=180
        call $f71617
        local.get $p0
        i32.load offset=268
      else
        local.get $l1
      end
      i32.const 128
      i32.and
      if $I22
        local.get $p0
        local.get $l2
        f32.load offset=128
        f32.store offset=92
      end
      local.get $l4
      i32.const 16384
      i32.and
      i32.eqz
      br_if $B7
      local.get $p0
      i32.load
      i32.const 2428
      i32.add
      i32.load
      local.set $l1
      local.get $l3
      local.get $l2
      i32.load16_u offset=268
      i32.store16 offset=8
      local.get $p0
      i32.const 16
      i32.add
      local.get $l1
      local.get $l3
      i32.const 8
      i32.add
      call $f71614
    end
    local.get $p0
    call $f72011
    local.get $p0
    i32.const 16
    i32.add
    local.set $l1
    block $B23
      local.get $l4
      i32.const 33554432
      i32.and
      i32.eqz
      if $I24
        local.get $l1
        i32.load
        local.tee $l1
        if $I25 (result i32)
          local.get $l1
          i32.load offset=156
          i32.const -3
          i32.gt_u
        else
          i32.const 1
        end
        local.set $l1
        local.get $p0
        i32.load offset=4
        i32.const -1073741825
        i32.gt_u
        br_if $B23
        local.get $p0
        local.get $l1
        i32.store offset=264
        br $B23
      end
      local.get $l1
      call $f71615
    end
    local.get $p0
    call $f72019
    local.get $p0
    i32.const 0
    i32.store offset=8
    local.get $p0
    i32.const 0
    i32.store offset=268
    local.get $p0
    local.get $p0
    i32.load8_u offset=7
    i32.const 24
    i32.shl
    i32.store offset=4
    local.get $l3
    i32.const 48
    i32.add
    global.set $g0)