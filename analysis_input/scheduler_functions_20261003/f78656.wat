  (func $f78656 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32)
    i32.const 4758240
    i32.load
    local.set $l3
    block $B0
      i32.const 4787792
      i32.load
      local.tee $l5
      i32.eqz
      br_if $B0
      local.get $l3
      i32.load offset=200
      local.tee $l6
      i32.eqz
      br_if $B0
      local.get $l3
      i32.load offset=192
      local.set $l7
      loop $L1
        block $B2
          local.get $p0
          local.get $l7
          local.get $l2
          i32.const 3
          i32.shl
          i32.add
          local.tee $l4
          i32.load
          i32.eq
          if $I3
            local.get $l4
            i32.load offset=4
            local.get $p1
            i32.eq
            br_if $B2
          end
          local.get $l2
          i32.const 1
          i32.add
          local.tee $l2
          local.get $l6
          i32.ne
          br_if $L1
          br $B0
        end
      end
      local.get $l4
      local.get $l4
      i32.const 8
      i32.add
      local.tee $l2
      local.get $l7
      local.get $l6
      i32.const 3
      i32.shl
      i32.add
      local.get $l2
      i32.sub
      call $f547
      local.set $l2
      local.get $l3
      local.get $l3
      i32.load offset=200
      i32.const 1
      i32.sub
      i32.store offset=200
      local.get $l5
      local.get $l2
      call $f80336
    end
    i32.const 0
    i32.const -1
    local.get $l5
    select)
