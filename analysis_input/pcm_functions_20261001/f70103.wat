  (func $f70103 (type $t192) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 f32) (param $p5 i32) (param $p6 i32) (result i32)
    (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i32) (local $l25 i32) (local $l26 i32) (local $l27 i32) (local $l28 i32) (local $l29 i32) (local $l30 i32) (local $l31 i32) (local $l32 i32) (local $l33 i32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32) (local $l38 f32) (local $l39 f32) (local $l40 f32) (local $l41 f32) (local $l42 f32) (local $l43 f32) (local $l44 f32) (local $l45 f32) (local $l46 f32) (local $l47 f32) (local $l48 f32) (local $l49 f32) (local $l50 f32) (local $l51 f32) (local $l52 f32) (local $l53 f32) (local $l54 f32) (local $l55 f32) (local $l56 f32) (local $l57 f32) (local $l58 f32) (local $l59 f32) (local $l60 f32) (local $l61 f32) (local $l62 f32) (local $l63 f32) (local $l64 f32) (local $l65 f32) (local $l66 f32) (local $l67 f32) (local $l68 f32) (local $l69 f32) (local $l70 f32) (local $l71 f32) (local $l72 i64) (local $l73 i64) (local $l74 i64)
    global.get $g0
    i32.const 6128
    i32.sub
    local.tee $l7
    global.set $g0
    local.get $p0
    i32.load offset=36
    local.tee $l13
    i32.load offset=56
    local.set $l25
    local.get $l7
    i32.const 0
    i32.store offset=2012
    local.get $l7
    i32.const 0
    i32.store offset=2008
    local.get $l7
    i64.const 0
    i64.store offset=2000
    local.get $l7
    i32.const 2000
    i32.add
    i32.const 128
    call $f70632
    local.get $l7
    local.get $p2
    f32.load
    f32.store offset=1936
    local.get $l7
    local.get $p2
    f32.load offset=4
    f32.store offset=1940
    local.get $l7
    local.get $p2
    f32.load offset=8
    f32.store offset=1944
    local.get $l7
    local.get $p2
    f32.load offset=12
    f32.store offset=1948
    local.get $l7
    i32.const 1952
    i32.add
    local.get $p2
    f32.load offset=16
    f32.store
    local.get $l7
    i32.const 1956
    i32.add
    local.get $p2
    f32.load offset=20
    f32.store
    local.get $l7
    local.get $p2
    f32.load offset=24
    f32.store offset=1960
    local.get $l7
    i32.const 1964
    i32.add
    local.get $p2
    f32.load offset=28
    f32.store
    local.get $l7
    i32.const 1968
    i32.add
    local.get $p2
    f32.load offset=32
    f32.store
    local.get $l7
    local.get $p2
    f32.load offset=36
    local.tee $l52
    f32.store offset=1972
    local.get $l7
    i32.const 1976
    i32.add
    local.get $p2
    f32.load offset=40
    local.tee $l53
    f32.store
    local.get $l7
    i32.const 1980
    i32.add
    local.get $p2
    f32.load offset=44
    local.tee $l54
    f32.store
    local.get $p3
    f32.load offset=24
    local.set $l39
    local.get $p3
    i64.load align=4
    local.set $l72
    local.get $p3
    i64.load offset=8 align=4
    local.set $l73
    local.get $p3
    i64.load offset=16 align=4
    local.set $l74
    local.get $l7
    local.get $p2
    f32.load offset=48
    local.tee $l34
    local.get $p2
    f32.load offset=52
    local.tee $l35
    local.get $l34
    local.get $l35
    f32.le
    select
    local.tee $l37
    local.get $p2
    f32.load offset=56
    local.tee $l36
    local.get $l36
    local.get $l37
    f32.ge
    select
    local.tee $l37
    f32.const 0x1.333334p-3 (;=0.15;)
    f32.mul
    local.tee $l42
    local.get $p4
    f32.add
    local.tee $p4
    f32.store offset=1920
    local.get $l7
    i32.const 1992
    i32.add
    local.get $l36
    local.get $p4
    f32.add
    f32.store
    local.get $l7
    i32.const 1988
    i32.add
    local.get $l35
    local.get $p4
    f32.add
    f32.store
    local.get $l7
    local.get $l34
    local.get $p4
    f32.add
    f32.store offset=1984
    local.get $l7
    i32.const 1916
    i32.add
    i32.const 0
    i32.store
    local.get $l7
    i32.const 1912
    i32.add
    local.get $l36
    f32.store
    local.get $l7
    i32.const 1908
    i32.add
    local.get $l35
    f32.store
    local.get $l7
    i32.const 0
    i32.store8 offset=1888
    local.get $l7
    i32.const 3
    i32.store offset=1884
    local.get $l7
    i64.const 0
    i64.store offset=1856
    local.get $l7
    i64.const 0
    i64.store offset=1864
    local.get $l7
    local.get $l34
    f32.store offset=1904
    local.get $l7
    local.get $l37
    f32.const 0x1.99999ap-5 (;=0.05;)
    f32.mul
    local.tee $l34
    f32.store offset=1880
    local.get $l7
    local.get $l34
    f32.store offset=1876
    local.get $l7
    local.get $l42
    f32.store offset=1872
    local.get $l7
    i32.const 1560
    i32.add
    local.get $p2
    i32.const 48
    i32.add
    call $f69944
    local.get $l7
    i32.const 1784
    i32.add
    call $f70032
    local.get $l7
    i32.const 1528
    i32.add
    i64.const 0
    i64.store
    local.get $l7
    i32.const 1524
    i32.add
    i32.const 1065353216
    i32.store
    local.get $l7
    i32.const 1536
    i32.add
    i64.const 0
    i64.store
    local.get $l7
    i32.const 1544
    i32.add
    i64.const 1065353216
    i64.store
    local.get $l7
    i64.const 0
    i64.store offset=1508 align=4
    local.get $l7
    i32.const 1065353216
    i32.store offset=1504
    local.get $l7
    i64.const 0
    i64.store offset=1516 align=4
    local.get $l7
    i32.const 1456
    i32.add
    local.get $p1
    local.get $p0
    i32.const 4
    i32.add
    local.tee $l28
    call $f70133
    local.get $l7
    i32.const 1452
    i32.add
    i32.const 0
    i32.store
    local.get $l7
    i32.const 1448
    i32.add
    local.get $l39
    f32.store
    local.get $l7
    local.get $l74
    i64.store offset=1440
    local.get $l7
    local.get $l73
    i64.store offset=1432
    local.get $l7
    local.get $l72
    i64.store offset=1424
    i32.const 268435455
    local.set $l11
    local.get $l7
    i32.const 1360
    i32.add
    local.tee $l29
    i32.const 8
    i32.add
    local.set $l30
    f32.const 0x0p+0 (;=0;)
    local.set $l42
    block $B0 (result i32)
      block $B1
        loop $L2
          block $B3
            local.get $l7
            i32.const 0
            i32.store offset=2004
            local.get $p0
            i32.load offset=36
            local.set $p2
            local.get $l7
            local.get $l7
            i32.const 1936
            i32.add
            local.get $p1
            local.get $l28
            call $f69940
            local.get $l7
            i32.const 3124884
            i32.store offset=1344
            local.get $l7
            local.get $l7
            i32.const 2000
            i32.add
            i32.store offset=1352
            local.get $l7
            i32.const 2
            i32.store offset=1348
            local.get $p2
            local.get $l7
            local.get $l7
            i32.const 1344
            i32.add
            i32.const 1
            i32.const 1
            local.get $p2
            i32.load16_u offset=4
            i32.const 2
            i32.shl
            i32.const 3124884
            i32.add
            i32.load
            call_indirect $__indirect_function_table (type $t6)
            local.get $l7
            i32.load offset=2004
            local.tee $l19
            i32.eqz
            br_if $B3
            i32.const 0
            local.set $l20
            local.get $l7
            i32.const 0
            i32.store offset=1452
            local.get $l7
            local.get $l54
            f32.store offset=1448
            local.get $l7
            local.get $l53
            f32.store offset=1444
            local.get $l7
            local.get $l52
            f32.store offset=1440
            local.get $l7
            i32.const 1
            i32.store8 offset=1388
            local.get $l7
            i32.const 3125888
            i32.store offset=1344
            local.get $l7
            local.get $l7
            i32.const 1504
            i32.add
            i32.store offset=1384
            local.get $l7
            local.get $l7
            i32.const 1504
            i32.add
            i32.store offset=1380
            local.get $l7
            local.get $l7
            i32.const 1424
            i32.add
            i32.store offset=1376
            local.get $l7
            local.get $l7
            i32.const 1856
            i32.add
            i32.store offset=1392
            local.get $l30
            i64.const 0
            i64.store
            local.get $l29
            i64.const 0
            i64.store
            local.get $l7
            f32.load offset=1980
            local.set $l58
            local.get $l7
            f32.load offset=1976
            local.set $l71
            local.get $l7
            f32.load offset=1972
            local.set $l59
            local.get $l7
            f32.load offset=1500
            local.set $l60
            local.get $l7
            f32.load offset=1492
            local.set $l61
            local.get $l7
            f32.load offset=1496
            local.set $l62
            local.get $l7
            f32.load offset=1464
            local.set $l43
            local.get $l7
            f32.load offset=1456
            local.set $l63
            local.get $l7
            f32.load offset=1460
            local.set $l64
            local.get $l7
            f32.load offset=1476
            local.set $l65
            local.get $l7
            f32.load offset=1468
            local.set $l66
            local.get $l7
            f32.load offset=1472
            local.set $l67
            local.get $l7
            f32.load offset=1944
            local.set $l34
            local.get $l7
            f32.load offset=1936
            local.set $l35
            local.get $l7
            f32.load offset=1940
            local.set $l36
            local.get $l7
            f32.load offset=1956
            local.set $p4
            local.get $l7
            f32.load offset=1948
            local.set $l39
            local.get $l7
            f32.load offset=1952
            local.set $l37
            local.get $l7
            f32.load offset=1488
            local.set $l68
            local.get $l7
            f32.load offset=1968
            local.set $l40
            local.get $l7
            f32.load offset=1480
            local.set $l69
            local.get $l7
            f32.load offset=1960
            local.set $l38
            local.get $l7
            f32.load offset=1484
            local.set $l70
            local.get $l7
            f32.load offset=1964
            local.set $l41
            local.get $l7
            i32.const 0
            i32.store offset=1340
            local.get $l7
            i32.const 0
            i32.store offset=1324
            local.get $l7
            i32.const 0
            i32.store offset=1308
            local.get $l7
            i32.const 0
            i32.store offset=1292
            local.get $l7
            local.get $l38
            local.get $l69
            f32.mul
            local.get $l41
            local.get $l70
            f32.mul
            f32.add
            local.get $l40
            local.get $l68
            f32.mul
            f32.add
            f32.store offset=1320
            local.get $l7
            local.get $l39
            local.get $l69
            f32.mul
            local.get $l37
            local.get $l70
            f32.mul
            f32.add
            local.get $p4
            local.get $l68
            f32.mul
            f32.add
            f32.store offset=1316
            local.get $l7
            local.get $l35
            local.get $l69
            f32.mul
            local.get $l36
            local.get $l70
            f32.mul
            f32.add
            local.get $l34
            local.get $l68
            f32.mul
            f32.add
            f32.store offset=1312
            local.get $l7
            local.get $l38
            local.get $l66
            f32.mul
            local.get $l41
            local.get $l67
            f32.mul
            f32.add
            local.get $l40
            local.get $l65
            f32.mul
            f32.add
            f32.store offset=1304
            local.get $l7
            local.get $l39
            local.get $l66
            f32.mul
            local.get $l37
            local.get $l67
            f32.mul
            f32.add
            local.get $p4
            local.get $l65
            f32.mul
            f32.add
            f32.store offset=1300
            local.get $l7
            local.get $l35
            local.get $l66
            f32.mul
            local.get $l36
            local.get $l67
            f32.mul
            f32.add
            local.get $l34
            local.get $l65
            f32.mul
            f32.add
            f32.store offset=1296
            local.get $l7
            local.get $l38
            local.get $l63
            f32.mul
            local.get $l41
            local.get $l64
            f32.mul
            f32.add
            local.get $l40
            local.get $l43
            f32.mul
            f32.add
            f32.store offset=1288
            local.get $l7
            local.get $l39
            local.get $l63
            f32.mul
            local.get $l37
            local.get $l64
            f32.mul
            f32.add
            local.get $p4
            local.get $l43
            f32.mul
            f32.add
            f32.store offset=1284
            local.get $l7
            local.get $l35
            local.get $l63
            f32.mul
            local.get $l36
            local.get $l64
            f32.mul
            f32.add
            local.get $l34
            local.get $l43
            f32.mul
            f32.add
            f32.store offset=1280
            local.get $l7
            local.get $l41
            local.get $l71
            f32.neg
            local.tee $l43
            f32.mul
            local.get $l38
            local.get $l59
            f32.mul
            f32.sub
            local.get $l40
            local.get $l58
            f32.mul
            f32.sub
            local.get $l38
            local.get $l61
            f32.mul
            local.get $l41
            local.get $l62
            f32.mul
            f32.add
            local.get $l40
            local.get $l60
            f32.mul
            f32.add
            f32.add
            f32.store offset=1336
            local.get $l7
            local.get $l37
            local.get $l43
            f32.mul
            local.get $l39
            local.get $l59
            f32.mul
            f32.sub
            local.get $p4
            local.get $l58
            f32.mul
            f32.sub
            local.get $l39
            local.get $l61
            f32.mul
            local.get $l37
            local.get $l62
            f32.mul
            f32.add
            local.get $p4
            local.get $l60
            f32.mul
            f32.add
            f32.add
            f32.store offset=1332
            local.get $l7
            local.get $l36
            local.get $l43
            f32.mul
            local.get $l35
            local.get $l59
            f32.mul
            f32.sub
            local.get $l34
            local.get $l58
            f32.mul
            f32.sub
            local.get $l35
            local.get $l61
            f32.mul
            local.get $l36
            local.get $l62
            f32.mul
            f32.add
            local.get $l34
            local.get $l60
            f32.mul
            f32.add
            f32.add
            f32.store offset=1328
            local.get $l19
            i32.const 31
            i32.add
            i32.const 5
            i32.shr_u
            local.tee $l31
            i32.eqz
            br_if $B3
            f32.const 0x1.fffffep+127 (;=3.40282e+38;)
            local.set $l37
            local.get $l19
            local.set $l14
            i32.const 0
            local.set $l21
            loop $L4
              block $B5
                local.get $l19
                local.get $l20
                i32.const 5
                i32.shl
                local.tee $l26
                i32.sub
                local.tee $p2
                i32.const 32
                local.get $p2
                i32.const 32
                i32.lt_u
                select
                local.tee $l27
                if $I6
                  local.get $l14
                  i32.const 32
                  local.get $l14
                  i32.const 32
                  i32.lt_u
                  select
                  local.set $l22
                  local.get $p0
                  f32.load offset=4
                  local.get $p0
                  f32.load offset=8
                  f32.mul
                  local.get $p0
                  f32.load offset=12
                  f32.mul
                  local.set $l34
                  local.get $l7
                  i32.load offset=2000
                  local.set $l23
                  i32.const 0
                  local.set $p3
                  loop $L7
                    local.get $l23
                    local.get $p3
                    local.get $l26
                    i32.add
                    i32.const 2
                    i32.shl
                    i32.add
                    i32.load
                    local.set $l12
                    block $B8 (result i32)
                      local.get $l13
                      i32.load8_u offset=64
                      i32.const 2
                      i32.and
                      if $I9
                        local.get $l13
                        i32.load offset=28
                        local.get $l12
                        i32.const 6
                        i32.mul
                        i32.add
                        local.tee $p2
                        i32.load16_u offset=4
                        local.set $l8
                        local.get $p2
                        i32.load16_u offset=2
                        local.set $l10
                        local.get $p2
                        i32.load16_u
                        br $B8
                      end
                      local.get $l13
                      i32.load offset=28
                      local.get $l12
                      i32.const 12
                      i32.mul
                      i32.add
                      local.tee $p2
                      i32.load offset=8
                      local.set $l8
                      local.get $p2
                      i32.load offset=4
                      local.set $l10
                      local.get $p2
                      i32.load
                    end
                    local.set $l9
                    local.get $l7
                    local.get $p3
                    i32.const 40
                    i32.mul
                    i32.add
                    local.tee $p2
                    local.get $l13
                    i32.load offset=24
                    local.tee $l15
                    local.get $l9
                    i32.const 12
                    i32.mul
                    i32.add
                    local.tee $l9
                    f32.load
                    f32.store
                    local.get $p2
                    local.get $l9
                    f32.load offset=4
                    f32.store offset=4
                    local.get $p2
                    local.get $l9
                    f32.load offset=8
                    f32.store offset=8
                    local.get $p2
                    local.get $l15
                    local.get $l8
                    local.get $l10
                    local.get $l34
                    f32.const 0x0p+0 (;=0;)
                    f32.lt
                    local.tee $l24
                    select
                    i32.const 12
                    i32.mul
                    i32.add
                    local.tee $l9
                    f32.load
                    f32.store offset=12
                    local.get $p2
                    local.get $l9
                    f32.load offset=4
                    f32.store offset=16
                    local.get $p2
                    local.get $l9
                    f32.load offset=8
                    f32.store offset=20
                    local.get $p2
                    local.get $l15
                    local.get $l10
                    local.get $l8
                    local.get $l24
                    select
                    i32.const 12
                    i32.mul
                    i32.add
                    local.tee $l8
                    f32.load
                    f32.store offset=24
                    local.get $p2
                    local.get $l8
                    f32.load offset=4
                    f32.store offset=28
                    local.get $p2
                    local.get $l8
                    f32.load offset=8
                    f32.store offset=32
                    local.get $p2
                    local.get $l25
                    if $I10 (result i32)
                      local.get $l12
                      local.get $l25
                      i32.add
                      i32.load8_u
                    else
                      i32.const 56
                    end
                    i32.store8 offset=36
                    local.get $p3
                    i32.const 1
                    i32.add
                    local.tee $p3
                    local.get $l22
                    i32.ne
                    br_if $L7
                  end
                  local.get $l7
                  i32.const 6120
                  i32.add
                  local.get $l7
                  i32.const 1416
                  i32.add
                  i32.load
                  i32.store
                  local.get $l7
                  local.get $l7
                  i64.load offset=1408 align=4
                  i64.store offset=6112
                  i32.const 0
                  local.set $l8
                  local.get $l27
                  i32.eqz
                  br_if $B5
                  i32.const 0
                  local.set $l16
                  loop $L11
                    local.get $l7
                    i32.const 0
                    i32.store offset=2012
                    local.get $l7
                    i32.const 1784
                    i32.add
                    local.get $l7
                    i32.const 1344
                    i32.add
                    local.get $l7
                    local.get $l16
                    i32.const 40
                    i32.mul
                    i32.add
                    local.tee $p2
                    local.get $l16
                    local.get $l26
                    i32.add
                    local.tee $l32
                    local.get $p2
                    i32.load8_u offset=36
                    local.get $l7
                    i32.const 1920
                    i32.add
                    local.get $p5
                    local.get $l7
                    i32.const 1424
                    i32.add
                    local.get $l7
                    i32.const 1280
                    i32.add
                    local.get $l7
                    i32.const 2016
                    i32.add
                    local.get $l7
                    i32.const 2012
                    i32.add
                    call $f70063
                    block $B12
                      local.get $l7
                      i32.load offset=2012
                      local.tee $p2
                      i32.eqz
                      br_if $B12
                      i32.const 0
                      local.set $p3
                      local.get $l7
                      f32.load offset=2060
                      local.set $l34
                      block $B13
                        local.get $p2
                        i32.const 1
                        i32.eq
                        br_if $B13
                        local.get $p2
                        i32.const 1
                        i32.sub
                        local.tee $p3
                        i32.const 3
                        i32.and
                        local.set $l8
                        block $B14
                          local.get $p2
                          i32.const 2
                          i32.sub
                          i32.const 3
                          i32.lt_u
                          if $I15
                            i32.const 0
                            local.set $p3
                            i32.const 1
                            local.set $p2
                            br $B14
                          end
                          local.get $p3
                          i32.const -4
                          i32.and
                          local.set $l10
                          i32.const 0
                          local.set $p3
                          i32.const 1
                          local.set $p2
                          loop $L16
                            local.get $p2
                            i32.const 3
                            i32.add
                            local.tee $l15
                            i32.const 6
                            i32.shl
                            local.get $l7
                            i32.add
                            i32.const 2060
                            i32.add
                            f32.load
                            local.tee $l35
                            local.get $p2
                            i32.const 2
                            i32.add
                            local.tee $l9
                            i32.const 6
                            i32.shl
                            local.get $l7
                            i32.add
                            i32.const 2060
                            i32.add
                            f32.load
                            local.tee $l36
                            local.get $p2
                            i32.const 1
                            i32.add
                            local.tee $l12
                            i32.const 6
                            i32.shl
                            local.get $l7
                            i32.add
                            i32.const 2060
                            i32.add
                            f32.load
                            local.tee $p4
                            local.get $p2
                            i32.const 6
                            i32.shl
                            local.get $l7
                            i32.add
                            i32.const 2060
                            i32.add
                            f32.load
                            local.tee $l39
                            local.get $l34
                            local.get $l34
                            local.get $l39
                            f32.gt
                            local.tee $l24
                            select
                            local.tee $l34
                            local.get $p4
                            local.get $l34
                            f32.lt
                            local.tee $l22
                            select
                            local.tee $l34
                            local.get $l34
                            local.get $l36
                            f32.gt
                            local.tee $l23
                            select
                            local.tee $l34
                            local.get $l34
                            local.get $l35
                            f32.gt
                            local.tee $l33
                            select
                            local.set $l34
                            local.get $l15
                            local.get $l9
                            local.get $l12
                            local.get $p2
                            local.get $p3
                            local.get $l24
                            select
                            local.get $l22
                            select
                            local.get $l23
                            select
                            local.get $l33
                            select
                            local.set $p3
                            local.get $p2
                            i32.const 4
                            i32.add
                            local.set $p2
                            local.get $l10
                            i32.const 4
                            i32.sub
                            local.tee $l10
                            br_if $L16
                          end
                        end
                        local.get $l8
                        i32.eqz
                        br_if $B13
                        loop $L17
                          local.get $p2
                          i32.const 6
                          i32.shl
                          local.get $l7
                          i32.add
                          i32.const 2060
                          i32.add
                          f32.load
                          local.tee $l35
                          local.get $l34
                          local.get $l34
                          local.get $l35
                          f32.gt
                          local.tee $l10
                          select
                          local.set $l34
                          local.get $p2
                          local.get $p3
                          local.get $l10
                          select
                          local.set $p3
                          local.get $p2
                          i32.const 1
                          i32.add
                          local.set $p2
                          local.get $l8
                          i32.const 1
                          i32.sub
                          local.tee $l8
                          br_if $L17
                        end
                      end
                      i32.const 1
                      local.set $l8
                      local.get $l34
                      local.get $l37
                      f32.lt
                      i32.eqz
                      br_if $B12
                      local.get $l7
                      i32.const 2016
                      i32.add
                      local.get $p3
                      i32.const 6
                      i32.shl
                      i32.add
                      local.tee $p2
                      f32.load offset=16
                      local.set $l45
                      local.get $p2
                      f32.load offset=32
                      local.set $l48
                      local.get $p2
                      f32.load offset=24
                      local.set $l42
                      local.get $p2
                      f32.load offset=20
                      local.set $l44
                      local.get $p2
                      f32.load offset=40
                      local.set $l46
                      local.get $p2
                      f32.load offset=36
                      local.set $l47
                      local.get $l32
                      local.set $l11
                      local.get $l34
                      local.set $l37
                    end
                    local.get $l16
                    i32.const 1
                    i32.add
                    local.tee $l16
                    local.get $l27
                    i32.ne
                    br_if $L11
                  end
                  local.get $l8
                  local.get $l21
                  i32.or
                  local.set $l21
                  br $B5
                end
                local.get $l7
                i32.const 6120
                i32.add
                local.get $l7
                i32.const 1416
                i32.add
                i32.load
                i32.store
                local.get $l7
                local.get $l7
                i64.load offset=1408 align=4
                i64.store offset=6112
              end
              local.get $l7
              i32.const 1416
              i32.add
              local.get $l7
              i32.const 6120
              i32.add
              i32.load
              i32.store
              local.get $l7
              local.get $l7
              i64.load offset=6112
              i64.store offset=1408
              local.get $l14
              i32.const 32
              i32.sub
              local.set $l14
              local.get $l20
              i32.const 1
              i32.add
              local.tee $l20
              local.get $l31
              i32.ne
              br_if $L4
            end
            local.get $l21
            i32.const 1
            i32.and
            i32.eqz
            br_if $B3
            local.get $l7
            f32.load offset=1448
            local.get $l7
            f32.load offset=1432
            local.tee $l34
            local.get $l45
            local.get $l7
            f32.load offset=1424
            local.tee $l35
            f32.mul
            local.get $l44
            local.get $l7
            f32.load offset=1428
            local.tee $l36
            f32.mul
            f32.add
            local.get $l42
            local.get $l34
            f32.mul
            f32.add
            local.tee $l40
            f32.mul
            local.get $l7
            f32.load offset=1436
            local.tee $p4
            local.get $l44
            local.get $l35
            f32.mul
            local.get $l45
            local.get $l36
            f32.mul
            f32.sub
            f32.mul
            local.get $l42
            local.get $p4
            local.get $p4
            f32.mul
            f32.const -0x1p-1 (;=-0.5;)
            f32.add
            local.tee $l39
            f32.mul
            f32.add
            f32.add
            local.tee $l38
            local.get $l38
            f32.add
            f32.add
            local.set $l55
            local.get $l7
            f32.load offset=1444
            local.get $l36
            local.get $l40
            f32.mul
            local.get $p4
            local.get $l45
            local.get $l34
            f32.mul
            local.get $l42
            local.get $l35
            f32.mul
            f32.sub
            f32.mul
            local.get $l44
            local.get $l39
            f32.mul
            f32.add
            f32.add
            local.tee $l38
            local.get $l38
            f32.add
            f32.add
            local.set $l56
            local.get $l7
            f32.load offset=1440
            local.get $l35
            local.get $l40
            f32.mul
            local.get $p4
            local.get $l42
            local.get $l36
            f32.mul
            local.get $l44
            local.get $l34
            f32.mul
            f32.sub
            f32.mul
            local.get $l45
            local.get $l39
            f32.mul
            f32.add
            f32.add
            local.tee $l40
            local.get $l40
            f32.add
            f32.add
            local.set $l57
            local.get $l34
            local.get $l48
            local.get $l35
            f32.mul
            local.get $l47
            local.get $l36
            f32.mul
            f32.add
            local.get $l46
            local.get $l34
            f32.mul
            f32.add
            local.tee $l40
            f32.mul
            local.get $p4
            local.get $l47
            local.get $l35
            f32.mul
            local.get $l48
            local.get $l36
            f32.mul
            f32.sub
            f32.mul
            local.get $l46
            local.get $l39
            f32.mul
            f32.add
            f32.add
            local.tee $l38
            local.get $l38
            f32.add
            local.set $l41
            local.get $l36
            local.get $l40
            f32.mul
            local.get $p4
            local.get $l48
            local.get $l34
            f32.mul
            local.get $l46
            local.get $l35
            f32.mul
            f32.sub
            f32.mul
            local.get $l47
            local.get $l39
            f32.mul
            f32.add
            f32.add
            local.tee $l38
            local.get $l38
            f32.add
            local.set $l38
            local.get $l35
            local.get $l40
            f32.mul
            local.get $p4
            local.get $l46
            local.get $l36
            f32.mul
            local.get $l47
            local.get $l34
            f32.mul
            f32.sub
            f32.mul
            local.get $l48
            local.get $l39
            f32.mul
            f32.add
            f32.add
            local.tee $l34
            local.get $l34
            f32.add
            local.set $l34
            local.get $l7
            i32.load offset=2000
            local.get $l11
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.set $l11
            local.get $l37
            f32.const 0x0p+0 (;=0;)
            f32.le
            i32.eqz
            if $I18
              i32.const 1
              local.set $l17
              local.get $l18
              br_if $B3
              local.get $p6
              local.get $l41
              f32.store offset=36
              local.get $p6
              local.get $l38
              f32.store offset=32
              local.get $p6
              local.get $l34
              f32.store offset=28
              local.get $p6
              local.get $l55
              f32.store offset=24
              local.get $p6
              local.get $l56
              f32.store offset=20
              local.get $p6
              local.get $l57
              f32.store offset=16
              local.get $p6
              i32.const 0
              i32.store offset=40
              local.get $p6
              local.get $l11
              i32.store offset=8
              br $B1
            end
            local.get $l7
            local.get $l54
            local.get $l37
            local.get $l41
            f32.mul
            local.tee $l35
            f32.sub
            local.tee $l54
            f32.store offset=1980
            local.get $l7
            local.get $l53
            local.get $l37
            local.get $l38
            f32.mul
            local.tee $l36
            f32.sub
            local.tee $l53
            f32.store offset=1976
            local.get $l7
            local.get $l52
            local.get $l37
            local.get $l34
            f32.mul
            local.tee $l34
            f32.sub
            local.tee $l52
            f32.store offset=1972
            local.get $l49
            local.get $l35
            f32.sub
            local.set $l49
            local.get $l50
            local.get $l36
            f32.sub
            local.set $l50
            local.get $l51
            local.get $l34
            f32.sub
            local.set $l51
            i32.const 1
            local.set $l17
            local.get $l18
            i32.const 1
            i32.add
            local.tee $l18
            i32.const 4
            i32.ne
            br_if $L2
          end
        end
        i32.const 0
        local.get $l17
        i32.eqz
        br_if $B0
        drop
        local.get $p6
        local.get $l55
        f32.store offset=24
        local.get $p6
        local.get $l56
        f32.store offset=20
        local.get $p6
        local.get $l57
        f32.store offset=16
        local.get $p6
        local.get $l11
        i32.store offset=8
        local.get $p6
        local.get $l49
        local.get $l49
        f32.mul
        local.get $l50
        local.get $l50
        f32.mul
        local.get $l51
        local.get $l51
        f32.mul
        f32.add
        f32.add
        f32.sqrt
        local.tee $l34
        f32.neg
        f32.store offset=40
        local.get $p6
        local.get $l49
        f32.const 0x1p+0 (;=1;)
        local.get $l34
        f32.div
        local.tee $l35
        f32.mul
        f32.const 0x0p+0 (;=0;)
        local.get $l34
        f32.const 0x0p+0 (;=0;)
        f32.gt
        local.tee $p2
        select
        f32.store offset=36
        local.get $p6
        local.get $l50
        local.get $l35
        f32.mul
        f32.const 0x0p+0 (;=0;)
        local.get $p2
        select
        f32.store offset=32
        local.get $p6
        local.get $l51
        local.get $l35
        f32.mul
        f32.const 0x0p+0 (;=0;)
        local.get $p2
        select
        f32.store offset=28
      end
      i32.const 1
    end
    local.set $p2
    block $B19
      local.get $l7
      i32.load offset=2008
      local.tee $p3
      i32.const 0
      i32.lt_s
      br_if $B19
      local.get $p3
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if $B19
      local.get $l7
      i32.load offset=2000
      local.tee $p3
      i32.eqz
      br_if $B19
      call $f69753
      local.tee $l8
      local.get $p3
      local.get $l8
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $l7
    i32.const 6128
    i32.add
    global.set $g0
    local.get $p2)
