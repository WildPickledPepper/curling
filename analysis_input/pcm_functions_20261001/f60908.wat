  (func $f60908 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 i64) (local $l15 f64)
    global.get $g0
    i32.const 144
    i32.sub
    local.tee $l2
    global.set $g0
    i32.const 4675020
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3746924
      call $f1661
      i32.const 3748808
      call $f1661
      i32.const 3767384
      call $f1661
      i32.const 3767156
      call $f1661
      i32.const 3767404
      call $f1661
      i32.const 3790516
      call $f1661
      i32.const 3790688
      call $f1661
      i32.const 3769840
      call $f1661
      i32.const 3769844
      call $f1661
      i32.const 3769848
      call $f1661
      i32.const 3741900
      call $f1661
      i32.const 3741904
      call $f1661
      i32.const 3792480
      call $f1661
      i32.const 3792496
      call $f1661
      i32.const 3792572
      call $f1661
      i32.const 3792588
      call $f1661
      i32.const 3751540
      call $f1661
      i32.const 3771204
      call $f1661
      i32.const 3771208
      call $f1661
      i32.const 3774828
      call $f1661
      i32.const 3771984
      call $f1661
      i32.const 3773132
      call $f1661
      i32.const 3771988
      call $f1661
      i32.const 3743880
      call $f1661
      i32.const 3752504
      call $f1661
      i32.const 3753376
      call $f1661
      i32.const 3755540
      call $f1661
      i32.const 3745968
      call $f1661
      i32.const 3781644
      call $f1661
      i32.const 3744896
      call $f1661
      i32.const 3781736
      call $f1661
      i32.const 3781740
      call $f1661
      i32.const 3808240
      call $f1661
      i32.const 3808244
      call $f1661
      i32.const 3808248
      call $f1661
      i32.const 3759028
      call $f1661
      i32.const 3824044
      call $f1661
      i32.const 3845296
      call $f1661
      i32.const 3813576
      call $f1661
      i32.const 3824096
      call $f1661
      i32.const 3820588
      call $f1661
      i32.const 3813948
      call $f1661
      i32.const 3859968
      call $f1661
      i32.const 3820972
      call $f1661
      i32.const 3821460
      call $f1661
      i32.const 3832776
      call $f1661
      i32.const 3826780
      call $f1661
      i32.const 3845324
      call $f1661
      i32.const 3836156
      call $f1661
      i32.const 3837344
      call $f1661
      i32.const 3816036
      call $f1661
      i32.const 3834384
      call $f1661
      i32.const 3813572
      call $f1661
      i32.const 3822768
      call $f1661
      i32.const 3836268
      call $f1661
      i32.const 4675020
      i32.const 1
      i32.store8
    end
    local.get $l2
    i64.const 0
    i64.store offset=112
    local.get $l2
    i64.const 0
    i64.store offset=104
    local.get $l2
    i64.const 0
    i64.store offset=96
    local.get $l2
    i32.const 0
    i32.store offset=92
    local.get $l2
    i32.const 0
    i32.store offset=88
    block $B1
      local.get $p0
      i32.load offset=284
      i32.const 3813572
      i32.load
      i32.const 0
      call $f53861
      i32.eqz
      br_if $B1
      local.get $p0
      i32.load offset=288
      i32.const 3813572
      i32.load
      i32.const 0
      call $f53861
      i32.eqz
      br_if $B1
      local.get $p0
      i32.load8_u offset=114
      i32.eqz
      br_if $B1
      local.get $p0
      i32.load8_u offset=115
      i32.eqz
      br_if $B1
      local.get $p0
      i32.load offset=124
      local.tee $p1
      i32.load offset=56
      local.tee $l3
      i32.eqz
      br_if $B1
      local.get $p1
      i32.load offset=80
      local.tee $p1
      i32.eqz
      br_if $B1
      local.get $p0
      local.get $p1
      i32.store offset=288
      local.get $p0
      local.get $l3
      i32.store offset=284
    end
    block $B2
      local.get $p0
      i32.load8_u offset=160
      br_if $B2
      local.get $p0
      i32.load8_u offset=114
      i32.eqz
      br_if $B2
      local.get $p0
      i32.load8_u offset=115
      i32.eqz
      br_if $B2
      i32.const 0
      call $f54556
      local.set $l8
      local.get $p0
      i32.const 3832776
      i32.load
      local.get $l8
      f32.const 0x1.4p+2 (;=5;)
      f32.mul
      i32.const 0
      call $f54430
      local.get $p0
      i32.const 1
      i32.store8 offset=160
    end
    block $B3
      local.get $p0
      i32.load8_u offset=300
      br_if $B3
      local.get $p0
      i32.load8_u offset=112
      i32.eqz
      br_if $B3
      local.get $p0
      i32.load8_u offset=113
      i32.eqz
      br_if $B3
      i32.const 4674994
      i32.load8_u
      i32.eqz
      if $I4
        i32.const 3836272
        call $f1661
        i32.const 3822832
        call $f1661
        i32.const 4674994
        i32.const 1
        i32.store8
      end
      local.get $p0
      i32.const 1
      i32.store8 offset=300
      i32.const 0
      call $f54556
      local.set $l8
      local.get $p0
      i32.const 3836272
      i32.load
      local.get $l8
      f32.const 0x1.cp+2 (;=7;)
      f32.mul
      i32.const 0
      call $f54430
      i32.const 0
      call $f54556
      local.set $l8
      local.get $p0
      i32.const 3822832
      i32.load
      local.get $l8
      f32.const 0x1.ep+3 (;=15;)
      f32.mul
      i32.const 0
      call $f54430
    end
    block $B5
      block $B6
        block $B7
          block $B8
            block $B9
              local.get $p0
              i32.load8_u offset=184
              i32.eqz
              if $I10
                local.get $p0
                local.get $p0
                call $f60863
                block $B11
                  local.get $p0
                  i32.load8_u offset=16
                  i32.eqz
                  br_if $B11
                  local.get $p0
                  local.get $p0
                  f32.load offset=24
                  i32.const 0
                  call $f54555
                  f32.add
                  local.tee $l8
                  f32.store offset=24
                  local.get $l8
                  f32.const 0x1.4p+2 (;=5;)
                  f32.ge
                  i32.eqz
                  br_if $B11
                  i32.const 3748808
                  i32.load
                  local.tee $p1
                  i32.load offset=116
                  i32.eqz
                  if $I12
                    local.get $p1
                    call $f65192
                  end
                  i32.const 3822768
                  i32.load
                  i32.const 0
                  call $f42976
                  local.get $p0
                  i32.const 0
                  i32.store offset=24
                  local.get $p0
                  i32.const 0
                  i32.store8 offset=16
                  f32.const 0x1p+0 (;=1;)
                  i32.const 0
                  call $f54557
                  local.get $p0
                  i32.load8_u offset=84
                  br_if $B11
                  local.get $p0
                  local.get $p0
                  call $f60866
                  local.get $p0
                  i32.load8_u offset=84
                  br_if $B11
                  local.get $p0
                  i32.const 3836268
                  i32.load
                  f32.const 0x1p+4 (;=16;)
                  i32.const 0
                  call $f54430
                end
                local.get $p0
                i32.load8_u offset=244
                i32.eqz
                br_if $B7
                block $B13
                  block $B14
                    local.get $p0
                    i32.load offset=124
                    local.tee $p1
                    i32.load offset=24
                    i32.eqz
                    if $I15
                      local.get $p1
                      i32.load offset=8
                      local.set $p1
                      local.get $p0
                      i32.load offset=220
                      local.set $l3
                      i32.const 3752504
                      i32.load
                      local.tee $l5
                      i32.load offset=116
                      i32.eqz
                      br_if $B14
                      br $B13
                    end
                    local.get $p1
                    i32.load offset=8
                    local.set $p1
                    local.get $p0
                    i32.load offset=224
                    local.set $l3
                    i32.const 3752504
                    i32.load
                    local.tee $l5
                    i32.load offset=116
                    br_if $B13
                  end
                  local.get $l5
                  call $f65192
                end
                local.get $l3
                block $B16 (result i32)
                  local.get $p1
                  f64.convert_i32_s
                  f64.const 0x1p-1 (;=0.5;)
                  f64.mul
                  f64.floor
                  local.tee $l15
                  f64.abs
                  f64.const 0x1p+31 (;=2.14748e+09;)
                  f64.lt
                  if $I17
                    local.get $l15
                    i32.trunc_f64_s
                    br $B16
                  end
                  i32.const -2147483648
                end
                i32.const 3773132
                i32.load
                call $f2903
                local.set $p1
                local.get $p0
                i32.load offset=192
                i32.const 0
                call $f54401
                local.set $l3
                local.get $l2
                i32.const 120
                i32.add
                local.get $p1
                i32.const 0
                call $f54401
                i32.const 0
                call $f54624
                local.get $l2
                f32.load offset=120
                local.set $l8
                local.get $l2
                f32.load offset=124
                local.set $l9
                local.get $p0
                f32.load offset=212
                local.set $l10
                local.get $p0
                f32.load offset=208
                local.set $l11
                local.get $l2
                i32.const 80
                i32.add
                local.tee $l5
                local.get $l2
                f32.load offset=128
                local.get $p0
                f32.load offset=216
                f32.sub
                f32.store
                local.get $l2
                i32.const -64
                i32.sub
                local.get $l5
                i32.load
                i32.store
                local.get $l2
                local.get $l9
                local.get $l10
                f32.sub
                f32.store offset=76
                local.get $l2
                local.get $l8
                local.get $l11
                f32.sub
                f32.store offset=72
                local.get $l2
                local.get $l2
                i64.load offset=72
                i64.store offset=56
                local.get $l3
                local.get $l2
                i32.const 56
                i32.add
                i32.const 0
                call $f54626
                local.get $l2
                i32.const 120
                i32.add
                local.get $p1
                i32.const 0
                call $f54401
                i32.const 0
                call $f54624
                local.get $l2
                f32.load offset=128
                local.set $l8
                local.get $l2
                f32.load offset=124
                local.set $l9
                local.get $l2
                f32.load offset=120
                local.set $l10
                local.get $p0
                f32.load offset=236
                local.set $l11
                local.get $p0
                f32.load offset=232
                local.set $l12
                local.get $p0
                f32.load offset=228
                local.set $l13
                i32.const 4675187
                i32.load8_u
                i32.eqz
                if $I18
                  i32.const 3752504
                  call $f1661
                  i32.const 4675187
                  i32.const 1
                  i32.store8
                end
                i32.const 3752504
                i32.load
                local.tee $l3
                i32.load offset=116
                i32.eqz
                if $I19
                  local.get $l3
                  call $f65192
                end
                local.get $l2
                i32.const 120
                i32.add
                local.get $p1
                i32.const 3792572
                i32.load
                call $f34548
                i32.const 0
                call $f32519
                local.get $l10
                local.get $l13
                f32.sub
                local.tee $l10
                local.get $l10
                f32.mul
                local.get $l9
                local.get $l12
                f32.sub
                local.tee $l9
                local.get $l9
                f32.mul
                f32.add
                local.get $l8
                local.get $l11
                f32.sub
                local.tee $l8
                local.get $l8
                f32.mul
                f32.add
                f32.sqrt
                f32.const 0x1p+0 (;=1;)
                f32.gt
                i32.eqz
                br_if $B7
                local.get $l2
                f32.load offset=120
                local.tee $l8
                local.get $l8
                f32.mul
                local.get $l2
                f32.load offset=124
                local.tee $l8
                local.get $l8
                f32.mul
                f32.add
                local.get $l2
                f32.load offset=128
                local.tee $l8
                local.get $l8
                f32.mul
                f32.add
                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                f32.lt
                i32.eqz
                br_if $B7
                i32.const 3748808
                i32.load
                local.tee $l3
                i32.load offset=116
                i32.eqz
                if $I20
                  local.get $l3
                  call $f65192
                end
                i32.const 3824044
                i32.load
                i32.const 0
                call $f42976
                local.get $p1
                i32.const 3792496
                i32.load
                call $f34548
                i32.const 0
                call $f32557
                f32.const 0x1.333334p-1 (;=0.6;)
                i32.const 0
                call $f32511
                local.get $p1
                i32.const 3792496
                i32.load
                call $f34548
                i32.const 0
                call $f32557
                f32.const 0x1.333334p-1 (;=0.6;)
                i32.const 0
                call $f32512
                i32.const 3820972
                i32.load
                i32.const 0
                call $f54416
                local.set $p1
                i32.const 3753376
                i32.load
                local.tee $l3
                i32.load offset=116
                i32.eqz
                if $I21
                  local.get $l3
                  call $f65192
                end
                local.get $p1
                i32.const 0
                i32.const 0
                call $f54398
                if $I22
                  i32.const 3820972
                  i32.load
                  i32.const 0
                  call $f54416
                  i32.const 3792588
                  i32.load
                  call $f34548
                  i32.const 0
                  i32.store8 offset=24
                end
                local.get $p0
                local.get $p0
                call $f60899
                i32.eqz
                br_if $B7
                local.get $p0
                i32.const 0
                i32.store8 offset=244
                local.get $p0
                local.get $p0
                call $f60893
                local.get $p0
                i32.load offset=124
                local.tee $p1
                local.get $p1
                i32.load offset=8
                i32.const 1
                i32.add
                local.tee $l3
                i32.store offset=8
                local.get $p0
                i32.load8_u offset=84
                if $I23 (result i32)
                  local.get $p0
                  local.get $p0
                  call $f60888
                  local.get $p0
                  local.get $p0
                  i32.const 136
                  i32.add
                  local.get $p0
                  call $f60865
                  local.get $p0
                  i32.load offset=124
                  local.tee $p1
                  i32.load offset=8
                else
                  local.get $l3
                end
                i32.const 16
                i32.eq
                if $I24
                  local.get $p0
                  local.get $p0
                  call $f60876
                  local.get $p0
                  i32.load offset=124
                  local.tee $p1
                  i32.load offset=20
                  local.get $p1
                  i32.load offset=12
                  i32.const 2
                  i32.shl
                  i32.add
                  local.get $p0
                  local.get $p1
                  local.get $p0
                  call $f60877
                  i32.store offset=16
                  local.get $p0
                  i32.load8_u offset=84
                  i32.eqz
                  if $I25
                    local.get $p0
                    local.get $p0
                    call $f60866
                  end
                  block $B26
                    local.get $p0
                    i32.load offset=124
                    local.tee $p1
                    i32.load offset=20
                    local.get $p1
                    i32.load offset=12
                    local.tee $l3
                    i32.const 2
                    i32.shl
                    i32.add
                    i32.load offset=16
                    local.tee $l5
                    i32.const 0
                    i32.gt_s
                    if $I27
                      local.get $p1
                      i32.const 0
                      i32.store offset=24
                      br $B26
                    end
                    local.get $l5
                    i32.const 0
                    i32.lt_s
                    if $I28
                      local.get $p1
                      i32.const 1
                      i32.store offset=24
                      br $B26
                    end
                    local.get $p1
                    local.get $p1
                    i32.load offset=24
                    i32.const 1
                    i32.xor
                    i32.store offset=24
                  end
                  local.get $p1
                  i32.const 0
                  i32.store offset=8
                  local.get $p1
                  local.get $l3
                  i32.const 1
                  i32.add
                  i32.store offset=12
                  local.get $p0
                  local.get $p0
                  call $f60896
                  block $B29
                    local.get $p0
                    i32.load offset=124
                    local.tee $p1
                    i32.load offset=12
                    local.get $p1
                    i32.load offset=16
                    i32.lt_s
                    if $I30
                      local.get $p0
                      local.get $p0
                      call $f60878
                      local.get $p0
                      local.get $p0
                      call $f60876
                      local.get $p0
                      i32.load8_u offset=84
                      if $I31
                        local.get $p0
                        local.get $p0
                        i32.load offset=124
                        local.tee $p1
                        i32.load offset=24
                        i32.store offset=156
                        br $B8
                      end
                      local.get $p0
                      local.get $p0
                      call $f60866
                      br $B29
                    end
                    block $B32
                      local.get $p0
                      i32.load8_u offset=84
                      br_if $B32
                      local.get $p0
                      local.get $p0
                      call $f60866
                      local.get $p0
                      i32.load8_u offset=84
                      br_if $B32
                      local.get $p0
                      local.get $p0
                      call $f60904
                    end
                    local.get $p0
                    i32.load offset=220
                    i32.const 0
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.load offset=224
                    i32.const 0
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.load offset=220
                    i32.const 1
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.load offset=224
                    i32.const 1
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.load offset=220
                    i32.const 2
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.load offset=224
                    i32.const 2
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.load offset=220
                    i32.const 3
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.load offset=224
                    i32.const 3
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.load offset=220
                    i32.const 4
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.load offset=224
                    i32.const 4
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.load offset=220
                    i32.const 5
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.load offset=224
                    i32.const 5
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.load offset=220
                    i32.const 6
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.load offset=224
                    i32.const 6
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.load offset=220
                    i32.const 7
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.load offset=224
                    i32.const 7
                    i32.const 3773132
                    i32.load
                    call $f2903
                    i32.const 0
                    i32.const 0
                    call $f54405
                    local.get $p0
                    i32.const 1
                    i32.store8 offset=184
                    local.get $p0
                    i32.load offset=108
                    i32.const 3746924
                    i32.load
                    local.tee $p1
                    i32.load offset=116
                    if $I33 (result i32)
                      local.get $p1
                    else
                      local.get $p1
                      call $f65192
                      i32.const 3746924
                      i32.load
                    end
                    i32.load offset=92
                    i32.const 8
                    i32.add
                    i32.const 0
                    call $f56590
                    i32.const 3826780
                    i32.load
                    local.get $p0
                    i32.load offset=284
                    i32.const 0
                    call $f60937
                    local.get $p0
                    i32.load offset=108
                    i32.const 3746924
                    i32.load
                    i32.load offset=92
                    i32.const 8
                    i32.add
                    i32.const 0
                    call $f56590
                    i32.const 3836156
                    i32.load
                    local.get $p0
                    i32.load offset=288
                    i32.const 0
                    call $f60937
                    local.get $p0
                    i32.load offset=88
                    i32.const 0
                    call $f51581
                    if $I34
                      local.get $p0
                      i32.load offset=88
                      local.set $l3
                      i32.const 3746924
                      i32.load
                      local.tee $p1
                      i32.load offset=116
                      if $I35 (result i32)
                        local.get $p1
                      else
                        local.get $p1
                        call $f65192
                        i32.const 3746924
                        i32.load
                      end
                      i32.load offset=92
                      local.tee $p1
                      i32.load offset=16
                      local.get $p1
                      i32.load offset=8
                      i32.const 1
                      i32.sub
                      i32.const 3771988
                      i32.load
                      call $f2903
                      i32.load offset=12
                      local.set $p1
                      local.get $p0
                      i32.load offset=100
                      i32.const 3813576
                      i32.load
                      i32.const 3813572
                      i32.load
                      i32.const 0
                      call $f53894
                      local.set $l5
                      local.get $l3
                      local.get $p1
                      i32.const 3845296
                      i32.load
                      local.get $l5
                      i32.const 0
                      call $f53871
                      i32.const 1
                      i32.const 0
                      call $f51741
                      local.get $p0
                      i32.load offset=88
                      local.set $p1
                      i32.const 3746924
                      i32.load
                      i32.load offset=92
                      local.tee $l3
                      i32.load offset=16
                      local.get $l3
                      i32.load offset=8
                      i32.const 1
                      i32.sub
                      i32.const 3771988
                      i32.load
                      call $f2903
                      i32.load offset=20
                      local.set $l3
                      local.get $p0
                      i32.load offset=100
                      i32.const 3813576
                      i32.load
                      i32.const 3813572
                      i32.load
                      i32.const 0
                      call $f53894
                      local.set $l5
                      local.get $p1
                      local.get $l3
                      i32.const 3845296
                      i32.load
                      local.get $l5
                      i32.const 0
                      call $f53871
                      i32.const 1
                      i32.const 0
                      call $f51741
                    end
                    i32.const 3746924
                    i32.load
                    local.tee $p1
                    i32.load offset=116
                    i32.eqz
                    if $I36
                      local.get $p1
                      call $f65192
                      i32.const 3746924
                      i32.load
                      local.set $p1
                    end
                    local.get $p1
                    i32.load offset=92
                    local.tee $l3
                    i32.load offset=16
                    i32.load offset=12
                    i32.const 1
                    i32.eq
                    if $I37
                      local.get $p1
                      i32.load offset=116
                      i32.eqz
                      if $I38
                        local.get $p1
                        call $f65192
                        i32.const 3746924
                        i32.load
                        local.tee $p1
                        i32.load offset=92
                        local.set $l3
                      end
                      local.get $l3
                      local.get $l3
                      i32.load offset=8
                      i32.const 1
                      i32.sub
                      i32.store offset=8
                    end
                    local.get $p1
                    i32.load offset=116
                    if $I39 (result i32)
                      local.get $p1
                    else
                      local.get $p1
                      call $f65192
                      i32.const 3746924
                      i32.load
                    end
                    i32.load offset=92
                    local.tee $p1
                    i32.load offset=8
                    local.get $p1
                    i32.load offset=16
                    i32.load offset=12
                    i32.eq
                    if $I40
                      i32.const 0
                      call $f51726
                      i32.const 3845324
                      i32.load
                      i32.const 0
                      call $f53732
                      local.set $p1
                      i32.const 0
                      call $f53215
                      local.set $l3
                      i32.const 3755540
                      i32.load
                      call $f1446
                      local.tee $l5
                      local.get $p1
                      i32.const 1
                      local.get $l3
                      i32.const 0
                      call $f51640
                      i32.const 3746924
                      i32.load
                      local.tee $p1
                      i32.load offset=116
                      if $I41 (result i32)
                        local.get $p1
                      else
                        local.get $p1
                        call $f65192
                        i32.const 3746924
                        i32.load
                      end
                      i32.load offset=92
                      i32.load offset=20
                      local.set $l6
                      i32.const 3759028
                      i32.load
                      local.tee $p1
                      i32.load offset=116
                      i32.eqz
                      if $I42
                        local.get $p1
                        call $f65192
                        i32.const 3759028
                        i32.load
                        local.set $p1
                      end
                      local.get $p1
                      i32.load offset=92
                      i32.load offset=36
                      local.tee $l3
                      i32.eqz
                      if $I43
                        local.get $p1
                        i32.load offset=116
                        if $I44 (result i32)
                          local.get $p1
                        else
                          local.get $p1
                          call $f65192
                          i32.const 3759028
                          i32.load
                        end
                        i32.load offset=92
                        i32.load
                        local.set $p1
                        i32.const 3741900
                        i32.load
                        call $f1446
                        local.tee $l3
                        local.get $p1
                        i32.const 3808240
                        i32.load
                        i32.const 0
                        call $f47200
                        i32.const 3759028
                        i32.load
                        i32.load offset=92
                        local.get $l3
                        i32.store offset=36
                      end
                      local.get $l6
                      local.get $l3
                      i32.const 3790516
                      i32.load
                      call $f34616
                      local.set $l4
                      i32.const 3759028
                      i32.load
                      local.tee $p1
                      i32.load offset=116
                      i32.eqz
                      if $I45
                        local.get $p1
                        call $f65192
                        i32.const 3759028
                        i32.load
                        local.set $p1
                      end
                      local.get $p1
                      i32.load offset=92
                      i32.load offset=40
                      local.tee $l3
                      i32.eqz
                      if $I46
                        local.get $p1
                        i32.load offset=116
                        if $I47 (result i32)
                          local.get $p1
                        else
                          local.get $p1
                          call $f65192
                          i32.const 3759028
                          i32.load
                        end
                        i32.load offset=92
                        i32.load
                        local.set $p1
                        i32.const 3741904
                        i32.load
                        call $f1446
                        local.tee $l3
                        local.get $p1
                        i32.const 3808244
                        i32.load
                        i32.const 0
                        call $f47201
                        i32.const 3759028
                        i32.load
                        local.tee $p1
                        i32.load offset=92
                        local.get $l3
                        i32.store offset=40
                      end
                      local.get $p1
                      i32.load offset=116
                      i32.eqz
                      if $I48
                        local.get $p1
                        call $f65192
                        i32.const 3759028
                        i32.load
                        local.set $p1
                      end
                      local.get $p1
                      i32.load offset=92
                      i32.load offset=44
                      local.tee $l6
                      i32.eqz
                      if $I49
                        local.get $p1
                        i32.load offset=116
                        if $I50 (result i32)
                          local.get $p1
                        else
                          local.get $p1
                          call $f65192
                          i32.const 3759028
                          i32.load
                        end
                        i32.load offset=92
                        i32.load
                        local.set $p1
                        i32.const 3741900
                        i32.load
                        call $f1446
                        local.tee $l6
                        local.get $p1
                        i32.const 3808248
                        i32.load
                        i32.const 0
                        call $f47200
                        i32.const 3759028
                        i32.load
                        i32.load offset=92
                        local.get $l6
                        i32.store offset=44
                      end
                      local.get $l4
                      local.get $l3
                      local.get $l6
                      i32.const 3790688
                      i32.load
                      call $f34643
                      local.set $p1
                      i32.const 3743880
                      i32.load
                      call $f1446
                      i32.const 3774828
                      i32.load
                      call $f2715
                      local.get $p0
                      local.get $p0
                      call $f60867
                      local.get $l5
                      i32.const 3859968
                      i32.load
                      local.get $l5
                      i32.load
                      local.tee $l3
                      i32.load offset=348
                      local.get $l3
                      i32.load offset=344
                      call_indirect $__indirect_function_table (type $t2)
                      local.get $l2
                      i32.const 120
                      i32.add
                      local.get $p1
                      i32.const 3767156
                      i32.load
                      call $f3829
                      local.get $l2
                      local.get $l2
                      i64.load offset=136
                      i64.store offset=112
                      local.get $l2
                      local.get $l2
                      i64.load offset=128
                      i64.store offset=104
                      local.get $l2
                      local.get $l2
                      i64.load offset=120
                      i64.store offset=96
                      local.get $l2
                      i32.const 0
                      i32.store offset=120
                      local.get $l2
                      local.get $l2
                      i32.const 96
                      i32.add
                      i32.store offset=124
                      i32.const 1
                      local.set $l6
                      block $B51
                        block $B52
                          block $B53
                            block $B54 (result i32)
                              block $B55
                                block $B56
                                  block $B57
                                    loop $L58
                                      i32.const 4133620
                                      i32.const 0
                                      i32.store
                                      i32.const 10662
                                      local.get $l2
                                      i32.const 96
                                      i32.add
                                      i32.const 3769844
                                      i32.load
                                      call $env.invoke_iii
                                      local.set $l3
                                      i32.const 4133620
                                      i32.load
                                      local.set $p1
                                      i32.const 4133620
                                      i32.const 0
                                      i32.store
                                      local.get $p1
                                      i32.const 1
                                      i32.eq
                                      br_if $B55
                                      local.get $l3
                                      i32.eqz
                                      br_if $B53
                                      i32.const 4133620
                                      i32.const 0
                                      i32.store
                                      local.get $l2
                                      i64.load offset=108 align=4
                                      local.set $l14
                                      i32.const 948
                                      i32.const 3745968
                                      i32.load
                                      i32.const 7
                                      call $env.invoke_iii
                                      local.set $p1
                                      i32.const 4133620
                                      i32.load
                                      local.set $l3
                                      i32.const 4133620
                                      i32.const 0
                                      i32.store
                                      block $B59
                                        block $B60
                                          block $B61
                                            block $B62
                                              block $B63
                                                block $B64
                                                  block $B65
                                                    block $B66
                                                      block $B67
                                                        block $B68
                                                          block $B69
                                                            local.get $l3
                                                            i32.const 1
                                                            i32.ne
                                                            if $I70
                                                              local.get $p1
                                                              local.get $l14
                                                              i32.wrap_i64
                                                              local.tee $l3
                                                              i32.store offset=16
                                                              local.get $p1
                                                              i32.const 3816036
                                                              i32.load
                                                              i32.store offset=20
                                                              i32.const 3746924
                                                              i32.load
                                                              local.tee $l4
                                                              i32.load offset=116
                                                              if $I71 (result i32)
                                                                local.get $l4
                                                              else
                                                                i32.const 4133620
                                                                i32.const 0
                                                                i32.store
                                                                i32.const 664
                                                                local.get $l4
                                                                call $env.invoke_vi
                                                                i32.const 4133620
                                                                i32.load
                                                                local.set $l4
                                                                i32.const 4133620
                                                                i32.const 0
                                                                i32.store
                                                                local.get $l4
                                                                i32.const 1
                                                                i32.eq
                                                                br_if $B69
                                                                i32.const 3746924
                                                                i32.load
                                                              end
                                                              i32.load offset=92
                                                              i32.load offset=24
                                                              local.set $l4
                                                              i32.const 4133620
                                                              i32.const 0
                                                              i32.store
                                                              i32.const 3823
                                                              local.get $l4
                                                              local.get $l3
                                                              i32.const 3767384
                                                              i32.load
                                                              call $env.invoke_iiii
                                                              local.set $l7
                                                              i32.const 4133620
                                                              i32.load
                                                              local.set $l4
                                                              i32.const 4133620
                                                              i32.const 0
                                                              i32.store
                                                              local.get $l4
                                                              i32.const 1
                                                              i32.eq
                                                              br_if $B68
                                                              i32.const 4133620
                                                              i32.const 0
                                                              i32.store
                                                              local.get $l2
                                                              i32.const 0
                                                              local.get $l6
                                                              local.get $l7
                                                              select
                                                              i32.store offset=92
                                                              i32.const 2143
                                                              local.get $l2
                                                              i32.const 92
                                                              i32.add
                                                              i32.const 0
                                                              call $env.invoke_iii
                                                              local.set $l7
                                                              i32.const 4133620
                                                              i32.load
                                                              local.set $l4
                                                              i32.const 4133620
                                                              i32.const 0
                                                              i32.store
                                                              local.get $l4
                                                              i32.const 1
                                                              i32.eq
                                                              br_if $B67
                                                              local.get $p1
                                                              local.get $l7
                                                              i32.store offset=24
                                                              local.get $p1
                                                              i32.const 3816036
                                                              i32.load
                                                              i32.store offset=28
                                                              i32.const 3746924
                                                              i32.load
                                                              local.tee $l4
                                                              i32.load offset=116
                                                              if $I72 (result i32)
                                                                local.get $l4
                                                              else
                                                                i32.const 4133620
                                                                i32.const 0
                                                                i32.store
                                                                i32.const 664
                                                                local.get $l4
                                                                call $env.invoke_vi
                                                                i32.const 4133620
                                                                i32.load
                                                                local.set $l4
                                                                i32.const 4133620
                                                                i32.const 0
                                                                i32.store
                                                                local.get $l4
                                                                i32.const 1
                                                                i32.eq
                                                                br_if $B66
                                                                i32.const 3746924
                                                                i32.load
                                                              end
                                                              i32.load offset=92
                                                              i32.load offset=24
                                                              local.set $l4
                                                              i32.const 4133620
                                                              i32.const 0
                                                              i32.store
                                                              i32.const 3823
                                                              local.get $l4
                                                              local.get $l3
                                                              i32.const 3767384
                                                              i32.load
                                                              call $env.invoke_iiii
                                                              local.set $l7
                                                              i32.const 4133620
                                                              i32.load
                                                              local.set $l4
                                                              i32.const 4133620
                                                              i32.const 0
                                                              i32.store
                                                              local.get $l4
                                                              i32.const 1
                                                              i32.eq
                                                              br_if $B65
                                                              i32.const 4133620
                                                              i32.const 0
                                                              i32.store
                                                              local.get $l2
                                                              i32.const 0
                                                              local.get $l14
                                                              i64.const 32
                                                              i64.shr_u
                                                              i32.wrap_i64
                                                              local.get $l7
                                                              select
                                                              i32.store offset=92
                                                              i32.const 2143
                                                              local.get $l2
                                                              i32.const 92
                                                              i32.add
                                                              i32.const 0
                                                              call $env.invoke_iii
                                                              local.set $l7
                                                              i32.const 4133620
                                                              i32.load
                                                              local.set $l4
                                                              i32.const 4133620
                                                              i32.const 0
                                                              i32.store
                                                              local.get $l4
                                                              i32.const 1
                                                              i32.eq
                                                              br_if $B64
                                                              local.get $p1
                                                              local.get $l7
                                                              i32.store offset=32
                                                              local.get $p1
                                                              i32.const 3816036
                                                              i32.load
                                                              i32.store offset=36
                                                              i32.const 3746924
                                                              i32.load
                                                              local.tee $l4
                                                              i32.load offset=116
                                                              if $I73 (result i32)
                                                                local.get $l4
                                                              else
                                                                i32.const 4133620
                                                                i32.const 0
                                                                i32.store
                                                                i32.const 664
                                                                local.get $l4
                                                                call $env.invoke_vi
                                                                i32.const 4133620
                                                                i32.load
                                                                local.set $l4
                                                                i32.const 4133620
                                                                i32.const 0
                                                                i32.store
                                                                local.get $l4
                                                                i32.const 1
                                                                i32.eq
                                                                br_if $B63
                                                                i32.const 3746924
                                                                i32.load
                                                              end
                                                              i32.load offset=92
                                                              i32.load offset=24
                                                              local.set $l4
                                                              i32.const 4133620
                                                              i32.const 0
                                                              i32.store
                                                              i32.const 3823
                                                              local.get $l4
                                                              local.get $l3
                                                              i32.const 3767384
                                                              i32.load
                                                              call $env.invoke_iiii
                                                              local.set $l7
                                                              i32.const 4133620
                                                              i32.load
                                                              local.set $l4
                                                              i32.const 4133620
                                                              i32.const 0
                                                              i32.store
                                                              local.get $l4
                                                              i32.const 1
                                                              i32.eq
                                                              br_if $B62
                                                              local.get $l7
                                                              br_if $B61
                                                              i32.const 3813572
                                                              i32.load
                                                              local.set $l3
                                                              br $B60
                                                            end
                                                            i32.const 3088636
                                                            call $env.__cxa_find_matching_catch_3
                                                            br $B54
                                                          end
                                                          i32.const 3088636
                                                          call $env.__cxa_find_matching_catch_3
                                                          br $B54
                                                        end
                                                        i32.const 3088636
                                                        call $env.__cxa_find_matching_catch_3
                                                        br $B54
                                                      end
                                                      i32.const 3088636
                                                      call $env.__cxa_find_matching_catch_3
                                                      br $B54
                                                    end
                                                    i32.const 3088636
                                                    call $env.__cxa_find_matching_catch_3
                                                    br $B54
                                                  end
                                                  i32.const 3088636
                                                  call $env.__cxa_find_matching_catch_3
                                                  br $B54
                                                end
                                                i32.const 3088636
                                                call $env.__cxa_find_matching_catch_3
                                                br $B54
                                              end
                                              i32.const 3088636
                                              call $env.__cxa_find_matching_catch_3
                                              br $B54
                                            end
                                            i32.const 3088636
                                            call $env.__cxa_find_matching_catch_3
                                            br $B54
                                          end
                                          i32.const 3746924
                                          i32.load
                                          local.tee $l4
                                          i32.load offset=116
                                          if $I74 (result i32)
                                            local.get $l4
                                          else
                                            i32.const 4133620
                                            i32.const 0
                                            i32.store
                                            i32.const 664
                                            local.get $l4
                                            call $env.invoke_vi
                                            i32.const 4133620
                                            i32.load
                                            local.set $l4
                                            i32.const 4133620
                                            i32.const 0
                                            i32.store
                                            local.get $l4
                                            i32.const 1
                                            i32.eq
                                            br_if $B59
                                            i32.const 3746924
                                            i32.load
                                          end
                                          i32.load offset=92
                                          i32.load offset=24
                                          local.set $l4
                                          i32.const 4133620
                                          i32.const 0
                                          i32.store
                                          i32.const 2358
                                          local.get $l4
                                          local.get $l3
                                          i32.const 3767404
                                          i32.load
                                          call $env.invoke_iiii
                                          local.set $l3
                                          i32.const 4133620
                                          i32.load
                                          local.set $l4
                                          i32.const 4133620
                                          i32.const 0
                                          i32.store
                                          local.get $l4
                                          i32.const 1
                                          i32.eq
                                          br_if $B57
                                        end
                                        local.get $p1
                                        local.get $l3
                                        i32.store offset=40
                                        i32.const 4133620
                                        i32.const 0
                                        i32.store
                                        i32.const 950
                                        local.get $p1
                                        i32.const 0
                                        call $env.invoke_iii
                                        local.set $l3
                                        i32.const 4133620
                                        i32.load
                                        local.set $p1
                                        i32.const 4133620
                                        i32.const 0
                                        i32.store
                                        local.get $p1
                                        i32.const 1
                                        i32.eq
                                        br_if $B56
                                        local.get $l5
                                        i32.load
                                        local.tee $p1
                                        i32.load offset=348
                                        local.set $l4
                                        local.get $p1
                                        i32.load offset=344
                                        local.set $p1
                                        i32.const 4133620
                                        i32.const 0
                                        i32.store
                                        local.get $p1
                                        local.get $l5
                                        local.get $l3
                                        local.get $l4
                                        call $env.invoke_viii
                                        i32.const 4133620
                                        i32.load
                                        local.set $p1
                                        i32.const 4133620
                                        i32.const 0
                                        i32.store
                                        local.get $p1
                                        i32.const 1
                                        i32.eq
                                        br_if $B56
                                        local.get $l6
                                        i32.const 1
                                        i32.add
                                        local.set $l6
                                        br $L58
                                      end
                                    end
                                    i32.const 3088636
                                    call $env.__cxa_find_matching_catch_3
                                    br $B54
                                  end
                                  i32.const 3088636
                                  call $env.__cxa_find_matching_catch_3
                                  br $B54
                                end
                                i32.const 3088636
                                call $env.__cxa_find_matching_catch_3
                                br $B54
                              end
                              i32.const 3088636
                              call $env.__cxa_find_matching_catch_3
                            end
                            local.set $p1
                            call $env.getTempRet0
                            i32.const 3088636
                            call $env.llvm_eh_typeid_for
                            i32.ne
                            br_if $B51
                            local.get $p1
                            call $env.__cxa_begin_catch
                            i32.load
                            local.set $p1
                            i32.const 4133620
                            i32.const 0
                            i32.store
                            local.get $l2
                            local.get $p1
                            i32.store offset=120
                            i32.const 58
                            call $env.invoke_v
                            i32.const 4133620
                            i32.load
                            local.set $p1
                            i32.const 4133620
                            i32.const 0
                            i32.store
                            local.get $p1
                            i32.const 1
                            i32.eq
                            br_if $B52
                          end
                          local.get $l2
                          i32.const 120
                          i32.add
                          call $f60868
                          drop
                          local.get $l5
                          local.get $l5
                          i32.load
                          local.tee $p1
                          i32.load offset=276
                          local.get $p1
                          i32.load offset=272
                          call_indirect $__indirect_function_table (type $t1)
                          local.get $l5
                          local.get $l5
                          i32.load
                          local.tee $p1
                          i32.load offset=260
                          local.get $p1
                          i32.load offset=256
                          call_indirect $__indirect_function_table (type $t1)
                          local.get $p0
                          local.get $p0
                          call $f60872
                          br $B29
                        end
                        call $env.__cxa_find_matching_catch_2
                        local.set $p1
                        call $env.getTempRet0
                        drop
                      end
                      i32.const 4133620
                      i32.const 0
                      i32.store
                      i32.const 10672
                      local.get $l2
                      i32.const 120
                      i32.add
                      call $env.invoke_ii
                      drop
                      i32.const 4133620
                      i32.load
                      local.set $p0
                      i32.const 4133620
                      i32.const 0
                      i32.store
                      local.get $p0
                      i32.const 1
                      i32.eq
                      br_if $B9
                      local.get $p1
                      call $env.__resumeException
                      unreachable
                    end
                    local.get $p0
                    local.get $p0
                    call $f60873
                  end
                  local.get $p0
                  local.get $p0
                  i32.load offset=124
                  local.tee $p1
                  i32.load offset=24
                  i32.store offset=156
                  local.get $p0
                  i32.load8_u offset=84
                  br_if $B8
                  i32.const 0
                  call $f54556
                  local.set $l8
                  local.get $p0
                  i32.const 3836268
                  i32.load
                  local.get $l8
                  i32.const 0
                  call $f54430
                  br $B7
                end
                local.get $p0
                i32.load8_u offset=184
                br_if $B7
                local.get $p1
                local.get $p1
                i32.load offset=24
                i32.const 1
                i32.xor
                i32.store offset=24
                local.get $p0
                local.get $p0
                call $f60876
                local.get $p0
                i32.const 0
                i32.store8 offset=244
                local.get $p0
                i32.load8_u offset=16
                br_if $B5
                block $B75
                  local.get $p0
                  i32.load8_u offset=84
                  br_if $B75
                  local.get $p0
                  local.get $p0
                  call $f60866
                  local.get $p0
                  i32.load8_u offset=84
                  br_if $B75
                  i32.const 0
                  call $f54556
                  local.set $l8
                  local.get $p0
                  i32.const 3836268
                  i32.load
                  local.get $l8
                  i32.const 0
                  call $f54430
                  br $B7
                end
                local.get $p0
                i32.const 0
                i32.store offset=240
                local.get $p0
                i32.load offset=104
                local.get $p0
                i32.load offset=124
                i32.const 12
                i32.add
                i32.const 3824096
                i32.load
                i32.const 0
                call $f56592
                local.get $p0
                i32.load offset=124
                i32.const 8
                i32.add
                i32.const 3824096
                i32.load
                i32.const 0
                call $f56592
                i32.const 0
                call $f53732
                i32.const 3820588
                i32.load
                i32.const 3813948
                i32.load
                i32.const 0
                call $f60936
                local.set $l3
                local.get $l2
                local.get $p0
                i32.load offset=124
                i32.load offset=24
                local.tee $l5
                i32.const 1
                i32.add
                i32.store offset=88
                local.get $l2
                i32.const 88
                i32.add
                i32.const 0
                call $f57314
                local.set $p1
                i32.const 3834384
                i32.load
                local.get $p1
                i32.const 0
                call $f53732
                local.set $l6
                i32.const 3744896
                i32.load
                call $f1446
                local.set $p1
                i32.const 3781644
                i32.load
                local.set $l4
                local.get $l2
                i64.const 0
                i64.store offset=132 align=4
                local.get $l2
                i64.const 0
                i64.store offset=124 align=4
                local.get $l2
                local.get $l2
                i64.load offset=128
                i64.store offset=40
                local.get $l2
                local.get $l6
                i32.store offset=140
                local.get $l2
                local.get $l2
                i64.load offset=136
                i64.store offset=48
                local.get $l2
                local.get $l5
                i32.store offset=120
                local.get $l2
                local.get $l2
                i64.load offset=120
                i64.store offset=32
                local.get $p1
                local.get $l2
                i32.const 32
                i32.add
                local.get $l3
                local.get $l4
                call $f41305
                local.get $p0
                local.get $p1
                local.get $p0
                call $f60864
                drop
                br $B7
              end
              local.get $p0
              i32.load offset=52
              i32.const 0
              i32.const 0
              call $f54405
              i32.const 3821460
              i32.load
              i32.const 0
              call $f54416
              i32.const 3792480
              i32.load
              call $f34548
              local.set $p1
              local.get $l2
              i32.const 2
              i32.store offset=120
              i32.const 3751540
              i32.load
              local.get $l2
              i32.const 120
              i32.add
              call $f1675
              local.set $l3
              local.get $p1
              i32.const 3837344
              i32.load
              local.get $l3
              i32.const 0
              call $f54371
              br $B6
            end
            i32.const 0
            call $env.__cxa_find_matching_catch_3
            drop
            call $env.getTempRet0
            drop
            call $f640
            unreachable
          end
          local.get $p0
          i32.const 0
          i32.store offset=240
          local.get $p0
          i32.load offset=104
          local.get $p1
          i32.const 12
          i32.add
          i32.const 3824096
          i32.load
          i32.const 0
          call $f56592
          local.get $p0
          i32.load offset=124
          i32.const 8
          i32.add
          i32.const 3824096
          i32.load
          i32.const 0
          call $f56592
          i32.const 0
          call $f53732
          i32.const 3820588
          i32.load
          i32.const 3813948
          i32.load
          i32.const 0
          call $f60936
          local.set $l3
          local.get $l2
          local.get $p0
          i32.load offset=124
          i32.load offset=24
          local.tee $l5
          i32.const 1
          i32.add
          i32.store offset=88
          local.get $l2
          i32.const 88
          i32.add
          i32.const 0
          call $f57314
          local.set $p1
          i32.const 3834384
          i32.load
          local.get $p1
          i32.const 0
          call $f53732
          local.set $l6
          i32.const 3744896
          i32.load
          call $f1446
          local.set $p1
          i32.const 3781644
          i32.load
          local.set $l4
          local.get $l2
          i64.const 0
          i64.store offset=132 align=4
          local.get $l2
          i64.const 0
          i64.store offset=124 align=4
          local.get $l2
          local.get $l2
          i64.load offset=128
          i64.store offset=16
          local.get $l2
          local.get $l6
          i32.store offset=140
          local.get $l2
          local.get $l2
          i64.load offset=136
          i64.store offset=24
          local.get $l2
          local.get $l5
          i32.store offset=120
          local.get $l2
          local.get $l2
          i64.load offset=120
          i64.store offset=8
          local.get $p1
          local.get $l2
          i32.const 8
          i32.add
          local.get $l3
          local.get $l4
          call $f41305
          local.get $p0
          local.get $p1
          local.get $p0
          call $f60864
          drop
        end
        local.get $p0
        i32.load8_u offset=117
        i32.eqz
        br_if $B6
        local.get $p0
        local.get $p0
        f32.load offset=120
        i32.const 0
        call $f54144
        i32.const 0
        call $f54556
        f32.div
        f32.add
        f32.store offset=120
      end
      local.get $p0
      i32.load8_u offset=264
      i32.eqz
      br_if $B5
      i32.const 0
      call $f54530
      local.get $p0
      f32.load offset=268
      local.get $p0
      f32.load offset=272
      f32.add
      f32.gt
      i32.eqz
      br_if $B5
      local.get $p0
      i64.const 0
      i64.store offset=268 align=4
      local.get $p0
      i32.const 0
      i32.store8 offset=264
      f32.const 0x1p+0 (;=1;)
      local.get $p0
      f32.load offset=276
      local.tee $l8
      local.get $l8
      f32.const 0x0p+0 (;=0;)
      f32.eq
      select
      i32.const 0
      call $f54557
    end
    local.get $l2
    i32.const 144
    i32.add
    global.set $g0)
