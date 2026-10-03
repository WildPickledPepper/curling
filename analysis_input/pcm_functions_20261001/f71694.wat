  (func $f71694 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32)
    block $B0
      block $B1
        block $B2
          local.get $p0
          i32.load offset=20
          local.tee $l4
          i32.eqz
          br_if $B2
          local.get $p0
          i32.load offset=12
          local.get $l4
          i32.const 1
          i32.sub
          local.get $p1
          i32.load offset=4
          local.tee $l7
          i32.const 14
          i32.shl
          i32.const -65536
          i32.and
          local.get $p1
          i32.load
          local.tee $l8
          i32.const 2
          i32.shr_u
          i32.const 65535
          i32.and
          i32.or
          local.tee $l3
          local.get $l3
          i32.const 15
          i32.shl
          i32.const -1
          i32.xor
          i32.add
          local.tee $l3
          i32.const 10
          i32.shr_u
          local.get $l3
          i32.xor
          i32.const 9
          i32.mul
          local.tee $l3
          i32.const 6
          i32.shr_u
          local.get $l3
          i32.xor
          local.tee $l3
          local.get $l3
          i32.const 11
          i32.shl
          i32.const -1
          i32.xor
          i32.add
          local.tee $l3
          i32.const 16
          i32.shr_u
          local.get $l3
          i32.xor
          i32.and
          local.tee $l5
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $l4
          i32.const -1
          i32.eq
          br_if $B2
          local.get $p0
          i32.const 4
          i32.add
          local.set $l6
          local.get $p0
          i32.load offset=4
          local.set $l9
          loop $L3
            local.get $l8
            local.get $l9
            local.get $l4
            i32.const 12
            i32.mul
            i32.add
            local.tee $l3
            i32.load
            i32.eq
            if $I4
              local.get $l3
              i32.load offset=4
              local.get $l7
              i32.eq
              br_if $B1
            end
            local.get $p0
            i32.load offset=8
            local.get $l4
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.tee $l4
            i32.const -1
            i32.ne
            br_if $L3
          end
        end
        local.get $p2
        i32.const 0
        i32.store8
        local.get $p0
        i32.load offset=36
        local.get $p0
        i32.load offset=16
        i32.eq
        if $I5
          local.get $p0
          i32.load offset=20
          local.tee $l4
          local.get $l4
          i32.const 1
          i32.shl
          i32.const 16
          local.get $l4
          select
          local.tee $l3
          i32.lt_u
          if $I6 (result i32)
            local.get $p0
            local.get $l3
            call $f71687
            local.get $p0
            i32.load offset=20
          else
            local.get $l4
          end
          i32.const 1
          i32.sub
          local.get $p1
          i32.load offset=4
          i32.const 14
          i32.shl
          i32.const -65536
          i32.and
          local.get $p1
          i32.load
          i32.const 2
          i32.shr_u
          i32.const 65535
          i32.and
          i32.or
          local.tee $l3
          local.get $l3
          i32.const 15
          i32.shl
          i32.const -1
          i32.xor
          i32.add
          local.tee $l3
          i32.const 10
          i32.shr_u
          local.get $l3
          i32.xor
          i32.const 9
          i32.mul
          local.tee $l3
          i32.const 6
          i32.shr_u
          local.get $l3
          i32.xor
          local.tee $l3
          local.get $l3
          i32.const 11
          i32.shl
          i32.const -1
          i32.xor
          i32.add
          local.tee $l3
          i32.const 16
          i32.shr_u
          local.get $l3
          i32.xor
          i32.and
          local.set $l5
        end
        local.get $p0
        local.get $p0
        i32.load offset=28
        local.tee $l4
        i32.const 1
        i32.add
        i32.store offset=28
        local.get $p0
        i32.load offset=8
        local.get $l4
        i32.const 2
        i32.shl
        i32.add
        local.get $l5
        i32.const 2
        i32.shl
        local.tee $l3
        local.get $p0
        i32.load offset=12
        i32.add
        i32.load
        i32.store
        local.get $p0
        i32.load offset=12
        local.get $l3
        i32.add
        local.get $l4
        i32.store
        local.get $p0
        local.get $p0
        i32.load offset=36
        i32.const 1
        i32.add
        i32.store offset=36
        local.get $p0
        local.get $p0
        i32.load offset=32
        i32.const 1
        i32.add
        i32.store offset=32
        local.get $p0
        i32.const 4
        i32.add
        local.set $l6
        br $B0
      end
      local.get $p2
      i32.const 1
      i32.store8
    end
    local.get $l6
    i32.load
    local.get $l4
    i32.const 12
    i32.mul
    i32.add)