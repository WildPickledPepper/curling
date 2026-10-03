  (func $f69898 (type $t18) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (result i32)
    (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32) (local $l30 f32) (local $l31 f32) (local $l32 f32) (local $l33 f32) (local $l34 f32) (local $l35 f32) (local $l36 f32) (local $l37 f32)
    global.get $g0
    i32.const 6336
    i32.sub
    local.tee $l11
    global.set $g0
    local.get $p4
    if $I0
      loop $L1
        local.get $l11
        i32.const 16
        i32.add
        local.get $p0
        local.get $p2
        local.get $l14
        i32.add
        i32.load8_u
        local.get $p0
        i32.load
        i32.load
        call_indirect $__indirect_function_table (type $t2)
        local.get $l14
        i32.const 4
        i32.shl
        local.tee $l16
        local.get $l11
        i32.const 6272
        i32.add
        i32.add
        local.tee $l8
        local.get $l11
        i64.load offset=24
        i64.store offset=8
        local.get $l8
        local.get $l11
        i64.load offset=16
        i64.store
        local.get $l11
        i32.const 16
        i32.add
        local.get $p1
        local.get $p3
        local.get $l14
        i32.add
        i32.load8_u
        local.get $p1
        i32.load
        i32.load
        call_indirect $__indirect_function_table (type $t2)
        local.get $l11
        i32.const 6208
        i32.add
        local.get $l16
        i32.add
        local.tee $l16
        local.get $l11
        i64.load offset=24
        i64.store offset=8
        local.get $l16
        local.get $l11
        i64.load offset=16
        i64.store
        local.get $l14
        i32.const 1
        i32.add
        local.tee $l14
        local.get $p4
        i32.ne
        br_if $L1
      end
    end
    local.get $l11
    i32.const 6192
    i32.add
    i32.const 0
    i32.store
    local.get $l11
    i32.const 5932
    i32.add
    i32.const 0
    i32.store
    local.get $l11
    i32.const 5668
    i32.add
    i32.const 0
    i32.store8
    local.get $l11
    i32.const 5664
    i32.add
    i32.const 0
    i32.store
    local.get $l11
    i32.const 0
    i32.store offset=5672
    local.get $l11
    i32.const 0
    i32.store offset=16
    local.get $l11
    local.get $l11
    i32.const 16
    i32.add
    i32.const 8
    i32.or
    i32.store offset=20
    local.get $l11
    local.get $p6
    i64.load
    i64.store
    local.get $l11
    local.get $p6
    i64.load offset=8
    i64.store offset=8
    local.get $p0
    local.set $p6
    local.get $p1
    local.set $l14
    local.get $p5
    local.set $l16
    global.get $g0
    i32.const 96
    i32.sub
    local.tee $l9
    global.set $g0
    local.get $l9
    i32.const 2139095039
    i32.store offset=80
    local.get $l11
    i32.const 16
    i32.add
    local.tee $l8
    local.get $l11
    i32.const 6272
    i32.add
    local.tee $p1
    i64.load
    i64.store offset=272
    local.get $l8
    i32.const 280
    i32.add
    local.tee $l15
    local.get $p1
    i64.load offset=8
    i64.store
    local.get $l8
    i32.const 288
    i32.add
    local.tee $l10
    local.get $p1
    i64.load offset=16
    i64.store
    local.get $l8
    i32.const 296
    i32.add
    local.tee $l12
    local.get $p1
    i64.load offset=24
    i64.store
    local.get $l8
    i32.const 304
    i32.add
    local.tee $p2
    local.get $p1
    i64.load offset=32
    i64.store
    local.get $l8
    i32.const 312
    i32.add
    local.tee $l19
    local.get $p1
    i64.load offset=40
    i64.store
    local.get $l8
    i32.const 328
    i32.add
    local.tee $p5
    local.get $p1
    i64.load offset=56
    i64.store
    local.get $l8
    i32.const 320
    i32.add
    local.tee $l17
    local.get $p1
    i64.load offset=48
    i64.store
    local.get $l8
    i32.const 1304
    i32.add
    local.tee $l18
    local.get $l11
    i32.const 6208
    i32.add
    local.tee $p0
    i64.load offset=8
    i64.store
    local.get $l8
    local.get $p0
    i64.load
    i64.store offset=1296
    local.get $l8
    i32.const 1312
    i32.add
    local.tee $l13
    local.get $p0
    i64.load offset=16
    i64.store
    local.get $l8
    i32.const 1320
    i32.add
    local.tee $l20
    local.get $p0
    i64.load offset=24
    i64.store
    local.get $l8
    i32.const 1328
    i32.add
    local.tee $p3
    local.get $p0
    i64.load offset=32
    i64.store
    local.get $l8
    i32.const 1336
    i32.add
    local.tee $l21
    local.get $p0
    i64.load offset=40
    i64.store
    local.get $l8
    i32.const 1352
    i32.add
    local.tee $l22
    local.get $p0
    i64.load offset=56
    i64.store
    local.get $l8
    i32.const 1344
    i32.add
    local.tee $l23
    local.get $p0
    i64.load offset=48
    i64.store
    local.get $l9
    i32.const 0
    i32.store offset=76
    local.get $l8
    i32.const 0
    i32.store
    block $B2
      block $B3
        block $B4
          block $B5
            block $B6
              block $B7
                local.get $p4
                i32.const 1
                i32.sub
                br_table $B7 $B6 $B5 $B4 $B3
              end
              i32.const 7
              local.set $p0
              local.get $l9
              i32.const 76
              i32.add
              local.set $p3
              local.get $l9
              i32.const 80
              i32.add
              local.set $p4
              global.get $g0
              i32.const 48
              i32.sub
              local.tee $p2
              global.set $g0
              local.get $p2
              i64.const 0
              i64.store offset=8
              local.get $p2
              i64.const 1065353216
              i64.store
              local.get $l8
              local.tee $p1
              f32.load offset=276
              local.set $l24
              local.get $l8
              i32.const 1300
              i32.add
              f32.load
              local.set $l25
              local.get $l8
              f32.load offset=280
              local.set $l26
              local.get $l8
              i32.const 1304
              i32.add
              f32.load
              local.set $l27
              local.get $l8
              f32.load offset=272
              local.set $l28
              local.get $l8
              f32.load offset=1296
              local.set $l29
              local.get $p2
              i64.const 2147483648
              i64.store offset=24
              local.get $p2
              i64.const -9223372033641938944
              i64.store offset=16
              local.get $p2
              i32.const 32
              i32.add
              local.get $p6
              local.get $p2
              i32.const 16
              i32.add
              local.get $p6
              i32.load
              i32.load offset=4
              call_indirect $__indirect_function_table (type $t2)
              local.get $p2
              i32.const 16
              i32.add
              local.get $l14
              local.get $p2
              local.get $l14
              i32.load
              i32.load offset=4
              call_indirect $__indirect_function_table (type $t2)
              local.get $l8
              local.get $p2
              i64.load offset=32
              i64.store offset=288
              local.get $l8
              local.get $p2
              i64.load offset=40
              i64.store offset=296
              local.get $l8
              i32.const 1312
              i32.add
              local.get $p2
              i64.load offset=16
              i64.store
              local.get $l8
              i32.const 1320
              i32.add
              local.get $p2
              i64.load offset=24
              i64.store
              block $B8 (result i32)
                block $B9
                  local.get $l28
                  local.get $l29
                  f32.sub
                  local.get $p2
                  f32.load offset=32
                  local.get $p2
                  f32.load offset=16
                  f32.sub
                  f32.ne
                  br_if $B9
                  local.get $l24
                  local.get $l25
                  f32.sub
                  local.get $p2
                  f32.load offset=36
                  local.get $p2
                  f32.load offset=20
                  f32.sub
                  f32.ne
                  br_if $B9
                  i32.const 0
                  local.get $l26
                  local.get $l27
                  f32.sub
                  local.get $p2
                  f32.load offset=40
                  local.get $p2
                  f32.load offset=24
                  f32.sub
                  f32.eq
                  br_if $B8
                  drop
                end
                local.get $p1
                local.get $p6
                local.get $l14
                local.get $p3
                local.get $p4
                call $f69899
              end
              local.set $p1
              local.get $p2
              i32.const 48
              i32.add
              global.set $g0
              local.get $p1
              br_if $B3
              br $B2
            end
            i32.const 7
            local.set $p0
            local.get $l8
            local.get $p6
            local.get $l14
            local.get $l9
            i32.const 76
            i32.add
            local.get $l9
            i32.const 80
            i32.add
            call $f69899
            br_if $B3
            br $B2
          end
          local.get $l9
          i32.const 3
          i32.store offset=76
          local.get $l8
          i32.const 0
          i32.const 1
          i32.const 2
          local.get $l9
          i32.const 80
          i32.add
          call $f69900
          local.set $p0
          local.get $l8
          i32.const 1
          i32.const 0
          i32.const 2
          local.get $l9
          i32.const 80
          i32.add
          call $f69900
          local.set $p1
          local.get $l8
          i32.load
          i32.eqz
          if $I10
            i32.const 7
            local.set $p0
            br $B2
          end
          local.get $p0
          i32.const 0
          i32.store8 offset=32
          local.get $p0
          local.get $p1
          i32.store offset=20
          local.get $p1
          i32.const 0
          i32.store8 offset=32
          local.get $p1
          local.get $p0
          i32.store offset=20
          local.get $p0
          i32.const 2
          i32.store8 offset=33
          local.get $p0
          local.get $p1
          i32.store offset=24
          local.get $p1
          i32.const 1
          i32.store8 offset=34
          local.get $p1
          local.get $p0
          i32.store offset=28
          local.get $p0
          i32.const 1
          i32.store8 offset=34
          local.get $p0
          local.get $p1
          i32.store offset=28
          local.get $p1
          i32.const 2
          i32.store8 offset=33
          local.get $p1
          local.get $p0
          i32.store offset=24
          br $B3
        end
        local.get $p5
        f32.load
        local.get $l22
        f32.load
        f32.sub
        local.get $l15
        f32.load
        local.get $l18
        f32.load
        f32.sub
        local.tee $l24
        f32.sub
        local.get $l10
        f32.load
        local.get $l13
        f32.load
        f32.sub
        local.get $l8
        f32.load offset=272
        local.get $l8
        f32.load offset=1296
        f32.sub
        local.tee $l27
        f32.sub
        local.tee $l26
        local.get $l8
        f32.load offset=308
        local.get $l8
        i32.const 1332
        i32.add
        f32.load
        f32.sub
        local.get $l8
        f32.load offset=276
        local.get $l8
        i32.const 1300
        i32.add
        f32.load
        f32.sub
        local.tee $l28
        f32.sub
        local.tee $l29
        f32.mul
        local.get $l8
        f32.load offset=292
        local.get $l8
        i32.const 1316
        i32.add
        f32.load
        f32.sub
        local.get $l28
        f32.sub
        local.tee $l30
        local.get $p2
        f32.load
        local.get $p3
        f32.load
        f32.sub
        local.get $l27
        f32.sub
        local.tee $l31
        f32.mul
        f32.sub
        local.tee $l25
        f32.const 0x1p+0 (;=1;)
        local.get $l25
        local.get $l25
        f32.mul
        local.get $l30
        local.get $l19
        f32.load
        local.get $l21
        f32.load
        f32.sub
        local.get $l24
        f32.sub
        local.tee $l25
        f32.mul
        local.get $l12
        f32.load
        local.get $l20
        f32.load
        f32.sub
        local.get $l24
        f32.sub
        local.tee $l30
        local.get $l29
        f32.mul
        f32.sub
        local.tee $l24
        local.get $l24
        f32.mul
        local.get $l30
        local.get $l31
        f32.mul
        local.get $l26
        local.get $l25
        f32.mul
        f32.sub
        local.tee $l25
        local.get $l25
        f32.mul
        f32.add
        f32.add
        f32.sqrt
        f32.div
        local.tee $l26
        f32.mul
        f32.mul
        local.get $l17
        f32.load
        local.get $l23
        f32.load
        f32.sub
        local.get $l27
        f32.sub
        local.get $l24
        local.get $l26
        f32.mul
        f32.mul
        local.get $l8
        f32.load offset=324
        local.get $l8
        i32.const 1348
        i32.add
        f32.load
        f32.sub
        local.get $l28
        f32.sub
        local.get $l25
        local.get $l26
        f32.mul
        f32.mul
        f32.add
        f32.add
        f32.const 0x0p+0 (;=0;)
        f32.gt
        if $I11
          local.get $l10
          local.get $p1
          i32.const 32
          i32.add
          local.tee $p4
          i64.load
          i64.store
          local.get $l10
          local.get $p4
          i64.load offset=8
          i64.store offset=8
          local.get $l13
          local.get $p0
          i32.const 32
          i32.add
          local.tee $p4
          i64.load
          i64.store
          local.get $l13
          local.get $p4
          i64.load offset=8
          i64.store offset=8
          local.get $p2
          local.get $p1
          i32.const 16
          i32.add
          local.tee $p1
          i64.load
          i64.store
          local.get $p2
          local.get $p1
          i64.load offset=8
          i64.store offset=8
          local.get $p3
          local.get $p0
          i32.const 16
          i32.add
          local.tee $p0
          i64.load
          i64.store
          local.get $p3
          local.get $p0
          i64.load offset=8
          i64.store offset=8
        end
        local.get $l8
        i32.const 0
        i32.const 1
        i32.const 2
        local.get $l9
        i32.const 80
        i32.add
        call $f69900
        local.set $p0
        local.get $l8
        i32.const 0
        i32.const 3
        i32.const 1
        local.get $l9
        i32.const 80
        i32.add
        call $f69900
        local.set $p1
        local.get $l8
        i32.const 0
        i32.const 2
        i32.const 3
        local.get $l9
        i32.const 80
        i32.add
        call $f69900
        local.set $p4
        local.get $l8
        i32.const 1
        i32.const 3
        i32.const 2
        local.get $l9
        i32.const 80
        i32.add
        call $f69900
        local.set $l10
        local.get $l8
        i32.load
        i32.eqz
        if $I12
          i32.const 7
          local.set $p0
          br $B2
        end
        local.get $p0
        i32.const 2
        i32.store8 offset=32
        local.get $p0
        local.get $p1
        i32.store offset=20
        local.get $p1
        i32.const 0
        i32.store8 offset=34
        local.get $p1
        local.get $p0
        i32.store offset=28
        local.get $p0
        i32.const 2
        i32.store8 offset=33
        local.get $p0
        local.get $l10
        i32.store offset=24
        local.get $l10
        i32.const 1
        i32.store8 offset=34
        local.get $l10
        local.get $p0
        i32.store offset=28
        local.get $p0
        i32.const 0
        i32.store8 offset=34
        local.get $p0
        local.get $p4
        i32.store offset=28
        local.get $p4
        i32.const 2
        i32.store8 offset=32
        local.get $p4
        local.get $p0
        i32.store offset=20
        local.get $p1
        i32.const 2
        i32.store8 offset=32
        local.get $p1
        local.get $p4
        i32.store offset=20
        local.get $p4
        i32.const 0
        i32.store8 offset=34
        local.get $p4
        local.get $p1
        i32.store offset=28
        local.get $p1
        i32.const 0
        i32.store8 offset=33
        local.get $p1
        local.get $l10
        i32.store offset=24
        local.get $l10
        i32.const 1
        i32.store8 offset=32
        local.get $l10
        local.get $p1
        i32.store offset=20
        local.get $p4
        i32.const 1
        i32.store8 offset=33
        local.get $p4
        local.get $l10
        i32.store offset=24
        local.get $l10
        i32.const 1
        i32.store8 offset=33
        local.get $l10
        local.get $p4
        i32.store offset=24
        local.get $l9
        i32.const 4
        i32.store offset=76
      end
      local.get $l8
      i32.const 1296
      i32.add
      local.set $l17
      local.get $l8
      i32.const 272
      i32.add
      local.set $l18
      local.get $l8
      i32.const 5392
      i32.add
      local.set $l20
      local.get $l8
      i32.const 5656
      i32.add
      local.set $p0
      local.get $l14
      i32.load offset=4
      f32.load offset=20
      local.tee $l24
      local.get $p6
      i32.load offset=4
      f32.load offset=20
      local.tee $l27
      local.get $l24
      local.get $l27
      f32.lt
      select
      f32.const 0x1.99999ap-4 (;=0.1;)
      f32.mul
      local.set $l32
      loop $L13
        block $B14
          local.get $l8
          i32.load offset=6176
          local.tee $p4
          i32.eqz
          br_if $B14
          local.get $p4
          i32.const 1
          i32.and
          local.set $p3
          i32.const 0
          local.set $p1
          local.get $p4
          i32.const 1
          i32.ne
          if $I15
            local.get $p4
            i32.const -2
            i32.and
            local.set $l10
            loop $L16
              local.get $p0
              local.set $p4
              local.get $p0
              local.get $p1
              i32.const 2
              i32.shl
              local.tee $p2
              i32.add
              i32.load offset=264
              local.tee $l13
              local.get $l8
              i32.load offset=5656
              i32.const 1
              i32.sub
              i32.ne
              if $I17 (result i32)
                local.get $l8
                local.get $l8
                i32.load offset=5916
                local.tee $p4
                i32.const 1
                i32.add
                i32.store offset=5916
                local.get $l8
                local.get $p4
                i32.const 2
                i32.shl
                i32.add
                i32.const 5660
                i32.add
              else
                local.get $p4
              end
              local.get $l13
              i32.store
              local.get $p0
              local.set $p4
              local.get $p0
              local.get $p2
              i32.const 4
              i32.or
              i32.add
              i32.load offset=264
              local.tee $p2
              local.get $l8
              i32.load offset=5656
              i32.const 1
              i32.sub
              i32.ne
              if $I18 (result i32)
                local.get $l8
                local.get $l8
                i32.load offset=5916
                local.tee $p4
                i32.const 1
                i32.add
                i32.store offset=5916
                local.get $l8
                local.get $p4
                i32.const 2
                i32.shl
                i32.add
                i32.const 5660
                i32.add
              else
                local.get $p4
              end
              local.get $p2
              i32.store
              local.get $p1
              i32.const 2
              i32.add
              local.set $p1
              local.get $l10
              i32.const 2
              i32.sub
              local.tee $l10
              br_if $L16
            end
          end
          local.get $p3
          i32.eqz
          br_if $B14
          local.get $p0
          local.set $p4
          local.get $p0
          local.get $p1
          i32.const 2
          i32.shl
          i32.add
          i32.load offset=264
          local.tee $p1
          local.get $l8
          i32.load offset=5656
          i32.const 1
          i32.sub
          i32.ne
          if $I19 (result i32)
            local.get $l8
            local.get $l8
            i32.load offset=5916
            local.tee $p4
            i32.const 1
            i32.add
            i32.store offset=5916
            local.get $l8
            local.get $p4
            i32.const 2
            i32.shl
            i32.add
            i32.const 5660
            i32.add
          else
            local.get $p4
          end
          local.get $p1
          i32.store
        end
        i32.const 0
        local.set $p3
        local.get $l8
        i32.const 0
        i32.store offset=6176
        local.get $l8
        local.get $l8
        i32.load
        i32.const 1
        i32.sub
        local.tee $l13
        i32.store
        local.get $l8
        i32.load offset=4
        local.tee $p1
        local.get $l13
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.set $l15
        local.get $p1
        i32.load
        local.set $l12
        block $B20
          local.get $l13
          i32.const 2
          i32.lt_u
          br_if $B20
          i32.const 1
          local.set $p4
          i32.const 2
          local.set $l10
          loop $L21 (result i32)
            local.get $l15
            f32.load offset=16
            local.get $p1
            local.get $p4
            local.get $l10
            local.get $l13
            i32.lt_u
            local.get $p1
            local.get $l10
            i32.const 2
            i32.shl
            i32.add
            i32.load
            f32.load offset=16
            local.get $p1
            local.get $p4
            i32.const 2
            i32.shl
            i32.add
            i32.load
            f32.load offset=16
            f32.lt
            i32.and
            i32.add
            local.tee $p2
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.tee $p4
            f32.load offset=16
            f32.lt
            br_if $B20
            local.get $p1
            local.get $p3
            i32.const 2
            i32.shl
            i32.add
            local.get $p4
            i32.store
            local.get $l8
            i32.load offset=4
            local.set $p1
            local.get $l13
            local.get $p2
            i32.const 1
            i32.shl
            local.tee $l10
            i32.const 1
            i32.or
            local.tee $p4
            i32.le_u
            if $I22 (result i32)
              local.get $p2
            else
              local.get $l10
              i32.const 2
              i32.add
              local.set $l10
              local.get $p2
              local.set $p3
              br $L21
            end
          end
          local.set $p3
        end
        local.get $p1
        local.get $p3
        i32.const 2
        i32.shl
        i32.add
        local.get $l15
        i32.store
        local.get $l12
        i32.const 0
        i32.store8 offset=39
        block $B23
          local.get $l12
          i32.load8_u offset=38
          i32.eqz
          if $I24
            local.get $l9
            local.get $l12
            i64.load
            i64.store offset=32
            local.get $l9
            local.get $l12
            i64.load offset=8
            i64.store offset=40
            local.get $l12
            f32.load offset=16
            local.set $l26
            local.get $l9
            i32.const 16
            i32.add
            local.get $p6
            local.get $l9
            i32.const 32
            i32.add
            local.get $p6
            i32.load
            i32.load offset=4
            call_indirect $__indirect_function_table (type $t2)
            local.get $l9
            f32.load offset=28
            local.set $l33
            local.get $l9
            f32.load offset=24
            local.set $l24
            local.get $l9
            f32.load offset=16
            local.set $l27
            local.get $l9
            f32.load offset=20
            local.set $l28
            local.get $l9
            i32.const 0
            i32.store offset=12
            local.get $l9
            local.get $l9
            f32.load offset=40
            f32.neg
            f32.store offset=8
            local.get $l9
            local.get $l9
            f32.load offset=36
            f32.neg
            f32.store offset=4
            local.get $l9
            local.get $l9
            f32.load offset=32
            f32.neg
            f32.store
            local.get $l9
            i32.const 16
            i32.add
            local.get $l14
            local.get $l9
            local.get $l14
            i32.load
            i32.load offset=4
            call_indirect $__indirect_function_table (type $t2)
            local.get $l9
            i32.const 0
            i32.store offset=60
            local.get $l9
            local.get $l28
            local.get $l9
            f32.load offset=20
            local.tee $l34
            f32.sub
            local.tee $l25
            f32.store offset=52
            local.get $l9
            f32.load offset=36
            local.set $l29
            local.get $l9
            local.get $l27
            local.get $l9
            f32.load offset=16
            local.tee $l35
            f32.sub
            local.tee $l30
            f32.store offset=48
            local.get $l9
            f32.load offset=32
            local.set $l31
            local.get $l9
            local.get $l24
            local.get $l9
            f32.load offset=24
            local.tee $l36
            f32.sub
            local.tee $l37
            f32.store offset=56
            local.get $l30
            local.get $l31
            f32.mul
            local.get $l25
            local.get $l29
            f32.mul
            f32.add
            local.get $l37
            local.get $l9
            f32.load offset=40
            f32.mul
            f32.add
            local.tee $l25
            local.get $l26
            f32.sub
            f32.abs
            local.get $l32
            f32.le
            if $I25
              local.get $l18
              local.get $l17
              local.get $l12
              local.get $p6
              local.get $l14
              local.get $l16
              local.get $p7
              call $f69901
              local.get $l16
              if $I26
                i32.const 6
                local.set $p0
                local.get $l11
                f32.load
                f32.const 0x1.0624dep-10 (;=0.001;)
                f32.mul
                local.get $p7
                f32.load offset=64
                f32.abs
                f32.add
                local.get $p7
                f32.load
                local.get $p7
                f32.load offset=16
                f32.sub
                local.tee $l24
                local.get $l24
                f32.mul
                local.get $p7
                f32.load offset=4
                local.get $p7
                f32.load offset=20
                f32.sub
                local.tee $l24
                local.get $l24
                f32.mul
                f32.add
                local.get $p7
                f32.load offset=8
                local.get $p7
                f32.load offset=24
                f32.sub
                local.tee $l24
                local.get $l24
                f32.mul
                f32.add
                local.tee $l24
                f32.sqrt
                f32.const 0x0p+0 (;=0;)
                local.get $l24
                f32.const 0x0p+0 (;=0;)
                f32.gt
                select
                f32.lt
                br_if $B2
              end
              i32.const 5
              local.set $p0
              br $B2
            end
            local.get $l9
            i32.load offset=76
            local.set $l15
            local.get $l9
            f32.load offset=28
            local.set $l26
            local.get $l9
            local.get $l25
            local.get $l9
            f32.load offset=80
            local.tee $l29
            local.get $l25
            local.get $l29
            f32.lt
            select
            f32.store offset=80
            local.get $l8
            local.get $l15
            i32.const 4
            i32.shl
            i32.add
            local.tee $p1
            local.get $l27
            f32.store offset=272
            local.get $p1
            local.get $l33
            f32.store offset=284
            local.get $p1
            local.get $l24
            f32.store offset=280
            local.get $p1
            local.get $l28
            f32.store offset=276
            local.get $p1
            i32.const 1296
            i32.add
            local.get $l35
            f32.store
            local.get $p1
            i32.const 1308
            i32.add
            local.get $l26
            f32.store
            local.get $p1
            i32.const 1304
            i32.add
            local.get $l36
            f32.store
            local.get $p1
            i32.const 1300
            i32.add
            local.get $l34
            f32.store
            local.get $l9
            local.get $l15
            i32.const 1
            i32.add
            i32.store offset=76
            local.get $l8
            i32.const 0
            i32.store8 offset=5652
            local.get $l8
            i32.const 0
            i32.store offset=5648
            local.get $l12
            i32.const 1
            i32.store8 offset=38
            local.get $l12
            i32.load offset=20
            local.get $l12
            i32.load8_s offset=32
            local.get $l9
            i32.const 48
            i32.add
            local.get $l18
            local.get $l17
            local.get $l20
            local.get $p0
            call $f69902
            local.get $l12
            i32.load offset=24
            local.get $l12
            i32.load8_s offset=33
            local.get $l9
            i32.const 48
            i32.add
            local.get $l18
            local.get $l17
            local.get $l20
            local.get $p0
            call $f69902
            local.get $l12
            i32.load offset=28
            local.get $l12
            i32.load8_s offset=34
            local.get $l9
            i32.const 48
            i32.add
            local.get $l18
            local.get $l17
            local.get $l20
            local.get $p0
            call $f69902
            local.get $l8
            i32.load offset=5648
            local.tee $l19
            i32.eqz
            br_if $B23
            local.get $l8
            i32.load8_u offset=5652
            br_if $B23
            local.get $l19
            local.get $l8
            i32.load offset=5916
            local.get $l8
            i32.load offset=5656
            i32.sub
            i32.const -64
            i32.sub
            i32.gt_u
            br_if $B23
            local.get $l8
            local.get $l8
            i32.load offset=5392
            i32.const 35
            i32.add
            local.tee $p1
            local.get $l8
            i32.load offset=5396
            local.tee $p4
            i32.const 2
            i32.shl
            i32.const 3122800
            i32.add
            i32.load
            i32.add
            i32.load8_s
            local.get $p1
            local.get $p4
            i32.add
            i32.load8_s
            local.get $l15
            local.get $l9
            i32.const 80
            i32.add
            call $f69900
            local.set $p5
            local.get $l8
            i32.load offset=5392
            local.set $p1
            local.get $p5
            local.get $l8
            i32.load offset=5396
            local.tee $p4
            i32.store8 offset=32
            local.get $p5
            local.get $p1
            i32.store offset=20
            local.get $p1
            local.get $p4
            i32.const 2
            i32.shl
            i32.add
            local.get $p5
            i32.store offset=20
            local.get $p1
            local.get $p4
            i32.add
            i32.const 0
            i32.store8 offset=32
            i32.const 1
            local.set $p2
            local.get $p5
            local.set $p4
            local.get $l19
            i32.const 2
            i32.ge_u
            if $I27
              loop $L28
                local.get $l8
                local.get $l8
                local.get $p2
                i32.const 3
                i32.shl
                i32.add
                local.tee $p1
                i32.const 5392
                i32.add
                local.tee $l10
                i32.load
                i32.const 35
                i32.add
                local.tee $l13
                local.get $p1
                i32.const 5396
                i32.add
                local.tee $p3
                i32.load
                local.tee $p1
                i32.const 2
                i32.shl
                i32.const 3122800
                i32.add
                i32.load
                i32.add
                i32.load8_s
                local.get $p1
                local.get $l13
                i32.add
                i32.load8_s
                local.get $l15
                local.get $l9
                i32.const 80
                i32.add
                call $f69900
                local.set $p1
                local.get $l10
                i32.load
                local.set $l10
                local.get $p1
                local.get $p3
                i32.load
                local.tee $l13
                i32.store8 offset=32
                local.get $p1
                local.get $l10
                i32.store offset=20
                local.get $l10
                local.get $l13
                i32.const 2
                i32.shl
                i32.add
                local.get $p1
                i32.store offset=20
                local.get $l10
                local.get $l13
                i32.add
                i32.const 0
                i32.store8 offset=32
                local.get $p1
                i32.const 1
                i32.store8 offset=34
                local.get $p1
                local.get $p4
                i32.store offset=28
                local.get $p4
                i32.const 2
                i32.store8 offset=33
                local.get $p4
                local.get $p1
                i32.store offset=24
                local.get $p1
                local.set $p4
                local.get $p2
                i32.const 1
                i32.add
                local.tee $p2
                local.get $l19
                i32.ne
                br_if $L28
              end
            end
            local.get $p5
            i32.const 1
            i32.store8 offset=34
            local.get $p5
            local.get $p4
            i32.store offset=28
            local.get $p4
            i32.const 2
            i32.store8 offset=33
            local.get $p4
            local.get $p5
            i32.store offset=24
          end
          local.get $l12
          i32.load8_u offset=40
          local.tee $p4
          local.get $p0
          local.tee $p1
          i32.load
          i32.const 1
          i32.sub
          i32.ne
          if $I29 (result i32)
            local.get $l8
            local.get $l8
            i32.load offset=5916
            local.tee $p1
            i32.const 1
            i32.add
            i32.store offset=5916
            local.get $l8
            local.get $p1
            i32.const 2
            i32.shl
            i32.add
            i32.const 5660
            i32.add
          else
            local.get $p1
          end
          local.get $p4
          i32.store
          local.get $l8
          i32.load
          i32.eqz
          br_if $B23
          local.get $l9
          f32.load offset=80
          local.get $l8
          i32.load offset=4
          i32.load
          f32.load offset=16
          f32.gt
          i32.eqz
          br_if $B23
          local.get $l9
          i32.load offset=76
          i32.const 64
          i32.ne
          br_if $L13
        end
      end
      local.get $l18
      local.get $l17
      local.get $l12
      local.get $p6
      local.get $l14
      local.get $l16
      local.get $p7
      call $f69901
      i32.const 6
      local.set $p0
    end
    local.get $l9
    i32.const 96
    i32.add
    global.set $g0
    local.get $l11
    i32.const 6336
    i32.add
    global.set $g0
    local.get $p0)