from copy import copy, deepcopy
from uuid import uuid4

from fastapi import FastAPI, Form, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AppProblem(HTTPException):
    ...


class Store:
    def __init__(self):
        self.store = {}

    def add(self, key, value):
        if key in self.store:
            raise Exception(f"{key} already exists")
        self.put(key, value)

    def put(self, key, value):
        self.store[key] = copy(value)

    def get(self, key):
        return deepcopy(self.store.get(key))

    def exists(self, key):
        return key in self.store

    def get_or(self, key, default):
        if self.exists(key):
            return self.get(key)
        else:
            return default


app_store = Store()
device_code_store = Store()
user_code_store = Store()


@app.post("/register_application")
async def register_application(name: str = Form(...), redirect_uri: str = Form(...)):
    client_id = uuid4().__str__()
    client_secret = uuid4().__str__()
    data = dict(
        name=name,  # unique
        client_id=client_id,  # unique
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )
    app_store.add(client_id, data)
    return data


@app.post("/generate_device_user_codes")
async def generate_device_user_codes(client_id: str):
    """デバイスコードとユーザーコードをリクエストします。"""
    from datetime import datetime

    from .stractures import DeviceAuthorizationResponse

    if not app_store.exists(client_id):
        raise Exception()

    device_code = str(uuid4())
    user_code = str(uuid4())[:8]  # 短いコード
    data = DeviceAuthorizationResponse(
        client_id=client_id,
        device_code=device_code,
        user_code=user_code,
        # creation_time=datetime.utcnow().timestamp(),
        # is_authenticated=True,
        # user_id=1,
    )
    user_code_store.add(user_code, data)
    del data["client_id"]
    return data


@app.post("/verify_user_code")
async def verify_user_code(user_code: str):
    """ユーザーコードを使用した認証を行います。
    * **user_code**: user code
    """

    data = user_code_store.get_or(user_code, None)
    if data:
        data["is_authenticated"] = True
        device_code = data[
            "device_code"
        ]  # 同じレコードで管理する場合は、フラグで。ストアが違う場合は単に登録すればよい。
        client_id = data["client_id"]
        device_code_store.add(device_code, data)

        return {"message": "User authenticated"}
    else:
        raise HTTPException(status_code=400, detail="Invalid user code")


@app.get("/poll_for_access_token")
async def poll_for_access_token(device_code: str):
    """アクセストークンを取得します。定期的に問い合わせるために使用します。"""
    data = device_code_store.get_or(device_code, None)
    if data:
        expires_in = 3600
        access_token_payload = create_payload(expires_in=expires_in)
        access_token = encode_jwt(access_token_payload)

        refresh_token_payload = create_payload(expires_in=3600 * 24 * 30)
        refresh_token = encode_jwt(refresh_token_payload)

        return {
            "access_token": access_token,
            "token_type": "Bearer",
            "access_token_expires_in": expires_in,
            "refresh_token": refresh_token,
        }
    else:
        raise HTTPException(status_code=400, detail="Invalid device code")


@app.get("/refresh")
async def refresh_access_token(refresh_token: str):
    payload: dict = decode_jwt(refresh_token)
    user_id = payload.get("sub", None)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    expires_in = 3600
    access_token_payload = create_payload(expires_in=expires_in)
    access_token = encode_jwt(access_token_payload)

    return {"access_token": access_token, "token_type": "Bearer"}


@app.post("/update_location")
async def update_location(lat: float, lng: float, authorization: str = Header("")):
    schema, _, encoded_token = authorization.partition(" ")
    if schema != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid token")

    print(encoded_token)

    return {
        "lat": lat,
        "lng": lng,
    }


SECRET = "YOUR_SECRET_KEY"


def create_payload(expires_in=60):
    import datetime

    payload = {
        "sub": 123,  # ユーザーの一意のID
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in),  # トークンの有効期限を1分後に設定
    }
    return payload


def encode_jwt(payload):
    import jwt

    encoded_jwt = jwt.encode(payload, SECRET, algorithm="HS256")
    return encoded_jwt


def decode_jwt(encoded_jwt):
    import jwt

    decoded_jwt = jwt.decode(encoded_jwt, SECRET, algorithms=["HS256"])
    return decoded_jwt
