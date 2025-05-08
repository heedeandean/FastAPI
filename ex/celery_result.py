from celery.result import AsyncResult
from common.messaging import celery

if __name__ == '__main__':
    async_result = AsyncResult('5b5134df-20b8-4c18-bca7-b201b01dcbb7', app=celery)
    result = async_result.result
    print(result)