from unittest import TestCase

from boatswain.common.utils import docker_utils


class TestDockerUtils(TestCase):

    def test_generate_tag_map(self):
        tag_map = docker_utils.generateTagMap('nginx', '1.17.6-alpine-perl'.split('.'))
        desired_map = {'nginx:1.x.x': {'nginx:1.17.x': {'nginx:1.17.6': {'nginx:1.17.6-alpine-perl': 1}}}}
        self.assertDictEqual(desired_map, tag_map)

        tag_map = docker_utils.generateTagMap('nginx', 'mainstream-perl'.split('.'))
        self.assertDictEqual({'nginx:mainstream': {'nginx:mainstream-perl': 1}}, tag_map)

    def test_parse_tag_map(self):
        tag_map = docker_utils.parseTagMap('nginx', '1.17.6-alpine-perl')
        desired_map = {'nginx:1': {'nginx:1.x.x': {'nginx:1.17.x': {'nginx:1.17.6': {'nginx:1.17.6-alpine-perl': 1}}}}}
        self.assertDictEqual(desired_map, tag_map)

    def test_merge_tag_map(self):
        tag_map = {}
        for tag in ['1.17.6-alpine-perl', 'mainstream-perl', 'latest', '1.17-alpine']:
            tag_map = docker_utils.mergeTagMap(tag_map, docker_utils.parseTagMap("nginx", tag))
        desired_map = {
            'nginx:1': {
                'nginx:1.x.x': {
                    'nginx:1.17.x': {
                        'nginx:1.17.6': {'nginx:1.17.6-alpine-perl': 1}
                    }
                },
                'nginx:1.x': {
                    'nginx:1.17': {'nginx:1.17-alpine': 1}
                }
            },
            'nginx:mainstream': {'nginx:mainstream-perl': 1},
            'nginx:latest': 1
        }
        self.assertDictEqual(desired_map, tag_map)

