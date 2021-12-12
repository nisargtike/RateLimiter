import time
import redis

# redis connection
def get_connection(host="127.0.0.1", port="6379", db=0):
	connection = redis.StrictRedis(host=host, port=port, db=db)
	return connection

class SlidingWindowCounterRateLimiter(object):

	LIMITER_RULES = [
		{
			"windowTime": 1,
			"maxRequests": 10,
			"bucketSize": 1,
			"type": "user"
		},
		{
			"windowTime": 6,
			"maxRequests": 20,
			"bucketSize": 5,
			"type": "user"
		},
		{
			"windowTime": 3600*24,
			"maxRequests": 6000,
			"bucketSize": 360*24,
			"type": "user"
		},
		{
			"windowTime": 1,
			"maxRequests": 200,
			"bucketSize": 1,
			"type": "host"
		}
	]
	
	def __init__(self, bucketSize=10):
		self.con = get_connection()

	@classmethod
	def getCurrentTimestampInSec(cls):
		return int(round(time.time()))

	def getBucket(self, timestamp, windowTimeInSec, bucketSize):
		factor = windowTimeInSec / bucketSize
		return (timestamp // factor) * factor

	def _incrementAHashKeyValByUnitAtomically(self, cache_key, bucket, redisPipeline):
		count = redisPipeline.hmget(cache_key, bucket)[0]
		if count is None:
			count = 0
		currentBucketCount = int(count)
		redisPipeline.multi()
		redisPipeline.hmset(cache_key, {bucket: currentBucketCount + 1})
		redisPipeline.hvals(cache_key)

	def shouldAllowServiceCall(self, userId, ip):

		limiter_rules = self.LIMITER_RULES
		for limiter_rule in limiter_rules:
			allowedRequests = limiter_rule["maxRequests"]
			windowTime = limiter_rule["windowTime"]
			bucketSize = limiter_rule["bucketSize"]
			limiter_type = limiter_rule["type"]

			cache_key = ""
			if limiter_type=="user":
				cache_key = userId + "_" + str(windowTime)
			else:
				cache_key = ip + "_" + str(windowTime)

			allBuckets = map(int, self.con.hkeys(cache_key))
			currentTimestamp = self.getCurrentTimestampInSec()
			oldestPossibleEntry = currentTimestamp - windowTime

			bucketsToBeDeleted = filter(lambda bucket: bucket < oldestPossibleEntry, allBuckets)

			if len(bucketsToBeDeleted) != 0:
				self.con.hdel(cache_key, *bucketsToBeDeleted)

			currentBucket = self.getBucket(currentTimestamp, windowTime, bucketSize)

			_, requests = self.con.transaction(
			    lambda pipe: self.
			    _incrementAHashKeyValByUnitAtomically(cache_key, currentBucket, pipe),
			    cache_key, currentBucket
			)
			if sum(map(int, requests)) > allowedRequests:
				return False
		return True