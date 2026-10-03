  (func $f72778 (type $t17) (param $p0 i32) (param $p1 f32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 f32) (local $l7 f32) (local $l8 f32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l4
    global.set $g0
    local.get $l4
    local.get $p1
    f32.store offset=12
    local.get $l4
    i32.const 12
    i32.add
    local.set $l5
    f32.const 0x0p+0 (;=0;)
    local.set $p1
    global.get $g0
    i32.const 128
    i32.sub
    local.tee $l3
    global.set $g0
    local.get $l3
    i32.const 1065353216
    i32.store offset=124
    local.get $l3
    i32.const 1065353216
    i32.store offset=120
    local.get $l3
    i64.const 4575657222473777152
    i64.store offset=112
    local.get $l3
    i64.const 4575657221408423936
    i64.store offset=104
    local.get $l3
    i64.const 0
    i64.store offset=96
    local.get $p2
    if $I0 (result f32)
      local.get $p2
      f32.load offset=8
      local.set $p1
      local.get $p2
      f32.load offset=4
      local.set $l6
      local.get $p2
      f32.load
    else
      f32.const 0x0p+0 (;=0;)
    end
    local.set $l7
    local.get $l3
    local.get $p1
    f32.store offset=88
    local.get $l3
    local.get $l6
    f32.store offset=84
    local.get $l3
    local.get $l7
    f32.store offset=80
    block $B1
      local.get $l5
      if $I2
        local.get $l3
        i32.const 0
        i32.store offset=72
        local.get $l3
        i32.const -64
        i32.sub
        i64.const 0
        i64.store
        local.get $l3
        i64.const 0
        i64.store offset=56
        local.get $l3
        i64.const 0
        i64.store offset=48
        local.get $l3
        i64.const 0
        i64.store offset=40
        local.get $l3
        i64.const 0
        i64.store offset=32
        local.get $l3
        i64.const 0
        i64.store offset=24
        block $B3
          local.get $p0
          i32.const 0
          local.get $l5
          local.get $l3
          i32.const 24
          i32.add
          call $f72776
          if $I4
            local.get $l3
            f32.load offset=72
            f32.const 0x0p+0 (;=0;)
            f32.ne
            if $I5
              local.get $l3
              i32.const 24
              i32.add
              local.get $l3
              i32.const 112
              i32.add
              local.get $l3
              i32.const 96
              i32.add
              local.get $l3
              i32.const 124
              i32.add
              local.get $l3
              i32.const 80
              i32.add
              local.get $p2
              i32.const 0
              i32.ne
              local.get $p0
              i32.const 3210678
              call $f72777
            end
            local.get $l3
            local.get $l5
            f32.load
            local.tee $l8
            f32.store offset=124
            br $B3
          end
          i32.const 4700888
          i32.load
          local.set $p2
          local.get $l3
          i32.const 3210678
          i32.store
          local.get $p2
          i32.const 4
          i32.const 3210117
          i32.const 342
          i32.const 3210172
          local.get $l3
          call $f69760
          f32.const 0x1p+0 (;=1;)
          local.set $l8
        end
        local.get $l3
        f32.load offset=88
        local.set $p1
        local.get $l3
        f32.load offset=84
        local.set $l6
        local.get $l3
        f32.load offset=80
        local.set $l7
        br $B1
      end
      i32.const 4700888
      i32.load
      local.set $p2
      local.get $l3
      i32.const 3210678
      i32.store offset=16
      local.get $p2
      i32.const 4
      i32.const 3210117
      i32.const 350
      i32.const 3210718
      local.get $l3
      i32.const 16
      i32.add
      call $f69760
      f32.const 0x1p+0 (;=1;)
      local.set $l8
    end
    local.get $p0
    local.get $l8
    local.get $p0
    i32.load
    i32.load offset=116
    call_indirect $__indirect_function_table (type $t21)
    local.get $p0
    local.get $l3
    i32.const 112
    i32.add
    local.get $p0
    i32.load
    i32.load offset=128
    call_indirect $__indirect_function_table (type $t1)
    local.get $l3
    local.get $p1
    f32.store offset=48
    local.get $l3
    local.get $l6
    f32.store offset=44
    local.get $l3
    local.get $l3
    i64.load offset=96
    i64.store offset=24
    local.get $l3
    local.get $l7
    f32.store offset=40
    local.get $l3
    local.get $l3
    i64.load offset=104
    i64.store offset=32
    local.get $p0
    local.get $l3
    i32.const 24
    i32.add
    local.get $p0
    i32.load
    i32.load offset=108
    call_indirect $__indirect_function_table (type $t1)
    local.get $l3
    i32.const 128
    i32.add
    global.set $g0
    local.get $l4
    i32.const 16
    i32.add
    global.set $g0)