import asyncio
import time

from fastapi import FastAPI
from schemas import CalculateRequest, CalculateResponse, CalculateResult

app = FastAPI(title="HW3 app")


@app.post("/calculate/", response_model=CalculateResponse)
async def calculate(request: CalculateRequest) -> CalculateResponse:
    start = time.perf_counter()

    tasks = []
    for i in range(len(request.numbers)):
        number = request.numbers[i]
        delay = request.delays[i]
        tasks.append(process_number(number, delay))

    results: list[CalculateResult] = await asyncio.gather(*tasks)

    end = time.perf_counter()
    total_time = end - start

    return CalculateResponse(
        results=results,
        total_time=round(total_time, 2),
        parallel_faster_than_sequential=total_time < sum(request.delays),
    )


async def process_number(number: int, delay: float) -> CalculateResult:
    start = time.perf_counter()
    await asyncio.sleep(delay)
    square = number**2
    end = time.perf_counter()
    processing_time = end - start

    return CalculateResult(
        number=number,
        square=square,
        delay=delay,
        time=round(processing_time, 2),
    )
