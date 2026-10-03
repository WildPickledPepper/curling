  (func $f72951 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i64)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l6
    global.set $g0
    i32.const 9
    call $f80140
    call $f73714
    local.get $p0
    i32.load offset=40
    if $I0
      local.get $p0
      local.get $p0
      i32.load
      i32.load offset=152
      call_indirect $__indirect_function_table (type $t7)
    end
    local.get $p0
    local.get $p0
    i32.load offset=84
    local.tee $l2
    i32.store offset=88
    local.get $p0
    local.get $p0
    i32.load offset=144
    i32.store offset=148
    block $B1
      local.get $l2
      i32.eqz
      br_if $B1
      local.get $l6
      local.get $l2
      i32.store offset=12
      block $B2
        block $B3
          i32.const 4782060
          i32.load
          local.tee $l2
          i32.eqz
          br_if $B3
          local.get $l6
          local.get $l2
          local.get $l6
          i32.const 12
          i32.add
          call $f66830
          local.get $l6
          i32.load
          local.tee $l3
          i32.const 4782060
          i32.load
          local.tee $l2
          i32.load
          local.get $l2
          i32.load offset=4
          i32.const 3
          i32.mul
          i32.add
          i32.const 12
          i32.add
          i32.eq
          br_if $B3
          local.get $l3
          i32.load offset=8
          br_if $B2
        end
        local.get $p0
        i32.load offset=84
        call $f80110
        i32.eqz
        br_if $B1
      end
      block $B4
        local.get $p0
        i32.load offset=84
        local.tee $l2
        i32.eqz
        if $I5
          i32.const 0
          local.set $l3
          br $B4
        end
        local.get $l6
        local.get $l2
        i32.store offset=12
        block $B6
          i32.const 4782060
          i32.load
          local.tee $l2
          i32.eqz
          br_if $B6
          local.get $l6
          local.get $l2
          local.get $l6
          i32.const 12
          i32.add
          call $f66830
          local.get $l6
          i32.load
          local.tee $l3
          i32.const 4782060
          i32.load
          local.tee $l2
          i32.load
          local.get $l2
          i32.load offset=4
          i32.const 3
          i32.mul
          i32.add
          i32.const 12
          i32.add
          i32.eq
          br_if $B6
          local.get $l3
          i32.load offset=8
          local.tee $l3
          br_if $B4
        end
        local.get $p0
        i32.load offset=84
        call $f80110
        local.set $l3
      end
      local.get $p0
      i32.const 92
      i32.add
      local.tee $l2
      local.get $l3
      i32.const 204
      i32.add
      local.tee $l3
      i32.eq
      br_if $B1
      local.get $l2
      i32.load
      local.tee $l4
      if $I7
        local.get $l4
        local.get $p0
        i32.const 96
        i32.add
        local.tee $l5
        i32.load
        i32.store offset=4
        local.get $l5
        i32.load
        local.get $p0
        i32.load offset=92
        i32.store
        local.get $p0
        i64.const 0
        i64.store offset=92 align=4
      end
      local.get $l3
      i32.load
      local.set $l4
      local.get $p0
      i32.const 96
      i32.add
      local.tee $l5
      local.get $l3
      i32.store
      local.get $p0
      local.get $l4
      i32.store offset=92
      local.get $l4
      local.get $l2
      i32.store offset=4
      local.get $l5
      i32.load
      local.get $l2
      i32.store
    end
    local.get $p0
    local.get $l6
    local.get $l6
    i32.const 12
    i32.add
    call $f72950
    local.tee $l2
    if $I8
      local.get $p0
      local.get $l6
      i32.load8_u offset=12
      i32.store8 offset=81
      local.get $p1
      local.set $l3
      local.get $l6
      local.set $p1
      global.get $g0
      i32.const 48
      i32.sub
      local.tee $l4
      global.set $g0
      block $B9
        local.get $l2
        i32.eqz
        br_if $B9
        i32.const 9
        call $f80140
        call $f73714
        local.get $p0
        i32.load offset=116
        local.tee $l5
        if $I10
          local.get $l5
          local.get $p0
          i32.const 120
          i32.add
          local.tee $l8
          i32.load
          i32.store offset=4
          local.get $l8
          i32.load
          local.get $p0
          i32.load offset=116
          i32.store
          local.get $p0
          i64.const 0
          i64.store offset=116 align=4
        end
        local.get $p0
        i32.load8_u offset=80
        if $I11
          local.get $l4
          i64.const 4575657221408423936
          i64.store offset=32
          local.get $l4
          i64.const 0
          i64.store offset=24
          local.get $l4
          i32.const 0
          i32.store8 offset=47
          local.get $l4
          i32.const 0
          i32.store16 offset=45 align=1
          local.get $l4
          i32.const 1
          i32.store8 offset=44
          local.get $l4
          i32.const 4
          i32.store offset=8
          local.get $l4
          local.get $l2
          i32.store offset=40
          local.get $p1
          i64.load align=4
          local.set $l11
          local.get $l4
          local.get $p1
          f32.load offset=8
          f32.store offset=20
          local.get $l4
          local.get $l11
          i64.store offset=12 align=4
          local.get $p0
          local.get $l4
          i32.const 8
          i32.add
          local.get $l3
          call $f73283
          br $B9
        end
        local.get $p0
        i32.const 116
        i32.add
        local.set $l5
        block $B12
          local.get $p0
          local.get $l3
          call $f73284
          local.tee $l8
          i32.eqz
          br_if $B12
          local.get $p0
          i32.const 104
          i32.add
          local.tee $l7
          local.get $l8
          i32.const 44
          i32.add
          local.tee $l10
          i32.ne
          if $I13
            local.get $l7
            i32.load
            local.tee $l9
            if $I14
              local.get $l9
              local.get $l7
              i32.load offset=4
              i32.store offset=4
              local.get $l7
              i32.load offset=4
              local.get $l7
              i32.load
              i32.store
              local.get $l7
              i64.const 0
              i64.store align=4
            end
            local.get $l10
            i32.load
            local.set $l9
            local.get $l7
            local.get $l10
            i32.store offset=4
            local.get $l7
            local.get $l9
            i32.store
            local.get $l9
            local.get $l7
            i32.store offset=4
            local.get $l7
            i32.load offset=4
            local.get $l7
            i32.store
          end
          local.get $l8
          i32.load8_u offset=133
          br_if $B12
          local.get $p0
          i32.const 0
          i32.store8 offset=136
          local.get $p0
          local.get $p0
          i32.store offset=132
          local.get $p0
          i32.const 239377
          i32.store offset=128
          local.get $l5
          i32.const 9
          call $f80140
          i32.const 76
          i32.add
          local.tee $l2
          i32.eq
          br_if $B9
          local.get $l5
          i32.load
          local.tee $p1
          if $I15
            local.get $p1
            local.get $p0
            i32.const 120
            i32.add
            local.tee $l3
            i32.load
            i32.store offset=4
            local.get $l3
            i32.load
            local.get $p0
            i32.load offset=116
            i32.store
            local.get $p0
            i64.const 0
            i64.store offset=116 align=4
          end
          local.get $l2
          i32.load
          local.set $p1
          local.get $p0
          i32.const 120
          i32.add
          local.tee $l3
          local.get $l2
          i32.store
          local.get $p0
          local.get $p1
          i32.store offset=116
          local.get $p1
          local.get $l5
          i32.store offset=4
          local.get $l3
          i32.load
          local.get $l5
          i32.store
          br $B9
        end
        local.get $p0
        local.get $l3
        call $f73285
        if $I16
          local.get $p0
          i32.const 0
          i32.store8 offset=136
          local.get $p0
          local.get $p0
          i32.store offset=132
          local.get $p0
          i32.const 239576
          i32.store offset=128
          local.get $l5
          i32.const 9
          call $f80140
          i32.const 76
          i32.add
          local.tee $l2
          i32.eq
          br_if $B9
          local.get $l5
          i32.load
          local.tee $p1
          if $I17
            local.get $p1
            local.get $p0
            i32.const 120
            i32.add
            local.tee $l3
            i32.load
            i32.store offset=4
            local.get $l3
            i32.load
            local.get $p0
            i32.load offset=116
            i32.store
            local.get $p0
            i64.const 0
            i64.store offset=116 align=4
          end
          local.get $l2
          i32.load
          local.set $p1
          local.get $p0
          i32.const 120
          i32.add
          local.tee $l3
          local.get $l2
          i32.store
          local.get $p0
          local.get $p1
          i32.store offset=116
          local.get $p1
          local.get $l5
          i32.store offset=4
          local.get $l3
          i32.load
          local.get $l5
          i32.store
          br $B9
        end
        local.get $p0
        i32.load8_u offset=60
        if $I18
          local.get $p0
          i32.const 0
          i32.store8 offset=136
          local.get $p0
          local.get $p0
          i32.store offset=132
          local.get $p0
          i32.const 237613
          i32.store offset=128
          local.get $l5
          i32.const 9
          call $f80140
          i32.const 76
          i32.add
          local.tee $l2
          i32.eq
          br_if $B9
          local.get $l5
          i32.load
          local.tee $p1
          if $I19
            local.get $p1
            local.get $p0
            i32.const 120
            i32.add
            local.tee $l3
            i32.load
            i32.store offset=4
            local.get $l3
            i32.load
            local.get $p0
            i32.load offset=116
            i32.store
            local.get $p0
            i64.const 0
            i64.store offset=116 align=4
          end
          local.get $l2
          i32.load
          local.set $p1
          local.get $p0
          i32.const 120
          i32.add
          local.tee $l3
          local.get $l2
          i32.store
          local.get $p0
          local.get $p1
          i32.store offset=116
          local.get $p1
          local.get $l5
          i32.store offset=4
          local.get $l3
          i32.load
          local.get $l5
          i32.store
          br $B9
        end
        local.get $l4
        i64.const 4575657221408423936
        i64.store offset=32
        local.get $l4
        i64.const 0
        i64.store offset=24
        local.get $l4
        i64.const 0
        i64.store offset=40
        local.get $l4
        i32.const 5
        i32.store offset=8
        local.get $l4
        local.get $l2
        i32.store offset=44
        local.get $p1
        i64.load align=4
        local.set $l11
        local.get $l4
        local.get $p1
        f32.load offset=8
        f32.store offset=20
        local.get $l4
        local.get $l11
        i64.store offset=12 align=4
        local.get $p0
        local.get $l4
        i32.const 8
        i32.add
        local.get $l3
        call $f73283
      end
      local.get $l4
      i32.const 48
      i32.add
      global.set $g0
      local.get $p0
      i32.const 0
      i32.store8 offset=140
    end
    local.get $l6
    i32.const 16
    i32.add
    global.set $g0)