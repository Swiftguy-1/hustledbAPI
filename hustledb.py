from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv(dotenv_path=".env")

app=FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

print(f"connecting... to {SUPABASE_URL}")
print(f"Accessing supabase with anon key: {SUPABASE_ANON_KEY[20:30]}*****end...")
print("Successfully connected to SUPABASE!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY) #supabase client instance

#safety check for .env variables anon key and url.
if SUPABASE_URL== None or SUPABASE_ANON_KEY== None:
    raise ValueError("Supabase KEY and URL returned None. Check .env file for correction.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)
class waitlist(BaseModel):
    name:str
    email:str
    # username:str
    # password:str
    
    
  
# waitlist endpoint or route
@app.post("/waitlist")

def reg(user_details: waitlist):
  data_dict = user_details.model_dump()
  response=supabase.table("Api_waitlist_table").insert(data_dict).execute()
  
  # if os.path.exists("user_data.json") and os.path.getsize("user_data.json") > 0: 
  #   # Read previous data from existing Json file 
  #   with open("user_data.json", "r") as file:
  #     prev_data=json.load(file)
  # else:
  #   # creates an empty list for nonexistent or empty Json file 
  #   prev_data=[]
  
  # # Append client data to the list  
  # prev_data.append(data_dict)
  
  # # Wirte the appended data to the Json file 
  # with open("user_data.json", "w") as file:
  #   json.dump(prev_data, file, indent=4)
  # Terminal feedback
  print(f'{user_details.email} has joined the waitlist!') 
  print(response)
#   # Browser feedback
  return {"feedback": 'You have been added to the waitlist!'}
