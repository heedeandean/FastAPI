import time
from fastapi import Request, FastAPI

def create_sample_middleware(app: FastAPI):

    # middleware: HTTP 요청과 응답이 처리되기 전에 실행되는 함수
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response