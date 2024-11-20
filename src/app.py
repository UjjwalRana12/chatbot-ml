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
    # Parse incoming JSON request body
    req_data = await request.json()
    
    # Extract parameters (with fallback values if not found)
    parameters = req_data.get("queryResult", {}).get("parameters", {})
    origin = parameters.get("origin", "India")  # Default to 'Unknown' if not found
    destination = parameters.get("destination", "USA")  # Default to 'Unknown' if not found
    
    # Get the shipping rate based on origin and destination
    shipping_rate = get_shipping_rate(origin, destination)
    
    # Create the response with fulfillment text
    response = {
        "fulfillmentText": f"The shipping rate from {origin} to {destination} is {shipping_rate}."
    }
    
    return response
