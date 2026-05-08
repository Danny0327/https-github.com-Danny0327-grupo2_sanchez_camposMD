import json
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RAW_FILE = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "apod_raw.json"
)

TRANSFORMED_DIR = os.path.join(
    BASE_DIR,
    "data",
    "transformed"
)

TRANSFORMED_FILE = os.path.join(
    TRANSFORMED_DIR,
    "apod_clean.json"
)


def load_raw_data():

    with open(RAW_FILE, "r", encoding="utf-8") as file:

        data = json.load(file)

    return data


def transform_apod(data):

    transformed = []

    for item in data:

        transformed_item = {

            "date": item.get("date"),

            "title": item.get("title"),

            "media_type": item.get("media_type"),

            "url": item.get("url")
            or item.get("thumbnail_url"),

            "explanation": item.get("explanation"),

            "copyright": item.get("copyright", "Unknown")

        }

        transformed.append(transformed_item)

    return transformed


def save_transformed_data(data):

    os.makedirs(
        TRANSFORMED_DIR,
        exist_ok=True
    )

    with open(
        TRANSFORMED_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"JSON transformado guardado en:"
        f"\n{TRANSFORMED_FILE}"
    )


if __name__ == "__main__":

    print("Leyendo JSON raw...")

    raw_data = load_raw_data()

    print("Transformando datos...")

    transformed_data = transform_apod(
        raw_data
    )

    print("Guardando JSON transformado...")

    save_transformed_data(
        transformed_data
    )

    print("Transformación completada")