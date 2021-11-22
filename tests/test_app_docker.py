import pytest
import subprocess
import testinfra


@pytest.fixture(scope='session')
def host(request):
    # build local ./Dockerfile
    subprocess.check_call(['docker', 'build', '-t', 'bgapp:test', '--build-arg', 'VERSION=test', '.'])
    # run a container
    docker_id = subprocess.check_output(
        ['docker', 'run', '-d', 'bgapp:test']).decode().strip()
    # return a testinfra connection to the container
    yield testinfra.get_host("docker://" + docker_id)
    # at the end of the test suite, destroy the container
    subprocess.check_call(['docker', 'rm', '-f', docker_id])


def test_myimage(host):
    # 'host' now binds to the container
    assert host.file('/srv/app/version.env').content_string == "VERSION=test\n"