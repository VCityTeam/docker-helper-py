import os
import sys
import docker
import logging
from base import DockerHelperBase


class DockerHelperPull(DockerHelperBase):
    """
    Pull an image from a well known docker registry
    """
    def pull(self):
        """
        Provision the docker image by pulling it from some well know docker
        registry (stored in self.repository).
        """
        try:
            self.client.images.pull(repository=self.image_name, tag=self.tag)
            logging.info(f'Docker pulling image: {self.full_image_name}')
            logging.info(f'Docker pulling image done.')
        except docker.errors.APIError as err:
            logging.error('Unable to build the docker image: with error')
            logging.error(f'   {err}')
            sys.exit(1)

