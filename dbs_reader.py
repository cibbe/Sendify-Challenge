import json
from playwright.sync_api import sync_playwright
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
# from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Optional, Literal
from datetime import datetime

# Sender information (name, address)

class Sender(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    postcode: Optional[str] = None

# Receiver information (name, address)
class Receiver(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    postcode: Optional[str] = None

# Package details (weight, dimensions, piece count, etc.)
class Packages(BaseModel):
    model_config = ConfigDict(extra="ignore")
    pieces: Optional[int] = None
    weight: Optional[float] = None
    weight_unit: Optional[str] = None
    volume: Optional[float] = None
    volume_unit: Optional[str] = None
    loading_meters: Optional[float] = None
    loading_meters_unit: Optional[str] = None

# Complete tracking history for the shipment
class Event(BaseModel):
    model_config = ConfigDict(extra="ignore")
    dt: Optional[datetime] = None
    city: Optional[str] = None
    country_code: Optional[str] = None
    comment: Optional[str] = None
    reasons: Optional[list[str]] = None

# Bonus: Individual tracking events per package

# OUTPUT_FILE = "data.json"
def get_data(tracking_id):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        with page.expect_response(
            lambda r: "tracking-public/shipments/land/" in r.url and r.status == 200,
            timeout=30_000
        ) as resp_info:
            page.goto(
                f"https://www.dbschenker.com/app/tracking-public/?refNumber={tracking_id}",
                wait_until="domcontentloaded"
            )

        response = resp_info.value
        data = response.json()

        browser.close()
        return data

def get_sender(data):
    name = None
    names= data.get("references", {}).get("shipper")
    if len(names) == 1: name = names[0]
    
    collect = data.get("location", {}).get("collectFrom", {})
    country = collect.get("country")
    city = collect.get("city")
    postcode = collect.get("postCode")

    # print(collect)
    # print(name, country, city, postcode)
    return Sender(
        name=name, 
        country=country,
        city=city,
        postcode=postcode,
        )

def get_reciever(data):
    name = None
    deliver = data.get("location", {}).get("deliverTo", {})
    country = deliver.get("country")
    city = deliver.get("city")
    postcode = deliver.get("postCode")

    return Receiver(
        name=name, 
        country=country,
        city=city,
        postcode=postcode,
        )

def get_packages(data):
    pieces = data.get("goods", {}).get("pieces")
    weight = data.get("goods", {}).get("weight", {}).get("value")
    weight_unit = data.get("goods", {}).get("weight", {}).get("unit")
    volume = data.get("goods", {}).get("volume", {}).get("value")
    volume_unit = data.get("goods", {}).get("volume", {}).get("unit")
    loading_meters = data.get("goods", {}).get("loadingMeters", {}).get("value")
    loading_meters_unit = data.get("goods", {}).get("loadingMeters", {}).get("unit")

    return Packages(
        pieces=pieces,
        weight=weight,
        weight_unit=weight_unit,
        volume=volume,
        volume_unit=volume_unit,
        loading_meters=loading_meters,
        loading_meters_unit=loading_meters_unit,
    )

def get_events(data):
    raw_events = data.get("events")
    events = []
    for raw_event in raw_events:
        date = raw_event.get("date")
        city = raw_event.get("location", {}).get("name")
        country_code = raw_event.get("location", {}).get("countryCode")
        comment = raw_event.get("comment")
        raw_reasons = raw_event.get("reasons")
        reasons = []
        for raw_reason in raw_reasons:
            reasons.append(raw_reason.get("description"))
        # print(date, city, country_code, comment, reasons)
        event = Event(
            dt = date,
            city=city,
            country_code=country_code,
            comment=comment,
            reasons=reasons,
        )
        events.append(event)
    return events

# # Tests
# tracking_numers = [
#     1806203236,
#     1806290829,
#     1806273700,
#     1806272330,
#     1806271886,
#     1806270433,
#     1806268072,
#     1806267579,
#     1806264568,
#     1806258974,
#     1806256390,
# ]

# for tracking_num in tracking_numers:
#     data = get_data(tracking_num)
#     print(get_sender(data))
#     print(get_reciever(data))
#     print(get_packages(data))
#     print(*get_events(data), sep='\n')

# data = get_data(1806203236)

# # with open("data_1.json", "w", encoding="utf-8") as f:
# #     json.dump(
# #         data,
# #         f,
# #         indent=4,          # readable indentation
# #         ensure_ascii=False # keep UTF-8 characters
# #     )

# print(get_sender(data))
# print(get_reciever(data))
# print(get_packages(data))
# print(get_events(data))