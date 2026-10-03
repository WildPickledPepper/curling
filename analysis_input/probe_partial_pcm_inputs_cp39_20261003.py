import json,sys,struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from local_simulator.runtime_loader import install_bundled_pyphysx
install_bundled_pyphysx()
from local_simulator.unity_physx import PersistentPhysxFrontHalfScene
def main():
    pcm=json.loads((ROOT/'analysis_input/remaining_pcm_first_input_20261003.json').read_text())
    scene=PersistentPhysxFrontHalfScene(stone_count=2)
    for i in range(2):
        s=scene.slots[i];g=pcm['shape'+str(i)]['decoded'];pose=pcm['transform'+str(i)]['decoded']
        info=s.shape.get_convex_mesh_runtime_hull_data()
        print('HULL',i,{k:v for k,v in info.items() if k in ('aabb_center','aabb_extents','center_of_mass','scale','scale_rotation_xyzw','mesh_flags','nb_edges','nb_hull_vertices','nb_polygons')})
        q=pose['q'];s.body.set_global_pose((pose['p'],[q[3],q[0],q[1],q[2]]))
        actual=s.body.get_global_pose();print('POSE',list(actual[0]),[actual[1].x,actual[1].y,actual[1].z,actual[1].w])
    p=pcm['narrowPhaseParams']['decoded']
    seed=pcm['cache']['manifoldWindow']['rawBytes']
    result=scene.pyphysx.generate_contacts_between_direct_pcm_cache_step(scene.slots[0].body,scene.slots[0].shape,scene.slots[1].body,scene.slots[1].shape,
        seed,p['contactDistance'],p['meshContactMargin'],p['toleranceLength'])
    print('RESULT',json.dumps({k:v for k,v in result.items() if 'raw' not in k})[:9000])
    (ROOT/'analysis_input/remaining_pcm_first_native_20261003.json').write_text(json.dumps(result),encoding='utf8')
if __name__=='__main__':main()
