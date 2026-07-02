from app.agent.tools import *

print(query_order("SF123456"))

print(query_track("SF123456"))

print(query_price(
    "深圳",
    "北京",
    2
))

print(transfer_to_human())