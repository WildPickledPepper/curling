  (func $f61071 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32)
    i32.const 4675134
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3746684
      call $f1661
      i32.const 3748808
      call $f1661
      i32.const 3808548
      call $f1661
      i32.const 3808552
      call $f1661
      i32.const 3808560
      call $f1661
      i32.const 3808564
      call $f1661
      i32.const 3759352
      call $f1661
      i32.const 3759348
      call $f1661
      i32.const 3757032
      call $f1661
      i32.const 3757504
      call $f1661
      i32.const 3757516
      call $f1661
      i32.const 3757528
      call $f1661
      i32.const 3757548
      call $f1661
      i32.const 3757556
      call $f1661
      i32.const 3825580
      call $f1661
      i32.const 3816840
      call $f1661
      i32.const 3816844
      call $f1661
      i32.const 3858144
      call $f1661
      i32.const 3837028
      call $f1661
      i32.const 4675134
      i32.const 1
      i32.store8
    end
    i32.const 3759352
    i32.load
    call $f1446
    local.tee $l3
    local.get $p0
    i32.store offset=12
    i32.const 3748808
    i32.load
    local.tee $p1
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $p1
      call $f65192
    end
    i32.const 3837028
    i32.load
    i32.const 0
    call $f42976
    i32.const 3746684
    i32.load
    local.tee $p1
    i32.load offset=116
    i32.eqz
    if $I2
      local.get $p1
      call $f65192
    end
    i32.const 0
    call $f42881
    local.set $l2
    i32.const 3757032
    i32.load
    call $f1446
    local.tee $p1
    local.get $l2
    i32.const 0
    call $f5874
    local.get $p1
    i32.const 0
    call $f5909
    local.set $l2
    local.get $p1
    i32.const 0
    call $f5921
    local.set $l4
    i32.const 3858144
    i32.load
    local.get $l2
    i32.const 3816840
    i32.load
    local.get $l4
    i32.const 0
    call $f53874
    local.set $l2
    local.get $p0
    i32.load8_u offset=180
    if $I3
      local.get $p1
      i32.const 0
      call $f5909
      local.set $l2
      local.get $p1
      i32.const 0
      call $f5921
      local.set $p1
      i32.const 3858144
      i32.load
      local.get $l2
      i32.const 3816844
      i32.load
      local.get $p1
      i32.const 0
      call $f53874
      local.set $l2
    end
    i32.const 3825580
    i32.load
    local.get $l2
    i32.const 0
    call $f53732
    local.set $p1
    i32.const 3748808
    i32.load
    local.tee $p0
    i32.load offset=116
    i32.eqz
    if $I4
      local.get $p0
      call $f65192
    end
    local.get $p1
    i32.const 0
    call $f42976
    i32.const 3757528
    i32.load
    local.tee $p1
    i32.load offset=116
    i32.eqz
    if $I5
      local.get $p1
      call $f65192
    end
    local.get $l3
    local.get $l2
    i32.const 0
    call $f59758
    local.tee $p1
    i32.store offset=8
    i32.const 3757556
    i32.load
    call $f1446
    local.tee $l2
    local.get $l3
    i32.const 3808560
    i32.load
    i32.const 0
    call $f59707
    local.get $p1
    local.get $l2
    i32.const 0
    call $f59722
    local.get $l3
    i32.load offset=8
    local.set $p1
    i32.const 3757548
    i32.load
    call $f1446
    local.tee $l2
    local.get $l3
    i32.const 3808564
    i32.load
    i32.const 0
    call $f59709
    local.get $p1
    local.get $l2
    i32.const 0
    call $f59724
    local.get $l3
    i32.load offset=8
    local.set $p0
    i32.const 3759348
    i32.load
    local.tee $p1
    i32.load offset=116
    i32.eqz
    if $I6
      local.get $p1
      call $f65192
      i32.const 3759348
      i32.load
      local.set $p1
    end
    local.get $p1
    i32.load offset=92
    i32.load offset=4
    local.tee $l2
    i32.eqz
    if $I7
      local.get $p1
      i32.load offset=116
      if $I8 (result i32)
        local.get $p1
      else
        local.get $p1
        call $f65192
        i32.const 3759348
        i32.load
      end
      i32.load offset=92
      i32.load
      local.set $p1
      i32.const 3757516
      i32.load
      call $f1446
      local.tee $l2
      local.get $p1
      i32.const 3808548
      i32.load
      i32.const 0
      call $f59710
      i32.const 3759348
      i32.load
      i32.load offset=92
      local.get $l2
      i32.store offset=4
    end
    local.get $p0
    local.get $l2
    i32.const 0
    call $f59726
    local.get $l3
    i32.load offset=8
    local.set $p0
    i32.const 3759348
    i32.load
    local.tee $p1
    i32.load offset=116
    i32.eqz
    if $I9
      local.get $p1
      call $f65192
      i32.const 3759348
      i32.load
      local.set $p1
    end
    local.get $p1
    i32.load offset=92
    i32.load offset=8
    local.tee $l2
    i32.eqz
    if $I10
      local.get $p1
      i32.load offset=116
      if $I11 (result i32)
        local.get $p1
      else
        local.get $p1
        call $f65192
        i32.const 3759348
        i32.load
      end
      i32.load offset=92
      i32.load
      local.set $p1
      i32.const 3757504
      i32.load
      call $f1446
      local.tee $l2
      local.get $p1
      i32.const 3808552
      i32.load
      i32.const 0
      call $f59711
      i32.const 3759348
      i32.load
      i32.load offset=92
      local.get $l2
      i32.store offset=8
    end
    local.get $p0
    local.get $l2
    i32.const 0
    call $f59728
    local.get $l3
    i32.load offset=8
    i32.const 0
    call $f59732
    local.get $l3
    i32.load offset=8)
