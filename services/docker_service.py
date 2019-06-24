import docker

client = docker.DockerClient(base_url='unix://var/run/docker.sock')


def search_containers(keyword):
    return client.images.search(keyword)
