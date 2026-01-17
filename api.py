from fastapi import APIRouter, HTTPException, Header
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
        response = await client.post(f"{BOOL_URL}/bool/", json={"user_ids": users})
        response.raise_for_status()
        return response.json()


def addTime(a, b):
    return (datetime.combine(date.today(), a) + b).time()


def parse_time(t):
    if isinstance(t, time):
        return t
    return datetime.strptime(t, "%H:%M:%S").time()


async def find_available_slot(timetable, duration: int, day: int):
    lunch_duration = timedelta(minutes=duration)

    existing_slots = [
        (parse_time(t["zacetek"]), int(t["dolzina"]))
        for t in timetable
        if int(t["dan"]) == int(day)
    ]

    existing_slots.sort(key=lambda x: x[0])

    current_time = time(9, 0)
    day_end = time(23, 30)

    for start_time, length in existing_slots:
        end_time = addTime(start_time, timedelta(minutes=length))

        # preveri luknjo do naslednjega termina
        if addTime(current_time, lunch_duration) <= start_time:
            return current_time

        # sicer premakni current_time za ta termin
        if end_time > current_time:
            current_time = end_time

    # po zadnjem terminu
    if addTime(current_time, lunch_duration) <= day_end:
        return current_time

    return None


@router.post("/")
async def create(
    with_arg: PostKosilo, authorization: str | None = Header(default=None)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    timetable = await get_timetable(with_arg.udelezenci)

    start_time = await find_available_slot(
        timetable,
        duration=30,
        day=with_arg.dan,
    )

    if start_time:
        start_str = start_time.strftime("%H:%M:%S")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{EV_URL}/urniki/{with_arg.uporabnik_id}/termini",
                headers={"Authorization": authorization},
                json={
                    "termin_id": None,
                    "zacetek": start_str,
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
