  (func $f60138 (type $t4) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32)
    (local $l4 i32)
    i32.const 4674476
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3753376
      call $f1661
      i32.const 3824764
      call $f1661
      i32.const 4674476
      i32.const 1
      i32.store8
    end
    i32.const 3753376
    i32.load
    local.tee $p3
    i32.load offset=116
    i32.eqz
    if $I1
      local.get $p3
      call $f65192
    end
    block $B2
      local.get $p1
      i32.const 0
      i32.const 0
      call $f54425
      br_if $B2
      local.get $p0
      i32.load offset=44
      local.set $p3
      i32.const 3753376
      i32.load
      local.tee $l4
      i32.load offset=116
      i32.eqz
      if $I3
        local.get $l4
        call $f65192
      end
      block $B4
        local.get $p3
        i32.const 0
        i32.const 0
        call $f54425
        i32.eqz
        if $I5
          local.get $p0
          i32.load offset=44
          local.set $p3
          br $B4
        end
        i32.const 4675186
        i32.load8_u
        i32.eqz
        if $I6
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
        local.tee $p3
        i32.store offset=44
      end
      local.get $p1
      local.get $p3
      local.get $p2
      i32.const 0
      call $f60665
      local.get $p1
      i32.load
      local.tee $p2
      i32.load offset=796
      local.get $p2
      i32.load offset=792
      call_indirect $__indirect_function_table (type $t2)
      local.get $p0
      i32.load offset=44
      i32.const 3824764
      i32.load
      i32.const 0
      call $f60671
      local.set $p0
      i32.const 3753376
      i32.load
      local.tee $p2
      i32.load offset=116
      i32.eqz
      if $I7
        local.get $p2
        call $f65192
      end
      local.get $p0
      i32.const 0
      i32.const 0
      call $f54398
      i32.eqz
      br_if $B2
      local.get $p1
      local.get $p0
      i32.const 0
      call $f33988
    end)