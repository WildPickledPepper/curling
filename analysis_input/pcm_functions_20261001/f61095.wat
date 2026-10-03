  (func $f61095 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32)
    global.get $g0
    i32.const 48
    i32.sub
    local.tee $l4
    global.set $g0
    i32.const 4675160
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3739632
      call $f1661
      i32.const 3739640
      call $f1661
      i32.const 3787812
      call $f1661
      i32.const 3787796
      call $f1661
      i32.const 3787800
      call $f1661
      i32.const 3787804
      call $f1661
      i32.const 3787808
      call $f1661
      i32.const 3787820
      call $f1661
      i32.const 3748320
      call $f1661
      i32.const 3748808
      call $f1661
      i32.const 3792472
      call $f1661
      i32.const 3792480
      call $f1661
      i32.const 3792572
      call $f1661
      i32.const 3792608
      call $f1661
      i32.const 3792616
      call $f1661
      i32.const 3751540
      call $f1661
      i32.const 3775972
      call $f1661
      i32.const 3775968
      call $f1661
      i32.const 3772444
      call $f1661
      i32.const 3774248
      call $f1661
      i32.const 3772036
      call $f1661
      i32.const 3773132
      call $f1661
      i32.const 3743760
      call $f1661
      i32.const 3744048
      call $f1661
      i32.const 3743328
      call $f1661
      i32.const 3743412
      call $f1661
      i32.const 3752336
      call $f1661
      i32.const 3753376
      call $f1661
      i32.const 3745900
      call $f1661
      i32.const 3755556
      call $f1661
      i32.const 3756240
      call $f1661
      i32.const 3756236
      call $f1661
      i32.const 3756912
      call $f1661
      i32.const 3843888
      call $f1661
      i32.const 3843876
      call $f1661
      i32.const 3837032
      call $f1661
      i32.const 3843880
      call $f1661
      i32.const 3843868
      call $f1661
      i32.const 3854740
      call $f1661
      i32.const 3821460
      call $f1661
      i32.const 3817856
      call $f1661
      i32.const 3847392
      call $f1661
      i32.const 3837344
      call $f1661
      i32.const 3847380
      call $f1661
      i32.const 3825504
      call $f1661
      i32.const 3854032
      call $f1661
      i32.const 3843860
      call $f1661
      i32.const 3843884
      call $f1661
      i32.const 3821468
      call $f1661
      i32.const 3854728
      call $f1661
      i32.const 3813572
      call $f1661
      i32.const 3838212
      call $f1661
      i32.const 4675160
      i32.const 1
      i32.store8
    end
    local.get $l4
    i32.const 0
    i32.store offset=40
    local.get $l4
    i64.const 0
    i64.store offset=32
    i32.const 4675186
    i32.load8_u
    i32.eqz
    if $I1
      i32.const 3752300
      call $f1661
      i32.const 4675186
      i32.const 1
      i32.store8
    end
    local.get $p0
    i32.const 3752300
    i32.load
    i32.load offset=92
    i32.load
    local.tee $p1
    i32.store offset=32
    i32.const 3739640
    i32.load
    call $f1446
    local.tee $l2
    local.get $p0
    i32.const 3787812
    i32.load
    i32.const 0
    call $f30341
    local.get $p1
    local.get $l2
    i32.const 0
    call $f60648
    i32.const 3739632
    i32.load
    call $f1446
    local.tee $l5
    local.get $p0
    i32.const 3787820
    i32.load
    i32.const 0
    call $f30369
    i32.const 4675162
    i32.load8_u
    i32.eqz
    if $I2
      i32.const 3739632
      call $f1661
      i32.const 4675162
      i32.const 1
      i32.store8
    end
    local.get $p0
    i32.const 312
    i32.add
    local.set $l6
    local.get $p0
    i32.load offset=312
    local.set $p1
    block $B3
      loop $L4
        i32.const 0
        local.set $l2
        local.get $p1
        local.get $l5
        i32.const 0
        call $f58115
        local.tee $l3
        if $I5
          local.get $l3
          i32.const 3739632
          i32.load
          local.tee $l7
          call $f1674
          local.tee $l2
          i32.eqz
          br_if $B3
        end
        local.get $p1
        local.get $l6
        local.get $l2
        local.get $p1
        call $f1705
        local.tee $l2
        i32.ne
        local.set $l3
        local.get $l2
        local.set $p1
        local.get $l3
        br_if $L4
      end
      local.get $p0
      local.get $p1
      call $f61094
      i32.const 3743412
      i32.load
      call $f1446
      local.tee $l2
      i32.const 3772444
      i32.load
      call $f2715
      i32.const 3748320
      i32.load
      local.tee $p1
      i32.load offset=116
      if $I6 (result i32)
        local.get $p1
      else
        local.get $p1
        call $f65192
        i32.const 3748320
        i32.load
      end
      i32.load offset=92
      local.get $l2
      i32.store offset=4
      i32.const 3743760
      i32.load
      call $f1446
      local.tee $p1
      i32.const 3774248
      i32.load
      call $f2715
      i32.const 3748320
      i32.load
      i32.load offset=92
      local.get $p1
      i32.store offset=12
      i32.const 3744048
      i32.load
      call $f1446
      local.tee $p1
      i32.const 3775968
      i32.load
      call $f2715
      local.get $p0
      local.get $p1
      call $f61071
      local.set $l2
      i32.const 3775972
      i32.load
      local.set $l5
      local.get $p1
      local.get $p1
      i32.load offset=16
      i32.const 1
      i32.add
      i32.store offset=16
      block $B7
        local.get $p1
        i32.load offset=12
        local.tee $l3
        local.get $p1
        i32.load offset=8
        local.tee $l6
        i32.load offset=12
        i32.lt_u
        if $I8
          local.get $p1
          local.get $l3
          i32.const 1
          i32.add
          i32.store offset=12
          local.get $l6
          local.get $l3
          i32.const 2
          i32.shl
          i32.add
          local.get $l2
          i32.store offset=16
          br $B7
        end
        local.get $p1
        local.get $l2
        local.get $l5
        i32.load offset=16
        i32.load offset=96
        i32.load offset=56
        call $f2908
      end
      local.get $p0
      local.get $p1
      call $f61071
      local.set $l2
      i32.const 3775972
      i32.load
      local.set $l5
      local.get $p1
      local.get $p1
      i32.load offset=16
      i32.const 1
      i32.add
      i32.store offset=16
      block $B9
        local.get $p1
        i32.load offset=12
        local.tee $l3
        local.get $p1
        i32.load offset=8
        local.tee $l6
        i32.load offset=12
        i32.lt_u
        if $I10
          local.get $p1
          local.get $l3
          i32.const 1
          i32.add
          i32.store offset=12
          local.get $l6
          local.get $l3
          i32.const 2
          i32.shl
          i32.add
          local.get $l2
          i32.store offset=16
          br $B9
        end
        local.get $p1
        local.get $l2
        local.get $l5
        i32.load offset=16
        i32.load offset=96
        i32.load offset=56
        call $f2908
      end
      i32.const 3748320
      i32.load
      i32.load offset=92
      local.get $p1
      i32.store offset=8
      local.get $p0
      i32.load offset=68
      local.set $p1
      i32.const 3753376
      i32.load
      local.tee $l2
      i32.load offset=116
      i32.eqz
      if $I11
        local.get $l2
        call $f65192
      end
      local.get $p1
      i32.const 0
      i32.const 0
      call $f54398
      if $I12
        local.get $p0
        i32.load offset=68
        i32.const 0
        i32.const 0
        call $f54405
      end
      i32.const 0
      local.set $l2
      local.get $p0
      i32.const 0
      i32.store8 offset=74
      local.get $p0
      i32.const 0
      i32.store16 offset=72
      local.get $p0
      i32.const 0
      i32.store8 offset=172
      local.get $p0
      block $B13 (result i32)
        i32.const 0
        i32.const 3847392
        i32.load
        i32.const 0
        call $f54315
        local.tee $l3
        i32.eqz
        br_if $B13
        drop
        i32.const 0
        i32.const 3756236
        i32.load
        local.tee $l6
        i32.load8_u offset=184
        local.tee $l7
        local.get $l3
        i32.load
        local.tee $l5
        i32.load8_u offset=184
        i32.gt_u
        br_if $B13
        drop
        local.get $l3
        i32.const 0
        local.get $l5
        i32.load offset=100
        local.get $l7
        i32.const 2
        i32.shl
        i32.add
        i32.const 4
        i32.sub
        i32.load
        local.get $l6
        i32.eq
        select
      end
      i32.store offset=52
      block $B14
        i32.const 3854740
        i32.load
        i32.const 0
        call $f54315
        local.tee $p1
        i32.eqz
        br_if $B14
        i32.const 3756236
        i32.load
        local.tee $l5
        i32.load8_u offset=184
        local.tee $l6
        local.get $p1
        i32.load
        local.tee $l3
        i32.load8_u offset=184
        i32.gt_u
        br_if $B14
        local.get $p1
        i32.const 0
        local.get $l3
        i32.load offset=100
        local.get $l6
        i32.const 2
        i32.shl
        i32.add
        i32.const 4
        i32.sub
        i32.load
        local.get $l5
        i32.eq
        select
        local.set $l2
      end
      local.get $p0
      local.get $l2
      i32.store offset=56
      i32.const 0
      local.set $p1
      local.get $p0
      i32.const 3847380
      i32.load
      i32.const 0
      call $f54315
      local.tee $l3
      if $I15 (result i32)
        local.get $l3
        i32.const 0
        local.get $l3
        i32.load
        i32.const 3756240
        i32.load
        i32.eq
        select
      else
        i32.const 0
      end
      i32.store offset=60
      local.get $p0
      i32.const 3854728
      i32.load
      i32.const 0
      call $f54315
      local.tee $l2
      if $I16 (result i32)
        local.get $l2
        i32.const 0
        local.get $l2
        i32.load
        i32.const 3756240
        i32.load
        i32.eq
        select
      else
        i32.const 0
      end
      i32.store offset=64
      local.get $p0
      i32.const 3838212
      i32.load
      i32.const 0
      call $f54416
      i32.store offset=240
      local.get $l4
      i32.const 16
      i32.add
      local.get $p0
      i32.load offset=212
      i32.const 0
      i32.const 3773132
      i32.load
      call $f2903
      i32.const 3792616
      i32.load
      call $f34548
      i32.const 0
      call $f54624
      local.get $p0
      local.get $l4
      i32.load offset=24
      i32.store offset=228
      local.get $p0
      local.get $l4
      i64.load offset=16
      i64.store offset=220 align=4
      local.get $l4
      local.get $p0
      i32.load offset=240
      i32.const 0
      call $f54401
      i32.const 0
      call $f54624
      local.get $p0
      local.get $l4
      i32.load offset=8
      i32.store offset=252
      local.get $p0
      local.get $l4
      i64.load
      i64.store offset=244 align=4
      local.get $p0
      i32.const 220
      i32.add
      local.set $l2
      loop $L17
        local.get $p0
        i32.load offset=212
        local.get $p1
        i32.const 3773132
        i32.load
        call $f2903
        i32.const 0
        i32.const 0
        call $f54405
        local.get $p0
        i32.load offset=216
        local.get $p1
        i32.const 3773132
        i32.load
        call $f2903
        i32.const 0
        i32.const 0
        call $f54405
        local.get $p0
        i32.load offset=212
        local.get $p1
        i32.const 3773132
        i32.load
        call $f2903
        i32.const 3792572
        i32.load
        call $f34548
        f32.const 0x1.4p+4 (;=20;)
        i32.const 0
        call $f32547
        local.get $p0
        i32.load offset=216
        local.get $p1
        i32.const 3773132
        i32.load
        call $f2903
        i32.const 3792572
        i32.load
        call $f34548
        f32.const 0x1.4p+4 (;=20;)
        i32.const 0
        call $f32547
        local.get $p1
        i32.const 1
        i32.add
        local.tee $p1
        i32.const 8
        i32.ne
        br_if $L17
      end
      local.get $l4
      local.get $l2
      i32.load offset=8
      i32.store offset=40
      local.get $l4
      local.get $l2
      i64.load align=4
      i64.store offset=32
      local.get $l4
      i32.const 32
      i32.add
      i32.const 0
      i32.const 0
      call $f54067
      local.set $p1
      i32.const 3854032
      i32.load
      local.get $p1
      i32.const 0
      call $f53732
      local.set $p1
      i32.const 3748808
      i32.load
      local.tee $l2
      i32.load offset=116
      i32.eqz
      if $I18
        local.get $l2
        call $f65192
      end
      local.get $p1
      i32.const 0
      call $f42976
      local.get $p0
      i32.load offset=36
      i32.const 3813572
      i32.load
      i32.const 0
      call $f53863
      if $I19
        i32.const 3843860
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792608
        i32.load
        call $f34548
        local.tee $p1
        local.get $p0
        i32.load offset=36
        i32.const 3817856
        i32.load
        i32.const 0
        call $f53732
        local.get $p1
        i32.load
        local.tee $p1
        i32.load offset=796
        local.get $p1
        i32.load offset=792
        call_indirect $__indirect_function_table (type $t2)
      end
      local.get $p0
      i32.load offset=40
      i32.const 3813572
      i32.load
      i32.const 0
      call $f53863
      if $I20
        i32.const 3843868
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792608
        i32.load
        call $f34548
        local.tee $p1
        local.get $p0
        i32.load offset=40
        i32.const 3817856
        i32.load
        i32.const 0
        call $f53732
        local.get $p1
        i32.load
        local.tee $p1
        i32.load offset=796
        local.get $p1
        i32.load offset=792
        call_indirect $__indirect_function_table (type $t2)
      end
      i32.const 3821460
      i32.load
      i32.const 0
      call $f54416
      i32.const 3792480
      i32.load
      call $f34548
      local.set $p1
      local.get $l4
      i32.const 5
      i32.store
      i32.const 3751540
      i32.load
      local.get $l4
      call $f1675
      local.set $l2
      local.get $p1
      i32.const 3837344
      i32.load
      local.get $l2
      i32.const 0
      call $f54371
      i32.const 3843884
      i32.load
      i32.const 0
      call $f54416
      i32.const 3792472
      i32.load
      call $f34548
      local.tee $p1
      i32.load offset=180
      local.set $l2
      i32.const 3756912
      i32.load
      call $f1446
      local.tee $l3
      local.get $p0
      i32.const 3787796
      i32.load
      i32.const 0
      call $f18179
      local.get $l2
      local.get $l3
      i32.const 0
      call $f18181
      local.get $p1
      i32.const 0
      i32.const 0
      call $f54337
      i32.const 3843888
      i32.load
      i32.const 0
      call $f54416
      i32.const 3792472
      i32.load
      call $f34548
      local.tee $p1
      i32.load offset=180
      local.set $l2
      i32.const 3756912
      i32.load
      call $f1446
      local.tee $l3
      local.get $p0
      i32.const 3787800
      i32.load
      i32.const 0
      call $f18179
      local.get $l2
      local.get $l3
      i32.const 0
      call $f18181
      local.get $p1
      i32.const 0
      i32.const 0
      call $f54337
      i32.const 3843880
      i32.load
      i32.const 0
      call $f54416
      i32.const 3792472
      i32.load
      call $f34548
      local.tee $p1
      i32.load offset=180
      local.set $l2
      i32.const 3756912
      i32.load
      call $f1446
      local.tee $l3
      local.get $p0
      i32.const 3787804
      i32.load
      i32.const 0
      call $f18179
      local.get $l2
      local.get $l3
      i32.const 0
      call $f18181
      local.get $p1
      i32.const 0
      i32.const 0
      call $f54337
      i32.const 3843876
      i32.load
      i32.const 0
      call $f54416
      i32.const 3792472
      i32.load
      call $f34548
      local.tee $p1
      i32.load offset=180
      local.set $l2
      i32.const 3756912
      i32.load
      call $f1446
      local.tee $l3
      local.get $p0
      i32.const 3787808
      i32.load
      i32.const 0
      call $f18179
      local.get $l2
      local.get $l3
      i32.const 0
      call $f18181
      local.get $p1
      i32.const 1
      i32.const 0
      call $f54337
      local.get $p0
      i32.const 3752336
      i32.load
      call $f1446
      i32.store offset=300
      local.get $p0
      i32.const 3821468
      i32.load
      i32.const 0
      call $f54416
      i32.store offset=184
      i32.const 3837032
      i32.load
      local.get $p0
      i32.load offset=36
      i32.const 0
      call $f53732
      local.set $p1
      i32.const 3748808
      i32.load
      local.tee $l2
      i32.load offset=116
      i32.eqz
      if $I21
        local.get $l2
        call $f65192
      end
      local.get $p1
      i32.const 0
      call $f42976
      local.get $p0
      i32.load offset=152
      i32.const 0
      i32.const 3773132
      i32.load
      call $f2903
      i32.const 3792608
      i32.load
      call $f34548
      local.tee $p1
      local.get $p0
      i32.load offset=36
      local.get $p1
      i32.load
      local.tee $p1
      i32.load offset=796
      local.get $p1
      i32.load offset=792
      call_indirect $__indirect_function_table (type $t2)
      local.get $p0
      i32.load offset=152
      i32.const 1
      i32.const 3773132
      i32.load
      call $f2903
      i32.const 3792608
      i32.load
      call $f34548
      local.tee $p1
      local.get $p0
      i32.load offset=40
      local.get $p1
      i32.load
      local.tee $p1
      i32.load offset=796
      local.get $p1
      i32.load offset=792
      call_indirect $__indirect_function_table (type $t2)
      local.get $l4
      i32.const 16
      i32.add
      local.get $p0
      i32.load offset=184
      i32.const 0
      call $f54401
      i32.const 0
      call $f54624
      local.get $p0
      local.get $l4
      i32.load offset=24
      i32.store offset=196
      local.get $p0
      local.get $l4
      i64.load offset=16
      i64.store offset=188 align=4
      local.get $p0
      i32.const 3745900
      i32.load
      i32.const 32
      call $f1052
      i32.store offset=124
      i32.const 3743328
      i32.load
      call $f1446
      local.tee $p1
      i32.const 3772036
      i32.load
      call $f2715
      local.get $p0
      local.get $p1
      i32.store offset=128
      i32.const 3755556
      i32.load
      call $f1446
      local.tee $p1
      i32.const 0
      call $f2167
      local.get $p0
      i32.const 0
      i32.store8 offset=136
      local.get $p0
      i32.const 0
      i32.store offset=132
      local.get $p0
      local.get $p1
      i32.store offset=140
      i32.const 3825504
      i32.load
      i32.const 0
      call $f42976
      local.get $l4
      i32.const 48
      i32.add
      global.set $g0
      return
    end
    local.get $l3
    local.get $l7
    call $f1678
    unreachable)
