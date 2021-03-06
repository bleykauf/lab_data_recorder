"""Classes and functions related to the Recorder part of LDR."""

import logging
from multiprocessing import Queue

import rpyc

from .common import Netloc
from .puller import Puller
from .writers import Writer

logger = logging.getLogger("lab_data_recorder.recorder")


JOIN_TIMEOUT = 1  # timeout for joining processes


class RecorderService(rpyc.Service):
    def __init__(self) -> None:
        """
        Service comprised of a Writer, various Pullers and methods for managing them.
        """
        super(RecorderService, self).__init__()
        self.queue = Queue()
        self.connected_sources = {}

    def set_writer(self, writer: Writer) -> None:
        """
        Set the writer of the recorder.
        """
        self.writer = writer
        self.writer.connect_queue(self.queue)
        self.writer.write_process.start()
        logger.debug("Writer process started.")

    def connect_source(
        self,
        netloc: Netloc,
        interval: float,
        measurement: str,
        tags: list[str] = [],
        requested_fields: list[str] = [],
    ) -> None:
        """
        Connect to a LabDataService and start pulling data.
        """
        if netloc in self.connected_sources.keys():
            logger.error(f"{netloc!s} is already connected.")
        else:
            puller = Puller(
                queue=self.queue,
                netloc=netloc,
                interval=interval,
                measurement=measurement,
                requested_fields=requested_fields,
                tags=tags,
            )
            logger.info(f"Starting pull process for {netloc!s}.")
            puller.pull_process.start()
            self.connected_sources[netloc] = puller

    def disconnect_source(self, netloc: Netloc) -> None:
        """Stop and remove a puller from the logger."""
        try:
            puller = self.connected_sources[netloc]
            # shutting down via Event
            puller.stop_event.set()
            puller.pull_process.join(JOIN_TIMEOUT)
            if puller.pull_process.is_alive():
                # if not successful, terminate
                puller.pull_process.terminate()
            logger.info(
                "Puller process for {} exited with code {}.".format(
                    netloc, puller.pull_process.exitcode
                )
            )
            del self.connected_sources[netloc]
        except KeyError:
            logger.error(f"No Puller pulling from {netloc}")
