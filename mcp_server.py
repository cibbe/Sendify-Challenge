from fastmcp import FastMCP
import dbs_reader

mcp = FastMCP("DB Schenker Shipment tracker")

@mcp.tool
async def get_sender(tracking_number: int) -> dict:
    '''Get the name, country, city and postal code of the Sender'''
    try:
        data = await dbs_reader.get_data(tracking_number)
    except Exception as exc:
        raise RuntimeError(f"failed to fetch tracking data: {exc}")
    sender = dbs_reader.get_sender(data)
    return sender.model_dump(mode="json")

@mcp.tool
async def get_receiver(tracking_number: int) -> dict:
    '''Get the name, country, city and postal code of the Reciever'''
    try:
        data = await dbs_reader.get_data(tracking_number)
    except Exception as exc:
        raise RuntimeError(f"failed to fetch tracking data: {exc}")
    receiver = dbs_reader.get_reciever(data)
    return receiver.model_dump(mode="json")

@mcp.tool
async def get_packages(tracking_number: int) -> dict:
    '''Get information about the packages'''
    try:
        data = await dbs_reader.get_data(tracking_number)
    except Exception as exc:
        raise RuntimeError(f"failed to fetch tracking data: {exc}")
    packages = dbs_reader.get_packages(data)
    return packages.model_dump(mode="json")

@mcp.tool
async def get_events(tracking_number: int) -> list:
    '''Get a list of tracking events'''
    try:
        data = await dbs_reader.get_data(tracking_number)
    except Exception as exc:
        raise RuntimeError(f"failed to fetch tracking data: {exc}")
    events = dbs_reader.get_events(data)
    return [e.model_dump(mode="json") for e in events]

@mcp.tool
async def get_info(tracking_number: int) -> dict:
    '''Get all shipment info'''
    try:
        data = await dbs_reader.get_data(tracking_number)
    except Exception as exc:
        raise RuntimeError(f"failed to fetch tracking data: {exc}")
    info = {}
    sender = dbs_reader.get_sender(data)
    receiver = dbs_reader.get_reciever(data)
    packages = dbs_reader.get_packages(data)
    events = dbs_reader.get_events(data)
    info["sender"] = sender.model_dump(mode="json")
    info["reciever"] = receiver.model_dump(mode="json")
    info["packages"] = packages.model_dump(mode="json")
    info["events"] = [e.model_dump(mode="json") for e in events]
    return info

if __name__ == "__main__":
    mcp.run_async()