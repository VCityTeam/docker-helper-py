import sys
import docker
import requests
import logging
from abc import ABC, abstractmethod


class DockerHelperBase(ABC):
    """
    Helper class for docker manipulation, built on docker SDK library.
    """
    def __init__(self, image_name, tag):
        """
        :param image_name: image name (e.g. "3DCityDB")
        :param tag: tag of the image (e.g. "v4.0.2")
        """
        # Some methods of docker SDK need the image_name and/or the tag_name
        # independently while others need the full image name which is a
        # concatenation of these.
        self.image_name = image_name
        self.tag = tag
        self.full_image_name = image_name + ':' + tag
        self.client = None  # The name for the docker client (read server)
        self.assert_server_is_active()

    def assert_server_is_active(self):
        """
        Assert that a docker server is up and available
        :return: None, sys.exit() on failure
        """
        self.client = docker.from_env()
        try:
            self.client.ping()
        except (requests.exceptions.ConnectionError, docker.errors.APIError):
            logging.error('Unable to connect to a docker server:')
            logging.error('   is a docker server running on this host ?')
            sys.exit(1)

