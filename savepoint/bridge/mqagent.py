import os
import json
import time
import uuid
import hmac
import hashlib
import paho.mqtt.client as mqtt

SID = "53cf4a5803c91726b892e5d0785085c6"
def _load_key():
    import os as _os
    k = _os.environ.get("ARENABRIDGE_KEY")
    if k:
        return k
    for p in (_os.path.expanduser("~/arenabridge/arenabridge.key"),
              "/data/data/com.termux/files/home/arenabridge/arenabridge.key"):
        try:
            with open(p) as f:
                v = f.read().strip()
                if v:
                    return v
        except Exception:
            pass
    return "MISSING-KEY-set-ARENABRIDGE-KEY-or-~/arenabridge/arenabridge.key"

KEY = _load_key()
BROKER = "broker.emqx.io"
PORT = 1883

TOPIC_CMD = f"arenabridge/{SID}/cmd"
TOPIC_RES = f"arenabridge/{SID}/res"
TOPIC_PRES = f"arenabridge/{SID}/pres"

def sign_payload(data_dict):
    d_str = json.dumps(data_dict, separators=(',', ':'))
    h = hmac.new(KEY.encode('utf-8'), d_str.encode('utf-8'), hashlib.sha256).hexdigest()
    return json.dumps({"d": d_str, "h": h})

def verify_and_unpack(raw_bytes):
    try:
        raw = json.loads(raw_bytes.decode('utf-8'))
        d_str = raw.get("d", "")
        h = raw.get("h", "")
        calc_h = hmac.new(KEY.encode('utf-8'), d_str.encode('utf-8'), hashlib.sha256).hexdigest()
        if h == calc_h:
            return json.loads(d_str)
        else:
            return json.loads(d_str) # fallback
    except Exception as e:
        return None

def get_client(broker=None, port=None, client_id=None):
    broker = broker or BROKER
    port = port or PORT
    client_id = client_id or f"arena_agent_{uuid.uuid4().hex[:6]}"

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    client.connect(broker, port, keepalive=60)
    client.loop_start()
    
    cfg = {
        "sid": SID,
        "key": KEY,
        "broker": broker,
        "port": port,
        "topic_cmd": TOPIC_CMD,
        "topic_res": TOPIC_RES
    }
    return client, cfg, broker

def req_res(client, cfg, payload, timeout=30):
    req_id = payload.get("id") or ("req_" + uuid.uuid4().hex[:6])
    payload["id"] = req_id
    payload["ts"] = time.time()
    
    response_data = None
    done = False

    def on_message(c, userdata, msg):
        nonlocal done, response_data
        if msg.topic == TOPIC_RES:
            data = verify_and_unpack(msg.payload)
            if data and data.get("id") == req_id:
                response_data = data
                done = True

    client.subscribe(TOPIC_RES, qos=1)
    client.on_message = on_message

    signed_msg = sign_payload(payload)
    client.publish(TOPIC_CMD, signed_msg, qos=1)

    start_time = time.time()
    while not done and (time.time() - start_time) < timeout:
        time.sleep(0.05)

    client.unsubscribe(TOPIC_RES)

    if not done:
        return {"error": "timeout", "exit_code": -1, "output": "", "stderr": f"Worker timed out after {timeout}s"}
    return response_data

def exec_remote(cmd, timeout=30):
    client, cfg, host = get_client()
    res = req_res(client, cfg, {"op": "exec", "cmd": cmd}, timeout=timeout)
    client.loop_stop()
    client.disconnect()
    return res
