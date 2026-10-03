  (func $f71750 (type $t2) (param $p0 i32) (param $p1 i32) (param $p2 i32)
    (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i64)
    global.get $g0
    i32.const 32
    i32.sub
    local.tee $l15
    global.set $g0
    block $B0
      local.get $p2
      i32.eqz
      br_if $B0
      local.get $p0
      i32.const 1
      i32.store8 offset=337
      local.get $p0
      i32.const 340
      i32.add
      local.set $l16
      local.get $p0
      i32.const 52
      i32.add
      local.set $l5
      local.get $p0
      i32.const 312
      i32.add
      local.set $l17
      local.get $p0
      i32.const 284
      i32.add
      local.set $l19
      loop $L1
        local.get $l15
        local.get $p0
        i32.load offset=296
        local.get $p0
        i32.load offset=300
        local.get $p1
        local.get $l18
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l12
        i32.const 2
        i32.shl
        i32.add
        local.tee $l8
        i32.load
        i32.const 3
        i32.shl
        i32.add
        i64.load align=4
        i64.store offset=24
        local.get $l8
        i32.load
        local.set $l8
        local.get $l19
        local.get $l12
        call $f71887
        local.set $l12
        block $B2
          local.get $p0
          i32.load8_u offset=336
          i32.eqz
          br_if $B2
          local.get $p0
          i32.load offset=4
          local.tee $l14
          i32.eqz
          br_if $B2
          local.get $p0
          i32.const 1
          i32.store8 offset=338
          i32.const -1
          local.set $l9
          local.get $l8
          local.get $p0
          i32.load offset=316
          i32.lt_u
          if $I3
            local.get $l17
            i32.load
            local.get $l8
            i32.const 2
            i32.shl
            i32.add
            i32.load
            local.set $l9
          end
          local.get $l15
          local.get $p0
          i32.load offset=296
          local.get $l8
          i32.const 3
          i32.shl
          i32.add
          i64.load align=4
          i64.store offset=16
          block $B4
            local.get $l9
            i32.const -1
            i32.ne
            if $I5
              local.get $l14
              local.get $l9
              call $f71747
              local.get $l5
              local.get $l8
              local.get $l15
              i32.const 16
              i32.add
              local.get $l12
              i32.const 1
              call $f71866
              br $B4
            end
            local.get $l15
            i32.const 24
            i32.add
            local.set $l6
            local.get $l15
            i32.const 16
            i32.add
            local.set $l14
            local.get $l15
            i32.const 8
            i32.add
            local.set $l9
            block $B6
              block $B7
                block $B8
                  local.get $l5
                  i32.load offset=164
                  i32.eqz
                  br_if $B8
                  local.get $l5
                  i32.load offset=140
                  local.get $l6
                  i32.load
                  local.tee $l11
                  i64.extend_i32_u
                  local.tee $l20
                  local.get $l6
                  i32.load offset=4
                  local.tee $l13
                  i64.extend_i32_u
                  i64.const 32
                  i64.shl
                  i64.or
                  local.get $l20
                  i64.const 32
                  i64.shl
                  i64.const -1
                  i64.xor
                  i64.add
                  local.tee $l20
                  i64.const 22
                  i64.shr_u
                  local.get $l20
                  i64.xor
                  local.tee $l20
                  local.get $l20
                  i64.const 13
                  i64.shl
                  i64.const -1
                  i64.xor
                  i64.add
                  local.tee $l20
                  i64.const 8
                  i64.shr_u
                  local.get $l20
                  i64.xor
                  i64.const 9
                  i64.mul
                  local.tee $l20
                  i64.const 15
                  i64.shr_u
                  local.get $l20
                  i64.xor
                  local.tee $l20
                  local.get $l20
                  i64.const 27
                  i64.shl
                  i64.const -1
                  i64.xor
                  i64.add
                  local.tee $l20
                  i64.const 31
                  i64.shr_u
                  local.get $l20
                  i64.xor
                  i32.wrap_i64
                  local.get $l5
                  i32.load offset=148
                  i32.const 1
                  i32.sub
                  i32.and
                  i32.const 2
                  i32.shl
                  i32.add
                  local.tee $l4
                  i32.load
                  local.tee $l6
                  i32.const -1
                  i32.eq
                  br_if $B8
                  local.get $l5
                  i32.load offset=136
                  local.set $l10
                  local.get $l11
                  local.get $l5
                  i32.load offset=132
                  local.tee $l3
                  local.get $l6
                  i32.const 20
                  i32.mul
                  i32.add
                  local.tee $l7
                  i32.load
                  i32.eq
                  if $I9
                    local.get $l7
                    i32.load offset=4
                    local.get $l13
                    i32.eq
                    br_if $B7
                  end
                  loop $L10
                    local.get $l10
                    local.get $l6
                    i32.const 2
                    i32.shl
                    i32.add
                    local.tee $l4
                    i32.load
                    local.tee $l6
                    i32.const -1
                    i32.eq
                    br_if $B8
                    local.get $l3
                    local.get $l6
                    i32.const 20
                    i32.mul
                    i32.add
                    local.tee $l7
                    i32.load
                    local.get $l11
                    i32.ne
                    br_if $L10
                    local.get $l13
                    local.get $l7
                    i32.load offset=4
                    i32.ne
                    br_if $L10
                  end
                  br $B7
                end
                local.get $l5
                local.get $l8
                local.get $l14
                local.get $l12
                i32.const 0
                call $f71866
                global.get $g0
                i32.const 32
                i32.sub
                local.tee $l3
                global.set $g0
                local.get $l3
                local.get $l12
                i32.store offset=20
                local.get $l3
                local.get $l8
                i32.store offset=24
                local.get $l3
                i64.const 0
                i64.store offset=8
                block $B11
                  i32.const 4
                  i32.const 0
                  local.get $l5
                  i32.const 4
                  i32.add
                  local.tee $l4
                  i32.load offset=4
                  i32.const 48
                  i32.mul
                  local.get $l4
                  i32.add
                  i32.const 16
                  i32.add
                  local.get $l3
                  i32.const 24
                  i32.add
                  local.get $l3
                  i32.const 8
                  i32.add
                  call $f71867
                  select
                  local.get $l4
                  i32.add
                  i32.load
                  local.tee $l11
                  local.get $l4
                  i32.load
                  i32.eq
                  if $I12
                    local.get $l4
                    local.get $l11
                    i32.const 48
                    i32.mul
                    i32.add
                    i32.const 16
                    i32.add
                    local.get $l3
                    i32.const 24
                    i32.add
                    local.get $l3
                    i32.const 8
                    i32.add
                    call $f71867
                    i32.eqz
                    br_if $B11
                  end
                  local.get $l9
                  local.get $l4
                  local.get $l11
                  i32.const 48
                  i32.mul
                  i32.add
                  local.tee $l14
                  i32.load offset=8
                  i32.store
                  block $B13
                    local.get $l14
                    i32.load offset=12
                    local.get $l3
                    i32.load offset=12
                    local.get $l3
                    i32.load offset=24
                    local.get $l4
                    i32.load offset=104
                    i32.load offset=8
                    call $f71794
                    local.tee $l9
                    i32.eqz
                    br_if $B13
                    local.get $l9
                    i32.load offset=40
                    br_if $B13
                    local.get $l9
                    i32.load offset=36
                    local.tee $l10
                    i32.load
                    i32.eqz
                    br_if $B13
                    local.get $l4
                    local.get $l11
                    i32.const 48
                    i32.mul
                    i32.add
                    i32.const 16
                    i32.add
                    local.set $l11
                    i32.const 0
                    local.set $l14
                    loop $L14
                      local.get $l3
                      local.get $l10
                      local.get $l14
                      i32.const 2
                      i32.shl
                      i32.add
                      i32.load offset=4
                      i32.store
                      local.get $l11
                      local.get $l3
                      local.get $l3
                      i32.const 31
                      i32.add
                      call $f71843
                      local.set $l10
                      local.get $l3
                      i32.load8_u offset=31
                      i32.eqz
                      if $I15
                        local.get $l3
                        i32.load
                        local.set $l13
                        local.get $l10
                        i32.const 0
                        i32.store offset=4
                        local.get $l10
                        local.get $l13
                        i32.store
                      end
                      local.get $l10
                      local.get $l9
                      i32.store offset=4
                      local.get $l14
                      i32.const 1
                      i32.add
                      local.tee $l14
                      local.get $l9
                      i32.load offset=36
                      local.tee $l10
                      i32.load
                      i32.lt_u
                      br_if $L14
                    end
                  end
                  local.get $l3
                  i32.load offset=24
                  local.get $l3
                  i32.load offset=20
                  i32.eq
                  br_if $B11
                  local.get $l3
                  i64.const 0
                  i64.store
                  local.get $l4
                  i32.const 0
                  i32.const 4
                  local.get $l4
                  local.get $l4
                  i32.load
                  i32.const 48
                  i32.mul
                  i32.add
                  i32.const 16
                  i32.add
                  local.get $l3
                  i32.const 20
                  i32.add
                  local.get $l3
                  call $f71867
                  select
                  i32.add
                  i32.load
                  local.tee $l10
                  local.get $l4
                  i32.load offset=4
                  i32.eq
                  if $I16
                    local.get $l4
                    local.get $l10
                    i32.const 48
                    i32.mul
                    i32.add
                    i32.const 16
                    i32.add
                    local.get $l3
                    i32.const 20
                    i32.add
                    local.get $l3
                    call $f71867
                    i32.eqz
                    br_if $B11
                  end
                  local.get $l3
                  i32.load offset=4
                  local.set $l11
                  local.get $l4
                  local.get $l10
                  i32.const 48
                  i32.mul
                  i32.add
                  i32.const 16
                  i32.add
                  local.get $l3
                  i32.const 24
                  i32.add
                  local.get $l3
                  i32.const 31
                  i32.add
                  call $f71843
                  local.set $l9
                  local.get $l3
                  i32.load8_u offset=31
                  i32.eqz
                  if $I17
                    local.get $l3
                    i32.load offset=24
                    local.set $l13
                    local.get $l9
                    i32.const 0
                    i32.store offset=4
                    local.get $l9
                    local.get $l13
                    i32.store
                  end
                  local.get $l9
                  local.get $l11
                  i32.store offset=4
                  local.get $l4
                  local.get $l10
                  i32.const 48
                  i32.mul
                  i32.add
                  i32.load offset=12
                  local.get $l3
                  i32.load offset=4
                  local.get $l3
                  i32.load offset=20
                  local.get $l3
                  i32.load offset=24
                  call $f71799
                end
                local.get $l3
                i32.const 32
                i32.add
                global.set $g0
                br $B6
              end
              local.get $l3
              local.get $l6
              i32.const 20
              i32.mul
              local.tee $l11
              i32.add
              local.tee $l7
              i32.load offset=16
              local.set $l3
              local.get $l7
              i32.load offset=12
              local.set $l13
              local.get $l4
              local.get $l10
              local.get $l6
              i32.const 2
              i32.shl
              local.tee $l9
              i32.add
              i32.load
              i32.store
              local.get $l5
              local.get $l5
              i32.load offset=164
              i32.const 1
              i32.sub
              local.tee $l7
              i32.store offset=164
              local.get $l5
              i32.const 160
              i32.add
              local.tee $l4
              local.get $l4
              i32.load
              i32.const 1
              i32.add
              i32.store
              local.get $l6
              local.get $l7
              i32.ne
              if $I18
                local.get $l5
                i32.load offset=132
                local.tee $l10
                local.get $l11
                i32.add
                local.tee $l4
                local.get $l10
                local.get $l7
                i32.const 20
                i32.mul
                i32.add
                local.tee $l7
                i64.load align=4
                i64.store align=4
                local.get $l4
                local.get $l7
                i64.load offset=8 align=4
                i64.store offset=8 align=4
                local.get $l4
                local.get $l7
                i32.load offset=16
                i32.store offset=16
                local.get $l5
                i32.load offset=136
                local.tee $l7
                local.get $l9
                i32.add
                local.get $l7
                local.get $l5
                i32.load offset=164
                i32.const 2
                i32.shl
                i32.add
                i32.load
                i32.store
                local.get $l5
                i32.load offset=140
                local.get $l5
                i32.load offset=132
                local.get $l11
                i32.add
                local.tee $l7
                i64.load32_u offset=4
                i64.const 32
                i64.shl
                local.get $l7
                i64.load32_u
                local.tee $l20
                i64.or
                local.get $l20
                i64.const 32
                i64.shl
                i64.const -1
                i64.xor
                i64.add
                local.tee $l20
                i64.const 22
                i64.shr_u
                local.get $l20
                i64.xor
                local.tee $l20
                local.get $l20
                i64.const 13
                i64.shl
                i64.const -1
                i64.xor
                i64.add
                local.tee $l20
                i64.const 8
                i64.shr_u
                local.get $l20
                i64.xor
                i64.const 9
                i64.mul
                local.tee $l20
                i64.const 15
                i64.shr_u
                local.get $l20
                i64.xor
                local.tee $l20
                local.get $l20
                i64.const 27
                i64.shl
                i64.const -1
                i64.xor
                i64.add
                local.tee $l20
                i64.const 31
                i64.shr_u
                local.get $l20
                i64.xor
                i32.wrap_i64
                local.get $l5
                i32.load offset=148
                i32.const 1
                i32.sub
                i32.and
                i32.const 2
                i32.shl
                i32.add
                local.tee $l4
                i32.load
                local.tee $l7
                local.get $l5
                i32.load offset=164
                local.tee $l11
                i32.ne
                if $I19
                  local.get $l5
                  i32.load offset=136
                  local.set $l10
                  loop $L20
                    local.get $l10
                    local.get $l7
                    i32.const 2
                    i32.shl
                    i32.add
                    local.tee $l4
                    i32.load
                    local.tee $l7
                    local.get $l11
                    i32.ne
                    br_if $L20
                  end
                end
                local.get $l4
                local.get $l6
                i32.store
              end
              local.get $l5
              i32.const 156
              i32.add
              local.tee $l6
              local.get $l6
              i32.load
              i32.const 1
              i32.sub
              i32.store
              local.get $l3
              i32.const 3
              i32.shl
              local.tee $l6
              local.get $l5
              i32.load offset=200
              i32.add
              i32.load
              local.get $l13
              call $f71747
              local.get $l5
              i32.load offset=168
              local.get $l3
              local.get $l5
              i32.load offset=176
              i32.lt_u
              if $I21 (result i32)
                local.get $l5
                i32.load offset=172
                local.get $l3
                i32.const 2
                i32.shl
                i32.add
                i32.load
              else
                i32.const -1
              end
              call $f71747
              block $B22
                local.get $l5
                i32.load offset=200
                local.get $l6
                i32.add
                i32.load
                local.tee $l6
                i32.load offset=8
                local.get $l13
                i32.const 28
                i32.mul
                i32.add
                local.tee $l4
                i32.load offset=24
                local.tee $l10
                i32.const 1
                i32.shr_u
                i32.const 15
                i32.and
                local.tee $l7
                i32.eqz
                br_if $B22
                local.get $l4
                i32.const 24
                i32.add
                local.set $l3
                local.get $l6
                i32.load
                local.get $l10
                i32.const 3
                i32.shr_u
                i32.const 536870908
                i32.and
                i32.add
                local.set $l4
                i32.const 0
                local.set $l6
                loop $L23
                  local.get $l8
                  local.get $l4
                  local.get $l6
                  i32.const 2
                  i32.shl
                  i32.add
                  local.tee $l11
                  i32.load
                  i32.eq
                  if $I24
                    local.get $l3
                    local.get $l10
                    i32.const -31
                    i32.and
                    local.get $l7
                    i32.const 1
                    i32.sub
                    local.tee $l7
                    i32.const 1
                    i32.shl
                    i32.or
                    i32.store
                    local.get $l11
                    i32.const -1
                    i32.store
                    local.get $l6
                    local.get $l7
                    i32.eq
                    br_if $B22
                    local.get $l11
                    local.get $l4
                    local.get $l7
                    i32.const 2
                    i32.shl
                    i32.add
                    local.tee $l6
                    i32.load
                    i32.store
                    local.get $l6
                    i32.const -1
                    i32.store
                    br $B22
                  end
                  local.get $l6
                  i32.const 1
                  i32.add
                  local.tee $l6
                  local.get $l7
                  i32.ne
                  br_if $L23
                end
              end
              local.get $l5
              local.get $l8
              local.get $l14
              local.get $l12
              i32.const 1
              call $f71866
              local.get $l5
              i32.const 1
              i32.store8 offset=212
            end
          end
          local.get $l17
          local.get $l8
          local.get $l12
          local.get $p0
          i32.load offset=4
          call $f71833
          local.get $p0
          i32.load offset=32
          i32.eqz
          br_if $B2
          local.get $l15
          local.get $l12
          i32.store offset=12
          local.get $l15
          local.get $l8
          i32.store offset=8
          local.get $p0
          i32.load offset=344
          local.tee $l8
          local.get $p0
          i32.load offset=348
          i32.const 2147483647
          i32.and
          i32.ge_u
          if $I25
            local.get $l15
            i32.const 8
            i32.add
            local.set $l14
            i32.const 0
            local.set $l12
            block $B26
              local.get $l16
              i32.load offset=8
              i32.const 2147483647
              i32.and
              local.tee $l3
              i32.const 1
              i32.shl
              i32.const 1
              local.get $l3
              select
              local.tee $l9
              i32.eqz
              br_if $B26
              local.get $l9
              i32.const 3
              i32.shl
              local.tee $l3
              i32.eqz
              br_if $B26
              call $f69753
              local.tee $l8
              local.get $l3
              i32.const 3176889
              i32.const 3176295
              i32.const 4700888
              i32.load
              local.tee $l13
              local.get $l13
              i32.load
              i32.load offset=20
              call_indirect $__indirect_function_table (type $t5)
              select
              i32.const 3176253
              i32.const 553
              local.get $l8
              i32.load
              i32.load offset=8
              call_indirect $__indirect_function_table (type $t9)
              local.set $l12
            end
            local.get $l12
            local.get $l16
            i32.load offset=4
            local.tee $l3
            i32.const 0
            i32.gt_s
            if $I27 (result i32)
              local.get $l12
              local.get $l3
              i32.const 3
              i32.shl
              i32.add
              local.set $l13
              local.get $l16
              i32.load
              local.set $l3
              local.get $l12
              local.set $l8
              loop $L28
                local.get $l8
                local.get $l3
                i64.load align=4
                i64.store align=4
                local.get $l3
                i32.const 8
                i32.add
                local.set $l3
                local.get $l8
                i32.const 8
                i32.add
                local.tee $l8
                local.get $l13
                i32.lt_u
                br_if $L28
              end
              local.get $l16
              i32.load offset=4
            else
              local.get $l3
            end
            i32.const 3
            i32.shl
            i32.add
            local.get $l14
            i64.load align=4
            i64.store align=4
            block $B29
              local.get $l16
              i32.load offset=8
              i32.const 0
              i32.lt_s
              br_if $B29
              local.get $l16
              i32.load
              local.tee $l3
              i32.eqz
              br_if $B29
              call $f69753
              local.tee $l8
              local.get $l3
              local.get $l8
              i32.load
              i32.load offset=12
              call_indirect $__indirect_function_table (type $t1)
            end
            local.get $l16
            local.get $l9
            i32.store offset=8
            local.get $l16
            local.get $l12
            i32.store
            local.get $l16
            local.get $l16
            i32.load offset=4
            i32.const 1
            i32.add
            i32.store offset=4
            br $B2
          end
          local.get $p0
          i32.load offset=340
          local.get $l8
          i32.const 3
          i32.shl
          i32.add
          local.get $l15
          i64.load offset=8
          i64.store align=4
          local.get $p0
          local.get $p0
          i32.load offset=344
          i32.const 1
          i32.add
          i32.store offset=344
        end
        local.get $l18
        i32.const 1
        i32.add
        local.tee $l18
        local.get $p2
        i32.ne
        br_if $L1
      end
      local.get $p0
      i32.load offset=284
      br_if $B0
      local.get $p0
      call $f71742
      local.get $p0
      i32.const 1
      i32.store8 offset=337
    end
    local.get $l15
    i32.const 32
    i32.add
    global.set $g0)