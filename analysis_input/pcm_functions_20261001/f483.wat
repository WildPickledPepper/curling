  (func $f483 (type $t3) (param $p0 i32) (param $p1 i32) (param $p2 i32) (result i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32)
    local.get $p2
    i32.const 512
    i32.ge_u
    if $I0
      local.get $p0
      local.get $p1
      local.get $p2
      call $env.emscripten_memcpy_big
      drop
      local.get $p0
      return
    end
    local.get $p0
    local.get $p2
    i32.add
    local.set $l3
    block $B1
      local.get $p0
      local.get $p1
      i32.xor
      i32.const 3
      i32.and
      i32.eqz
      if $I2
        block $B3
          local.get $p0
          i32.const 3
          i32.and
          i32.eqz
          if $I4
            local.get $p0
            local.set $p2
            br $B3
          end
          local.get $p2
          i32.eqz
          if $I5
            local.get $p0
            local.set $p2
            br $B3
          end
          local.get $p0
          local.set $p2
          loop $L6
            local.get $p2
            local.get $p1
            i32.load8_u
            i32.store8
            local.get $p1
            i32.const 1
            i32.add
            local.set $p1
            local.get $p2
            i32.const 1
            i32.add
            local.tee $p2
            i32.const 3
            i32.and
            i32.eqz
            br_if $B3
            local.get $p2
            local.get $l3
            i32.lt_u
            br_if $L6
          end
        end
        block $B7
          local.get $l3
          i32.const -4
          i32.and
          local.tee $l4
          i32.const 64
          i32.lt_u
          br_if $B7
          local.get $p2
          local.get $l4
          i32.const -64
          i32.add
          local.tee $l5
          i32.gt_u
          br_if $B7
          loop $L8
            local.get $p2
            local.get $p1
            i32.load
            i32.store
            local.get $p2
            local.get $p1
            i32.load offset=4
            i32.store offset=4
            local.get $p2
            local.get $p1
            i32.load offset=8
            i32.store offset=8
            local.get $p2
            local.get $p1
            i32.load offset=12
            i32.store offset=12
            local.get $p2
            local.get $p1
            i32.load offset=16
            i32.store offset=16
            local.get $p2
            local.get $p1
            i32.load offset=20
            i32.store offset=20
            local.get $p2
            local.get $p1
            i32.load offset=24
            i32.store offset=24
            local.get $p2
            local.get $p1
            i32.load offset=28
            i32.store offset=28
            local.get $p2
            local.get $p1
            i32.load offset=32
            i32.store offset=32
            local.get $p2
            local.get $p1
            i32.load offset=36
            i32.store offset=36
            local.get $p2
            local.get $p1
            i32.load offset=40
            i32.store offset=40
            local.get $p2
            local.get $p1
            i32.load offset=44
            i32.store offset=44
            local.get $p2
            local.get $p1
            i32.load offset=48
            i32.store offset=48
            local.get $p2
            local.get $p1
            i32.load offset=52
            i32.store offset=52
            local.get $p2
            local.get $p1
            i32.load offset=56
            i32.store offset=56
            local.get $p2
            local.get $p1
            i32.load offset=60
            i32.store offset=60
            local.get $p1
            i32.const -64
            i32.sub
            local.set $p1
            local.get $p2
            i32.const -64
            i32.sub
            local.tee $p2
            local.get $l5
            i32.le_u
            br_if $L8
          end
        end
        local.get $p2
        local.get $l4
        i32.ge_u
        br_if $B1
        loop $L9
          local.get $p2
          local.get $p1
          i32.load
          i32.store
          local.get $p1
          i32.const 4
          i32.add
          local.set $p1
          local.get $p2
          i32.const 4
          i32.add
          local.tee $p2
          local.get $l4
          i32.lt_u
          br_if $L9
        end
        br $B1
      end
      local.get $l3
      i32.const 4
      i32.lt_u
      if $I10
        local.get $p0
        local.set $p2
        br $B1
      end
      local.get $p0
      local.get $l3
      i32.const 4
      i32.sub
      local.tee $l4
      i32.gt_u
      if $I11
        local.get $p0
        local.set $p2
        br $B1
      end
      local.get $p0
      local.set $p2
      loop $L12
        local.get $p2
        local.get $p1
        i32.load8_u
        i32.store8
        local.get $p2
        local.get $p1
        i32.load8_u offset=1
        i32.store8 offset=1
        local.get $p2
        local.get $p1
        i32.load8_u offset=2
        i32.store8 offset=2
        local.get $p2
        local.get $p1
        i32.load8_u offset=3
        i32.store8 offset=3
        local.get $p1
        i32.const 4
        i32.add
        local.set $p1
        local.get $p2
        i32.const 4
        i32.add
        local.tee $p2
        local.get $l4
        i32.le_u
        br_if $L12
      end
    end
    local.get $p2
    local.get $l3
    i32.lt_u
    if $I13
      loop $L14
        local.get $p2
        local.get $p1
        i32.load8_u
        i32.store8
        local.get $p1
        i32.const 1
        i32.add
        local.set $p1
        local.get $p2
        i32.const 1
        i32.add
        local.tee $p2
        local.get $l3
        i32.ne
        br_if $L14
      end
    end
    local.get $p0)