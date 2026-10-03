"""Publish scope-specific results and keep all unhandled local evidence visible."""
from collections import Counter
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'analysis_input/local_partial_validation_20261003'
def read(name):return json.loads((OUT/name).read_text(encoding='utf8'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    inventory=read('inventory.json');functions=read('function_windows.json')
    trajectory=read('partial_trajectories.json');motion=read('motion_windows.json');reset=read('reset_windows.json')
    legacy=read('legacy_motion_windows.json');geometry=read('geometry_numeric_windows.json')
    startup=read('startup_windows.json');position=read('reset_position_inputs.json');pcm=read('pcm_windows.json')
    source=sha(ROOT/'local_simulator/unity_physx.py')
    assert source==functions['productionSourceSha256']==trajectory['productionSourceSha256']
    assert functions['capturesWithDifferences']==trajectory['capturesWithDifferences']==motion['capturesWithDifferences']==0
    assert reset['totals'].get('different',0)==0
    assert legacy['capturesWithDifferences']==geometry['capturesWithDifferences']==0
    assert startup['capturesWithDifferences']==position['capturesWithDifferences']==pcm['capturesWithDifferences']==0
    assert source==startup['sourceSha256']==position['sourceSha256']==pcm['productionSourceSha256']
    checked={}
    def add(path,scope):checked.setdefault(path,[]).append(scope)
    for r in functions['capturesInventory']:
        if r['checks'].get('angularSetterFromBodyPose.bridge164.compared',0) or r['checks'].get('angularProjection.bridge164.compared',0):add(r['path'],'angular setter')
        if r['checks'].get('poseNormalization.compared',0):add(r['path'],'normalization arithmetic')
    for r in trajectory['captures']:add(r['path'],'sampled fresh-scene trajectory states')
    for r in motion['capturesInventory']:
        if r['compared']:add(r['path'],'measured sliding math input to angular output')
    for r in reset['capturesInventory']:
        if r['checks'].get('compared'):add(r['path'],'first Reset sampled solver cores')
    previous_checked=set(checked)
    legacy_by_path={r['path']:r for r in legacy['capturesInventory']}
    geometry_by_path={r['path']:r for r in geometry['capturesInventory']}
    for r in legacy['capturesInventory']:
        if r['checks'].get('compared'):add(r['path'],'legacy A0/A2 measured sliding input to sampled setter outputs')
    for r in geometry['capturesInventory']:
        for scope in sorted({w['scope'] for w in r['comparedWindows']}):add(r['path'],scope)
    before_current_followup=set(checked)
    for result,scope in ((startup,'startup formal-stone constructor numeric input/output'),
                         (position,'Reset protocol to sampled Transform position setter input'),
                         (pcm,'measured convex/convex PCM input and cache to contact output')):
        for r in result['capturesInventory']:
            if r['checks'].get('compared'):add(r['path'],scope)
    direct_types={'physx.native.before','physx.native.after','c04.dynamic_solver_frame',
        'c03.first_dynamic_writeback','a12.pcm_internal_call','a12.static_solve',
        'a12.static_writeback','a12.pcm_convex_mesh','a12.pcm_geometry_scale',
        'a12.geometry_write','a12.startup_convex_runtime','a9.native_core_to_solver_setup',
        'a8.static_contact_window','a9.angular_setter_native_delta','c05.persistent_pcm_call',
        'c25.history_positive_stone_pcm','c26.target_static_frame'}
    coverage=[];category=Counter();remaining=Counter()
    for r in inventory['capturesInventory']:
        pending={k:v for k,v in r['eventCounts'].items() if k in direct_types}
        phases=r['phases']
        if phases.get('PxsDynamics.solverSetupSolve'):
            pending['a12.early_phase_core.solverSetupSolve']=phases['PxsDynamics.solverSetupSolve']
        scopes=checked.get(r['path'],[])
        category['withComparedNumericScope' if scopes else 'withoutComparedNumericScope']+=1
        remaining.update(pending)
        coverage.append(dict(path=r['path'],sha256=r['sha256'],passedScopes=scopes,
            actualCapturedEventTypes=r['eventCounts'],
            existingRawEvidenceNeedingSpecificAdapter=pending,
            legacyInputWindowsExcluded=legacy_by_path.get(r['path'],{}).get('excluded',{}),
            geometryNumericWindowsExcluded=geometry_by_path.get(r['path'],{}).get('unsupportedNumericWindows',[]),
            noComparedNumericScopeReason=None if scopes else
                'Existing event types and buffers still need their specific comparison adapter or missing same-call input/branch evidence; this is not a passed log.',
            inputOrProtocolEventCounts={k:v for k,v in r['eventCounts'].items()
                if k in ('sliding.random_range.friction','websocket.recv','websocket.send')},
            allLocalEventTypesChecked=False))
    review_path=OUT/'remaining_capture_payload_review.json'
    review=read(review_path.name) if review_path.exists() else None
    if review:
        if {r['path'] for r in review['capturesInventory']}!={r['path'] for r in coverage if not r['passedScopes']}:review=None
    trajectory_states=trajectory['totals']['denseBeforeTick.windows']+trajectory['totals']['tailBoundary.windows']
    module=ROOT/'local_simulator/runtime/pyphysx/_pyphysx.cp39-win_amd64.pyd'
    assert sha(module)=='7c31ced1773023e552391645e42040c9f3694d513805bc8b95ef0f8bc737bd38'
    sources=[ROOT/'local_simulator/unity_physx.py',
        ROOT/'local_simulator/runtime_support/tools/reverse/recovered_curling_motion.py',
        ROOT/'local_simulator/runtime_support/tools/reverse/recovered_transform_scale.py',
        ROOT/'local_simulator/runtime_support/tools/reverse/recovered_stone_mass.py',
        ROOT/'local_simulator/native_wall_contact.py',ROOT/'local_simulator/native_integrate_cos.py',
        module,ROOT/'local_simulator/runtime/unity_integrate_cos.dll',
        ROOT/'local_simulator/assets/unity_wall_colliders.json',
        ROOT/'local_simulator/assets/unity_startup_body_roster.json',
        ROOT/'analysis_input/unity_20260930.wasm']
    result=dict(inventoriedCaptures=inventory['captures'],inventoriedBytes=inventory['bytes'],
        capturesWithComparedNumericScopes=len(checked),sampledTrajectoryCaptures=trajectory['comparedCaptures'],
        previouslyComparedCaptures=len(previous_checked),newlyComparedCaptures=len(set(checked)-previous_checked),
        previousFollowupComparedCaptures=len(before_current_followup),
        newlyComparedCapturesThisFollowup=len(set(checked)-before_current_followup),
        capturesWithoutComparedNumericScopes=inventory['captures']-len(checked),
        remainingCapturePayloadReview=None if review is None else dict(path=str(review_path.relative_to(ROOT)),
            sha256=sha(review_path),reviewedCaptures=review['captures'],
            capturesWithListedSolverPcmRawTypes=review['capturesWithListedSolverPcmRawTypes']),
        sampledTrajectory13WordStates=trajectory_states,
        sampledTrajectoryStateBytes=trajectory['totals']['denseBeforeTick.bytesCompared']+trajectory['totals']['tailBoundary.bytesCompared'],
        liveActorMembershipWindows=trajectory['totals']['membership.windows'],
        measuredMotionWindows=motion['totals']['compared'],
        legacyMotionCapturesWithComparedCalls=legacy['capturesWithComparedCalls'],
        legacyMotionWindows=legacy['totals']['compared'],
        legacyMotionWindowsWithSampledLinearOutput=legacy['totals']['withLinearOutput'],
        geometryNumericWindows=geometry['totals']['compared'],
        startupConstructorWindows=startup['totals']['compared'],
        startupConstructorWords=startup['totals']['wordsCompared'],
        resetPositionSetterInputs=position['totals']['compared'],
        convexPcmContactWindows=pcm['totals']['compared'],
        convexPcmPendingUnpairedWindows=pcm['pendingUnpairedWindows'],
        convexPcmUnsupportedWindows=[dict(path=r['path'],pending=r['pending']) for r in pcm['capturesInventory'] if r['pending']],
        measuredTransformAngularProjectionWindows=functions['totals']['angularProjection.bridge164.compared'],
        productionAngularSetterBodyPoseWindows=functions['totals']['angularSetterFromBodyPose.bridge164.compared'],
        resetCapturesWithComparedStates=sum(bool(r['checks'].get('compared')) for r in reset['capturesInventory']),
        reset13WordCoreStates=reset['totals']['compared'],
        normalizationFormulaWindows=functions['totals']['poseNormalization.compared'],
        unityGetterCaptureConsistencyEvents=functions['totals']['velocityGetter.velocity.outputBits.compared']+
            functions['totals']['velocityGetter.angularVelocity.outputBits.compared'],
        firstConfirmedDifferenceInComparedScopes=None,
        allLocalCapturesFullyAligned=False,
        existingRawTypesStillNeedingAdapters=dict(remaining),coverage=coverage,
        historicalTrajectoryWindowsNeedingHistoryAdapter=trajectory['pendingCaptures'],
        emptyOrUnusableResetWindows=reset['pendingCaptures'],
        sourceSha256={str(p.relative_to(ROOT)):sha(p) for p in sources},
        reportSha256={name:sha(OUT/name) for name in ('inventory.json','function_windows.json',
            'partial_trajectories.json','motion_windows.json','reset_windows.json','legacy_motion_windows.json','geometry_numeric_windows.json',
            'startup_windows.json','reset_position_inputs.json','pcm_windows.json')},
        boundaryRule='Initial dense angular setter cache output is before SetActive; do not compare it to native after-activation releaseBits. Original f73018 calls f73035 directly again during actor recreation.',
        limitations=['Counts include repeated captures of the same input, not that many independent shots.',
            'Unity getter memory consistency is observer validation, not a new simulator trajectory comparison.',
            'Current Unity wasm hash is the reference; older logs without binary hashes have unresolved per-capture version provenance.',
            'Archived diagnostic captures can contain reset.rotation_restored interventions; measured-input function equality does not certify untouched scenario replay or observer passivity.',
            'No new Unity sampling or physical-model change in this batch. Existing local raw solver/cache/geometry evidence is retained for the next specific adapters.'])
    (OUT/'report.json').write_text(json.dumps(result,indent=2),encoding='utf8')
    text='''# 本地局部 Unity 采样验收（2026-10-03）

按用户要求：已有局部采样可以作为验收依据，不要求每份日志都包含完整轨迹。没有抓到的字段不补造；只核对实际输入、调用阶段和实际输出。本轮没有新增 Unity 采样，没有修改生产物理。

盘点了 **{captures} 份 events.jsonl，{size} 字节**，其中 **{checked} 份日志**已有数值窗口接入本轮核对。

原先只接入 81 份，是比较器支持范围过窄且验收提前停止，并非剩余日志不能使用。上一轮扩展到 222 份后也提前停止；本次从此前未核对的 130 份中，又增加 **{followupnew} 份**。总计增加 **{newchecked} 份此前未核对日志**；仍有 **{unchecked} 份**没有接入数值比较，逐份保留实际事件类型及待处理原因，不能计入通过数量。

`remaining_capture_payload_review.json` 读取剩余日志实际 payload，保留每种事件的首次行号及字段结构。未核对项需逐项区分未完成适配器、缺少同一次调用输入/输出、只有安装或调度记录等情况，不按是否有完整轨迹排除整份日志。归档中存在 reset.rotation_restored 主动干预记录；局部同输入函数验算通过不等于原场景未经干预，也不证明串行前缀通过。

本轮已核对的范围全部逐位一致，没有确认新的分叉：

- **{trajectory} 份局部轨迹日志，{states:,} 个 P/Q/v/w 状态，{statebytes:,} 字节**。完整原生回放只使用同一布局、投掷和实测摩擦随机数；只比较 Unity 实际抓到的释放姿态、滑行前状态和完成边界。另核对 {membership:,} 个活动对象成员集合。
- **74 份日志的 {motion:,} 次滑行计算**：实测速度 getter 和摩擦随机数输入到脚本角速度 setter 输出，包含历史批次里的局部窗口。扫冰分支由原样例清单的 sent_sweep/requested.sweep 和实收命令核对。
- **{legacycaptures} 份旧格式日志的 {legacy:,} 个 A0/A2 调用阶段窗口**：同一次实测速度 getter、同 tick 摩擦随机数到角速度 setter，另有 {legacylinear:,} 个窗口同时核对线速度 setter；全部逐位一致。这与前面的日志有重叠，不相加为独立日志数量。归档样例通过采集 session 时间、实际 BESTSHOT/Reset 浮点输入与原样例清单匹配扫冰分支；缺少证据时留空。
- **{geometry} 个实测 Transform 矩阵/正式冰壶惯量窗口**，当前生产函数输出逐位一致。只核对采到且满足已还原分支的函数；其他物体质量属性、缺失层级或输入字段单独记录。早期协议超时采集中的同输入函数验算不证明该采集的整场轨迹透明性。
- **54 份日志的 {startup:,} 个初始冰壶构造器输入/输出窗口，{startupwords:,} 个数值字**逐位一致。Unity f71726 与当前原生 RVA 0x214bd0 同边界比较；指针、填充位、其他对象和更早工厂步骤未算入。原生有/无插桩初始化状态一致。
- **121 份日志的 {position:,} 个 Reset 位置 setter 输入**，由实际协议输入调用当前生产放置计算，三项 float32 全部逐位一致；不包含 setter 内部、旋转、物理步及先前历史。
- **9 份日志的 {pcm:,} 次凸包/凸包 PCM（f70576）**：将实测完整凸包、姿态、参数及持久缓存输入当前原生函数，接触点数量、法线、距离、位置与 face index 全部逐位一致。缺少成对快照或输入数组的调用逐项留空；不含未初始化临时字段与先前场景历史。
- **{angular:,} 次角速度投影**：使用实测 Transform 四元数和实测 setter 输入，两个内存输出位置都逐位一致。
- **{bodyangular:,} 次当前生产角速度设置路径**：使用实测刚体姿态和调用序号，核对两个内存输出。首次释放缺少约束分支证据的调用单独留空，不强套锁轴路径。
- **35 份日志的 {reset:,} 个 Reset 求解器入口/出口核心状态**全部逐位一致。原生采集器另外跑了一次无插桩 Reset，所有逐步状态相同，实际自然休眠为第 42 步。
- {norm} 对姿态归一化输入/输出算术逐位一致。{getter:,} 次 Unity getter 原始内存记录通过复制/不改写一致性检查；该数值仅是采样有效性检查。

这些数量包含同一案例的重复采集，不能解释为同样数量的独立投掷。局部函数通过也不自动证明此前整段场景历史通过。

**尚未宣称全部本地采样已通过。** 报告逐份保留了还需接入核对器的碰撞约束、求解器、PCM/缓存、几何等现成原始证据。历史批次的完整轨迹需要保留此前投掷与 Reset 历史，不能用新场景替代；它们已采到的函数窗口已经参与上面的函数验算。`unity_reset_core_bounded` 的 Reset 窗口只有空 cores，没有对应核心状态可比，但该日志的滑行窗口已经验算。

调用阶段必须一致：首次角速度缓存设置的 dense post 在 SetActive 前；f73018 重建 actor 时还会直接调用 f73035。它不能与 activation 完成后的 native releaseBits 混比。17 份旋转样例的这两个不同阶段数值不同，这不是相同边界的轨迹分叉，原始记录保存在 partial_trajectories.json。

结果：`local_partial_validation_20261003/report.json`。逐份路径、事件 SHA256、调用行号/序号、已比较范围、剩余证据均可复查；各函数范围分别保存在同目录下的 *_windows.json 和 reset_position_inputs.json。

复跑（仓库根目录）：

```powershell
D:\\anaconda3\\python.exe analysis_input/audit_all_local_partial_captures_20261003.py --reuse-inventory
D:\\anaconda3\\python.exe analysis_input/compare_local_motion_windows_20261003.py
D:\\anaconda3\\python.exe analysis_input/compare_local_partial_trajectories_20261003.py
D:\\anaconda3\\python.exe analysis_input/compare_local_reset_windows_20261003.py
D:\\anaconda3\\python.exe analysis_input/compare_legacy_motion_windows_20261003.py
D:\\anaconda3\\python.exe analysis_input/compare_local_geometry_numeric_windows_20261003.py
D:\\anaconda3\\python.exe analysis_input/compare_local_startup_windows_20261003.py
D:\\anaconda3\\python.exe analysis_input/compare_local_reset_position_inputs_20261003.py
D:\\anaconda3\\python.exe analysis_input/compare_local_pcm_windows_20261003.py
D:\\anaconda3\\python.exe analysis_input/summarize_local_partial_validation_20261003.py
D:\\anaconda3\\python.exe analysis_input/review_remaining_capture_payloads_20261003.py
D:\\anaconda3\\python.exe analysis_input/summarize_local_partial_validation_20261003.py
```

新增日志后，先运行 audit 脚本且不传 --reuse-inventory，重新扫描全部 events.jsonl。
'''.format(captures=result['inventoriedCaptures'],size=result['inventoriedBytes'],checked=len(checked),
    trajectory=result['sampledTrajectoryCaptures'],states=trajectory_states,statebytes=result['sampledTrajectoryStateBytes'],
    membership=result['liveActorMembershipWindows'],motion=result['measuredMotionWindows'],angular=result['measuredTransformAngularProjectionWindows'],
    bodyangular=result['productionAngularSetterBodyPoseWindows'],reset=result['reset13WordCoreStates'],
    norm=result['normalizationFormulaWindows'],getter=result['unityGetterCaptureConsistencyEvents'],
    newchecked=result['newlyComparedCaptures'],unchecked=result['capturesWithoutComparedNumericScopes'],
    followupnew=result['newlyComparedCapturesThisFollowup'],startup=result['startupConstructorWindows'],
    startupwords=result['startupConstructorWords'],position=result['resetPositionSetterInputs'],pcm=result['convexPcmContactWindows'],
    legacycaptures=result['legacyMotionCapturesWithComparedCalls'],legacy=result['legacyMotionWindows'],
    legacylinear=result['legacyMotionWindowsWithSampledLinearOutput'],geometry=result['geometryNumericWindows'])
    (ROOT/'analysis_input/local_partial_validation_20261003.md').write_text(text,encoding='utf8')
    print(json.dumps({k:v for k,v in result.items() if k in ('inventoriedCaptures','capturesWithComparedNumericScopes',
        'sampledTrajectoryCaptures','sampledTrajectory13WordStates','measuredMotionWindows','reset13WordCoreStates',
        'firstConfirmedDifferenceInComparedScopes','allLocalCapturesFullyAligned')},indent=2))
if __name__=='__main__':main()
