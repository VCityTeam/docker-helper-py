import os
import sys
import docker
import logging
import time
import .container


class DockerHelperService(DockerHelperContainer):
    """
    Have the container run a server and serve until explicit termination
    is required.
    """
    def __init__(self, image_name, tag):
        super().__init__(image_name, tag)
        self.ports = None
        self.stop_arguments = dict()

    def add_stop_argument(self, key, value):
        self.stop_arguments[key] = value

    def halt_service(self):
        try:
            self.get_container().stop(**self.stop_arguments)
        except docker.errors.APIError:
            logging.error('Container stop failed '
                          f'(arguments used: {self.stop_arguments}).')
        self.retrieve_output_and_errors()
        self.get_container().remove()

    def run(self):
        self.set_run_arguments()
        if self.ports:
            self.run_arguments['ports'] = self.ports
        super().run()

