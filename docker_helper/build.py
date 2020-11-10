import os
import sys
import docker
import logging
from .base import DockerHelperBase


class DockerHelperBuild(DockerHelperBase):
    """
    Build an image from a local Docker context
    """
    def build(self, context_dir):
        """
        Provision the docker image by building it.
        """
        if not os.path.exists(context_dir):
            logging.error(f'Context directory {context_dir} not found.')
            sys.exit(1)

        try:
            # Note: The tag argument is not self.tag since it is not the
            # version of the image that is expected here but the full image
            # name; i.e. here we "tag" the built image with the full image name.
            result = self.client.images.build(
                path=context_dir,
                tag=self.full_image_name)
            logging.info(f'Docker building image: {self.full_image_name}')
            for line in result:
                logging.info(f'    {line}')
            logging.info(f'Docker building image done.')
        except docker.errors.APIError as err:
            logging.error('Unable to build the docker image: with error')
            logging.error(f'   {err}')
            sys.exit(1)
        except TypeError:
            logging.error('Building the docker image requires path or fileobj.')
            sys.exit(1)

