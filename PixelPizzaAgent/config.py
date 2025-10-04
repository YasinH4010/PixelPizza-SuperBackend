import json

with open('config.json', 'r', encoding='utf-8') as configj:
    CONFIG = json.load(configj)

WAITINGS = {}
SESSIONS = {}