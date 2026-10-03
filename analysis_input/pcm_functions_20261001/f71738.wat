  (func $f71738 (type $t1) (param $p0 i32) (param $p1 i32)
    (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32)
    i32.const 32
    local.set $l10
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l3
    global.set $g0
    local.get $l3
    local.tee $l14
    i32.const 0
    i32.store8 offset=12
    local.get $l3
    i32.const 128
    i32.sub
    local.tee $l5
    global.set $g0
    local.get $l3
    local.get $l5
    i32.store offset=8
    block $B0
      local.get $p1
      i32.const 1
      i32.sub
      local.tee $l6
      i32.const 0
      i32.le_s
      br_if $B0
      loop $L1
        block $B2
          local.get $l6
          local.get $l7
          i32.le_s
          br_if $B2
          loop $L3
            local.get $l6
            local.get $l7
            i32.sub
            i32.const 4
            i32.le_u
            if $I4
              loop $L5
                local.get $l7
                local.tee $l4
                i32.const 1
                i32.add
                local.tee $l7
                local.set $l2
                local.get $l4
                local.set $l3
                loop $L6
                  local.get $l2
                  local.get $l3
                  local.get $p0
                  local.get $l2
                  i32.const 2
                  i32.shl
                  i32.add
                  i32.load
                  local.get $p0
                  local.get $l3
                  i32.const 2
                  i32.shl
                  i32.add
                  i32.load
                  i32.lt_u
                  select
                  local.set $l3
                  local.get $l2
                  local.get $l6
                  i32.lt_s
                  local.set $p1
                  local.get $l2
                  i32.const 1
                  i32.add
                  local.set $l2
                  local.get $p1
                  br_if $L6
                end
                local.get $l3
                local.get $l4
                i32.ne
                if $I7
                  local.get $p0
                  local.get $l3
                  i32.const 2
                  i32.shl
                  i32.add
                  local.tee $l2
                  i32.load
                  local.set $l3
                  local.get $l2
                  local.get $p0
                  local.get $l4
                  i32.const 2
                  i32.shl
                  i32.add
                  local.tee $p1
                  i32.load
                  i32.store
                  local.get $p1
                  local.get $l3
                  i32.store
                end
                local.get $l6
                local.get $l7
                i32.ne
                br_if $L5
                br $B2
              end
              unreachable
            end
            block $B8 (result i32)
              local.get $p0
              local.get $l6
              local.get $l7
              i32.add
              i32.const 2
              i32.div_s
              i32.const 2
              i32.shl
              i32.add
              local.tee $l4
              i32.load
              local.tee $l2
              local.get $p0
              local.get $l7
              i32.const 2
              i32.shl
              i32.add
              local.tee $p1
              i32.load
              local.tee $l9
              i32.ge_u
              if $I9
                local.get $l9
                br $B8
              end
              local.get $p1
              local.get $l2
              i32.store
              local.get $l4
              local.get $l9
              i32.store
              local.get $l9
              local.set $l2
              local.get $p1
              i32.load
            end
            local.set $l3
            block $B10
              local.get $l3
              local.get $p0
              local.get $l6
              i32.const 2
              i32.shl
              i32.add
              local.tee $l9
              i32.load
              local.tee $l11
              i32.le_u
              if $I11
                local.get $l11
                local.set $l3
                br $B10
              end
              local.get $p1
              local.get $l11
              i32.store
              local.get $l9
              local.get $l3
              i32.store
              local.get $l4
              i32.load
              local.set $l2
            end
            local.get $l2
            local.get $l3
            i32.gt_u
            if $I12
              local.get $l4
              local.get $l3
              i32.store
              local.get $l9
              local.get $l2
              i32.store
              local.get $l4
              i32.load
              local.set $l2
            end
            local.get $l4
            local.get $p0
            local.get $l6
            i32.const 1
            i32.sub
            local.tee $p1
            i32.const 2
            i32.shl
            i32.add
            local.tee $l15
            i32.load
            i32.store
            local.get $l15
            local.get $l2
            i32.store
            local.get $l7
            local.set $l3
            loop $L13
              local.get $p0
              local.get $l3
              local.tee $l12
              i32.const 1
              i32.add
              local.tee $l3
              i32.const 2
              i32.shl
              i32.add
              local.tee $l4
              i32.load
              local.tee $l9
              local.get $l2
              i32.lt_u
              br_if $L13
              loop $L14
                local.get $l2
                local.get $p0
                local.get $p1
                i32.const 1
                i32.sub
                local.tee $p1
                i32.const 2
                i32.shl
                i32.add
                local.tee $l11
                i32.load
                local.tee $l16
                i32.lt_u
                br_if $L14
              end
              local.get $p1
              local.get $l3
              i32.gt_s
              if $I15
                local.get $l4
                local.get $l16
                i32.store
                local.get $l11
                local.get $l9
                i32.store
                local.get $l15
                i32.load
                local.set $l2
                br $L13
              end
            end
            local.get $l4
            local.get $l2
            i32.store
            local.get $l15
            local.get $l9
            i32.store
            block $B16
              local.get $l3
              local.get $l7
              i32.sub
              local.get $l6
              local.get $l3
              i32.sub
              i32.lt_s
              if $I17
                block $B18
                  local.get $l10
                  i32.const 1
                  i32.sub
                  local.get $l8
                  i32.gt_u
                  if $I19
                    local.get $l5
                    local.set $l2
                    br $B18
                  end
                  local.get $l10
                  i32.const 3
                  i32.shl
                  local.tee $l2
                  if $I20 (result i32)
                    call $f69753
                    local.tee $l3
                    local.get $l2
                    i32.const 3173399
                    i32.const 3172190
                    i32.const 4700888
                    i32.load
                    local.tee $p1
                    local.get $p1
                    i32.load
                    i32.load offset=20
                    call_indirect $__indirect_function_table (type $t5)
                    select
                    i32.const 3172815
                    i32.const 155
                    local.get $l3
                    i32.load
                    i32.load offset=8
                    call_indirect $__indirect_function_table (type $t9)
                  else
                    i32.const 0
                  end
                  local.tee $l2
                  local.get $l5
                  local.get $l8
                  i32.const 2
                  i32.shl
                  call $f483
                  local.set $l3
                  block $B21
                    local.get $l5
                    i32.eqz
                    br_if $B21
                    local.get $l13
                    i32.eqz
                    br_if $B21
                    call $f69753
                    local.tee $p1
                    local.get $l5
                    local.get $p1
                    i32.load
                    i32.load offset=12
                    call_indirect $__indirect_function_table (type $t1)
                  end
                  local.get $l10
                  i32.const 1
                  i32.shl
                  local.set $l10
                  i32.const 1
                  local.set $l13
                  local.get $l3
                  local.set $l5
                end
                local.get $l2
                local.get $l8
                i32.const 2
                i32.shl
                i32.add
                local.tee $l2
                local.get $l7
                i32.store
                local.get $l2
                local.get $l12
                i32.store offset=4
                local.get $l12
                i32.const 2
                i32.add
                local.set $l7
                br $B16
              end
              local.get $l12
              i32.const 2
              i32.add
              local.set $l3
              block $B22
                local.get $l10
                i32.const 1
                i32.sub
                local.get $l8
                i32.gt_u
                if $I23
                  local.get $l5
                  local.set $l2
                  br $B22
                end
                local.get $l10
                i32.const 3
                i32.shl
                local.tee $l2
                if $I24 (result i32)
                  call $f69753
                  local.tee $p1
                  local.get $l2
                  i32.const 3173399
                  i32.const 3172190
                  i32.const 4700888
                  i32.load
                  local.tee $l4
                  local.get $l4
                  i32.load
                  i32.load offset=20
                  call_indirect $__indirect_function_table (type $t5)
                  select
                  i32.const 3172815
                  i32.const 155
                  local.get $p1
                  i32.load
                  i32.load offset=8
                  call_indirect $__indirect_function_table (type $t9)
                else
                  i32.const 0
                end
                local.tee $l2
                local.get $l5
                local.get $l8
                i32.const 2
                i32.shl
                call $f483
                local.set $p1
                block $B25
                  local.get $l5
                  i32.eqz
                  br_if $B25
                  local.get $l13
                  i32.eqz
                  br_if $B25
                  call $f69753
                  local.tee $l4
                  local.get $l5
                  local.get $l4
                  i32.load
                  i32.load offset=12
                  call_indirect $__indirect_function_table (type $t1)
                end
                local.get $l10
                i32.const 1
                i32.shl
                local.set $l10
                i32.const 1
                local.set $l13
                local.get $p1
                local.set $l5
              end
              local.get $l2
              local.get $l8
              i32.const 2
              i32.shl
              i32.add
              local.tee $l2
              local.get $l3
              i32.store
              local.get $l2
              local.get $l6
              i32.store offset=4
              local.get $l12
              local.set $l6
            end
            local.get $l8
            i32.const 2
            i32.add
            local.set $l8
            local.get $l6
            local.get $l7
            i32.gt_s
            br_if $L3
          end
        end
        local.get $l8
        if $I26
          local.get $l5
          local.get $l8
          i32.const 2
          i32.sub
          local.tee $l2
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.set $l7
          local.get $l8
          i32.const 2
          i32.shl
          local.get $l5
          i32.add
          i32.const 4
          i32.sub
          i32.load
          local.set $l6
          local.get $l2
          local.set $l8
          br $L1
        end
      end
      local.get $l5
      i32.eqz
      br_if $B0
      local.get $l13
      i32.eqz
      br_if $B0
      call $f69753
      local.tee $p0
      local.get $l5
      local.get $p0
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $l14
    i32.load8_u offset=12
    if $I27
      local.get $l14
      i32.load offset=8
      call $f70044
    end
    local.get $l14
    i32.const 16
    i32.add
    global.set $g0)