  (func $f71259 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 i32) (local $l23 i32) (local $l24 i64)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l21
    global.set $g0
    local.get $p0
    i32.load offset=92
    i32.const 5
    i32.shl
    local.set $l18
    local.get $p0
    i32.load offset=28
    local.tee $l1
    i32.load offset=440
    local.set $l23
    local.get $l1
    i32.load offset=452
    local.set $l22
    local.get $p0
    i32.load offset=32
    i32.load
    local.tee $l4
    i32.load offset=11960
    local.set $l5
    block $B0
      local.get $l4
      i32.const 11896
      i32.add
      i32.load
      i32.eqz
      if $I1
        local.get $l5
        local.set $l7
        br $B0
      end
      local.get $l5
      local.set $l7
      i32.const 0
      local.set $l1
      loop $L2
        i32.const 0
        local.set $l16
        block $B3 (result i32)
          local.get $l4
          i32.load offset=11892
          local.tee $l3
          local.get $l19
          i32.const 2
          i32.shl
          local.tee $l20
          i32.add
          i32.load
          local.get $l12
          i32.add
          local.tee $l17
          local.get $l12
          i32.gt_u
          if $I4
            local.get $l12
            local.set $l14
            loop $L5
              local.get $l2
              local.set $l15
              block $B6
                local.get $l4
                i32.load offset=11964
                local.get $l14
                i32.const 3
                i32.shl
                i32.add
                i32.load16_u offset=4
                local.tee $l8
                i32.eqz
                br_if $B6
                local.get $l1
                local.get $l8
                i32.add
                local.set $l9
                loop $L7
                  block $B8
                    local.get $l5
                    local.get $l1
                    i32.const 5
                    i32.shl
                    i32.add
                    local.tee $l3
                    i32.load16_u offset=22
                    i32.eqz
                    if $I9
                      local.get $l8
                      i32.const 1
                      i32.sub
                      local.set $l8
                      br $B8
                    end
                    local.get $l1
                    local.get $l2
                    i32.ne
                    if $I10
                      local.get $l5
                      local.get $l2
                      i32.const 5
                      i32.shl
                      i32.add
                      local.tee $l6
                      local.get $l3
                      i64.load align=4
                      i64.store align=4
                      local.get $l6
                      local.get $l3
                      i64.load offset=24 align=4
                      i64.store offset=24 align=4
                      local.get $l6
                      local.get $l3
                      i64.load offset=16 align=4
                      i64.store offset=16 align=4
                      local.get $l6
                      local.get $l3
                      i64.load offset=8 align=4
                      i64.store offset=8 align=4
                    end
                    local.get $l7
                    i32.const 32
                    i32.add
                    local.set $l7
                    local.get $l2
                    i32.const 1
                    i32.add
                    local.set $l2
                  end
                  local.get $l9
                  i32.const 65535
                  i32.and
                  local.get $l1
                  i32.const 1
                  i32.add
                  local.tee $l1
                  i32.const 65535
                  i32.and
                  i32.ne
                  br_if $L7
                end
                local.get $l8
                i32.const 65535
                i32.and
                local.tee $l3
                i32.eqz
                br_if $B6
                local.get $l10
                i32.const 3
                i32.shl
                local.tee $l13
                local.get $l4
                i32.load offset=11964
                i32.add
                local.get $l15
                i32.store
                local.get $l4
                i32.load offset=11964
                local.get $l13
                i32.add
                local.get $l8
                i32.store16 offset=4
                block $B11
                  local.get $l5
                  local.get $l15
                  i32.const 5
                  i32.shl
                  i32.add
                  i32.load offset=24
                  i32.load8_u
                  local.tee $l6
                  i32.const 5
                  i32.ne
                  br_if $B11
                  i32.const 5
                  local.set $l6
                  local.get $l3
                  i32.const 2
                  i32.lt_u
                  br_if $B11
                  local.get $l3
                  i32.const 1
                  i32.sub
                  local.tee $l6
                  i32.const 3
                  i32.and
                  local.set $l8
                  block $B12
                    local.get $l3
                    i32.const 2
                    i32.sub
                    i32.const 3
                    i32.lt_u
                    if $I13
                      i32.const 1
                      local.set $l3
                      i32.const 5
                      local.set $l6
                      br $B12
                    end
                    local.get $l6
                    i32.const -4
                    i32.and
                    local.set $l11
                    i32.const 1
                    local.set $l3
                    i32.const 5
                    local.set $l6
                    loop $L14
                      i32.const 1
                      i32.const 1
                      i32.const 1
                      i32.const 1
                      local.get $l6
                      local.get $l5
                      local.get $l3
                      local.get $l15
                      i32.add
                      i32.const 5
                      i32.shl
                      i32.add
                      local.tee $l9
                      i32.load offset=24
                      i32.load8_u
                      i32.const 1
                      i32.eq
                      select
                      local.get $l9
                      i32.load offset=56
                      i32.load8_u
                      i32.const 1
                      i32.eq
                      select
                      local.get $l9
                      i32.load offset=88
                      i32.load8_u
                      i32.const 1
                      i32.eq
                      select
                      local.get $l9
                      i32.load offset=120
                      i32.load8_u
                      i32.const 1
                      i32.eq
                      select
                      local.set $l6
                      local.get $l3
                      i32.const 4
                      i32.add
                      local.set $l3
                      local.get $l11
                      i32.const 4
                      i32.sub
                      local.tee $l11
                      br_if $L14
                    end
                  end
                  local.get $l8
                  i32.eqz
                  br_if $B11
                  loop $L15
                    i32.const 1
                    local.get $l6
                    local.get $l5
                    local.get $l3
                    local.get $l15
                    i32.add
                    i32.const 5
                    i32.shl
                    i32.add
                    i32.load offset=24
                    i32.load8_u
                    i32.const 1
                    i32.eq
                    select
                    local.set $l6
                    local.get $l3
                    i32.const 1
                    i32.add
                    local.set $l3
                    local.get $l8
                    i32.const 1
                    i32.sub
                    local.tee $l8
                    br_if $L15
                  end
                end
                local.get $l4
                i32.load offset=11964
                local.get $l13
                i32.add
                local.get $l6
                i32.const 255
                i32.and
                i32.store16 offset=6
                local.get $l16
                i32.const 1
                i32.add
                local.set $l16
                local.get $l10
                i32.const 1
                i32.add
                local.set $l10
              end
              local.get $l14
              i32.const 1
              i32.add
              local.tee $l14
              local.get $l17
              i32.ne
              br_if $L5
            end
            local.get $l4
            i32.load offset=11892
            local.tee $l3
            local.get $l20
            i32.add
            i32.load
            local.get $l12
            i32.add
            br $B3
          end
          local.get $l17
        end
        local.set $l12
        local.get $l3
        local.get $l20
        i32.add
        local.get $l16
        i32.store
        local.get $l19
        i32.const 1
        i32.add
        local.tee $l19
        local.get $l4
        i32.load offset=11896
        i32.lt_u
        br_if $L2
      end
    end
    local.get $l18
    local.get $l23
    i32.add
    local.set $l19
    local.get $l4
    local.get $l10
    i32.store offset=11968
    local.get $l4
    local.get $l2
    i32.store offset=12080
    local.get $l4
    local.get $l7
    local.get $l5
    i32.sub
    i32.const 5
    i32.shr_s
    local.tee $l1
    i32.store offset=11868
    local.get $l4
    local.get $l2
    local.get $l1
    i32.sub
    i32.store offset=11876
    local.get $p0
    i32.load offset=28
    local.tee $l1
    i32.load offset=112
    if $I16
      local.get $l4
      i32.const 11992
      i32.add
      i32.const 0
      i32.store
      local.get $l4
      i32.load offset=11976
      local.set $l18
      local.get $l10
      local.get $l4
      i32.const 11996
      i32.add
      i32.load
      i32.const 2147483647
      i32.and
      i32.gt_u
      if $I17
        local.get $l4
        i32.const 11988
        i32.add
        local.get $l10
        call $f71188
      end
      local.get $l4
      i32.const 11908
      i32.add
      i32.const 0
      i32.store
      local.get $l4
      i32.const 11904
      i32.add
      local.set $l20
      local.get $l4
      i32.load offset=11988
      local.set $l11
      local.get $l4
      i32.const 11900
      i32.add
      i32.load
      i32.const 2147483647
      i32.and
      local.tee $l1
      local.get $l4
      i32.const 11912
      i32.add
      i32.load
      i32.const 2147483647
      i32.and
      i32.gt_u
      if $I18
        local.get $l20
        local.get $l1
        call $f70632
      end
      i32.const 0
      local.set $l10
      block $B19
        local.get $l4
        i32.load offset=11896
        i32.eqz
        if $I20
          local.get $l18
          local.set $l1
          br $B19
        end
        local.get $l18
        local.set $l1
        i32.const 0
        local.set $l17
        i32.const 0
        local.set $l12
        i32.const 0
        local.set $l16
        loop $L21
          local.get $l12
          local.set $l13
          local.get $l17
          local.tee $l14
          local.get $l14
          local.get $l4
          i32.load offset=11892
          local.get $l16
          i32.const 2
          i32.shl
          i32.add
          i32.load
          i32.add
          local.tee $l17
          i32.lt_u
          if $I22
            loop $L23
              block $B24
                local.get $l4
                i32.load offset=11964
                local.get $l14
                i32.const 3
                i32.shl
                i32.add
                local.tee $l9
                i32.load16_u offset=6
                local.tee $l2
                i32.const 8
                i32.gt_u
                br_if $B24
                local.get $l9
                i32.load16_u offset=4
                local.set $l8
                i32.const 1
                local.get $l2
                i32.shl
                local.tee $l2
                i32.const 42
                i32.and
                i32.eqz
                if $I25
                  local.get $l2
                  i32.const 384
                  i32.and
                  i32.eqz
                  br_if $B24
                  local.get $l5
                  local.get $l9
                  i32.load
                  i32.const 5
                  i32.shl
                  i32.add
                  local.tee $l2
                  i32.load offset=24
                  local.tee $l3
                  local.get $l3
                  i32.load16_u offset=2
                  local.tee $l7
                  i32.add
                  local.tee $l3
                  i32.load8_u
                  local.set $l6
                  local.get $l2
                  i32.load16_u offset=22
                  local.set $l15
                  local.get $l1
                  local.get $l3
                  i32.store offset=24
                  local.get $l1
                  local.get $l15
                  i32.const 4
                  i32.shl
                  local.get $l7
                  i32.sub
                  i32.const 4
                  i32.shr_u
                  local.tee $l7
                  i32.store16 offset=22
                  local.get $l1
                  local.get $l2
                  i32.load
                  i32.store
                  local.get $l1
                  local.get $l2
                  i32.load offset=4
                  i32.store offset=4
                  local.get $l1
                  local.get $l2
                  i32.load offset=12
                  i32.store offset=12
                  local.get $l1
                  local.get $l2
                  i32.load offset=16
                  i32.store offset=16
                  local.get $l1
                  local.get $l2
                  i32.load16_u offset=8
                  i32.store16 offset=8
                  local.get $l2
                  i32.load16_u offset=10
                  local.set $l2
                  local.get $l1
                  i32.const 0
                  i32.store offset=28
                  local.get $l1
                  local.get $l2
                  i32.store16 offset=10
                  local.get $l1
                  i32.const 0
                  i32.store16 offset=20
                  local.get $l9
                  i32.load
                  local.set $l2
                  local.get $l1
                  local.get $l3
                  i32.store offset=56
                  local.get $l1
                  local.get $l7
                  i32.store16 offset=54
                  local.get $l1
                  local.get $l2
                  i32.const 5
                  i32.shl
                  local.get $l5
                  i32.add
                  local.tee $l2
                  i32.load offset=32
                  i32.store offset=32
                  local.get $l1
                  local.get $l2
                  i32.load offset=36
                  i32.store offset=36
                  local.get $l1
                  local.get $l2
                  i32.load offset=44
                  i32.store offset=44
                  local.get $l1
                  local.get $l2
                  i32.load offset=48
                  i32.store offset=48
                  local.get $l1
                  local.get $l2
                  i32.load16_u offset=40
                  i32.store16 offset=40
                  local.get $l2
                  i32.load16_u offset=42
                  local.set $l2
                  local.get $l1
                  i32.const 0
                  i32.store offset=60
                  local.get $l1
                  local.get $l2
                  i32.store16 offset=42
                  local.get $l1
                  i32.const 0
                  i32.store16 offset=52
                  local.get $l9
                  i32.load
                  local.set $l2
                  local.get $l1
                  local.get $l3
                  i32.store offset=88
                  local.get $l1
                  local.get $l7
                  i32.store16 offset=86
                  local.get $l1
                  local.get $l2
                  i32.const 5
                  i32.shl
                  local.get $l5
                  i32.add
                  local.tee $l2
                  i32.const -64
                  i32.sub
                  i32.load
                  i32.store offset=64
                  local.get $l1
                  local.get $l2
                  i32.load offset=68
                  i32.store offset=68
                  local.get $l1
                  local.get $l2
                  i32.load offset=76
                  i32.store offset=76
                  local.get $l1
                  local.get $l2
                  i32.load offset=80
                  i32.store offset=80
                  local.get $l1
                  local.get $l2
                  i32.load16_u offset=72
                  i32.store16 offset=72
                  local.get $l2
                  i32.load16_u offset=74
                  local.set $l2
                  local.get $l1
                  i32.const 0
                  i32.store offset=92
                  local.get $l1
                  local.get $l2
                  i32.store16 offset=74
                  local.get $l1
                  i32.const 0
                  i32.store16 offset=84
                  local.get $l9
                  i32.load
                  local.set $l2
                  local.get $l1
                  local.get $l3
                  i32.store offset=120
                  local.get $l1
                  local.get $l7
                  i32.store16 offset=118
                  local.get $l1
                  local.get $l2
                  i32.const 5
                  i32.shl
                  local.get $l5
                  i32.add
                  local.tee $l2
                  i32.load offset=96
                  i32.store offset=96
                  local.get $l1
                  local.get $l2
                  i32.load offset=100
                  i32.store offset=100
                  local.get $l1
                  local.get $l2
                  i32.load offset=108
                  i32.store offset=108
                  local.get $l1
                  local.get $l2
                  i32.load offset=112
                  i32.store offset=112
                  local.get $l1
                  local.get $l2
                  i32.load16_u offset=104
                  i32.store16 offset=104
                  local.get $l2
                  i32.load16_u offset=106
                  local.set $l2
                  local.get $l1
                  i32.const 0
                  i32.store offset=124
                  local.get $l1
                  local.get $l2
                  i32.store16 offset=106
                  local.get $l1
                  i32.const 0
                  i32.store16 offset=116
                  local.get $l11
                  local.get $l6
                  i32.store16 offset=6
                  local.get $l11
                  local.get $l8
                  i32.store16 offset=4
                  local.get $l11
                  local.get $l10
                  i32.store
                  local.get $l8
                  local.get $l10
                  i32.add
                  local.set $l10
                  local.get $l13
                  i32.const 1
                  i32.add
                  local.set $l13
                  local.get $l11
                  i32.const 8
                  i32.add
                  local.set $l11
                  local.get $l1
                  i32.const 128
                  i32.add
                  local.set $l1
                  br $B24
                end
                local.get $l11
                block $B26 (result i32)
                  local.get $l8
                  i32.eqz
                  if $I27
                    local.get $l10
                    local.set $l3
                    i32.const 0
                    br $B26
                  end
                  i32.const 0
                  local.set $l3
                  loop $L28
                    local.get $l5
                    local.get $l9
                    i32.load
                    local.get $l3
                    i32.add
                    i32.const 5
                    i32.shl
                    i32.add
                    local.tee $l2
                    i32.load16_u offset=22
                    local.set $l7
                    local.get $l1
                    local.get $l2
                    i32.load offset=24
                    local.tee $l6
                    local.get $l6
                    i32.load16_u offset=2
                    local.tee $l6
                    i32.add
                    local.tee $l15
                    i32.store offset=24
                    local.get $l1
                    local.get $l7
                    i32.const 4
                    i32.shl
                    local.get $l6
                    i32.sub
                    i32.const 4
                    i32.shr_u
                    i32.store16 offset=22
                    local.get $l1
                    local.get $l2
                    i32.load
                    i32.store
                    local.get $l1
                    local.get $l2
                    i32.load offset=4
                    i32.store offset=4
                    local.get $l1
                    local.get $l2
                    i32.load offset=12
                    i32.store offset=12
                    local.get $l1
                    local.get $l2
                    i32.load offset=16
                    i32.store offset=16
                    local.get $l1
                    local.get $l2
                    i32.load16_u offset=8
                    i32.store16 offset=8
                    local.get $l2
                    i32.load16_u offset=10
                    local.set $l2
                    local.get $l1
                    i32.const 0
                    i32.store offset=28
                    local.get $l1
                    local.get $l2
                    i32.store16 offset=10
                    local.get $l1
                    i32.const 0
                    i32.store16 offset=20
                    local.get $l1
                    i32.const 32
                    i32.add
                    local.set $l1
                    local.get $l3
                    i32.const 1
                    i32.add
                    local.tee $l3
                    local.get $l8
                    i32.ne
                    br_if $L28
                  end
                  local.get $l8
                  local.get $l10
                  i32.add
                  local.set $l3
                  local.get $l15
                  i32.load8_u
                end
                i32.store16 offset=6
                local.get $l11
                local.get $l8
                i32.store16 offset=4
                local.get $l11
                local.get $l10
                i32.store
                local.get $l13
                i32.const 1
                i32.add
                local.set $l13
                local.get $l11
                i32.const 8
                i32.add
                local.set $l11
                local.get $l3
                local.set $l10
              end
              local.get $l14
              i32.const 1
              i32.add
              local.tee $l14
              local.get $l17
              i32.ne
              br_if $L23
            end
            block $B29
              local.get $l12
              local.get $l13
              i32.ge_u
              br_if $B29
              local.get $l21
              local.get $l13
              local.get $l12
              i32.sub
              local.tee $l2
              i32.store offset=12
              local.get $l4
              i32.load offset=11908
              local.tee $l3
              local.get $l4
              i32.load offset=11912
              i32.const 2147483647
              i32.and
              i32.ge_u
              if $I30
                local.get $l20
                local.get $l21
                i32.const 12
                i32.add
                call $f72545
                br $B29
              end
              local.get $l4
              i32.load offset=11904
              local.get $l3
              i32.const 2
              i32.shl
              i32.add
              local.get $l2
              i32.store
              local.get $l4
              local.get $l4
              i32.load offset=11908
              i32.const 1
              i32.add
              i32.store offset=11908
            end
            local.get $l13
            local.set $l12
          end
          local.get $l16
          i32.const 1
          i32.add
          local.tee $l16
          local.get $l4
          i32.load offset=11896
          i32.lt_u
          br_if $L21
        end
      end
      local.get $l4
      local.get $l10
      i32.store offset=12084
      local.get $l4
      local.get $l1
      local.get $l18
      i32.sub
      i32.const 5
      i32.shr_s
      local.tee $l1
      i32.store offset=11872
      local.get $l4
      local.get $l11
      local.get $l4
      i32.load offset=11988
      i32.sub
      i32.const 3
      i32.shr_s
      i32.store offset=11992
      local.get $l4
      local.get $l10
      local.get $l1
      i32.sub
      i32.store offset=11884
      local.get $p0
      i32.load offset=28
      local.set $l1
    end
    local.get $l4
    i32.load offset=11976
    local.set $l5
    local.get $l4
    i32.load offset=11960
    local.set $l7
    local.get $l1
    i32.load offset=584
    local.tee $l3
    i32.load
    drop
    local.get $l3
    i32.const 156
    call $f72200
    local.set $l2
    local.get $l3
    i32.load
    drop
    local.get $l2
    local.get $l4
    i32.load offset=12112
    i32.store
    local.get $l4
    i32.load offset=12116
    local.set $l3
    local.get $l2
    local.get $l22
    i32.store offset=12
    local.get $l2
    local.get $l19
    i32.store offset=8
    local.get $l2
    local.get $l3
    i32.store offset=4
    local.get $l2
    local.get $p0
    i32.load offset=92
    i32.store offset=20
    local.get $l2
    local.get $p0
    i32.load offset=32
    i32.load offset=4
    i32.store offset=16
    local.get $l2
    local.get $l4
    i32.load offset=12144
    i32.store offset=24
    local.get $l4
    i32.const 12148
    i32.add
    i32.load
    local.set $l3
    local.get $l2
    i64.const 0
    i64.store offset=68 align=4
    local.get $l2
    local.get $l7
    i32.store offset=32
    local.get $l2
    local.get $l3
    i32.store offset=28
    local.get $l2
    i64.const 0
    i64.store offset=76 align=4
    local.get $l2
    i64.const 0
    i64.store offset=84 align=4
    local.get $l2
    i32.const 0
    i32.store offset=92
    local.get $l2
    local.get $p0
    i32.load offset=28
    i32.load offset=4
    i32.load offset=4
    i32.store offset=132
    local.get $p0
    i32.load offset=28
    i32.load offset=4
    i32.load offset=8
    local.set $l3
    local.get $l2
    local.get $l1
    i32.const 536
    i32.add
    i32.store offset=140
    local.get $l2
    local.get $l3
    i32.store offset=136
    local.get $l2
    local.get $l4
    i32.load offset=11940
    i32.store offset=52
    local.get $l4
    i32.load offset=11928
    local.set $l1
    local.get $l2
    i32.const 0
    i32.store offset=96
    local.get $l2
    local.get $l1
    i32.store offset=60
    local.get $l2
    local.get $l4
    i32.load offset=11964
    i32.store offset=36
    local.get $l2
    local.get $l4
    i32.load offset=11968
    i32.store offset=40
    local.get $l2
    local.get $l4
    i32.load offset=11892
    i32.store offset=44
    local.get $l2
    local.get $l4
    i32.load offset=11896
    i32.store offset=48
    local.get $l2
    local.get $p0
    i32.load offset=36
    i32.store offset=64
    local.get $l2
    local.get $l4
    i32.load offset=11904
    i32.store offset=120
    local.get $l2
    local.get $l4
    i32.const 11908
    i32.add
    i32.load
    i32.store offset=124
    local.get $l2
    local.get $l4
    i32.load offset=11988
    i32.store offset=112
    local.get $l4
    i32.const 11992
    i32.add
    i32.load
    local.set $l1
    local.get $l2
    i32.const 0
    i32.store offset=128
    local.get $l2
    local.get $l1
    i32.store offset=116
    local.get $l2
    local.get $l5
    i32.store offset=108
    local.get $l2
    local.get $l4
    i32.load offset=12128
    i32.store offset=144
    local.get $l2
    local.get $p0
    i32.load offset=28
    f32.load offset=52
    f32.store offset=100
    local.get $l2
    local.get $p0
    i32.load offset=28
    f32.load offset=56
    f32.store offset=104
    local.get $l4
    i32.load offset=12104
    local.set $l3
    local.get $p0
    i32.load offset=16
    local.tee $l1
    local.get $l1
    i32.load
    i32.load offset=4
    call_indirect $__indirect_function_table (type $t5)
    local.tee $l1
    local.get $l1
    i32.load
    i32.load offset=4
    call_indirect $__indirect_function_table (type $t5)
    local.set $l1
    block $B31
      local.get $l3
      i32.const 3
      i32.shl
      local.tee $l3
      i32.const 1
      local.get $l3
      select
      local.tee $l3
      local.get $l4
      i32.load offset=11968
      i32.add
      i32.const 1
      i32.sub
      local.get $l3
      i32.div_u
      local.tee $l3
      local.get $l1
      local.get $l1
      local.get $l3
      i32.gt_u
      select
      local.tee $l1
      i32.const 2
      i32.ge_u
      if $I32
        local.get $l2
        local.get $l3
        i32.const 3
        i32.shl
        local.get $l1
        i32.const 1
        local.get $l1
        i32.const 1
        i32.gt_u
        select
        local.tee $l9
        i32.const 1
        i32.shl
        i32.div_u
        local.tee $l1
        i32.const 8
        local.get $l1
        i32.const 8
        i32.gt_u
        select
        i32.store offset=56
        i32.const 1
        local.set $l7
        loop $L33
          local.get $p0
          i32.load offset=28
          i32.load offset=584
          local.tee $l3
          i32.load
          drop
          local.get $l3
          i32.const 48
          call $f72200
          local.set $l1
          local.get $l3
          i32.load
          drop
          local.get $p0
          i32.load offset=28
          local.tee $l3
          i32.load offset=112
          local.set $l5
          local.get $p0
          i32.load offset=96
          local.set $l6
          local.get $l3
          i64.load offset=600
          local.set $l24
          local.get $l1
          i32.const 0
          i32.store offset=24
          local.get $l1
          i64.const 0
          i64.store offset=16
          local.get $l1
          local.get $l24
          i64.store offset=8
          local.get $l1
          local.get $l6
          i32.store offset=40
          local.get $l1
          local.get $l5
          i32.store offset=36
          local.get $l1
          local.get $l3
          i32.store offset=32
          local.get $l1
          local.get $l2
          i32.store offset=28
          local.get $l1
          i32.const 3152164
          i32.store
          local.get $l1
          local.get $p0
          i32.load offset=20
          local.tee $l3
          i32.store offset=20
          local.get $l1
          i32.const 1
          i32.store offset=24
          local.get $l1
          local.get $l3
          if $I34 (result i32)
            local.get $l3
            local.get $l3
            i32.load
            i32.load offset=16
            call_indirect $__indirect_function_table (type $t7)
            local.get $l1
            local.get $l1
            i32.load offset=20
            i32.load offset=16
            i32.store offset=16
            local.get $l1
            i32.load
          else
            i32.const 3152164
          end
          i32.load offset=20
          call_indirect $__indirect_function_table (type $t7)
          local.get $l7
          i32.const 1
          i32.add
          local.tee $l7
          local.get $l9
          i32.ne
          br_if $L33
        end
        local.get $p0
        i32.load offset=28
        local.get $l2
        local.get $p0
        i32.load offset=96
        call $f71196
        local.get $p0
        i32.load offset=32
        local.tee $l1
        i32.load offset=8
        i32.const 2147483647
        i32.and
        local.get $l1
        i32.load offset=4
        i32.add
        local.tee $l3
        local.get $l2
        i32.load offset=96
        i32.le_s
        br_if $B31
        local.get $l2
        i32.load offset=96
        local.get $l3
        i32.ge_s
        br_if $B31
        i32.const 30000
        local.set $l1
        loop $L35
          local.get $l2
          i32.load offset=96
          local.get $l3
          i32.ge_s
          br_if $B31
          local.get $l1
          i32.const 1
          i32.sub
          local.tee $l1
          br_if $L35
          i32.const 10000
          local.set $l1
          br $L35
        end
        unreachable
      end
      local.get $l4
      i32.const 12052
      i32.add
      i32.const 0
      i32.store
      local.get $l4
      i32.load offset=12128
      local.tee $l1
      local.get $l4
      i32.const 12056
      i32.add
      i32.load
      i32.const 2147483647
      i32.and
      i32.gt_u
      if $I36
        local.get $l4
        i32.const 12048
        i32.add
        local.get $l1
        call $f71197
        local.get $l4
        i32.load offset=12128
        local.set $l1
      end
      local.get $l4
      local.get $l1
      i32.store offset=12052
      i32.const 0
      local.set $l5
      local.get $l4
      i32.const 12064
      i32.add
      i32.const 0
      i32.store
      local.get $l4
      local.get $l1
      local.get $l4
      i32.const 12068
      i32.add
      i32.load
      i32.const 2147483647
      i32.and
      i32.gt_u
      if $I37 (result i32)
        local.get $l4
        i32.const 12060
        i32.add
        local.get $l1
        call $f71197
        local.get $l4
        i32.load offset=12128
      else
        local.get $l1
      end
      i32.store offset=12064
      local.get $l2
      local.get $l4
      i32.load offset=12048
      i32.store offset=148
      local.get $l2
      local.get $l4
      i32.load offset=12060
      i32.store offset=152
      local.get $p0
      i32.load offset=28
      local.tee $l1
      local.get $l1
      i32.load offset=112
      i32.const 2
      i32.shl
      i32.add
      i32.load offset=484
      local.tee $l12
      local.get $l2
      local.get $l12
      i32.load
      i32.load offset=16
      call_indirect $__indirect_function_table (type $t1)
      local.get $p0
      i32.load offset=32
      local.tee $l2
      i32.load offset=4
      if $I38
        local.get $l22
        local.get $p0
        i32.load offset=92
        i32.const 112
        i32.mul
        i32.add
        i32.const 112
        i32.add
        local.set $l8
        loop $L39
          local.get $l5
          i32.const 5
          i32.shl
          local.tee $l7
          local.get $l4
          i32.load offset=11940
          i32.add
          local.tee $l1
          local.get $l1
          i32.const 16
          i32.add
          local.get $l7
          local.get $l19
          i32.add
          local.get $l8
          local.get $l5
          i32.const 112
          i32.mul
          i32.add
          local.tee $l2
          local.get $p0
          i32.load offset=28
          f32.load offset=52
          call $f71198
          local.get $l5
          i32.const 2
          i32.shl
          local.tee $l6
          local.get $p0
          i32.load offset=36
          i32.add
          i32.load
          local.tee $l3
          local.get $l3
          i32.load offset=36
          local.tee $l1
          f32.load
          f32.store
          local.get $l3
          local.get $l1
          f32.load offset=4
          f32.store offset=4
          local.get $l3
          local.get $l1
          f32.load offset=8
          f32.store offset=8
          local.get $l3
          local.get $l1
          f32.load offset=12
          f32.store offset=12
          local.get $l3
          local.get $l1
          f32.load offset=16
          f32.store offset=16
          local.get $l3
          local.get $l1
          i32.const 20
          i32.add
          local.tee $l9
          f32.load
          f32.store offset=20
          local.get $l3
          local.get $l1
          i32.const 24
          i32.add
          local.tee $l3
          f32.load
          f32.store offset=24
          local.get $l1
          local.get $l2
          f32.load offset=80
          f32.store
          local.get $l1
          local.get $l2
          f32.load offset=84
          f32.store offset=4
          local.get $l1
          local.get $l2
          f32.load offset=88
          f32.store offset=8
          local.get $l1
          local.get $l2
          f32.load offset=92
          f32.store offset=12
          local.get $l1
          local.get $l2
          f32.load offset=96
          f32.store offset=16
          local.get $l9
          local.get $l2
          f32.load offset=100
          f32.store
          local.get $l3
          local.get $l2
          f32.load offset=104
          f32.store
          local.get $l1
          local.get $l2
          f32.load
          f32.store offset=64
          local.get $l1
          local.get $l2
          f32.load offset=4
          f32.store offset=68
          local.get $l1
          local.get $l2
          f32.load offset=8
          f32.store offset=72
          local.get $l1
          local.get $l2
          f32.load offset=16
          f32.store offset=80
          local.get $l1
          local.get $l2
          f32.load offset=20
          f32.store offset=84
          local.get $l1
          local.get $l2
          f32.load offset=24
          f32.store offset=88
          local.get $p0
          i32.load offset=36
          local.get $l6
          i32.add
          i32.load
          local.tee $l1
          local.get $p0
          i32.load offset=28
          local.tee $l3
          f32.load offset=52
          local.get $l3
          f32.load offset=56
          local.get $l3
          i32.load8_u offset=64
          local.get $l3
          i32.load8_u offset=66
          local.get $l4
          i32.load offset=11940
          local.get $l7
          i32.add
          local.get $p0
          i32.load offset=96
          local.tee $l3
          i32.load offset=100
          local.get $l3
          i32.load offset=204
          local.get $l2
          i32.load offset=72
          i32.const 2
          i32.shl
          i32.add
          i32.load
          i32.const 2
          i32.shl
          i32.add
          i32.load
          i32.const 0
          i32.ne
          call $f71199
          f32.const 0x0p+0 (;=0;)
          f32.eq
          if $I40
            local.get $l1
            i64.const 0
            i64.store offset=64 align=4
            local.get $l1
            i64.const 0
            i64.store offset=48 align=4
            local.get $l1
            i32.const 0
            i32.store offset=72
            local.get $l1
            i32.const 0
            i32.store offset=56
            local.get $l1
            local.get $l1
            i32.load16_u offset=28
            i32.const 16
            i32.or
            i32.store16 offset=28
          end
          local.get $l5
          i32.const 1
          i32.add
          local.tee $l5
          local.get $p0
          i32.load offset=32
          local.tee $l2
          i32.load offset=4
          i32.lt_u
          br_if $L39
        end
      end
      local.get $l2
      i32.load offset=8
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if $B31
      i32.const 0
      local.set $l1
      loop $L41
        local.get $l4
        i32.load offset=12144
        local.get $l1
        i32.const 56
        i32.mul
        i32.add
        local.tee $l3
        i32.load
        i32.load offset=24
        i32.const 2
        i32.shl
        i32.const 4701972
        i32.add
        i32.load
        local.tee $l5
        if $I42
          local.get $l3
          local.get $p0
          i32.load offset=28
          f32.load offset=52
          local.get $l5
          call_indirect $__indirect_function_table (type $t21)
          local.get $p0
          i32.load offset=32
          local.set $l2
        end
        local.get $l1
        i32.const 1
        i32.add
        local.tee $l1
        local.get $l2
        i32.load offset=8
        i32.const 2147483647
        i32.and
        i32.lt_u
        br_if $L41
      end
    end
    local.get $l21
    i32.const 16
    i32.add
    global.set $g0)