from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import string


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ALPHABET = string.ascii_lowercase


def calculate_point(params, x):
    y = sum([param * x**(len(params)-1-i) for i, param in enumerate(params)])
    return x, y


@app.get("/")
async def root():
    return {"message", "it's working"}


class Body(BaseModel):
    grade_min: int = 2,
    grade_max: int = 3,
    param_min: int = -4,
    param_max: int = 5,


@app.post("/generate/function")
async def generate_function(body: Body):
    function_letters = ('y', 'x',)
    function_grade = random.randint(body.grade_min, body.grade_max)

    # function_params = [random.random() * (param_max - param_min) + param_min for _ in range(function_grade + 1)]
    function_params = [random.randint(body.param_min, body.param_max) for _ in range(function_grade + 1)]

    function_solved = (
            f"{function_letters[0]}({function_letters[1]})= " +
            " + ".join([
                f"{e}*{function_letters[1]}^{len(function_params) - i - 1}" for i, e in enumerate(function_params)
            ])
    ).replace(f"*{function_letters[1]}^0", "").replace(f"{function_letters[1]}^1", function_letters[1])
    function_veiled = (
            f"{function_letters[0]}({function_letters[1]})= " +
            " + ".join([
                f"{ALPHABET[i]}*{function_letters[1]}^{len(function_params) - i - 1}" for i, e in enumerate(function_params)
            ])
    ).replace(f"*{function_letters[1]}^0", "").replace(f"{function_letters[1]}^1", function_letters[1])
    points_available = list(range(0 - function_grade, 2 + function_grade))
    points = []
    for _ in range(len(function_params)):
        points.append(calculate_point(function_params, points_available.pop(random.randint(0, len(points_available) - 1))))
    task = f"""
    Bestimmen sie die Parameter {", ".join(ALPHABET[0:len(function_params)])} so, dass der Graph der Funktion \n
    {function_veiled}\n 
    durch die Punkte {', '.join([f"({point[0]}|{point[1]})" for point in points])} geht.
    """
    return {
        "task": task,
        "grade": function_grade,
        "function_solved": function_solved,
        "function_veiled": function_veiled,
        "parameters": function_params,
        "points": points
    }


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
