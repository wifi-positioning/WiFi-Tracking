from multiprocessing import Process

class Locator(Process):

	def __init__(self, locator_queue, config):
		super().__init__()
		self._locator_queue = locator_queue

	def run(self):
		while True:
			print(self._locator_queue.get())