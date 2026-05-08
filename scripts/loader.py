import json
import os
from datetime import datetime

from database import SessionLocal
from models import APOD


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

TRANSFORMED_FILE = os.path.join(
    BASE_DIR,
    "data",
    "transformed",
    "apod_clean.json"
)


def load_transformed_data():

    with open(
        TRANSFORMED_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return data


def save_to_database(data):

    db = SessionLocal()

    inserted = 0

    try:

        for item in data:

            existing = db.get(
                APOD,
                datetime.strptime(
                    item["date"],
                    "%Y-%m-%d"
                ).date()
            )

            if existing:
                continue

            apod = APOD(

                date=datetime.strptime(
                    item["date"],
                    "%Y-%m-%d"
                ).date(),

                title=item.get("title"),

                media_type=item.get(
                    "media_type"
                ),

                url=item.get("url"),

                explanation=item.get(
                    "explanation"
                ),

                copyright=item.get(
                    "copyright"
                )
            )

            db.add(apod)

            inserted += 1

        db.commit()

        print(
            f"{inserted} registros insertados"
        )

    except Exception as e:

        db.rollback()

        print(
            f"Error insertando datos: {e}"
        )

    finally:

        db.close()


if __name__ == "__main__":

    print(
        "Leyendo datos transformados..."
    )

    transformed_data = (
        load_transformed_data()
    )

    print(
        "Insertando en PostgreSQL..."
    )

    save_to_database(
        transformed_data
    )

    print("Carga completada")