import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict

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

# OUTPUT_FILE = "data.json"
async def get_data(tracking_id: int) -> Any:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            async with page.expect_response(
                lambda r: "tracking-public/shipments/land/" in r.url and r.status == 200,
                timeout=30_000
            ) as resp_info:
                await page.goto(
                    f"https://www.dbschenker.com/app/tracking-public/?refNumber={tracking_id}",
                    wait_until="domcontentloaded"
                )

            response = await resp_info.value
            data = await response.json()

            await browser.close()
            
            # Check if the response indicates an invalid tracking number
            if data.get("error") or not data.get("events"):
                return {"error": "Invalid tracking number or no data found"}
            
            return data
    except TimeoutError:
        return {"error": "Request timed out - tracking number may be invalid"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def get_sender(data: Any) -> Sender:
    if isinstance(data, dict) and "error" in data:
        return Sender()  # Return empty sender for error case
    
    name = None
    names = data.get("references", {}).get("shipper")
    if names and len(names) == 1:
        name = names[0]
    
    collect = data.get("location", {}).get("collectFrom", {})
    country = collect.get("country")
    city = collect.get("city")
    postcode = collect.get("postCode")

    return Sender(
        name=name, 
        country=country,
        city=city,
        postcode=postcode,
    )

def get_receiver(data: Any) -> Receiver:
    if isinstance(data, dict) and "error" in data:
        return Receiver()  # Return empty receiver for error case
    
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

def get_packages(data: Any) -> Packages:
    if isinstance(data, dict) and "error" in data:
        return Packages()  # Return empty packages for error case
    
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

def get_events(data: Any) -> list[Event]:
    if isinstance(data, dict) and "error" in data:
        return []  # Return empty list for error case
    
    raw_events = data.get("events", [])
    events = []
    for raw_event in raw_events:
        date_str = raw_event.get("date")
        dt = None
        if date_str:
            try:
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except ValueError:
                pass  # Keep as None if parsing fails
        city = raw_event.get("location", {}).get("name")
        country_code = raw_event.get("location", {}).get("countryCode")
        comment = raw_event.get("comment")
        raw_reasons = raw_event.get("reasons", [])
        reasons = [reason.get("description") for reason in raw_reasons if reason.get("description")]
        event = Event(
            dt=dt,
            city=city,
            country_code=country_code,
            comment=comment,
            reasons=reasons,
        )
        events.append(event)
    return events

# asyncio.run(get_data(1806258974))