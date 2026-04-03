import os
import sys
import mailer
import logging
import traceback
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import FastAPI,BackgroundTasks
from fastapi import HTTPException
from pydantic import BaseModel,EmailStr
from dotenv import load_dotenv
from supabase import create_client, Client
from fastapi.middleware.cors import CORSMiddleware
from postgrest.exceptions import APIError
from fastapi.responses import JSONResponse

limiter = Limiter(key_func = get_remote_address)

logging.basicConfig(
    stream=sys.stderr,
    level = logging.ERROR,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv(dotenv_path=".env")

app=FastAPI()

app.state.limiter = limiter

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGINS")

print(f"connecting... to {SUPABASE_URL}")
print(f"accessing supabase with anon key: {SUPABASE_ANON_KEY[20:30]}*****END...")
print("successfully connected to SUPABASE!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY) #supabase client instance

#safety check for .env variables anon key and url.
if SUPABASE_URL== None or SUPABASE_ANON_KEY== None:
    raise ValueError("Supabase KEY and URL returned None. Check .env file for correction.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

class waitlist(BaseModel):
    '''Schema for Validating client input'''
    name:str
    email:EmailStr
    
# route
@app.post("/waitlist")
@limiter.limit("5/minute")
def reg(request: Request, user_details: waitlist, background_tasks: BackgroundTasks):
    try:
        strip_email = user_details.email.strip().lower() 
        strip_name = user_details.name.strip().title()

        response1=supabase.table("Api_waitlist_table").select("name").eq("name", strip_name).execute()

        if len(response1.data) > 0:
            return {"Feedback": "Name already taken. Try another one."}

        response2=supabase.table("Api_waitlist_table").select("email").eq("email", strip_email).execute()

        if len(response2.data) > 0:
            return {"Feedback":  "Email is already taken. Try another email"}

        data_json = user_details.model_dump()
        db_response = supabase.table("Api_waitlist_table").insert(data_json).execute()

        print(f"{user_details.name}, just joined the waitlist.")

        background_tasks.add_task(
            mailer.send_welcome_message,
            user_details.email,
            user_details.name
        )

        print(db_response.data)
        return {"Feedbck": "You successfully joined the waitlist!"}
        
    except HTTPException as http_err:
        logging.error(f"CLIENT ERROR: {http_err}")
        raise http_err

    except APIError as db_err:
        logging.error(f"DATABASE ERROR: {db_err}")
        raise HTTPException (
            status_code = 500,
            detail= "Database error, Try again later."
        )   

    except Exception as e:
        logging.error(f"UNEXPECTED SYSTEM ERROR: {e}")
        traceback.print_exc()
        raise HTTPException (
            status_code = 500,
            detail = "Something went wrong on our end. And not yours."
        )

@app.exception_handler(Exception)
async def all_exceptions(request: Request, exc: Exception):
    logging.error(f"Unhandled error on {request.url}:{exc}", exc_info=True)
    return JsonResponse(status_code=500, content={"detail": "Something went wrong on our end. This isn't your fault."})

@app.get("/health")
def health_check():
    return{"status" : "ok"}