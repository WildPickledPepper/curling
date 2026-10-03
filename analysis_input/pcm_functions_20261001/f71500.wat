  (func $f71500 (type $t7) (param $p0 i32)
    (local $l1 i32) (local $l2 i32) (local $l3 i32) (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 f32) (local $l9 f32) (local $l10 f32) (local $l11 f32) (local $l12 f32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 f32) (local $l28 f32) (local $l29 f32)
    local.get $p0
    i32.load offset=36
    if $I0
      loop $L1
        local.get $p0
        i32.load offset=28
        i32.load offset=16
        local.get $p0
        i32.load offset=32
        local.get $l7
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
        i32.load offset=16
        local.set $l2
        local.get $p0
        f32.load offset=40
        local.set $l25
        f32.const 0x0p+0 (;=0;)
        local.set $l15
        global.get $g0
        i32.const 32
        i32.sub
        local.tee $l4
        global.set $g0
        block $B2
          local.get $l2
          i32.load offset=28
          i32.eqz
          br_if $B2
          local.get $l2
          i32.load offset=24
          i32.load
          i32.load offset=156
          i32.const -3
          i32.gt_u
          br_if $B2
          local.get $l2
          i32.load offset=8
          local.set $l3
          block $B3
            local.get $l2
            i32.load offset=16
            if $I4
              local.get $l3
              f32.load offset=24
              local.set $l29
              i32.const 0
              local.set $l3
              f32.const 0x1.fffffep+127 (;=3.40282e+38;)
              local.set $l17
              loop $L5
                local.get $l4
                local.get $l2
                i32.load
                local.tee $l1
                local.get $l3
                local.get $l1
                i32.load
                i32.load offset=184
                call_indirect $__indirect_function_table (type $t2)
                local.get $l17
                block $B6 (result f32)
                  local.get $l2
                  i32.load offset=24
                  local.get $l3
                  i32.const 2
                  i32.shl
                  i32.add
                  i32.load
                  local.tee $l1
                  f32.load offset=136
                  local.set $l8
                  local.get $l1
                  f32.load offset=132
                  local.set $l18
                  local.get $l1
                  f32.load offset=128
                  local.set $l19
                  local.get $l1
                  f32.load offset=120
                  local.set $l20
                  local.get $l1
                  f32.load offset=116
                  local.set $l21
                  local.get $l1
                  f32.load offset=112
                  local.set $l22
                  block $B7
                    block $B8
                      local.get $l1
                      i32.load offset=44
                      local.tee $l5
                      f32.load offset=156
                      local.tee $l26
                      f32.const 0x1.999998p-3 (;=0.2;)
                      f32.lt
                      local.get $l25
                      local.get $l26
                      f32.gt
                      i32.or
                      i32.eqz
                      br_if $B8
                      local.get $l5
                      call $f71608
                      local.set $l6
                      local.get $l5
                      f32.load offset=28
                      local.set $l9
                      local.get $l4
                      f32.load offset=20
                      local.set $l10
                      local.get $l4
                      f32.load offset=24
                      local.set $l11
                      local.get $l5
                      f32.load offset=16
                      local.set $l12
                      local.get $l5
                      f32.load offset=24
                      local.set $l13
                      local.get $l4
                      f32.load offset=16
                      local.set $l14
                      local.get $l5
                      f32.load offset=20
                      local.set $l23
                      local.get $l6
                      f32.load offset=4
                      local.set $l27
                      local.get $l6
                      f32.load
                      local.set $l28
                      local.get $l6
                      f32.load offset=8
                      local.set $l16
                      local.get $l22
                      local.get $l4
                      f32.load
                      f32.add
                      local.tee $l22
                      local.get $l22
                      f32.mul
                      local.get $l21
                      local.get $l4
                      f32.load offset=4
                      f32.add
                      local.tee $l21
                      local.get $l21
                      f32.mul
                      f32.add
                      local.get $l20
                      local.get $l4
                      f32.load offset=8
                      f32.add
                      local.tee $l20
                      local.get $l20
                      f32.mul
                      f32.add
                      f32.const 0x1p+0 (;=1;)
                      local.get $l5
                      call $f71606
                      local.tee $l24
                      local.get $l24
                      f32.const 0x0p+0 (;=0;)
                      f32.eq
                      select
                      f32.const 0x1p+0 (;=1;)
                      local.get $l16
                      f32.div
                      f32.const 0x1p+0 (;=1;)
                      local.get $l16
                      f32.const 0x0p+0 (;=0;)
                      f32.gt
                      select
                      local.get $l8
                      local.get $l11
                      local.get $l11
                      f32.add
                      local.tee $l11
                      local.get $l9
                      local.get $l9
                      f32.mul
                      f32.const -0x1p-1 (;=-0.5;)
                      f32.add
                      local.tee $l16
                      f32.mul
                      local.get $l9
                      local.get $l12
                      local.get $l10
                      local.get $l10
                      f32.add
                      local.tee $l10
                      f32.mul
                      local.get $l23
                      local.get $l14
                      local.get $l14
                      f32.add
                      local.tee $l14
                      f32.mul
                      f32.sub
                      f32.mul
                      f32.sub
                      local.get $l13
                      local.get $l14
                      local.get $l12
                      f32.mul
                      local.get $l10
                      local.get $l23
                      f32.mul
                      f32.add
                      local.get $l11
                      local.get $l13
                      f32.mul
                      f32.add
                      local.tee $l24
                      f32.mul
                      f32.add
                      f32.add
                      local.tee $l8
                      local.get $l8
                      f32.mul
                      f32.mul
                      f32.const 0x1p+0 (;=1;)
                      local.get $l28
                      f32.div
                      f32.const 0x1p+0 (;=1;)
                      local.get $l28
                      f32.const 0x0p+0 (;=0;)
                      f32.gt
                      select
                      local.get $l19
                      local.get $l12
                      local.get $l24
                      f32.mul
                      local.get $l14
                      local.get $l16
                      f32.mul
                      local.get $l9
                      local.get $l11
                      local.get $l23
                      f32.mul
                      local.get $l10
                      local.get $l13
                      f32.mul
                      f32.sub
                      f32.mul
                      f32.sub
                      f32.add
                      f32.add
                      local.tee $l19
                      local.get $l19
                      f32.mul
                      f32.mul
                      f32.const 0x1p+0 (;=1;)
                      local.get $l27
                      f32.div
                      f32.const 0x1p+0 (;=1;)
                      local.get $l27
                      f32.const 0x0p+0 (;=0;)
                      f32.gt
                      select
                      local.get $l18
                      local.get $l23
                      local.get $l24
                      f32.mul
                      local.get $l10
                      local.get $l16
                      f32.mul
                      local.get $l9
                      local.get $l14
                      local.get $l13
                      f32.mul
                      local.get $l11
                      local.get $l12
                      f32.mul
                      f32.sub
                      f32.mul
                      f32.sub
                      f32.add
                      f32.add
                      local.tee $l18
                      local.get $l18
                      f32.mul
                      f32.mul
                      f32.add
                      f32.add
                      f32.mul
                      f32.add
                      f32.const 0x1p-1 (;=0.5;)
                      f32.mul
                      local.tee $l13
                      local.get $l1
                      i32.load offset=100
                      i32.load offset=148
                      i32.const 1
                      i32.add
                      f32.convert_i32_u
                      local.tee $l12
                      local.get $l29
                      f32.mul
                      local.tee $l9
                      f32.ge
                      i32.eqz
                      br_if $B8
                      local.get $l1
                      i32.const 0
                      i32.store offset=136
                      local.get $l1
                      i64.const 0
                      i64.store offset=128 align=4
                      local.get $l1
                      i32.const 0
                      i32.store offset=120
                      local.get $l1
                      i64.const 0
                      i64.store offset=112 align=4
                      local.get $l5
                      local.get $l12
                      f32.const -0x1p+0 (;=-1;)
                      f32.add
                      local.get $l25
                      f32.mul
                      local.get $l9
                      f32.const 0x0p+0 (;=0;)
                      f32.ne
                      if $I9 (result f32)
                        local.get $l13
                        local.get $l9
                        f32.div
                        local.tee $l8
                        f32.const 0x1p+1 (;=2;)
                        local.get $l8
                        f32.const 0x1p+1 (;=2;)
                        f32.lt
                        select
                        f32.const 0x1p-1 (;=0.5;)
                        f32.mul
                        f32.const 0x1.999998p-2 (;=0.4;)
                        f32.mul
                      else
                        f32.const 0x1.999998p-2 (;=0.4;)
                      end
                      f32.add
                      local.tee $l8
                      f32.store offset=156
                      local.get $l26
                      f32.const 0x0p+0 (;=0;)
                      f32.ne
                      br_if $B7
                      local.get $l1
                      i32.load offset=40
                      i32.load offset=1000
                      local.get $l1
                      i64.load offset=144
                      call $f70712
                      local.get $l8
                      br $B6
                    end
                    local.get $l1
                    local.get $l8
                    f32.store offset=136
                    local.get $l1
                    local.get $l18
                    f32.store offset=132
                    local.get $l1
                    local.get $l19
                    f32.store offset=128
                    local.get $l1
                    local.get $l20
                    f32.store offset=120
                    local.get $l1
                    local.get $l21
                    f32.store offset=116
                    local.get $l1
                    local.get $l22
                    f32.store offset=112
                    local.get $l5
                    local.get $l26
                    local.get $l25
                    f32.sub
                    local.tee $l8
                    f32.const 0x0p+0 (;=0;)
                    local.get $l8
                    f32.const 0x0p+0 (;=0;)
                    f32.gt
                    select
                    local.tee $l8
                    f32.store offset=156
                  end
                  local.get $l8
                end
                local.tee $l8
                local.get $l8
                local.get $l17
                f32.gt
                select
                local.set $l17
                local.get $l15
                local.get $l8
                local.get $l8
                local.get $l15
                f32.lt
                select
                local.set $l15
                local.get $l3
                i32.const 1
                i32.add
                local.tee $l3
                local.get $l2
                i32.load offset=16
                i32.lt_u
                br_if $L5
              end
              local.get $l2
              i32.load offset=8
              local.get $l15
              f32.store offset=32
              local.get $l15
              f32.const 0x0p+0 (;=0;)
              f32.eq
              br_if $B3
              local.get $l17
              f32.const 0x0p+0 (;=0;)
              f32.ne
              br_if $B2
              local.get $l2
              i32.load offset=16
              i32.eqz
              br_if $B2
              i32.const 0
              local.set $l3
              loop $L10
                local.get $l2
                i32.load offset=24
                local.get $l3
                i32.const 2
                i32.shl
                i32.add
                i32.load
                i32.load offset=44
                i32.const 156
                i32.add
                local.tee $l1
                local.get $l1
                f32.load
                f32.const 0x1.0c6f7ap-20 (;=1e-06;)
                f32.max
                f32.store
                local.get $l3
                i32.const 1
                i32.add
                local.tee $l3
                local.get $l2
                i32.load offset=16
                i32.lt_u
                br_if $L10
              end
              br $B2
            end
            local.get $l3
            i32.const 0
            i32.store offset=32
          end
          local.get $l2
          i32.load offset=16
          if $I11
            i32.const 0
            local.set $l3
            loop $L12
              local.get $l3
              i32.const 2
              i32.shl
              local.tee $l1
              local.get $l2
              i32.load offset=24
              i32.add
              i32.load
              call $f71567
              local.get $l2
              i32.load offset=24
              local.get $l1
              i32.add
              i32.load
              local.tee $l1
              i32.const 0
              i32.store offset=136
              local.get $l1
              i64.const 0
              i64.store offset=128 align=4
              local.get $l1
              i32.const 0
              i32.store offset=120
              local.get $l1
              i64.const 0
              i64.store offset=112 align=4
              local.get $l3
              i32.const 1
              i32.add
              local.tee $l3
              local.get $l2
              i32.load offset=16
              i32.lt_u
              br_if $L12
            end
          end
          local.get $l2
          i32.load offset=4
          i32.load offset=1000
          local.get $l2
          i64.load offset=48
          call $f70713
        end
        local.get $l4
        i32.const 32
        i32.add
        global.set $g0
        local.get $l2
        i32.const 0
        call $f71658
        local.get $l7
        i32.const 1
        i32.add
        local.tee $l7
        local.get $p0
        i32.load offset=36
        i32.lt_u
        br_if $L1
      end
    end)
