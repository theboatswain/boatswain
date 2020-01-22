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
