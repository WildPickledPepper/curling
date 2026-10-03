  (func $f70576 (type $t18) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (result i32)
    (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 i64)
    global.get $g0
    i32.const 960
    i32.sub
    local.tee $l8
    global.set $g0
    local.get $p5
    i32.load
    local.set $p5
    local.get $p0
    f32.load offset=8
    local.set $l35
    local.get $p0
    f32.load offset=12
    local.set $l36
    local.get $p0
    f32.load offset=4
    local.set $l37
    local.get $l8
    i32.const 0
    i32.store offset=828
    local.get $l8
    local.get $l36
    f32.store offset=824
    local.get $l8
    local.get $l35
    f32.store offset=820
    local.get $l8
    local.get $l37
    f32.store offset=816
    local.get $p1
    f32.load offset=8
    local.set $l38
    local.get $p1
    f32.load offset=12
    local.set $l39
    local.get $p1
    f32.load offset=4
    local.set $l41
    local.get $l8
    i32.const 0
    i32.store offset=812
    local.get $l8
    local.get $l39
    f32.store offset=808
    local.get $l8
    local.get $l38
    f32.store offset=804
    local.get $l8
    local.get $l41
    f32.store offset=800
    local.get $l8
    local.get $p4
    f32.load
    f32.store offset=784
    local.get $p2
    local.tee $p7
    f32.load offset=20
    local.set $l30
    local.get $p7
    f32.load offset=24
    local.set $l28
    local.get $p7
    f32.load
    local.set $l25
    local.get $p7
    f32.load offset=4
    local.set $l27
    local.get $p7
    f32.load offset=8
    local.set $l29
    local.get $p7
    f32.load offset=12
    local.set $l40
    local.get $p7
    f32.load offset=16
    local.set $l31
    local.get $l8
    i32.const 0
    i32.store offset=780
    local.get $l8
    local.get $l28
    f32.store offset=776
    local.get $l8
    local.get $l30
    f32.store offset=772
    local.get $l8
    local.get $l31
    f32.store offset=768
    local.get $l8
    local.get $l40
    f32.store offset=764
    local.get $l8
    local.get $l29
    f32.store offset=760
    local.get $l8
    local.get $l27
    f32.store offset=756
    local.get $l8
    local.get $l25
    f32.store offset=752
    local.get $p3
    f32.load offset=20
    local.set $l33
    local.get $p3
    f32.load offset=24
    local.set $l34
    local.get $p3
    f32.load
    local.set $l23
    local.get $p3
    f32.load offset=4
    local.set $l26
    local.get $p3
    f32.load offset=8
    local.set $l24
    local.get $p3
    f32.load offset=12
    local.set $l22
    local.get $p3
    f32.load offset=16
    local.set $l32
    local.get $l8
    i32.const 0
    i32.store offset=748
    local.get $l8
    local.get $l34
    f32.store offset=744
    local.get $l8
    local.get $l33
    f32.store offset=740
    local.get $l8
    local.get $l32
    f32.store offset=736
    local.get $l8
    local.get $l22
    f32.store offset=732
    local.get $l8
    local.get $l24
    f32.store offset=728
    local.get $l8
    local.get $l26
    f32.store offset=724
    local.get $l8
    local.get $l23
    f32.store offset=720
    local.get $l8
    i32.const 0
    i32.store offset=716
    local.get $l8
    local.get $l22
    local.get $l22
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l42
    local.get $l30
    local.get $l33
    f32.sub
    local.tee $l30
    f32.mul
    local.get $l22
    local.get $l23
    local.get $l28
    local.get $l34
    f32.sub
    local.tee $l28
    f32.mul
    local.get $l24
    local.get $l31
    local.get $l32
    f32.sub
    local.tee $l31
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l26
    local.get $l30
    local.get $l26
    f32.neg
    local.tee $l34
    f32.mul
    local.get $l23
    local.get $l31
    f32.mul
    f32.sub
    local.get $l24
    local.get $l28
    f32.mul
    f32.sub
    local.tee $l33
    f32.mul
    f32.sub
    local.tee $l32
    local.get $l32
    f32.add
    f32.store offset=708
    local.get $l8
    i32.const 712
    i32.add
    local.tee $l9
    local.get $l42
    local.get $l28
    f32.mul
    local.get $l22
    local.get $l26
    local.get $l31
    f32.mul
    local.get $l23
    local.get $l30
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l24
    local.get $l33
    f32.mul
    f32.sub
    local.tee $l32
    local.get $l32
    f32.add
    f32.store
    local.get $l8
    local.get $l42
    local.get $l31
    f32.mul
    local.get $l22
    local.get $l24
    local.get $l30
    f32.mul
    local.get $l26
    local.get $l28
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l23
    local.get $l33
    f32.mul
    f32.sub
    local.tee $l30
    local.get $l30
    f32.add
    f32.store offset=704
    local.get $l8
    local.get $l25
    local.get $l26
    f32.mul
    local.get $l27
    local.get $l23
    f32.mul
    f32.sub
    local.get $l29
    local.get $l22
    f32.mul
    local.get $l40
    local.get $l24
    f32.mul
    f32.sub
    f32.add
    local.tee $l30
    f32.store offset=696
    local.get $l8
    local.get $l27
    local.get $l24
    f32.mul
    local.get $l29
    local.get $l26
    f32.mul
    f32.sub
    local.get $l25
    local.get $l22
    f32.mul
    local.get $l40
    local.get $l23
    f32.mul
    f32.sub
    f32.add
    local.tee $l28
    f32.store offset=688
    local.get $l8
    local.get $l29
    local.get $l23
    f32.mul
    local.get $l25
    local.get $l24
    f32.mul
    f32.sub
    local.get $l27
    local.get $l22
    f32.mul
    local.get $l40
    local.get $l26
    f32.mul
    f32.sub
    f32.add
    local.tee $l26
    f32.store offset=692
    local.get $l8
    local.get $l40
    local.get $l22
    f32.mul
    local.get $l27
    local.get $l34
    f32.mul
    local.get $l25
    local.get $l23
    f32.mul
    f32.sub
    local.get $l29
    local.get $l24
    f32.mul
    f32.sub
    f32.sub
    local.tee $l22
    f32.store offset=700
    local.get $l8
    i32.const 0
    i32.store offset=668
    local.get $l8
    f32.const 0x1p+0 (;=1;)
    local.get $l28
    local.get $l28
    local.get $l28
    f32.add
    local.tee $l23
    f32.mul
    f32.sub
    local.tee $l25
    local.get $l26
    local.get $l26
    local.get $l26
    f32.add
    local.tee $l24
    f32.mul
    local.tee $l27
    f32.sub
    f32.store offset=664
    local.get $l8
    local.get $l30
    local.get $l24
    f32.mul
    local.tee $l29
    local.get $l22
    local.get $l23
    f32.mul
    local.tee $l40
    f32.sub
    f32.store offset=660
    local.get $l8
    i32.const 0
    i32.store offset=652
    local.get $l8
    local.get $l29
    local.get $l40
    f32.add
    f32.store offset=648
    local.get $l8
    local.get $l25
    local.get $l30
    local.get $l30
    local.get $l30
    f32.add
    local.tee $l29
    f32.mul
    local.tee $l40
    f32.sub
    f32.store offset=644
    local.get $l8
    local.get $l9
    i64.load
    i64.store offset=680
    local.get $l8
    local.get $l30
    local.get $l23
    f32.mul
    local.tee $l25
    local.get $l22
    local.get $l24
    f32.mul
    local.tee $l24
    f32.add
    f32.store offset=656
    local.get $l8
    local.get $l26
    local.get $l23
    f32.mul
    local.tee $l23
    local.get $l22
    local.get $l29
    f32.mul
    local.tee $l22
    f32.sub
    f32.store offset=640
    local.get $l8
    i32.const 0
    i32.store offset=636
    local.get $l8
    local.get $l25
    local.get $l24
    f32.sub
    f32.store offset=632
    local.get $l8
    local.get $l23
    local.get $l22
    f32.add
    f32.store offset=628
    local.get $l8
    f32.const 0x1p+0 (;=1;)
    local.get $l27
    f32.sub
    local.get $l40
    f32.sub
    f32.store offset=624
    local.get $l8
    local.get $l8
    i64.load offset=704
    i64.store offset=672
    local.get $p5
    i32.load8_u offset=64
    local.set $l20
    local.get $l8
    local.get $p4
    f32.load offset=8
    local.tee $l40
    f32.const 0x1.99999ap-5 (;=0.05;)
    f32.mul
    local.tee $l22
    local.get $l41
    local.get $p1
    i32.load offset=40
    local.tee $p3
    f32.load offset=52
    f32.mul
    local.tee $l23
    local.get $l38
    local.get $p3
    f32.load offset=56
    f32.mul
    local.tee $l24
    local.get $l23
    local.get $l24
    f32.le
    select
    local.tee $l23
    local.get $l39
    local.get $p3
    f32.load offset=60
    f32.mul
    local.tee $l24
    local.get $l23
    local.get $l24
    f32.le
    select
    f32.const 0x1p-2 (;=0.25;)
    f32.mul
    local.tee $l23
    local.get $l22
    local.get $l23
    f32.lt
    select
    local.tee $l23
    local.get $l22
    local.get $l37
    local.get $p0
    i32.load offset=40
    local.tee $p7
    i32.const 52
    i32.add
    local.tee $p4
    f32.load
    f32.mul
    local.tee $l24
    local.get $l35
    local.get $p7
    i32.const 56
    i32.add
    local.tee $p2
    f32.load
    f32.mul
    local.tee $l26
    local.get $l24
    local.get $l26
    f32.le
    select
    local.tee $l24
    local.get $l36
    local.get $p7
    i32.const 60
    i32.add
    local.tee $l11
    f32.load
    f32.mul
    local.tee $l26
    local.get $l24
    local.get $l26
    f32.le
    select
    f32.const 0x1p-2 (;=0.25;)
    f32.mul
    local.tee $l24
    local.get $l22
    local.get $l24
    f32.lt
    select
    local.tee $l22
    local.get $l22
    local.get $l23
    f32.gt
    select
    local.tee $l22
    f32.store offset=608
    local.get $l8
    local.get $l22
    f32.const 0x1.99999ap-1 (;=0.8;)
    f32.mul
    f32.store offset=592
    local.get $p5
    local.get $l8
    i32.const 624
    i32.add
    local.get $l8
    i32.const 592
    i32.add
    call $f70045
    local.get $p5
    i32.load8_u offset=64
    local.set $l12
    local.get $l8
    f32.load offset=808
    local.set $l22
    local.get $l8
    f32.load offset=800
    local.set $l23
    local.get $l8
    f32.load offset=804
    local.set $l24
    local.get $l8
    local.get $p4
    f32.load
    local.tee $l26
    local.get $l8
    f32.load offset=816
    f32.mul
    local.tee $l25
    local.get $l25
    f32.mul
    local.get $p2
    f32.load
    local.tee $l25
    local.get $l8
    f32.load offset=820
    f32.mul
    local.tee $l27
    local.get $l27
    f32.mul
    f32.add
    local.get $l11
    f32.load
    local.tee $l27
    local.get $l8
    f32.load offset=824
    f32.mul
    local.tee $l29
    local.get $l29
    f32.mul
    f32.add
    f32.sqrt
    f32.store offset=576
    local.get $l8
    local.get $l26
    local.get $l23
    f32.mul
    local.tee $l23
    local.get $l23
    f32.mul
    local.get $l25
    local.get $l24
    f32.mul
    local.tee $l23
    local.get $l23
    f32.mul
    f32.add
    local.get $l27
    local.get $l22
    f32.mul
    local.tee $l22
    local.get $l22
    f32.mul
    f32.add
    f32.sqrt
    f32.store offset=560
    block $B0 (result i32)
      block $B1
        local.get $l12
        local.get $l20
        i32.eq
        if $I2
          local.get $p5
          local.get $l8
          i32.const 688
          i32.add
          local.get $l8
          i32.const 752
          i32.add
          local.get $l8
          i32.const 720
          i32.add
          local.get $l8
          i32.const 608
          i32.add
          local.get $l8
          i32.const 576
          i32.add
          local.get $l8
          i32.const 560
          i32.add
          call $f70072
          i32.eqz
          br_if $B1
        end
        local.get $l8
        local.get $l8
        i64.load offset=760
        i64.store offset=216
        local.get $l8
        local.get $l8
        i64.load offset=728
        i64.store offset=376
        local.get $p5
        local.get $l9
        i64.load
        i64.store offset=24
        local.get $l8
        local.get $l8
        i64.load offset=752
        i64.store offset=208
        local.get $l8
        local.get $l8
        i64.load offset=720
        i64.store offset=368
        local.get $p5
        local.get $l8
        i64.load offset=704
        i64.store offset=16
        local.get $p5
        local.get $l8
        i64.load offset=696
        i64.store offset=8
        local.get $p5
        local.get $l8
        i64.load offset=688
        i64.store
        local.get $p5
        local.get $l8
        i64.load offset=216
        i64.store offset=40
        local.get $p5
        local.get $l8
        i64.load offset=208
        i64.store offset=32
        local.get $p5
        local.get $l8
        i64.load offset=368
        i64.store offset=48
        local.get $p5
        local.get $l8
        i64.load offset=376
        i64.store offset=56
        block $B3
          local.get $p0
          f32.load offset=4
          f32.const 0x1p+0 (;=1;)
          f32.ne
          br_if $B3
          local.get $p0
          f32.load offset=8
          f32.const 0x1p+0 (;=1;)
          f32.ne
          br_if $B3
          local.get $p0
          f32.load offset=12
          f32.const 0x1p+0 (;=1;)
          f32.eq
          local.set $l10
        end
        block $B4 (result i32)
          i32.const 0
          local.get $p1
          f32.load offset=4
          f32.const 0x1p+0 (;=1;)
          f32.ne
          br_if $B4
          drop
          i32.const 0
          local.get $p1
          f32.load offset=8
          f32.const 0x1p+0 (;=1;)
          f32.ne
          br_if $B4
          drop
          local.get $p1
          f32.load offset=12
          f32.const 0x1p+0 (;=1;)
          f32.eq
        end
        local.set $p4
        local.get $l8
        i32.const 672
        i32.add
        local.set $l9
        local.get $p0
        i64.load offset=16 align=4
        local.set $l58
        local.get $l8
        local.get $p0
        i64.load offset=24 align=4
        i64.store offset=552
        local.get $l8
        local.get $l58
        i64.store offset=544
        local.get $p1
        i64.load offset=16 align=4
        local.set $l58
        local.get $l8
        local.get $p1
        i64.load offset=24 align=4
        i64.store offset=536
        local.get $l8
        local.get $l58
        i64.store offset=528
        local.get $p7
        f32.load offset=32
        local.set $l22
        local.get $p7
        i64.load offset=24 align=4
        local.set $l58
        local.get $l8
        i32.const 0
        i32.store8 offset=400
        local.get $l8
        i32.const 0
        i32.store offset=396
        local.get $l8
        local.get $l58
        i64.store offset=368
        local.get $l8
        local.get $p7
        i32.store offset=512
        local.get $l8
        i32.const 0
        i32.store offset=380
        local.get $l8
        local.get $l22
        f32.store offset=376
        local.get $l8
        local.get $p7
        i32.load offset=40
        local.get $p7
        i32.load8_u offset=39
        i32.const 20
        i32.mul
        i32.add
        i32.store offset=520
        local.get $l8
        local.get $p7
        i32.load8_u offset=38
        i32.store8 offset=524
        local.get $l8
        local.get $p7
        f32.load offset=52
        local.get $l8
        f32.load offset=816
        f32.mul
        local.tee $l22
        local.get $p7
        f32.load offset=56
        local.get $l8
        f32.load offset=820
        f32.mul
        local.tee $l23
        local.get $l22
        local.get $l23
        f32.le
        select
        local.tee $l22
        local.get $p7
        f32.load offset=60
        local.get $l8
        f32.load offset=824
        f32.mul
        local.tee $l23
        local.get $l22
        local.get $l23
        f32.le
        select
        local.tee $l22
        f32.const 0x1.99999ap-6 (;=0.025;)
        f32.mul
        f32.store offset=392
        local.get $l8
        local.get $l22
        f32.const 0x1.99999ap-5 (;=0.05;)
        f32.mul
        f32.store offset=388
        local.get $l8
        local.get $l22
        f32.const 0x1.99999ap-4 (;=0.1;)
        f32.mul
        f32.store offset=384
        local.get $l8
        i32.const 816
        i32.add
        local.get $l8
        i32.const 544
        i32.add
        local.get $l8
        i32.const 416
        i32.add
        local.get $l8
        i32.const 464
        i32.add
        local.get $l8
        i32.const 368
        i32.add
        local.get $l10
        call $f70494
        local.get $l8
        local.get $p7
        i32.load offset=44
        i32.store offset=516
        local.get $p3
        f32.load offset=32
        local.set $l22
        local.get $p3
        i64.load offset=24 align=4
        local.set $l58
        local.get $l8
        i32.const 0
        i32.store8 offset=240
        local.get $l8
        i32.const 0
        i32.store offset=236
        local.get $l8
        local.get $l58
        i64.store offset=208
        local.get $l8
        local.get $p3
        i32.store offset=352
        local.get $l8
        i32.const 0
        i32.store offset=220
        local.get $l8
        local.get $l22
        f32.store offset=216
        local.get $l8
        local.get $p3
        i32.load offset=40
        local.get $p3
        i32.load8_u offset=39
        i32.const 20
        i32.mul
        i32.add
        i32.store offset=360
        local.get $l8
        local.get $p3
        i32.load8_u offset=38
        i32.store8 offset=364
        local.get $l8
        local.get $p3
        f32.load offset=52
        local.get $l8
        f32.load offset=800
        f32.mul
        local.tee $l22
        local.get $p3
        f32.load offset=56
        local.get $l8
        f32.load offset=804
        f32.mul
        local.tee $l23
        local.get $l22
        local.get $l23
        f32.le
        select
        local.tee $l22
        local.get $p3
        f32.load offset=60
        local.get $l8
        f32.load offset=808
        f32.mul
        local.tee $l23
        local.get $l22
        local.get $l23
        f32.le
        select
        local.tee $l22
        f32.const 0x1.99999ap-6 (;=0.025;)
        f32.mul
        f32.store offset=232
        local.get $l8
        local.get $l22
        f32.const 0x1.99999ap-5 (;=0.05;)
        f32.mul
        f32.store offset=228
        local.get $l8
        local.get $l22
        f32.const 0x1.99999ap-4 (;=0.1;)
        f32.mul
        f32.store offset=224
        local.get $l8
        i32.const 800
        i32.add
        local.get $l8
        i32.const 528
        i32.add
        local.get $l8
        i32.const 256
        i32.add
        local.get $l8
        i32.const 304
        i32.add
        local.get $l8
        i32.const 208
        i32.add
        local.get $p4
        call $f70494
        local.get $l8
        local.get $p3
        i32.load offset=44
        i32.store offset=356
        local.get $l8
        i64.const 0
        i64.store offset=168
        local.get $l8
        i64.const 0
        i64.store offset=160
        local.get $l8
        i64.const 0
        i64.store offset=152
        local.get $l8
        i64.const 0
        i64.store offset=144
        local.get $l8
        i64.const 0
        i64.store offset=136
        local.get $l8
        i64.const 0
        i64.store offset=128
        local.get $l8
        i32.const 0
        i32.store offset=192
        local.get $l10
        if $I5
          local.get $l8
          local.get $l8
          i64.load offset=608
          i64.store offset=832
          local.get $l8
          local.get $l8
          i64.load offset=616
          i64.store offset=840
          local.get $l8
          local.get $l8
          i64.load offset=792
          i64.store offset=856
          local.get $l8
          local.get $l8
          i64.load offset=784
          i64.store offset=848
          local.get $l8
          i32.const 912
          i32.add
          local.tee $p3
          local.get $l8
          i64.load offset=640
          i64.store
          local.get $l8
          i32.const 904
          i32.add
          local.tee $p7
          local.get $l8
          i64.load offset=632
          i64.store
          local.get $l8
          i32.const 920
          i32.add
          local.tee $p1
          local.get $l8
          i64.load offset=648
          i64.store
          local.get $l8
          i32.const 928
          i32.add
          local.tee $p0
          local.get $l8
          i64.load offset=656
          i64.store
          local.get $l8
          local.get $l8
          i64.load offset=664
          i64.store offset=936
          local.get $l8
          local.get $l8
          i64.load offset=672
          i64.store offset=944
          local.get $l8
          local.get $l8
          i64.load offset=680
          i64.store offset=952
          local.get $l8
          local.get $l8
          i64.load offset=624
          i64.store offset=896
          local.get $l8
          i32.const 900
          i32.add
          local.tee $l10
          f32.load
          local.set $l22
          local.get $l10
          local.get $p3
          f32.load
          f32.store
          local.get $l8
          i32.const 3124324
          i32.store offset=880
          local.get $l8
          local.get $l8
          i32.const 624
          i32.add
          i32.store offset=888
          local.get $l8
          local.get $l8
          i32.const 368
          i32.add
          i32.store offset=884
          local.get $p7
          f32.load
          local.set $l23
          local.get $p1
          f32.load
          local.set $l24
          local.get $p3
          local.get $l22
          f32.store
          local.get $p7
          local.get $p0
          f32.load
          f32.store
          local.get $p1
          local.get $l8
          i32.const 932
          i32.add
          local.tee $p3
          f32.load
          f32.store
          local.get $p3
          local.get $l24
          f32.store
          local.get $p0
          local.get $l23
          f32.store
          local.get $p4
          if $I6
            local.get $l8
            i32.const 3124628
            i32.store offset=872
            local.get $l8
            local.get $l8
            i32.const 208
            i32.add
            i32.store offset=876
            local.get $p5
            i32.const 67
            i32.add
            local.set $l11
            local.get $p5
            i32.const 71
            i32.add
            local.set $l12
            local.get $l8
            i32.const 128
            i32.add
            local.set $l10
            i32.const 0
            local.set $p0
            global.get $g0
            i32.const 320
            i32.sub
            local.tee $p7
            global.set $g0
            local.get $l8
            i32.const 872
            i32.add
            local.tee $l17
            i32.load offset=4
            local.tee $l15
            f32.load offset=20
            local.set $l23
            local.get $l8
            i32.const 880
            i32.add
            local.tee $p2
            i32.load offset=4
            local.tee $l16
            f32.load offset=20
            local.set $l25
            local.get $l8
            f32.load offset=848
            local.set $l41
            local.get $l16
            i32.load8_u offset=32
            local.set $l18
            local.get $l16
            f32.load offset=16
            local.set $l43
            local.get $l15
            i32.load8_u offset=32
            local.set $l19
            local.get $l15
            f32.load offset=16
            local.set $l44
            local.get $p7
            i32.const 0
            i32.store offset=28
            local.get $l23
            local.get $l25
            local.get $l23
            local.get $l25
            f32.lt
            select
            f32.const 0x1.99999ap-4 (;=0.1;)
            f32.mul
            local.set $l45
            block $B7 (result f32)
              local.get $p5
              i32.const 66
              i32.add
              local.tee $l14
              i32.load8_u
              local.tee $l21
              if $I8
                local.get $p2
                i32.load offset=8
                local.set $l9
                i32.const 0
                local.set $p3
                loop $L9
                  local.get $p3
                  i32.const 2
                  i32.shl
                  local.tee $p4
                  local.get $p7
                  i32.const 48
                  i32.add
                  i32.add
                  local.get $p3
                  local.get $l11
                  i32.add
                  i32.load8_u
                  local.tee $l13
                  i32.store
                  local.get $p7
                  i32.const 32
                  i32.add
                  local.get $p4
                  i32.add
                  local.get $p3
                  local.get $l12
                  i32.add
                  i32.load8_u
                  local.tee $p1
                  i32.store
                  local.get $l16
                  i32.load offset=152
                  local.get $l13
                  i32.const 12
                  i32.mul
                  i32.add
                  local.tee $p4
                  f32.load offset=8
                  local.set $l23
                  local.get $p4
                  f32.load
                  local.set $l25
                  local.get $p4
                  f32.load offset=4
                  local.set $l22
                  local.get $l15
                  i32.load offset=152
                  local.get $p1
                  i32.const 12
                  i32.mul
                  i32.add
                  local.tee $p4
                  f32.load
                  local.set $l24
                  local.get $p4
                  f32.load offset=4
                  local.set $l27
                  local.get $p4
                  f32.load offset=8
                  local.set $l26
                  local.get $l9
                  f32.load offset=48
                  local.set $l28
                  local.get $l9
                  f32.load offset=32
                  local.set $l31
                  local.get $l9
                  f32.load
                  local.set $l30
                  local.get $l9
                  f32.load offset=16
                  local.set $l32
                  local.get $l9
                  f32.load offset=52
                  local.set $l29
                  local.get $l9
                  f32.load offset=36
                  local.set $l34
                  local.get $l9
                  f32.load offset=4
                  local.set $l35
                  local.get $l9
                  f32.load offset=20
                  local.set $l36
                  local.get $l9
                  f32.load offset=56
                  local.set $l33
                  local.get $l9
                  f32.load offset=40
                  local.set $l37
                  local.get $l9
                  f32.load offset=8
                  local.set $l38
                  local.get $l9
                  f32.load offset=24
                  local.set $l39
                  local.get $p0
                  local.tee $p1
                  i32.const 4
                  i32.shl
                  local.tee $l13
                  local.get $p7
                  i32.const 128
                  i32.add
                  i32.add
                  local.tee $p4
                  i32.const 0
                  i32.store offset=12
                  local.get $p7
                  i32.const -64
                  i32.sub
                  local.get $l13
                  i32.add
                  local.tee $p0
                  i32.const 0
                  i32.store offset=12
                  local.get $p0
                  local.get $l26
                  f32.store offset=8
                  local.get $p0
                  local.get $l27
                  f32.store offset=4
                  local.get $p0
                  local.get $l24
                  f32.store
                  local.get $p7
                  i32.const 192
                  i32.add
                  local.get $l13
                  i32.add
                  local.tee $p0
                  i32.const 0
                  i32.store offset=12
                  local.get $p4
                  local.get $l33
                  local.get $l25
                  local.get $l38
                  f32.mul
                  local.get $l22
                  local.get $l39
                  f32.mul
                  f32.add
                  local.get $l23
                  local.get $l37
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l33
                  f32.store offset=8
                  local.get $p4
                  local.get $l29
                  local.get $l25
                  local.get $l35
                  f32.mul
                  local.get $l22
                  local.get $l36
                  f32.mul
                  f32.add
                  local.get $l23
                  local.get $l34
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l29
                  f32.store offset=4
                  local.get $p4
                  local.get $l28
                  local.get $l25
                  local.get $l30
                  f32.mul
                  local.get $l22
                  local.get $l32
                  f32.mul
                  f32.add
                  local.get $l23
                  local.get $l31
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l23
                  f32.store
                  local.get $p0
                  local.get $l33
                  local.get $l26
                  f32.sub
                  local.tee $l25
                  f32.store offset=8
                  local.get $p0
                  local.get $l29
                  local.get $l27
                  f32.sub
                  local.tee $l22
                  f32.store offset=4
                  local.get $p0
                  local.get $l23
                  local.get $l24
                  f32.sub
                  local.tee $l23
                  f32.store
                  local.get $p7
                  local.get $p1
                  i32.const 1
                  i32.add
                  local.tee $p0
                  i32.store offset=28
                  local.get $p3
                  i32.const 1
                  i32.add
                  local.tee $p3
                  local.get $l21
                  i32.ne
                  br_if $L9
                end
                block $B10
                  block $B11
                    block $B12
                      block $B13
                        block $B14
                          block $B15
                            block $B16
                              local.get $p1
                              br_table $B16 $B15 $B14 $B13 $B12
                            end
                            local.get $p7
                            i32.const 0
                            i32.store offset=316
                            br $B11
                          end
                          local.get $p7
                          f32.load offset=208
                          local.get $p7
                          f32.load offset=192
                          local.tee $l24
                          f32.sub
                          local.tee $l23
                          local.get $l23
                          f32.mul
                          local.get $p7
                          f32.load offset=212
                          local.get $p7
                          f32.load offset=196
                          local.tee $l27
                          f32.sub
                          local.tee $l25
                          local.get $l25
                          f32.mul
                          f32.add
                          local.get $p7
                          f32.load offset=216
                          local.get $p7
                          f32.load offset=200
                          local.tee $l26
                          f32.sub
                          local.tee $l22
                          local.get $l22
                          f32.mul
                          f32.add
                          local.tee $l28
                          f32.const 0x1p-23 (;=1.19209e-07;)
                          f32.le
                          if $I17
                            local.get $p7
                            i32.const 1
                            i32.store offset=28
                            local.get $p7
                            local.get $p7
                            i64.load offset=192
                            i64.store offset=304
                            local.get $p7
                            local.get $p7
                            i64.load offset=200
                            i64.store offset=312
                            br $B10
                          end
                          local.get $p7
                          i32.const 0
                          i32.store offset=316
                          local.get $p7
                          local.get $l26
                          local.get $l22
                          local.get $l25
                          local.get $l27
                          f32.neg
                          f32.mul
                          local.get $l24
                          local.get $l23
                          f32.mul
                          f32.sub
                          local.get $l26
                          local.get $l22
                          f32.mul
                          f32.sub
                          local.get $l28
                          f32.div
                          f32.const 0x1p+0 (;=1;)
                          f32.min
                          local.tee $l28
                          f32.const 0x0p+0 (;=0;)
                          local.get $l28
                          f32.const 0x0p+0 (;=0;)
                          f32.gt
                          select
                          local.tee $l28
                          f32.mul
                          f32.add
                          f32.store offset=312
                          local.get $p7
                          local.get $l27
                          local.get $l25
                          local.get $l28
                          f32.mul
                          f32.add
                          f32.store offset=308
                          local.get $p7
                          local.get $l24
                          local.get $l23
                          local.get $l28
                          f32.mul
                          f32.add
                          f32.store offset=304
                          br $B10
                        end
                        local.get $p7
                        i32.const 304
                        i32.add
                        local.get $p7
                        i32.const 192
                        i32.add
                        local.get $p7
                        i32.const 128
                        i32.add
                        local.get $p7
                        i32.const -64
                        i32.sub
                        local.get $p7
                        i32.const 48
                        i32.add
                        local.get $p7
                        i32.const 32
                        i32.add
                        local.get $p7
                        i32.const 28
                        i32.add
                        call $f70518
                        br $B10
                      end
                      local.get $p7
                      i32.const 304
                      i32.add
                      local.get $p7
                      i32.const 192
                      i32.add
                      local.get $p7
                      i32.const 128
                      i32.add
                      local.get $p7
                      i32.const -64
                      i32.sub
                      local.get $p7
                      i32.const 48
                      i32.add
                      local.get $p7
                      i32.const 32
                      i32.add
                      local.get $p7
                      i32.const 28
                      i32.add
                      call $f69905
                      br $B10
                    end
                    local.get $p7
                    i32.const 0
                    i32.store offset=316
                  end
                  local.get $p7
                  local.get $l25
                  f32.store offset=312
                  local.get $p7
                  local.get $l22
                  f32.store offset=308
                  local.get $p7
                  local.get $l23
                  f32.store offset=304
                end
                local.get $p7
                local.get $p7
                i64.load offset=304
                i64.store offset=256
                local.get $p7
                local.get $p7
                i64.load offset=312
                i64.store offset=264
                local.get $p7
                f32.load offset=256
                local.tee $l23
                local.get $l23
                f32.mul
                local.get $p7
                f32.load offset=260
                local.tee $l30
                local.get $l30
                f32.mul
                f32.add
                local.get $p7
                f32.load offset=264
                local.tee $l25
                local.get $l25
                f32.mul
                f32.add
                f32.sqrt
                local.tee $l28
                local.get $l45
                f32.gt
                local.set $l9
                local.get $l25
                f32.const 0x1p+0 (;=1;)
                local.get $l28
                f32.div
                local.tee $l22
                f32.mul
                local.set $l32
                local.get $l30
                local.get $l22
                f32.mul
                local.set $l29
                local.get $l23
                local.get $l22
                f32.mul
                local.set $l34
                local.get $p7
                f32.load offset=268
                br $B7
              end
              local.get $l9
              f32.load offset=8
              local.set $l23
              local.get $l9
              f32.load
              local.set $l22
              local.get $l9
              f32.load offset=4
              local.set $l24
              local.get $p7
              i32.const 0
              i32.store offset=268
              local.get $p7
              local.get $l23
              f32.const 0x0p+0 (;=0;)
              local.get $l22
              local.get $l22
              f32.mul
              local.get $l24
              local.get $l24
              f32.mul
              f32.add
              local.get $l23
              local.get $l23
              f32.mul
              f32.add
              f32.const 0x0p+0 (;=0;)
              f32.gt
              local.tee $l9
              select
              local.tee $l25
              f32.store offset=264
              local.get $p7
              local.get $l24
              f32.const 0x0p+0 (;=0;)
              local.get $l9
              select
              local.tee $l30
              f32.store offset=260
              local.get $p7
              local.get $l22
              f32.const 0x1p+0 (;=1;)
              local.get $l9
              select
              local.tee $l23
              f32.store offset=256
              local.get $l25
              f32.const 0x1p+0 (;=1;)
              local.get $l25
              local.get $l25
              f32.mul
              local.get $l23
              local.get $l23
              f32.mul
              local.get $l30
              local.get $l30
              f32.mul
              f32.add
              f32.add
              f32.sqrt
              f32.div
              local.tee $l22
              f32.mul
              local.set $l32
              local.get $l30
              local.get $l22
              f32.mul
              local.set $l29
              local.get $l23
              local.get $l22
              f32.mul
              local.set $l34
              f32.const 0x1.fffffep+127 (;=3.40282e+38;)
              local.set $l28
              i32.const 1
              local.set $l9
              f32.const 0x0p+0 (;=0;)
            end
            local.set $l42
            block $B18
              block $B19
                local.get $l9
                i32.eqz
                br_if $B19
                local.get $l41
                local.get $l43
                f32.const 0x0p+0 (;=0;)
                local.get $l18
                select
                local.get $l44
                f32.const 0x0p+0 (;=0;)
                local.get $l19
                select
                f32.add
                f32.add
                local.set $l46
                local.get $p7
                i32.const 280
                i32.add
                local.set $p0
                loop $L20
                  local.get $p0
                  local.get $p7
                  i32.load offset=296
                  i32.store
                  local.get $p7
                  local.get $p7
                  i64.load offset=288 align=4
                  i64.store offset=272
                  local.get $p2
                  i32.load offset=8
                  local.set $l9
                  local.get $p2
                  i32.load offset=4
                  local.set $p3
                  local.get $p7
                  i32.load offset=28
                  local.set $p4
                  local.get $p2
                  f32.load offset=48
                  local.set $l24
                  local.get $p2
                  f32.load offset=32
                  local.set $l27
                  local.get $p2
                  f32.load offset=16
                  local.set $l26
                  local.get $p2
                  f32.load offset=52
                  local.set $l31
                  local.get $p2
                  f32.load offset=36
                  local.set $l35
                  local.get $p2
                  f32.load offset=20
                  local.set $l36
                  local.get $p2
                  f32.load offset=56
                  local.set $l33
                  local.get $p2
                  f32.load offset=40
                  local.set $l37
                  local.get $p2
                  f32.load offset=24
                  local.set $l38
                  local.get $p7
                  i32.const 0
                  i32.store offset=316
                  local.get $p7
                  local.get $l37
                  local.get $l30
                  f32.neg
                  local.tee $l22
                  f32.mul
                  local.get $l23
                  local.get $l38
                  f32.mul
                  f32.sub
                  local.get $l25
                  local.get $l33
                  f32.mul
                  f32.sub
                  f32.store offset=312
                  local.get $p7
                  local.get $l35
                  local.get $l22
                  f32.mul
                  local.get $l23
                  local.get $l36
                  f32.mul
                  f32.sub
                  local.get $l25
                  local.get $l31
                  f32.mul
                  f32.sub
                  f32.store offset=308
                  local.get $p7
                  local.get $l27
                  local.get $l22
                  f32.mul
                  local.get $l23
                  local.get $l26
                  f32.mul
                  f32.sub
                  local.get $l25
                  local.get $l24
                  f32.mul
                  f32.sub
                  f32.store offset=304
                  local.get $p7
                  i32.const 48
                  i32.add
                  local.get $p4
                  i32.const 2
                  i32.shl
                  i32.add
                  local.get $p3
                  local.get $p7
                  i32.const 304
                  i32.add
                  call $f70525
                  local.tee $p4
                  i32.store
                  local.get $l9
                  f32.load offset=52
                  local.set $l31
                  local.get $l9
                  f32.load offset=20
                  local.set $l35
                  local.get $l9
                  f32.load offset=36
                  local.set $l36
                  local.get $l9
                  f32.load offset=56
                  local.set $l33
                  local.get $p3
                  i32.load offset=152
                  local.get $p4
                  i32.const 12
                  i32.mul
                  i32.add
                  local.tee $p3
                  f32.load
                  local.set $l22
                  local.get $l9
                  f32.load offset=24
                  local.set $l37
                  local.get $p3
                  f32.load offset=4
                  local.set $l24
                  local.get $l9
                  f32.load offset=40
                  local.set $l38
                  local.get $p3
                  f32.load offset=8
                  local.set $l27
                  local.get $l9
                  f32.load offset=48
                  local.set $l26
                  local.get $l9
                  f32.load offset=32
                  local.set $l39
                  local.get $l9
                  f32.load
                  local.set $l41
                  local.get $l9
                  f32.load offset=16
                  local.set $l43
                  local.get $l9
                  f32.load offset=4
                  local.set $l44
                  local.get $l9
                  f32.load offset=8
                  local.set $l47
                  local.get $p7
                  i32.const 32
                  i32.add
                  local.get $p7
                  i32.load offset=28
                  i32.const 2
                  i32.shl
                  i32.add
                  local.get $l17
                  i32.load offset=4
                  local.tee $l9
                  local.get $p7
                  i32.const 256
                  i32.add
                  call $f70525
                  local.tee $p3
                  i32.store
                  local.get $l46
                  local.get $l34
                  local.get $l26
                  local.get $l22
                  local.get $l41
                  f32.mul
                  local.get $l24
                  local.get $l43
                  f32.mul
                  f32.add
                  local.get $l27
                  local.get $l39
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l39
                  local.get $l9
                  i32.load offset=152
                  local.get $p3
                  i32.const 12
                  i32.mul
                  i32.add
                  local.tee $l9
                  f32.load
                  local.tee $l41
                  f32.sub
                  local.tee $l26
                  f32.mul
                  local.get $l29
                  local.get $l31
                  local.get $l22
                  local.get $l44
                  f32.mul
                  local.get $l24
                  local.get $l35
                  f32.mul
                  f32.add
                  local.get $l27
                  local.get $l36
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l35
                  local.get $l9
                  f32.load offset=4
                  local.tee $l36
                  f32.sub
                  local.tee $l31
                  f32.mul
                  f32.add
                  local.get $l32
                  local.get $l33
                  local.get $l22
                  local.get $l47
                  f32.mul
                  local.get $l24
                  local.get $l37
                  f32.mul
                  f32.add
                  local.get $l27
                  local.get $l38
                  f32.mul
                  f32.add
                  f32.add
                  local.tee $l27
                  local.get $l9
                  f32.load offset=8
                  local.tee $l33
                  f32.sub
                  local.tee $l22
                  f32.mul
                  f32.add
                  local.tee $l24
                  f32.lt
                  if $I21
                    i32.const 0
                    local.set $p2
                    local.get $l11
                    i32.eqz
                    br_if $B18
                    local.get $l14
                    local.get $p7
                    i32.load offset=28
                    local.tee $p3
                    i32.store8
                    local.get $p3
                    i32.eqz
                    br_if $B18
                    local.get $p3
                    i32.const 1
                    i32.and
                    local.set $l13
                    i32.const 0
                    local.set $l9
                    local.get $p3
                    i32.const 1
                    i32.ne
                    if $I22
                      local.get $p3
                      i32.const -2
                      i32.and
                      local.set $p4
                      loop $L23
                        local.get $l9
                        local.get $l11
                        i32.add
                        local.get $l9
                        i32.const 2
                        i32.shl
                        local.tee $p3
                        local.get $p7
                        i32.const 48
                        i32.add
                        i32.add
                        i32.load
                        i32.store8
                        local.get $l9
                        local.get $l12
                        i32.add
                        local.get $p7
                        i32.const 32
                        i32.add
                        local.get $p3
                        i32.add
                        i32.load
                        i32.store8
                        local.get $l11
                        local.get $l9
                        i32.const 1
                        i32.or
                        local.tee $p3
                        i32.add
                        local.get $p3
                        i32.const 2
                        i32.shl
                        local.tee $p0
                        local.get $p7
                        i32.const 48
                        i32.add
                        i32.add
                        i32.load
                        i32.store8
                        local.get $p3
                        local.get $l12
                        i32.add
                        local.get $p7
                        i32.const 32
                        i32.add
                        local.get $p0
                        i32.add
                        i32.load
                        i32.store8
                        local.get $l9
                        i32.const 2
                        i32.add
                        local.set $l9
                        local.get $p4
                        i32.const 2
                        i32.sub
                        local.tee $p4
                        br_if $L23
                      end
                    end
                    local.get $l13
                    i32.eqz
                    br_if $B18
                    local.get $l9
                    local.get $l11
                    i32.add
                    local.get $l9
                    i32.const 2
                    i32.shl
                    local.tee $p3
                    local.get $p7
                    i32.const 48
                    i32.add
                    i32.add
                    i32.load
                    i32.store8
                    local.get $l9
                    local.get $l12
                    i32.add
                    local.get $p7
                    i32.const 32
                    i32.add
                    local.get $p3
                    i32.add
                    i32.load
                    i32.store8
                    br $B18
                  end
                  local.get $p7
                  i32.load offset=28
                  local.set $l9
                  local.get $l28
                  f32.const 0x1.ffe282p-1 (;=0.999775;)
                  f32.mul
                  local.get $l24
                  f32.lt
                  if $I24
                    block $B25
                      local.get $l11
                      i32.eqz
                      br_if $B25
                      local.get $l14
                      local.get $l9
                      i32.store8
                      local.get $l9
                      i32.eqz
                      br_if $B25
                      local.get $l9
                      i32.const 1
                      i32.and
                      local.set $l13
                      i32.const 0
                      local.set $p3
                      local.get $l9
                      i32.const 1
                      i32.ne
                      if $I26
                        local.get $l9
                        i32.const -2
                        i32.and
                        local.set $p0
                        loop $L27
                          local.get $p3
                          local.get $l11
                          i32.add
                          local.get $p3
                          i32.const 2
                          i32.shl
                          local.tee $p4
                          local.get $p7
                          i32.const 48
                          i32.add
                          i32.add
                          i32.load
                          i32.store8
                          local.get $p3
                          local.get $l12
                          i32.add
                          local.get $p7
                          i32.const 32
                          i32.add
                          local.get $p4
                          i32.add
                          i32.load
                          i32.store8
                          local.get $l11
                          local.get $p3
                          i32.const 1
                          i32.or
                          local.tee $p4
                          i32.add
                          local.get $p4
                          i32.const 2
                          i32.shl
                          local.tee $p2
                          local.get $p7
                          i32.const 48
                          i32.add
                          i32.add
                          i32.load
                          i32.store8
                          local.get $p4
                          local.get $l12
                          i32.add
                          local.get $p7
                          i32.const 32
                          i32.add
                          local.get $p2
                          i32.add
                          i32.load
                          i32.store8
                          local.get $p3
                          i32.const 2
                          i32.add
                          local.set $p3
                          local.get $p0
                          i32.const 2
                          i32.sub
                          local.tee $p0
                          br_if $L27
                        end
                      end
                      local.get $l13
                      i32.eqz
                      br_if $B25
                      local.get $p3
                      local.get $l11
                      i32.add
                      local.get $p3
                      i32.const 2
                      i32.shl
                      local.tee $p4
                      local.get $p7
                      i32.const 48
                      i32.add
                      i32.add
                      i32.load
                      i32.store8
                      local.get $p3
                      local.get $l12
                      i32.add
                      local.get $p7
                      i32.const 32
                      i32.add
                      local.get $p4
                      i32.add
                      i32.load
                      i32.store8
                    end
                    local.get $l10
                    local.get $l34
                    f32.store offset=32
                    local.get $l10
                    i32.const 0
                    i32.store offset=44
                    local.get $l10
                    local.get $l32
                    f32.store offset=40
                    local.get $l10
                    local.get $l29
                    f32.store offset=36
                    local.get $p7
                    i32.const 192
                    i32.add
                    local.get $p7
                    i32.const 128
                    i32.add
                    local.get $p7
                    i32.const -64
                    i32.sub
                    local.get $p7
                    i32.const 256
                    i32.add
                    local.get $p7
                    i32.const 304
                    i32.add
                    local.get $p7
                    local.get $l9
                    call $f70517
                    local.get $l10
                    local.get $p7
                    i64.load offset=304
                    i64.store
                    local.get $l10
                    local.get $p7
                    i64.load offset=312
                    i64.store offset=8
                    local.get $l10
                    local.get $p7
                    i64.load
                    i64.store offset=16
                    local.get $l10
                    local.get $p7
                    i64.load offset=8
                    i64.store offset=24
                    local.get $l10
                    local.get $p7
                    i64.load offset=288 align=4
                    i64.store offset=68 align=4
                    local.get $l10
                    local.get $p7
                    i32.load offset=296
                    i32.store offset=76
                    local.get $l10
                    local.get $l28
                    f32.store offset=64
                    i32.const 2
                    local.set $p2
                    br $B18
                  end
                  local.get $l9
                  i32.const 4
                  i32.shl
                  local.tee $p4
                  local.get $p7
                  i32.const 128
                  i32.add
                  i32.add
                  local.tee $p3
                  i32.const 0
                  i32.store offset=12
                  local.get $p3
                  local.get $l27
                  f32.store offset=8
                  local.get $p3
                  local.get $l35
                  f32.store offset=4
                  local.get $p3
                  local.get $l39
                  f32.store
                  local.get $p7
                  i32.const -64
                  i32.sub
                  local.get $p4
                  i32.add
                  local.tee $p3
                  i32.const 0
                  i32.store offset=12
                  local.get $p3
                  local.get $l33
                  f32.store offset=8
                  local.get $p3
                  local.get $l36
                  f32.store offset=4
                  local.get $p3
                  local.get $l41
                  f32.store
                  local.get $p7
                  i32.const 192
                  i32.add
                  local.get $p4
                  i32.add
                  local.tee $p3
                  i32.const 0
                  i32.store offset=12
                  local.get $p3
                  local.get $l22
                  f32.store offset=8
                  local.get $p3
                  local.get $l31
                  f32.store offset=4
                  local.get $p3
                  local.get $l26
                  f32.store
                  local.get $p7
                  local.get $l9
                  i32.const 1
                  i32.add
                  i32.store offset=28
                  block $B28
                    block $B29
                      block $B30
                        block $B31
                          block $B32
                            local.get $l9
                            i32.const 1
                            i32.sub
                            br_table $B32 $B31 $B30 $B29
                          end
                          local.get $p7
                          f32.load offset=208
                          local.get $p7
                          f32.load offset=192
                          local.tee $l26
                          f32.sub
                          local.tee $l22
                          local.get $l22
                          f32.mul
                          local.get $p7
                          f32.load offset=212
                          local.get $p7
                          f32.load offset=196
                          local.tee $l31
                          f32.sub
                          local.tee $l24
                          local.get $l24
                          f32.mul
                          f32.add
                          local.get $p7
                          f32.load offset=216
                          local.get $p7
                          f32.load offset=200
                          local.tee $l32
                          f32.sub
                          local.tee $l27
                          local.get $l27
                          f32.mul
                          f32.add
                          local.tee $l29
                          f32.const 0x1p-23 (;=1.19209e-07;)
                          f32.le
                          if $I33
                            local.get $p7
                            i32.const 1
                            i32.store offset=28
                            local.get $p7
                            local.get $p7
                            i64.load offset=192
                            i64.store offset=304
                            local.get $p7
                            local.get $p7
                            i64.load offset=200
                            i64.store offset=312
                            br $B28
                          end
                          local.get $p7
                          i32.const 0
                          i32.store offset=316
                          local.get $p7
                          local.get $l32
                          local.get $l27
                          local.get $l24
                          local.get $l31
                          f32.neg
                          f32.mul
                          local.get $l26
                          local.get $l22
                          f32.mul
                          f32.sub
                          local.get $l32
                          local.get $l27
                          f32.mul
                          f32.sub
                          local.get $l29
                          f32.div
                          f32.const 0x1p+0 (;=1;)
                          f32.min
                          local.tee $l29
                          f32.const 0x0p+0 (;=0;)
                          local.get $l29
                          f32.const 0x0p+0 (;=0;)
                          f32.gt
                          select
                          local.tee $l29
                          f32.mul
                          f32.add
                          f32.store offset=312
                          local.get $p7
                          local.get $l31
                          local.get $l24
                          local.get $l29
                          f32.mul
                          f32.add
                          f32.store offset=308
                          local.get $p7
                          local.get $l26
                          local.get $l22
                          local.get $l29
                          f32.mul
                          f32.add
                          f32.store offset=304
                          br $B28
                        end
                        local.get $p7
                        i32.const 304
                        i32.add
                        local.get $p7
                        i32.const 192
                        i32.add
                        local.get $p7
                        i32.const 128
                        i32.add
                        local.get $p7
                        i32.const -64
                        i32.sub
                        local.get $p7
                        i32.const 48
                        i32.add
                        local.get $p7
                        i32.const 32
                        i32.add
                        local.get $p7
                        i32.const 28
                        i32.add
                        call $f70518
                        br $B28
                      end
                      local.get $p7
                      i32.const 304
                      i32.add
                      local.get $p7
                      i32.const 192
                      i32.add
                      local.get $p7
                      i32.const 128
                      i32.add
                      local.get $p7
                      i32.const -64
                      i32.sub
                      local.get $p7
                      i32.const 48
                      i32.add
                      local.get $p7
                      i32.const 32
                      i32.add
                      local.get $p7
                      i32.const 28
                      i32.add
                      call $f69905
                      br $B28
                    end
                    local.get $p7
                    i32.const 0
                    i32.store offset=316
                    local.get $p7
                    local.get $l22
                    f32.store offset=312
                    local.get $p7
                    local.get $l31
                    f32.store offset=308
                    local.get $p7
                    local.get $l26
                    f32.store offset=304
                  end
                  local.get $p7
                  local.get $p7
                  i64.load offset=304
                  i64.store offset=256
                  local.get $p7
                  local.get $p7
                  i64.load offset=312
                  i64.store offset=264
                  local.get $p7
                  f32.load offset=264
                  local.tee $l24
                  f32.const 0x1p+0 (;=1;)
                  local.get $p7
                  f32.load offset=256
                  local.tee $l27
                  local.get $l27
                  f32.mul
                  local.get $p7
                  f32.load offset=260
                  local.tee $l26
                  local.get $l26
                  f32.mul
                  f32.add
                  local.get $l24
                  local.get $l24
                  f32.mul
                  f32.add
                  f32.sqrt
                  local.tee $l22
                  f32.div
                  local.tee $l31
                  f32.mul
                  local.set $l32
                  local.get $l26
                  local.get $l31
                  f32.mul
                  local.set $l29
                  local.get $l27
                  local.get $l31
                  f32.mul
                  local.set $l34
                  block $B34
                    local.get $l22
                    local.get $l45
                    f32.gt
                    i32.eqz
                    br_if $B34
                    local.get $l22
                    local.get $l28
                    f32.lt
                    i32.eqz
                    br_if $B34
                    local.get $p7
                    f32.load offset=268
                    local.set $l42
                    local.get $l24
                    local.set $l25
                    local.get $l26
                    local.set $l30
                    local.get $l27
                    local.set $l23
                    local.get $l22
                    local.set $l28
                    br $L20
                  end
                end
                local.get $l22
                local.get $l28
                f32.lt
                br_if $B19
                local.get $p7
                i32.load offset=28
                local.set $p2
                block $B35
                  local.get $l11
                  i32.eqz
                  br_if $B35
                  local.get $l14
                  local.get $p2
                  i32.const 1
                  i32.sub
                  local.tee $p3
                  i32.store8
                  local.get $p3
                  i32.eqz
                  br_if $B35
                  local.get $p3
                  i32.const 1
                  i32.and
                  local.set $l13
                  i32.const 0
                  local.set $l9
                  local.get $p2
                  i32.const 2
                  i32.ne
                  if $I36
                    local.get $p3
                    i32.const -2
                    i32.and
                    local.set $p4
                    loop $L37
                      local.get $l9
                      local.get $l11
                      i32.add
                      local.get $l9
                      i32.const 2
                      i32.shl
                      local.tee $p3
                      local.get $p7
                      i32.const 48
                      i32.add
                      i32.add
                      i32.load
                      i32.store8
                      local.get $l9
                      local.get $l12
                      i32.add
                      local.get $p7
                      i32.const 32
                      i32.add
                      local.get $p3
                      i32.add
                      i32.load
                      i32.store8
                      local.get $l11
                      local.get $l9
                      i32.const 1
                      i32.or
                      local.tee $p3
                      i32.add
                      local.get $p3
                      i32.const 2
                      i32.shl
                      local.tee $p0
                      local.get $p7
                      i32.const 48
                      i32.add
                      i32.add
                      i32.load
                      i32.store8
                      local.get $p3
                      local.get $l12
                      i32.add
                      local.get $p7
                      i32.const 32
                      i32.add
                      local.get $p0
                      i32.add
                      i32.load
                      i32.store8
                      local.get $l9
                      i32.const 2
                      i32.add
                      local.set $l9
                      local.get $p4
                      i32.const 2
                      i32.sub
                      local.tee $p4
                      br_if $L37
                    end
                  end
                  local.get $l13
                  i32.eqz
                  br_if $B35
                  local.get $l9
                  local.get $l11
                  i32.add
                  local.get $l9
                  i32.const 2
                  i32.shl
                  local.tee $p3
                  local.get $p7
                  i32.const 48
                  i32.add
                  i32.add
                  i32.load
                  i32.store8
                  local.get $l9
                  local.get $l12
                  i32.add
                  local.get $p7
                  i32.const 32
                  i32.add
                  local.get $p3
                  i32.add
                  i32.load
                  i32.store8
                end
                local.get $p7
                local.get $p7
                i32.const 280
                i32.add
                local.tee $l9
                i32.load
                i32.store offset=296
                local.get $p7
                local.get $p7
                i64.load offset=272
                i64.store offset=288
                local.get $p7
                local.get $l42
                f32.store offset=268
                local.get $p7
                local.get $l23
                f32.store offset=256
                local.get $p7
                local.get $l30
                f32.store offset=260
                local.get $p7
                local.get $l25
                f32.store offset=264
                local.get $p7
                i32.const 192
                i32.add
                local.get $p7
                i32.const 128
                i32.add
                local.get $p7
                i32.const -64
                i32.sub
                local.get $p7
                i32.const 256
                i32.add
                local.get $p7
                i32.const 304
                i32.add
                local.get $p7
                local.get $p2
                call $f70517
                local.get $l10
                i32.const 0
                i32.store offset=60
                local.get $l10
                local.get $l32
                f32.store offset=56
                local.get $l10
                local.get $l29
                f32.store offset=52
                local.get $l10
                local.get $l34
                f32.store offset=48
                local.get $l10
                i32.const 0
                i32.store offset=44
                local.get $l10
                local.get $l25
                f32.const 0x1p+0 (;=1;)
                local.get $l28
                f32.div
                local.tee $l22
                f32.mul
                f32.store offset=40
                local.get $l10
                local.get $l30
                local.get $l22
                f32.mul
                f32.store offset=36
                local.get $l10
                local.get $l23
                local.get $l22
                f32.mul
                f32.store offset=32
                local.get $l10
                local.get $p7
                i64.load offset=304
                i64.store
                local.get $l10
                local.get $p7
                i64.load offset=312
                i64.store offset=8
                local.get $l10
                local.get $p7
                i64.load
                i64.store offset=16
                local.get $l10
                local.get $p7
                i64.load offset=8
                i64.store offset=24
                local.get $l10
                local.get $l28
                f32.store offset=64
                local.get $l10
                local.get $p7
                i64.load offset=272
                i64.store offset=68 align=4
                local.get $l10
                local.get $l9
                i32.load
                i32.store offset=76
                i32.const 4
                local.set $p2
                br $B18
              end
              i32.const 5
              local.set $p2
              local.get $l11
              i32.eqz
              br_if $B18
              local.get $l14
              local.get $p7
              i32.load offset=28
              local.tee $p3
              i32.store8
              local.get $p3
              i32.eqz
              br_if $B18
              local.get $p3
              i32.const 1
              i32.and
              local.set $l13
              i32.const 0
              local.set $l9
              local.get $p3
              i32.const 1
              i32.ne
              if $I38
                local.get $p3
                i32.const -2
                i32.and
                local.set $p4
                loop $L39
                  local.get $l9
                  local.get $l11
                  i32.add
                  local.get $l9
                  i32.const 2
                  i32.shl
                  local.tee $p3
                  local.get $p7
                  i32.const 48
                  i32.add
                  i32.add
                  i32.load
                  i32.store8
                  local.get $l9
                  local.get $l12
                  i32.add
                  local.get $p7
                  i32.const 32
                  i32.add
                  local.get $p3
                  i32.add
                  i32.load
                  i32.store8
                  local.get $l11
                  local.get $l9
                  i32.const 1
                  i32.or
                  local.tee $p3
                  i32.add
                  local.get $p3
                  i32.const 2
                  i32.shl
                  local.tee $p0
                  local.get $p7
                  i32.const 48
                  i32.add
                  i32.add
                  i32.load
                  i32.store8
                  local.get $p3
                  local.get $l12
                  i32.add
                  local.get $p7
                  i32.const 32
                  i32.add
                  local.get $p0
                  i32.add
                  i32.load
                  i32.store8
                  local.get $l9
                  i32.const 2
                  i32.add
                  local.set $l9
                  local.get $p4
                  i32.const 2
                  i32.sub
                  local.tee $p4
                  br_if $L39
                end
              end
              local.get $l13
              i32.eqz
              br_if $B18
              local.get $l9
              local.get $l11
              i32.add
              local.get $l9
              i32.const 2
              i32.shl
              local.tee $p3
              local.get $p7
              i32.const 48
              i32.add
              i32.add
              i32.load
              i32.store8
              local.get $l9
              local.get $l12
              i32.add
              local.get $p7
              i32.const 32
              i32.add
              local.get $p3
              i32.add
              i32.load
              i32.store8
            end
            local.get $p7
            i32.const 320
            i32.add
            global.set $g0
            local.get $l8
            local.get $l8
            i64.load offset=840
            i64.store offset=24
            local.get $l8
            local.get $l8
            i64.load offset=832
            i64.store offset=16
            local.get $l8
            local.get $l8
            i64.load offset=848
            i64.store
            local.get $l8
            local.get $l8
            i64.load offset=856
            i64.store offset=8
            local.get $l8
            i32.const 880
            i32.add
            local.get $l8
            i32.const 872
            i32.add
            local.get $l8
            i32.const 752
            i32.add
            local.get $l8
            i32.const 720
            i32.add
            local.get $l8
            i32.const 624
            i32.add
            local.get $p2
            local.get $l8
            i32.const 128
            i32.add
            local.get $p5
            local.get $p6
            local.get $l20
            local.get $l8
            i32.const 16
            i32.add
            local.get $l8
            i32.const 1
            i32.const 1
            local.get $l40
            call $f70073
            br $B0
          end
          local.get $l8
          i32.const 3132572
          i32.store offset=872
          local.get $l8
          local.get $l8
          i32.const 208
          i32.add
          i32.store offset=876
          local.get $p5
          i32.const 67
          i32.add
          local.set $l12
          local.get $p5
          i32.const 71
          i32.add
          local.set $l13
          local.get $l8
          i32.const 128
          i32.add
          local.set $l10
          i32.const 0
          local.set $p0
          global.get $g0
          i32.const 320
          i32.sub
          local.tee $p7
          global.set $g0
          local.get $l8
          i32.const 872
          i32.add
          local.tee $l21
          i32.load offset=4
          local.tee $p3
          f32.load offset=20
          local.set $l23
          local.get $l8
          i32.const 880
          i32.add
          local.tee $l14
          i32.load offset=4
          local.tee $l15
          f32.load offset=20
          local.set $l26
          local.get $l8
          f32.load offset=848
          local.set $l48
          local.get $l15
          i32.load8_u offset=32
          local.set $l17
          local.get $l15
          f32.load offset=16
          local.set $l49
          local.get $p3
          i32.load8_u offset=32
          local.set $l18
          local.get $p3
          f32.load offset=16
          local.set $l50
          local.get $p7
          i32.const 0
          i32.store offset=28
          local.get $l23
          local.get $l26
          local.get $l23
          local.get $l26
          f32.lt
          select
          f32.const 0x1.99999ap-4 (;=0.1;)
          f32.mul
          local.set $l54
          block $B40 (result f32)
            local.get $p5
            i32.const 66
            i32.add
            local.tee $l16
            i32.load8_u
            local.tee $l19
            if $I41
              local.get $l14
              i32.load offset=8
              local.set $l9
              i32.const 0
              local.set $p4
              loop $L42
                local.get $p4
                i32.const 2
                i32.shl
                local.tee $p2
                local.get $p7
                i32.const 48
                i32.add
                i32.add
                local.get $p4
                local.get $l12
                i32.add
                i32.load8_u
                local.tee $l11
                i32.store
                local.get $p7
                i32.const 32
                i32.add
                local.get $p2
                i32.add
                local.get $p4
                local.get $l13
                i32.add
                i32.load8_u
                local.tee $p1
                i32.store
                local.get $l15
                i32.load offset=152
                local.get $l11
                i32.const 12
                i32.mul
                i32.add
                local.tee $p2
                f32.load offset=8
                local.set $l23
                local.get $p2
                f32.load
                local.set $l26
                local.get $p2
                f32.load offset=4
                local.set $l22
                local.get $p3
                i32.load offset=152
                local.get $p1
                i32.const 12
                i32.mul
                i32.add
                local.tee $p2
                f32.load offset=8
                local.set $l24
                local.get $p2
                f32.load
                local.set $l27
                local.get $p2
                f32.load offset=4
                local.set $l25
                local.get $l9
                f32.load offset=48
                local.set $l28
                local.get $l9
                f32.load offset=32
                local.set $l29
                local.get $l9
                f32.load
                local.set $l32
                local.get $l9
                f32.load offset=16
                local.set $l30
                local.get $l9
                f32.load offset=52
                local.set $l31
                local.get $l9
                f32.load offset=36
                local.set $l33
                local.get $l9
                f32.load offset=4
                local.set $l34
                local.get $l9
                f32.load offset=20
                local.set $l35
                local.get $l9
                f32.load offset=56
                local.set $l36
                local.get $l9
                f32.load offset=40
                local.set $l37
                local.get $l9
                f32.load offset=8
                local.set $l38
                local.get $l9
                f32.load offset=24
                local.set $l43
                local.get $p3
                f32.load offset=80
                local.set $l44
                local.get $p3
                f32.load offset=48
                local.set $l46
                local.get $p3
                f32.load offset=64
                local.set $l41
                local.get $p3
                f32.load offset=84
                local.set $l39
                local.get $p3
                f32.load offset=52
                local.set $l47
                local.get $p3
                f32.load offset=68
                local.set $l45
                local.get $p3
                f32.load offset=88
                local.set $l42
                local.get $p3
                f32.load offset=56
                local.set $l51
                local.get $p3
                f32.load offset=72
                local.set $l52
                local.get $p0
                local.tee $p1
                i32.const 4
                i32.shl
                local.tee $l11
                local.get $p7
                i32.const 128
                i32.add
                i32.add
                local.tee $p2
                i32.const 0
                i32.store offset=12
                local.get $p7
                i32.const -64
                i32.sub
                local.get $l11
                i32.add
                local.tee $p0
                i32.const 0
                i32.store offset=12
                local.get $p7
                i32.const 192
                i32.add
                local.get $l11
                i32.add
                local.tee $l11
                i32.const 0
                i32.store offset=12
                local.get $p0
                local.get $l27
                local.get $l51
                f32.mul
                local.get $l25
                local.get $l52
                f32.mul
                f32.add
                local.get $l24
                local.get $l42
                f32.mul
                f32.add
                local.tee $l42
                f32.store offset=8
                local.get $p0
                local.get $l27
                local.get $l47
                f32.mul
                local.get $l25
                local.get $l45
                f32.mul
                f32.add
                local.get $l24
                local.get $l39
                f32.mul
                f32.add
                local.tee $l39
                f32.store offset=4
                local.get $p0
                local.get $l27
                local.get $l46
                f32.mul
                local.get $l25
                local.get $l41
                f32.mul
                f32.add
                local.get $l24
                local.get $l44
                f32.mul
                f32.add
                local.tee $l24
                f32.store
                local.get $p2
                local.get $l36
                local.get $l26
                local.get $l38
                f32.mul
                local.get $l22
                local.get $l43
                f32.mul
                f32.add
                local.get $l23
                local.get $l37
                f32.mul
                f32.add
                f32.add
                local.tee $l27
                f32.store offset=8
                local.get $p2
                local.get $l31
                local.get $l26
                local.get $l34
                f32.mul
                local.get $l22
                local.get $l35
                f32.mul
                f32.add
                local.get $l23
                local.get $l33
                f32.mul
                f32.add
                f32.add
                local.tee $l25
                f32.store offset=4
                local.get $p2
                local.get $l28
                local.get $l26
                local.get $l32
                f32.mul
                local.get $l22
                local.get $l30
                f32.mul
                f32.add
                local.get $l23
                local.get $l29
                f32.mul
                f32.add
                f32.add
                local.tee $l23
                f32.store
                local.get $l11
                local.get $l27
                local.get $l42
                f32.sub
                local.tee $l26
                f32.store offset=8
                local.get $l11
                local.get $l25
                local.get $l39
                f32.sub
                local.tee $l22
                f32.store offset=4
                local.get $l11
                local.get $l23
                local.get $l24
                f32.sub
                local.tee $l23
                f32.store
                local.get $p7
                local.get $p1
                i32.const 1
                i32.add
                local.tee $p0
                i32.store offset=28
                local.get $p4
                i32.const 1
                i32.add
                local.tee $p4
                local.get $l19
                i32.ne
                br_if $L42
              end
              block $B43
                block $B44
                  block $B45
                    block $B46
                      block $B47
                        block $B48
                          block $B49
                            local.get $p1
                            br_table $B49 $B48 $B47 $B46 $B45
                          end
                          local.get $p7
                          i32.const 0
                          i32.store offset=316
                          br $B44
                        end
                        local.get $p7
                        f32.load offset=208
                        local.get $p7
                        f32.load offset=192
                        local.tee $l24
                        f32.sub
                        local.tee $l23
                        local.get $l23
                        f32.mul
                        local.get $p7
                        f32.load offset=212
                        local.get $p7
                        f32.load offset=196
                        local.tee $l27
                        f32.sub
                        local.tee $l26
                        local.get $l26
                        f32.mul
                        f32.add
                        local.get $p7
                        f32.load offset=216
                        local.get $p7
                        f32.load offset=200
                        local.tee $l25
                        f32.sub
                        local.tee $l22
                        local.get $l22
                        f32.mul
                        f32.add
                        local.tee $l28
                        f32.const 0x1p-23 (;=1.19209e-07;)
                        f32.le
                        if $I50
                          local.get $p7
                          i32.const 1
                          i32.store offset=28
                          local.get $p7
                          local.get $p7
                          i64.load offset=192
                          i64.store offset=304
                          local.get $p7
                          local.get $p7
                          i64.load offset=200
                          i64.store offset=312
                          br $B43
                        end
                        local.get $p7
                        i32.const 0
                        i32.store offset=316
                        local.get $p7
                        local.get $l25
                        local.get $l22
                        local.get $l26
                        local.get $l27
                        f32.neg
                        f32.mul
                        local.get $l24
                        local.get $l23
                        f32.mul
                        f32.sub
                        local.get $l25
                        local.get $l22
                        f32.mul
                        f32.sub
                        local.get $l28
                        f32.div
                        f32.const 0x1p+0 (;=1;)
                        f32.min
                        local.tee $l28
                        f32.const 0x0p+0 (;=0;)
                        local.get $l28
                        f32.const 0x0p+0 (;=0;)
                        f32.gt
                        select
                        local.tee $l28
                        f32.mul
                        f32.add
                        f32.store offset=312
                        local.get $p7
                        local.get $l27
                        local.get $l26
                        local.get $l28
                        f32.mul
                        f32.add
                        f32.store offset=308
                        local.get $p7
                        local.get $l24
                        local.get $l23
                        local.get $l28
                        f32.mul
                        f32.add
                        f32.store offset=304
                        br $B43
                      end
                      local.get $p7
                      i32.const 304
                      i32.add
                      local.get $p7
                      i32.const 192
                      i32.add
                      local.get $p7
                      i32.const 128
                      i32.add
                      local.get $p7
                      i32.const -64
                      i32.sub
                      local.get $p7
                      i32.const 48
                      i32.add
                      local.get $p7
                      i32.const 32
                      i32.add
                      local.get $p7
                      i32.const 28
                      i32.add
                      call $f70518
                      br $B43
                    end
                    local.get $p7
                    i32.const 304
                    i32.add
                    local.get $p7
                    i32.const 192
                    i32.add
                    local.get $p7
                    i32.const 128
                    i32.add
                    local.get $p7
                    i32.const -64
                    i32.sub
                    local.get $p7
                    i32.const 48
                    i32.add
                    local.get $p7
                    i32.const 32
                    i32.add
                    local.get $p7
                    i32.const 28
                    i32.add
                    call $f69905
                    br $B43
                  end
                  local.get $p7
                  i32.const 0
                  i32.store offset=316
                end
                local.get $p7
                local.get $l26
                f32.store offset=312
                local.get $p7
                local.get $l22
                f32.store offset=308
                local.get $p7
                local.get $l23
                f32.store offset=304
              end
              local.get $p7
              local.get $p7
              i64.load offset=304
              i64.store offset=256
              local.get $p7
              local.get $p7
              i64.load offset=312
              i64.store offset=264
              local.get $p7
              f32.load offset=256
              local.tee $l23
              local.get $l23
              f32.mul
              local.get $p7
              f32.load offset=260
              local.tee $l30
              local.get $l30
              f32.mul
              f32.add
              local.get $p7
              f32.load offset=264
              local.tee $l26
              local.get $l26
              f32.mul
              f32.add
              f32.sqrt
              local.tee $l28
              local.get $l54
              f32.gt
              local.set $l9
              local.get $l26
              f32.const 0x1p+0 (;=1;)
              local.get $l28
              f32.div
              local.tee $l22
              f32.mul
              local.set $l34
              local.get $l30
              local.get $l22
              f32.mul
              local.set $l35
              local.get $l23
              local.get $l22
              f32.mul
              local.set $l36
              local.get $p7
              f32.load offset=268
              br $B40
            end
            local.get $l9
            f32.load offset=8
            local.set $l23
            local.get $l9
            f32.load
            local.set $l22
            local.get $l9
            f32.load offset=4
            local.set $l24
            local.get $p7
            i32.const 0
            i32.store offset=268
            local.get $p7
            local.get $l23
            f32.const 0x0p+0 (;=0;)
            local.get $l22
            local.get $l22
            f32.mul
            local.get $l24
            local.get $l24
            f32.mul
            f32.add
            local.get $l23
            local.get $l23
            f32.mul
            f32.add
            f32.const 0x0p+0 (;=0;)
            f32.gt
            local.tee $l9
            select
            local.tee $l26
            f32.store offset=264
            local.get $p7
            local.get $l24
            f32.const 0x0p+0 (;=0;)
            local.get $l9
            select
            local.tee $l30
            f32.store offset=260
            local.get $p7
            local.get $l22
            f32.const 0x1p+0 (;=1;)
            local.get $l9
            select
            local.tee $l23
            f32.store offset=256
            local.get $l26
            f32.const 0x1p+0 (;=1;)
            local.get $l26
            local.get $l26
            f32.mul
            local.get $l23
            local.get $l23
            f32.mul
            local.get $l30
            local.get $l30
            f32.mul
            f32.add
            f32.add
            f32.sqrt
            f32.div
            local.tee $l22
            f32.mul
            local.set $l34
            local.get $l30
            local.get $l22
            f32.mul
            local.set $l35
            local.get $l23
            local.get $l22
            f32.mul
            local.set $l36
            f32.const 0x1.fffffep+127 (;=3.40282e+38;)
            local.set $l28
            i32.const 1
            local.set $l9
            f32.const 0x0p+0 (;=0;)
          end
          local.set $l53
          block $B51
            block $B52
              local.get $l9
              i32.eqz
              br_if $B52
              local.get $l48
              local.get $l49
              f32.const 0x0p+0 (;=0;)
              local.get $l17
              select
              local.get $l50
              f32.const 0x0p+0 (;=0;)
              local.get $l18
              select
              f32.add
              f32.add
              local.set $l55
              local.get $p7
              i32.const 280
              i32.add
              local.set $l18
              loop $L53
                local.get $l18
                local.get $p7
                i32.load offset=296
                i32.store
                local.get $p7
                local.get $p7
                i64.load offset=288 align=4
                i64.store offset=272
                local.get $l14
                i32.load offset=8
                local.set $l9
                local.get $l14
                i32.load offset=4
                local.set $p3
                local.get $p7
                i32.load offset=28
                local.set $p4
                local.get $l14
                f32.load offset=48
                local.set $l24
                local.get $l14
                f32.load offset=32
                local.set $l27
                local.get $l14
                f32.load offset=16
                local.set $l25
                local.get $l14
                f32.load offset=52
                local.set $l29
                local.get $l14
                f32.load offset=36
                local.set $l32
                local.get $l14
                f32.load offset=20
                local.set $l31
                local.get $l14
                f32.load offset=56
                local.set $l33
                local.get $l14
                f32.load offset=40
                local.set $l37
                local.get $l14
                f32.load offset=24
                local.set $l38
                local.get $p7
                i32.const 0
                i32.store offset=316
                local.get $p7
                local.get $l37
                local.get $l30
                f32.neg
                local.tee $l22
                f32.mul
                local.get $l23
                local.get $l38
                f32.mul
                f32.sub
                local.get $l26
                local.get $l33
                f32.mul
                f32.sub
                f32.store offset=312
                local.get $p7
                local.get $l32
                local.get $l22
                f32.mul
                local.get $l23
                local.get $l31
                f32.mul
                f32.sub
                local.get $l26
                local.get $l29
                f32.mul
                f32.sub
                f32.store offset=308
                local.get $p7
                local.get $l27
                local.get $l22
                f32.mul
                local.get $l23
                local.get $l25
                f32.mul
                f32.sub
                local.get $l26
                local.get $l24
                f32.mul
                f32.sub
                f32.store offset=304
                local.get $p7
                i32.const 48
                i32.add
                local.get $p4
                i32.const 2
                i32.shl
                i32.add
                local.get $p3
                local.get $p7
                i32.const 304
                i32.add
                call $f70525
                local.tee $p4
                i32.store
                local.get $l9
                f32.load offset=52
                local.set $l33
                local.get $l9
                f32.load offset=20
                local.set $l37
                local.get $l9
                f32.load offset=36
                local.set $l38
                local.get $l9
                f32.load offset=56
                local.set $l43
                local.get $p3
                i32.load offset=152
                local.get $p4
                i32.const 12
                i32.mul
                i32.add
                local.tee $p3
                f32.load
                local.set $l22
                local.get $l9
                f32.load offset=24
                local.set $l44
                local.get $p3
                f32.load offset=4
                local.set $l24
                local.get $l9
                f32.load offset=40
                local.set $l46
                local.get $p3
                f32.load offset=8
                local.set $l27
                local.get $l9
                f32.load offset=48
                local.set $l31
                local.get $l9
                f32.load offset=32
                local.set $l41
                local.get $l9
                f32.load
                local.set $l39
                local.get $l9
                f32.load offset=16
                local.set $l47
                local.get $l9
                f32.load offset=4
                local.set $l45
                local.get $l9
                f32.load offset=8
                local.set $l42
                local.get $p7
                i32.load offset=28
                local.set $p3
                local.get $l21
                i32.load offset=4
                local.tee $l9
                i32.const 56
                i32.add
                local.tee $p4
                f32.load
                local.set $l51
                local.get $l9
                i32.const 52
                i32.add
                local.tee $p2
                f32.load
                local.set $l52
                local.get $l9
                i32.const 72
                i32.add
                local.tee $p0
                f32.load
                local.set $l48
                local.get $l9
                i32.const -64
                i32.sub
                local.tee $l11
                f32.load
                local.set $l49
                local.get $l9
                i32.const 68
                i32.add
                local.tee $p1
                f32.load
                local.set $l50
                local.get $l9
                i32.const 88
                i32.add
                local.tee $l15
                f32.load
                local.set $l56
                local.get $l9
                i32.const 80
                i32.add
                local.tee $l19
                f32.load
                local.set $l29
                local.get $l9
                i32.const 84
                i32.add
                local.tee $l17
                f32.load
                local.set $l32
                local.get $l9
                f32.load offset=48
                local.set $l57
                local.get $p7
                i32.const 0
                i32.store offset=316
                local.get $p7
                local.get $l29
                local.get $p7
                f32.load offset=256
                local.tee $l25
                f32.mul
                local.get $l32
                local.get $p7
                f32.load offset=260
                local.tee $l29
                f32.mul
                f32.add
                local.get $l56
                local.get $p7
                f32.load offset=264
                local.tee $l32
                f32.mul
                f32.add
                f32.store offset=312
                local.get $p7
                local.get $l25
                local.get $l49
                f32.mul
                local.get $l29
                local.get $l50
                f32.mul
                f32.add
                local.get $l32
                local.get $l48
                f32.mul
                f32.add
                f32.store offset=308
                local.get $p7
                local.get $l25
                local.get $l57
                f32.mul
                local.get $l29
                local.get $l52
                f32.mul
                f32.add
                local.get $l32
                local.get $l51
                f32.mul
                f32.add
                f32.store offset=304
                local.get $p7
                i32.const 32
                i32.add
                local.get $p3
                i32.const 2
                i32.shl
                i32.add
                local.get $l9
                local.get $p7
                i32.const 304
                i32.add
                call $f70525
                local.tee $p3
                i32.store
                local.get $l55
                local.get $l36
                local.get $l31
                local.get $l22
                local.get $l39
                f32.mul
                local.get $l24
                local.get $l47
                f32.mul
                f32.add
                local.get $l27
                local.get $l41
                f32.mul
                f32.add
                f32.add
                local.tee $l41
                local.get $l9
                i32.load offset=152
                local.get $p3
                i32.const 12
                i32.mul
                i32.add
                local.tee $p3
                f32.load
                local.tee $l25
                local.get $l9
                f32.load offset=48
                f32.mul
                local.get $p3
                f32.load offset=4
                local.tee $l29
                local.get $l11
                f32.load
                f32.mul
                f32.add
                local.get $p3
                f32.load offset=8
                local.tee $l32
                local.get $l19
                f32.load
                f32.mul
                f32.add
                local.tee $l39
                f32.sub
                local.tee $l31
                f32.mul
                local.get $l35
                local.get $l33
                local.get $l22
                local.get $l45
                f32.mul
                local.get $l24
                local.get $l37
                f32.mul
                f32.add
                local.get $l27
                local.get $l38
                f32.mul
                f32.add
                f32.add
                local.tee $l37
                local.get $l25
                local.get $p2
                f32.load
                f32.mul
                local.get $l29
                local.get $p1
                f32.load
                f32.mul
                f32.add
                local.get $l32
                local.get $l17
                f32.load
                f32.mul
                f32.add
                local.tee $l38
                f32.sub
                local.tee $l33
                f32.mul
                f32.add
                local.get $l34
                local.get $l43
                local.get $l22
                local.get $l42
                f32.mul
                local.get $l24
                local.get $l44
                f32.mul
                f32.add
                local.get $l27
                local.get $l46
                f32.mul
                f32.add
                f32.add
                local.tee $l27
                local.get $l25
                local.get $p4
                f32.load
                f32.mul
                local.get $l29
                local.get $p0
                f32.load
                f32.mul
                f32.add
                local.get $l32
                local.get $l15
                f32.load
                f32.mul
                f32.add
                local.tee $l25
                f32.sub
                local.tee $l22
                f32.mul
                f32.add
                local.tee $l24
                f32.lt
                if $I54
                  i32.const 0
                  local.set $p0
                  local.get $l12
                  i32.eqz
                  br_if $B51
                  local.get $l16
                  local.get $p7
                  i32.load offset=28
                  local.tee $p3
                  i32.store8
                  local.get $p3
                  i32.eqz
                  br_if $B51
                  local.get $p3
                  i32.const 1
                  i32.and
                  local.set $l11
                  i32.const 0
                  local.set $l9
                  local.get $p3
                  i32.const 1
                  i32.ne
                  if $I55
                    local.get $p3
                    i32.const -2
                    i32.and
                    local.set $p4
                    loop $L56
                      local.get $l9
                      local.get $l12
                      i32.add
                      local.get $l9
                      i32.const 2
                      i32.shl
                      local.tee $p3
                      local.get $p7
                      i32.const 48
                      i32.add
                      i32.add
                      i32.load
                      i32.store8
                      local.get $l9
                      local.get $l13
                      i32.add
                      local.get $p7
                      i32.const 32
                      i32.add
                      local.get $p3
                      i32.add
                      i32.load
                      i32.store8
                      local.get $l12
                      local.get $l9
                      i32.const 1
                      i32.or
                      local.tee $p3
                      i32.add
                      local.get $p3
                      i32.const 2
                      i32.shl
                      local.tee $p2
                      local.get $p7
                      i32.const 48
                      i32.add
                      i32.add
                      i32.load
                      i32.store8
                      local.get $p3
                      local.get $l13
                      i32.add
                      local.get $p7
                      i32.const 32
                      i32.add
                      local.get $p2
                      i32.add
                      i32.load
                      i32.store8
                      local.get $l9
                      i32.const 2
                      i32.add
                      local.set $l9
                      local.get $p4
                      i32.const 2
                      i32.sub
                      local.tee $p4
                      br_if $L56
                    end
                  end
                  local.get $l11
                  i32.eqz
                  br_if $B51
                  local.get $l9
                  local.get $l12
                  i32.add
                  local.get $l9
                  i32.const 2
                  i32.shl
                  local.tee $p3
                  local.get $p7
                  i32.const 48
                  i32.add
                  i32.add
                  i32.load
                  i32.store8
                  local.get $l9
                  local.get $l13
                  i32.add
                  local.get $p7
                  i32.const 32
                  i32.add
                  local.get $p3
                  i32.add
                  i32.load
                  i32.store8
                  br $B51
                end
                local.get $p7
                i32.load offset=28
                local.set $l9
                local.get $l28
                f32.const 0x1.ffe282p-1 (;=0.999775;)
                f32.mul
                local.get $l24
                f32.lt
                if $I57
                  block $B58
                    local.get $l12
                    i32.eqz
                    br_if $B58
                    local.get $l16
                    local.get $l9
                    i32.store8
                    local.get $l9
                    i32.eqz
                    br_if $B58
                    local.get $l9
                    i32.const 1
                    i32.and
                    local.set $l11
                    i32.const 0
                    local.set $p3
                    local.get $l9
                    i32.const 1
                    i32.ne
                    if $I59
                      local.get $l9
                      i32.const -2
                      i32.and
                      local.set $p2
                      loop $L60
                        local.get $p3
                        local.get $l12
                        i32.add
                        local.get $p3
                        i32.const 2
                        i32.shl
                        local.tee $p4
                        local.get $p7
                        i32.const 48
                        i32.add
                        i32.add
                        i32.load
                        i32.store8
                        local.get $p3
                        local.get $l13
                        i32.add
                        local.get $p7
                        i32.const 32
                        i32.add
                        local.get $p4
                        i32.add
                        i32.load
                        i32.store8
                        local.get $l12
                        local.get $p3
                        i32.const 1
                        i32.or
                        local.tee $p4
                        i32.add
                        local.get $p4
                        i32.const 2
                        i32.shl
                        local.tee $p0
                        local.get $p7
                        i32.const 48
                        i32.add
                        i32.add
                        i32.load
                        i32.store8
                        local.get $p4
                        local.get $l13
                        i32.add
                        local.get $p7
                        i32.const 32
                        i32.add
                        local.get $p0
                        i32.add
                        i32.load
                        i32.store8
                        local.get $p3
                        i32.const 2
                        i32.add
                        local.set $p3
                        local.get $p2
                        i32.const 2
                        i32.sub
                        local.tee $p2
                        br_if $L60
                      end
                    end
                    local.get $l11
                    i32.eqz
                    br_if $B58
                    local.get $p3
                    local.get $l12
                    i32.add
                    local.get $p3
                    i32.const 2
                    i32.shl
                    local.tee $p4
                    local.get $p7
                    i32.const 48
                    i32.add
                    i32.add
                    i32.load
                    i32.store8
                    local.get $p3
                    local.get $l13
                    i32.add
                    local.get $p7
                    i32.const 32
                    i32.add
                    local.get $p4
                    i32.add
                    i32.load
                    i32.store8
                  end
                  local.get $l10
                  local.get $l36
                  f32.store offset=32
                  local.get $l10
                  i32.const 0
                  i32.store offset=44
                  local.get $l10
                  local.get $l34
                  f32.store offset=40
                  local.get $l10
                  local.get $l35
                  f32.store offset=36
                  local.get $p7
                  i32.const 192
                  i32.add
                  local.get $p7
                  i32.const 128
                  i32.add
                  local.get $p7
                  i32.const -64
                  i32.sub
                  local.get $p7
                  i32.const 256
                  i32.add
                  local.get $p7
                  i32.const 304
                  i32.add
                  local.get $p7
                  local.get $l9
                  call $f70517
                  local.get $l10
                  local.get $p7
                  i64.load offset=304
                  i64.store
                  local.get $l10
                  local.get $p7
                  i64.load offset=312
                  i64.store offset=8
                  local.get $l10
                  local.get $p7
                  i64.load
                  i64.store offset=16
                  local.get $l10
                  local.get $p7
                  i64.load offset=8
                  i64.store offset=24
                  local.get $l10
                  local.get $p7
                  i64.load offset=288 align=4
                  i64.store offset=68 align=4
                  local.get $l10
                  local.get $p7
                  i32.load offset=296
                  i32.store offset=76
                  local.get $l10
                  local.get $l28
                  f32.store offset=64
                  i32.const 2
                  local.set $p0
                  br $B51
                end
                local.get $l9
                i32.const 4
                i32.shl
                local.tee $p4
                local.get $p7
                i32.const 128
                i32.add
                i32.add
                local.tee $p3
                i32.const 0
                i32.store offset=12
                local.get $p3
                local.get $l27
                f32.store offset=8
                local.get $p3
                local.get $l37
                f32.store offset=4
                local.get $p3
                local.get $l41
                f32.store
                local.get $p7
                i32.const -64
                i32.sub
                local.get $p4
                i32.add
                local.tee $p3
                i32.const 0
                i32.store offset=12
                local.get $p3
                local.get $l25
                f32.store offset=8
                local.get $p3
                local.get $l38
                f32.store offset=4
                local.get $p3
                local.get $l39
                f32.store
                local.get $p7
                i32.const 192
                i32.add
                local.get $p4
                i32.add
                local.tee $p3
                i32.const 0
                i32.store offset=12
                local.get $p3
                local.get $l22
                f32.store offset=8
                local.get $p3
                local.get $l33
                f32.store offset=4
                local.get $p3
                local.get $l31
                f32.store
                local.get $p7
                local.get $l9
                i32.const 1
                i32.add
                i32.store offset=28
                block $B61
                  block $B62
                    block $B63
                      block $B64
                        block $B65
                          local.get $l9
                          i32.const 1
                          i32.sub
                          br_table $B65 $B64 $B63 $B62
                        end
                        local.get $p7
                        f32.load offset=208
                        local.get $p7
                        f32.load offset=192
                        local.tee $l25
                        f32.sub
                        local.tee $l22
                        local.get $l22
                        f32.mul
                        local.get $p7
                        f32.load offset=212
                        local.get $p7
                        f32.load offset=196
                        local.tee $l29
                        f32.sub
                        local.tee $l24
                        local.get $l24
                        f32.mul
                        f32.add
                        local.get $p7
                        f32.load offset=216
                        local.get $p7
                        f32.load offset=200
                        local.tee $l32
                        f32.sub
                        local.tee $l27
                        local.get $l27
                        f32.mul
                        f32.add
                        local.tee $l31
                        f32.const 0x1p-23 (;=1.19209e-07;)
                        f32.le
                        if $I66
                          local.get $p7
                          i32.const 1
                          i32.store offset=28
                          local.get $p7
                          local.get $p7
                          i64.load offset=192
                          i64.store offset=304
                          local.get $p7
                          local.get $p7
                          i64.load offset=200
                          i64.store offset=312
                          br $B61
                        end
                        local.get $p7
                        i32.const 0
                        i32.store offset=316
                        local.get $p7
                        local.get $l32
                        local.get $l27
                        local.get $l24
                        local.get $l29
                        f32.neg
                        f32.mul
                        local.get $l25
                        local.get $l22
                        f32.mul
                        f32.sub
                        local.get $l32
                        local.get $l27
                        f32.mul
                        f32.sub
                        local.get $l31
                        f32.div
                        f32.const 0x1p+0 (;=1;)
                        f32.min
                        local.tee $l31
                        f32.const 0x0p+0 (;=0;)
                        local.get $l31
                        f32.const 0x0p+0 (;=0;)
                        f32.gt
                        select
                        local.tee $l31
                        f32.mul
                        f32.add
                        f32.store offset=312
                        local.get $p7
                        local.get $l29
                        local.get $l24
                        local.get $l31
                        f32.mul
                        f32.add
                        f32.store offset=308
                        local.get $p7
                        local.get $l25
                        local.get $l22
                        local.get $l31
                        f32.mul
                        f32.add
                        f32.store offset=304
                        br $B61
                      end
                      local.get $p7
                      i32.const 304
                      i32.add
                      local.get $p7
                      i32.const 192
                      i32.add
                      local.get $p7
                      i32.const 128
                      i32.add
                      local.get $p7
                      i32.const -64
                      i32.sub
                      local.get $p7
                      i32.const 48
                      i32.add
                      local.get $p7
                      i32.const 32
                      i32.add
                      local.get $p7
                      i32.const 28
                      i32.add
                      call $f70518
                      br $B61
                    end
                    local.get $p7
                    i32.const 304
                    i32.add
                    local.get $p7
                    i32.const 192
                    i32.add
                    local.get $p7
                    i32.const 128
                    i32.add
                    local.get $p7
                    i32.const -64
                    i32.sub
                    local.get $p7
                    i32.const 48
                    i32.add
                    local.get $p7
                    i32.const 32
                    i32.add
                    local.get $p7
                    i32.const 28
                    i32.add
                    call $f69905
                    br $B61
                  end
                  local.get $p7
                  i32.const 0
                  i32.store offset=316
                  local.get $p7
                  local.get $l22
                  f32.store offset=312
                  local.get $p7
                  local.get $l33
                  f32.store offset=308
                  local.get $p7
                  local.get $l31
                  f32.store offset=304
                end
                local.get $p7
                local.get $p7
                i64.load offset=304
                i64.store offset=256
                local.get $p7
                local.get $p7
                i64.load offset=312
                i64.store offset=264
                local.get $p7
                f32.load offset=264
                local.tee $l24
                f32.const 0x1p+0 (;=1;)
                local.get $p7
                f32.load offset=256
                local.tee $l27
                local.get $l27
                f32.mul
                local.get $p7
                f32.load offset=260
                local.tee $l25
                local.get $l25
                f32.mul
                f32.add
                local.get $l24
                local.get $l24
                f32.mul
                f32.add
                f32.sqrt
                local.tee $l22
                f32.div
                local.tee $l29
                f32.mul
                local.set $l34
                local.get $l25
                local.get $l29
                f32.mul
                local.set $l35
                local.get $l27
                local.get $l29
                f32.mul
                local.set $l36
                block $B67
                  local.get $l22
                  local.get $l54
                  f32.gt
                  i32.eqz
                  br_if $B67
                  local.get $l22
                  local.get $l28
                  f32.lt
                  i32.eqz
                  br_if $B67
                  local.get $p7
                  f32.load offset=268
                  local.set $l53
                  local.get $l24
                  local.set $l26
                  local.get $l25
                  local.set $l30
                  local.get $l27
                  local.set $l23
                  local.get $l22
                  local.set $l28
                  br $L53
                end
              end
              local.get $l22
              local.get $l28
              f32.lt
              br_if $B52
              local.get $p7
              i32.load offset=28
              local.set $p0
              block $B68
                local.get $l12
                i32.eqz
                br_if $B68
                local.get $l16
                local.get $p0
                i32.const 1
                i32.sub
                local.tee $p3
                i32.store8
                local.get $p3
                i32.eqz
                br_if $B68
                local.get $p3
                i32.const 1
                i32.and
                local.set $l11
                i32.const 0
                local.set $l9
                local.get $p0
                i32.const 2
                i32.ne
                if $I69
                  local.get $p3
                  i32.const -2
                  i32.and
                  local.set $p4
                  loop $L70
                    local.get $l9
                    local.get $l12
                    i32.add
                    local.get $l9
                    i32.const 2
                    i32.shl
                    local.tee $p3
                    local.get $p7
                    i32.const 48
                    i32.add
                    i32.add
                    i32.load
                    i32.store8
                    local.get $l9
                    local.get $l13
                    i32.add
                    local.get $p7
                    i32.const 32
                    i32.add
                    local.get $p3
                    i32.add
                    i32.load
                    i32.store8
                    local.get $l12
                    local.get $l9
                    i32.const 1
                    i32.or
                    local.tee $p3
                    i32.add
                    local.get $p3
                    i32.const 2
                    i32.shl
                    local.tee $p2
                    local.get $p7
                    i32.const 48
                    i32.add
                    i32.add
                    i32.load
                    i32.store8
                    local.get $p3
                    local.get $l13
                    i32.add
                    local.get $p7
                    i32.const 32
                    i32.add
                    local.get $p2
                    i32.add
                    i32.load
                    i32.store8
                    local.get $l9
                    i32.const 2
                    i32.add
                    local.set $l9
                    local.get $p4
                    i32.const 2
                    i32.sub
                    local.tee $p4
                    br_if $L70
                  end
                end
                local.get $l11
                i32.eqz
                br_if $B68
                local.get $l9
                local.get $l12
                i32.add
                local.get $l9
                i32.const 2
                i32.shl
                local.tee $p3
                local.get $p7
                i32.const 48
                i32.add
                i32.add
                i32.load
                i32.store8
                local.get $l9
                local.get $l13
                i32.add
                local.get $p7
                i32.const 32
                i32.add
                local.get $p3
                i32.add
                i32.load
                i32.store8
              end
              local.get $p7
              local.get $p7
              i32.const 280
              i32.add
              local.tee $l9
              i32.load
              i32.store offset=296
              local.get $p7
              local.get $p7
              i64.load offset=272
              i64.store offset=288
              local.get $p7
              local.get $l53
              f32.store offset=268
              local.get $p7
              local.get $l23
              f32.store offset=256
              local.get $p7
              local.get $l30
              f32.store offset=260
              local.get $p7
              local.get $l26
              f32.store offset=264
              local.get $p7
              i32.const 192
              i32.add
              local.get $p7
              i32.const 128
              i32.add
              local.get $p7
              i32.const -64
              i32.sub
              local.get $p7
              i32.const 256
              i32.add
              local.get $p7
              i32.const 304
              i32.add
              local.get $p7
              local.get $p0
              call $f70517
              local.get $l10
              i32.const 0
              i32.store offset=60
              local.get $l10
              local.get $l34
              f32.store offset=56
              local.get $l10
              local.get $l35
              f32.store offset=52
              local.get $l10
              local.get $l36
              f32.store offset=48
              local.get $l10
              i32.const 0
              i32.store offset=44
              local.get $l10
              local.get $l26
              f32.const 0x1p+0 (;=1;)
              local.get $l28
              f32.div
              local.tee $l22
              f32.mul
              f32.store offset=40
              local.get $l10
              local.get $l30
              local.get $l22
              f32.mul
              f32.store offset=36
              local.get $l10
              local.get $l23
              local.get $l22
              f32.mul
              f32.store offset=32
              local.get $l10
              local.get $p7
              i64.load offset=304
              i64.store
              local.get $l10
              local.get $p7
              i64.load offset=312
              i64.store offset=8
              local.get $l10
              local.get $p7
              i64.load
              i64.store offset=16
              local.get $l10
              local.get $p7
              i64.load offset=8
              i64.store offset=24
              local.get $l10
              local.get $l28
              f32.store offset=64
              local.get $l10
              local.get $p7
              i64.load offset=272
              i64.store offset=68 align=4
              local.get $l10
              local.get $l9
              i32.load
              i32.store offset=76
              i32.const 4
              local.set $p0
              br $B51
            end
            i32.const 5
            local.set $p0
            local.get $l12
            i32.eqz
            br_if $B51
            local.get $l16
            local.get $p7
            i32.load offset=28
            local.tee $p3
            i32.store8
            local.get $p3
            i32.eqz
            br_if $B51
            local.get $p3
            i32.const 1
            i32.and
            local.set $l11
            i32.const 0
            local.set $l9
            local.get $p3
            i32.const 1
            i32.ne
            if $I71
              local.get $p3
              i32.const -2
              i32.and
              local.set $p4
              loop $L72
                local.get $l9
                local.get $l12
                i32.add
                local.get $l9
                i32.const 2
                i32.shl
                local.tee $p3
                local.get $p7
                i32.const 48
                i32.add
                i32.add
                i32.load
                i32.store8
                local.get $l9
                local.get $l13
                i32.add
                local.get $p7
                i32.const 32
                i32.add
                local.get $p3
                i32.add
                i32.load
                i32.store8
                local.get $l12
                local.get $l9
                i32.const 1
                i32.or
                local.tee $p3
                i32.add
                local.get $p3
                i32.const 2
                i32.shl
                local.tee $p2
                local.get $p7
                i32.const 48
                i32.add
                i32.add
                i32.load
                i32.store8
                local.get $p3
                local.get $l13
                i32.add
                local.get $p7
                i32.const 32
                i32.add
                local.get $p2
                i32.add
                i32.load
                i32.store8
                local.get $l9
                i32.const 2
                i32.add
                local.set $l9
                local.get $p4
                i32.const 2
                i32.sub
                local.tee $p4
                br_if $L72
              end
            end
            local.get $l11
            i32.eqz
            br_if $B51
            local.get $l9
            local.get $l12
            i32.add
            local.get $l9
            i32.const 2
            i32.shl
            local.tee $p3
            local.get $p7
            i32.const 48
            i32.add
            i32.add
            i32.load
            i32.store8
            local.get $l9
            local.get $l13
            i32.add
            local.get $p7
            i32.const 32
            i32.add
            local.get $p3
            i32.add
            i32.load
            i32.store8
          end
          local.get $p7
          i32.const 320
          i32.add
          global.set $g0
          local.get $l8
          local.get $l8
          i64.load offset=840
          i64.store offset=56
          local.get $l8
          local.get $l8
          i64.load offset=832
          i64.store offset=48
          local.get $l8
          local.get $l8
          i64.load offset=848
          i64.store offset=32
          local.get $l8
          local.get $l8
          i64.load offset=856
          i64.store offset=40
          local.get $l8
          i32.const 880
          i32.add
          local.get $l8
          i32.const 872
          i32.add
          local.get $l8
          i32.const 752
          i32.add
          local.get $l8
          i32.const 720
          i32.add
          local.get $l8
          i32.const 624
          i32.add
          local.get $p0
          local.get $l8
          i32.const 128
          i32.add
          local.get $p5
          local.get $p6
          local.get $l20
          local.get $l8
          i32.const 48
          i32.add
          local.get $l8
          i32.const 32
          i32.add
          i32.const 1
          i32.const 0
          local.get $l40
          call $f70073
          br $B0
        end
        local.get $l8
        local.get $l8
        i64.load offset=608
        i64.store offset=832
        local.get $l8
        local.get $l8
        i64.load offset=616
        i64.store offset=840
        local.get $l8
        local.get $l8
        i64.load offset=792
        i64.store offset=856
        local.get $l8
        local.get $l8
        i64.load offset=784
        i64.store offset=848
        local.get $l8
        i32.const 912
        i32.add
        local.tee $p3
        local.get $l8
        i64.load offset=640
        i64.store
        local.get $l8
        i32.const 904
        i32.add
        local.tee $p7
        local.get $l8
        i64.load offset=632
        i64.store
        local.get $l8
        i32.const 920
        i32.add
        local.tee $p1
        local.get $l8
        i64.load offset=648
        i64.store
        local.get $l8
        i32.const 928
        i32.add
        local.tee $p0
        local.get $l8
        i64.load offset=656
        i64.store
        local.get $l8
        local.get $l8
        i64.load offset=664
        i64.store offset=936
        local.get $l8
        local.get $l8
        i64.load offset=672
        i64.store offset=944
        local.get $l8
        local.get $l8
        i64.load offset=680
        i64.store offset=952
        local.get $l8
        local.get $l8
        i64.load offset=624
        i64.store offset=896
        local.get $l8
        i32.const 900
        i32.add
        local.tee $l10
        f32.load
        local.set $l22
        local.get $l10
        local.get $p3
        f32.load
        f32.store
        local.get $l8
        i32.const 3132644
        i32.store offset=880
        local.get $l8
        local.get $l8
        i32.const 624
        i32.add
        i32.store offset=888
        local.get $l8
        local.get $l8
        i32.const 368
        i32.add
        i32.store offset=884
        local.get $p7
        f32.load
        local.set $l23
        local.get $p1
        f32.load
        local.set $l24
        local.get $p3
        local.get $l22
        f32.store
        local.get $p7
        local.get $p0
        f32.load
        f32.store
        local.get $p1
        local.get $l8
        i32.const 932
        i32.add
        local.tee $p3
        f32.load
        f32.store
        local.get $p3
        local.get $l24
        f32.store
        local.get $p0
        local.get $l23
        f32.store
        local.get $p4
        if $I73
          local.get $l8
          i32.const 3124628
          i32.store offset=872
          local.get $l8
          local.get $l8
          i32.const 208
          i32.add
          i32.store offset=876
          local.get $p5
          i32.const 67
          i32.add
          local.set $l11
          local.get $p5
          i32.const 71
          i32.add
          local.set $l12
          local.get $l8
          i32.const 128
          i32.add
          local.set $p4
          i32.const 0
          local.set $p0
          global.get $g0
          i32.const 320
          i32.sub
          local.tee $p7
          global.set $g0
          local.get $l8
          i32.const 872
          i32.add
          local.tee $l17
          i32.load offset=4
          local.tee $l16
          f32.load offset=20
          local.set $l22
          local.get $l8
          i32.const 880
          i32.add
          local.tee $l14
          i32.load offset=4
          local.tee $p3
          f32.load offset=20
          local.set $l23
          local.get $l8
          f32.load offset=848
          local.set $l48
          local.get $p3
          i32.load8_u offset=32
          local.set $l18
          local.get $p3
          f32.load offset=16
          local.set $l49
          local.get $l16
          i32.load8_u offset=32
          local.set $l19
          local.get $l16
          f32.load offset=16
          local.set $l50
          local.get $p7
          i32.const 0
          i32.store offset=44
          local.get $l22
          local.get $l23
          local.get $l22
          local.get $l23
          f32.lt
          select
          f32.const 0x1.99999ap-4 (;=0.1;)
          f32.mul
          local.set $l53
          block $B74 (result f32)
            local.get $p5
            i32.const 66
            i32.add
            local.tee $l15
            i32.load8_u
            local.tee $l21
            if $I75
              local.get $l14
              i32.load offset=8
              local.set $l9
              i32.const 0
              local.set $l10
              loop $L76
                local.get $l10
                i32.const 2
                i32.shl
                local.tee $p2
                local.get $p7
                i32.const -64
                i32.sub
                i32.add
                local.get $l10
                local.get $l11
                i32.add
                i32.load8_u
                local.tee $l13
                i32.store
                local.get $p7
                i32.const 48
                i32.add
                local.get $p2
                i32.add
                local.get $l10
                local.get $l12
                i32.add
                i32.load8_u
                local.tee $p1
                i32.store
                local.get $p3
                i32.load offset=152
                local.get $l13
                i32.const 12
                i32.mul
                i32.add
                local.tee $p2
                f32.load offset=8
                local.set $l22
                local.get $p2
                f32.load
                local.set $l23
                local.get $p2
                f32.load offset=4
                local.set $l24
                local.get $l16
                i32.load offset=152
                local.get $p1
                i32.const 12
                i32.mul
                i32.add
                local.tee $p2
                f32.load
                local.set $l27
                local.get $p2
                f32.load offset=4
                local.set $l26
                local.get $p2
                f32.load offset=8
                local.set $l29
                local.get $l9
                f32.load offset=48
                local.set $l30
                local.get $l9
                f32.load offset=32
                local.set $l32
                local.get $l9
                f32.load
                local.set $l31
                local.get $l9
                f32.load offset=16
                local.set $l33
                local.get $l9
                f32.load offset=52
                local.set $l34
                local.get $l9
                f32.load offset=36
                local.set $l36
                local.get $l9
                f32.load offset=4
                local.set $l37
                local.get $l9
                f32.load offset=20
                local.set $l38
                local.get $l9
                f32.load offset=56
                local.set $l39
                local.get $l9
                f32.load offset=40
                local.set $l41
                local.get $p3
                f32.load offset=88
                local.set $l35
                local.get $p3
                f32.load offset=56
                local.set $l42
                local.get $p3
                f32.load offset=72
                local.set $l43
                local.get $l9
                f32.load offset=8
                local.set $l28
                local.get $p3
                f32.load offset=80
                local.set $l25
                local.get $p3
                f32.load offset=48
                local.set $l44
                local.get $p3
                f32.load offset=64
                local.set $l46
                local.get $l9
                f32.load offset=24
                local.set $l47
                local.get $p3
                f32.load offset=84
                local.set $l45
                local.get $p3
                f32.load offset=52
                local.set $l51
                local.get $p3
                f32.load offset=68
                local.set $l52
                local.get $p0
                local.tee $p1
                i32.const 4
                i32.shl
                local.tee $l13
                local.get $p7
                i32.const 144
                i32.add
                i32.add
                local.tee $p2
                i32.const 0
                i32.store offset=12
                local.get $p7
                i32.const 80
                i32.add
                local.get $l13
                i32.add
                local.tee $p0
                i32.const 0
                i32.store offset=12
                local.get $p0
                local.get $l29
                f32.store offset=8
                local.get $p0
                local.get $l26
                f32.store offset=4
                local.get $p0
                local.get $l27
                f32.store
                local.get $p7
                i32.const 208
                i32.add
                local.get $l13
                i32.add
                local.tee $p0
                i32.const 0
                i32.store offset=12
                local.get $p2
                local.get $l39
                local.get $l28
                local.get $l23
                local.get $l44
                f32.mul
                local.get $l24
                local.get $l46
                f32.mul
                f32.add
                local.get $l22
                local.get $l25
                f32.mul
                f32.add
                local.tee $l25
                f32.mul
                local.get $l47
                local.get $l23
                local.get $l51
                f32.mul
                local.get $l24
                local.get $l52
                f32.mul
                f32.add
                local.get $l22
                local.get $l45
                f32.mul
                f32.add
                local.tee $l28
                f32.mul
                f32.add
                local.get $l41
                local.get $l23
                local.get $l42
                f32.mul
                local.get $l24
                local.get $l43
                f32.mul
                f32.add
                local.get $l22
                local.get $l35
                f32.mul
                f32.add
                local.tee $l22
                f32.mul
                f32.add
                f32.add
                local.tee $l23
                f32.store offset=8
                local.get $p2
                local.get $l34
                local.get $l25
                local.get $l37
                f32.mul
                local.get $l28
                local.get $l38
                f32.mul
                f32.add
                local.get $l22
                local.get $l36
                f32.mul
                f32.add
                f32.add
                local.tee $l24
                f32.store offset=4
                local.get $p2
                local.get $l30
                local.get $l25
                local.get $l31
                f32.mul
                local.get $l28
                local.get $l33
                f32.mul
                f32.add
                local.get $l22
                local.get $l32
                f32.mul
                f32.add
                f32.add
                local.tee $l22
                f32.store
                local.get $p0
                local.get $l23
                local.get $l29
                f32.sub
                local.tee $l23
                f32.store offset=8
                local.get $p0
                local.get $l24
                local.get $l26
                f32.sub
                local.tee $l24
                f32.store offset=4
                local.get $p0
                local.get $l22
                local.get $l27
                f32.sub
                local.tee $l22
                f32.store
                local.get $p7
                local.get $p1
                i32.const 1
                i32.add
                local.tee $p0
                i32.store offset=44
                local.get $l10
                i32.const 1
                i32.add
                local.tee $l10
                local.get $l21
                i32.ne
                br_if $L76
              end
              block $B77
                block $B78
                  block $B79
                    block $B80
                      block $B81
                        block $B82
                          block $B83
                            local.get $p1
                            br_table $B83 $B82 $B81 $B80 $B79
                          end
                          local.get $p7
                          i32.const 0
                          i32.store offset=28
                          br $B78
                        end
                        local.get $p7
                        f32.load offset=224
                        local.get $p7
                        f32.load offset=208
                        local.tee $l27
                        f32.sub
                        local.tee $l22
                        local.get $l22
                        f32.mul
                        local.get $p7
                        f32.load offset=228
                        local.get $p7
                        f32.load offset=212
                        local.tee $l26
                        f32.sub
                        local.tee $l23
                        local.get $l23
                        f32.mul
                        f32.add
                        local.get $p7
                        f32.load offset=232
                        local.get $p7
                        f32.load offset=216
                        local.tee $l29
                        f32.sub
                        local.tee $l24
                        local.get $l24
                        f32.mul
                        f32.add
                        local.tee $l25
                        f32.const 0x1p-23 (;=1.19209e-07;)
                        f32.le
                        if $I84
                          local.get $p7
                          i32.const 1
                          i32.store offset=44
                          local.get $p7
                          local.get $p7
                          i64.load offset=208
                          i64.store offset=16
                          local.get $p7
                          local.get $p7
                          i64.load offset=216
                          i64.store offset=24
                          br $B77
                        end
                        local.get $p7
                        i32.const 0
                        i32.store offset=28
                        local.get $p7
                        local.get $l29
                        local.get $l24
                        local.get $l23
                        local.get $l26
                        f32.neg
                        f32.mul
                        local.get $l27
                        local.get $l22
                        f32.mul
                        f32.sub
                        local.get $l29
                        local.get $l24
                        f32.mul
                        f32.sub
                        local.get $l25
                        f32.div
                        f32.const 0x1p+0 (;=1;)
                        f32.min
                        local.tee $l25
                        f32.const 0x0p+0 (;=0;)
                        local.get $l25
                        f32.const 0x0p+0 (;=0;)
                        f32.gt
                        select
                        local.tee $l25
                        f32.mul
                        f32.add
                        f32.store offset=24
                        local.get $p7
                        local.get $l26
                        local.get $l23
                        local.get $l25
                        f32.mul
                        f32.add
                        f32.store offset=20
                        local.get $p7
                        local.get $l27
                        local.get $l22
                        local.get $l25
                        f32.mul
                        f32.add
                        f32.store offset=16
                        br $B77
                      end
                      local.get $p7
                      i32.const 16
                      i32.add
                      local.get $p7
                      i32.const 208
                      i32.add
                      local.get $p7
                      i32.const 144
                      i32.add
                      local.get $p7
                      i32.const 80
                      i32.add
                      local.get $p7
                      i32.const -64
                      i32.sub
                      local.get $p7
                      i32.const 48
                      i32.add
                      local.get $p7
                      i32.const 44
                      i32.add
                      call $f70518
                      br $B77
                    end
                    local.get $p7
                    i32.const 16
                    i32.add
                    local.get $p7
                    i32.const 208
                    i32.add
                    local.get $p7
                    i32.const 144
                    i32.add
                    local.get $p7
                    i32.const 80
                    i32.add
                    local.get $p7
                    i32.const -64
                    i32.sub
                    local.get $p7
                    i32.const 48
                    i32.add
                    local.get $p7
                    i32.const 44
                    i32.add
                    call $f69905
                    br $B77
                  end
                  local.get $p7
                  i32.const 0
                  i32.store offset=28
                end
                local.get $p7
                local.get $l23
                f32.store offset=24
                local.get $p7
                local.get $l24
                f32.store offset=20
                local.get $p7
                local.get $l22
                f32.store offset=16
              end
              local.get $p7
              local.get $p7
              i64.load offset=16
              i64.store offset=272
              local.get $p7
              local.get $p7
              i64.load offset=24
              i64.store offset=280
              local.get $p7
              f32.load offset=272
              local.tee $l25
              local.get $l25
              f32.mul
              local.get $p7
              f32.load offset=276
              local.tee $l28
              local.get $l28
              f32.mul
              f32.add
              local.get $p7
              f32.load offset=280
              local.tee $l30
              local.get $l30
              f32.mul
              f32.add
              f32.sqrt
              local.tee $l26
              local.get $l53
              f32.gt
              local.set $l9
              local.get $l30
              f32.const 0x1p+0 (;=1;)
              local.get $l26
              f32.div
              local.tee $l22
              f32.mul
              local.set $l31
              local.get $l28
              local.get $l22
              f32.mul
              local.set $l33
              local.get $l25
              local.get $l22
              f32.mul
              local.set $l34
              local.get $p7
              f32.load offset=284
              br $B74
            end
            local.get $l9
            f32.load offset=8
            local.set $l22
            local.get $l9
            f32.load
            local.set $l23
            local.get $l9
            f32.load offset=4
            local.set $l24
            local.get $p7
            i32.const 0
            i32.store offset=284
            local.get $p7
            local.get $l22
            f32.const 0x0p+0 (;=0;)
            local.get $l23
            local.get $l23
            f32.mul
            local.get $l24
            local.get $l24
            f32.mul
            f32.add
            local.get $l22
            local.get $l22
            f32.mul
            f32.add
            f32.const 0x0p+0 (;=0;)
            f32.gt
            local.tee $l9
            select
            local.tee $l30
            f32.store offset=280
            local.get $p7
            local.get $l24
            f32.const 0x0p+0 (;=0;)
            local.get $l9
            select
            local.tee $l28
            f32.store offset=276
            local.get $p7
            local.get $l23
            f32.const 0x1p+0 (;=1;)
            local.get $l9
            select
            local.tee $l25
            f32.store offset=272
            local.get $l30
            f32.const 0x1p+0 (;=1;)
            local.get $l30
            local.get $l30
            f32.mul
            local.get $l25
            local.get $l25
            f32.mul
            local.get $l28
            local.get $l28
            f32.mul
            f32.add
            f32.add
            f32.sqrt
            f32.div
            local.tee $l22
            f32.mul
            local.set $l31
            local.get $l28
            local.get $l22
            f32.mul
            local.set $l33
            local.get $l25
            local.get $l22
            f32.mul
            local.set $l34
            f32.const 0x1.fffffep+127 (;=3.40282e+38;)
            local.set $l26
            i32.const 1
            local.set $l9
            f32.const 0x0p+0 (;=0;)
          end
          local.set $l35
          block $B85
            block $B86
              local.get $l9
              i32.eqz
              br_if $B86
              local.get $l48
              local.get $l49
              f32.const 0x0p+0 (;=0;)
              local.get $l18
              select
              local.get $l50
              f32.const 0x0p+0 (;=0;)
              local.get $l19
              select
              f32.add
              f32.add
              local.set $l42
              local.get $l14
              i32.const 16
              i32.add
              local.set $p2
              loop $L87
                local.get $p7
                local.get $p7
                i32.load offset=312
                i32.store offset=296
                local.get $p7
                local.get $p7
                i64.load offset=304 align=4
                i64.store offset=288
                local.get $p7
                i32.const 0
                i32.store offset=12
                local.get $p7
                local.get $l30
                f32.neg
                f32.store offset=8
                local.get $p7
                local.get $l28
                f32.neg
                f32.store offset=4
                local.get $p7
                local.get $l25
                f32.neg
                f32.store
                local.get $p7
                i32.const 16
                i32.add
                local.get $l14
                i32.load offset=4
                local.get $p7
                local.get $l14
                i32.load offset=8
                local.get $p2
                local.get $p7
                i32.const -64
                i32.sub
                local.get $p7
                i32.load offset=44
                i32.const 2
                i32.shl
                i32.add
                call $f70538
                local.get $p7
                f32.load offset=28
                local.set $l37
                local.get $p7
                f32.load offset=24
                local.set $l22
                local.get $p7
                f32.load offset=16
                local.set $l23
                local.get $p7
                f32.load offset=20
                local.set $l24
                local.get $p7
                i32.const 48
                i32.add
                local.get $p7
                i32.load offset=44
                i32.const 2
                i32.shl
                i32.add
                local.get $l17
                i32.load offset=4
                local.tee $l9
                local.get $p7
                i32.const 272
                i32.add
                call $f70525
                local.tee $p3
                i32.store
                local.get $l42
                local.get $l34
                local.get $l23
                local.get $l9
                i32.load offset=152
                local.get $p3
                i32.const 12
                i32.mul
                i32.add
                local.tee $l9
                f32.load
                local.tee $l38
                f32.sub
                local.tee $l27
                f32.mul
                local.get $l33
                local.get $l24
                local.get $l9
                f32.load offset=4
                local.tee $l39
                f32.sub
                local.tee $l29
                f32.mul
                f32.add
                local.get $l31
                local.get $l22
                local.get $l9
                f32.load offset=8
                local.tee $l41
                f32.sub
                local.tee $l32
                f32.mul
                f32.add
                local.tee $l36
                f32.lt
                if $I88
                  i32.const 0
                  local.set $p0
                  local.get $l11
                  i32.eqz
                  br_if $B85
                  local.get $l15
                  local.get $p7
                  i32.load offset=44
                  local.tee $p3
                  i32.store8
                  local.get $p3
                  i32.eqz
                  br_if $B85
                  local.get $p3
                  i32.const 1
                  i32.and
                  local.set $l13
                  i32.const 0
                  local.set $l9
                  local.get $p3
                  i32.const 1
                  i32.ne
                  if $I89
                    local.get $p3
                    i32.const -2
                    i32.and
                    local.set $l10
                    loop $L90
                      local.get $l9
                      local.get $l11
                      i32.add
                      local.get $l9
                      i32.const 2
                      i32.shl
                      local.tee $p3
                      local.get $p7
                      i32.const -64
                      i32.sub
                      i32.add
                      i32.load
                      i32.store8
                      local.get $l9
                      local.get $l12
                      i32.add
                      local.get $p7
                      i32.const 48
                      i32.add
                      local.get $p3
                      i32.add
                      i32.load
                      i32.store8
                      local.get $l11
                      local.get $l9
                      i32.const 1
                      i32.or
                      local.tee $p3
                      i32.add
                      local.get $p3
                      i32.const 2
                      i32.shl
                      local.tee $p2
                      local.get $p7
                      i32.const -64
                      i32.sub
                      i32.add
                      i32.load
                      i32.store8
                      local.get $p3
                      local.get $l12
                      i32.add
                      local.get $p7
                      i32.const 48
                      i32.add
                      local.get $p2
                      i32.add
                      i32.load
                      i32.store8
                      local.get $l9
                      i32.const 2
                      i32.add
                      local.set $l9
                      local.get $l10
                      i32.const 2
                      i32.sub
                      local.tee $l10
                      br_if $L90
                    end
                  end
                  local.get $l13
                  i32.eqz
                  br_if $B85
                  local.get $l9
                  local.get $l11
                  i32.add
                  local.get $l9
                  i32.const 2
                  i32.shl
                  local.tee $p3
                  local.get $p7
                  i32.const -64
                  i32.sub
                  i32.add
                  i32.load
                  i32.store8
                  local.get $l9
                  local.get $l12
                  i32.add
                  local.get $p7
                  i32.const 48
                  i32.add
                  local.get $p3
                  i32.add
                  i32.load
                  i32.store8
                  br $B85
                end
                local.get $p7
                i32.load offset=44
                local.set $l9
                local.get $l26
                f32.const 0x1.ffe282p-1 (;=0.999775;)
                f32.mul
                local.get $l36
                f32.lt
                if $I91
                  block $B92
                    local.get $l11
                    i32.eqz
                    br_if $B92
                    local.get $l15
                    local.get $l9
                    i32.store8
                    local.get $l9
                    i32.eqz
                    br_if $B92
                    local.get $l9
                    i32.const 1
                    i32.and
                    local.set $l13
                    i32.const 0
                    local.set $p3
                    local.get $l9
                    i32.const 1
                    i32.ne
                    if $I93
                      local.get $l9
                      i32.const -2
                      i32.and
                      local.set $p2
                      loop $L94
                        local.get $p3
                        local.get $l11
                        i32.add
                        local.get $p3
                        i32.const 2
                        i32.shl
                        local.tee $l10
                        local.get $p7
                        i32.const -64
                        i32.sub
                        i32.add
                        i32.load
                        i32.store8
                        local.get $p3
                        local.get $l12
                        i32.add
                        local.get $p7
                        i32.const 48
                        i32.add
                        local.get $l10
                        i32.add
                        i32.load
                        i32.store8
                        local.get $l11
                        local.get $p3
                        i32.const 1
                        i32.or
                        local.tee $l10
                        i32.add
                        local.get $l10
                        i32.const 2
                        i32.shl
                        local.tee $p0
                        local.get $p7
                        i32.const -64
                        i32.sub
                        i32.add
                        i32.load
                        i32.store8
                        local.get $l10
                        local.get $l12
                        i32.add
                        local.get $p7
                        i32.const 48
                        i32.add
                        local.get $p0
                        i32.add
                        i32.load
                        i32.store8
                        local.get $p3
                        i32.const 2
                        i32.add
                        local.set $p3
                        local.get $p2
                        i32.const 2
                        i32.sub
                        local.tee $p2
                        br_if $L94
                      end
                    end
                    local.get $l13
                    i32.eqz
                    br_if $B92
                    local.get $p3
                    local.get $l11
                    i32.add
                    local.get $p3
                    i32.const 2
                    i32.shl
                    local.tee $l10
                    local.get $p7
                    i32.const -64
                    i32.sub
                    i32.add
                    i32.load
                    i32.store8
                    local.get $p3
                    local.get $l12
                    i32.add
                    local.get $p7
                    i32.const 48
                    i32.add
                    local.get $l10
                    i32.add
                    i32.load
                    i32.store8
                  end
                  local.get $p4
                  local.get $l34
                  f32.store offset=32
                  local.get $p4
                  i32.const 0
                  i32.store offset=44
                  local.get $p4
                  local.get $l31
                  f32.store offset=40
                  local.get $p4
                  local.get $l33
                  f32.store offset=36
                  local.get $p7
                  i32.const 208
                  i32.add
                  local.get $p7
                  i32.const 144
                  i32.add
                  local.get $p7
                  i32.const 80
                  i32.add
                  local.get $p7
                  i32.const 272
                  i32.add
                  local.get $p7
                  i32.const 16
                  i32.add
                  local.get $p7
                  local.get $l9
                  call $f70517
                  local.get $p4
                  local.get $p7
                  i64.load offset=16
                  i64.store
                  local.get $p4
                  local.get $p7
                  i64.load offset=24
                  i64.store offset=8
                  local.get $p4
                  local.get $p7
                  i64.load
                  i64.store offset=16
                  local.get $p4
                  local.get $p7
                  i64.load offset=8
                  i64.store offset=24
                  local.get $p4
                  local.get $p7
                  i64.load offset=304 align=4
                  i64.store offset=68 align=4
                  local.get $p4
                  local.get $p7
                  i32.load offset=312
                  i32.store offset=76
                  local.get $p4
                  local.get $l26
                  f32.store offset=64
                  i32.const 2
                  local.set $p0
                  br $B85
                end
                local.get $l9
                i32.const 4
                i32.shl
                local.tee $l10
                local.get $p7
                i32.const 144
                i32.add
                i32.add
                local.tee $p3
                local.get $l37
                f32.store offset=12
                local.get $p3
                local.get $l22
                f32.store offset=8
                local.get $p3
                local.get $l24
                f32.store offset=4
                local.get $p3
                local.get $l23
                f32.store
                local.get $p7
                i32.const 80
                i32.add
                local.get $l10
                i32.add
                local.tee $p3
                i32.const 0
                i32.store offset=12
                local.get $p3
                local.get $l41
                f32.store offset=8
                local.get $p3
                local.get $l39
                f32.store offset=4
                local.get $p3
                local.get $l38
                f32.store
                local.get $p7
                i32.const 208
                i32.add
                local.get $l10
                i32.add
                local.tee $p3
                i32.const 0
                i32.store offset=12
                local.get $p3
                local.get $l32
                f32.store offset=8
                local.get $p3
                local.get $l29
                f32.store offset=4
                local.get $p3
                local.get $l27
                f32.store
                local.get $p7
                local.get $l9
                i32.const 1
                i32.add
                i32.store offset=44
                block $B95
                  block $B96
                    block $B97
                      block $B98
                        block $B99
                          local.get $l9
                          i32.const 1
                          i32.sub
                          br_table $B99 $B98 $B97 $B96
                        end
                        local.get $p7
                        f32.load offset=224
                        local.get $p7
                        f32.load offset=208
                        local.tee $l27
                        f32.sub
                        local.tee $l22
                        local.get $l22
                        f32.mul
                        local.get $p7
                        f32.load offset=228
                        local.get $p7
                        f32.load offset=212
                        local.tee $l29
                        f32.sub
                        local.tee $l23
                        local.get $l23
                        f32.mul
                        f32.add
                        local.get $p7
                        f32.load offset=232
                        local.get $p7
                        f32.load offset=216
                        local.tee $l32
                        f32.sub
                        local.tee $l24
                        local.get $l24
                        f32.mul
                        f32.add
                        local.tee $l31
                        f32.const 0x1p-23 (;=1.19209e-07;)
                        f32.le
                        if $I100
                          local.get $p7
                          i32.const 1
                          i32.store offset=44
                          local.get $p7
                          local.get $p7
                          i64.load offset=208
                          i64.store offset=16
                          local.get $p7
                          local.get $p7
                          i64.load offset=216
                          i64.store offset=24
                          br $B95
                        end
                        local.get $p7
                        i32.const 0
                        i32.store offset=28
                        local.get $p7
                        local.get $l32
                        local.get $l24
                        local.get $l23
                        local.get $l29
                        f32.neg
                        f32.mul
                        local.get $l27
                        local.get $l22
                        f32.mul
                        f32.sub
                        local.get $l32
                        local.get $l24
                        f32.mul
                        f32.sub
                        local.get $l31
                        f32.div
                        f32.const 0x1p+0 (;=1;)
                        f32.min
                        local.tee $l31
                        f32.const 0x0p+0 (;=0;)
                        local.get $l31
                        f32.const 0x0p+0 (;=0;)
                        f32.gt
                        select
                        local.tee $l31
                        f32.mul
                        f32.add
                        f32.store offset=24
                        local.get $p7
                        local.get $l29
                        local.get $l23
                        local.get $l31
                        f32.mul
                        f32.add
                        f32.store offset=20
                        local.get $p7
                        local.get $l27
                        local.get $l22
                        local.get $l31
                        f32.mul
                        f32.add
                        f32.store offset=16
                        br $B95
                      end
                      local.get $p7
                      i32.const 16
                      i32.add
                      local.get $p7
                      i32.const 208
                      i32.add
                      local.get $p7
                      i32.const 144
                      i32.add
                      local.get $p7
                      i32.const 80
                      i32.add
                      local.get $p7
                      i32.const -64
                      i32.sub
                      local.get $p7
                      i32.const 48
                      i32.add
                      local.get $p7
                      i32.const 44
                      i32.add
                      call $f70518
                      br $B95
                    end
                    local.get $p7
                    i32.const 16
                    i32.add
                    local.get $p7
                    i32.const 208
                    i32.add
                    local.get $p7
                    i32.const 144
                    i32.add
                    local.get $p7
                    i32.const 80
                    i32.add
                    local.get $p7
                    i32.const -64
                    i32.sub
                    local.get $p7
                    i32.const 48
                    i32.add
                    local.get $p7
                    i32.const 44
                    i32.add
                    call $f69905
                    br $B95
                  end
                  local.get $p7
                  i32.const 0
                  i32.store offset=28
                  local.get $p7
                  local.get $l32
                  f32.store offset=24
                  local.get $p7
                  local.get $l29
                  f32.store offset=20
                  local.get $p7
                  local.get $l27
                  f32.store offset=16
                end
                local.get $p7
                local.get $p7
                i64.load offset=16
                i64.store offset=272
                local.get $p7
                local.get $p7
                i64.load offset=24
                i64.store offset=280
                local.get $p7
                f32.load offset=280
                local.tee $l23
                f32.const 0x1p+0 (;=1;)
                local.get $p7
                f32.load offset=272
                local.tee $l24
                local.get $l24
                f32.mul
                local.get $p7
                f32.load offset=276
                local.tee $l27
                local.get $l27
                f32.mul
                f32.add
                local.get $l23
                local.get $l23
                f32.mul
                f32.add
                f32.sqrt
                local.tee $l22
                f32.div
                local.tee $l29
                f32.mul
                local.set $l31
                local.get $l27
                local.get $l29
                f32.mul
                local.set $l33
                local.get $l24
                local.get $l29
                f32.mul
                local.set $l34
                block $B101
                  local.get $l22
                  local.get $l53
                  f32.gt
                  i32.eqz
                  br_if $B101
                  local.get $l22
                  local.get $l26
                  f32.lt
                  i32.eqz
                  br_if $B101
                  local.get $p7
                  f32.load offset=284
                  local.set $l35
                  local.get $l23
                  local.set $l30
                  local.get $l27
                  local.set $l28
                  local.get $l24
                  local.set $l25
                  local.get $l22
                  local.set $l26
                  br $L87
                end
              end
              local.get $l22
              local.get $l26
              f32.lt
              br_if $B86
              local.get $p7
              i32.load offset=44
              local.set $p0
              block $B102
                local.get $l11
                i32.eqz
                br_if $B102
                local.get $l15
                local.get $p0
                i32.const 1
                i32.sub
                local.tee $p3
                i32.store8
                local.get $p3
                i32.eqz
                br_if $B102
                local.get $p3
                i32.const 1
                i32.and
                local.set $l13
                i32.const 0
                local.set $l9
                local.get $p0
                i32.const 2
                i32.ne
                if $I103
                  local.get $p3
                  i32.const -2
                  i32.and
                  local.set $l10
                  loop $L104
                    local.get $l9
                    local.get $l11
                    i32.add
                    local.get $l9
                    i32.const 2
                    i32.shl
                    local.tee $p3
                    local.get $p7
                    i32.const -64
                    i32.sub
                    i32.add
                    i32.load
                    i32.store8
                    local.get $l9
                    local.get $l12
                    i32.add
                    local.get $p7
                    i32.const 48
                    i32.add
                    local.get $p3
                    i32.add
                    i32.load
                    i32.store8
                    local.get $l11
                    local.get $l9
                    i32.const 1
                    i32.or
                    local.tee $p3
                    i32.add
                    local.get $p3
                    i32.const 2
                    i32.shl
                    local.tee $p2
                    local.get $p7
                    i32.const -64
                    i32.sub
                    i32.add
                    i32.load
                    i32.store8
                    local.get $p3
                    local.get $l12
                    i32.add
                    local.get $p7
                    i32.const 48
                    i32.add
                    local.get $p2
                    i32.add
                    i32.load
                    i32.store8
                    local.get $l9
                    i32.const 2
                    i32.add
                    local.set $l9
                    local.get $l10
                    i32.const 2
                    i32.sub
                    local.tee $l10
                    br_if $L104
                  end
                end
                local.get $l13
                i32.eqz
                br_if $B102
                local.get $l9
                local.get $l11
                i32.add
                local.get $l9
                i32.const 2
                i32.shl
                local.tee $p3
                local.get $p7
                i32.const -64
                i32.sub
                i32.add
                i32.load
                i32.store8
                local.get $l9
                local.get $l12
                i32.add
                local.get $p7
                i32.const 48
                i32.add
                local.get $p3
                i32.add
                i32.load
                i32.store8
              end
              local.get $p7
              local.get $p7
              i32.const 296
              i32.add
              local.tee $l9
              i32.load
              i32.store offset=312
              local.get $p7
              local.get $p7
              i64.load offset=288
              i64.store offset=304
              local.get $p7
              local.get $l35
              f32.store offset=284
              local.get $p7
              local.get $l25
              f32.store offset=272
              local.get $p7
              local.get $l28
              f32.store offset=276
              local.get $p7
              local.get $l30
              f32.store offset=280
              local.get $p7
              i32.const 208
              i32.add
              local.get $p7
              i32.const 144
              i32.add
              local.get $p7
              i32.const 80
              i32.add
              local.get $p7
              i32.const 272
              i32.add
              local.get $p7
              i32.const 16
              i32.add
              local.get $p7
              local.get $p0
              call $f70517
              local.get $p4
              i32.const 0
              i32.store offset=60
              local.get $p4
              local.get $l31
              f32.store offset=56
              local.get $p4
              local.get $l33
              f32.store offset=52
              local.get $p4
              local.get $l34
              f32.store offset=48
              local.get $p4
              i32.const 0
              i32.store offset=44
              local.get $p4
              local.get $l30
              f32.const 0x1p+0 (;=1;)
              local.get $l26
              f32.div
              local.tee $l22
              f32.mul
              f32.store offset=40
              local.get $p4
              local.get $l28
              local.get $l22
              f32.mul
              f32.store offset=36
              local.get $p4
              local.get $l25
              local.get $l22
              f32.mul
              f32.store offset=32
              local.get $p4
              local.get $p7
              i64.load offset=16
              i64.store
              local.get $p4
              local.get $p7
              i64.load offset=24
              i64.store offset=8
              local.get $p4
              local.get $p7
              i64.load
              i64.store offset=16
              local.get $p4
              local.get $p7
              i64.load offset=8
              i64.store offset=24
              local.get $p4
              local.get $l26
              f32.store offset=64
              local.get $p4
              local.get $p7
              i64.load offset=288
              i64.store offset=68 align=4
              local.get $p4
              local.get $l9
              i32.load
              i32.store offset=76
              i32.const 4
              local.set $p0
              br $B85
            end
            i32.const 5
            local.set $p0
            local.get $l11
            i32.eqz
            br_if $B85
            local.get $l15
            local.get $p7
            i32.load offset=44
            local.tee $p3
            i32.store8
            local.get $p3
            i32.eqz
            br_if $B85
            local.get $p3
            i32.const 1
            i32.and
            local.set $l13
            i32.const 0
            local.set $l9
            local.get $p3
            i32.const 1
            i32.ne
            if $I105
              local.get $p3
              i32.const -2
              i32.and
              local.set $l10
              loop $L106
                local.get $l9
                local.get $l11
                i32.add
                local.get $l9
                i32.const 2
                i32.shl
                local.tee $p3
                local.get $p7
                i32.const -64
                i32.sub
                i32.add
                i32.load
                i32.store8
                local.get $l9
                local.get $l12
                i32.add
                local.get $p7
                i32.const 48
                i32.add
                local.get $p3
                i32.add
                i32.load
                i32.store8
                local.get $l11
                local.get $l9
                i32.const 1
                i32.or
                local.tee $p3
                i32.add
                local.get $p3
                i32.const 2
                i32.shl
                local.tee $p2
                local.get $p7
                i32.const -64
                i32.sub
                i32.add
                i32.load
                i32.store8
                local.get $p3
                local.get $l12
                i32.add
                local.get $p7
                i32.const 48
                i32.add
                local.get $p2
                i32.add
                i32.load
                i32.store8
                local.get $l9
                i32.const 2
                i32.add
                local.set $l9
                local.get $l10
                i32.const 2
                i32.sub
                local.tee $l10
                br_if $L106
              end
            end
            local.get $l13
            i32.eqz
            br_if $B85
            local.get $l9
            local.get $l11
            i32.add
            local.get $l9
            i32.const 2
            i32.shl
            local.tee $p3
            local.get $p7
            i32.const -64
            i32.sub
            i32.add
            i32.load
            i32.store8
            local.get $l9
            local.get $l12
            i32.add
            local.get $p7
            i32.const 48
            i32.add
            local.get $p3
            i32.add
            i32.load
            i32.store8
          end
          local.get $p7
          i32.const 320
          i32.add
          global.set $g0
          local.get $l8
          local.get $l8
          i64.load offset=840
          i64.store offset=88
          local.get $l8
          local.get $l8
          i64.load offset=832
          i64.store offset=80
          local.get $l8
          local.get $l8
          i64.load offset=848
          i64.store offset=64
          local.get $l8
          local.get $l8
          i64.load offset=856
          i64.store offset=72
          local.get $l8
          i32.const 880
          i32.add
          local.get $l8
          i32.const 872
          i32.add
          local.get $l8
          i32.const 752
          i32.add
          local.get $l8
          i32.const 720
          i32.add
          local.get $l8
          i32.const 624
          i32.add
          local.get $p0
          local.get $l8
          i32.const 128
          i32.add
          local.get $p5
          local.get $p6
          local.get $l20
          local.get $l8
          i32.const 80
          i32.add
          local.get $l8
          i32.const -64
          i32.sub
          i32.const 0
          i32.const 1
          local.get $l40
          call $f70073
          br $B0
        end
        local.get $l8
        i32.const 3132572
        i32.store offset=872
        local.get $l8
        local.get $l8
        i32.const 208
        i32.add
        i32.store offset=876
        local.get $l8
        i32.const 880
        i32.add
        local.get $l8
        i32.const 872
        i32.add
        local.get $l9
        local.get $l8
        i32.const 848
        i32.add
        i32.const 1
        local.get $p5
        i32.const 67
        i32.add
        local.get $p5
        i32.const 71
        i32.add
        local.get $p5
        i32.const 66
        i32.add
        local.get $l8
        i32.const 128
        i32.add
        call $f70533
        local.set $p3
        local.get $l8
        local.get $l8
        i64.load offset=840
        i64.store offset=120
        local.get $l8
        local.get $l8
        i64.load offset=832
        i64.store offset=112
        local.get $l8
        local.get $l8
        i64.load offset=848
        i64.store offset=96
        local.get $l8
        local.get $l8
        i64.load offset=856
        i64.store offset=104
        local.get $l8
        i32.const 880
        i32.add
        local.get $l8
        i32.const 872
        i32.add
        local.get $l8
        i32.const 752
        i32.add
        local.get $l8
        i32.const 720
        i32.add
        local.get $l8
        i32.const 624
        i32.add
        local.get $p3
        local.get $l8
        i32.const 128
        i32.add
        local.get $p5
        local.get $p6
        local.get $l20
        local.get $l8
        i32.const 112
        i32.add
        local.get $l8
        i32.const 96
        i32.add
        i32.const 0
        i32.const 0
        local.get $l40
        call $f70073
        br $B0
      end
      i32.const 0
      local.get $p5
      i32.load8_u offset=64
      local.tee $p3
      i32.eqz
      br_if $B0
      drop
      i32.const 1
      local.set $p7
      local.get $p5
      i32.load offset=76
      local.tee $p0
      f32.load offset=32
      local.tee $l27
      local.set $l22
      local.get $p0
      f32.load offset=36
      local.tee $l40
      local.set $l23
      local.get $p0
      f32.load offset=40
      local.tee $l25
      local.set $l24
      block $B107
        local.get $p3
        i32.const 1
        i32.eq
        br_if $B107
        local.get $p3
        i32.const 1
        i32.sub
        local.tee $p1
        i32.const 1
        i32.and
        local.set $p4
        local.get $l25
        local.set $l24
        local.get $l40
        local.set $l23
        local.get $l27
        local.set $l22
        local.get $p3
        i32.const 2
        i32.ne
        if $I108
          local.get $p1
          i32.const -2
          i32.and
          local.set $p1
          loop $L109
            local.get $l22
            local.get $p0
            local.get $p7
            i32.const 48
            i32.mul
            i32.add
            local.tee $p3
            f32.load offset=32
            f32.add
            local.get $p3
            f32.load offset=80
            f32.add
            local.set $l22
            local.get $l24
            local.get $p3
            f32.load offset=40
            f32.add
            local.get $p3
            f32.load offset=88
            f32.add
            local.set $l24
            local.get $l23
            local.get $p3
            f32.load offset=36
            f32.add
            local.get $p3
            f32.load offset=84
            f32.add
            local.set $l23
            local.get $p7
            i32.const 2
            i32.add
            local.set $p7
            local.get $p1
            i32.const 2
            i32.sub
            local.tee $p1
            br_if $L109
          end
        end
        local.get $p4
        i32.eqz
        br_if $B107
        local.get $l22
        local.get $p0
        local.get $p7
        i32.const 48
        i32.mul
        i32.add
        local.tee $p3
        f32.load offset=32
        f32.add
        local.set $l22
        local.get $l23
        local.get $p3
        f32.load offset=36
        f32.add
        local.set $l23
        local.get $l24
        local.get $p3
        f32.load offset=40
        f32.add
        local.set $l24
      end
      local.get $l8
      i32.const 0
      i32.store offset=380
      local.get $l8
      local.get $l8
      f32.load offset=728
      local.tee $l26
      local.get $l26
      local.get $l24
      local.get $l25
      local.get $l22
      local.get $l22
      f32.mul
      local.get $l23
      local.get $l23
      f32.mul
      f32.add
      local.get $l24
      local.get $l24
      f32.mul
      f32.add
      f32.const 0x1p-23 (;=1.19209e-07;)
      f32.gt
      local.tee $p3
      select
      local.tee $l24
      f32.mul
      local.get $l8
      f32.load offset=720
      local.tee $l25
      local.get $l22
      local.get $l27
      local.get $p3
      select
      local.tee $l27
      f32.mul
      local.get $l8
      f32.load offset=724
      local.tee $l29
      local.get $l23
      local.get $l40
      local.get $p3
      select
      local.tee $l23
      f32.mul
      f32.add
      f32.add
      local.tee $l40
      f32.mul
      local.get $l8
      f32.load offset=732
      local.tee $l22
      local.get $l25
      local.get $l23
      f32.mul
      local.get $l29
      local.get $l27
      f32.mul
      f32.sub
      f32.mul
      local.get $l24
      local.get $l22
      local.get $l22
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l30
      f32.mul
      f32.add
      f32.add
      local.tee $l28
      local.get $l28
      f32.add
      local.tee $l28
      f32.const 0x1p+0 (;=1;)
      local.get $l28
      local.get $l28
      f32.mul
      local.get $l25
      local.get $l40
      f32.mul
      local.get $l22
      local.get $l29
      local.get $l24
      f32.mul
      local.get $l26
      local.get $l23
      f32.mul
      f32.sub
      f32.mul
      local.get $l27
      local.get $l30
      f32.mul
      f32.add
      f32.add
      local.tee $l28
      local.get $l28
      f32.add
      local.tee $l28
      local.get $l28
      f32.mul
      local.get $l29
      local.get $l40
      f32.mul
      local.get $l22
      local.get $l26
      local.get $l27
      f32.mul
      local.get $l25
      local.get $l24
      f32.mul
      f32.sub
      f32.mul
      local.get $l23
      local.get $l30
      f32.mul
      f32.add
      f32.add
      local.tee $l22
      local.get $l22
      f32.add
      local.tee $l22
      local.get $l22
      f32.mul
      f32.add
      f32.add
      f32.sqrt
      f32.div
      local.tee $l23
      f32.mul
      f32.store offset=376
      local.get $l8
      local.get $l22
      local.get $l23
      f32.mul
      f32.store offset=372
      local.get $l8
      local.get $l28
      local.get $l23
      f32.mul
      f32.store offset=368
      local.get $p5
      local.get $p6
      local.get $l8
      i32.const 368
      i32.add
      local.get $l8
      i32.const 720
      i32.add
      local.get $l8
      i32.const 784
      i32.add
      call $f69970
      i32.const 1
    end
    local.set $p5
    local.get $l8
    i32.const 960
    i32.add
    global.set $g0
    local.get $p5)