import time
from .container import DockerHelperContainer


class DockerHelperTask(DockerHelperContainer):
    """
    Have the container execute some (computational) task and, when
    computation is done, terminate the container.
    """
    def run(self):
        self.set_run_arguments()
        super().run()
        self.get_container().wait()
        self.retrieve_output_and_errors()
        self.get_container().remove()

        # Because of caching issues for bind mounts on OSX, refer e.g. to
        # https://docs.docker.com/docker-for-mac/osxfs-caching/
        # the following check sometimes fails (although the file will
        # eventually "pop up" when the buffers get processed). We thus
        # introduce the following delay kludge:
        time.sleep(10)
