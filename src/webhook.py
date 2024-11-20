from fastapi import FastAPI, Request
import requests

app = FastAPI()


def get_shipping_rate(source, destination):
    
    shipping_rates = {
        ("India", "USA"): "$50",
        ("India", "Canada"): "$55",
        ("India", "Germany"): "$60",
       
    }
    return shipping_rates.get((source, destination), "Shipping rates not available for this route.")

@app.post("/webhook")
async def webhook(request: Request):
    req_data = await request.json()
    
   
    parameters = req_data.get("queryResult", {}).get("parameters", {})
    origin = parameters.get("origin", [{}])[0].get("country", "Unknown")
    destination = parameters.get("destination", [{}])[0].get("country", "Unknown")
    
    
    shipping_rate = get_shipping_rate(origin, destination)
    
    
    response = {
        "fulfillmentText": f"The shipping rate from {origin} to {destination} is {shipping_rate}."
    }
    
    return response

