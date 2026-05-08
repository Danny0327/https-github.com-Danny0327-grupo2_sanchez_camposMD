import json
import os
import time
from datetime import date, timedelta

import requests
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")

BASE_URL = "https://api.nasa.gov"

if not NASA_API_KEY:
    raise Exception("NASA_API_KEY no configurada")


def request_json(path: str, params: dict, retries: int = 3):

    params = dict(params)
    params["api_key"] = NASA_API_KEY

    url = f"{BASE_URL}{path}"

    last_error = None

    for attempt in range(1, retries + 1):

        try:

            response = requests.get(
                url,
                params=params,
                timeout=30
            )

            if response.status_code == 429:

                wait = 10 * attempt

                print(f"Rate limit alcanzado. Esperando {wait}s")

                time.sleep(wait)

                continue

            response.raise_for_status()

            return response.json()

        except requests.RequestException as exc:

            last_error = exc

            wait = 3 * attempt

            print(
                f"Intento {attempt}/{retries} falló: {exc}"
            )

            time.sleep(wait)

    raise RuntimeError(
        f"No se pudo consultar {url}: {last_error}"
    )


def extract_apod(start_date, end_date):

    print("Extrayendo datos APOD...")

    data = request_json(
        "/planetary/apod",
        {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "thumbs": "true"
        }
    )

    if isinstance(data, dict):
        data = [data]

    return data
def save_raw_json(data, filename):

    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    RAW_DIR = os.path.join(
        BASE_DIR,
        "data",
        "raw"
    )

    os.makedirs(RAW_DIR, exist_ok=True)

    filepath = os.path.join(
        RAW_DIR,
        filename
    )

    with open(filepath, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"JSON guardado en {filepath}")

    
if __name__ == "__main__":

    end_date = date.today()

    start_date = end_date - timedelta(days=5)

    raw_data = extract_apod(
        start_date,
        end_date
    )

    save_raw_json(
        raw_data,
        "apod_raw.json"
    )