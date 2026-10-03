  (func $f78699 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32)
    i32.const 4125408
    i32.load
    local.set $l2
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l3
    global.set $g0
    local.get $p1
    local.get $l2
    i32.const 4129148
    i32.load
    local.get $l3
    i32.const 8
    i32.add
    i32.const 1
    call $f78385
    local.tee $l2
    if $I0
      block $B1
        local.get $l2
        i32.const 0
        i32.gt_s
        if $I2
          local.get $p0
          local.get $p1
          call $f80218
          local.get $p1
          i32.const 136988
          i32.const 220012
          local.get $l3
          i32.const 12
          i32.add
          i32.const 1
          call $f78385
          local.tee $l2
          i32.eqz
          br_if $B1
          local.get $p0
          i32.const 32
          i32.add
          local.set $p0
          local.get $l2
          i32.const 0
          i32.gt_s
          if $I3
            local.get $p0
            local.get $p1
            call $f82992
            local.get $p1
            call $f78387
            br $B1
          end
          local.get $l3
          i32.load offset=12
          local.tee $l2
          if $I4
            local.get $p0
            local.get $p1
            local.get $l2
            call_indirect $__indirect_function_table (type $t0)
            drop
          end
          local.get $p1
          call $f78387
          br $B1
        end
        local.get $l3
        i32.load offset=8
        local.tee $l2
        i32.eqz
        br_if $B1
        local.get $p0
        local.get $p1
        local.get $l2
        call_indirect $__indirect_function_table (type $t0)
        drop
      end
      local.get $p1
      call $f78387
    end
    local.get $l3
    i32.const 16
    i32.add
    global.set $g0)
