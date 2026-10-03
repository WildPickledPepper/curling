  (func $f60198 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32)
    i32.const 4674521
    i32.load8_u
    i32.eqz
    if $I0
      i32.const 3749060
      call $f1661
      i32.const 3845340
      call $f1661
      i32.const 3816756
      call $f1661
      i32.const 3816628
      call $f1661
      i32.const 4674521
      i32.const 1
      i32.store8
    end
    i32.const 0
    call $f51726
    i32.const 3845340
    i32.load
    i32.const 0
    call $f53732
    local.set $p2
    i32.const 3749060
    i32.load
    call $f1446
    local.tee $p0
    local.get $p2
    i32.const 0
    call $f51727
    local.get $p0
    i32.const 0
    call $f51728
    local.tee $l4
    i32.load offset=12
    i32.const 0
    i32.gt_s
    if $I1
      i32.const 0
      local.set $p2
      loop $L2
        local.get $l4
        local.get $p2
        i32.const 2
        i32.shl
        i32.add
        i32.load offset=16
        local.tee $p0
        i32.const 0
        call $f22568
        i32.const 3816756
        i32.load
        i32.const 0
        call $f53861
        if $I3
          local.get $p1
          local.get $p0
          local.get $p0
          i32.load
          local.tee $l3
          i32.load offset=268
          local.get $l3
          i32.load offset=264
          call_indirect $__indirect_function_table (type $t0)
          local.get $p0
          local.get $p0
          i32.load
          local.tee $l3
          i32.load offset=268
          local.get $l3
          i32.load offset=264
          call_indirect $__indirect_function_table (type $t0)
          i32.const 3816628
          i32.load
          i32.const 0
          call $f53954
          i32.const 0
          call $f53891
          i32.store
        end
        local.get $p2
        i32.const 1
        i32.add
        local.tee $p2
        local.get $l4
        i32.load offset=12
        i32.lt_s
        br_if $L2
      end
    end)
