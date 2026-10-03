  (func $f71315 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 f32) (local $l7 f32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32)
    local.get $p0
    i32.load offset=48
    local.tee $l1
    f32.load offset=56
    local.set $l6
    local.get $l1
    f32.load offset=60
    local.set $l7
    local.get $l1
    f32.load offset=52
    local.set $l8
    local.get $l1
    f32.load offset=88
    local.set $l9
    local.get $l1
    f32.load offset=84
    local.set $l10
    local.get $l1
    f32.load offset=100
    local.set $l11
    local.get $l1
    i32.load offset=368
    call $f69738
    local.tee $l4
    i32.eqz
    if $I0
      call $f69753
      local.tee $l2
      i32.const 12195
      i32.const 3154657
      i32.const 3154312
      i32.const 4700888
      i32.load
      local.tee $l3
      local.get $l3
      i32.load
      i32.load offset=20
      call_indirect $__indirect_function_table (type $t5)
      select
      i32.const 3154589
      i32.const 82
      local.get $l2
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
      local.tee $l3
      i32.const 19
      i32.add
      i32.const -16
      i32.and
      local.tee $l2
      i32.const 4
      i32.sub
      local.get $l2
      local.get $l3
      i32.sub
      i32.store
      local.get $l2
      local.get $l1
      i32.load offset=372
      call $f71150
      local.set $l4
    end
    local.get $l4
    i32.const 11856
    i32.add
    i64.const 0
    i64.store align=4
    local.get $p0
    i32.load offset=32
    if $I1
      local.get $l7
      local.get $l6
      local.get $l6
      local.get $l7
      f32.gt
      select
      local.set $l6
      i32.const 0
      local.set $l1
      loop $L2
        local.get $p0
        i32.load offset=28
        local.get $l1
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l3
        local.get $p0
        i32.load offset=56
        local.tee $l2
        f32.load offset=92
        local.get $l8
        local.get $l2
        f32.load offset=96
        local.get $l6
        local.get $p0
        i32.load offset=52
        local.get $l4
        local.get $l11
        local.get $l10
        local.get $l9
        local.get $p0
        i32.load offset=36
        local.get $p0
        i32.load offset=40
        local.get $p0
        i32.load offset=44
        i32.const 11836
        i32.add
        local.get $p0
        i32.load offset=48
        local.tee $l5
        i32.load offset=168
        local.get $l2
        i32.load offset=80
        local.get $l5
        f32.load offset=612
        local.get $l3
        i32.load
        i32.load offset=152
        call_indirect $__indirect_function_table (type $t318)
        local.get $l1
        i32.const 1
        i32.add
        local.tee $l1
        local.get $p0
        i32.load offset=32
        i32.lt_u
        br_if $L2
      end
    end
    local.get $p0
    i32.load offset=48
    i32.load offset=368
    local.get $l4
    call $f69737)