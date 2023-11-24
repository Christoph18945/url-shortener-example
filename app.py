#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""url shortener"""

import webbrowser
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import hashlib
import validators

app = FastAPI()

# here: storage in memory
# database would be used in production
url_mapping = {}

class URLItem(BaseModel):
    """URLitem class"""
    original_url: str

@app.post("/shorten")
async def shorten_original_url(url_item: URLItem) -> dict[str, str]:
    """shorten the oriinal url"""
    short_url = generate_short_url(url_item.original_url) # generate short url based on original
    url_mapping[short_url] = url_item.original_url # store mapping between short url and original
    print(f"Shortened URL: {short_url} -> Original URL: {url_item.original_url}") # print message
    return {"short_url": short_url} # return the json response with short url

@app.get("/expand/{short_url}")
async def get_orig_url(short_url: str):
    """get original url from shortened one"""
    original_url = url_mapping.get(short_url) # retriev eoriginal url
    # If original url is not found, raise HTTPException with 404 code
    if original_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    print(f"Expanded URL: {short_url} -> Original URL: {original_url}") # print message indicating the expanded ur
    return {"original_url": original_url} # return json response containing original URL

@app.get("/{short_url}")
async def redirect_url(short_url: str):
    """open the shortened url in webbrowser"""
    original_url = url_mapping.get(short_url)
    if original_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    webbrowser.open(original_url) # Open the original URL in the default web browser
    return RedirectResponse(url=original_url) # Optionally, you can redirect to the original URL as well

def generate_short_url(original_url):
    """generate shortened url"""
    md5_hash = hashlib.md5(original_url.encode()).hexdigest() # Calculate MD5 hash of original URL, get the hexadecimal representation
    short_url = md5_hash[:8] # first 8 characters of the MD5 hash as the short URL
    print(f"Generated Short URL: {short_url} from Original URL: {original_url}") # Print a message indicating the generated short URL and its corresponding original URL
    return short_url # Return the generated short URL
