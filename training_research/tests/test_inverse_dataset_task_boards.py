import unittest

from training_research.inverse_dataset.sampling import deduplicate_scenes, validate_scene
from training_research.inverse_dataset.schema import split_for_group
from training_research.inverse_dataset.task_boards import TASK_FAMILIES, task_boards


class TaskBoardTests(unittest.TestCase):
    def test_diverse_valid_reproducible_boards_and_neighbourhood_groups(self):
        scenes = task_boards(4, 2, 123, 8)
        self.assertEqual(scenes, task_boards(4, 2, 123, 8))
        self.assertEqual(len(scenes), len(TASK_FAMILIES) * 8)
        self.assertEqual(len({s['scene_key'] for s in scenes}), len(scenes))
        self.assertGreater(len({s['active_index'] for s in scenes}), 5)
        self.assertGreater(len({len(s['stones']) for s in scenes}), 5)
        for before, variant in zip(scenes[::2], scenes[1::2]):
            self.assertEqual(before['group_id'], variant['group_id'])
            self.assertEqual(split_for_group(before['group_id'], 123), split_for_group(variant['group_id'], 123))
            self.assertNotEqual(before['scene_key'], variant['scene_key'])
            self.assertNotEqual(before['task_key'], variant['task_key'])
        for scene in scenes:
            self.assertEqual(validate_scene(scene), scene)

    def test_same_board_distinct_goals_preserved_and_groups_unioned(self):
        a = validate_scene({'active_index': 6, 'stones': [], 'group_id': 'a',
            'selection': {'tactic': 'draw_button', 'goal': {'stones': {'6': {'type': 'IN_REGION', 'x': 2.375, 'y': 4.88, 'radius': .3}}}}})
        b = validate_scene({'active_index': 6, 'stones': [], 'group_id': 'b',
            'selection': {'tactic': 'center_guard', 'goal': {'stones': {'6': {'type': 'IN_REGION', 'x': 2.375, 'y': 8., 'radius': .3}}}}})
        neighbour = validate_scene({'active_index': 6, 'stones': [{'index': 1, 'x': 3., 'y': 6.}], 'group_id': 'b'})
        result = deduplicate_scenes([a, b, neighbour, a])
        self.assertEqual(len(result), 3)
        self.assertEqual(len({s['group_id'] for s in result}), 1)
        self.assertEqual(a['scene_key'], b['scene_key'])
        self.assertNotEqual(a['task_key'], b['task_key'])


if __name__ == '__main__':
    unittest.main()
