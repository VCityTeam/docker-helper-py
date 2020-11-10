import os
import sys
import logging
import time
from abc import ABC, abstractmethod
import .base


class DockerHelperContainer(DockerHelperBase):
    """
    Helper class for docker containers. Helps input / outputs
    management, volumes management and running containers
    """
    def __init__(self, image_name, tag):
        super().__init__(image_name, tag)
        self.container_name = None
        self.mounted_input_dir = os.getcwd()
        self.mounted_output_dir = os.getcwd()
        # Some containers (like 3DUse) provide multiple commands each of
        # which might require its proper working directory (i.e. the WORKDIR
        # variable of the Dockerfile)
        self.working_dir = None
        self.volumes = dict()
        self.environment = None      # Docker run environment variables
        self.run_arguments = dict()  # The arguments handled over to the run()

        self.__container = None

    def set_mounted_input_directory(self, directory):
        if not os.path.isdir(directory):
            logging.info(f'Input dir to mount {directory} not found. Exiting')
            sys.exit(1)
        self.mounted_input_dir = directory

    def get_mounted_input_directory(self):
        return self.mounted_input_dir

    def set_mounted_output_directory(self, directory):
        if not os.path.isdir(directory):
            logging.info(f'Output dir to mount {directory} not found. Exiting')
            sys.exit(1)
        self.mounted_output_dir = directory

    def get_mounted_output_directory(self):
        return self.mounted_output_dir

    def get_container(self):
        if not self.__container:
            logging.info('Warning: requesting an unset container.')
        return self.__container

    def add_volume(self, host_volume, inside_docker_volume, mode):
        """
        :param host_volume: The host path (must be absolute) or
        the volume name (must have been created earlier with
        docker volume create) to bind the data to.
        :param inside_docker_volume: The path to mount
        the volume inside the container.
        :param mode: Volume access mode which is either
        'rw' for 'read write' or 'ro' for read-only.
        """
        if not os.path.isdir(host_volume):
            logging.error(f'No such host directory {host_volume}. Exiting')
            sys.exit(1)
        if not os.path.isabs(host_volume):
            logging.error(f'Host directory {host_volume} is not absolute.'
                          'Exiting')
            sys.exit(1)
        if not os.path.isabs(inside_docker_volume):
            logging.error(f'Mount point {inside_docker_volume} is not absolute.'
                          ' Exiting')
            sys.exit(1)
        self.volumes[host_volume] = {'bind': inside_docker_volume, 'mode': mode}

    @abstractmethod
    def get_command(self):
        raise NotImplementedError()
    
    def set_run_arguments(self):
        """
        Sets common arguments passed to the run method of the docker SDK lib.
        Other arguments can be set by child classes, e.g. the
        DockerHelperService class sets the 'ports' argument.
        """
        self.run_arguments = dict(
            # command=["/bin/sh", "-c", "ls /Input /Output"],      # for debug
            command=self.get_command(),
            volumes=self.volumes,
            working_dir=self.working_dir,
            stdin_open=True,
            stderr=True,
            detach=True,
            tty=True
        )

        if self.container_name:
            containers = self.client.containers.list(
                filters={'name': self.container_name})
            if containers:
                logging.error(f'A container named {self.container_name} already exists.')
                logging.error('With some understanding of docker and in despair '
                              'you might try this command:')
                logging.error(f'   docker stop {self.container_name} && '
                              f'docker rm {self.container_name}')
                logging.error('Exiting.')
                sys.exit(1)
            self.run_arguments['name'] = self.container_name

        if self.environment:
            self.run_arguments['environment'] = self.environment
        if self.working_dir:
            self.run_arguments['working_dir'] = self.working_dir

    def run(self):
        """
        Prepare the information required to launch the container and run it
        (always in a detached mode, for technical reasons).
        """
        self.__container = self.client.containers.run(
            self.full_image_name,
            **self.run_arguments)

    def retrieve_output_and_errors(self):
        out = self.__container.logs(stdout=True, stderr=False)
        if out:
            logging.info('Docker run standard output follows:')
            logging.info(f'docker-stdout> {out}')
        err = self.__container.logs(stdout=False, stderr=True)
        if err:
            logging.info('Docker run standard error follows:')
            logging.info(f'docker-stderr> {err}')
