  (func $f60175 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 f32) (local $l13 f32) (local $l14 f64) (local $l15 i64)
    global.get $g0
    i32.const 160
    i32.sub
    local.tee $p2
    global.set $g0
    i32.const 4674502
    i32.load8_u
    i32.eqz
    if $I0
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
      i32.const 3792604
      call $f1661
      i32.const 3792608
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
      i32.const 3820588
      call $f1661
      i32.const 3821168
      call $f1661
      i32.const 3813948
      call $f1661
      i32.const 3852284
      call $f1661
      i32.const 3843868
      call $f1661
      i32.const 3820972
      call $f1661
      i32.const 3832492
      call $f1661
      i32.const 3850800
      call $f1661
      i32.const 3834388
      call $f1661
      i32.const 3821460
      call $f1661
      i32.const 3833976
      call $f1661
      i32.const 3814476
      call $f1661
      i32.const 3834392
      call $f1661
      i32.const 3835100
      call $f1661
      i32.const 3834396
      call $f1661
      i32.const 3834920
      call $f1661
      i32.const 3856860
      call $f1661
      i32.const 3858552
      call $f1661
      i32.const 3834896
      call $f1661
      i32.const 3817856
      call $f1661
      i32.const 3827816
      call $f1661
      i32.const 3854648
      call $f1661
      i32.const 3837344
      call $f1661
      i32.const 3843860
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
      i32.const 3855760
      call $f1661
      i32.const 3849248
      call $f1661
      i32.const 3836268
      call $f1661
      i32.const 4674502
      i32.const 1
      i32.store8
    end
    local.get $p2
    i32.const 0
    i32.store offset=156
    local.get $p2
    i32.const 0
    i32.store offset=152
    local.get $p2
    i32.const 0
    i32.store offset=148
    local.get $p2
    i32.const 0
    i32.store offset=144
    local.get $p1
    i32.load offset=32
    i32.const 0
    call $f53919
    local.set $l3
    i32.const 3754332
    i32.load
    local.tee $l4
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $l4
      call $f65192
    end
    local.get $l3
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
    local.set $l3
    local.get $p1
    i32.load offset=28
    local.set $l8
    local.get $p1
    i32.load offset=8
    local.set $l5
    i32.const 3827816
    i32.load
    local.get $p1
    i32.load offset=32
    i32.const 0
    call $f53732
    local.set $p1
    i32.const 3748808
    i32.load
    local.tee $l4
    i32.load offset=116
    i32.eqz
    if $I2
      local.get $l4
      call $f65192
    end
    local.get $p1
    i32.const 0
    call $f42976
    i32.const 1
    local.set $p1
    block $B3
      local.get $l3
      i32.load offset=12
      i32.eqz
      br_if $B3
      local.get $p0
      i32.load offset=252
      i32.const 3850800
      i32.load
      local.get $l3
      i32.const 16
      i32.add
      local.tee $l4
      i32.load
      i32.const 0
      call $f53732
      i32.const 0
      call $f61055
      block $B4
        local.get $l4
        i32.load
        i32.const 3832492
        i32.load
        i32.const 0
        call $f53861
        i32.eqz
        br_if $B4
        local.get $l3
        i32.load offset=12
        i32.const 2
        i32.lt_s
        br_if $B4
        local.get $l8
        i32.const 3834396
        i32.load
        i32.const 0
        call $f53861
        local.set $l7
        local.get $l3
        i32.load offset=20
        local.set $l6
        block $B5 (result i32)
          local.get $l7
          if $I6
            local.get $p0
            local.get $l6
            i32.store offset=36
            local.get $p0
            i32.const 28
            i32.add
            local.set $l9
            i32.const 3843860
            local.set $l10
            local.get $p0
            i32.const 36
            i32.add
            br $B5
          end
          local.get $p0
          local.get $l6
          i32.store offset=40
          local.get $p0
          i32.const 32
          i32.add
          local.set $l9
          i32.const 3843868
          local.set $l10
          i32.const 1
          local.set $l11
          local.get $p0
          i32.const 40
          i32.add
        end
        local.set $l7
        local.get $l9
        local.get $l6
        i32.store
        local.get $p0
        i32.load offset=136
        local.get $l11
        i32.const 3773132
        i32.load
        call $f2903
        i32.const 3792608
        i32.load
        call $f34548
        local.tee $l6
        local.get $l7
        i32.load
        local.get $l6
        i32.load
        local.tee $l6
        i32.load offset=796
        local.get $l6
        i32.load offset=792
        call_indirect $__indirect_function_table (type $t2)
        local.get $l10
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792604
        i32.load
        call $f34548
        local.tee $l6
        local.get $l7
        i32.load
        i32.const 3817856
        i32.load
        i32.const 0
        call $f53732
        local.get $l6
        i32.load
        local.tee $l6
        i32.load offset=724
        local.get $l6
        i32.load offset=720
        call_indirect $__indirect_function_table (type $t2)
      end
      local.get $l4
      i32.load
      i32.const 3834892
      i32.load
      i32.const 0
      call $f53861
      if $I7
        i32.const 3834896
        i32.load
        local.get $l8
        i32.const 3814476
        i32.load
        i32.const 0
        call $f53871
        local.set $l3
        i32.const 3748808
        i32.load
        local.tee $l4
        i32.load offset=116
        i32.eqz
        if $I8
          local.get $l4
          call $f65192
        end
        local.get $l3
        i32.const 0
        call $f42976
        block $B9
          block $B10
            local.get $l5
            br_table $B10 $B9 $B3
          end
          local.get $p0
          i32.const 1
          i32.store8 offset=87
          br $B3
        end
        local.get $p0
        i32.const 1
        i32.store8 offset=88
        br $B3
      end
      block $B11
        local.get $l3
        i32.const 16
        i32.add
        local.tee $l4
        i32.load
        i32.const 3820588
        i32.load
        i32.const 0
        call $f53861
        i32.eqz
        br_if $B11
        local.get $l5
        local.get $p0
        i32.load offset=96
        i32.load offset=24
        i32.ne
        br_if $B11
        local.get $p0
        i32.const 0
        i32.store offset=92
        local.get $p0
        i32.const 0
        i32.store8 offset=90
        local.get $p2
        i32.const 0
        i32.store offset=152
        local.get $l3
        i32.load offset=20
        local.get $p2
        i32.const 156
        i32.add
        i32.const 0
        call $f56989
        i32.eqz
        if $I12
          i32.const 3748808
          i32.load
          local.tee $p1
          i32.load offset=116
          i32.eqz
          if $I13
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
        local.get $l3
        i32.load offset=24
        local.get $p2
        i32.const 152
        i32.add
        i32.const 0
        call $f56989
        i32.eqz
        if $I14
          i32.const 0
          local.set $p1
          i32.const 3748808
          i32.load
          local.tee $l4
          i32.load offset=116
          i32.eqz
          if $I15
            local.get $l4
            call $f65192
          end
          i32.const 3858552
          i32.load
          i32.const 0
          call $f42976
        end
        local.get $l3
        i32.load offset=28
        local.get $p2
        i32.const 148
        i32.add
        i32.const 0
        call $f56989
        i32.eqz
        if $I16
          i32.const 3748808
          i32.load
          local.tee $p0
          i32.load offset=116
          i32.eqz
          if $I17
            local.get $p0
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
        if $I18
          local.get $p1
          i32.const 0
          i32.ne
          local.set $p1
          br $B3
        end
        block $B19
          local.get $p2
          f32.load offset=156
          local.tee $l12
          f32.const 0x1.a36e2ep-14 (;=0.0001;)
          f32.lt
          if $I20
            local.get $p2
            i32.const 1065353216
            i32.store offset=156
            br $B19
          end
          local.get $l12
          f32.const 0x1.8p+2 (;=6;)
          f32.gt
          i32.eqz
          br_if $B19
          local.get $p2
          i32.const 1086324736
          i32.store offset=156
        end
        block $B21
          local.get $p2
          f32.load offset=152
          local.tee $l12
          f32.const 0x1.1d70a4p+1 (;=2.23;)
          f32.gt
          if $I22
            local.get $p2
            i32.const 1074706514
            i32.store offset=152
            br $B21
          end
          local.get $l12
          f32.const -0x1.1d70a4p+1 (;=-2.23;)
          f32.lt
          i32.eqz
          br_if $B21
          local.get $p2
          i32.const -1072777134
          i32.store offset=152
        end
        block $B23
          local.get $p2
          f32.load offset=148
          local.tee $l12
          f32.const 0x1.f66666p+3 (;=15.7;)
          f32.gt
          if $I24
            local.get $p2
            i32.const 1098593075
            i32.store offset=148
            br $B23
          end
          local.get $l12
          f32.const -0x1.f66666p+3 (;=-15.7;)
          f32.lt
          i32.eqz
          br_if $B23
          local.get $p2
          i32.const -1048890573
          i32.store offset=148
        end
        i32.const 3748808
        i32.load
        local.tee $p1
        i32.load offset=116
        i32.eqz
        if $I25
          local.get $p1
          call $f65192
        end
        i32.const 3835100
        i32.load
        i32.const 0
        call $f42976
        block $B26
          block $B27
            local.get $p0
            i32.load offset=96
            local.tee $p1
            i32.load offset=24
            i32.eqz
            if $I28
              local.get $p1
              i32.load offset=8
              local.set $p1
              local.get $p0
              i32.load offset=192
              local.set $l4
              i32.const 3752504
              i32.load
              local.tee $l3
              i32.load offset=116
              i32.eqz
              br_if $B27
              br $B26
            end
            local.get $p1
            i32.load offset=8
            local.set $p1
            local.get $p0
            i32.load offset=196
            local.set $l4
            i32.const 3752504
            i32.load
            local.tee $l3
            i32.load offset=116
            br_if $B26
          end
          local.get $l3
          call $f65192
        end
        block $B29 (result i32)
          local.get $p1
          f64.convert_i32_s
          f64.const 0x1p-1 (;=0.5;)
          f64.mul
          f64.floor
          local.tee $l14
          f64.abs
          f64.const 0x1p+31 (;=2.14748e+09;)
          f64.lt
          if $I30
            local.get $l14
            i32.trunc_f64_s
            br $B29
          end
          i32.const -2147483648
        end
        local.set $l3
        i32.const 1
        local.set $p1
        local.get $l4
        local.get $l3
        i32.const 3773132
        i32.load
        call $f2903
        local.tee $l3
        i32.const 1
        i32.const 0
        call $f54405
        local.get $p0
        i32.load offset=164
        i32.const 0
        call $f54401
        local.set $l5
        local.get $p2
        local.get $p0
        i32.const 176
        i32.add
        local.tee $l4
        i32.load
        i32.store offset=56
        local.get $p2
        local.get $p0
        i64.load offset=168 align=4
        i64.store offset=48
        local.get $l5
        local.get $p2
        i32.const 48
        i32.add
        i32.const 0
        call $f54626
        local.get $p2
        i32.const 128
        i32.add
        local.get $p0
        i32.load offset=164
        i32.const 0
        call $f54401
        i32.const 0
        call $f54624
        local.get $l4
        local.get $p2
        i32.load offset=136
        i32.store
        local.get $p0
        local.get $p2
        i64.load offset=128
        i64.store offset=168 align=4
        local.get $p2
        i32.const 112
        i32.add
        local.get $l3
        i32.const 0
        call $f54401
        i32.const 0
        call $f54624
        local.get $p2
        f32.load offset=112
        local.set $l12
        local.get $p2
        f32.load offset=116
        local.set $l13
        local.get $p0
        local.get $p2
        f32.load offset=120
        local.get $l4
        f32.load
        f32.sub
        f32.store offset=188
        local.get $p0
        local.get $l13
        local.get $p0
        f32.load offset=172
        f32.sub
        f32.store offset=184
        local.get $p0
        local.get $l12
        local.get $p0
        f32.load offset=168
        f32.sub
        f32.store offset=180
        i32.const 3821460
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792480
        i32.load
        call $f34548
        local.set $l4
        local.get $p2
        i32.const 1
        i32.store offset=108
        i32.const 3751540
        i32.load
        local.get $p2
        i32.const 108
        i32.add
        call $f1675
        local.set $l5
        local.get $l4
        i32.const 3837344
        i32.load
        local.get $l5
        i32.const 0
        call $f54371
        local.get $p2
        i32.const 112
        i32.add
        local.get $l3
        i32.const 3792572
        i32.load
        call $f34548
        local.tee $l4
        i32.const 0
        call $f32544
        local.get $p2
        i32.const 104
        i32.add
        local.tee $l5
        local.get $p2
        f32.load offset=120
        local.get $p2
        f32.load offset=152
        f32.sub
        f32.store
        local.get $p2
        local.get $l5
        i32.load
        i32.store offset=40
        local.get $p2
        local.get $p2
        i64.load offset=112
        local.tee $l15
        i64.store offset=96
        local.get $p2
        local.get $l15
        i64.store offset=32
        local.get $l4
        local.get $p2
        i32.const 32
        i32.add
        i32.const 0
        call $f32546
        i32.const 3821464
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792544
        i32.load
        call $f34548
        local.get $l3
        i32.const 0
        call $f54401
        i32.store offset=16
        local.get $p2
        f32.load offset=156
        local.set $l12
        local.get $p0
        local.get $p2
        call $f60172
        local.set $l4
        local.get $p0
        local.get $p0
        i32.load offset=96
        local.get $l4
        local.get $p2
        call $f60171
        local.get $l3
        i32.const 3792496
        i32.load
        call $f34548
        i32.const 0
        call $f32557
        f32.const 0x0p+0 (;=0;)
        i32.const 0
        call $f32512
        local.get $l3
        i32.const 3792496
        i32.load
        call $f34548
        i32.const 0
        call $f32557
        f32.const 0x0p+0 (;=0;)
        i32.const 0
        call $f32511
        local.get $l3
        i32.const 3792572
        i32.load
        call $f34548
        local.set $l4
        local.get $p2
        i64.const 0
        i64.store offset=84 align=4
        local.get $p2
        local.get $p2
        i32.load offset=88
        i32.store offset=24
        local.get $p2
        local.get $l12
        f32.store offset=80
        local.get $p2
        local.get $p2
        i64.load offset=80
        i64.store offset=16
        local.get $l4
        local.get $p2
        i32.const 16
        i32.add
        i32.const 0
        call $f32521
        local.get $l3
        i32.const 3792572
        i32.load
        call $f34548
        local.set $l4
        local.get $p2
        i32.const 0
        i32.store offset=72
        local.get $p2
        i32.const 0
        i32.store offset=8
        local.get $p2
        i32.const 0
        i32.store offset=64
        local.get $p2
        local.get $p2
        f32.load offset=148
        f32.store offset=68
        local.get $p2
        local.get $p2
        i64.load offset=64
        i64.store
        local.get $l4
        local.get $p2
        i32.const 0
        call $f32524
        local.get $p0
        local.get $l3
        i32.store offset=212
        local.get $p0
        i32.const 1
        i32.store8 offset=216
        br $B3
      end
      block $B31
        local.get $l4
        i32.load
        i32.const 3835920
        i32.load
        i32.const 0
        call $f53861
        i32.eqz
        br_if $B31
        local.get $l5
        local.get $p0
        i32.load offset=96
        i32.load offset=24
        i32.ne
        br_if $B31
        local.get $p0
        i32.load offset=212
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
        local.get $l3
        i32.load offset=20
        local.get $p2
        i32.const 144
        i32.add
        i32.const 0
        call $f56989
        local.tee $p1
        i32.eqz
        if $I32
          i32.const 3748808
          i32.load
          local.tee $p0
          i32.load offset=116
          i32.eqz
          if $I33
            local.get $p0
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
        local.get $p2
        f32.load offset=144
        f32.store offset=28
        br $B3
      end
      block $B34
        local.get $l3
        i32.const 16
        i32.add
        local.tee $l4
        i32.load
        i32.const 3833976
        i32.load
        i32.const 0
        call $f53861
        i32.eqz
        br_if $B34
        local.get $l5
        local.get $p0
        i32.load offset=96
        i32.load offset=24
        i32.ne
        br_if $B34
        loop $L35
          local.get $l3
          local.get $p1
          i32.const 2
          i32.shl
          local.tee $l4
          i32.add
          i32.const 16
          i32.add
          local.tee $l5
          i32.load
          local.set $l8
          local.get $p0
          i32.load offset=108
          local.set $l6
          i32.const 3748144
          i32.load
          local.tee $l7
          i32.load offset=116
          i32.eqz
          if $I36
            local.get $l7
            call $f65192
          end
          local.get $l4
          local.get $l6
          i32.add
          local.get $l8
          i32.const 0
          call $f58954
          f32.const -0x1.3p+1 (;=-2.375;)
          f32.add
          f32.store offset=16
          local.get $l4
          local.get $p0
          i32.load offset=108
          i32.add
          local.get $l5
          i32.load
          i32.const 0
          call $f58954
          f32.const -0x1.3851ecp+2 (;=-4.88;)
          f32.add
          f32.store offset=20
          local.get $p1
          i32.const 30
          i32.lt_u
          local.set $l4
          local.get $p1
          i32.const 2
          i32.add
          local.set $p1
          local.get $l4
          br_if $L35
        end
        i32.const 1
        local.set $p1
        br $B3
      end
      local.get $l4
      i32.load
      i32.const 3821168
      i32.load
      i32.const 0
      call $f53861
      i32.eqz
      br_if $B3
      local.get $p0
      i32.load8_u offset=16
      i32.eqz
      br_if $B3
      local.get $l5
      local.get $p0
      i32.load offset=20
      i32.ne
      br_if $B3
      local.get $p0
      i32.const 0
      i32.store offset=24
      local.get $p0
      i32.const 0
      i32.store8 offset=16
      block $B37
        local.get $l3
        i32.load offset=12
        i32.const 2
        i32.lt_s
        br_if $B37
        block $B38
          local.get $l3
          i32.load offset=20
          i32.const 3834920
          i32.load
          i32.const 0
          call $f53861
          if $I39
            i32.const 3748808
            i32.load
            local.tee $l3
            i32.load offset=116
            i32.eqz
            if $I40
              local.get $l3
              call $f65192
            end
            i32.const 3834392
            i32.load
            i32.const 0
            call $f42976
            local.get $p0
            i32.load offset=96
            local.get $p0
            i32.load offset=104
            call $f1448
            local.tee $l3
            i32.const 3745900
            i32.load
            call $f55390
            i32.store offset=28
            local.get $l3
            i32.const 3745900
            i32.load
            call $f55390
            drop
            local.get $p0
            local.get $p0
            i32.load offset=104
            call $f1448
            local.tee $l3
            i32.const 3745900
            i32.load
            call $f55390
            i32.store offset=100
            local.get $l3
            i32.const 3745900
            i32.load
            call $f55390
            drop
            local.get $p0
            local.get $p0
            i32.const 104
            i32.add
            local.tee $l3
            local.get $p2
            call $f60176
            i32.const 3816036
            i32.load
            local.get $p0
            i32.load offset=104
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
            i32.load offset=100
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
            local.get $p0
            i32.const 1
            i32.store8 offset=56
            br $B38
          end
          local.get $l3
          i32.load offset=12
          i32.const 2
          i32.lt_s
          br_if $B37
          local.get $l3
          i32.load offset=20
          i32.const 3830768
          i32.load
          i32.const 0
          call $f53861
          i32.eqz
          br_if $B37
          i32.const 3748808
          i32.load
          local.tee $l3
          i32.load offset=116
          i32.eqz
          if $I41
            local.get $l3
            call $f65192
          end
          i32.const 3834388
          i32.load
          i32.const 0
          call $f42976
          local.get $p0
          i32.const 104
          i32.add
          local.set $l3
        end
        local.get $l3
        i32.const 0
        i32.store
      end
      f32.const 0x1p+0 (;=1;)
      i32.const 0
      call $f54557
      local.get $p0
      i32.load8_u offset=84
      br_if $B3
      local.get $p0
      local.get $p2
      call $f60177
      local.get $p0
      i32.load8_u offset=84
      br_if $B3
      local.get $p0
      i32.const 3836268
      i32.load
      f32.const 0x1p+4 (;=16;)
      i32.const 0
      call $f54430
    end
    local.get $p2
    i32.const 160
    i32.add
    global.set $g0
    local.get $p1)
