from fastapi import FastAPI, Request
import requests

app = FastAPI()

def get_shipping_rate(source, destination):
    # Predefined shipping rates
    shipping_rates = {
        ("India", "USA"): "$50",
        ("India", "Canada"): "$55",
        ("India", "Germany"): "$60",
    }
    
    # Return the shipping rate if it exists, else return a default message
    return shipping_rates.get((source, destination), "Shipping rates not available for this route.")

@app.get("/")
async def get_request():
    return {"message": "this is the get request"}

@app.post("/webhook")
async def webhook(request: Request):
    req_data = await request.json()

    
    parameters = req_data.get("queryResult", {}).get("parameters", {})

    
    origin_data = parameters.get("origin", [{}])[0]  
    destination_data = parameters.get("destination", [{}])[0] 
    
    
    origin = origin_data.get("country", "Unknown")
    destination = destination_data.get("country", "Unknown")

    
    shipping_rate = get_shipping_rate(origin, destination)

    
    response = {
        "fulfillmentText": f"The shipping rate from {origin} to {destination} is {shipping_rate}."
    }

    return response
