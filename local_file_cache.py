"""Cache API calls using local file storage.

Class functions decorated with the @cache decorator will have their results cached in files in
the cache directory. This function only works for class methods where the arguments are json-
serializable.

Args:
    timeout: maximum cache time in seconds, defaults to a day
"""
def cache(timeout=86400):

    def decorator_cache(func):

        def wrapper_cache(self, *args, **kwargs):

            # Create cache hash from function name, args and kwargs
            cache_hash = hash(json.dumps((func.__name__, args, kwargs)).encode('utf-8'))
            path = '{}/cache/{}.txt'.format(DIRECTORY, cache_hash)

            # Check if cache exists, and if so, if it is recent.
            if os.path.exists(path):
                if os.path.getmtime(path) > time.time() - timeout:
                    with open(path) as infile:
                        return json.loads(infile.read())
                else:
                    os.remove(path)

            # Retrieve result and write to cache
            result = func(self, *args, **kwargs)
            with open(path, 'w') as outfile:
                outfile.write(json.dumps(result))

            return result
        return wrapper_cache
    return decorator_cache
