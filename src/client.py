import json
import sys
import time
from contextlib import contextmanager

import httpx

from .cli import UIThread
from .stractures import DeviceAuthorizationResponse


class Client:
    def __init__(self, endpoint: str):
        if not endpoint.endswith("/"):
            endpoint += "/"

        self.endpoint = endpoint

    def set_token(self, token):
        self.token = token

    def generate_device_user_codes(self, client_id: str, scope: dict = None):
        # /device/authorization
        # client_id=1406020730&scope=example_scope
        res = httpx.post(self.endpoint + f"generate_device_user_codes?client_id={client_id}")
        res.raise_for_status()
        data: DeviceAuthorizationResponse = res.json()
        return data

    def verification(self):
        # /device/verification
        ...

    def poll_for_access_token(self, client_id: str, device_code: str):
        grant_type = "urn:ietf:params:oauth:grant-type:device_code"  # 固定値
        res = httpx.get(
            self.endpoint
            + f"poll_for_access_token?grant_type={grant_type}&device_code={device_code}&client_id={client_id}"
        )
        res.raise_for_status()
        return res.json()

    def refresh_access_token(self, refresh_token: str):
        res = httpx.get(self.endpoint + f"refresh?refresh_token={refresh_token}")
        res.raise_for_status()
        return res.json()

    def heartbeat(self):
        ...


class DeviceflowAgent:
    def __init__(self, client: Client):
        self.client = client

    @classmethod
    @contextmanager
    def join_to(cls, endpoint: str, out=sys.stdout, thread=None):
        agent = cls(Client(endpoint))
        client = agent.client

        client_id = input("Please input client_id: ")

        data = client.generate_device_user_codes(client_id)
        # {'device_code': '89357757-2651-47df-b331-58e4272a16db', 'user_code': 'a8855c03', 'creation_time': 1703142051.687141, 'is_authenticated': True, 'user_id': 1}

        user_code = data["user_code"]
        device_code = data["device_code"]

        # verify_user_code?user_code
        verify_endpoint = endpoint + "docs#/default/verify_user_code_verify_user_code_post"

        out.write(
            "Succeeded to publish Device code\n"
            + json.dumps(data, indent=2)
            + "\n"
            + f"Please input USER CODE to: {verify_endpoint}\n"
        )

        with UIThread(out).wait() as canceller:
            canceller.update_progress("waiting for authentication...")
            canceller.handle_keyboard_interrupt()

            token = None

            while canceller.running:
                try:
                    token = client.poll_for_access_token(client_id, device_code)
                except Exception as e:
                    canceller.update_progress(str(e))

                if token:
                    client.set_token(token)
                    canceller.cancel(json.dumps(token, indent=2))
                else:
                    time.sleep(1)

        out.write(canceller.get_cancel_message() + "\n")
        yield agent


def run():
    """
    3. クライアントアプリケーションの構築
    ステップ 1: ユーザー認証リクエストの送信

    サーバーにデバイスコードを要求。
    ユーザーに認証用のコードを表示。
    ステップ 2: 認証ステータスのポーリング

    定期的にサーバーに認証ステータスを問い合わせ。
    認証が完了するまで待機。
    ステップ 3: アクセストークンの取得

    認証完了後、サーバーからアクセストークンを受け取る。
    """
    with DeviceflowAgent.join_to("http://localhost:8000/") as agent:
        print(agent)
