  (func $f71011 (type $t24) (param $p0 i32) (param $p1 i32) (param $p2 i32) (param $p3 i32) (param $p4 i32) (param $p5 i32) (param $p6 i32) (param $p7 i32) (param $p8 i32)
    (local $l9 i32) (local $l10 i32) (local $l11 i32) (local $l12 i32) (local $l13 f32) (local $l14 f32) (local $l15 f32) (local $l16 f32) (local $l17 f32) (local $l18 f32) (local $l19 f32) (local $l20 f32) (local $l21 f32) (local $l22 f32) (local $l23 f32) (local $l24 f32) (local $l25 f32) (local $l26 f32) (local $l27 i64)
    global.get $g0
    i32.const 160
    i32.sub
    local.tee $l10
    global.set $g0
    block $B0
      local.get $p3
      local.get $p0
      local.get $p6
      i32.const 80
      i32.mul
      i32.add
      i32.load offset=72
      i32.eq
      if $I1
        local.get $p4
        f32.load offset=20
        local.set $l13
        local.get $p4
        f32.load offset=24
        local.set $l14
        local.get $p7
        f32.load offset=20
        local.set $l15
        local.get $p4
        f32.load
        local.set $l16
        local.get $p4
        f32.load offset=4
        local.set $l17
        local.get $p4
        f32.load offset=8
        local.set $l18
        local.get $p4
        f32.load offset=16
        local.set $l19
        local.get $p7
        f32.load
        local.set $l20
        local.get $p7
        f32.load offset=4
        local.set $l21
        local.get $p7
        f32.load offset=8
        local.set $l22
        local.get $p7
        f32.load offset=16
        local.set $l23
        local.get $l10
        local.get $p7
        f32.load offset=24
        f32.neg
        f32.store offset=152
        local.get $l10
        local.get $l15
        f32.neg
        f32.store offset=148
        local.get $l10
        i32.const 0
        i32.store offset=156
        local.get $l10
        local.get $l23
        f32.neg
        f32.store offset=144
        local.get $l10
        i32.const 0
        i32.store offset=140
        local.get $l10
        local.get $l22
        f32.neg
        f32.store offset=136
        local.get $l10
        local.get $l21
        f32.neg
        f32.store offset=132
        local.get $l10
        local.get $l20
        f32.neg
        f32.store offset=128
        local.get $l10
        i32.const 96
        i32.add
        local.get $p2
        i32.load offset=284
        local.get $p6
        i32.const 96
        i32.mul
        i32.add
        local.get $p6
        i32.const 160
        i32.mul
        local.tee $p4
        local.get $p2
        i32.load offset=340
        i32.add
        i32.const 120
        i32.add
        local.get $p6
        i32.const 76
        i32.mul
        local.tee $p7
        local.get $p2
        i32.load offset=272
        i32.add
        local.get $l10
        i32.const 128
        i32.add
        call $f71003
        local.get $l10
        local.get $l14
        local.get $l10
        f32.load offset=120
        f32.sub
        f32.store offset=88
        local.get $l10
        local.get $l13
        local.get $l10
        f32.load offset=116
        f32.sub
        f32.store offset=84
        local.get $l10
        i32.const 0
        i32.store offset=92
        local.get $l10
        i32.const 0
        i32.store offset=76
        local.get $l10
        local.get $l19
        local.get $l10
        f32.load offset=112
        f32.sub
        f32.store offset=80
        local.get $l10
        local.get $l18
        local.get $l10
        f32.load offset=104
        f32.sub
        f32.store offset=72
        local.get $l10
        local.get $l17
        local.get $l10
        f32.load offset=100
        f32.sub
        f32.store offset=68
        local.get $l10
        local.get $l16
        local.get $l10
        f32.load offset=96
        f32.sub
        f32.store offset=64
        local.get $l10
        i32.const 32
        i32.add
        local.get $p2
        i32.load offset=224
        local.get $p3
        i32.const 192
        i32.mul
        i32.add
        local.get $l10
        i32.const -64
        i32.sub
        call $f71205
        local.get $l10
        local.get $p2
        i32.load offset=340
        local.get $p4
        i32.add
        i32.const 120
        i32.add
        local.get $p2
        i32.load offset=236
        local.get $p6
        i32.const 112
        i32.mul
        i32.add
        local.get $p2
        i32.load offset=248
        local.get $p6
        i32.const 36
        i32.mul
        i32.add
        local.get $p2
        i32.load offset=272
        local.get $p7
        i32.add
        local.get $l10
        i32.const 128
        i32.add
        local.get $l10
        i32.const 32
        i32.add
        call $f70999
        local.get $l10
        f32.load offset=56
        local.set $l13
        local.get $l10
        i64.load offset=48
        local.set $l27
        local.get $p5
        i32.const 0
        i32.store offset=12
        local.get $p5
        local.get $l13
        f32.store offset=8
        local.get $p5
        local.get $l27
        i64.store
        local.get $l10
        i64.load offset=32
        local.set $l27
        local.get $l10
        f32.load offset=40
        local.set $l13
        local.get $p5
        i32.const 0
        i32.store offset=28
        local.get $p5
        local.get $l13
        f32.store offset=24
        local.get $p5
        local.get $l27
        i64.store offset=16
        local.get $l10
        f32.load offset=24
        local.set $l13
        local.get $l10
        i64.load offset=16
        local.set $l27
        local.get $p8
        i32.const 0
        i32.store offset=12
        local.get $p8
        local.get $l13
        f32.store offset=8
        local.get $p8
        local.get $l27
        i64.store
        local.get $l10
        i64.load
        local.set $l27
        local.get $l10
        f32.load offset=8
        local.set $l13
        local.get $p8
        i32.const 0
        i32.store offset=28
        local.get $p8
        local.get $l13
        f32.store offset=24
        local.get $p8
        local.get $l27
        i64.store offset=16
        br $B0
      end
      local.get $p0
      local.set $l11
      local.get $p1
      local.set $l12
      global.get $g0
      i32.const 1216
      i32.sub
      local.tee $l9
      global.set $g0
      local.get $p3
      local.set $p1
      local.get $p3
      local.get $p6
      i32.ne
      if $I2
        local.get $p3
        local.set $p0
        local.get $p6
        local.set $p1
        loop $L3
          block $B4
            local.get $p0
            local.get $p1
            i32.lt_u
            if $I5
              local.get $l11
              local.get $p1
              i32.const 80
              i32.mul
              i32.add
              i32.load offset=72
              local.set $p1
              br $B4
            end
            local.get $l11
            local.get $p0
            i32.const 80
            i32.mul
            i32.add
            i32.load offset=72
            local.set $p0
          end
          local.get $p0
          local.get $p1
          i32.ne
          br_if $L3
        end
      end
      local.get $p4
      f32.load offset=20
      local.set $l13
      local.get $p4
      f32.load
      local.set $l14
      local.get $p4
      f32.load offset=4
      local.set $l15
      local.get $p4
      f32.load offset=8
      local.set $l16
      local.get $p4
      f32.load offset=16
      local.set $l17
      local.get $l9
      local.get $p4
      f32.load offset=24
      f32.neg
      local.tee $l23
      f32.store offset=184
      local.get $l9
      local.get $l13
      f32.neg
      local.tee $l13
      f32.store offset=180
      i32.const 0
      local.set $p0
      local.get $l9
      i32.const 0
      i32.store offset=188
      local.get $l9
      local.get $l17
      f32.neg
      local.tee $l17
      f32.store offset=176
      local.get $l9
      i32.const 0
      i32.store offset=172
      local.get $l9
      local.get $l16
      f32.neg
      local.tee $l16
      f32.store offset=168
      local.get $l9
      local.get $l15
      f32.neg
      local.tee $l15
      f32.store offset=164
      local.get $l9
      local.get $l14
      f32.neg
      local.tee $l14
      f32.store offset=160
      local.get $p7
      f32.load offset=20
      local.set $l18
      local.get $p7
      f32.load
      local.set $l19
      local.get $p7
      f32.load offset=4
      local.set $l20
      local.get $p7
      f32.load offset=8
      local.set $l21
      local.get $p7
      f32.load offset=16
      local.set $l22
      local.get $l9
      local.get $p7
      f32.load offset=24
      f32.neg
      local.tee $l24
      f32.store offset=152
      local.get $l9
      local.get $l18
      f32.neg
      local.tee $l18
      f32.store offset=148
      local.get $l9
      i32.const 0
      i32.store offset=156
      local.get $l9
      i32.const 0
      i32.store offset=140
      local.get $l9
      local.get $l22
      f32.neg
      local.tee $l22
      f32.store offset=144
      local.get $l9
      local.get $l21
      f32.neg
      local.tee $l21
      f32.store offset=136
      local.get $l9
      local.get $l20
      f32.neg
      local.tee $l20
      f32.store offset=132
      local.get $l9
      local.get $l19
      f32.neg
      local.tee $l19
      f32.store offset=128
      local.get $l12
      local.get $p3
      i32.const 5
      i32.shl
      i32.add
      local.tee $p4
      i32.const 0
      i32.store offset=28
      local.get $p4
      local.get $l23
      f32.store offset=24
      local.get $p4
      local.get $l13
      f32.store offset=20
      local.get $p4
      local.get $l17
      f32.store offset=16
      local.get $p4
      i32.const 0
      i32.store offset=12
      local.get $p4
      local.get $l16
      f32.store offset=8
      local.get $p4
      local.get $l15
      f32.store offset=4
      local.get $p4
      local.get $l14
      f32.store
      local.get $l12
      local.get $p6
      i32.const 5
      i32.shl
      i32.add
      local.tee $p4
      i32.const 0
      i32.store offset=28
      local.get $p4
      local.get $l24
      f32.store offset=24
      local.get $p4
      local.get $l18
      f32.store offset=20
      local.get $p4
      local.get $l22
      f32.store offset=16
      local.get $p4
      i32.const 0
      i32.store offset=12
      local.get $p4
      local.get $l21
      f32.store offset=8
      local.get $p4
      local.get $l20
      f32.store offset=4
      local.get $p4
      local.get $l19
      f32.store
      local.get $p1
      local.get $p3
      i32.ne
      if $I6
        loop $L7
          local.get $l9
          i32.const 96
          i32.add
          local.get $p2
          i32.load offset=284
          local.get $p3
          i32.const 96
          i32.mul
          i32.add
          local.get $p2
          i32.load offset=340
          local.get $p3
          i32.const 160
          i32.mul
          i32.add
          i32.const 120
          i32.add
          local.get $p2
          i32.load offset=272
          local.get $p3
          i32.const 76
          i32.mul
          i32.add
          local.get $l9
          i32.const 160
          i32.add
          call $f71003
          local.get $l9
          i32.const 0
          i32.store offset=172
          local.get $l9
          i32.const 0
          i32.store offset=188
          local.get $l9
          local.get $l9
          f32.load offset=96
          local.tee $l14
          f32.store offset=160
          local.get $l9
          local.get $l9
          f32.load offset=100
          local.tee $l15
          f32.store offset=164
          local.get $l9
          local.get $l9
          f32.load offset=104
          local.tee $l16
          f32.store offset=168
          local.get $l9
          local.get $l9
          f32.load offset=112
          local.tee $l17
          f32.store offset=176
          local.get $l9
          local.get $l9
          f32.load offset=116
          local.tee $l13
          f32.store offset=180
          local.get $l9
          local.get $l9
          f32.load offset=120
          local.tee $l23
          f32.store offset=184
          local.get $l12
          local.get $l11
          local.get $p3
          i32.const 80
          i32.mul
          i32.add
          local.tee $p7
          i32.load offset=72
          i32.const 5
          i32.shl
          i32.add
          local.tee $p4
          i32.const 0
          i32.store offset=28
          local.get $p4
          local.get $l17
          f32.store offset=16
          local.get $p4
          i32.const 0
          i32.store offset=12
          local.get $p4
          local.get $l16
          f32.store offset=8
          local.get $p4
          local.get $l15
          f32.store offset=4
          local.get $p4
          local.get $l14
          f32.store
          local.get $p4
          local.get $l23
          f32.store offset=24
          local.get $p4
          local.get $l13
          f32.store offset=20
          local.get $l9
          i32.const 192
          i32.add
          local.get $p0
          i32.const 2
          i32.shl
          i32.add
          local.get $p3
          i32.store
          local.get $p0
          i32.const 1
          i32.add
          local.set $p0
          local.get $p7
          i32.load offset=72
          local.tee $p3
          local.get $p1
          i32.ne
          br_if $L7
        end
      end
      local.get $p0
      local.set $p3
      local.get $p1
      local.get $p6
      i32.ne
      if $I8
        loop $L9
          local.get $l9
          i32.const 96
          i32.add
          local.get $p2
          i32.load offset=284
          local.get $p6
          i32.const 96
          i32.mul
          i32.add
          local.get $p2
          i32.load offset=340
          local.get $p6
          i32.const 160
          i32.mul
          i32.add
          i32.const 120
          i32.add
          local.get $p2
          i32.load offset=272
          local.get $p6
          i32.const 76
          i32.mul
          i32.add
          local.get $l9
          i32.const 128
          i32.add
          call $f71003
          local.get $l9
          i32.const 0
          i32.store offset=140
          local.get $l9
          i32.const 0
          i32.store offset=156
          local.get $l9
          local.get $l9
          f32.load offset=96
          local.tee $l19
          f32.store offset=128
          local.get $l9
          local.get $l9
          f32.load offset=100
          local.tee $l20
          f32.store offset=132
          local.get $l9
          local.get $l9
          f32.load offset=104
          local.tee $l21
          f32.store offset=136
          local.get $l9
          local.get $l9
          f32.load offset=112
          local.tee $l22
          f32.store offset=144
          local.get $l9
          local.get $l9
          f32.load offset=116
          local.tee $l18
          f32.store offset=148
          local.get $l9
          local.get $l9
          f32.load offset=120
          local.tee $l24
          f32.store offset=152
          local.get $l12
          local.get $l11
          local.get $p6
          i32.const 80
          i32.mul
          i32.add
          local.tee $p7
          i32.load offset=72
          i32.const 5
          i32.shl
          i32.add
          local.tee $p4
          i32.const 0
          i32.store offset=28
          local.get $p4
          local.get $l22
          f32.store offset=16
          local.get $p4
          i32.const 0
          i32.store offset=12
          local.get $p4
          local.get $l21
          f32.store offset=8
          local.get $p4
          local.get $l20
          f32.store offset=4
          local.get $p4
          local.get $l19
          f32.store
          local.get $p4
          local.get $l24
          f32.store offset=24
          local.get $p4
          local.get $l18
          f32.store offset=20
          local.get $l9
          i32.const 192
          i32.add
          local.get $p3
          i32.const 2
          i32.shl
          i32.add
          local.get $p6
          i32.store
          local.get $p3
          i32.const 1
          i32.add
          local.set $p3
          local.get $p7
          i32.load offset=72
          local.tee $p6
          local.get $p1
          i32.ne
          br_if $L9
        end
      end
      local.get $p2
      i32.load offset=224
      local.set $p4
      local.get $l9
      i32.const 88
      i32.add
      local.tee $p6
      local.get $l23
      local.get $l24
      f32.add
      f32.neg
      f32.store
      local.get $l9
      i32.const 84
      i32.add
      local.tee $l11
      local.get $l13
      local.get $l18
      f32.add
      f32.neg
      f32.store
      local.get $l9
      i32.const 0
      i32.store offset=92
      local.get $l9
      local.get $l17
      local.get $l22
      f32.add
      f32.neg
      f32.store offset=80
      local.get $l9
      i32.const 0
      i32.store offset=76
      local.get $l9
      local.get $l16
      local.get $l21
      f32.add
      f32.neg
      f32.store offset=72
      local.get $l9
      local.get $l15
      local.get $l20
      f32.add
      f32.neg
      f32.store offset=68
      local.get $l9
      local.get $l14
      local.get $l19
      f32.add
      f32.neg
      f32.store offset=64
      local.get $l9
      i32.const 96
      i32.add
      local.get $p4
      local.get $p1
      i32.const 192
      i32.mul
      i32.add
      local.get $l9
      i32.const -64
      i32.sub
      call $f71205
      local.get $l11
      local.get $l9
      f32.load offset=116
      local.tee $l24
      f32.store
      local.get $p6
      local.get $l9
      f32.load offset=120
      local.tee $l18
      f32.store
      local.get $l9
      local.get $l9
      f32.load offset=96
      local.tee $l22
      f32.store offset=64
      local.get $l9
      local.get $l9
      f32.load offset=100
      local.tee $l21
      f32.store offset=68
      local.get $l9
      local.get $l9
      f32.load offset=104
      local.tee $l20
      f32.store offset=72
      local.get $l9
      local.get $l9
      f32.load offset=108
      local.tee $l25
      f32.store offset=76
      local.get $l9
      local.get $l9
      f32.load offset=112
      local.tee $l19
      f32.store offset=80
      local.get $l9
      local.get $l9
      f32.load offset=124
      local.tee $l26
      f32.store offset=92
      local.get $l18
      local.set $l23
      local.get $l24
      local.set $l13
      local.get $l19
      local.set $l17
      local.get $l20
      local.set $l16
      local.get $l21
      local.set $l15
      local.get $l22
      local.set $l14
      local.get $p0
      local.get $p3
      i32.lt_u
      if $I10
        loop $L11
          local.get $l9
          i32.const 32
          i32.add
          local.get $p2
          i32.load offset=340
          local.get $l9
          i32.const 192
          i32.add
          local.get $p3
          i32.const 1
          i32.sub
          local.tee $p3
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $p4
          i32.const 160
          i32.mul
          i32.add
          i32.const 120
          i32.add
          local.get $p2
          i32.load offset=236
          local.get $p4
          i32.const 112
          i32.mul
          i32.add
          local.get $p2
          i32.load offset=248
          local.get $p4
          i32.const 36
          i32.mul
          i32.add
          local.get $p2
          i32.load offset=272
          local.get $p4
          i32.const 76
          i32.mul
          i32.add
          local.get $l12
          local.get $p4
          i32.const 5
          i32.shl
          i32.add
          local.get $l9
          i32.const -64
          i32.sub
          call $f70999
          local.get $l9
          i32.const 0
          i32.store offset=76
          local.get $l9
          i32.const 0
          i32.store offset=92
          local.get $l9
          local.get $l9
          f32.load offset=32
          local.tee $l22
          f32.store offset=64
          local.get $l9
          local.get $l9
          f32.load offset=36
          local.tee $l21
          f32.store offset=68
          local.get $l9
          local.get $l9
          f32.load offset=40
          local.tee $l20
          f32.store offset=72
          local.get $l9
          local.get $l9
          f32.load offset=48
          local.tee $l19
          f32.store offset=80
          local.get $l9
          local.get $l9
          f32.load offset=52
          local.tee $l24
          f32.store offset=84
          local.get $l9
          local.get $l9
          f32.load offset=56
          local.tee $l18
          f32.store offset=88
          local.get $p0
          local.get $p3
          i32.lt_u
          br_if $L11
        end
        local.get $l9
        f32.load offset=124
        local.set $l26
        local.get $l9
        f32.load offset=112
        local.set $l17
        local.get $l9
        f32.load offset=108
        local.set $l25
        local.get $l9
        f32.load offset=104
        local.set $l16
        local.get $l9
        f32.load offset=100
        local.set $l15
        local.get $l9
        f32.load offset=96
        local.set $l14
        local.get $l9
        f32.load offset=120
        local.set $l23
        local.get $l9
        f32.load offset=116
        local.set $l13
      end
      local.get $l9
      local.get $l23
      f32.store offset=56
      local.get $l9
      local.get $l13
      f32.store offset=52
      local.get $l9
      local.get $l26
      f32.store offset=60
      local.get $l9
      local.get $l17
      f32.store offset=48
      local.get $l9
      local.get $l25
      f32.store offset=44
      local.get $l9
      local.get $l16
      f32.store offset=40
      local.get $l9
      local.get $l15
      f32.store offset=36
      local.get $l9
      local.get $l14
      f32.store offset=32
      local.get $p0
      if $I12
        loop $L13
          local.get $l9
          local.get $p2
          i32.load offset=340
          local.get $l9
          i32.const 192
          i32.add
          local.get $p0
          i32.const 1
          i32.sub
          local.tee $p0
          i32.const 2
          i32.shl
          i32.add
          i32.load
          local.tee $p4
          i32.const 160
          i32.mul
          i32.add
          i32.const 120
          i32.add
          local.get $p2
          i32.load offset=236
          local.get $p4
          i32.const 112
          i32.mul
          i32.add
          local.get $p2
          i32.load offset=248
          local.get $p4
          i32.const 36
          i32.mul
          i32.add
          local.get $p2
          i32.load offset=272
          local.get $p4
          i32.const 76
          i32.mul
          i32.add
          local.get $l12
          local.get $p4
          i32.const 5
          i32.shl
          i32.add
          local.get $l9
          i32.const 32
          i32.add
          call $f70999
          local.get $l9
          i32.const 0
          i32.store offset=44
          local.get $l9
          i32.const 0
          i32.store offset=60
          local.get $l9
          local.get $l9
          f32.load
          local.tee $l14
          f32.store offset=32
          local.get $l9
          local.get $l9
          f32.load offset=4
          local.tee $l15
          f32.store offset=36
          local.get $l9
          local.get $l9
          f32.load offset=8
          local.tee $l16
          f32.store offset=40
          local.get $l9
          local.get $l9
          f32.load offset=16
          local.tee $l17
          f32.store offset=48
          local.get $l9
          local.get $l9
          f32.load offset=20
          local.tee $l13
          f32.store offset=52
          local.get $l9
          local.get $l9
          f32.load offset=24
          local.tee $l23
          f32.store offset=56
          local.get $p0
          br_if $L13
        end
      end
      local.get $p5
      local.get $l14
      f32.store offset=16
      local.get $p5
      local.get $l23
      f32.store offset=8
      local.get $p5
      local.get $l13
      f32.store offset=4
      local.get $p5
      local.get $l17
      f32.store
      local.get $p5
      local.get $l16
      f32.store offset=24
      local.get $p5
      local.get $l15
      f32.store offset=20
      local.get $p8
      local.get $l20
      f32.store offset=24
      local.get $p8
      local.get $l21
      f32.store offset=20
      local.get $p8
      local.get $l22
      f32.store offset=16
      local.get $p8
      local.get $l18
      f32.store offset=8
      local.get $p8
      local.get $l24
      f32.store offset=4
      local.get $p8
      local.get $l19
      f32.store
      local.get $l9
      i32.const 1216
      i32.add
      global.set $g0
    end
    local.get $l10
    i32.const 160
    i32.add
    global.set $g0)
