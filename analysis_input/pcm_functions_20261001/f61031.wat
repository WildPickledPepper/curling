  (func $f61031 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l3
    global.set $g0
    i32.const 4675108
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3792468
      call $f1661
      i32.const 3792508
      call $f1661
      i32.const 3792504
      call $f1661
      i32.const 3792520
      call $f1661
      i32.const 3754772
      call $f1661
      i32.const 3824116
      call $f1661
      i32.const 3828104
      call $f1661
      i32.const 3820532
      call $f1661
      i32.const 3826608
      call $f1661
      i32.const 3826604
      call $f1661
      i32.const 3827988
      call $f1661
      i32.const 3824108
      call $f1661
      i32.const 3832148
      call $f1661
      i32.const 3820528
      call $f1661
      i32.const 4675108
      i32.const 1
      i32.store8
    end
    local.get $l3
    i32.const 0
    i32.store offset=8
    block $B1
      local.get $p1
      i32.const 0
      call $f54361
      i32.const 0
      call $f54485
      i32.const 3832148
      i32.load
      i32.const 0
      call $f53861
      i32.eqz
      br_if $B1
      local.get $p0
      i32.const 1
      i32.store8 offset=17
      i32.const 3754772
      i32.load
      local.tee $p2
      i32.load offset=116
      i32.eqz
      if $I2
        local.get $p2
        call $f65192
      end
      local.get $l3
      i32.const 0
      call $f18204
      i32.store offset=8
      local.get $l3
      i32.const 8
      i32.add
      i32.const 0
      call $f18194
      i32.const 3826608
      i32.load
      i32.const 0
      call $f53861
      if $I3
        i32.const 3826604
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792520
        i32.load
        call $f34548
        i32.load8_u offset=84
        br_if $B1
        i32.const 3826604
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792520
        i32.load
        call $f34548
        i32.const 0
        call $f60196
        br $B1
      end
      i32.const 3754772
      i32.load
      local.tee $p2
      i32.load offset=116
      i32.eqz
      if $I4
        local.get $p2
        call $f65192
      end
      local.get $l3
      i32.const 0
      call $f18204
      i32.store offset=8
      local.get $l3
      i32.const 8
      i32.add
      i32.const 0
      call $f18194
      i32.const 3820532
      i32.load
      i32.const 0
      call $f53861
      if $I5
        i32.const 3820528
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792468
        i32.load
        call $f34548
        i32.load8_u offset=84
        local.set $p2
        i32.const 3820528
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792468
        i32.load
        call $f34548
        local.set $l4
        local.get $p2
        if $I6
          local.get $l4
          i32.const 0
          call $f60869
          br $B1
        end
        local.get $l4
        i32.const 0
        call $f60903
        br $B1
      end
      i32.const 3754772
      i32.load
      local.tee $p2
      i32.load offset=116
      i32.eqz
      if $I7
        local.get $p2
        call $f65192
      end
      local.get $l3
      i32.const 0
      call $f18204
      i32.store offset=8
      local.get $l3
      i32.const 8
      i32.add
      i32.const 0
      call $f18194
      i32.const 3828104
      i32.load
      i32.const 0
      call $f53861
      if $I8
        i32.const 3824116
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792508
        i32.load
        call $f34548
        i32.load8_u offset=112
        local.set $p2
        i32.const 3824116
        i32.load
        i32.const 0
        call $f54416
        i32.const 3792508
        i32.load
        call $f34548
        local.set $l4
        local.get $p2
        br_if $B1
        local.get $l4
        i32.const 0
        call $f60096
        br $B1
      end
      i32.const 3824108
      i32.load
      i32.const 0
      call $f54416
      i32.const 3792504
      i32.load
      call $f34548
      i32.load8_u offset=100
      local.set $p2
      i32.const 3824108
      i32.load
      i32.const 0
      call $f54416
      i32.const 3792504
      i32.load
      call $f34548
      local.set $l4
      local.get $p2
      br_if $B1
      local.get $l4
      local.get $l3
      call $f61032
    end
    local.get $p1
    i32.const 0
    call $f54361
    i32.const 0
    call $f54485
    i32.const 3827988
    i32.load
    i32.const 0
    call $f53861
    if $I9
      local.get $p0
      i32.const 0
      i32.store8 offset=17
    end
    local.get $l3
    i32.const 16
    i32.add
    global.set $g0)
