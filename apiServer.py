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


@app.get("/")
async def root():
    return {"message", "it's working"}


class Information:
    def __init__(self, text, value: int = 1):
        self.text = text
        self.value = value


class Function:
    ALPHABET = string.ascii_lowercase
    points = list(string.ascii_uppercase[15:])

    def __init__(self, grade_range: tuple, parameter_range: tuple, letters: tuple = ('f', 'x'), grade_parameter_lowering: bool = False):
        grade = random.randint(*grade_range)
        self.parameters = [random.randint(*parameter_range) for _ in range(grade + 1)]
        if grade_parameter_lowering and len(self.parameters) > 4:
            self.parameters = [round(random.random() * 2 - 1, 2) if i < (len(self.parameters) - 4) else e for i, e in enumerate(self.parameters)]
        self.letters = letters

    def insert(self, insertion_value: int | float):
        return sum([parameter * insertion_value ** (len(self.parameters)-1-i) for i, parameter in enumerate(self.parameters)])

    def calculate_zeros(self, calculation_range: range = None):
        if calculation_range is None:
            calculation_range = (-10*self.grade, 10*self.grade)
        zeros = []
        for i in calculation_range:
            current_value = self.insert(i)
            if current_value == 0:
                zeros.append(i)
        return zeros

    def make_task(self):
        wrapper_text = random.randint(0, 4)
        match wrapper_text:
            case 0:
                task = f"""
                Bestimmen sie die Parameter {", ".join(self.ALPHABET[0:len(self.parameters)])} so, dass der Graph der Funktion \n
                {self.veiled}\n
                """
            case 1:
                task = f"""
                Bestimmen sie eine Funktion {self.grade}. Grades so, dass sie 
                """
            case 2:
                task = f"""
                Ist es möglich, die Parameter {", ".join(self.ALPHABET[0:len(self.parameters)])} so zu bestimmen, dass die Funktion {self.letters[0]} 
                """
            case 3:
                task = f"""
                Gegeben ist die Funktion {self.veiled}.\n
                Bestimmen Sie die Parameter so, dass die Funktion 
                """
            case 4:
                task = f"""
                Geben sie ein möglichst einfache Funktion an, die 
                """
            case _:
                task = ""

        values_available = []
        for i in range(-100 - self.grade, 100 + self.grade):
            values_available.append((i, self.insert(i)))
        values_available.sort(key=lambda e: abs(e[1]))
        values_available = values_available[:-(len(values_available) - self.grade - 2)]
        special = []

        match random.randint(0, 1):
            case 0:
                special.append(
                    f"die y-Achse bei y = {self.insert(0)} schneidet"
                )
            case 1:
                special.append(
                    f"bei y = {self.insert(0)} durch die y-Achse läuft"
                )
        values_available = list(filter(lambda e: e[0] != 0, values_available))

        for i in self.calculate_zeros():
            match random.randint(0, 1):
                case 0:
                    special.append(
                        f"eine Nullstelle bei x = {i} hat"
                    )
                case 1:
                    special.append(
                        f"die x-Achse bei x = {i} schneidet"
                    )
            values_available = list(filter(lambda e: e[0] != i, values_available))
        for i in self.derived.calculate_zeros():
            match random.randint(0, 5):
                case 0:
                    special.append(
                        f"an der Stelle x = {i} eine Steigung von m = 0 hat"
                    )
                case 1:
                    special.append(
                        f"an der Stelle x = {i} ein lokales Extrema hat"
                    )
                case 2:
                    special.append(
                        f"eine horizontale Tangente an der Stelle x = {i} hat"
                    )
                case 3 | 4 | 5:
                    current_2nd_derived_value = self.derived.derived.insert(i)
                    if current_2nd_derived_value == 0:
                        special.append(
                            f"einen {'Sattelpunkt' if random.randint(0, 1) else 'Terrassenpunkt'} an der Stelle x = {i} hat"
                        )
                    elif current_2nd_derived_value < 0:
                        special.append(
                            f"einen Hochpunkt an der Stelle x = {i} hat"
                        )
                    elif current_2nd_derived_value > 0:
                        special.append(
                            f"einen Tiefpunkt an der Stelle x = {i} hat"
                        )

        i = values_available.pop(random.randint(0, len(values_available) - 1))[0]
        derived_value = self.derived.insert(i)
        match 0:
            case 0:
                special.append(
                    f"bei x = {i} eine Steigung von m = {derived_value} hat"
                )
        
        informations = []
        for _ in range(self.grade + 1):
            if len(special) >= 1:
                match random.randint(0, 3):
                    case 0 | 1 | 2:
                        informations.append(special.pop(random.randint(0, len(special) - 1)))
                    case 3:
                        point = values_available.pop(random.randint(0, len(values_available) - 1))
                        informations.append(
                            f"durch den Punkt {self.get_point()}({point[0]}| {point[1]}) geht"
                        )

            else:
                point = values_available.pop(random.randint(0, len(values_available) - 1))
                informations.append(
                    f"durch den Punkt {self.get_point()}({point[0]}| {point[1]}) geht"
                )

        task += ", ".join(informations[:-1]) + " und " + informations[-1]

        match wrapper_text:
            case 0 | 1 | 3 | 4:
                task += "."
            case 2:
                task += "?"

        match random.randint(0, 5):
            case 5:
                task += "\nIst die Funktion damit eindeutig bestimmt?"

        return task

    def get_point(self):
        self.points = self.points[1:] + [self.points[0]]
        return self.points[-1]

    @property
    def solved(self):
        return (
                f"{self.letters[0]}({self.letters[1]})= " +
                " + ".join([
                    f"{e}*{self.letters[1]}^{len(self.parameters) - i - 1}" for i, e in enumerate(self.parameters)
                ])
        ).replace(f"*{self.letters[1]}^0", "").replace(f"{self.letters[1]}^1", self.letters[1])

    @property
    def veiled(self):
        return (
                f"{self.letters[0]}({self.letters[1]})= " +
                " + ".join([
                    f"{self.ALPHABET[i]}*{self.letters[1]}^{len(self.parameters) - i - 1}" for i, e in enumerate(self.parameters)
                ])
        ).replace(f"*{self.letters[1]}^0", "").replace(f"{self.letters[1]}^1", self.letters[1])

    @property
    def derived(self):
        derived_function = Function((0, 1), (-4, 5))
        derived_function.parameters = [e * (len(self.parameters) - i - 1) for i, e in enumerate(self.parameters) if len(self.parameters) - i - 1 != 0]
        return derived_function

    @property
    def grade(self):
        return len(self.parameters) - 1


class FunctionPreferences(BaseModel):
    grade_min: int = 2,
    grade_max: int = 3,
    param_min: int = -4,
    param_max: int = 5,
    parameter_lowering: bool = False


@app.post("/generate/function")
async def generate_function(preferences: FunctionPreferences):
    working_function = Function(
        grade_range=(preferences.grade_min, preferences.grade_max),
        parameter_range=(preferences.param_min, preferences.param_max),
        grade_parameter_lowering=preferences.parameter_lowering
    )
    return {
        "task": working_function.make_task(),
        "function_solved": working_function.solved,
    }


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
