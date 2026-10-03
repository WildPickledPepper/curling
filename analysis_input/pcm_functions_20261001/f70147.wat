  (func $f70147 (type $t8) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (result i32)
    (local $l4 i32) (local $l5 i32) (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 i32) (local $l14 i32) (local $l15 i32) (local $l16 i32) (local $l17 i32) (local $l18 i32) (local $l19 i32) (local $l20 i32) (local $l21 i32) (local $l22 f32) (local $l23 f32)
    global.get $g0
    i32.const 80
    i32.sub
    local.tee $l4
    global.set $g0
    local.get $l4
    i64.const 0
    i64.store offset=40
    local.get $l4
    i64.const 0
    i64.store offset=48
    local.get $l4
    i64.const 0
    i64.store offset=32
    local.get $l4
    i32.const 0
    i32.store16 offset=28
    local.get $l4
    i32.const -1
    i32.store offset=24
    local.get $l4
    i64.const 0
    i64.store offset=16
    local.get $l4
    i32.const 0
    i32.store offset=64
    local.get $l4
    i64.const 2139095039
    i64.store offset=56
    block $B0
      local.get $p1
      i32.eqz
      if $I1
        br $B0
      end
      local.get $p0
      i32.const 108
      i32.add
      local.set $l12
      local.get $p0
      i32.const -64
      i32.sub
      local.set $l14
      local.get $p0
      i32.const 40
      i32.add
      local.set $l16
      local.get $p0
      i32.const 28
      i32.add
      local.set $l17
      local.get $l4
      i32.const -64
      i32.sub
      local.set $l18
      local.get $l4
      i32.const 60
      i32.add
      local.set $l10
      local.get $l4
      i32.const 56
      i32.add
      local.set $l19
      i32.const 1
      local.set $l11
      loop $L2
        local.get $p2
        local.get $l9
        i32.const 2
        i32.shl
        i32.add
        i32.load
        local.tee $l5
        i32.const 5
        i32.shr_u
        local.set $l20
        local.get $l5
        i32.const 1
        i32.shr_u
        i32.const 15
        i32.and
        local.set $l21
        i32.const 0
        local.set $l5
        loop $L3
          local.get $l5
          local.tee $l15
          local.get $l20
          i32.add
          local.set $l13
          block $B4 (result i32)
            local.get $p0
            i32.load offset=12
            if $I5
              local.get $p0
              i32.load offset=16
              local.get $l13
              i32.const 6
              i32.mul
              i32.add
              local.tee $l5
              i32.load16_u offset=4
              local.set $l8
              local.get $l5
              i32.load16_u
              local.set $l6
              local.get $l5
              i32.load16_u offset=2
              br $B4
            end
            local.get $p0
            i32.load offset=16
            local.get $l13
            i32.const 12
            i32.mul
            i32.add
            local.tee $l5
            i32.load offset=8
            local.set $l8
            local.get $l5
            i32.load
            local.set $l6
            local.get $l5
            i32.load offset=4
          end
          local.set $l7
          local.get $p0
          i32.load offset=20
          local.set $l5
          local.get $l4
          local.get $l8
          i32.store offset=12
          local.get $l4
          local.get $l7
          i32.store offset=8
          local.get $l4
          local.get $l6
          i32.store offset=4
          block $B6
            local.get $l17
            local.get $l16
            local.get $l5
            local.get $l6
            i32.const 12
            i32.mul
            i32.add
            local.tee $l6
            local.get $l5
            local.get $l7
            i32.const 12
            i32.mul
            i32.add
            local.tee $l7
            local.get $l5
            local.get $l8
            i32.const 12
            i32.mul
            i32.add
            local.tee $l5
            local.get $l19
            local.get $l10
            local.get $l18
            local.get $p0
            i32.load8_u offset=52
            i32.eqz
            local.get $p0
            f32.load offset=56
            call $f70472
            i32.eqz
            br_if $B6
            local.get $l4
            f32.load offset=56
            local.tee $l22
            f32.const 0x0p+0 (;=0;)
            f32.lt
            br_if $B6
            local.get $l22
            local.get $p0
            f32.load offset=60
            f32.le
            i32.eqz
            br_if $B6
            local.get $l4
            i32.const 1
            i32.store16 offset=28
            local.get $l4
            local.get $l13
            i32.store offset=24
            block $B7
              local.get $p0
              i32.load8_u offset=177
              if $I8
                local.get $l22
                local.get $p0
                f32.load offset=104
                f32.lt
                i32.eqz
                br_if $B7
                local.get $l14
                local.get $l4
                i64.load offset=16
                i64.store align=4
                local.get $l14
                local.get $l4
                i32.load offset=24
                i32.store offset=8
                local.get $p0
                i32.const 1
                i32.store16 offset=76
                local.get $p0
                local.get $l4
                f32.load offset=32
                f32.store offset=80
                local.get $p0
                local.get $l4
                f32.load offset=36
                f32.store offset=84
                local.get $p0
                local.get $l4
                f32.load offset=40
                f32.store offset=88
                local.get $p0
                local.get $l4
                f32.load offset=44
                f32.store offset=92
                local.get $p0
                local.get $l4
                f32.load offset=48
                f32.store offset=96
                local.get $l4
                f32.load offset=52
                local.set $l23
                local.get $p0
                local.get $l22
                f32.store offset=104
                local.get $p0
                local.get $l23
                f32.store offset=100
                local.get $l12
                local.get $l10
                i32.load offset=16
                i32.store offset=16
                local.get $l12
                local.get $l10
                i64.load offset=8 align=4
                i64.store offset=8 align=4
                local.get $l12
                local.get $l10
                i64.load align=4
                i64.store align=4
                local.get $p3
                local.get $l22
                local.get $p3
                f32.load
                local.tee $l23
                local.get $l22
                local.get $l23
                f32.lt
                select
                f32.store
                local.get $p0
                local.get $l6
                f32.load
                f32.store offset=128
                local.get $p0
                local.get $l6
                f32.load offset=4
                f32.store offset=132
                local.get $p0
                local.get $l6
                f32.load offset=8
                f32.store offset=136
                local.get $p0
                local.get $l7
                f32.load
                f32.store offset=140
                local.get $p0
                local.get $l7
                f32.load offset=4
                f32.store offset=144
                local.get $p0
                local.get $l7
                f32.load offset=8
                f32.store offset=148
                local.get $p0
                local.get $l5
                f32.load
                f32.store offset=152
                local.get $p0
                local.get $l5
                f32.load offset=4
                f32.store offset=156
                local.get $p0
                local.get $l5
                f32.load offset=8
                f32.store offset=160
                local.get $p0
                local.get $l4
                i32.load offset=4
                i32.store offset=164
                local.get $p0
                local.get $l4
                i32.load offset=8
                i32.store offset=168
                local.get $l4
                i32.load offset=12
                local.set $l5
                local.get $p0
                i32.const 1
                i32.store8 offset=176
                local.get $p0
                local.get $l5
                i32.store offset=172
                br $B7
              end
              local.get $l4
              local.get $p3
              f32.load
              f32.store
              local.get $p0
              i32.load offset=8
              local.tee $l8
              local.get $l4
              i32.const 16
              i32.add
              local.get $l6
              local.get $l7
              local.get $l5
              local.get $l4
              local.get $l4
              i32.const 4
              i32.add
              local.get $l8
              i32.load
              i32.load
              call_indirect $__indirect_function_table (type $t14)
              i32.eqz
              br_if $B0
              local.get $l4
              f32.load
              local.tee $l22
              local.get $p3
              f32.load
              f32.lt
              i32.eqz
              br_if $B7
              local.get $p3
              local.get $l22
              f32.store
              local.get $p0
              local.get $l22
              f32.store offset=60
            end
            local.get $p0
            i32.load offset=8
            i32.load offset=4
            i32.eqz
            br_if $B0
          end
          local.get $l15
          i32.const 1
          i32.add
          local.set $l5
          local.get $l15
          local.get $l21
          i32.ne
          br_if $L3
        end
        local.get $l9
        i32.const 1
        i32.add
        local.tee $l9
        local.get $p1
        i32.lt_u
        local.set $l11
        local.get $p1
        local.get $l9
        i32.ne
        br_if $L2
      end
    end
    local.get $l4
    i32.const 80
    i32.add
    global.set $g0
    local.get $l11
    i32.const -1
    i32.xor
    i32.const 1
    i32.and)
