  (func $f60126 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32)
    i32.const 4674463
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3753376
      call $f1661
      i32.const 3851236
      call $f1661
      i32.const 3859936
      call $f1661
      i32.const 3828044
      call $f1661
      i32.const 3859920
      call $f1661
      i32.const 4674463
      i32.const 1
      i32.store8
    end
    local.get $p0
    local.get $p0
    call $f60103
    local.get $p0
    i32.load offset=200
    local.set $p1
    i32.const 3753376
    i32.load
    local.tee $l3
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $l3
      call $f65192
    end
    block $B2
      local.get $p1
      i32.const 0
      i32.const 0
      call $f54398
      i32.eqz
      br_if $B2
      block $B3
        local.get $p0
        i32.load offset=200
        i32.load offset=276
        i32.const 0
        call $f53919
        local.tee $p1
        i32.const 0
        call $f53872
        br_if $B3
        local.get $p1
        i32.const 3859920
        i32.load
        i32.const 0
        call $f53861
        br_if $B3
        local.get $p1
        i32.const 3828044
        i32.load
        i32.const 0
        call $f53861
        br_if $B3
        local.get $p1
        i32.const 3859936
        i32.load
        i32.const 0
        call $f53861
        i32.eqz
        br_if $B2
      end
      i32.const 3851236
      i32.load
      local.set $p1
      local.get $p0
      i32.load offset=200
      local.set $l3
      i32.const 4674403
      i32.load8_u
      i32.eqz
      if $I4
        i32.const 3753376
        call $f1661
        i32.const 4674403
        i32.const 1
        i32.store8
      end
      local.get $p0
      i32.load offset=44
      local.set $p2
      i32.const 3753376
      i32.load
      local.tee $l4
      i32.load offset=116
      i32.eqz
      if $I5
        local.get $l4
        call $f65192
      end
      block $B6
        local.get $p2
        i32.const 0
        i32.const 0
        call $f54425
        i32.eqz
        if $I7
          local.get $p0
          i32.load offset=44
          local.set $p2
          br $B6
        end
        i32.const 4675186
        i32.load8_u
        i32.eqz
        if $I8
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
        local.tee $p2
        i32.store offset=44
      end
      local.get $l3
      local.get $p2
      local.get $p1
      i32.const 0
      call $f60665
      i32.const 0
      call $f33357
      local.get $p0
      local.get $p0
      i32.load offset=200
      i32.load offset=276
      i32.store offset=204
    end)
