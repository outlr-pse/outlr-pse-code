import asyncio
import threading

from execution.odm_scheduler import ODMScheduler
from execution.experiment_scheduler.event_loop_experiment_scheduler import EventLoopExperimentScheduler


class BackgroundThreadEventLoopExperimentScheduler(EventLoopExperimentScheduler):
    """
    A specific ``EventLoopExperimentScheduler`` that creates a loop and runs it on a single new thread forever
    """

    @staticmethod
    def start_loop(loop: asyncio.AbstractEventLoop):
        asyncio.set_event_loop(loop)
        loop.run_forever()
        # print("BackgroundThreadEventLoopExperimentScheduler: Loop and thread stopped")

    def __init__(self, odm_scheduler: ODMScheduler):
        """
        Create a new ``BackgroundThreadEventLoopExperimentScheduler``.
        This will start a new thread on which a new event loop is run forever.
        Call ``EventLoopExperimentScheduler.stop`` to stop the event loop and consequently also the background thread.
        The ``stop`` method is automatically called when the scheduler is garbage collected.
        Args:
            odm_scheduler: The ``ODMScheduler`` that is used to schedule the execution of individual ODMs
        """
        super().__init__(odm_scheduler, asyncio.new_event_loop())

        # Create a new thread that runs the event loop forever
        # This might be better than letting the loop (and thread) stop, because experiments run all the time
        thread = threading.Thread(
            target=BackgroundThreadEventLoopExperimentScheduler.start_loop,
            args=(self.loop,)
        )
        # Maybe it would be better to make the thread a daemon thread (thread.daemon = True)
        thread.start()

    def __del__(self):
        # Since this scheduler object has started the loop,
        # it is responsible for stopping the loop when the scheduler is garbage collected
        self.stop()
