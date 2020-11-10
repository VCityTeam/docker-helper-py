import time
from docker_helper import DockerHelperPull, DockerHelperService


class PostgresServer(DockerHelperPull, DockerHelperService):

    def __init__(self):
        super().__init__('postgres', '13.0')
        self.pull()
        self.container_name = 'my_postgres-13'

    def get_command(self):
        # No command is declared here since the command is already set
        # by default (in the Dockerfile) for this container
        return None


if __name__ == '__main__':
    print('Pulling or building the container.') 
    server = PostgresServer()
    print('Launching the container as service.')
    server.run()
    print(f'Using the {server.get_container().name} container: ', end="")
    for i in range(10):
        print(".", end="")
        time.sleep(1)
    print('')
    print('Halting the service.')
    server.halt_service()
    print('Exiting.')