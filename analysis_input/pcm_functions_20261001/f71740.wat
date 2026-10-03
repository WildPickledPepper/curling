  (func $f71740 (type $t96) (param $p0 i32) (param $p1 i32) (param $p2 i64)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32)
    local.get $p0
    i64.const 4294967296
    i64.store offset=4 align=4
    local.get $p0
    i32.const 3175444
    i32.store
    local.get $p0
    i64.const 0
    i64.store offset=12 align=4
    local.get $p0
    i64.const 0
    i64.store offset=20 align=4
    local.get $p0
    i64.const 0
    i64.store offset=28 align=4
    local.get $p0
    i64.const 0
    i64.store offset=36 align=4
    local.get $p0
    i64.const 0
    i64.store offset=44 align=4
    local.get $p0
    i32.const 52
    i32.add
    local.tee $l4
    i32.const 3177800
    i32.store
    local.get $l4
    i32.const 4
    i32.add
    local.tee $l3
    i64.const 0
    i64.store offset=4 align=4
    local.get $l3
    i32.const 1
    i32.store
    local.get $l3
    i64.const 0
    i64.store offset=12 align=4
    local.get $l3
    i64.const 0
    i64.store offset=20 align=4
    local.get $l3
    i64.const 0
    i64.store offset=28 align=4
    local.get $l3
    i32.const 36
    i32.add
    local.tee $l6
    i32.const 0
    i32.store
    local.get $l3
    i64.const 0
    i64.store offset=48 align=4
    local.get $l3
    i64.const -3233808384
    i64.store offset=40 align=4
    local.get $l3
    i32.const 16
    i32.add
    local.tee $l8
    i32.const 64
    call $f71836
    local.get $l3
    i64.const 0
    i64.store offset=80 align=4
    local.get $l3
    i64.const 0
    i64.store offset=72 align=4
    local.get $l3
    i32.const -64
    i32.sub
    local.tee $l5
    i64.const 0
    i64.store align=4
    local.get $l3
    i64.const 0
    i64.store offset=56 align=4
    local.get $l3
    i64.const 0
    i64.store offset=96 align=4
    local.get $l3
    i64.const -3233808384
    i64.store offset=88 align=4
    local.get $l5
    i32.const 64
    call $f71836
    local.get $l3
    i32.const 0
    i32.store offset=116
    local.get $l3
    i64.const 0
    i64.store offset=108 align=4
    local.get $l3
    local.get $p0
    i32.const 284
    i32.add
    local.tee $l9
    local.tee $l5
    i32.store offset=104
    local.get $l6
    i32.load
    i32.const 255
    i32.le_u
    if $I0
      local.get $l8
      i32.const 256
      call $f71836
    end
    local.get $l3
    i32.load offset=84
    i32.const 255
    i32.le_u
    if $I1
      local.get $l3
      i32.const -64
      i32.sub
      i32.const 256
      call $f71836
    end
    local.get $l3
    i32.load offset=116
    i32.const 2147483616
    i32.and
    i32.eqz
    if $I2
      local.get $l3
      i32.const 108
      i32.add
      i32.const 32
      call $f71838
    end
    local.get $l4
    i64.const 0
    i64.store offset=128 align=4
    local.get $l4
    local.get $l5
    i32.store offset=124
    local.get $l4
    i64.const 0
    i64.store offset=136 align=4
    local.get $l4
    i64.const 0
    i64.store offset=144 align=4
    local.get $l4
    i64.const 0
    i64.store offset=160 align=4
    local.get $l4
    i64.const -3233808384
    i64.store offset=152 align=4
    local.get $l4
    i32.const 128
    i32.add
    local.tee $l6
    i32.const 64
    call $f71860
    local.get $l4
    i64.const 0
    i64.store offset=168 align=4
    local.get $l4
    i32.const 0
    i32.store8 offset=212
    local.get $l4
    i64.const 0
    i64.store offset=176 align=4
    local.get $l4
    i64.const 0
    i64.store offset=184 align=4
    local.get $l4
    i64.const 0
    i64.store offset=192 align=4
    local.get $l4
    i64.const 0
    i64.store offset=200 align=4
    local.get $l4
    i32.const 32
    i32.store offset=208
    local.get $l4
    call $f69753
    local.tee $l5
    i32.const 792
    i32.const 3178132
    i32.const 3177808
    i32.const 60
    local.get $l5
    i32.load
    i32.load offset=8
    call_indirect $__indirect_function_table (type $t9)
    i32.store offset=196
    local.get $l4
    i32.load offset=208
    local.tee $l5
    i32.const 3
    i32.shl
    local.tee $l3
    if $I3
      call $f69753
      local.tee $l5
      local.get $l3
      i32.const 3178132
      i32.const 3177808
      i32.const 61
      local.get $l5
      i32.load
      i32.load offset=8
      call_indirect $__indirect_function_table (type $t9)
      local.set $l7
      local.get $l4
      i32.load offset=208
      local.set $l5
    end
    local.get $l4
    local.get $l7
    i32.store offset=200
    local.get $l5
    local.get $l4
    i32.load offset=148
    i32.gt_u
    if $I4
      local.get $l6
      local.get $l5
      call $f71860
    end
    call $f69753
    local.tee $l5
    i32.const 64
    i32.const 3178780
    i32.const 3178240
    i32.const 4700888
    i32.load
    local.tee $l7
    local.get $l7
    i32.load
    i32.load offset=20
    call_indirect $__indirect_function_table (type $t5)
    select
    i32.const 3177808
    i32.const 65
    local.get $l5
    i32.load
    i32.load offset=8
    call_indirect $__indirect_function_table (type $t9)
    local.tee $l5
    call $f71774
    local.get $l4
    local.get $l5
    i32.store offset=168
    local.get $l4
    i32.load offset=208
    if $I5
      i32.const 0
      local.set $l5
      loop $L6
        local.get $l5
        i32.const 3
        i32.shl
        local.tee $l7
        local.get $l4
        i32.load offset=200
        i32.add
        i32.const 0
        i32.store offset=4
        call $f69753
        local.tee $l3
        i32.const 64
        i32.const 3178780
        i32.const 3178240
        i32.const 4700888
        i32.load
        local.tee $l6
        local.get $l6
        i32.load
        i32.load offset=20
        call_indirect $__indirect_function_table (type $t5)
        select
        i32.const 3177808
        i32.const 71
        local.get $l3
        i32.load
        i32.load offset=8
        call_indirect $__indirect_function_table (type $t9)
        local.tee $l3
        call $f71774
        local.get $l4
        i32.load offset=200
        local.get $l7
        i32.add
        local.get $l3
        i32.store
        local.get $l5
        i32.const 1
        i32.add
        local.tee $l5
        local.get $l4
        i32.load offset=208
        i32.lt_u
        br_if $L6
      end
    end
    local.get $p0
    i32.const 0
    i32.store offset=280
    local.get $p0
    i64.const 429496729600
    i64.store offset=268 align=4
    local.get $l9
    call $f71882
    drop
    local.get $p0
    i64.const 0
    i64.store offset=328 align=4
    local.get $p0
    i64.const 0
    i64.store offset=320 align=4
    local.get $p0
    i64.const 0
    i64.store offset=312 align=4
    local.get $p0
    i64.const 0
    i64.store offset=340 align=4
    local.get $p0
    i32.const 0
    i32.store16 offset=337 align=1
    local.get $p0
    local.get $p1
    i32.store8 offset=336
    local.get $p0
    i64.const 0
    i64.store offset=348 align=4
    local.get $p0
    i64.const 0
    i64.store offset=356 align=4
    local.get $p0
    local.get $p2
    i64.store offset=368)