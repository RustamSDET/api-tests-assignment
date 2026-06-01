from typing import Dict, Any, Optional
from playwright.sync_api import APIRequestContext

class QiwiApiClient:
    def __init__(self, request_context: APIRequestContext, base_url: str, token: str, agent_id: str, point_id: str):
        self.request_context = request_context
        self.base_url = base_url
        self.token = token
        self.agent_id = agent_id
        self.point_id = point_id
        
    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _get_url(self, path: str, **kwargs) -> str:
        params = {"agentId": self.agent_id, "pointId": self.point_id}
        params.update(kwargs)
        path_filled = path.format(**params)
        return f"{self.base_url.rstrip('/')}/{path_filled.lstrip('/')}"

    def get_all_payments(self, limit: int = 20, offset: int = 0):
        url = self._get_url("/v1/agents/{agentId}/points/{pointId}/payments")
        params = {"limit": limit, "offset": offset}
        return self.request_context.get(url, headers=self.headers, params=params)

    def get_balance(self):
        url = self._get_url("/v1/agents/{agentId}/points/{pointId}/balance")
        return self.request_context.get(url, headers=self.headers)

    def create_payment(self, payment_id: str, payload: Dict[str, Any]):
        url = self._get_url("/v1/agents/{agentId}/points/{pointId}/payments/{paymentId}", paymentId=payment_id)
        return self.request_context.put(url, headers=self.headers, data=payload)

    def execute_payment(self, payment_id: str):
        url = self._get_url("/v1/agents/{agentId}/points/{pointId}/payments/{paymentId}/execute", paymentId=payment_id)
        return self.request_context.post(url, headers=self.headers)
