#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) ACE 

import os
import logging
from dotenv import load_dotenv

load_dotenv()


MOGO_URI = os.environ.get("MOGO_URI", "mongodb+srv://GurjarBot:GurjarBot@cluster0.2r00whc.mongodb.net/?retryWrites=true&w=majority")       
API_KEY = os.environ.get("API_KEY", "")
# AUTH_USERS = os.environ.get("AUTH_USERS", "")   

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
