  (func $f70484 (type $t171) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 f32) (param $p7 i32) (param $p8 i32) (param $p9 f32) (param $p10 i32) (param $p11 f32) (result f32)
    (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32)
    global.get $g0
    i32.const 1536
    i32.sub
    local.tee $l12
    global.set $g0
    local.get $l12
    i32.const 1416
    i32.add
    local.get $p1
    i32.load
    local.tee $l17
    i32.const 4
    i32.add
    local.tee $l13
    local.get $l17
    i32.const 16
    i32.add
    call $f70485
    local.get $p4
    f32.load offset=24
    local.set $p9
    local.get $p2
    f32.load offset=24
    local.set $l27
    local.get $p4
    f32.load offset=16
    local.set $l29
    local.get $p2
    f32.load offset=16
    local.set $l28
    local.get $l12
    local.get $p2
    f32.load offset=20
    local.get $p4
    f32.load offset=20
    f32.sub
    local.tee $l31
    f32.store offset=1404
    local.get $l12
    local.get $l27
    local.get $p9
    f32.sub
    local.tee $p9
    f32.store offset=1408
    local.get $l12
    local.get $l28
    local.get $l29
    f32.sub
    local.tee $l27
    f32.store offset=1400
    local.get $p5
    f32.load offset=20
    local.set $l29
    local.get $p3
    f32.load offset=20
    local.set $l28
    local.get $p5
    f32.load offset=16
    local.set $l30
    local.get $p3
    f32.load offset=16
    local.set $l33
    local.get $l12
    local.get $p3
    f32.load offset=24
    local.get $p5
    f32.load offset=24
    f32.sub
    local.tee $l32
    f32.store offset=1392
    local.get $l12
    local.get $l28
    local.get $l29
    f32.sub
    local.tee $l29
    f32.store offset=1388
    local.get $l12
    local.get $l33
    local.get $l30
    f32.sub
    local.tee $l28
    f32.store offset=1384
    local.get $l12
    local.get $p9
    local.get $l32
    f32.sub
    local.tee $l36
    f32.store offset=1376
    local.get $l12
    local.get $l31
    local.get $l29
    f32.sub
    local.tee $l35
    f32.store offset=1372
    local.get $l12
    local.get $l27
    local.get $l28
    f32.sub
    local.tee $l37
    f32.store offset=1368
    local.get $l37
    local.get $l37
    f32.mul
    local.get $l35
    local.get $l35
    f32.mul
    f32.add
    local.get $l36
    local.get $l36
    f32.mul
    f32.add
    f32.sqrt
    local.tee $p9
    f32.const 0x0p+0 (;=0;)
    f32.gt
    if $I0
      local.get $l12
      local.get $l36
      f32.const 0x1p+0 (;=1;)
      local.get $p9
      f32.div
      local.tee $l27
      f32.mul
      f32.store offset=1376
      local.get $l12
      local.get $l35
      local.get $l27
      f32.mul
      f32.store offset=1372
      local.get $l12
      local.get $l37
      local.get $l27
      f32.mul
      f32.store offset=1368
    end
    local.get $l12
    i32.const 1360
    i32.add
    i32.const 1065353216
    i32.store
    local.get $l12
    i32.const 1344
    i32.add
    i64.const 1065353216
    i64.store
    local.get $l12
    i64.const 0
    i64.store offset=1352
    local.get $l12
    i64.const 0
    i64.store offset=1336
    local.get $l12
    i64.const 1065353216
    i64.store offset=1328
    local.get $l12
    i32.const 1264
    i32.add
    local.get $p0
    i32.const -64
    i32.sub
    local.get $p0
    i32.const 76
    i32.add
    local.get $l12
    i32.const 1328
    i32.add
    local.get $l12
    i32.const 1368
    i32.add
    local.get $p9
    call $f70395
    local.get $l12
    i32.const 1256
    i32.add
    block $B1 (result f32)
      block $B2
        local.get $l13
        f32.load
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B2
        local.get $l17
        f32.load offset=8
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B2
        local.get $l17
        f32.load offset=12
        f32.const 0x1p+0 (;=1;)
        f32.ne
        br_if $B2
        local.get $l12
        local.get $p3
        f32.load offset=24
        f32.const -0x1p+1 (;=-2;)
        f32.mul
        local.tee $l31
        local.get $p3
        f32.load offset=12
        local.tee $p9
        local.get $p9
        f32.mul
        f32.const -0x1p-1 (;=-0.5;)
        f32.add
        local.tee $l32
        f32.mul
        local.get $p9
        local.get $p3
        f32.load offset=20
        f32.const -0x1p+1 (;=-2;)
        f32.mul
        local.tee $l30
        local.get $p3
        f32.load
        local.tee $l27
        f32.mul
        local.get $p3
        f32.load offset=16
        f32.const -0x1p+1 (;=-2;)
        f32.mul
        local.tee $l33
        local.get $p3
        f32.load offset=4
        local.tee $l29
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        local.get $p3
        f32.load offset=8
        local.tee $l28
        local.get $l33
        local.get $l27
        f32.mul
        local.get $l30
        local.get $l29
        f32.mul
        f32.add
        local.get $l31
        local.get $l28
        f32.mul
        f32.add
        local.tee $l34
        f32.mul
        f32.add
        f32.store offset=632
        local.get $l12
        local.get $l29
        local.get $l34
        f32.mul
        local.get $l30
        local.get $l32
        f32.mul
        local.get $p9
        local.get $l33
        local.get $l28
        f32.mul
        local.get $l31
        local.get $l27
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        f32.store offset=628
        local.get $l12
        local.get $p9
        f32.store offset=620
        local.get $l12
        local.get $l28
        f32.neg
        f32.store offset=616
        local.get $l12
        local.get $l29
        f32.neg
        f32.store offset=612
        local.get $l12
        local.get $l27
        f32.neg
        f32.store offset=608
        local.get $l12
        local.get $l27
        local.get $l34
        f32.mul
        local.get $l33
        local.get $l32
        f32.mul
        local.get $p9
        local.get $l31
        local.get $l29
        f32.mul
        local.get $l30
        local.get $l28
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        f32.store offset=624
        local.get $l12
        i32.const 928
        i32.add
        local.get $l12
        i32.const 1264
        i32.add
        local.get $l12
        i32.const 608
        i32.add
        call $f70486
        local.get $l12
        i32.const 1220
        i32.add
        local.get $l12
        i64.load offset=948 align=4
        i64.store align=4
        local.get $l12
        i32.const 1228
        i32.add
        local.get $l12
        i64.load offset=956 align=4
        i64.store align=4
        local.get $l12
        i32.const 1244
        i32.add
        local.get $l12
        f32.load offset=972
        f32.store
        local.get $l12
        local.get $l12
        f32.load offset=928
        f32.store offset=1200
        local.get $l12
        local.get $l12
        i64.load offset=932 align=4
        i64.store offset=1204 align=4
        local.get $l12
        local.get $l12
        i64.load offset=940 align=4
        i64.store offset=1212 align=4
        local.get $l12
        local.get $l12
        i64.load offset=964 align=4
        i64.store offset=1236 align=4
        local.get $l12
        f32.load offset=980
        local.set $l27
        local.get $l12
        f32.load offset=976
        local.set $l29
        local.get $l12
        f32.load offset=984
        br $B1
      end
      local.get $l12
      i32.const 1200
      i32.add
      local.get $l12
      i32.const 1264
      i32.add
      local.get $p3
      local.get $l13
      call $f69940
      local.get $l12
      i32.const 1252
      i32.add
      f32.load
      local.set $l27
      local.get $l12
      f32.load offset=1248
      local.set $l29
      local.get $l12
      i32.const 1256
      i32.add
      f32.load
    end
    local.get $p6
    f32.add
    f32.store
    local.get $l12
    i32.const 1252
    i32.add
    local.get $l27
    local.get $p6
    f32.add
    f32.store
    local.get $l12
    local.get $l29
    local.get $p6
    f32.add
    f32.store offset=1248
    local.get $l12
    i32.const 1
    i32.store8 offset=1184
    local.get $l12
    i64.const 274877906944
    i64.store offset=1192
    local.get $l12
    local.get $l12
    i32.const 928
    i32.add
    i32.store offset=1188
    local.get $l12
    i32.const 3132404
    i32.store offset=912
    local.get $l12
    local.get $l12
    i32.const 928
    i32.add
    i32.store offset=920
    local.get $l12
    i32.const 2
    i32.store offset=916
    local.get $l17
    i32.load offset=40
    local.tee $l13
    local.get $l12
    i32.const 1200
    i32.add
    local.get $l12
    i32.const 912
    i32.add
    i32.const 1
    i32.const 1
    local.get $l13
    i32.load16_u offset=4
    i32.const 2
    i32.shl
    i32.const 3132404
    i32.add
    i32.load
    call_indirect $__indirect_function_table (type $t6)
    block $B3
      local.get $l12
      i32.load offset=1192
      local.tee $l21
      i32.eqz
      if $I4
        f32.const 0x1.fffffep+127 (;=3.40282e+38;)
        local.set $l38
        br $B3
      end
      local.get $l12
      i32.load offset=1188
      local.set $l24
      local.get $l12
      local.get $p0
      f32.load offset=76
      f32.store offset=896
      local.get $l12
      local.get $p0
      f32.load offset=80
      f32.store offset=900
      local.get $l12
      local.get $p0
      f32.load offset=84
      f32.store offset=904
      local.get $p0
      f32.load offset=68
      local.set $p9
      local.get $p0
      f32.load offset=64
      local.set $l27
      local.get $l12
      local.get $p0
      f32.load offset=72
      local.get $p6
      f32.add
      f32.store offset=888
      local.get $l12
      local.get $p9
      local.get $p6
      f32.add
      f32.store offset=884
      local.get $l12
      local.get $l27
      local.get $p6
      f32.add
      f32.store offset=880
      local.get $l12
      i32.const 1
      i32.store8 offset=864
      local.get $l12
      i64.const 274877906944
      i64.store offset=872
      local.get $l12
      local.get $l12
      i32.const 608
      i32.add
      i32.store offset=868
      local.get $l12
      i32.const 0
      i32.store offset=336
      local.get $l12
      i32.const 608
      i32.add
      local.get $l21
      local.get $l12
      i32.const 336
      i32.add
      call $f70487
      local.get $l12
      i32.const 1
      i32.store8 offset=592
      local.get $l12
      i64.const 274877906944
      i64.store offset=600
      local.get $l12
      local.get $l12
      i32.const 336
      i32.add
      i32.store offset=596
      local.get $l12
      i32.load offset=1192
      local.set $l13
      local.get $l12
      i32.const 0
      i32.store offset=80
      local.get $l12
      i32.const 336
      i32.add
      local.get $l13
      local.get $l12
      i32.const 80
      i32.add
      call $f70487
      local.get $l12
      i32.load offset=596
      local.set $l18
      local.get $l12
      i32.load offset=868
      local.set $l22
      local.get $l12
      i32.const 144
      i32.add
      local.tee $l23
      i32.const 5
      i32.add
      local.set $l26
      loop $L5
        local.get $l12
        i64.const -108086391082057729
        i64.store offset=136
        local.get $l12
        i64.const -108086393229541377
        i64.store offset=128
        local.get $l12
        i64.const 9115285643625234431
        i64.store offset=120
        local.get $l12
        i32.const 1
        i32.store offset=92
        local.get $l12
        local.get $l17
        i32.store offset=80
        local.get $l12
        local.get $l24
        local.get $l19
        i32.const 2
        i32.shl
        i32.add
        local.tee $l16
        i32.store offset=88
        local.get $l12
        local.get $l12
        i32.const 1496
        i32.add
        i32.store offset=96
        local.get $l12
        local.get $l12
        i32.const 1416
        i32.add
        i32.store offset=84
        local.get $l26
        i64.const 0
        i64.store align=1
        local.get $l23
        i64.const 0
        i64.store align=4
        local.get $l12
        i32.const 232
        i32.add
        local.get $l12
        i32.const 80
        i32.add
        call $f70488
        block $B6
          local.get $l35
          local.get $p3
          f32.load offset=4
          local.tee $l27
          local.get $l12
          f32.load offset=232
          local.tee $p9
          local.get $p9
          f32.add
          local.tee $l29
          local.get $p3
          f32.load
          local.tee $l28
          f32.mul
          local.get $l27
          local.get $l12
          f32.load offset=236
          local.tee $p9
          local.get $p9
          f32.add
          local.tee $l31
          f32.mul
          f32.add
          local.get $l12
          f32.load offset=240
          local.tee $p9
          local.get $p9
          f32.add
          local.tee $l30
          local.get $p3
          f32.load offset=8
          local.tee $l33
          f32.mul
          f32.add
          local.tee $l32
          f32.mul
          local.get $l31
          local.get $p3
          f32.load offset=12
          local.tee $p9
          local.get $p9
          f32.mul
          f32.const -0x1p-1 (;=-0.5;)
          f32.add
          local.tee $l34
          f32.mul
          local.get $p9
          local.get $l29
          local.get $l33
          f32.mul
          local.get $l30
          local.get $l28
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          f32.neg
          f32.mul
          local.get $l37
          local.get $l28
          local.get $l32
          f32.mul
          local.get $l29
          local.get $l34
          f32.mul
          local.get $p9
          local.get $l30
          local.get $l27
          f32.mul
          local.get $l31
          local.get $l33
          f32.mul
          f32.sub
          f32.mul
          f32.add
          f32.add
          f32.mul
          f32.sub
          local.get $l36
          local.get $l30
          local.get $l34
          f32.mul
          local.get $p9
          local.get $l31
          local.get $l28
          f32.mul
          local.get $l29
          local.get $l27
          f32.mul
          f32.sub
          f32.mul
          f32.add
          local.get $l33
          local.get $l32
          f32.mul
          f32.add
          f32.mul
          f32.sub
          local.get $p11
          f32.ge
          i32.eqz
          br_if $B6
          local.get $l12
          i32.const 80
          i32.add
          local.get $l12
          i32.const 232
          i32.add
          local.get $p5
          call $f70489
          local.get $l12
          local.get $l12
          f32.load offset=240
          local.tee $p9
          local.get $l12
          f32.load offset=252
          local.tee $l27
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=8
          local.get $l12
          local.get $l12
          f32.load offset=236
          local.tee $l29
          local.get $l12
          f32.load offset=248
          local.tee $l28
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=4
          local.get $l12
          local.get $l12
          f32.load offset=232
          local.tee $l31
          local.get $l12
          f32.load offset=244
          local.tee $l30
          f32.add
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store
          local.get $l12
          local.get $l27
          local.get $p9
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.const 0x1.47ae14p-6 (;=0.02;)
          f32.add
          f32.store offset=1528
          local.get $l12
          local.get $l28
          local.get $l29
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.const 0x1.47ae14p-6 (;=0.02;)
          f32.add
          f32.store offset=1524
          local.get $l12
          local.get $l30
          local.get $l31
          f32.sub
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.const 0x1.47ae14p-6 (;=0.02;)
          f32.add
          f32.store offset=1520
          local.get $l12
          i32.const 896
          i32.add
          local.get $l12
          i32.const 880
          i32.add
          local.get $l12
          local.get $l12
          i32.const 1520
          i32.add
          local.get $l12
          i32.const 1400
          i32.add
          local.get $l12
          i32.const 1384
          i32.add
          call $f70620
          local.tee $l27
          f32.const 0x1p+0 (;=1;)
          f32.le
          i32.eqz
          br_if $B6
          i32.const 0
          local.set $l25
          block $B7
            local.get $l20
            local.tee $l13
            i32.eqz
            br_if $B7
            loop $L8
              local.get $l27
              local.get $l18
              local.get $l13
              i32.const 1
              i32.sub
              local.tee $l14
              i32.const 2
              i32.shl
              local.tee $l15
              i32.add
              f32.load
              local.tee $p9
              f32.ge
              if $I9
                local.get $l13
                local.set $l25
                br $B7
              end
              local.get $l18
              local.get $l13
              i32.const 2
              i32.shl
              local.tee $l13
              i32.add
              local.get $p9
              f32.store
              local.get $l13
              local.get $l22
              i32.add
              local.get $l15
              local.get $l22
              i32.add
              i32.load
              i32.store
              local.get $l14
              local.tee $l13
              br_if $L8
            end
          end
          local.get $l22
          local.get $l25
          i32.const 2
          i32.shl
          local.tee $l13
          i32.add
          local.get $l16
          i32.load
          i32.store
          local.get $l13
          local.get $l18
          i32.add
          local.get $l27
          f32.store
          local.get $l20
          i32.const 1
          i32.add
          local.set $l20
        end
        local.get $l19
        i32.const 1
        i32.add
        local.tee $l19
        local.get $l21
        i32.ne
        br_if $L5
      end
      local.get $p0
      f32.load offset=4
      local.set $l36
      local.get $l12
      local.get $p5
      f32.load offset=24
      local.get $p3
      f32.load offset=24
      local.tee $l35
      f32.sub
      local.tee $p9
      local.get $p9
      f32.add
      local.tee $l30
      local.get $p3
      f32.load offset=12
      local.tee $p9
      local.get $p9
      f32.mul
      f32.const -0x1p-1 (;=-0.5;)
      f32.add
      local.tee $l31
      f32.mul
      local.get $p9
      local.get $p5
      f32.load offset=20
      local.get $p3
      f32.load offset=20
      local.tee $l37
      f32.sub
      local.tee $l27
      local.get $l27
      f32.add
      local.tee $l33
      local.get $p3
      f32.load
      local.tee $l27
      f32.mul
      local.get $p5
      f32.load offset=16
      local.get $p3
      f32.load offset=16
      local.tee $p11
      f32.sub
      local.tee $l29
      local.get $l29
      f32.add
      local.tee $l32
      local.get $p3
      f32.load offset=4
      local.tee $l29
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      local.get $p3
      f32.load offset=8
      local.tee $l28
      local.get $l32
      local.get $l27
      f32.mul
      local.get $l33
      local.get $l29
      f32.mul
      f32.add
      local.get $l30
      local.get $l28
      f32.mul
      f32.add
      local.tee $l34
      f32.mul
      f32.add
      f32.store offset=328
      local.get $l12
      local.get $l29
      local.get $l34
      f32.mul
      local.get $l33
      local.get $l31
      f32.mul
      local.get $p9
      local.get $l32
      local.get $l28
      f32.mul
      local.get $l30
      local.get $l27
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      f32.store offset=324
      local.get $l12
      local.get $l27
      local.get $l34
      f32.mul
      local.get $l32
      local.get $l31
      f32.mul
      local.get $p9
      local.get $l30
      local.get $l29
      f32.mul
      local.get $l33
      local.get $l28
      f32.mul
      f32.sub
      f32.mul
      f32.sub
      f32.add
      f32.store offset=320
      f32.const 0x1.fffffep+127 (;=3.40282e+38;)
      local.set $l38
      i32.const -1
      local.set $l23
      block $B10
        local.get $l20
        i32.eqz
        if $I11
          br $B10
        end
        local.get $l31
        local.get $p4
        f32.load offset=24
        local.get $l35
        f32.sub
        local.tee $l30
        local.get $l30
        f32.add
        local.tee $l30
        f32.mul
        local.get $p9
        local.get $l27
        local.get $p4
        f32.load offset=20
        local.get $l37
        f32.sub
        local.tee $l33
        local.get $l33
        f32.add
        local.tee $l33
        f32.mul
        local.get $l29
        local.get $p4
        f32.load offset=16
        local.get $p11
        f32.sub
        local.tee $l32
        local.get $l32
        f32.add
        local.tee $l32
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        local.get $l28
        local.get $l27
        local.get $l32
        f32.mul
        local.get $l29
        local.get $l33
        f32.mul
        f32.add
        local.get $l28
        local.get $l30
        f32.mul
        f32.add
        local.tee $l34
        f32.mul
        f32.add
        local.set $l56
        local.get $l29
        local.get $l34
        f32.mul
        local.get $l31
        local.get $l33
        f32.mul
        local.get $p9
        local.get $l28
        local.get $l32
        f32.mul
        local.get $l27
        local.get $l30
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        local.set $l57
        local.get $l27
        local.get $l34
        f32.mul
        local.get $l31
        local.get $l32
        f32.mul
        local.get $p9
        local.get $l29
        local.get $l30
        f32.mul
        local.get $l28
        local.get $l33
        f32.mul
        f32.sub
        f32.mul
        f32.sub
        f32.add
        local.set $l58
        local.get $l36
        local.get $p6
        f32.add
        local.tee $l40
        local.get $l40
        f32.add
        local.set $l59
        local.get $l40
        local.get $l40
        f32.mul
        local.set $l60
        i32.const 0
        local.set $l18
        local.get $l12
        i32.const 296
        i32.add
        local.tee $l21
        i32.const 5
        i32.add
        local.set $l24
        loop $L12
          local.get $l12
          i64.const -108086391082057729
          i64.store offset=288
          local.get $l12
          i64.const -108086393229541377
          i64.store offset=280
          local.get $l12
          i64.const 9115285643625234431
          i64.store offset=272
          local.get $l12
          i32.const 1
          i32.store offset=244
          local.get $l12
          local.get $l22
          local.get $l18
          i32.const 2
          i32.shl
          i32.add
          local.tee $l19
          i32.store offset=240
          local.get $l12
          local.get $l12
          i32.const 316
          i32.add
          i32.store offset=248
          local.get $l12
          local.get $l12
          i32.const 1416
          i32.add
          i32.store offset=236
          local.get $l12
          local.get $l17
          i32.store offset=232
          local.get $l24
          i64.const 0
          i64.store align=1
          local.get $l21
          i64.const 0
          i64.store align=4
          local.get $l19
          i32.load
          local.set $l15
          local.get $l17
          i32.load offset=40
          local.tee $l13
          i32.load offset=24
          local.set $l14
          block $B13 (result i32)
            local.get $l13
            i32.load8_u offset=64
            i32.const 2
            i32.and
            if $I14
              local.get $l13
              i32.load offset=28
              local.get $l15
              i32.const 6
              i32.mul
              i32.add
              local.tee $l16
              i32.load16_u offset=4
              local.set $l13
              local.get $l16
              i32.load16_u offset=2
              local.set $l15
              local.get $l16
              i32.load16_u
              br $B13
            end
            local.get $l13
            i32.load offset=28
            local.get $l15
            i32.const 12
            i32.mul
            i32.add
            local.tee $l16
            i32.load offset=8
            local.set $l13
            local.get $l16
            i32.load offset=4
            local.set $l15
            local.get $l16
            i32.load
          end
          local.set $l16
          local.get $l14
          local.get $l13
          i32.const 12
          i32.mul
          i32.add
          local.tee $l13
          f32.load offset=8
          local.set $p9
          local.get $l14
          local.get $l15
          i32.const 12
          i32.mul
          i32.add
          local.tee $l15
          f32.load offset=8
          local.set $l27
          local.get $l13
          f32.load
          local.set $l29
          local.get $l15
          f32.load
          local.set $l28
          local.get $l13
          f32.load offset=4
          local.set $l31
          local.get $l15
          f32.load offset=4
          local.set $l30
          local.get $l12
          i32.load8_u offset=1488
          local.set $l13
          local.get $l12
          local.get $l14
          local.get $l16
          i32.const 12
          i32.mul
          i32.add
          local.tee $l14
          f32.load
          local.tee $l33
          local.get $l12
          f32.load offset=1424
          local.tee $l32
          f32.mul
          local.get $l14
          f32.load offset=4
          local.tee $l34
          local.get $l12
          f32.load offset=1436
          local.tee $l36
          f32.mul
          f32.add
          local.get $l14
          f32.load offset=8
          local.tee $l35
          local.get $l12
          f32.load offset=1448
          local.tee $l37
          f32.mul
          f32.add
          local.tee $p11
          f32.store offset=192
          local.get $l12
          local.get $l33
          local.get $l12
          f32.load offset=1420
          local.tee $l47
          f32.mul
          local.get $l34
          local.get $l12
          f32.load offset=1432
          local.tee $l48
          f32.mul
          f32.add
          local.get $l35
          local.get $l12
          f32.load offset=1444
          local.tee $l49
          f32.mul
          f32.add
          local.tee $l50
          f32.store offset=188
          local.get $l12
          local.get $l33
          local.get $l12
          f32.load offset=1416
          local.tee $l51
          f32.mul
          local.get $l34
          local.get $l12
          f32.load offset=1428
          local.tee $l33
          f32.mul
          f32.add
          local.get $l35
          local.get $l12
          f32.load offset=1440
          local.tee $l34
          f32.mul
          f32.add
          local.tee $l35
          f32.store offset=184
          local.get $l12
          i32.const 0
          i32.store8 offset=112
          local.get $l12
          i64.const 23613931519
          i64.store offset=104
          local.get $l12
          i32.const 0
          i32.store offset=172
          local.get $l12
          local.get $l32
          local.get $l28
          local.get $l29
          local.get $l13
          select
          local.tee $l39
          f32.mul
          local.get $l36
          local.get $l30
          local.get $l31
          local.get $l13
          select
          local.tee $l52
          f32.mul
          f32.add
          local.get $l37
          local.get $l27
          local.get $p9
          local.get $l13
          select
          local.tee $l53
          f32.mul
          f32.add
          local.tee $l54
          f32.store offset=168
          local.get $l12
          local.get $l39
          local.get $l47
          f32.mul
          local.get $l52
          local.get $l48
          f32.mul
          f32.add
          local.get $l53
          local.get $l49
          f32.mul
          f32.add
          local.tee $l55
          f32.store offset=164
          local.get $l12
          local.get $l39
          local.get $l51
          f32.mul
          local.get $l52
          local.get $l33
          f32.mul
          f32.add
          local.get $l53
          local.get $l34
          f32.mul
          f32.add
          local.tee $l39
          f32.store offset=160
          local.get $l12
          i32.const 0
          i32.store offset=156
          local.get $l12
          local.get $l32
          local.get $l29
          local.get $l28
          local.get $l13
          select
          local.tee $l29
          f32.mul
          local.get $l36
          local.get $l31
          local.get $l30
          local.get $l13
          select
          local.tee $l28
          f32.mul
          f32.add
          local.get $l37
          local.get $p9
          local.get $l27
          local.get $l13
          select
          local.tee $p9
          f32.mul
          f32.add
          local.tee $l27
          f32.store offset=152
          local.get $l12
          local.get $l29
          local.get $l47
          f32.mul
          local.get $l28
          local.get $l48
          f32.mul
          f32.add
          local.get $p9
          local.get $l49
          f32.mul
          f32.add
          local.tee $l31
          f32.store offset=148
          local.get $l12
          local.get $l29
          local.get $l51
          f32.mul
          local.get $l28
          local.get $l33
          f32.mul
          f32.add
          local.get $p9
          local.get $l34
          f32.mul
          f32.add
          local.tee $l29
          f32.store offset=144
          local.get $l12
          i32.const 0
          i32.store offset=140
          local.get $l12
          local.get $p11
          f32.store offset=136
          local.get $l12
          local.get $l50
          f32.store offset=132
          local.get $l12
          local.get $l35
          f32.store offset=128
          local.get $l12
          i32.const 0
          i32.store offset=92
          local.get $l12
          i64.const 9187343235540844544
          i64.store offset=96
          local.get $l12
          local.get $l54
          local.get $p11
          local.get $l27
          f32.add
          f32.add
          f32.const 0x1.55553ep-2 (;=0.333333;)
          f32.mul
          f32.store offset=88
          local.get $l12
          local.get $l55
          local.get $l50
          local.get $l31
          f32.add
          f32.add
          f32.const 0x1.55553ep-2 (;=0.333333;)
          f32.mul
          f32.store offset=84
          local.get $l12
          local.get $l39
          local.get $l35
          local.get $l29
          f32.add
          f32.add
          f32.const 0x1.55553ep-2 (;=0.333333;)
          f32.mul
          f32.store offset=80
          local.get $p1
          i32.load
          local.set $l14
          local.get $p0
          i32.load
          local.set $l13
          local.get $l12
          i32.const 0
          i32.store8 offset=72
          local.get $l12
          i64.const 4575657221408423936
          i64.store offset=64
          local.get $l12
          i64.const 0
          i64.store offset=56
          local.get $l12
          i64.const 4575657221408423936
          i64.store offset=48
          local.get $l12
          i64.const 0
          i64.store offset=40
          local.get $l12
          i64.const 4575657222473777152
          i64.store offset=32
          local.get $l12
          i64.const 0
          i64.store offset=24
          local.get $l12
          i64.const 1065353216
          i64.store offset=16
          local.get $l12
          i64.const 0
          i64.store offset=8
          local.get $l12
          i64.const 1065353216
          i64.store
          local.get $l13
          local.get $l14
          local.get $p2
          local.get $p3
          local.get $p4
          local.get $p5
          local.get $p6
          local.get $l12
          i32.const 216
          i32.add
          local.get $l12
          i32.const 200
          i32.add
          local.get $l12
          local.get $l12
          i32.const 80
          i32.add
          f32.const 0x0p+0 (;=0;)
          local.get $l13
          i32.load
          i32.const 2
          i32.shl
          i32.const 4117728
          i32.add
          i32.load
          call_indirect $__indirect_function_table (type $t216)
          local.set $p9
          local.get $l12
          local.get $l12
          f32.load offset=216
          f32.neg
          local.tee $l28
          f32.store offset=216
          local.get $l12
          local.get $l12
          f32.load offset=220
          f32.neg
          local.tee $l30
          f32.store offset=220
          local.get $l12
          local.get $l12
          f32.load offset=224
          f32.neg
          local.tee $l33
          f32.store offset=224
          local.get $p9
          f32.const 0x0p+0 (;=0;)
          f32.le
          if $I15
            local.get $l12
            f32.load offset=184
            local.set $p9
            local.get $l12
            f32.load offset=188
            local.set $l28
            local.get $l12
            local.get $l12
            f32.load offset=192
            local.tee $l30
            local.get $l27
            local.get $l30
            f32.sub
            local.tee $l27
            f32.add
            f32.store offset=8
            local.get $l12
            local.get $l28
            local.get $l31
            local.get $l28
            f32.sub
            local.tee $l31
            f32.add
            f32.store offset=4
            local.get $l12
            local.get $p9
            local.get $l29
            local.get $p9
            f32.sub
            local.tee $l29
            f32.add
            f32.store
            local.get $l12
            local.get $l30
            local.get $l54
            local.get $l30
            f32.sub
            local.tee $l33
            f32.add
            f32.store offset=1528
            local.get $l12
            local.get $l28
            local.get $l55
            local.get $l28
            f32.sub
            local.tee $l30
            f32.add
            f32.store offset=1524
            local.get $l12
            local.get $p9
            local.get $l39
            local.get $p9
            f32.sub
            local.tee $l28
            f32.add
            f32.store offset=1520
            local.get $l12
            i32.const 1496
            i32.add
            local.get $l12
            i32.const 320
            i32.add
            local.get $l12
            i32.const 184
            i32.add
            local.get $l12
            local.get $l12
            i32.const 1520
            i32.add
            local.get $l12
            i32.const 1516
            i32.add
            local.get $l12
            i32.const 1512
            i32.add
            call $f69887
            f32.const 0x0p+0 (;=0;)
            local.set $p9
            local.get $l60
            local.get $l12
            f32.load offset=1496
            local.get $l12
            f32.load offset=320
            f32.sub
            local.tee $l32
            local.get $l32
            f32.mul
            local.get $l12
            f32.load offset=1500
            local.get $l12
            f32.load offset=324
            f32.sub
            local.tee $l32
            local.get $l32
            f32.mul
            f32.add
            local.get $l12
            f32.load offset=1504
            local.get $l12
            f32.load offset=328
            f32.sub
            local.tee $l32
            local.get $l32
            f32.mul
            f32.add
            local.tee $l32
            f32.gt
            if $I16
              local.get $l59
              local.get $l32
              f32.sqrt
              local.tee $p9
              f32.sub
              f32.neg
              local.get $p9
              local.get $l40
              f32.sub
              local.get $l56
              local.get $l29
              local.get $l30
              f32.mul
              local.get $l28
              local.get $l31
              f32.mul
              f32.sub
              local.tee $p9
              f32.mul
              local.get $l58
              local.get $l31
              local.get $l33
              f32.mul
              local.get $l30
              local.get $l27
              f32.mul
              f32.sub
              local.tee $l31
              f32.mul
              local.get $l57
              local.get $l28
              local.get $l27
              f32.mul
              local.get $l29
              local.get $l33
              f32.mul
              f32.sub
              local.tee $l27
              f32.mul
              f32.add
              f32.add
              local.get $l31
              local.get $l12
              f32.load offset=184
              f32.mul
              local.get $l27
              local.get $l12
              f32.load offset=188
              f32.mul
              f32.add
              local.get $p9
              local.get $l12
              f32.load offset=192
              f32.mul
              f32.add
              f32.sub
              f32.const 0x0p+0 (;=0;)
              f32.lt
              select
              local.set $p9
            end
            local.get $l12
            local.get $l12
            i32.const 232
            i32.add
            call $f70488
            local.get $l12
            local.get $l12
            f32.load offset=8
            local.tee $l27
            local.get $l27
            f32.add
            local.tee $l29
            local.get $p3
            f32.load offset=12
            local.tee $l27
            local.get $l27
            f32.mul
            f32.const -0x1p-1 (;=-0.5;)
            f32.add
            local.tee $l35
            f32.mul
            local.get $l27
            local.get $l12
            f32.load offset=4
            local.tee $l28
            local.get $l28
            f32.add
            local.tee $l28
            local.get $p3
            f32.load
            local.tee $l31
            f32.mul
            local.get $l12
            f32.load
            local.tee $l30
            local.get $l30
            f32.add
            local.tee $l32
            local.get $p3
            f32.load offset=4
            local.tee $l34
            f32.mul
            f32.sub
            f32.mul
            f32.add
            local.get $p3
            f32.load offset=8
            local.tee $l36
            local.get $l32
            local.get $l31
            f32.mul
            local.get $l28
            local.get $l34
            f32.mul
            f32.add
            local.get $l29
            local.get $l36
            f32.mul
            f32.add
            local.tee $l37
            f32.mul
            f32.add
            local.tee $l33
            f32.store offset=224
            local.get $l12
            local.get $l34
            local.get $l37
            f32.mul
            local.get $l28
            local.get $l35
            f32.mul
            local.get $l27
            local.get $l32
            local.get $l36
            f32.mul
            local.get $l29
            local.get $l31
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            local.tee $l30
            f32.store offset=220
            local.get $l12
            local.get $l31
            local.get $l37
            f32.mul
            local.get $l32
            local.get $l35
            f32.mul
            local.get $l27
            local.get $l29
            local.get $l34
            f32.mul
            local.get $l28
            local.get $l36
            f32.mul
            f32.sub
            f32.mul
            f32.add
            f32.add
            local.tee $l28
            f32.store offset=216
          end
          local.get $p9
          local.get $l38
          f32.lt
          if $I17
            local.get $l19
            i32.load
            local.set $l23
            local.get $l12
            f32.load offset=208
            local.set $l43
            local.get $l12
            f32.load offset=204
            local.set $l42
            local.get $l12
            f32.load offset=200
            local.set $l41
            local.get $l28
            local.set $l44
            local.get $l30
            local.set $l45
            local.get $l33
            local.set $l46
            local.get $p9
            local.set $l38
          end
          local.get $l18
          i32.const 1
          i32.add
          local.tee $l18
          local.get $l20
          i32.ne
          br_if $L12
        end
      end
      local.get $p7
      local.get $l46
      f32.store offset=8
      local.get $p7
      local.get $l45
      f32.store offset=4
      local.get $p7
      local.get $l44
      f32.store
      local.get $p8
      local.get $l43
      f32.store offset=8
      local.get $p8
      local.get $l42
      f32.store offset=4
      local.get $p8
      local.get $l41
      f32.store
      local.get $p10
      local.get $l23
      i32.store
      block $B18
        local.get $l12
        i32.load offset=604
        local.tee $l13
        i32.const 0
        i32.lt_s
        br_if $B18
        local.get $l13
        i32.const 2147483647
        i32.and
        i32.eqz
        br_if $B18
        local.get $l12
        i32.load offset=596
        local.tee $l13
        local.get $l12
        i32.const 336
        i32.add
        i32.eq
        br_if $B18
        local.get $l13
        i32.eqz
        br_if $B18
        call $f69753
        local.tee $l14
        local.get $l13
        local.get $l14
        i32.load
        i32.load offset=12
        call_indirect $__indirect_function_table (type $t1)
      end
      local.get $l12
      i32.load offset=876
      local.tee $l13
      i32.const 0
      i32.lt_s
      br_if $B3
      local.get $l13
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if $B3
      local.get $l12
      i32.load offset=868
      local.tee $l13
      local.get $l12
      i32.const 608
      i32.add
      i32.eq
      br_if $B3
      local.get $l13
      i32.eqz
      br_if $B3
      call $f69753
      local.tee $l14
      local.get $l13
      local.get $l14
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    block $B19
      local.get $l12
      i32.load offset=1196
      local.tee $l13
      i32.const 0
      i32.lt_s
      br_if $B19
      local.get $l13
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if $B19
      local.get $l12
      i32.load offset=1188
      local.tee $l13
      local.get $l12
      i32.const 928
      i32.add
      i32.eq
      br_if $B19
      local.get $l13
      i32.eqz
      br_if $B19
      call $f69753
      local.tee $l14
      local.get $l13
      local.get $l14
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $l12
    i32.const 1536
    i32.add
    global.set $g0
    local.get $l38)
