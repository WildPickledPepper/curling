  (func $f71871 (type $t9) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (result i32)
    (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32)
    global.get $g0
    i32.const 1184
    i32.sub
    local.tee $l5
    global.set $g0
    local.get $l5
    i32.const 1
    i32.store8 offset=1168
    local.get $l5
    i64.const 1099511628032
    i64.store offset=1176
    local.get $l5
    local.get $l5
    i32.const 144
    i32.add
    i32.store offset=1172
    local.get $l5
    local.get $p2
    i32.load offset=8
    local.tee $l12
    i32.store offset=144
    loop $L0
      local.get $l5
      i32.load offset=1172
      local.get $l7
      i32.const 2
      i32.shl
      i32.add
      i32.load
      local.tee $l6
      f32.load
      local.tee $l14
      local.get $l6
      f32.load offset=12
      local.tee $l15
      f32.add
      local.set $l18
      local.get $l15
      local.get $l14
      f32.sub
      local.set $l14
      local.get $l6
      f32.load offset=8
      local.tee $l16
      local.get $l6
      f32.load offset=20
      local.tee $l17
      f32.add
      local.set $l15
      local.get $l6
      f32.load offset=4
      local.tee $l20
      local.get $l6
      f32.load offset=16
      local.tee $l21
      f32.add
      local.set $l19
      local.get $l17
      local.get $l16
      f32.sub
      local.set $l16
      local.get $l21
      local.get $l20
      f32.sub
      local.set $l17
      loop $L1
        block $B2
          local.get $l5
          local.get $l19
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=132
          local.get $l5
          local.get $l18
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=128
          local.get $l5
          i32.const 0
          i32.store offset=140
          local.get $l5
          local.get $l15
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=136
          local.get $l5
          local.get $l17
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=116
          local.get $l5
          local.get $l14
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=112
          local.get $l5
          i32.const 0
          i32.store offset=124
          local.get $l5
          local.get $l16
          f32.const 0x1p-1 (;=0.5;)
          f32.mul
          f32.store offset=120
          local.get $l5
          local.get $l5
          i64.load offset=128
          i64.store offset=48
          local.get $l5
          local.get $l5
          i64.load offset=136
          i64.store offset=56
          local.get $l5
          local.get $l5
          i64.load offset=112
          i64.store offset=32
          local.get $l5
          local.get $l5
          i64.load offset=120
          i64.store offset=40
          block $B3
            block $B4
              local.get $p3
              local.get $l5
              i32.const 48
              i32.add
              local.get $l5
              i32.const 32
              i32.add
              call $f71852
              i32.eqz
              br_if $B4
              local.get $l6
              i32.load offset=24
              local.tee $l6
              i32.const 1
              i32.shr_u
              local.set $l8
              local.get $l6
              i32.const 1
              i32.and
              i32.eqz
              br_if $B3
              local.get $l8
              i32.const 15
              i32.and
              local.tee $l9
              i32.eqz
              br_if $B4
              local.get $p2
              i32.load
              local.get $l6
              i32.const 3
              i32.shr_u
              i32.const 536870908
              i32.and
              i32.add
              local.set $l6
              local.get $l9
              local.set $l10
              loop $L5
                local.get $l6
                i32.load
                local.set $l11
                block $B6
                  local.get $l9
                  i32.const 2
                  i32.ge_u
                  if $I7
                    local.get $p1
                    local.get $l11
                    i32.const 24
                    i32.mul
                    i32.add
                    local.tee $l8
                    f32.load offset=8
                    local.set $l18
                    local.get $l8
                    f32.load offset=20
                    local.set $l14
                    local.get $l8
                    f32.load offset=4
                    local.set $l15
                    local.get $l8
                    f32.load offset=16
                    local.set $l19
                    local.get $l5
                    local.get $l8
                    f32.load
                    local.tee $l16
                    local.get $l8
                    f32.load offset=12
                    local.tee $l17
                    f32.add
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=96
                    local.get $l5
                    local.get $l15
                    local.get $l19
                    f32.add
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=100
                    local.get $l5
                    i32.const 0
                    i32.store offset=108
                    local.get $l5
                    local.get $l18
                    local.get $l14
                    f32.add
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=104
                    local.get $l5
                    local.get $l17
                    local.get $l16
                    f32.sub
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=80
                    local.get $l5
                    local.get $l19
                    local.get $l15
                    f32.sub
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=84
                    local.get $l5
                    i32.const 0
                    i32.store offset=92
                    local.get $l5
                    local.get $l14
                    local.get $l18
                    f32.sub
                    f32.const 0x1p-1 (;=0.5;)
                    f32.mul
                    f32.store offset=88
                    local.get $l5
                    local.get $l5
                    i64.load offset=96
                    i64.store offset=16
                    local.get $l5
                    local.get $l5
                    i64.load offset=104
                    i64.store offset=24
                    local.get $l5
                    local.get $l5
                    i64.load offset=80
                    i64.store
                    local.get $l5
                    local.get $l5
                    i64.load offset=88
                    i64.store offset=8
                    local.get $p3
                    local.get $l5
                    i32.const 16
                    i32.add
                    local.get $l5
                    call $f71852
                    i32.eqz
                    br_if $B6
                  end
                  local.get $p4
                  local.get $l5
                  i32.const 76
                  i32.add
                  local.get $p0
                  local.get $l11
                  i32.const 3
                  i32.shl
                  i32.add
                  local.get $p4
                  i32.load
                  i32.load
                  call_indirect $__indirect_function_table (type $t3)
                  i32.eqz
                  br_if $B2
                end
                local.get $l6
                i32.const 4
                i32.add
                local.set $l6
                local.get $l10
                i32.const 1
                i32.sub
                local.tee $l10
                br_if $L5
              end
            end
            local.get $l7
            i32.eqz
            local.set $l13
            local.get $l7
            i32.eqz
            br_if $B2
            local.get $l7
            i32.const 1
            i32.sub
            local.set $l7
            br $L0
          end
          local.get $l5
          i32.load offset=1172
          local.get $l7
          i32.const 2
          i32.shl
          i32.add
          local.get $l12
          local.get $l8
          i32.const 28
          i32.mul
          i32.add
          local.tee $l6
          i32.const 28
          i32.add
          i32.store
          local.get $l7
          i32.const 1
          i32.add
          local.tee $l7
          local.get $l5
          i32.load offset=1180
          i32.const 2147483647
          i32.and
          i32.eq
          if $I8
            local.get $l5
            i32.const 144
            i32.add
            local.get $l7
            i32.const 1
            i32.shl
            call $f71870
          end
          local.get $l6
          f32.load
          local.tee $l14
          local.get $l6
          f32.load offset=12
          local.tee $l15
          f32.add
          local.set $l18
          local.get $l15
          local.get $l14
          f32.sub
          local.set $l14
          local.get $l6
          f32.load offset=8
          local.tee $l16
          local.get $l6
          f32.load offset=20
          local.tee $l17
          f32.add
          local.set $l15
          local.get $l6
          f32.load offset=4
          local.tee $l20
          local.get $l6
          f32.load offset=16
          local.tee $l21
          f32.add
          local.set $l19
          local.get $l17
          local.get $l16
          f32.sub
          local.set $l16
          local.get $l21
          local.get $l20
          f32.sub
          local.set $l17
          br $L1
        end
      end
    end
    block $B9
      local.get $l5
      i32.load offset=1180
      local.tee $l6
      i32.const 0
      i32.lt_s
      br_if $B9
      local.get $l6
      i32.const 2147483647
      i32.and
      i32.eqz
      br_if $B9
      local.get $l5
      i32.load offset=1172
      local.tee $l6
      local.get $l5
      i32.const 144
      i32.add
      i32.eq
      br_if $B9
      local.get $l6
      i32.eqz
      br_if $B9
      call $f69753
      local.tee $l7
      local.get $l6
      local.get $l7
      i32.load
      i32.load offset=12
      call_indirect $__indirect_function_table (type $t1)
    end
    local.get $l5
    i32.const 1184
    i32.add
    global.set $g0
    local.get $l13)
