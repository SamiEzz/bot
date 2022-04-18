import requests
import json
import pandas as pd
from datetime import datetime
import yaml


def get_bot_key():
    with open("./keys.yml") as yml_keys_file:
      return yaml.safe_load(yml_keys_file)["telegram_bot"]
  
def get_yml_config():
    with open("./config.yml") as yml_config_file:
      return yaml.safe_load(yml_config_file)

def is_admin(id,config):
  for user_id in config['admin_ids']:
    if user_id == id:
      return True
  return False

def is_command( msg_str,config):
  for com in config["commands"]:
    if msg_str.find(com["text"])>-1:
      return True
  return False

config = get_yml_config() 


get_updates_url = f"https://api.telegram.org/bot{get_bot_key()}/getUpdates"
raw_json = requests.get(get_updates_url)
json_inst = json.loads(raw_json.content)

# get admin user messages
messages_results =[]
for update in json_inst["result"]:
  if "message" in update.keys():
    msg = {}
    msg["id"]=update["message"]["message_id"]
    msg["sender_id"]=update["message"]["from"]["id"]
    msg["sender_username"]=update["message"]["from"]["username"]
    msg["timestamp"]=update["message"]["date"]
    ts=int(msg["timestamp"])
    msg["time_str"]=datetime.fromtimestamp(ts)
    msg["text"]=update["message"]["text"]
    msg["is_command"]=is_command(msg["text"],config)
    msg["is_admin"]=is_admin(int(msg["sender_id"]),config)
    messages_results.append(msg)

results_df = pd.DataFrame(messages_results)
results_df = results_df.sort_values(by="timestamp")

print(results_df.tail())