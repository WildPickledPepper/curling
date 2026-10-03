  (func $f71468 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32)
    global.get $g0
    i32.const 6144
    i32.sub
    local.tee $l4
    global.set $g0
    block $B0 (result i32)
      i32.const 1
      local.get $p0
      i32.load offset=32
      i32.eqz
      br_if $B0
      drop
      local.get $p0
      i32.load offset=48
      local.tee $l1
      i32.load offset=1140
      local.set $l14
      local.get $l1
      i32.load offset=1000
      local.set $l9
      loop $L1
        local.get $l9
        i32.load offset=184
        local.get $p0
        i32.load offset=28
        local.get $l6
        i32.const 3
        i32.shl
        i32.add
        i64.load
        i64.const 9
        i64.shr_u
        i32.wrap_i64
        i32.const 5
        i32.shl
        i32.add
        i32.load offset=28
        local.tee $l3
        i32.const 20
        i32.sub
        i32.load
        local.tee $l5
        local.get $l5
        f32.load offset=160
        f32.store offset=156
        local.get $l3
        i32.const -64
        i32.add
        local.set $l2
        block $B2
          block $B3
            block $B4
              local.get $l3
              i32.load16_u offset=28
              local.tee $l1
              i32.const 1
              i32.and
              i32.eqz
              if $I5
                local.get $l4
                i32.const 5120
                i32.add
                local.get $l7
                i32.const 2
                i32.shl
                i32.add
                local.get $l2
                i32.store
                local.get $l2
                local.get $p0
                i32.load offset=44
                local.get $l14
                call $f71561
                local.get $l7
                i32.const 1
                i32.add
                local.set $l7
                local.get $l3
                i32.load16_u offset=28
                local.set $l1
                br $B4
              end
              local.get $l1
              i32.const 2
              i32.and
              i32.eqz
              br_if $B4
              local.get $l4
              i32.const 1024
              i32.add
              local.get $l10
              i32.const 2
              i32.shl
              i32.add
              local.set $l8
              local.get $l10
              i32.const 1
              i32.add
              local.set $l10
              br $B3
            end
            local.get $l1
            i32.const 4
            i32.and
            i32.eqz
            br_if $B2
            local.get $l4
            local.get $l15
            i32.const 2
            i32.shl
            i32.add
            local.set $l8
            local.get $l15
            i32.const 1
            i32.add
            local.set $l15
          end
          local.get $l8
          local.get $l2
          i32.store
        end
        local.get $l5
        i32.load8_u offset=44
        i32.const 4
        i32.and
        if $I6
          local.get $l4
          i32.const 4096
          i32.add
          local.get $l11
          i32.const 2
          i32.shl
          i32.add
          local.get $l2
          i32.store
          local.get $l11
          i32.const 1
          i32.add
          local.set $l11
          local.get $l3
          i32.load16_u offset=28
          local.set $l1
        end
        block $B7
          block $B8
            local.get $l1
            i32.const 8
            i32.and
            if $I9
              local.get $l4
              i32.const 3072
              i32.add
              local.get $l12
              i32.const 2
              i32.shl
              i32.add
              local.set $l5
              local.get $l12
              i32.const 1
              i32.add
              local.set $l12
              br $B8
            end
            local.get $l1
            i32.const 16
            i32.and
            i32.eqz
            br_if $B7
            local.get $l4
            i32.const 2048
            i32.add
            local.get $l13
            i32.const 2
            i32.shl
            i32.add
            local.set $l5
            local.get $l13
            i32.const 1
            i32.add
            local.set $l13
          end
          local.get $l5
          local.get $l2
          i32.store
        end
        local.get $l3
        local.get $l1
        i32.const 1
        i32.and
        i32.store16 offset=28
        local.get $l6
        i32.const 1
        i32.add
        local.tee $l6
        local.get $p0
        i32.load offset=32
        i32.lt_u
        br_if $L1
      end
      i32.const 1
      local.get $l7
      i32.eqz
      br_if $B0
      drop
      local.get $p0
      i32.load offset=44
      i32.const 1
      i32.store8 offset=20
      local.get $l14
      i32.const 1
      i32.store8 offset=16
      local.get $l7
      local.set $l16
      i32.const 0
    end
    local.set $l2
    local.get $l12
    local.get $l13
    i32.or
    local.get $l10
    i32.or
    local.get $l11
    i32.or
    local.get $l16
    i32.or
    if $I10
      local.get $p0
      i32.load offset=36
      i32.load offset=1016
      drop
      local.get $p0
      i32.load offset=48
      local.tee $l1
      i32.load offset=980
      local.tee $l3
      i32.const 160
      i32.add
      local.set $l9
      local.get $l2
      i32.eqz
      if $I11
        loop $L12
          local.get $l4
          i32.const 5120
          i32.add
          local.get $l17
          i32.const 2
          i32.shl
          i32.add
          i32.load
          i32.load offset=32
          local.tee $l1
          if $I13
            loop $L14
              local.get $l1
              i32.load offset=40
              i32.const -64
              i32.sub
              i32.load8_u
              i32.const 5
              i32.and
              if $I15
                block $B16
                  local.get $l1
                  i32.load offset=8
                  local.tee $l5
                  i32.const 2147483647
                  i32.and
                  local.tee $l7
                  i32.const 32
                  i32.add
                  i32.const 5
                  i32.shr_u
                  local.tee $l6
                  local.get $l3
                  i32.load offset=164
                  i32.const 2147483647
                  i32.and
                  i32.le_u
                  if $I17
                    local.get $l9
                    i32.load
                    local.set $l2
                    br $B16
                  end
                  local.get $l3
                  i32.load offset=168
                  local.tee $l2
                  local.get $l6
                  i32.const 2
                  i32.shl
                  i32.const 3160746
                  i32.const 438
                  local.get $l2
                  i32.load
                  i32.load offset=8
                  call_indirect $__indirect_function_table (type $t8)
                  local.set $l2
                  block $B18
                    local.get $l3
                    i32.load offset=160
                    local.tee $l8
                    i32.eqz
                    br_if $B18
                    local.get $l2
                    local.get $l8
                    local.get $l3
                    i32.load offset=164
                    i32.const 2
                    i32.shl
                    call $f483
                    drop
                    local.get $l3
                    i32.load offset=164
                    i32.const 0
                    i32.lt_s
                    br_if $B18
                    local.get $l9
                    i32.load
                    local.tee $l8
                    i32.eqz
                    br_if $B18
                    local.get $l3
                    i32.load offset=168
                    local.tee $l14
                    local.get $l8
                    local.get $l14
                    i32.load
                    i32.load offset=12
                    call_indirect $__indirect_function_table (type $t1)
                  end
                  local.get $l2
                  local.get $l3
                  i32.load offset=164
                  local.tee $l8
                  i32.const 2
                  i32.shl
                  i32.add
                  i32.const 0
                  local.get $l6
                  local.get $l8
                  i32.sub
                  i32.const 2
                  i32.shl
                  call $f484
                  drop
                  local.get $l3
                  local.get $l6
                  i32.store offset=164
                  local.get $l3
                  local.get $l2
                  i32.store offset=160
                end
                local.get $l2
                local.get $l7
                i32.const 3
                i32.shr_u
                i32.const 268435452
                i32.and
                i32.add
                local.tee $l2
                local.get $l2
                i32.load
                i32.const 1
                local.get $l5
                i32.shl
                i32.or
                i32.store
              end
              local.get $l1
              i32.load
              local.tee $l1
              br_if $L14
            end
          end
          local.get $l17
          i32.const 1
          i32.add
          local.tee $l17
          local.get $l16
          i32.ne
          br_if $L12
        end
        local.get $p0
        i32.load offset=48
        local.set $l1
      end
      local.get $l11
      if $I19
        local.get $l1
        i32.const 1156
        i32.add
        local.set $l5
        i32.const 0
        local.set $l3
        loop $L20
          local.get $l4
          i32.const 4096
          i32.add
          local.get $l3
          i32.const 2
          i32.shl
          i32.add
          local.set $l2
          block $B21
            local.get $l1
            i32.load offset=1160
            local.tee $l6
            local.get $l1
            i32.load offset=1164
            i32.const 2147483647
            i32.and
            i32.ge_u
            if $I22
              local.get $l5
              local.get $l2
              call $f71653
              br $B21
            end
            local.get $l1
            i32.load offset=1156
            local.get $l6
            i32.const 2
            i32.shl
            i32.add
            local.get $l2
            i32.load
            i32.store
            local.get $l1
            local.get $l1
            i32.load offset=1160
            i32.const 1
            i32.add
            i32.store offset=1160
          end
          local.get $l3
          i32.const 1
          i32.add
          local.tee $l3
          local.get $l11
          i32.ne
          br_if $L20
        end
      end
      local.get $l10
      if $I23
        i32.const 0
        local.set $l1
        loop $L24
          local.get $l4
          i32.const 1024
          i32.add
          local.get $l1
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.get $l9
          call $f71576
          local.get $l1
          i32.const 1
          i32.add
          local.tee $l1
          local.get $l10
          i32.ne
          br_if $L24
        end
      end
      local.get $l15
      if $I25
        i32.const 0
        local.set $l1
        loop $L26
          local.get $l4
          local.get $l1
          i32.const 2
          i32.shl
          i32.add
          i32.load
          call $f71570
          local.get $l1
          i32.const 1
          i32.add
          local.tee $l1
          local.get $l15
          i32.ne
          br_if $L26
        end
      end
      local.get $l12
      if $I27
        i32.const 0
        local.set $l1
        loop $L28
          local.get $l4
          i32.const 3072
          i32.add
          local.get $l1
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $l7
          i32.load offset=40
          i32.load offset=1000
          local.get $l7
          i64.load offset=144
          call $f70712
          local.get $l1
          i32.const 1
          i32.add
          local.tee $l1
          local.get $l12
          i32.ne
          br_if $L28
        end
      end
      local.get $l13
      if $I29
        i32.const 0
        local.set $l1
        loop $L30
          local.get $l4
          i32.const 2048
          i32.add
          local.get $l1
          i32.const 2
          i32.shl
          i32.add
          i32.load
          call $f71567
          local.get $l1
          i32.const 1
          i32.add
          local.tee $l1
          local.get $l13
          i32.ne
          br_if $L30
        end
      end
      local.get $p0
      i32.load offset=36
      i32.load offset=1016
      drop
    end
    local.get $l4
    i32.const 6144
    i32.add
    global.set $g0)