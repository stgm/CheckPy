_caches = []

class _Cache(object):
	def __init__(self):
		self._cache = {}
		_caches.append(self)

	def __setitem__(self, key, value):
		self._cache[key] = value

	def __getitem__(self, key):
		return self._cache.get(key, None)

	def __contains__(self, key):
		return key in self._cache
	
	def delete(self, key):
		if key not in self._cache:
			return False
		del self._cache[key]
		return True

	def clear(self):
		self._cache.clear()

"""
cache decorator
Caches input and output of a function. If arguments are passed to
the decorator, take those as key for the cache, otherwise the
function arguments.
"""
def cache(*keys):
	def cacheWrapper(func, localCache = _Cache()):
		def cachedFuncWrapper(*args, **kwargs):
			if keys:
				key = keys
			else:
				key = args + tuple(kwargs.values())

			if key not in localCache:
				localCache[key] = func(*args, **kwargs)

			return localCache[key]
		return cachedFuncWrapper
	return cacheWrapper

def clearAllCaches():
	for cache in _caches:
		cache.clear()