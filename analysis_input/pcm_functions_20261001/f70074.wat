  (func $f70074 (type $t490) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 f32) (param $p8 i32) (param $p9 i32) (param $p10 i32) (param $p11 i32) (param $p12 i32) (result i32)
    (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32)
    global.get $g0
    i32.const 9008
    i32.sub
    local.tee $l13
    global.set $g0
    local.get $p6
    i32.const 20
    i32.add
    local.tee $l14
    f32.load
    local.set $l25
    local.get $p6
    i32.const 24
    i32.add
    local.tee $l15
    f32.load
    local.set $l26
    local.get $p5
    i32.const 20
    i32.add
    local.tee $l16
    f32.load
    local.set $l27
    local.get $p5
    i32.const 24
    i32.add
    local.tee $l17
    f32.load
    local.set $l30
    local.get $p6
    f32.load
    local.set $l19
    local.get $p6
    f32.load offset=4
    local.set $l21
    local.get $p6
    f32.load offset=8
    local.set $l18
    local.get $p6
    f32.load offset=12
    local.set $l20
    local.get $p6
    f32.load offset=16
    local.set $l22
    local.get $p5
    f32.load
    local.set $l23
    local.get $p5
    f32.load offset=4
    local.set $l24
    local.get $p5
    f32.load offset=8
    local.set $l28
    local.get $p5
    f32.load offset=12
    local.set $l29
    local.get $p5
    f32.load offset=16
    local.set $l31
    local.get $l13
    local.get $p7
    f32.store offset=8992
    local.get $l13
    i32.const 8988
    i32.add
    i32.const 0
    i32.store
    local.get $l13
    i32.const 8984
    i32.add
    local.get $l30
    f32.store
    local.get $l13
    i32.const 8980
    i32.add
    local.get $l27
    f32.store
    local.get $l13
    local.get $l31
    f32.store offset=8976
    local.get $l13
    local.get $l29
    f32.store offset=8972
    local.get $l13
    local.get $l28
    f32.store offset=8968
    local.get $l13
    local.get $l24
    f32.store offset=8964
    local.get $l13
    local.get $l23
    f32.store offset=8960
    local.get $l13
    i32.const 8956
    i32.add
    i32.const 0
    i32.store
    local.get $l13
    i32.const 8952
    i32.add
    local.get $l26
    f32.store
    local.get $l13
    i32.const 8948
    i32.add
    local.get $l25
    f32.store
    local.get $l13
    local.get $l22
    f32.store offset=8944
    local.get $l13
    local.get $l20
    f32.store offset=8940
    local.get $l13
    local.get $l18
    f32.store offset=8936
    local.get $l13
    local.get $l21
    f32.store offset=8932
    local.get $l13
    local.get $l19
    f32.store offset=8928
    local.get $l20
    local.get $l20
    f32.mul
    f32.const -0x1p-1 (;=-0.5;)
    f32.add
    local.tee $p7
    local.get $l31
    local.get $l22
    f32.sub
    local.tee $l22
    f32.mul
    local.get $l20
    local.get $l18
    local.get $l27
    local.get $l25
    f32.sub
    local.tee $l25
    f32.mul
    local.get $l21
    local.get $l30
    local.get $l26
    f32.sub
    local.tee $l26
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l19
    local.get $l25
    local.get $l21
    f32.neg
    local.tee $l32
    f32.mul
    local.get $l19
    local.get $l22
    f32.mul
    f32.sub
    local.get $l18
    local.get $l26
    f32.mul
    f32.sub
    local.tee $l27
    f32.mul
    f32.sub
    local.tee $l30
    local.get $l30
    f32.add
    local.set $l30
    local.get $p7
    local.get $l26
    f32.mul
    local.get $l20
    local.get $l21
    local.get $l22
    f32.mul
    local.get $l19
    local.get $l25
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l18
    local.get $l27
    f32.mul
    f32.sub
    local.tee $l31
    local.get $l31
    f32.add
    local.set $l31
    local.get $p7
    local.get $l25
    f32.mul
    local.get $l20
    local.get $l19
    local.get $l26
    f32.mul
    local.get $l18
    local.get $l22
    f32.mul
    f32.sub
    f32.mul
    f32.add
    local.get $l21
    local.get $l27
    f32.mul
    f32.sub
    local.tee $l22
    local.get $l22
    f32.add
    local.set $l26
    local.get $p2
    f32.load
    local.set $l27
    block $B0
      block $B1
        local.get $l24
        local.get $l18
        f32.mul
        local.get $l28
        local.get $l21
        f32.mul
        f32.sub
        local.get $l23
        local.get $l20
        f32.mul
        local.get $l29
        local.get $l19
        f32.mul
        f32.sub
        f32.add
        local.tee $l25
        local.get $p11
        f32.load
        f32.mul
        local.get $l28
        local.get $l19
        f32.mul
        local.get $l23
        local.get $l18
        f32.mul
        f32.sub
        local.get $l24
        local.get $l20
        f32.mul
        local.get $l29
        local.get $l21
        f32.mul
        f32.sub
        f32.add
        local.tee $l22
        local.get $p11
        f32.load offset=4
        f32.mul
        f32.add
        local.get $l23
        local.get $l21
        f32.mul
        local.get $l24
        local.get $l19
        f32.mul
        f32.sub
        local.get $l28
        local.get $l20
        f32.mul
        local.get $l29
        local.get $l18
        f32.mul
        f32.sub
        f32.add
        local.tee $l21
        local.get $p11
        f32.load offset=8
        f32.mul
        f32.add
        local.get $l29
        local.get $l20
        f32.mul
        local.get $l24
        local.get $l32
        f32.mul
        local.get $l23
        local.get $l19
        f32.mul
        f32.sub
        local.get $l28
        local.get $l18
        f32.mul
        f32.sub
        f32.sub
        local.tee $l20
        local.get $p11
        f32.load offset=12
        f32.mul
        f32.add
        f32.const 0x1.ffe5cap-1 (;=0.9998;)
        f32.lt
        i32.eqz
        if $I2
          local.get $l27
          f32.const 0x1.99999ap-3 (;=0.2;)
          f32.mul
          local.get $l30
          local.get $p11
          f32.load offset=16
          f32.sub
          local.tee $l19
          local.get $l19
          f32.neg
          local.tee $l18
          local.get $l18
          local.get $l19
          f32.lt
          select
          local.tee $l19
          local.get $l26
          local.get $p11
          f32.load offset=20
          f32.sub
          local.tee $l18
          local.get $l18
          f32.neg
          local.tee $l23
          local.get $l18
          local.get $l23
          f32.gt
          select
          local.tee $l18
          local.get $l18
          local.get $l19
          f32.le
          select
          local.tee $l23
          local.get $l19
          f32.const 0x0p+0 (;=0;)
          local.get $l31
          local.get $p11
          f32.load offset=24
          f32.sub
          local.tee $l18
          local.get $l18
          f32.neg
          local.tee $l24
          local.get $l18
          local.get $l24
          f32.gt
          select
          f32.const 0x0p+0 (;=0;)
          f32.ge
          select
          local.tee $l19
          local.get $l19
          local.get $l23
          f32.le
          select
          f32.lt
          i32.eqz
          br_if $B1
        end
        local.get $l13
        local.get $l27
        f32.const 0x1.99999ap-5 (;=0.05;)
        f32.mul
        f32.store offset=8912
        local.get $p11
        i32.const 0
        i32.store offset=28
        local.get $p11
        local.get $l31
        f32.store offset=24
        local.get $p11
        local.get $l26
        f32.store offset=20
        local.get $p11
        local.get $l30
        f32.store offset=16
        local.get $p11
        local.get $l20
        f32.store offset=12
        local.get $p11
        local.get $l21
        f32.store offset=8
        local.get $p11
        local.get $l22
        f32.store offset=4
        local.get $p11
        local.get $l25
        f32.store
        local.get $p11
        i32.const 0
        i32.store8 offset=62
        local.get $p5
        f32.load offset=8
        local.set $l23
        local.get $p5
        f32.load offset=4
        local.set $l24
        local.get $p5
        f32.load
        local.set $l28
        local.get $p5
        f32.load offset=12
        local.set $l29
        local.get $l13
        i32.const 8904
        i32.add
        local.get $p6
        f32.load offset=12
        local.tee $l20
        local.get $l20
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.tee $l27
        local.get $l17
        f32.load
        local.get $l15
        f32.load
        f32.sub
        local.tee $l19
        local.get $l19
        f32.add
        local.tee $l22
        f32.mul
        local.get $l20
        local.get $p6
        f32.load offset=4
        local.tee $l19
        local.get $p5
        f32.load offset=16
        local.get $p6
        f32.load offset=16
        f32.sub
        local.tee $l18
        local.get $l18
        f32.add
        local.tee $l25
        f32.mul
        local.get $p6
        f32.load
        local.tee $l18
        local.get $l16
        f32.load
        local.get $l14
        f32.load
        f32.sub
        local.tee $l21
        local.get $l21
        f32.add
        local.tee $l26
        f32.mul
        f32.sub
        f32.mul
        f32.add
        local.get $p6
        f32.load offset=8
        local.tee $l21
        local.get $l26
        local.get $l19
        f32.neg
        f32.mul
        local.get $l18
        local.get $l25
        f32.mul
        f32.sub
        local.get $l21
        local.get $l22
        f32.mul
        f32.sub
        local.tee $l30
        f32.mul
        f32.sub
        f32.store
        local.get $l13
        i32.const 8900
        i32.add
        local.get $l27
        local.get $l26
        f32.mul
        local.get $l20
        local.get $l18
        local.get $l22
        f32.mul
        local.get $l21
        local.get $l25
        f32.mul
        f32.sub
        f32.mul
        f32.add
        local.get $l19
        local.get $l30
        f32.mul
        f32.sub
        f32.store
        local.get $l13
        local.get $l21
        local.get $l23
        f32.mul
        local.get $l18
        local.get $l28
        f32.mul
        local.get $l20
        local.get $l29
        f32.mul
        f32.add
        local.get $l19
        local.get $l24
        f32.mul
        f32.add
        f32.add
        f32.store offset=8892
        local.get $l13
        local.get $l19
        local.get $l28
        f32.mul
        local.get $l20
        local.get $l23
        f32.mul
        local.get $l21
        local.get $l29
        f32.mul
        f32.sub
        local.get $l18
        local.get $l24
        f32.mul
        f32.sub
        f32.add
        f32.store offset=8888
        local.get $l13
        local.get $l18
        local.get $l23
        f32.mul
        local.get $l20
        local.get $l24
        f32.mul
        local.get $l19
        local.get $l29
        f32.mul
        f32.sub
        local.get $l21
        local.get $l28
        f32.mul
        f32.sub
        f32.add
        f32.store offset=8884
        local.get $l13
        local.get $l20
        local.get $l28
        f32.mul
        local.get $l18
        local.get $l29
        f32.mul
        f32.sub
        local.get $l19
        local.get $l23
        f32.mul
        f32.sub
        local.get $l21
        local.get $l24
        f32.mul
        f32.add
        f32.store offset=8880
        local.get $l13
        local.get $l27
        local.get $l25
        f32.mul
        local.get $l20
        local.get $l21
        local.get $l26
        f32.mul
        local.get $l19
        local.get $l22
        f32.mul
        f32.sub
        f32.mul
        f32.add
        local.get $l18
        local.get $l30
        f32.mul
        f32.sub
        f32.store offset=8896
        local.get $p4
        i32.load offset=4
        local.set $p5
        local.get $l13
        local.get $p4
        i32.store offset=8872
        local.get $l13
        local.get $p5
        i32.store offset=8868
        local.get $l13
        f32.const 0x1p+0 (;=1;)
        local.get $p4
        f32.load offset=8
        f32.div
        f32.store offset=8860
        local.get $l13
        f32.const 0x1p+0 (;=1;)
        local.get $p4
        f32.load offset=12
        f32.div
        f32.store offset=8856
        local.get $l13
        f32.const 0x1p+0 (;=1;)
        local.get $p4
        f32.load offset=16
        f32.div
        f32.store offset=8864
        local.get $l13
        i64.const 4672924418048
        i64.store offset=8840
        local.get $l13
        local.get $l13
        i32.const 4480
        i32.add
        i32.store offset=8836
        local.get $l13
        i32.const 1
        i32.store8 offset=8832
        local.get $l13
        i32.const 24
        i32.add
        local.get $p5
        local.get $p5
        i32.load
        i32.load offset=52
        call_indirect $__indirect_function_table (type $t1)
        local.get $l13
        local.get $p6
        i32.store offset=40
        local.get $l13
        i32.const 3124380
        i32.store offset=32
        local.get $l13
        local.get $l13
        i32.const 8856
        i32.add
        i32.store offset=36
        local.get $l13
        i32.load8_u offset=24
        local.set $p4
        local.get $l13
        local.get $p5
        local.get $p5
        i32.load
        i32.load offset=52
        call_indirect $__indirect_function_table (type $t1)
        local.get $l13
        local.get $l13
        i32.load8_u
        i32.const -1
        i32.xor
        i32.const 1
        i32.and
        i32.store8 offset=44
        local.get $l13
        i32.const 3124360
        i32.store offset=32
        local.get $l13
        i32.const 48
        i32.add
        local.tee $p5
        local.get $l13
        i32.const 8992
        i32.add
        local.get $l13
        i32.const 8912
        i32.add
        local.get $l13
        i32.const 8960
        i32.add
        local.get $l13
        i32.const 8928
        i32.add
        local.get $p11
        local.get $p8
        local.get $l13
        i32.const 4480
        i32.add
        local.get $p12
        call $f70050
        local.set $p2
        local.get $l13
        i32.const 4444
        i32.add
        i32.const 0
        i32.store
        local.get $l13
        i32.const 4316
        i32.add
        i32.const 255
        i32.const 128
        call $f484
        drop
        local.get $l13
        i32.const 4477
        i32.add
        local.get $p4
        i32.const -1
        i32.xor
        i32.const 1
        i32.and
        i32.store8
        local.get $l13
        i32.const 4476
        i32.add
        local.get $p10
        i32.store8
        local.get $l13
        i32.const 4472
        i32.add
        local.get $p9
        i32.store
        local.get $l13
        i32.const 4468
        i32.add
        local.get $p1
        i32.store
        local.get $l13
        i32.const 4464
        i32.add
        local.get $p0
        i32.store
        local.get $p0
        f32.load offset=8
        local.set $l18
        local.get $p0
        f32.load
        local.set $l20
        local.get $p0
        f32.load offset=4
        local.set $l19
        local.get $l13
        i32.const 4460
        i32.add
        i32.const 0
        i32.store
        local.get $l13
        i32.const 4456
        i32.add
        local.get $l20
        local.get $l13
        i32.const 2352
        i32.add
        f32.load
        f32.sub
        local.tee $l20
        local.get $l13
        i32.const 2336
        i32.add
        f32.load
        f32.mul
        local.get $l19
        local.get $l13
        i32.const 2356
        i32.add
        f32.load
        f32.sub
        local.tee $l19
        local.get $l13
        i32.const 2340
        i32.add
        f32.load
        f32.mul
        f32.add
        local.get $l18
        local.get $l13
        i32.const 2360
        i32.add
        f32.load
        f32.sub
        local.tee $l18
        local.get $l13
        i32.const 2344
        i32.add
        f32.load
        f32.mul
        f32.add
        f32.store
        local.get $l13
        i32.const 4452
        i32.add
        local.get $l20
        local.get $l13
        i32.const 2320
        i32.add
        f32.load
        f32.mul
        local.get $l19
        local.get $l13
        i32.const 2324
        i32.add
        f32.load
        f32.mul
        f32.add
        local.get $l18
        local.get $l13
        i32.const 2328
        i32.add
        f32.load
        f32.mul
        f32.add
        f32.store
        local.get $l13
        i32.const 4448
        i32.add
        local.get $l20
        local.get $l13
        i32.const 2304
        i32.add
        f32.load
        f32.mul
        local.get $l19
        local.get $l13
        i32.const 2308
        i32.add
        f32.load
        f32.mul
        f32.add
        local.get $l18
        local.get $l13
        i32.const 2312
        i32.add
        f32.load
        f32.mul
        f32.add
        f32.store
        local.get $l13
        local.get $l13
        i32.const 8880
        i32.add
        local.get $p3
        call $f70451
        local.get $l13
        i32.const 8856
        i32.add
        local.get $p6
        local.get $l13
        i32.const 0
        local.get $l13
        i32.const 32
        i32.add
        call $f70450
        local.get $p5
        call $f70054
        local.get $p2
        i32.const 6
        i32.const 0
        call $f70051
        local.get $l13
        i32.load offset=8844
        local.tee $p6
        i32.const 0
        i32.lt_s
        br_if $B0
        local.get $p6
        i32.const 2147483647
        i32.and
        i32.eqz
        br_if $B0
        local.get $l13
        i32.load offset=8836
        local.tee $p6
        local.get $l13
        i32.const 4480
        i32.add
        i32.eq
        br_if $B0
        local.get $p6
        i32.eqz
        br_if $B0
        call $f69753
        local.tee $p5
        local.get $p6
        local.get $p5
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
        br $B0
      end
      i32.const 0
      local.set $p6
      local.get $l13
      i32.const 0
      i32.store offset=92
      local.get $l13
      local.get $l31
      f32.store offset=88
      local.get $l13
      local.get $l26
      f32.store offset=84
      local.get $l13
      i32.const 0
      i32.store offset=76
      local.get $l13
      i32.const 0
      i32.store offset=60
      local.get $l13
      local.get $l21
      local.get $l22
      local.get $l22
      f32.add
      local.tee $l18
      f32.mul
      local.tee $l23
      local.get $l20
      local.get $l25
      local.get $l25
      f32.add
      local.tee $l19
      f32.mul
      local.tee $l24
      f32.sub
      f32.store offset=68
      local.get $l13
      local.get $l23
      local.get $l24
      f32.add
      f32.store offset=56
      local.get $l13
      f32.const 0x1p+0 (;=1;)
      local.get $l25
      local.get $l19
      f32.mul
      f32.sub
      local.tee $l23
      local.get $l22
      local.get $l18
      f32.mul
      local.tee $l24
      f32.sub
      f32.store offset=72
      local.get $l13
      local.get $l23
      local.get $l21
      local.get $l21
      local.get $l21
      f32.add
      local.tee $l28
      f32.mul
      local.tee $l29
      f32.sub
      f32.store offset=52
      local.get $l13
      local.get $l30
      f32.store offset=80
      local.get $l13
      i32.const 0
      i32.store offset=44
      local.get $l13
      local.get $l21
      local.get $l19
      f32.mul
      local.tee $l21
      local.get $l20
      local.get $l18
      f32.mul
      local.tee $l18
      f32.add
      f32.store offset=64
      local.get $l13
      local.get $l22
      local.get $l19
      f32.mul
      local.tee $l19
      local.get $l20
      local.get $l28
      f32.mul
      local.tee $l20
      f32.sub
      f32.store offset=48
      local.get $l13
      local.get $l21
      local.get $l18
      f32.sub
      f32.store offset=40
      local.get $l13
      local.get $l19
      local.get $l20
      f32.add
      f32.store offset=36
      local.get $l13
      f32.const 0x1p+0 (;=1;)
      local.get $l24
      f32.sub
      local.get $l29
      f32.sub
      f32.store offset=32
      local.get $l13
      local.get $l27
      f32.const 0x1.333334p-1 (;=0.6;)
      f32.mul
      f32.store offset=8880
      local.get $p11
      i32.load8_u offset=62
      i32.eqz
      br_if $B0
      loop $L3
        local.get $l13
        i32.const 4480
        i32.add
        local.get $p11
        local.get $p6
        local.get $p11
        i32.add
        i32.const 56
        i32.add
        local.tee $p0
        i32.load8_u
        local.tee $p4
        i32.const 400
        i32.mul
        i32.add
        local.tee $p5
        i32.const -64
        i32.sub
        local.get $l13
        i32.const 32
        i32.add
        local.get $l13
        i32.const 8880
        i32.add
        call $f69978
        block $B4
          local.get $p5
          i32.load offset=448
          i32.eqz
          if $I5
            local.get $p11
            local.get $p11
            i32.load8_u offset=62
            i32.const 1
            i32.sub
            local.tee $p5
            i32.store8 offset=62
            local.get $p11
            local.get $p5
            i32.const 255
            i32.and
            i32.add
            i32.const 56
            i32.add
            local.tee $p5
            i32.load8_u
            local.set $p2
            local.get $p5
            local.get $p4
            i32.store8
            local.get $p0
            local.get $p2
            i32.store8
            local.get $p6
            i32.const 1
            i32.sub
            local.set $p6
            br $B4
          end
          local.get $p11
          local.get $p4
          i32.const 2
          i32.shl
          i32.add
          local.get $l13
          f32.load offset=4480
          f32.store offset=32
        end
        local.get $p6
        i32.const 1
        i32.add
        local.tee $p6
        local.get $p11
        i32.load8_u offset=62
        i32.lt_u
        br_if $L3
      end
    end
    local.get $p11
    local.get $p8
    local.get $l13
    i32.const 8928
    i32.add
    call $f69979
    local.set $p11
    local.get $l13
    i32.const 9008
    i32.add
    global.set $g0
    local.get $p11)
