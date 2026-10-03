  (func $f71700 (type $t10) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (result i32)
    (local $l6 i32) (local $l7 i32) (local $l8 i32) (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i64) (local $l13 i64)
    global.get $g0
    i32.const 16
    i32.sub
    local.tee $l8
    global.set $g0
    local.get $p2
    i32.load offset=4
    local.tee $l9
    i32.load offset=44
    i32.load8_u offset=9
    local.set $l6
    block $B0
      block $B1
        block $B2
          block $B3
            block $B4
              local.get $p1
              i32.load offset=4
              local.tee $l10
              i32.load offset=44
              i32.load8_u offset=9
              local.tee $l7
              i32.const 2
              i32.ne
              br_if $B4
              local.get $l6
              i32.const 255
              i32.and
              i32.const 2
              i32.ne
              br_if $B4
              local.get $p1
              call $f71419
              i32.load offset=100
              i32.load8_u offset=159
              i32.const 0
              i32.ne
              local.set $l11
              br $B3
            end
            local.get $l7
            i32.eqz
            br_if $B2
          end
          local.get $l6
          i32.const 255
          i32.and
          i32.const 1
          i32.eq
          local.get $l7
          i32.const 2
          i32.eq
          i32.and
          br_if $B2
          local.get $l11
          br_if $B2
          block $B5
            local.get $l7
            i32.const 1
            i32.ne
            br_if $B5
            local.get $l6
            i32.const 255
            i32.and
            i32.const 1
            i32.ne
            br_if $B5
            local.get $p1
            call $f71419
            i32.load offset=44
            i32.load8_u offset=44
            i32.const 1
            i32.and
            br_if $B2
          end
          local.get $l7
          local.get $l6
          i32.const 255
          i32.and
          i32.ne
          br_if $B1
          local.get $l10
          i32.load offset=48
          local.get $l9
          i32.load offset=48
          i32.ge_u
          br_if $B1
        end
        local.get $p2
        local.set $l6
        br $B0
      end
      local.get $p1
      local.set $l6
      local.get $p2
      local.set $p1
    end
    local.get $p5
    i32.eqz
    if $I6
      local.get $p0
      i32.load offset=984
      local.tee $p5
      i32.eqz
      if $I7
        local.get $p0
        i32.const 696
        i32.add
        call $f71704
        local.get $p0
        i32.load offset=984
        local.set $p5
      end
      local.get $p0
      local.get $p5
      i32.load
      i32.store offset=984
      local.get $p0
      i32.const 976
      i32.add
      local.tee $l7
      local.get $l7
      i32.load
      i32.const 1
      i32.add
      i32.store
    end
    local.get $l8
    local.get $p3
    i32.load16_u
    i32.store16 offset=8
    block $B8 (result i32)
      local.get $p5
      i32.const 4
      i32.add
      local.get $l6
      i32.load offset=4
      local.get $p1
      i32.load offset=4
      i32.const 0
      i32.const 5
      call $f71680
      local.set $p0
      local.get $p5
      i32.const -1
      i32.store offset=36
      local.get $p5
      local.get $p1
      i32.store offset=32
      local.get $p5
      local.get $l6
      i32.store offset=28
      local.get $p5
      i32.const 0
      i32.store16 offset=64
      local.get $p5
      i64.const -4294967296
      i64.store offset=56 align=4
      local.get $p5
      i64.const -4294967296
      i64.store offset=48 align=4
      local.get $p5
      i64.const 4294967295
      i64.store offset=40 align=4
      local.get $p5
      i32.const 3171232
      i32.store
      local.get $p5
      local.get $l8
      i32.const 8
      i32.add
      local.tee $l7
      i32.load16_u
      i32.const 32767
      i32.and
      i32.store offset=44
      local.get $p0
      i32.load
      i32.load offset=40
      local.set $p2
      local.get $l6
      call $f71419
      local.set $p1
      local.get $p5
      i32.load offset=32
      call $f71419
      local.set $p3
      local.get $l7
      i32.load16_u
      local.set $l6
      i32.const 1
      local.set $l7
      local.get $p5
      block $B9 (result i32)
        block $B10
          block $B11
            local.get $p1
            i32.load offset=44
            i32.load8_u offset=44
            i32.const 1
            i32.and
            if $I12
              local.get $p3
              i32.eqz
              br_if $B11
              local.get $p3
              i32.load offset=44
              i32.load8_u offset=44
              i32.const 1
              i32.and
              i32.eqz
              local.set $l7
            end
            local.get $l6
            i32.const 1
            i32.and
            i32.eqz
            br_if $B11
            local.get $l7
            br_if $B10
          end
          local.get $p5
          i32.load offset=44
          i32.const 262144
          i32.or
          br $B9
        end
        local.get $p5
        i32.load offset=44
        i32.const -262145
        i32.and
      end
      i32.store offset=44
      local.get $p5
      block $B13 (result i32)
        block $B14
          block $B15
            local.get $l6
            i32.const 514
            i32.and
            br_if $B15
            local.get $p2
            i32.const 6
            call $f71389
            f32.const 0x0p+0 (;=0;)
            f32.ne
            br_if $B15
            local.get $p2
            i32.const 7
            call $f71389
            f32.const 0x0p+0 (;=0;)
            f32.ne
            br_if $B15
            local.get $p2
            i32.const 8
            call $f71389
            f32.const 0x0p+0 (;=0;)
            f32.ne
            br_if $B15
            local.get $p2
            i32.const 9
            call $f71389
            f32.const 0x0p+0 (;=0;)
            f32.eq
            br_if $B14
          end
          local.get $p5
          i32.load offset=44
          i32.const 131072
          i32.or
          br $B13
        end
        local.get $p5
        i32.load offset=44
        i32.const -131073
        i32.and
      end
      i32.store offset=44
      local.get $p4
      i32.eqz
      if $I16
        local.get $p1
        i64.load offset=144
        local.set $l13
        local.get $p1
        i32.load offset=100
        local.tee $l6
        local.get $l6
        i32.load offset=148
        i32.const 1
        i32.add
        i32.store offset=148
        block $B17
          local.get $p3
          i32.eqz
          if $I18
            i64.const 2199023255040
            local.set $l12
            br $B17
          end
          local.get $p3
          i64.load offset=144
          local.set $l12
          local.get $p3
          i32.load offset=100
          local.tee $l6
          local.get $l6
          i32.load offset=148
          i32.const 1
          i32.add
          i32.store offset=148
        end
        local.get $p5
        local.get $p2
        i32.load offset=1000
        i32.const 0
        local.get $l13
        local.get $l12
        local.get $p0
        call $f70708
        i32.store offset=60
        local.get $p0
        call $f71361
        local.set $l6
        local.get $p0
        i32.load
        local.get $p0
        call $f71333
        local.get $p5
        i32.load offset=8
        local.get $p0
        call $f71333
        local.get $p2
        i32.load offset=2168
        local.get $p5
        call $f71693
        local.get $p2
        local.get $p0
        local.get $l6
        call $f71383
        local.get $p5
        br $B8
      end
      local.get $p5
      local.get $p4
      call $f71627
      drop
      local.get $p5
    end
    local.set $p1
    local.get $l8
    i32.const 16
    i32.add
    global.set $g0
    local.get $p1)