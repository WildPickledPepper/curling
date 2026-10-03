  (func $f60188 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l3
    global.set $g0
    i32.const 4674511
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3748808
      call $f1661
      i32.const 3749616
      call $f1661
      i32.const 3792480
      call $f1661
      i32.const 3751540
      call $f1661
      i32.const 3772452
      call $f1661
      i32.const 3772456
      call $f1661
      i32.const 3753376
      call $f1661
      i32.const 3745900
      call $f1661
      i32.const 3832504
      call $f1661
      i32.const 3836244
      call $f1661
      i32.const 3821460
      call $f1661
      i32.const 3827208
      call $f1661
      i32.const 3822976
      call $f1661
      i32.const 3847980
      call $f1661
      i32.const 3837344
      call $f1661
      i32.const 3843852
      call $f1661
      i32.const 3836252
      call $f1661
      i32.const 4674511
      i32.const 1
      i32.store8
    end
    i32.const 4674496
    i32.load8_u
    i32.eqz
    if $I1
      i32.const 3749968
      call $f1661
      i32.const 4674496
      i32.const 1
      i32.store8
    end
    local.get $p0
    i32.load offset=160
    local.set $l2
    i32.const 3749968
    i32.load
    call $f1446
    local.tee $p1
    local.get $l2
    i32.const 0
    call $f61050
    local.get $p0
    local.get $p1
    i32.store offset=96
    local.get $p0
    local.get $p1
    i32.load offset=24
    i32.store offset=128
    local.get $l3
    i32.const 3749616
    i32.load
    local.tee $p1
    i32.load offset=116
    if $I2 (result i32)
      local.get $p1
    else
      local.get $p1
      call $f65192
      i32.const 3749616
      i32.load
    end
    i32.load offset=92
    i32.load offset=4
    i32.load offset=12
    i32.store offset=12
    local.get $l3
    i32.const 12
    i32.add
    i32.const 0
    call $f56590
    local.set $p1
    i32.const 3847980
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
    if $I3
      local.get $l2
      call $f65192
    end
    local.get $p1
    i32.const 0
    call $f42976
    local.get $p0
    i32.load offset=96
    i32.const 3749616
    i32.load
    i32.load offset=92
    i32.load offset=4
    i32.const 0
    i32.const 3772456
    i32.load
    call $f2903
    i32.store offset=44
    local.get $p0
    i32.load offset=96
    i32.const 3749616
    i32.load
    i32.load offset=92
    i32.load offset=4
    i32.const 1
    i32.const 3772456
    i32.load
    call $f2903
    i32.store offset=68
    local.get $p0
    i32.load offset=160
    local.set $l2
    local.get $p0
    i32.load offset=96
    local.tee $p1
    i32.const 0
    i32.store offset=108
    local.get $p1
    local.get $l2
    i32.store offset=16
    local.get $p1
    i64.const 4294967296000
    i64.store offset=48 align=4
    local.get $p1
    i64.const 4294967296000
    i64.store offset=72 align=4
    local.get $p1
    local.get $p0
    i32.load offset=28
    i32.store offset=56
    local.get $p0
    i32.load offset=32
    local.set $l2
    local.get $p1
    i32.const -64
    i32.sub
    i32.const 1
    i32.store
    local.get $p1
    i32.const 1
    i32.store offset=40
    local.get $p1
    local.get $l2
    i32.store offset=80
    local.get $p0
    i32.const 0
    i32.store8 offset=84
    local.get $p0
    i32.load offset=252
    local.set $l2
    local.get $l3
    i32.const 3749616
    i32.load
    local.tee $p1
    i32.load offset=116
    if $I4 (result i32)
      local.get $p1
    else
      local.get $p1
      call $f65192
      i32.const 3749616
      i32.load
    end
    i32.load offset=92
    i32.load offset=4
    i32.load offset=12
    i32.store offset=12
    local.get $l3
    i32.const 12
    i32.add
    i32.const 0
    call $f56590
    local.set $p1
    local.get $l2
    i32.const 3822976
    i32.load
    local.get $p1
    i32.const 0
    call $f53732
    i32.const 0
    call $f61055
    block $B5
      block $B6
        block $B7
          local.get $p0
          i32.load offset=96
          i32.load offset=28
          call $f1448
          local.tee $p1
          i32.eqz
          if $I8
            local.get $p0
            i32.const 0
            i32.store offset=100
            br $B7
          end
          local.get $p1
          i32.const 3745900
          i32.load
          local.tee $l4
          call $f1674
          local.tee $l2
          i32.eqz
          br_if $B6
          local.get $p0
          local.get $l2
          i32.store offset=100
          local.get $p1
          i32.const 3745900
          i32.load
          local.tee $l2
          call $f1674
          i32.eqz
          br_if $B5
        end
        local.get $p0
        i32.const 1
        i32.store8 offset=89
        i32.const 3821460
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792480
        i32.load
        call $f34548
        local.set $p1
        local.get $l3
        i32.const 1
        i32.store offset=8
        i32.const 3751540
        i32.load
        local.get $l3
        i32.const 8
        i32.add
        call $f1675
        local.set $l2
        local.get $p1
        i32.const 3837344
        i32.load
        local.get $l2
        i32.const 0
        call $f54371
        i32.const 3843852
        i32.load
        i32.const 0
        call $f54416
        local.set $p1
        i32.const 3753376
        i32.load
        local.tee $l2
        i32.load offset=116
        i32.eqz
        if $I9
          local.get $l2
          call $f65192
        end
        local.get $p1
        i32.const 0
        i32.const 0
        call $f54398
        if $I10
          i32.const 3843852
          i32.load
          i32.const 0
          call $f54416
          i32.const 0
          i32.const 0
          call $f54405
        end
        local.get $p0
        i32.const 1
        i32.store8 offset=132
        local.get $p0
        i32.load offset=52
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
          i32.load offset=52
          i32.const 1
          i32.const 0
          call $f54405
        end
        block $B13
          local.get $p0
          i32.load offset=96
          local.tee $p1
          i32.load offset=40
          i32.const 1
          i32.ne
          br_if $B13
          local.get $p1
          i32.const -64
          i32.sub
          i32.load
          i32.const 1
          i32.ne
          br_if $B13
          local.get $p1
          i32.load offset=44
          i32.const 3832504
          i32.load
          i32.const 0
          call $f61033
          local.get $p0
          i32.load offset=96
          i32.load offset=68
          i32.const 3832504
          i32.load
          i32.const 0
          call $f61033
          local.get $p0
          i32.load offset=252
          i32.const 3832504
          i32.load
          i32.const 0
          call $f61055
          local.get $p0
          local.get $p0
          call $f60177
          i32.const 3827208
          i32.load
          local.set $p1
          i32.const 500
          i32.const 0
          call $f52516
          local.get $p0
          i32.load offset=96
          local.tee $l2
          i32.const 68
          i32.const 44
          local.get $l2
          i32.load offset=24
          local.tee $l2
          select
          i32.add
          i32.load
          local.get $p1
          i32.const 0
          call $f61033
          local.get $p0
          i32.load offset=252
          i32.const 3836252
          i32.const 3836244
          local.get $l2
          select
          i32.load
          local.get $p1
          i32.const 0
          call $f53732
          i32.const 0
          call $f61055
          local.get $p0
          i32.const 1
          i32.store8 offset=90
          local.get $p0
          i32.const 0
          i32.store offset=92
        end
        f32.const 0x1p+5 (;=32;)
        i32.const 0
        call $f54557
        local.get $l3
        i32.const 16
        i32.add
        global.set $g0
        return
      end
      local.get $p1
      local.get $l4
      call $f1678
      unreachable
    end
    local.get $p1
    local.get $l2
    call $f1678
    unreachable)
