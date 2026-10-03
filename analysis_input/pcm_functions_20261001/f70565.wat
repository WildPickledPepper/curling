  (func $f70565 (type $t18) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (result i32)
    (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32)
    global.get $g0
    i32.const 11328
    i32.sub
    local.tee $l8
    global.set $g0
    local.get $p3
    i32.const 20
    i32.add
    local.tee $l9
    f32.load
    local.set $l20
    local.get $p3
    i32.const 24
    i32.add
    local.tee $l10
    f32.load
    local.set $l22
    local.get $p2
    i32.const 20
    i32.add
    local.tee $l11
    f32.load
    local.set $l24
    local.get $p2
    i32.const 24
    i32.add
    local.tee $l12
    f32.load
    local.set $l25
    local.get $p5
    i32.load
    local.set $p5
    local.get $p3
    f32.load
    local.set $l14
    local.get $p3
    f32.load offset=4
    local.set $l18
    local.get $p3
    f32.load offset=8
    local.set $l13
    local.get $p3
    f32.load offset=12
    local.set $l16
    local.get $p3
    f32.load offset=16
    local.set $l21
    local.get $p2
    f32.load
    local.set $l15
    local.get $p2
    f32.load offset=4
    local.set $l17
    local.get $p2
    f32.load offset=8
    local.set $l19
    local.get $p2
    f32.load offset=12
    local.set $l23
    local.get $p2
    f32.load offset=16
    local.set $l26
    local.get $l8
    local.get $p0
    f32.load offset=4
    local.tee $l28
    f32.store offset=11312
    local.get $l8
    local.get $p4
    f32.load
    local.tee $l30
    f32.store offset=11296
    local.get $l8
    i32.const 11292
    i32.add
    i32.const 0
    i32.store
    local.get $l8
    i32.const 11288
    i32.add
    local.get $l25
    f32.store
    local.get $l8
    i32.const 11284
    i32.add
    local.get $l24
    f32.store
    local.get $l8
    local.get $l26
    f32.store offset=11280
    local.get $l8
    local.get $l23
    f32.store offset=11276
    local.get $l8
    local.get $l19
    f32.store offset=11272
    local.get $l8
    local.get $l17
    f32.store offset=11268
    local.get $l8
    local.get $l15
    f32.store offset=11264
    local.get $l8
    i32.const 11260
    i32.add
    i32.const 0
    i32.store
    local.get $l8
    i32.const 11256
    i32.add
    local.get $l22
    f32.store
    local.get $l8
    i32.const 11252
    i32.add
    local.get $l20
    f32.store
    local.get $l8
    local.get $l21
    f32.store offset=11248
    local.get $l8
    local.get $l16
    f32.store offset=11244
    local.get $l8
    local.get $l13
    f32.store offset=11240
    local.get $l8
    local.get $l18
    f32.store offset=11236
    local.get $l8
    local.get $l14
    f32.store offset=11232
    local.get $l16
    local.get $l16
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l27
    local.get $l26
    local.get $l21
    f32.sub
    local.tee $l21
    f32.mul
    local.get $l16
    local.get $l13
    local.get $l24
    local.get $l20
    f32.sub
    local.tee $l20
    f32.mul
    local.get $l18
    local.get $l25
    local.get $l22
    f32.sub
    local.tee $l22
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l14
    local.get $l20
    local.get $l18
    f32.neg
    local.tee $l29
    f32.mul
    local.get $l14
    local.get $l21
    f32.mul
    f32.sub
    local.get $l13
    local.get $l22
    f32.mul
    f32.sub
    local.tee $l24
    f32.mul
    f32.sub
    local.tee $l25
    local.get $l25
    f32.add
    local.set $l25
    local.get $l27
    local.get $l22
    f32.mul
    local.get $l16
    local.get $l18
    local.get $l21
    f32.mul
    local.get $l14
    local.get $l20
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l13
    local.get $l24
    f32.mul
    f32.sub
    local.tee $l26
    local.get $l26
    f32.add
    local.set $l26
    local.get $l27
    local.get $l20
    f32.mul
    local.get $l16
    local.get $l14
    local.get $l22
    f32.mul
    local.get $l13
    local.get $l21
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l18
    local.get $l24
    f32.mul
    f32.sub
    local.tee $l20
    local.get $l20
    f32.add
    local.set $l24
    block $B0
      block $B1
        local.get $l17
        local.get $l13
        f32.mul
        local.get $l19
        local.get $l18
        f32.mul
        f32.sub
        local.get $l15
        local.get $l16
        f32.mul
        local.get $l23
        local.get $l14
        f32.mul
        f32.sub
        f32.add
        local.tee $l22
        local.get $p5
        f32.load
        f32.mul
        local.get $l19
        local.get $l14
        f32.mul
        local.get $l15
        local.get $l13
        f32.mul
        f32.sub
        local.get $l17
        local.get $l16
        f32.mul
        local.get $l23
        local.get $l18
        f32.mul
        f32.sub
        f32.add
        local.tee $l20
        local.get $p5
        f32.load offset=4
        f32.mul
        f32.add
        local.get $l15
        local.get $l18
        f32.mul
        local.get $l17
        local.get $l14
        f32.mul
        f32.sub
        local.get $l19
        local.get $l16
        f32.mul
        local.get $l23
        local.get $l13
        f32.mul
        f32.sub
        f32.add
        local.tee $l18
        local.get $p5
        f32.load offset=8
        f32.mul
        f32.add
        local.get $l23
        local.get $l16
        f32.mul
        local.get $l17
        local.get $l29
        f32.mul
        local.get $l15
        local.get $l14
        f32.mul
        f32.sub
        local.get $l19
        local.get $l13
        f32.mul
        f32.sub
        f32.sub
        local.tee $l16
        local.get $p5
        f32.load offset=12
        f32.mul
        f32.add
        f32.const 0x1.ffe5cap-1 (;=0.9998;)
        f32.lt
        i32.eqz
        if $I2
          local.get $l28
          f32.const 0x1.47ae14p-6 (;=0.02;)
          f32.mul
          local.get $l25
          local.get $p5
          f32.load offset=16
          f32.sub
          local.tee $l13
          local.get $l13
          f32.neg
          local.tee $l15
          local.get $l13
          local.get $l15
          f32.gt
          select
          local.tee $l13
          local.get $l24
          local.get $p5
          f32.load offset=20
          f32.sub
          local.tee $l15
          local.get $l15
          f32.neg
          local.tee $l17
          local.get $l15
          local.get $l17
          f32.gt
          select
          local.tee $l15
          local.get $l13
          local.get $l15
          f32.ge
          select
          local.tee $l17
          local.get $l13
          f32.const 0x0p+0 (;=0;)
          local.get $l26
          local.get $p5
          f32.load offset=24
          f32.sub
          local.tee $l15
          local.get $l15
          f32.neg
          local.tee $l19
          local.get $l15
          local.get $l19
          f32.gt
          select
          f32.const 0x0p+0 (;=0;)
          f32.ge
          select
          local.tee $l13
          local.get $l13
          local.get $l17
          f32.le
          select
          f32.lt
          i32.eqz
          br_if $B1
        end
        local.get $l8
        local.get $l28
        f32.const 0x1.0624dep-10 (;=0.001;)
        f32.mul
        f32.store offset=11216
        local.get $p1
        i32.load offset=40
        local.set $p2
        local.get $l9
        f32.load
        local.set $l19
        local.get $l11
        f32.load
        local.set $l23
        local.get $l10
        f32.load
        local.set $l27
        local.get $l12
        f32.load
        local.set $l29
        local.get $p3
        f32.load offset=12
        local.set $l13
        local.get $p3
        f32.load offset=4
        local.set $l15
        local.get $p3
        f32.load offset=8
        local.set $l17
        local.get $l8
        i32.const 11200
        i32.add
        i64.const 4575657221408423936
        i64.store
        local.get $l8
        i32.const 11192
        i32.add
        i64.const 0
        i64.store
        local.get $l8
        i32.const 11184
        i32.add
        i64.const 4575657221408423936
        i64.store
        local.get $l8
        i32.const 11176
        i32.add
        i64.const 0
        i64.store
        local.get $l8
        i32.const 11168
        i32.add
        i64.const 4575657222473777152
        i64.store
        local.get $l8
        i32.const 11152
        i32.add
        i64.const 1065353216
        i64.store
        local.get $l8
        i32.const 0
        i32.store8 offset=11208
        local.get $l8
        i64.const 0
        i64.store offset=11160
        local.get $l8
        i64.const 0
        i64.store offset=11144
        local.get $l8
        i64.const 1065353216
        i64.store offset=11136
        local.get $l29
        local.get $l27
        f32.sub
        local.tee $l27
        local.get $l27
        f32.add
        local.tee $l27
        local.get $l13
        local.get $l13
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.tee $l31
        f32.mul
        local.get $l13
        local.get $l14
        local.get $l23
        local.get $l19
        f32.sub
        local.tee $l19
        local.get $l19
        f32.add
        local.tee $l29
        f32.mul
        local.get $l15
        local.get $l21
        local.get $l21
        f32.add
        local.tee $l21
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        local.get $l17
        local.get $l14
        local.get $l21
        f32.mul
        local.get $l29
        local.get $l15
        f32.mul
        f32.add
        local.get $l27
        local.get $l17
        f32.mul
        f32.add
        local.tee $l32
        f32.mul
        f32.add
        local.set $l19
        local.get $l15
        local.get $l32
        f32.mul
        local.get $l29
        local.get $l31
        f32.mul
        local.get $l13
        local.get $l21
        local.get $l17
        f32.mul
        local.get $l14
        local.get $l27
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        local.set $l23
        local.get $l14
        local.get $l32
        f32.mul
        local.get $l21
        local.get $l31
        f32.mul
        local.get $l13
        local.get $l27
        local.get $l15
        f32.mul
        local.get $l29
        local.get $l17
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        local.set $l13
        local.get $l28
        local.get $l30
        f32.add
        local.set $l14
        block $B3 (result i32)
          block $B4
            local.get $p1
            f32.load offset=4
            f32.const 0x1p+0 (;=1;)
            f32.ne
            br_if $B4
            local.get $p1
            f32.load offset=8
            f32.const 0x1p+0 (;=1;)
            f32.ne
            br_if $B4
            i32.const 1
            local.get $p1
            f32.load offset=12
            f32.const 0x1p+0 (;=1;)
            f32.eq
            br_if $B3
            drop
          end
          local.get $l8
          i32.const 11136
          i32.add
          local.get $p1
          i32.const 4
          i32.add
          local.get $p1
          i32.const 16
          i32.add
          call $f70485
          i32.const 0
        end
        local.set $p3
        local.get $p5
        local.get $l26
        f32.store offset=24
        local.get $p5
        local.get $l24
        f32.store offset=20
        local.get $p5
        local.get $l25
        f32.store offset=16
        local.get $p5
        local.get $l16
        f32.store offset=12
        local.get $p5
        local.get $l18
        f32.store offset=8
        local.get $p5
        local.get $l20
        f32.store offset=4
        local.get $p5
        local.get $l22
        f32.store
        local.get $p5
        i32.const 0
        i32.store8 offset=62
        local.get $p5
        i32.const 0
        i32.store offset=28
        local.get $l8
        i32.const 1
        i32.store8 offset=11120
        local.get $l8
        i64.const 4672924418048
        i64.store offset=11128
        local.get $l8
        local.get $l8
        i32.const 6768
        i32.add
        i32.store offset=11124
        local.get $p2
        i32.load offset=56
        local.set $p1
        local.get $l8
        i32.const 0
        i32.store offset=1012
        local.get $l8
        local.get $p3
        i32.store8 offset=160
        local.get $l8
        local.get $p1
        i32.store offset=156
        local.get $l8
        i32.const 2
        i32.store offset=148
        local.get $l8
        i32.const 3124404
        i32.store offset=144
        local.get $l8
        local.get $l8
        i32.const 11136
        i32.add
        i32.store offset=152
        local.get $l8
        i32.const 1024
        i32.add
        local.tee $l9
        local.get $l8
        i32.const 11296
        i32.add
        local.get $l8
        i32.const 11216
        i32.add
        local.get $l8
        i32.const 11264
        i32.add
        local.get $l8
        i32.const 11232
        i32.add
        local.get $p5
        local.get $p6
        local.get $l8
        i32.const 6768
        i32.add
        local.get $p7
        call $f70050
        local.set $l10
        local.get $l8
        i32.const 4668
        i32.add
        i32.const 0
        i32.store
        local.get $l8
        i32.const 4664
        i32.add
        local.get $l19
        f32.store
        local.get $l8
        i32.const 4660
        i32.add
        local.get $l23
        f32.store
        local.get $l8
        i32.const 4656
        i32.add
        local.get $l13
        f32.store
        local.get $l8
        i32.const 6760
        i32.add
        i64.const 274877906944
        i64.store
        local.get $l8
        i32.const 6756
        i32.add
        local.get $l8
        i32.const 4704
        i32.add
        i32.store
        local.get $l8
        i32.const 6752
        i32.add
        i32.const 1
        i32.store8
        local.get $l8
        i32.const 4672
        i32.add
        local.get $l8
        i64.load offset=11312
        i64.store
        local.get $l8
        i32.const 4680
        i32.add
        local.get $l8
        i64.load offset=11320
        i64.store
        local.get $l8
        i32.const 4688
        i32.add
        local.get $l8
        f32.load offset=11312
        local.get $l8
        f32.load offset=11296
        f32.add
        local.tee $l16
        local.get $l16
        f32.mul
        f32.store
        local.get $l8
        local.get $l19
        f32.store offset=136
        local.get $l8
        local.get $l23
        f32.store offset=132
        local.get $l8
        local.get $l13
        f32.store offset=128
        local.get $l8
        local.get $l14
        f32.store offset=120
        local.get $l8
        local.get $l14
        f32.store offset=116
        local.get $l8
        local.get $l14
        f32.store offset=112
        local.get $l8
        i32.const 1065353216
        i32.store offset=104
        local.get $l8
        i64.const 1065353216
        i64.store offset=88
        local.get $l8
        i64.const 0
        i64.store offset=96
        local.get $l8
        i64.const 0
        i64.store offset=80
        local.get $l8
        i64.const 1065353216
        i64.store offset=72
        block $B5 (result f32)
          local.get $p3
          if $I6
            f32.const 0x0p+0 (;=0;)
            local.set $l16
            f32.const 0x1p+0 (;=1;)
            local.set $l18
            local.get $l14
            local.set $l17
            f32.const 0x0p+0 (;=0;)
            local.set $l21
            f32.const 0x0p+0 (;=0;)
            local.set $l20
            f32.const 0x1p+0 (;=1;)
            local.set $l22
            f32.const 0x0p+0 (;=0;)
            local.set $l28
            f32.const 0x0p+0 (;=0;)
            local.set $l24
            f32.const 0x0p+0 (;=0;)
            local.set $l25
            f32.const 0x1p+0 (;=1;)
            local.set $l26
            local.get $l14
            br $B5
          end
          local.get $l8
          i32.const 11136
          i32.add
          local.get $l8
          i32.const 128
          i32.add
          local.get $l8
          i32.const 112
          i32.add
          local.get $l8
          i32.const 72
          i32.add
          call $f70179
          local.get $l8
          f32.load offset=120
          local.set $l14
          local.get $l8
          f32.load offset=112
          local.set $l17
          local.get $l8
          f32.load offset=136
          local.set $l19
          local.get $l8
          f32.load offset=132
          local.set $l23
          local.get $l8
          f32.load offset=128
          local.set $l13
          local.get $l8
          f32.load offset=104
          local.set $l18
          local.get $l8
          f32.load offset=100
          local.set $l16
          local.get $l8
          f32.load offset=96
          local.set $l21
          local.get $l8
          f32.load offset=92
          local.set $l20
          local.get $l8
          f32.load offset=88
          local.set $l22
          local.get $l8
          f32.load offset=84
          local.set $l28
          local.get $l8
          f32.load offset=80
          local.set $l24
          local.get $l8
          f32.load offset=76
          local.set $l25
          local.get $l8
          f32.load offset=72
          local.set $l26
          local.get $l8
          f32.load offset=116
        end
        local.set $l15
        local.get $l8
        local.get $l14
        f32.store offset=56
        local.get $l8
        local.get $l15
        f32.store offset=52
        local.get $l8
        local.get $l19
        f32.store offset=44
        local.get $l8
        local.get $l23
        f32.store offset=40
        local.get $l8
        local.get $l18
        f32.store offset=32
        local.get $l8
        local.get $l16
        f32.store offset=28
        local.get $l8
        local.get $l20
        f32.store offset=20
        local.get $l8
        local.get $l22
        f32.store offset=16
        local.get $l8
        local.get $l17
        f32.store offset=48
        local.get $l8
        local.get $l13
        f32.store offset=36
        local.get $l8
        local.get $l21
        f32.store offset=24
        local.get $l8
        local.get $l28
        f32.store offset=12
        local.get $l8
        local.get $l24
        f32.store offset=8
        local.get $l8
        local.get $l25
        f32.store offset=4
        local.get $l8
        local.get $l26
        f32.store
        local.get $p2
        local.get $l8
        local.get $l8
        i32.const 144
        i32.add
        i32.const 1
        i32.const 1
        local.get $p2
        i32.load16_u offset=4
        i32.const 2
        i32.shl
        i32.const 3124600
        i32.add
        i32.load
        call_indirect $__indirect_function_table (type $t6)
        local.get $l8
        i32.load offset=1012
        local.tee $p0
        if $I7
          local.get $l8
          i32.const 164
          i32.add
          local.set $p3
          local.get $l8
          i32.const 740
          i32.add
          local.set $p2
          local.get $l8
          i32.const 932
          i32.add
          local.set $p1
          local.get $l8
          i32.const 996
          i32.add
          local.set $p4
          local.get $l8
          i32.const 1024
          i32.add
          local.set $p7
          loop $L8
            local.get $p7
            local.get $p3
            local.get $p1
            i32.load
            local.get $p4
            i32.load8_u
            local.get $p2
            call $f70064
            local.get $p4
            i32.const 1
            i32.add
            local.set $p4
            local.get $p1
            i32.const 4
            i32.add
            local.set $p1
            local.get $p2
            i32.const 12
            i32.add
            local.set $p2
            local.get $p3
            i32.const 36
            i32.add
            local.set $p3
            local.get $p0
            i32.const 1
            i32.sub
            local.tee $p0
            br_if $L8
          end
          local.get $l8
          i32.const 0
          i32.store offset=1012
        end
        local.get $l9
        call $f70066
        local.get $l10
        i32.const 1
        i32.const 0
        call $f70051
        local.get $l8
        i32.const 3124404
        i32.store offset=144
        block $B9
          local.get $l8
          i32.load offset=6764
          local.tee $p3
          i32.const 0
          i32.lt_s
          br_if $B9
          local.get $p3
          i32.const 2147483647
          i32.and
          i32.eqz
          br_if $B9
          local.get $l8
          i32.load offset=6756
          local.tee $p3
          local.get $l8
          i32.const 4704
          i32.add
          i32.eq
          br_if $B9
          local.get $p3
          i32.eqz
          br_if $B9
          call $f69753
          local.tee $p2
          local.get $p3
          local.get $p2
          i32.load
          i32.load offset=12
          call_indirect $__indirect_function_table (type $t1)
        end
        local.get $l8
        i32.load offset=11132
        local.tee $p3
        i32.const 0
        i32.lt_s
        br_if $B0
        local.get $p3
        i32.const 2147483647
        i32.and
        i32.eqz
        br_if $B0
        local.get $l8
        i32.load offset=11124
        local.tee $p3
        local.get $l8
        i32.const 6768
        i32.add
        i32.eq
        br_if $B0
        local.get $p3
        i32.eqz
        br_if $B0
        call $f69753
        local.tee $p2
        local.get $p3
        local.get $p2
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
        br $B0
      end
      i32.const 0
      local.set $p3
      local.get $l8
      i32.const 0
      i32.store offset=204
      local.get $l8
      local.get $l26
      f32.store offset=200
      local.get $l8
      local.get $l24
      f32.store offset=196
      local.get $l8
      i32.const 0
      i32.store offset=188
      local.get $l8
      i32.const 0
      i32.store offset=172
      local.get $l8
      local.get $l18
      local.get $l20
      local.get $l20
      f32.add
      local.tee $l13
      f32.mul
      local.tee $l15
      local.get $l16
      local.get $l22
      local.get $l22
      f32.add
      local.tee $l14
      f32.mul
      local.tee $l17
      f32.sub
      f32.store offset=180
      local.get $l8
      local.get $l15
      local.get $l17
      f32.add
      f32.store offset=168
      local.get $l8
      f32.const 0x1p+0 (;=1;)
      local.get $l22
      local.get $l14
      f32.mul
      f32.sub
      local.tee $l15
      local.get $l20
      local.get $l13
      f32.mul
      local.tee $l17
      f32.sub
      f32.store offset=184
      local.get $l8
      local.get $l15
      local.get $l18
      local.get $l18
      local.get $l18
      f32.add
      local.tee $l19
      f32.mul
      local.tee $l23
      f32.sub
      f32.store offset=164
      local.get $l8
      local.get $l25
      f32.store offset=192
      local.get $l8
      i32.const 0
      i32.store offset=156
      local.get $l8
      local.get $l18
      local.get $l14
      f32.mul
      local.tee $l18
      local.get $l16
      local.get $l13
      f32.mul
      local.tee $l13
      f32.add
      f32.store offset=176
      local.get $l8
      local.get $l20
      local.get $l14
      f32.mul
      local.tee $l14
      local.get $l16
      local.get $l19
      f32.mul
      local.tee $l16
      f32.sub
      f32.store offset=160
      local.get $l8
      local.get $l18
      local.get $l13
      f32.sub
      f32.store offset=152
      local.get $l8
      local.get $l14
      local.get $l16
      f32.add
      f32.store offset=148
      local.get $l8
      f32.const 0x1p+0 (;=1;)
      local.get $l17
      f32.sub
      local.get $l23
      f32.sub
      f32.store offset=144
      local.get $l8
      local.get $l28
      f32.const 0x1.99999ap-5 (;=0.05;)
      f32.mul
      f32.store offset=11136
      local.get $l8
      local.get $l28
      local.get $l30
      f32.add
      f32.store
      local.get $p5
      i32.load8_u offset=62
      i32.eqz
      br_if $B0
      loop $L10
        local.get $l8
        i32.const 6768
        i32.add
        local.get $p5
        local.get $p3
        local.get $p5
        i32.add
        i32.const 56
        i32.add
        local.tee $p4
        i32.load8_u
        local.tee $p1
        i32.const 400
        i32.mul
        i32.add
        local.tee $p2
        i32.const -64
        i32.sub
        local.get $l8
        i32.const 144
        i32.add
        local.get $l8
        i32.const 11136
        i32.add
        call $f69978
        block $B11
          local.get $p2
          i32.load offset=448
          i32.eqz
          if $I12
            local.get $p5
            local.get $p5
            i32.load8_u offset=62
            i32.const 1
            i32.sub
            local.tee $p2
            i32.store8 offset=62
            local.get $p5
            local.get $p2
            i32.const 255
            i32.and
            i32.add
            i32.const 56
            i32.add
            local.tee $p2
            i32.load8_u
            local.set $p0
            local.get $p2
            local.get $p1
            i32.store8
            local.get $p4
            local.get $p0
            i32.store8
            local.get $p3
            i32.const 1
            i32.sub
            local.set $p3
            br $B11
          end
          local.get $p5
          local.get $p1
          i32.const 2
          i32.shl
          i32.add
          local.get $l8
          f32.load offset=6768
          f32.store offset=32
        end
        local.get $p3
        i32.const 1
        i32.add
        local.tee $p3
        local.get $p5
        i32.load8_u offset=62
        i32.lt_u
        br_if $L10
      end
    end
    local.get $p5
    local.get $p6
    local.get $l8
    i32.const 11264
    i32.add
    local.get $l8
    i32.const 11232
    i32.add
    local.get $l8
    i32.const 11312
    i32.add
    call $f69980
    local.set $p5
    local.get $l8
    i32.const 11328
    i32.add
    global.set $g0
    local.get $p5)
