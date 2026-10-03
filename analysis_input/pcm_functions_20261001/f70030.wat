  (func $f70030 (type $t486) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 f32) (param $p8 i32) (param $p9 i32) (param $p10 i32) (param $p11 i32) (param $p12 i32) (param $p13 i32) (param $p14 i32) (result i32)
    (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32)
    global.get $g0
    i32.const 9952
    i32.sub
    local.tee $l15
    global.set $g0
    local.get $p6
    i32.const 20
    i32.add
    local.tee $l16
    f32.load
    local.set $l29
    local.get $p6
    i32.const 24
    i32.add
    local.tee $l17
    f32.load
    local.set $l30
    local.get $p5
    i32.const 20
    i32.add
    local.tee $l18
    f32.load
    local.set $l31
    local.get $p5
    i32.const 24
    i32.add
    local.tee $l19
    f32.load
    local.set $l32
    local.get $p6
    f32.load
    local.set $l21
    local.get $p6
    f32.load offset=4
    local.set $l23
    local.get $p6
    f32.load offset=8
    local.set $l20
    local.get $p6
    f32.load offset=12
    local.set $l22
    local.get $p6
    f32.load offset=16
    local.set $l25
    local.get $p5
    f32.load
    local.set $l24
    local.get $p5
    f32.load offset=4
    local.set $l26
    local.get $p5
    f32.load offset=8
    local.set $l27
    local.get $p5
    f32.load offset=12
    local.set $l28
    local.get $p5
    f32.load offset=16
    local.set $l33
    local.get $l15
    local.get $p7
    f32.store offset=9936
    local.get $l15
    i32.const 9932
    i32.add
    i32.const 0
    i32.store
    local.get $l15
    i32.const 9928
    i32.add
    local.get $l32
    f32.store
    local.get $l15
    i32.const 9924
    i32.add
    local.get $l31
    f32.store
    local.get $l15
    local.get $l33
    f32.store offset=9920
    local.get $l15
    local.get $l28
    f32.store offset=9916
    local.get $l15
    local.get $l27
    f32.store offset=9912
    local.get $l15
    local.get $l26
    f32.store offset=9908
    local.get $l15
    local.get $l24
    f32.store offset=9904
    local.get $l15
    i32.const 9900
    i32.add
    i32.const 0
    i32.store
    local.get $l15
    i32.const 9896
    i32.add
    local.get $l30
    f32.store
    local.get $l15
    i32.const 9892
    i32.add
    local.get $l29
    f32.store
    local.get $l15
    local.get $l25
    f32.store offset=9888
    local.get $l15
    local.get $l22
    f32.store offset=9884
    local.get $l15
    local.get $l20
    f32.store offset=9880
    local.get $l15
    local.get $l23
    f32.store offset=9876
    local.get $l15
    local.get $l21
    f32.store offset=9872
    local.get $l22
    local.get $l22
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $l34
    local.get $l33
    local.get $l25
    f32.sub
    local.tee $l25
    f32.mul
    local.get $l22
    local.get $l20
    local.get $l31
    local.get $l29
    f32.sub
    local.tee $l29
    f32.mul
    local.get $l23
    local.get $l32
    local.get $l30
    f32.sub
    local.tee $l30
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l21
    local.get $l29
    local.get $l23
    f32.neg
    local.tee $l35
    f32.mul
    local.get $l21
    local.get $l25
    f32.mul
    f32.sub
    local.get $l20
    local.get $l30
    f32.mul
    f32.sub
    local.tee $l31
    f32.mul
    f32.sub
    local.tee $l32
    local.get $l32
    f32.add
    local.set $l32
    local.get $l34
    local.get $l30
    f32.mul
    local.get $l22
    local.get $l23
    local.get $l25
    f32.mul
    local.get $l21
    local.get $l29
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l20
    local.get $l31
    f32.mul
    f32.sub
    local.tee $l33
    local.get $l33
    f32.add
    local.set $l33
    local.get $l34
    local.get $l29
    f32.mul
    local.get $l22
    local.get $l21
    local.get $l30
    f32.mul
    local.get $l20
    local.get $l25
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l23
    local.get $l31
    f32.mul
    f32.sub
    local.tee $l25
    local.get $l25
    f32.add
    local.set $l30
    local.get $p2
    f32.load
    local.set $l31
    block $B0
      block $B1
        local.get $l26
        local.get $l20
        f32.mul
        local.get $l27
        local.get $l23
        f32.mul
        f32.sub
        local.get $l24
        local.get $l22
        f32.mul
        local.get $l28
        local.get $l21
        f32.mul
        f32.sub
        f32.add
        local.tee $l29
        local.get $p13
        f32.load
        f32.mul
        local.get $l27
        local.get $l21
        f32.mul
        local.get $l24
        local.get $l20
        f32.mul
        f32.sub
        local.get $l26
        local.get $l22
        f32.mul
        local.get $l28
        local.get $l23
        f32.mul
        f32.sub
        f32.add
        local.tee $l25
        local.get $p13
        f32.load offset=4
        f32.mul
        f32.add
        local.get $l24
        local.get $l23
        f32.mul
        local.get $l26
        local.get $l21
        f32.mul
        f32.sub
        local.get $l27
        local.get $l22
        f32.mul
        local.get $l28
        local.get $l20
        f32.mul
        f32.sub
        f32.add
        local.tee $l23
        local.get $p13
        f32.load offset=8
        f32.mul
        f32.add
        local.get $l28
        local.get $l22
        f32.mul
        local.get $l26
        local.get $l35
        f32.mul
        local.get $l24
        local.get $l21
        f32.mul
        f32.sub
        local.get $l27
        local.get $l20
        f32.mul
        f32.sub
        f32.sub
        local.tee $l22
        local.get $p13
        f32.load offset=12
        f32.mul
        f32.add
        f32.const 0x1.ffe5cap-1 (;=0.9998;)
        f32.lt
        i32.eqz
        if $I2
          local.get $l31
          f32.const 0x1.99999ap-3 (;=0.2;)
          f32.mul
          local.get $l32
          local.get $p13
          f32.load offset=16
          f32.sub
          local.tee $l21
          local.get $l21
          f32.neg
          local.tee $l20
          local.get $l20
          local.get $l21
          f32.lt
          select
          local.tee $l21
          local.get $l30
          local.get $p13
          f32.load offset=20
          f32.sub
          local.tee $l20
          local.get $l20
          f32.neg
          local.tee $l24
          local.get $l20
          local.get $l24
          f32.gt
          select
          local.tee $l20
          local.get $l20
          local.get $l21
          f32.le
          select
          local.tee $l24
          local.get $l21
          f32.const 0x0p+0 (;=0;)
          local.get $l33
          local.get $p13
          f32.load offset=24
          f32.sub
          local.tee $l20
          local.get $l20
          f32.neg
          local.tee $l26
          local.get $l20
          local.get $l26
          f32.gt
          select
          f32.const 0x0p+0 (;=0;)
          f32.ge
          select
          local.tee $l21
          local.get $l21
          local.get $l24
          f32.le
          select
          f32.lt
          i32.eqz
          br_if $B1
        end
        local.get $l15
        local.get $l31
        f32.const 0x1.99999ap-5 (;=0.05;)
        f32.mul
        f32.store offset=9856
        local.get $p13
        i32.const 0
        i32.store offset=28
        local.get $p13
        local.get $l33
        f32.store offset=24
        local.get $p13
        local.get $l30
        f32.store offset=20
        local.get $p13
        local.get $l32
        f32.store offset=16
        local.get $p13
        local.get $l22
        f32.store offset=12
        local.get $p13
        local.get $l23
        f32.store offset=8
        local.get $p13
        local.get $l25
        f32.store offset=4
        local.get $p13
        local.get $l29
        f32.store
        local.get $p13
        i32.const 0
        i32.store8 offset=62
        local.get $p4
        i32.load offset=40
        local.set $p4
        local.get $l15
        i32.const 9836
        i32.add
        local.get $p5
        f32.load offset=4
        local.tee $l21
        local.get $l21
        f32.add
        local.tee $l23
        local.get $p5
        f32.load offset=8
        local.tee $l22
        f32.mul
        local.tee $l27
        local.get $p5
        f32.load
        local.tee $l24
        local.get $l24
        f32.add
        local.tee $l20
        local.get $p5
        f32.load offset=12
        local.tee $l26
        f32.mul
        local.tee $l28
        f32.sub
        f32.store
        local.get $l15
        i32.const 9828
        i32.add
        local.get $l27
        local.get $l28
        f32.add
        f32.store
        local.get $l15
        i32.const 9840
        i32.add
        f32.const 0x1p+0 (;=1;)
        local.get $l24
        local.get $l20
        f32.mul
        f32.sub
        local.tee $l24
        local.get $l21
        local.get $l23
        f32.mul
        local.tee $l27
        f32.sub
        f32.store
        local.get $l15
        i32.const 9824
        i32.add
        local.get $l24
        local.get $l22
        local.get $l22
        local.get $l22
        f32.add
        local.tee $l28
        f32.mul
        local.tee $l25
        f32.sub
        f32.store
        local.get $l15
        local.get $l20
        local.get $l22
        f32.mul
        local.tee $l22
        local.get $l23
        local.get $l26
        f32.mul
        local.tee $l23
        f32.add
        f32.store offset=9832
        local.get $l15
        local.get $l20
        local.get $l21
        f32.mul
        local.tee $l21
        local.get $l28
        local.get $l26
        f32.mul
        local.tee $l20
        f32.sub
        f32.store offset=9820
        local.get $l15
        local.get $l22
        local.get $l23
        f32.sub
        f32.store offset=9816
        local.get $l15
        local.get $l21
        local.get $l20
        f32.add
        f32.store offset=9812
        local.get $l15
        f32.const 0x1p+0 (;=1;)
        local.get $l27
        f32.sub
        local.get $l25
        f32.sub
        f32.store offset=9808
        local.get $l15
        local.get $p5
        f32.load offset=16
        f32.store offset=9844
        local.get $l15
        i32.const 9848
        i32.add
        local.get $l18
        f32.load
        f32.store
        local.get $l15
        i32.const 9852
        i32.add
        local.get $l19
        f32.load
        f32.store
        local.get $l15
        i32.const 9788
        i32.add
        local.get $p6
        f32.load offset=4
        local.tee $l21
        local.get $l21
        f32.add
        local.tee $l23
        local.get $p6
        f32.load offset=8
        local.tee $l22
        f32.mul
        local.tee $l27
        local.get $p6
        f32.load
        local.tee $l24
        local.get $l24
        f32.add
        local.tee $l20
        local.get $p6
        f32.load offset=12
        local.tee $l26
        f32.mul
        local.tee $l28
        f32.sub
        f32.store
        local.get $l15
        i32.const 9780
        i32.add
        local.get $l27
        local.get $l28
        f32.add
        f32.store
        local.get $l15
        i32.const 9792
        i32.add
        f32.const 0x1p+0 (;=1;)
        local.get $l24
        local.get $l20
        f32.mul
        f32.sub
        local.tee $l24
        local.get $l21
        local.get $l23
        f32.mul
        local.tee $l27
        f32.sub
        f32.store
        local.get $l15
        i32.const 9776
        i32.add
        local.get $l24
        local.get $l22
        local.get $l22
        local.get $l22
        f32.add
        local.tee $l28
        f32.mul
        local.tee $l25
        f32.sub
        f32.store
        local.get $l15
        local.get $l20
        local.get $l22
        f32.mul
        local.tee $l22
        local.get $l23
        local.get $l26
        f32.mul
        local.tee $l23
        f32.add
        f32.store offset=9784
        local.get $l15
        local.get $l20
        local.get $l21
        f32.mul
        local.tee $l21
        local.get $l28
        local.get $l26
        f32.mul
        local.tee $l20
        f32.sub
        f32.store offset=9772
        local.get $l15
        local.get $l22
        local.get $l23
        f32.sub
        f32.store offset=9768
        local.get $l15
        local.get $l21
        local.get $l20
        f32.add
        f32.store offset=9764
        local.get $l15
        f32.const 0x1p+0 (;=1;)
        local.get $l27
        f32.sub
        local.get $l25
        f32.sub
        f32.store offset=9760
        local.get $l15
        local.get $p6
        f32.load offset=16
        f32.store offset=9796
        local.get $l15
        i32.const 9800
        i32.add
        local.get $l16
        f32.load
        f32.store
        local.get $l15
        i32.const 9804
        i32.add
        local.get $l17
        f32.load
        f32.store
        local.get $l15
        i32.const 9696
        i32.add
        local.get $p3
        local.get $p7
        local.get $l15
        i32.const 9808
        i32.add
        local.get $l15
        i32.const 9760
        i32.add
        local.get $p10
        local.get $p12
        call $f69939
        local.get $l15
        i32.const 1
        i32.store8 offset=9680
        local.get $l15
        i64.const 4672924418048
        i64.store offset=9688
        local.get $l15
        local.get $l15
        i32.const 5328
        i32.add
        i32.store offset=9684
        local.get $p4
        i32.load offset=56
        local.set $p5
        local.get $l15
        i32.const 868
        i32.add
        local.tee $p6
        i32.const 0
        i32.store
        local.get $l15
        local.get $p12
        i32.store8 offset=16
        local.get $l15
        local.get $p5
        i32.store offset=12
        local.get $l15
        local.get $p10
        i32.store offset=8
        local.get $l15
        i32.const 3124204
        i32.store
        local.get $l15
        i32.const 2
        i32.store offset=4
        local.get $l15
        i32.const 880
        i32.add
        local.tee $p2
        local.get $l15
        i32.const 9936
        i32.add
        local.get $l15
        i32.const 9856
        i32.add
        local.get $l15
        i32.const 9904
        i32.add
        local.get $l15
        i32.const 9872
        i32.add
        local.get $p13
        local.get $p8
        local.get $l15
        i32.const 5328
        i32.add
        local.get $p14
        call $f70050
        local.set $p3
        local.get $l15
        i32.const 5276
        i32.add
        i32.const 0
        i32.store
        local.get $l15
        i32.const 5148
        i32.add
        i32.const 255
        i32.const 128
        call $f484
        drop
        local.get $l15
        i32.const 5309
        i32.add
        i32.const 1
        i32.store8
        local.get $l15
        i32.const 5308
        i32.add
        local.get $p11
        i32.store8
        local.get $l15
        i32.const 5304
        i32.add
        local.get $p9
        i32.store
        local.get $l15
        i32.const 5300
        i32.add
        local.get $p1
        i32.store
        local.get $l15
        i32.const 5296
        i32.add
        local.get $p0
        i32.store
        local.get $p0
        f32.load offset=8
        local.set $l20
        local.get $p0
        f32.load
        local.set $l22
        local.get $p0
        f32.load offset=4
        local.set $l21
        local.get $l15
        i32.const 5292
        i32.add
        i32.const 0
        i32.store
        local.get $l15
        i32.const 5288
        i32.add
        local.get $l22
        local.get $l15
        i32.const 3184
        i32.add
        f32.load
        f32.sub
        local.tee $l22
        local.get $l15
        i32.const 3168
        i32.add
        f32.load
        f32.mul
        local.get $l21
        local.get $l15
        i32.const 3188
        i32.add
        f32.load
        f32.sub
        local.tee $l21
        local.get $l15
        i32.const 3172
        i32.add
        f32.load
        f32.mul
        f32.add
        local.get $l20
        local.get $l15
        i32.const 3192
        i32.add
        f32.load
        f32.sub
        local.tee $l20
        local.get $l15
        i32.const 3176
        i32.add
        f32.load
        f32.mul
        f32.add
        f32.store
        local.get $l15
        i32.const 5284
        i32.add
        local.get $l22
        local.get $l15
        i32.const 3152
        i32.add
        f32.load
        f32.mul
        local.get $l21
        local.get $l15
        i32.const 3156
        i32.add
        f32.load
        f32.mul
        f32.add
        local.get $l20
        local.get $l15
        i32.const 3160
        i32.add
        f32.load
        f32.mul
        f32.add
        f32.store
        local.get $l15
        i32.const 5280
        i32.add
        local.get $l22
        local.get $l15
        i32.const 3136
        i32.add
        f32.load
        f32.mul
        local.get $l21
        local.get $l15
        i32.const 3140
        i32.add
        f32.load
        f32.mul
        f32.add
        local.get $l20
        local.get $l15
        i32.const 3144
        i32.add
        f32.load
        f32.mul
        f32.add
        f32.store
        local.get $l15
        local.get $l15
        i32.const 9696
        i32.add
        i32.store offset=5312
        local.get $p4
        local.get $l15
        i32.const 9696
        i32.add
        local.get $l15
        i32.const 1
        i32.const 1
        local.get $p4
        i32.load16_u offset=4
        i32.const 2
        i32.shl
        i32.const 3124176
        i32.add
        i32.load
        call_indirect $__indirect_function_table (type $t6)
        local.get $p6
        i32.load
        local.tee $p12
        if $I3
          local.get $l15
          i32.const 20
          i32.add
          local.set $p5
          local.get $l15
          i32.const 596
          i32.add
          local.set $p6
          local.get $l15
          i32.const 788
          i32.add
          local.set $p0
          local.get $l15
          i32.const 852
          i32.add
          local.set $p10
          loop $L4
            local.get $p2
            local.get $p5
            local.get $p0
            i32.load
            local.get $p10
            i32.load8_u
            local.get $p6
            call $f70056
            local.get $p10
            i32.const 1
            i32.add
            local.set $p10
            local.get $p0
            i32.const 4
            i32.add
            local.set $p0
            local.get $p6
            i32.const 12
            i32.add
            local.set $p6
            local.get $p5
            i32.const 36
            i32.add
            local.set $p5
            local.get $p12
            i32.const 1
            i32.sub
            local.tee $p12
            br_if $L4
          end
          local.get $l15
          i32.const 0
          i32.store offset=868
        end
        local.get $p2
        call $f70054
        local.get $p3
        i32.const 6
        i32.const 0
        call $f70051
        local.get $l15
        i32.load offset=9692
        local.tee $p5
        i32.const 0
        i32.lt_s
        br_if $B0
        local.get $p5
        i32.const 2147483647
        i32.and
        i32.eqz
        br_if $B0
        local.get $l15
        i32.load offset=9684
        local.tee $p5
        local.get $l15
        i32.const 5328
        i32.add
        i32.eq
        br_if $B0
        local.get $p5
        i32.eqz
        br_if $B0
        call $f69753
        local.tee $p6
        local.get $p5
        local.get $p6
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
        br $B0
      end
      i32.const 0
      local.set $p5
      local.get $l15
      i32.const 0
      i32.store offset=60
      local.get $l15
      local.get $l33
      f32.store offset=56
      local.get $l15
      local.get $l30
      f32.store offset=52
      local.get $l15
      i32.const 0
      i32.store offset=44
      local.get $l15
      i32.const 0
      i32.store offset=28
      local.get $l15
      local.get $l23
      local.get $l25
      local.get $l25
      f32.add
      local.tee $l20
      f32.mul
      local.tee $l24
      local.get $l22
      local.get $l29
      local.get $l29
      f32.add
      local.tee $l21
      f32.mul
      local.tee $l26
      f32.sub
      f32.store offset=36
      local.get $l15
      local.get $l24
      local.get $l26
      f32.add
      f32.store offset=24
      local.get $l15
      f32.const 0x1p+0 (;=1;)
      local.get $l29
      local.get $l21
      f32.mul
      f32.sub
      local.tee $l24
      local.get $l25
      local.get $l20
      f32.mul
      local.tee $l26
      f32.sub
      f32.store offset=40
      local.get $l15
      local.get $l24
      local.get $l23
      local.get $l23
      local.get $l23
      f32.add
      local.tee $l27
      f32.mul
      local.tee $l28
      f32.sub
      f32.store offset=20
      local.get $l15
      local.get $l32
      f32.store offset=48
      local.get $l15
      i32.const 0
      i32.store offset=12
      local.get $l15
      local.get $l23
      local.get $l21
      f32.mul
      local.tee $l23
      local.get $l22
      local.get $l20
      f32.mul
      local.tee $l20
      f32.add
      f32.store offset=32
      local.get $l15
      local.get $l25
      local.get $l21
      f32.mul
      local.tee $l21
      local.get $l22
      local.get $l27
      f32.mul
      local.tee $l22
      f32.sub
      f32.store offset=16
      local.get $l15
      local.get $l23
      local.get $l20
      f32.sub
      f32.store offset=8
      local.get $l15
      local.get $l21
      local.get $l22
      f32.add
      f32.store offset=4
      local.get $l15
      f32.const 0x1p+0 (;=1;)
      local.get $l26
      f32.sub
      local.get $l28
      f32.sub
      f32.store
      local.get $l15
      local.get $l31
      f32.const 0x1.99999ap-1 (;=0.8;)
      f32.mul
      f32.store offset=9696
      local.get $p13
      i32.load8_u offset=62
      i32.eqz
      br_if $B0
      loop $L5
        local.get $l15
        i32.const 5328
        i32.add
        local.get $p13
        local.get $p5
        local.get $p13
        i32.add
        i32.const 56
        i32.add
        local.tee $p10
        i32.load8_u
        local.tee $p0
        i32.const 400
        i32.mul
        i32.add
        local.tee $p6
        i32.const -64
        i32.sub
        local.get $l15
        local.get $l15
        i32.const 9696
        i32.add
        call $f69978
        block $B6
          local.get $p6
          i32.load offset=448
          i32.eqz
          if $I7
            local.get $p13
            local.get $p13
            i32.load8_u offset=62
            i32.const 1
            i32.sub
            local.tee $p6
            i32.store8 offset=62
            local.get $p13
            local.get $p6
            i32.const 255
            i32.and
            i32.add
            i32.const 56
            i32.add
            local.tee $p6
            i32.load8_u
            local.set $p12
            local.get $p6
            local.get $p0
            i32.store8
            local.get $p10
            local.get $p12
            i32.store8
            local.get $p5
            i32.const 1
            i32.sub
            local.set $p5
            br $B6
          end
          local.get $p13
          local.get $p0
          i32.const 2
          i32.shl
          i32.add
          local.get $l15
          f32.load offset=5328
          f32.store offset=32
        end
        local.get $p5
        i32.const 1
        i32.add
        local.tee $p5
        local.get $p13
        i32.load8_u offset=62
        i32.lt_u
        br_if $L5
      end
    end
    local.get $p13
    local.get $p8
    local.get $l15
    i32.const 9872
    i32.add
    call $f69979
    local.set $p13
    local.get $l15
    i32.const 9952
    i32.add
    global.set $g0
    local.get $p13)
