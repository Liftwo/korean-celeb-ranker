from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import random
import json
import os

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Load celebrities from JSON file
def load_celebrities():
    with open("celebrities.json", "r", encoding="utf-8") as f:
        return json.load(f)

celebrities = load_celebrities()
# Keep track of eliminated celebrities
eliminated_celebs = set()

@app.get("/")
async def home(request: Request):
    # Reset eliminated celebrities when starting a new game
    eliminated_celebs.clear()
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/get-pair/{winner_id}/{loser_id}")
async def get_pair(winner_id: int = None, loser_id: int = None):
    if winner_id is not None and loser_id is not None:
        # Get the winner celebrity
        winner = next((celeb for celeb in celebrities if celeb["id"] == winner_id), None)
        if winner:
            # Add the loser to eliminated list
            eliminated_celebs.add(loser_id)
            
            # Get all celebrities except the winner and previously eliminated ones
            remaining_celebs = [celeb for celeb in celebrities 
                              if celeb["id"] != winner_id and celeb["id"] not in eliminated_celebs]
            
            if remaining_celebs:
                # Select one random celebrity from remaining ones
                opponent = random.choice(remaining_celebs)
                return JSONResponse(content={"celebs": [winner, opponent]})
            else:
                # If no remaining celebrities, return only the winner
                return JSONResponse(content={"celebs": [winner], "winner": True})
    
    # If no winner_id/loser_id or winner not found, select two random celebrities
    available_celebs = [celeb for celeb in celebrities if celeb["id"] not in eliminated_celebs]
    if len(available_celebs) >= 2:
        pair = random.sample(available_celebs, 2)
    else:
        # If less than 2 celebrities available, we have our winner
        return JSONResponse(content={"celebs": available_celebs, "winner": True})
    return JSONResponse(content={"celebs": pair})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
