  (func $f18888 (type $t427) (param $p0 f64) (result f32)
    (local $l1 f64) (local $l2 f64)
    local.get $p0
    local.get $p0
    f64.mul
    local.tee $l1
    local.get $p0
    f64.mul
    local.tee $l2
    local.get $l1
    local.get $l1
    f64.mul
    f64.mul
    local.get $l1
    f64.const 0x1.6cd878c3b46a7p-19 (;=2.71831e-06;)
    f64.mul
    f64.const -0x1.a00f9e2cae774p-13 (;=-0.000198393;)
    f64.add
    f64.mul
    local.get $l2
    local.get $l1
    f64.const 0x1.11110896efbb2p-7 (;=0.00833333;)
    f64.mul
    f64.const -0x1.5555554cbac77p-3 (;=-0.166667;)
    f64.add
    f64.mul
    local.get $p0
    f64.add
    f64.add
    f32.demote_f64)
