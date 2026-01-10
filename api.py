from fastapi import APIRouter, HTTPException
from schemas import PostKosilo, Termin
from config import EV_URL, BOOL_URL
import httpx
import asyncio
from datetime import time, timedelta, date, datetime

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


async def get_timetable(users: list[int]):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BOOL_URL}/get", json={"user_ids": users})
        response.raise_for_status()
        return response.json()


def addTime(a, b):
    return (datetime.combine(date.today(), a) + b).time()


async def find_available_slot(timetable, duration: int, day: int):
    lunch_duration = timedelta(minutes=duration)

    existing_slots = (
        (time_entry["zacetek"], time_entry["dolzina"])
        for time_entry in timetable
        if time_entry["dan"] == day
    )

    existing_slots.sort(key=lambda x: x[0])

    current_time = time(9, 0)
    for start_time, length in existing_slots:
        end_time = (
            combine(date.today(), start_time) + timedelta(minutes=length)
        ).time()

        if addTime(current_time, lunch_duration) <= start_time and current_time <= time(
            23, 30
        ):
            return current_time

        current_time = max(current_time, end_time)

    if current_time + lunch_duration <= time(23, 30):
        return current_time

    return None


@router.post("/create")
async def create(with_arg: PostKosilo):
    timetable = await get_timetable(with_arg.udelezenci)

    start_time = await find_available_slot(
        timetable,
        duration=30,
        day=with_arg.dan,
    )

    if start_time:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{EV_URL}/urniki/{with_arg.uporabnik_id}/novTermin",
                json={
                    "termin_id": None,
                    "zacetek": start_time,
                    "dolzina": 30,
                    "dan": with_arg.dan,
                    "lokacija": "kosilo",
                    "tip": "kosilo",
                    "predmet": None,
                    "aktivnost": {
                        "aktivnost_id": None,
                        "oznaka": "Kosilo",
                        "ime": "Kosilo",
                    },
                },
            )
            response.raise_for_status()
