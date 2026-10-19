from typing import Self

from pydantic import BaseModel, model_validator


class CalculateRequest(BaseModel):
    numbers: list[int]
    delays: list[float]

    @model_validator(mode="after")
    def check(self) -> Self:
        if len(self.numbers) != len(self.delays):
            raise ValueError("Длина numbers должна совпадать с длиной delays")
        if any(d < 0 for d in self.delays):
            raise ValueError("Задержки в delays не могут быть отрицательными")
        return self


class CalculateResult(BaseModel):
    number: int
    square: int
    delay: float
    time: float


class CalculateResponse(BaseModel):
    results: list[CalculateResult]
    total_time: float
    parallel_faster_than_sequential: bool
