from typing import TypedDict


class DeviceAuthorizationResponse(TypedDict):
    device_code: str
    user_code: str
    # creation_time: float
    # is_authenticated: bool
    verification_uri: str  # エンドユーザー検証
    verification_uri_complete: str  # User Code を含むエンドユーザー検証 URI
    user_id: int
    expires_in: int  # device_code, user_code の有効期間
    interval: int
