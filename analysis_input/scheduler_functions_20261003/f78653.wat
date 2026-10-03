  (func $f78653 (type $t0) (param $p0 i32) (param $p1 i32) (result i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32)
    i32.const 4758240
    i32.load
    local.set $l3
    i32.const -1
    local.set $l4
    block $B0
      i32.const 4787792
      i32.load
      local.tee $l5
      i32.eqz
      br_if $B0
      block $B1 (result i32)
        block $B2
          local.get $l3
          i32.load offset=64
          local.tee $l2
          i32.load
          local.get $p0
          i32.ne
          br_if $B2
          local.get $l2
          i32.load offset=4
          local.get $p1
          i32.ne
          br_if $B2
          i32.const 0
          br $B1
        end
        block $B3
          local.get $l2
          i32.load offset=8
          local.get $p0
          i32.ne
          br_if $B3
          local.get $l2
          i32.load offset=12
          local.get $p1
          i32.ne
          br_if $B3
          local.get $l2
          i32.const 8
          i32.add
          local.set $l2
          i32.const 1
          br $B1
        end
        block $B4
          local.get $l2
          i32.load offset=16
          local.get $p0
          i32.ne
          br_if $B4
          local.get $l2
          i32.load offset=20
          local.get $p1
          i32.ne
          br_if $B4
          local.get $l2
          i32.const 16
          i32.add
          local.set $l2
          i32.const 2
          br $B1
        end
        local.get $l2
        i32.load offset=24
        local.get $p0
        i32.ne
        br_if $B0
        local.get $l2
        i32.load offset=28
        local.get $p1
        i32.ne
        br_if $B0
        local.get $l2
        i32.const 24
        i32.add
        local.set $l2
        i32.const 3
      end
      local.set $p0
      i32.const 0
      local.set $l4
      local.get $l2
      i32.const 0
      i32.store
      local.get $l3
      i32.load offset=64
      local.get $p0
      i32.const 3
      i32.shl
      i32.add
      i32.const 0
      i32.store offset=4
      local.get $l5
      local.get $l2
      call $f80335
    end
    local.get $l4)
