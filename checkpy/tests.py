import caches

class Test(object):
	def __init__(self, priority):
		self._priority = priority

	def __cmp__(self, other):
		return cmp(self._priority, other._priority)

	@caches.cache()
	def run(self):
		try:
			result = self.test()
			if type(result) == tuple:
				hasPassed, info = result
			else:
				hasPassed, info = result, ""
		except Exception as e:
			return TestResult(False, self.description(), self.exception(e))

		return TestResult(hasPassed, self.description(), self.success(info) if hasPassed else self.fail(info))
	
	@staticmethod
	def test():
		raise NotImplementedError()
	
	@staticmethod
	def description():
		raise NotImplementedError()
	
	@staticmethod
	def success(info):
		return ""
	
	@staticmethod    
	def fail(info):
		return info
		
	@staticmethod
	def exception(exception):
		return exception
		
		
class TestResult(object):
	def __init__(self, hasPassed, description, message):
		self._hasPassed = hasPassed
		self._description = description
		self._message = message
		
	@property
	def description(self):
		return self._description
	
	@property
	def message(self):
		return self._message
		
	@property
	def hasPassed(self):
		return self._hasPassed

def test(priority):
	def testDecorator(testCreator):
		@caches.cache(testCreator)
		def testWrapper():
			t = Test(priority)
			testCreator(t)
			return t
		return testWrapper
	return testDecorator


def failed(*precondTestCreators):
	def failedDecorator(testCreator):
		def testWrapper():
			test = testCreator()
			run = test.run
			test.run = lambda : run() if not any(t().run().hasPassed for t in precondTestCreators) else None
			return test
		return testWrapper
	return failedDecorator


def passed(*precondTestCreators):
	def passedDecorator(testCreator):
		def testWrapper():
			test = testCreator()
			run = test.run
			test.run = lambda : run() if all(t().run().hasPassed for t in precondTestCreators) else None
			return test
		return testWrapper
	return passedDecorator