"""Same-input calls to the current native PCM function; no Scene simulation."""
import hashlib,json,struct,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx,_resolve_bundled_extension
install_bundled_pyphysx()
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene
def bits(v):return list(struct.unpack('<%dI'%len(v),struct.pack('<%df'%len(v),*v)))
def main():
    requests=json.loads(Path(sys.argv[1]).read_text(encoding='utf8'));scene=PersistentPhysxFrontHalfScene(stone_count=2)
    replies=[]
    for request in requests:
        pcm=request['before'];reply=dict(key=request['key']);reason=None
        for i in range(2):
            source=pcm['shape'+str(i)];g=source['decoded'];slot=scene.slots[i]
            if g['geometryType']!=4 or g['scaleRotation']!=[0,0,0,1] or g['meshFlags']!=1:
                reason='Captured geometry outside the verified formal convex/identity-scale-rotation branch.';break
            runtime=source.get('hullRuntime') or {};hull=(runtime.get('runtimeBufferWindow') or {}).get('rawBytes')
            if hull is None:
                reason='Captured complete hull bytes unavailable.';break
            if bytes(hull)!=bytes(scene._stone_runtime_hull):
                reason='Captured complete hull bytes differ from current formal hull; a measured-hull adapter is required.';break
            if bits(slot.geometry_scale)!=bits(g['scale']):
                previous=slot.shape
                shape=scene.pyphysx.Shape.create_convex_mesh_from_points_with_scale(scene._stone_shape_points,slot.material,True,g['scale'],255,255,False,False)
                scene.probe._patch_runtime_stone_shape(shape,runtime_hull_raw_bytes=scene._stone_runtime_hull,runtime_big_convex_arrays=scene._stone_runtime_bigconvex)
                shape.set_local_pose(previous.get_local_pose());shape.set_contact_offset(previous.get_contact_offset());shape.set_rest_offset(previous.get_rest_offset())
                slot.body.detach_shape(previous);slot.body.attach_shape(shape);slot.shape=shape;slot.geometry_scale=g['scale']
            info=slot.shape.get_convex_mesh_runtime_hull_data();u=source.get('hullData')
            mapping={'aabbCenter':'aabb_center','aabbExtents':'aabb_extents','centerOfMass':'center_of_mass'}
            if not u or any(bits(u[k])!=bits(info[v]) for k,v in mapping.items()) or any(u[k]!=info[v] for k,v in {'nbEdges':'nb_edges','nbHullVertices':'nb_hull_vertices','nbPolygons':'nb_polygons'}.items()):
                reason='Captured hull header differs from actual native geometric input.';break
            arrays=runtime.get('bigConvexRawDataArrays') or {}
            for name,window in {'samples_raw_bytes':'samplesWindow','valencies_raw_bytes':'valenciesWindow','adjacent_vertices_raw_bytes':'adjacentVertsWindow'}.items():
                observed=(arrays.get(window) or {}).get('rawBytes')
                if observed is None:
                    reason='Captured full BigConvex support input unavailable: '+window;break
                if bytes(observed)!=bytes(scene._stone_runtime_bigconvex[name]):
                    reason='Captured full BigConvex support input differs from formal input: '+window;break
            if reason:break
            pose=pcm['transform'+str(i)]['decoded'];q=pose['q'];slot.body.set_global_pose((pose['p'],[q[3],q[0],q[1],q[2]]))
        if reason:reply['pendingReason']=reason;replies.append(reply);continue
        cache=pcm['cache'];decoded=cache['decoded']
        if decoded['isMultiManifold'] or not decoded['isManifold']:
            reply['pendingReason']='Actual cache is not the captured single persistent manifold branch.';replies.append(reply);continue
        seed=(cache.get('manifoldWindow') or {}).get('rawBytes')
        if decoded['cachedDataPtr'] and seed is None:
            reply['pendingReason']='Actual nonempty cache pointer has no captured input bytes.';replies.append(reply);continue
        if pcm['contactBuffer']['decoded']['count']!=0:
            reply['pendingReason']='Nonempty initial contact buffer requires an append-state adapter.';replies.append(reply);continue
        p=pcm['narrowPhaseParams']['decoded']
        result=scene.pyphysx.generate_contacts_between_direct_pcm_cache_step(scene.slots[0].body,scene.slots[0].shape,scene.slots[1].body,scene.slots[1].shape,
            seed,p['contactDistance'],p['meshContactMargin'],p['toleranceLength'])
        for i in range(2):
            original=pcm['transform'+str(i)]['decoded'];actual=result['input_transform'+str(i)]
            assert bits(original['p']+original['q'])==bits(actual['p']+actual['q']),'Native query changed captured input pose'
        reply.update(actual=result,measuredPoseInputsUnchanged=True)
        replies.append(reply)
    output=dict(replies=replies,nativeModuleSha256=hashlib.sha256(_resolve_bundled_extension().read_bytes()).hexdigest(),
        productionSourceSha256=hashlib.sha256((ROOT/'local_simulator/unity_physx.py').read_bytes()).hexdigest(),
        scope='Observed PCM pose/scale/params/cache input -> current bundled native kernel. No historical state or full-scene replay claim.')
    Path(sys.argv[2]).write_text(json.dumps(output),encoding='utf8')
    print(json.dumps(dict(requests=len(requests),compared=sum('actual' in r for r in replies),pending=sum('pendingReason' in r for r in replies))))
if __name__=='__main__':main()
