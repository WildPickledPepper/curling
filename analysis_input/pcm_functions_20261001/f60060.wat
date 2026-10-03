  (func $f60060 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 f32) (local $l11 f32) (local $l12 f64) (local $l13 i64)
    global.get $g0
    i32.const 240
    i32.sub
    local.tee $l3
    global.set $g0
    i32.const 4674413
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3747280
      call $f1661
      i32.const 3748144
      call $f1661
      i32.const 3748808
      call $f1661
      i32.const 3792480
      call $f1661
      i32.const 3792496
      call $f1661
      i32.const 3792500
      call $f1661
      i32.const 3792544
      call $f1661
      i32.const 3792572
      call $f1661
      i32.const 3792588
      call $f1661
      i32.const 3751540
      call $f1661
      i32.const 3773132
      call $f1661
      i32.const 3752504
      call $f1661
      i32.const 3754332
      call $f1661
      i32.const 3745900
      call $f1661
      i32.const 3800744
      call $f1661
      i32.const 3781648
      call $f1661
      i32.const 3781652
      call $f1661
      i32.const 3845252
      call $f1661
      i32.const 3854688
      call $f1661
      i32.const 3820588
      call $f1661
      i32.const 3821168
      call $f1661
      i32.const 3851256
      call $f1661
      i32.const 3813948
      call $f1661
      i32.const 3852284
      call $f1661
      i32.const 3820972
      call $f1661
      i32.const 3851264
      call $f1661
      i32.const 3832492
      call $f1661
      i32.const 3848144
      call $f1661
      i32.const 3850800
      call $f1661
      i32.const 3834388
      call $f1661
      i32.const 3821460
      call $f1661
      i32.const 3833976
      call $f1661
      i32.const 3847788
      call $f1661
      i32.const 3848156
      call $f1661
      i32.const 3834392
      call $f1661
      i32.const 3834900
      call $f1661
      i32.const 3835100
      call $f1661
      i32.const 3851396
      call $f1661
      i32.const 3848152
      call $f1661
      i32.const 3835096
      call $f1661
      i32.const 3850000
      call $f1661
      i32.const 3834924
      call $f1661
      i32.const 3834920
      call $f1661
      i32.const 3856860
      call $f1661
      i32.const 3821244
      call $f1661
      i32.const 3858552
      call $f1661
      i32.const 3827816
      call $f1661
      i32.const 3835092
      call $f1661
      i32.const 3854648
      call $f1661
      i32.const 3837344
      call $f1661
      i32.const 3816120
      call $f1661
      i32.const 3834892
      call $f1661
      i32.const 3830768
      call $f1661
      i32.const 3821464
      call $f1661
      i32.const 3816036
      call $f1661
      i32.const 3835920
      call $f1661
      i32.const 3834904
      call $f1661
      i32.const 3825320
      call $f1661
      i32.const 3855760
      call $f1661
      i32.const 3821256
      call $f1661
      i32.const 3849248
      call $f1661
      i32.const 3848148
      call $f1661
      i32.const 3851268
      call $f1661
      i32.const 3851260
      call $f1661
      i32.const 3848140
      call $f1661
      i32.const 3834928
      call $f1661
      i32.const 3836268
      call $f1661
      i32.const 4674413
      i32.const 1
      i32.store8
    end
    local.get $l3
    i32.const 0
    i32.store offset=212
    local.get $l3
    i32.const 0
    i32.store offset=208
    local.get $l3
    i32.const 0
    i32.store offset=204
    local.get $l3
    i32.const 0
    i32.store offset=200
    local.get $l3
    i32.const 0
    i32.store8 offset=199
    local.get $p1
    i32.load offset=32
    i32.const 0
    call $f53919
    local.set $l4
    i32.const 3754332
    i32.load
    local.tee $p2
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $p2
      call $f65192
    end
    local.get $l4
    i32.const 3845252
    i32.load
    i32.const 3813948
    i32.load
    i32.const 0
    call $f7706
    i32.const 3813948
    i32.load
    i32.const 0
    call $f53974
    i32.const 0
    call $f53901
    local.set $l4
    local.get $l3
    local.get $p1
    i64.load offset=24 align=4
    i64.store offset=232
    local.get $l3
    local.get $p1
    i64.load offset=16 align=4
    i64.store offset=224
    local.get $l3
    local.get $p1
    i64.load offset=8 align=4
    i64.store offset=216
    i32.const 3827816
    i32.load
    local.get $p1
    i32.load offset=32
    i32.const 0
    call $f53732
    local.set $p1
    i32.const 3748808
    i32.load
    local.tee $p2
    i32.load offset=116
    i32.eqz
    if $I2
      local.get $p2
      call $f65192
    end
    local.get $p1
    i32.const 0
    call $f42976
    i32.const 1
    local.set $p1
    block $B3
      local.get $l4
      i32.load offset=12
      i32.eqz
      br_if $B3
      i32.const 3850800
      i32.load
      local.get $l4
      i32.const 16
      i32.add
      local.tee $p2
      i32.load
      i32.const 0
      call $f53732
      local.set $l5
      i32.const 3748808
      i32.load
      local.tee $l6
      i32.load offset=116
      i32.eqz
      if $I4
        local.get $l6
        call $f65192
      end
      local.get $l5
      i32.const 0
      call $f42976
      block $B5
        local.get $p2
        i32.load
        i32.const 3821244
        i32.load
        i32.const 0
        call $f53861
        i32.eqz
        if $I6
          local.get $l4
          i32.load offset=16
          i32.const 3832492
          i32.load
          i32.const 0
          call $f53861
          i32.eqz
          br_if $B5
        end
        i32.const 3821256
        i32.load
        local.get $l3
        i32.load offset=236
        i32.const 0
        call $f53732
        local.set $p2
        i32.const 3748808
        i32.load
        local.tee $l5
        i32.load offset=116
        i32.eqz
        if $I7
          local.get $l5
          call $f65192
        end
        local.get $p2
        i32.const 0
        call $f42976
        local.get $l4
        i32.load offset=12
        i32.const 2
        i32.lt_s
        br_if $B5
        local.get $l4
        i32.load offset=20
        local.set $p2
        local.get $l3
        local.get $l3
        i64.load offset=232
        i64.store offset=112
        local.get $l3
        local.get $l3
        i64.load offset=224
        i64.store offset=104
        local.get $l3
        local.get $l3
        i64.load offset=216
        i64.store offset=96
        local.get $p0
        local.get $l3
        i32.const 96
        i32.add
        local.get $p2
        local.get $l3
        call $f60061
      end
      local.get $l4
      i32.const 16
      i32.add
      local.tee $p2
      i32.load
      i32.const 3834892
      i32.load
      i32.const 0
      call $f53865
      if $I8
        local.get $l3
        i32.load offset=236
        local.set $l4
        local.get $l3
        i32.load offset=216
        local.set $p2
        i32.const 4674411
        i32.load8_u
        i32.eqz
        if $I9
          i32.const 3748808
          call $f1661
          i32.const 3814476
          call $f1661
          i32.const 3834896
          call $f1661
          i32.const 4674411
          i32.const 1
          i32.store8
        end
        i32.const 3834896
        i32.load
        local.get $l4
        i32.const 3814476
        i32.load
        i32.const 0
        call $f53871
        local.set $l4
        i32.const 3748808
        i32.load
        local.tee $l5
        i32.load offset=116
        i32.eqz
        if $I10
          local.get $l5
          call $f65192
        end
        local.get $l4
        i32.const 0
        call $f42976
        block $B11
          block $B12
            local.get $p2
            br_table $B12 $B11 $B3
          end
          local.get $p0
          i32.const 1
          i32.store8 offset=115
          br $B3
        end
        local.get $p0
        i32.const 1
        i32.store8 offset=116
        br $B3
      end
      block $B13
        local.get $p2
        i32.load
        i32.const 3834904
        i32.load
        i32.const 0
        call $f53861
        i32.eqz
        if $I14
          local.get $l4
          i32.const 16
          i32.add
          local.tee $p2
          i32.load
          i32.const 3834900
          i32.load
          i32.const 0
          call $f53861
          i32.eqz
          br_if $B13
        end
        local.get $l3
        i32.load offset=236
        local.set $p2
        local.get $l3
        i32.load offset=216
        local.set $l5
        i32.const 4674411
        i32.load8_u
        i32.eqz
        if $I15
          i32.const 3748808
          call $f1661
          i32.const 3814476
          call $f1661
          i32.const 3834896
          call $f1661
          i32.const 4674411
          i32.const 1
          i32.store8
        end
        i32.const 3834896
        i32.load
        local.get $p2
        i32.const 3814476
        i32.load
        i32.const 0
        call $f53871
        local.set $p2
        i32.const 3748808
        i32.load
        local.tee $l6
        i32.load offset=116
        i32.eqz
        if $I16
          local.get $l6
          call $f65192
        end
        local.get $p2
        i32.const 0
        call $f42976
        block $B17
          block $B18
            block $B19
              local.get $l5
              br_table $B19 $B18 $B17
            end
            local.get $p0
            i32.const 1
            i32.store8 offset=115
            br $B17
          end
          local.get $p0
          i32.const 1
          i32.store8 offset=116
        end
        local.get $l4
        i32.load offset=12
        i32.const 2
        i32.lt_s
        br_if $B3
        local.get $l4
        i32.load offset=20
        local.set $l4
        local.get $l3
        local.get $l3
        i64.load offset=232
        i64.store offset=24
        local.get $l3
        local.get $l3
        i64.load offset=224
        i64.store offset=16
        local.get $l3
        local.get $l3
        i64.load offset=216
        i64.store offset=8
        local.get $p0
        local.get $l3
        i32.const 8
        i32.add
        local.get $l4
        local.get $l3
        call $f60061
        br $B3
      end
      block $B20
        local.get $p2
        i32.load
        i32.const 3820588
        i32.load
        i32.const 0
        call $f53861
        i32.eqz
        br_if $B20
        local.get $l3
        i32.load offset=216
        local.get $p0
        i32.load offset=124
        i32.load offset=24
        i32.ne
        br_if $B20
        local.get $p0
        i32.const 0
        i32.store offset=120
        local.get $p0
        i32.const 0
        i32.store8 offset=118
        local.get $l3
        i32.const 0
        i32.store offset=208
        local.get $l4
        i32.load offset=20
        local.get $l3
        i32.const 212
        i32.add
        i32.const 0
        call $f56989
        i32.eqz
        if $I21
          i32.const 3748808
          i32.load
          local.tee $p1
          i32.load offset=116
          i32.eqz
          if $I22
            local.get $p1
            call $f65192
          end
          i32.const 3855760
          i32.load
          i32.const 0
          call $f42976
          i32.const 0
          local.set $p1
        end
        local.get $l4
        i32.load offset=24
        local.get $l3
        i32.const 208
        i32.add
        i32.const 0
        call $f56989
        i32.eqz
        if $I23
          i32.const 0
          local.set $p1
          i32.const 3748808
          i32.load
          local.tee $p2
          i32.load offset=116
          i32.eqz
          if $I24
            local.get $p2
            call $f65192
          end
          i32.const 3858552
          i32.load
          i32.const 0
          call $f42976
        end
        local.get $l4
        i32.load offset=28
        local.get $l3
        i32.const 204
        i32.add
        i32.const 0
        call $f56989
        i32.eqz
        if $I25
          i32.const 3748808
          i32.load
          local.tee $p1
          i32.load offset=116
          i32.eqz
          if $I26
            local.get $p1
            call $f65192
          end
          i32.const 0
          local.set $p1
          i32.const 3856860
          i32.load
          i32.const 0
          call $f42976
          br $B3
        end
        local.get $p1
        i32.eqz
        if $I27
          local.get $p1
          i32.const 0
          i32.ne
          local.set $p1
          br $B3
        end
        block $B28
          local.get $l3
          f32.load offset=212
          local.tee $l10
          f32.const 0x1.a36e2ep-14 (;=0.0001;)
          f32.lt
          if $I29
            local.get $l3
            i32.const 1065353216
            i32.store offset=212
            br $B28
          end
          local.get $l10
          f32.const 0x1.8p+2 (;=6;)
          f32.gt
          i32.eqz
          br_if $B28
          local.get $l3
          i32.const 1086324736
          i32.store offset=212
        end
        block $B30
          local.get $l3
          f32.load offset=208
          local.tee $l10
          f32.const 0x1.1d70a4p+1 (;=2.23;)
          f32.gt
          if $I31
            local.get $l3
            i32.const 1074706514
            i32.store offset=208
            br $B30
          end
          local.get $l10
          f32.const -0x1.1d70a4p+1 (;=-2.23;)
          f32.lt
          i32.eqz
          br_if $B30
          local.get $l3
          i32.const -1072777134
          i32.store offset=208
        end
        block $B32
          local.get $l3
          f32.load offset=204
          local.tee $l10
          f32.const 0x1.f66666p+3 (;=15.7;)
          f32.gt
          if $I33
            local.get $l3
            i32.const 1098593075
            i32.store offset=204
            br $B32
          end
          local.get $l10
          f32.const -0x1.f66666p+3 (;=-15.7;)
          f32.lt
          i32.eqz
          br_if $B32
          local.get $l3
          i32.const -1048890573
          i32.store offset=204
        end
        i32.const 3748808
        i32.load
        local.tee $p1
        i32.load offset=116
        i32.eqz
        if $I34
          local.get $p1
          call $f65192
        end
        i32.const 3835100
        i32.load
        i32.const 0
        call $f42976
        block $B35
          block $B36
            local.get $p0
            i32.load offset=124
            local.tee $p1
            i32.load offset=24
            i32.eqz
            if $I37
              local.get $p1
              i32.load offset=8
              local.set $p1
              local.get $p0
              i32.load offset=240
              local.set $p2
              i32.const 3752504
              i32.load
              local.tee $l4
              i32.load offset=116
              i32.eqz
              br_if $B36
              br $B35
            end
            local.get $p1
            i32.load offset=8
            local.set $p1
            local.get $p0
            i32.load offset=244
            local.set $p2
            i32.const 3752504
            i32.load
            local.tee $l4
            i32.load offset=116
            br_if $B35
          end
          local.get $l4
          call $f65192
        end
        block $B38 (result i32)
          local.get $p1
          f64.convert_i32_s
          f64.const 0x1p-1 (;=0.5;)
          f64.mul
          f64.floor
          local.tee $l12
          f64.abs
          f64.const 0x1p+31 (;=2.14748e+09;)
          f64.lt
          if $I39
            local.get $l12
            i32.trunc_f64_s
            br $B38
          end
          i32.const -2147483648
        end
        local.set $l4
        i32.const 1
        local.set $p1
        local.get $p2
        local.get $l4
        i32.const 3773132
        i32.load
        call $f2903
        local.tee $l4
        i32.const 1
        i32.const 0
        call $f54405
        local.get $p0
        i32.load offset=212
        i32.const 0
        call $f54401
        local.set $l5
        local.get $l3
        local.get $p0
        i32.const 224
        i32.add
        local.tee $p2
        i32.load
        i32.store offset=88
        local.get $l3
        local.get $p0
        i64.load offset=216 align=4
        i64.store offset=80
        local.get $l5
        local.get $l3
        i32.const 80
        i32.add
        i32.const 0
        call $f54626
        local.get $l3
        i32.const 184
        i32.add
        local.get $p0
        i32.load offset=212
        i32.const 0
        call $f54401
        i32.const 0
        call $f54624
        local.get $p2
        local.get $l3
        i32.load offset=192
        i32.store
        local.get $p0
        local.get $l3
        i64.load offset=184
        i64.store offset=216 align=4
        local.get $l3
        i32.const 168
        i32.add
        local.get $l4
        i32.const 0
        call $f54401
        i32.const 0
        call $f54624
        local.get $l3
        f32.load offset=168
        local.set $l10
        local.get $l3
        f32.load offset=172
        local.set $l11
        local.get $p0
        local.get $l3
        f32.load offset=176
        local.get $p2
        f32.load
        f32.sub
        f32.store offset=236
        local.get $p0
        local.get $l11
        local.get $p0
        f32.load offset=220
        f32.sub
        f32.store offset=232
        local.get $p0
        local.get $l10
        local.get $p0
        f32.load offset=216
        f32.sub
        f32.store offset=228
        i32.const 3821460
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792480
        i32.load
        call $f34548
        local.set $p2
        local.get $l3
        i32.const 1
        i32.store offset=164
        i32.const 3751540
        i32.load
        local.get $l3
        i32.const 164
        i32.add
        call $f1675
        local.set $l5
        local.get $p2
        i32.const 3837344
        i32.load
        local.get $l5
        i32.const 0
        call $f54371
        local.get $l3
        i32.const 168
        i32.add
        local.get $l4
        i32.const 3792572
        i32.load
        call $f34548
        local.tee $p2
        i32.const 0
        call $f32544
        local.get $l3
        i32.const 160
        i32.add
        local.tee $l5
        local.get $l3
        f32.load offset=176
        local.get $l3
        f32.load offset=208
        f32.sub
        f32.store
        local.get $l3
        local.get $l5
        i32.load
        i32.store offset=72
        local.get $l3
        local.get $l3
        i64.load offset=168
        local.tee $l13
        i64.store offset=152
        local.get $l3
        local.get $l13
        i64.store offset=64
        local.get $p2
        local.get $l3
        i32.const -64
        i32.sub
        i32.const 0
        call $f32546
        i32.const 3821464
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792544
        i32.load
        call $f34548
        local.get $l4
        i32.const 0
        call $f54401
        i32.store offset=16
        local.get $l3
        f32.load offset=212
        local.set $l10
        local.get $l3
        local.get $p0
        i32.load offset=124
        local.get $l3
        call $f60057
        drop
        local.get $l4
        i32.const 3792496
        i32.load
        call $f34548
        i32.const 0
        call $f32557
        f32.const 0x0p+0 (;=0;)
        i32.const 0
        call $f32512
        local.get $l4
        i32.const 3792496
        i32.load
        call $f34548
        i32.const 0
        call $f32557
        f32.const 0x0p+0 (;=0;)
        i32.const 0
        call $f32511
        local.get $l4
        i32.const 3792572
        i32.load
        call $f34548
        local.set $p2
        local.get $l3
        i64.const 0
        i64.store offset=140 align=4
        local.get $l3
        local.get $l3
        i32.load offset=144
        i32.store offset=56
        local.get $l3
        local.get $l10
        f32.store offset=136
        local.get $l3
        local.get $l3
        i64.load offset=136
        i64.store offset=48
        local.get $p2
        local.get $l3
        i32.const 48
        i32.add
        i32.const 0
        call $f32521
        local.get $l4
        i32.const 3792572
        i32.load
        call $f34548
        local.set $p2
        local.get $l3
        i32.const 0
        i32.store offset=128
        local.get $l3
        i32.const 0
        i32.store offset=40
        local.get $l3
        i32.const 0
        i32.store offset=120
        local.get $l3
        local.get $l3
        f32.load offset=204
        f32.store offset=124
        local.get $l3
        local.get $l3
        i64.load offset=120
        i64.store offset=32
        local.get $p2
        local.get $l3
        i32.const 32
        i32.add
        i32.const 0
        call $f32524
        local.get $p0
        local.get $l4
        i32.store offset=260
        local.get $p0
        i32.const 1
        i32.store8 offset=264
        br $B3
      end
      block $B40
        local.get $l4
        i32.const 16
        i32.add
        local.tee $p2
        i32.load
        i32.const 3835920
        i32.load
        i32.const 0
        call $f53861
        i32.eqz
        br_if $B40
        local.get $l3
        i32.load offset=216
        local.get $p0
        i32.load offset=124
        i32.load offset=24
        i32.ne
        br_if $B40
        local.get $p0
        i32.load offset=260
        i32.const 3792500
        i32.load
        call $f34548
        i32.load8_u offset=17
        i32.eqz
        br_if $B3
        i32.const 3820972
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792588
        i32.load
        call $f34548
        i32.const 1
        i32.store8 offset=24
        local.get $l4
        i32.load offset=20
        local.get $l3
        i32.const 200
        i32.add
        i32.const 0
        call $f56989
        local.tee $p1
        i32.eqz
        if $I41
          i32.const 3748808
          i32.load
          local.tee $l4
          i32.load offset=116
          i32.eqz
          if $I42
            local.get $l4
            call $f65192
          end
          i32.const 3849248
          i32.load
          i32.const 0
          call $f42976
        end
        i32.const 3820972
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792588
        i32.load
        call $f34548
        local.get $l3
        f32.load offset=200
        f32.store offset=28
        br $B3
      end
      block $B43
        local.get $p2
        i32.load
        i32.const 3833976
        i32.load
        i32.const 0
        call $f53861
        i32.eqz
        br_if $B43
        local.get $l3
        i32.load offset=216
        local.get $p0
        i32.load offset=124
        i32.load offset=24
        i32.ne
        br_if $B43
        i32.const 1
        local.set $p2
        loop $L44
          local.get $l4
          local.get $p2
          i32.const 2
          i32.shl
          local.tee $p1
          i32.add
          i32.const 16
          i32.add
          local.tee $l5
          i32.load
          local.set $l6
          local.get $p0
          i32.load offset=136
          local.set $l8
          i32.const 3748144
          i32.load
          local.tee $l7
          i32.load offset=116
          i32.eqz
          if $I45
            local.get $l7
            call $f65192
          end
          local.get $p1
          local.get $l8
          i32.add
          local.get $l6
          i32.const 0
          call $f58954
          f32.const -0x1.3p+1 (;=-2.375;)
          f32.add
          f32.store offset=16
          local.get $p1
          local.get $p0
          i32.load offset=136
          i32.add
          local.get $l5
          i32.load
          i32.const 0
          call $f58954
          f32.const -0x1.3851ecp+2 (;=-4.88;)
          f32.add
          f32.store offset=20
          local.get $p2
          i32.const 30
          i32.lt_u
          local.set $l5
          i32.const 1
          local.set $p1
          local.get $p2
          i32.const 2
          i32.add
          local.set $p2
          local.get $l5
          br_if $L44
        end
        br $B3
      end
      block $B46
        local.get $l4
        i32.const 16
        i32.add
        local.tee $p2
        i32.load
        i32.const 3821168
        i32.load
        i32.const 0
        call $f53861
        i32.eqz
        br_if $B46
        local.get $p0
        i32.load8_u offset=28
        i32.eqz
        br_if $B46
        i32.const 3748808
        i32.load
        local.tee $p2
        i32.load offset=116
        i32.eqz
        if $I47
          local.get $p2
          call $f65192
        end
        i32.const 3851396
        i32.load
        i32.const 0
        call $f42976
        local.get $p0
        i32.const 32
        i32.add
        i32.const 0
        call $f57314
        local.set $p2
        local.get $l3
        i32.const 216
        i32.add
        i32.const 0
        call $f57314
        local.set $l5
        i32.const 3847788
        i32.load
        local.get $p2
        i32.const 3816120
        i32.load
        local.get $l5
        i32.const 0
        call $f53874
        i32.const 0
        call $f42976
        local.get $l3
        i32.load offset=216
        local.get $p0
        i32.load offset=32
        i32.ne
        br_if $B3
        i32.const 3748808
        i32.load
        local.tee $p1
        i32.load offset=116
        i32.eqz
        if $I48
          local.get $p1
          call $f65192
        end
        i32.const 3851256
        i32.load
        i32.const 0
        call $f42976
        local.get $p0
        i32.const 0
        i32.store offset=36
        local.get $p0
        i32.const 0
        i32.store8 offset=28
        i32.const 3816036
        i32.load
        local.get $l4
        i32.const 0
        call $f53884
        local.set $p1
        i32.const 3848140
        i32.load
        local.get $p1
        i32.const 0
        call $f53732
        i32.const 0
        call $f42976
        i32.const 3848144
        i32.load
        local.get $l4
        i32.const 20
        i32.add
        local.tee $p1
        i32.load
        i32.const 0
        call $f53732
        i32.const 0
        call $f42976
        local.get $l3
        local.get $l4
        i32.load offset=12
        i32.const 1
        i32.gt_s
        i32.store8 offset=199
        i32.const 3747280
        i32.load
        local.tee $p2
        i32.load offset=116
        i32.eqz
        if $I49
          local.get $p2
          call $f65192
        end
        local.get $l3
        i32.const 199
        i32.add
        i32.const 0
        call $f58644
        local.set $p2
        i32.const 3848148
        i32.load
        local.get $p2
        i32.const 0
        call $f53732
        i32.const 0
        call $f42976
        local.get $l3
        local.get $p1
        i32.load
        i32.const 3834920
        i32.load
        i32.const 0
        call $f53861
        i32.store8 offset=199
        local.get $l3
        i32.const 199
        i32.add
        i32.const 0
        call $f58644
        local.set $p2
        i32.const 3848152
        i32.load
        local.get $p2
        i32.const 0
        call $f53732
        i32.const 0
        call $f42976
        local.get $l3
        local.get $p1
        i32.load
        i32.const 3834920
        i32.load
        i32.const 5
        i32.const 0
        call $f53932
        i32.store8 offset=199
        local.get $l3
        i32.const 199
        i32.add
        i32.const 0
        call $f58644
        local.set $p1
        i32.const 3848156
        i32.load
        local.get $p1
        i32.const 0
        call $f53732
        i32.const 0
        call $f42976
        block $B50
          local.get $l4
          i32.load offset=12
          i32.const 2
          i32.lt_s
          br_if $B50
          block $B51
            local.get $l4
            i32.load offset=20
            i32.const 3834920
            i32.load
            i32.const 5
            i32.const 0
            call $f53932
            if $I52
              i32.const 3748808
              i32.load
              local.tee $p1
              i32.load offset=116
              i32.eqz
              if $I53
                local.get $p1
                call $f65192
              end
              i32.const 3851260
              i32.load
              i32.const 0
              call $f42976
              i32.const 3834392
              i32.load
              i32.const 0
              call $f42976
              local.get $p0
              i32.load offset=124
              local.get $p0
              i32.load offset=132
              call $f1448
              local.tee $p1
              i32.const 3745900
              i32.load
              call $f55390
              i32.store offset=28
              local.get $p1
              i32.const 3745900
              i32.load
              call $f55390
              drop
              local.get $p0
              local.get $p0
              i32.load offset=132
              call $f1448
              local.tee $p1
              i32.const 3745900
              i32.load
              call $f55390
              i32.store offset=128
              local.get $p1
              i32.const 3745900
              i32.load
              call $f55390
              drop
              local.get $p0
              local.get $p0
              i32.const 132
              i32.add
              local.tee $p1
              local.get $l3
              call $f60062
              local.get $p0
              i32.const 1
              i32.store8 offset=84
              i32.const 3816036
              i32.load
              local.get $p0
              i32.load offset=132
              i32.const 3800744
              i32.load
              call $f54805
              local.set $l4
              i32.const 3854648
              i32.load
              local.get $l4
              i32.const 0
              call $f53732
              i32.const 0
              call $f42976
              i32.const 3816036
              i32.load
              local.get $p0
              i32.load offset=128
              i32.const 3800744
              i32.load
              call $f54805
              local.set $l4
              i32.const 3852284
              i32.load
              local.get $l4
              i32.const 0
              call $f53732
              i32.const 0
              call $f42976
              br $B51
            end
            local.get $l4
            i32.load offset=12
            i32.const 2
            i32.lt_s
            br_if $B50
            local.get $l4
            i32.load offset=20
            i32.const 3830768
            i32.load
            i32.const 0
            call $f53861
            i32.eqz
            br_if $B50
            i32.const 3748808
            i32.load
            local.tee $p1
            i32.load offset=116
            i32.eqz
            if $I54
              local.get $p1
              call $f65192
            end
            i32.const 3851264
            i32.load
            i32.const 0
            call $f42976
            i32.const 3834388
            i32.load
            i32.const 0
            call $f42976
            local.get $p0
            i32.const 132
            i32.add
            local.set $p1
          end
          local.get $p1
          i32.const 0
          i32.store
        end
        i32.const 3748808
        i32.load
        local.tee $p1
        i32.load offset=116
        i32.eqz
        if $I55
          local.get $p1
          call $f65192
        end
        i32.const 3851268
        i32.load
        i32.const 0
        call $f42976
        i32.const 1
        local.set $p1
        local.get $p0
        i32.load8_u offset=112
        br_if $B3
        local.get $p0
        local.get $l3
        call $f60063
        local.get $p0
        i32.load8_u offset=112
        br_if $B3
        local.get $p0
        i32.const 3836268
        i32.load
        f32.const 0x1p+4 (;=16;)
        i32.const 0
        call $f54430
        br $B3
      end
      local.get $p2
      i32.load
      i32.const 3825320
      i32.load
      i32.const 0
      call $f53861
      if $I56
        local.get $l4
        i32.load offset=20
        local.get $p0
        i32.const 304
        i32.add
        i32.const 0
        call $f56605
        br_if $B3
        i32.const 3748808
        i32.load
        local.tee $p1
        i32.load offset=116
        i32.eqz
        if $I57
          local.get $p1
          call $f65192
        end
        i32.const 0
        local.set $p1
        i32.const 3850000
        i32.load
        i32.const 0
        call $f42976
        br $B3
      end
      block $B58
        local.get $l4
        i32.const 16
        i32.add
        local.tee $p2
        i32.load
        i32.const 3834924
        i32.load
        i32.const 0
        call $f53861
        i32.eqz
        br_if $B58
        local.get $l3
        i32.load offset=216
        local.get $p0
        i32.load offset=124
        i32.load offset=24
        i32.ne
        br_if $B58
        i32.const 3748808
        i32.load
        local.tee $p1
        i32.load offset=116
        i32.eqz
        if $I59
          local.get $p1
          call $f65192
        end
        i32.const 3835092
        i32.load
        i32.const 0
        call $f42976
        local.get $p0
        i32.const 1
        i32.store8 offset=40
        local.get $p0
        i32.const 136
        i32.add
        local.set $l8
        i32.const 0
        local.set $p1
        loop $L60
          local.get $l4
          local.get $p1
          i32.const 1
          i32.or
          i32.const 2
          i32.shl
          local.tee $l5
          i32.add
          i32.const 16
          i32.add
          local.tee $l6
          i32.load
          local.set $p2
          i32.const 3748144
          i32.load
          local.tee $l7
          i32.load offset=116
          i32.eqz
          if $I61
            local.get $l7
            call $f65192
          end
          block $B62 (result f32)
            block $B63
              local.get $p2
              i32.const 0
              call $f58954
              f32.const 0x1.0c6f7ap-20 (;=1e-06;)
              f32.gt
              i32.eqz
              if $I64
                local.get $l4
                local.get $p1
                i32.const 2
                i32.add
                local.tee $p2
                i32.const 2
                i32.shl
                i32.add
                i32.load offset=16
                local.set $l7
                i32.const 3748144
                i32.load
                local.tee $l9
                i32.load offset=116
                i32.eqz
                if $I65
                  local.get $l9
                  call $f65192
                end
                local.get $l7
                i32.const 0
                call $f58954
                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                f32.gt
                i32.eqz
                br_if $B63
              end
              local.get $l6
              i32.load
              local.set $p2
              local.get $l8
              i32.load
              local.set $l6
              i32.const 3748144
              i32.load
              local.tee $l7
              i32.load offset=116
              i32.eqz
              if $I66
                local.get $l7
                call $f65192
              end
              local.get $l6
              local.get $p1
              i32.const 2
              i32.shl
              i32.add
              local.get $p2
              i32.const 0
              call $f58954
              f32.const -0x1.3p+1 (;=-2.375;)
              f32.add
              f32.store offset=16
              local.get $l8
              i32.load
              local.set $l6
              local.get $l4
              local.get $p1
              i32.const 2
              i32.add
              local.tee $p2
              i32.const 2
              i32.shl
              i32.add
              i32.load offset=16
              i32.const 0
              call $f58954
              f32.const -0x1.3851fp+2 (;=-4.88;)
              f32.add
              br $B62
            end
            local.get $l8
            i32.load
            local.tee $l6
            local.get $p1
            i32.const 2
            i32.shl
            i32.add
            i32.const 0
            i32.store offset=16
            f32.const 0x0p+0 (;=0;)
          end
          local.set $l10
          local.get $l5
          local.get $l6
          i32.add
          local.get $l10
          f32.store offset=16
          local.get $p1
          i32.const 30
          i32.lt_u
          local.set $l5
          local.get $p2
          local.set $p1
          local.get $l5
          br_if $L60
        end
        local.get $p0
        local.get $l8
        local.get $l3
        call $f60062
        i32.const 3816036
        i32.load
        local.get $p0
        i32.load offset=136
        i32.const 3800744
        i32.load
        call $f54805
        local.set $p1
        i32.const 3854688
        i32.load
        local.get $p1
        i32.const 0
        call $f53732
        local.set $p1
        i32.const 3748808
        i32.load
        local.tee $l4
        i32.load offset=116
        i32.eqz
        if $I67
          local.get $l4
          call $f65192
        end
        local.get $p1
        i32.const 0
        call $f42976
        local.get $p0
        local.get $p0
        i32.load offset=136
        call $f1448
        local.tee $p1
        i32.const 3745900
        i32.load
        call $f55390
        i32.store offset=128
        local.get $p1
        i32.const 3745900
        i32.load
        call $f55390
        drop
        local.get $p0
        i32.load offset=124
        local.get $p0
        i32.load offset=136
        call $f1448
        local.tee $p1
        i32.const 3745900
        i32.load
        call $f55390
        i32.store offset=28
        local.get $p1
        i32.const 3745900
        i32.load
        call $f55390
        drop
        i32.const 1
        local.set $p1
        br $B3
      end
      local.get $p2
      i32.load
      i32.const 3834928
      i32.load
      i32.const 0
      call $f53861
      i32.eqz
      br_if $B3
      i32.const 3748808
      i32.load
      local.tee $p1
      i32.load offset=116
      i32.eqz
      if $I68
        local.get $p1
        call $f65192
      end
      i32.const 3835096
      i32.load
      i32.const 0
      call $f42976
      i32.const 1
      local.set $p1
      local.get $p0
      i32.const 1
      i32.store8 offset=41
      local.get $p0
      local.get $l4
      local.get $l3
      call $f60064
    end
    local.get $l3
    i32.const 240
    i32.add
    global.set $g0
    local.get $p1)