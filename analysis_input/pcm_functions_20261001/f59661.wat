  (func $f59661 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i64) (local $l6 f32)
    global.get $g0
    i32.const 96
    i32.sub
    local.tee $p1
    global.set $g0
    i32.const 4674181
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3786760
      call $f1661
      i32.const 3775548
      call $f1661
      i32.const 3753376
      call $f1661
      i32.const 3757392
      call $f1661
      i32.const 3835520
      call $f1661
      i32.const 4674181
      i32.const 1
      i32.store8
    end
    block $B1
      block $B2
        block $B3
          local.get $p0
          i32.load offset=8
          br_table $B3 $B2 $B1
        end
        local.get $p0
        i32.const -1
        i32.store offset=8
        local.get $p0
        f32.load offset=16
        local.set $l6
        i32.const 3757392
        i32.load
        call $f1446
        local.tee $l2
        local.get $l6
        i32.const 0
        call $f3188
        i32.const 1
        local.set $l4
        local.get $p0
        i32.const 1
        i32.store offset=8
        local.get $p0
        local.get $l2
        i32.store offset=12
        br $B1
      end
      local.get $p0
      i32.load offset=20
      local.set $l2
      local.get $p0
      i32.const -1
      i32.store offset=8
      local.get $l2
      i32.const 3786760
      i32.load
      call $f59519
      local.tee $l4
      i32.load offset=12
      i32.const 0
      i32.gt_s
      if $I4
        i32.const 0
        local.set $p0
        loop $L5
          local.get $l2
          i32.load offset=44
          local.get $l4
          local.get $p0
          i32.const 2
          i32.shl
          i32.add
          i32.load offset=16
          local.tee $l3
          i32.const 3775548
          i32.load
          call $f55128
          i32.eqz
          if $I6
            local.get $l3
            i32.const 0
            i32.const 0
            call $f54645
          end
          local.get $p0
          i32.const 1
          i32.add
          local.tee $p0
          local.get $l4
          i32.load offset=12
          i32.lt_s
          br_if $L5
        end
      end
      local.get $l2
      i32.const 0
      call $f54360
      local.set $p0
      local.get $p1
      local.get $l2
      i32.load offset=24
      i32.store offset=56
      local.get $p1
      local.get $l2
      i64.load offset=16 align=4
      i64.store offset=48
      local.get $p0
      local.get $p1
      i32.const 48
      i32.add
      i32.const 0
      call $f54626
      local.get $l2
      i32.const 0
      call $f54360
      local.set $p0
      local.get $p1
      local.get $l2
      i64.load offset=36 align=4
      i64.store offset=40
      local.get $p1
      local.get $l2
      i64.load offset=28 align=4
      i64.store offset=32
      local.get $p0
      local.get $p1
      i32.const 32
      i32.add
      i32.const 0
      call $f54633
      local.get $l2
      i32.load offset=48
      local.set $p0
      i32.const 3753376
      i32.load
      local.tee $l4
      i32.load offset=116
      i32.eqz
      if $I7
        local.get $l4
        call $f65192
      end
      i32.const 0
      local.set $l4
      local.get $p0
      i32.const 0
      call $f54484
      if $I8
        local.get $l2
        i32.load offset=48
        local.set $p0
        i32.const 4674229
        i32.load8_u
        i32.eqz
        if $I9
          i32.const 3757216
          call $f1661
          i32.const 4674229
          i32.const 1
          i32.store8
        end
        i32.const 3757216
        i32.load
        i32.load offset=92
        local.tee $l3
        i64.load align=4
        local.set $l5
        local.get $p1
        local.get $l3
        i32.load offset=8
        local.tee $l3
        i32.store offset=24
        local.get $p1
        local.get $l3
        i32.store offset=88
        local.get $p1
        local.get $l5
        i64.store offset=80
        local.get $p1
        local.get $l5
        i64.store offset=16
        local.get $p0
        local.get $p1
        i32.const 16
        i32.add
        i32.const 0
        call $f32521
        local.get $l2
        i32.load offset=48
        local.set $p0
        i32.const 4674229
        i32.load8_u
        i32.eqz
        if $I10
          i32.const 3757216
          call $f1661
          i32.const 4674229
          i32.const 1
          i32.store8
        end
        i32.const 3757216
        i32.load
        i32.load offset=92
        local.tee $l3
        i64.load align=4
        local.set $l5
        local.get $p1
        local.get $l3
        i32.load offset=8
        local.tee $l3
        i32.store offset=8
        local.get $p1
        local.get $l3
        i32.store offset=72
        local.get $p1
        local.get $l5
        i64.store offset=64
        local.get $p1
        local.get $l5
        i64.store
        local.get $p0
        local.get $p1
        i32.const 0
        call $f32524
      end
      local.get $l2
      i32.const 3835520
      i32.load
      i32.const 0
      call $f54373
    end
    local.get $p1
    i32.const 96
    i32.add
    global.set $g0
    local.get $l4)