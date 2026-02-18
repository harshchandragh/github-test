import base64
import logging
from typing import Any, Dict, Optional, List
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class JiraAPIClient:
    """Async HTTP client for Jira Cloud REST API."""
    
    def __init__(self, instance_url: str, email: str, api_token: str):
        self.instance_url = instance_url.rstrip('/')
        self.email = email
        self.api_token = api_token
        self.client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers=self._get_headers(),
            base_url=self.instance_url
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
    
    def _get_headers(self) -> Dict[str, str]:
        """Generate authentication headers."""
        credentials = f"{self.email}:{self.api_token}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make HTTP request with automatic retry."""
        if not self.client:
            raise RuntimeError("Client not initialized")
        
        try:
            response = await self.client.request(method, endpoint, **kwargs)
            response.raise_for_status()
            return response.json() if response.content else {}
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            raise
    
    async def test_connection(self) -> bool:
        """Test if connection credentials are valid."""
        try:
            await self._make_request("GET", "/rest/api/3/myself")
            return True
        except:
            return False
    
    async def get_boards(self, start_at: int = 0, max_results: int = 50) -> Dict[str, Any]:
        """Fetch boards from Jira."""
        params = {"startAt": start_at, "maxResults": min(max_results, 50)}
        return await self._make_request("GET", "/rest/agile/1.0/board", params=params)
    
    async def get_sprints(self, board_id: int, start_at: int = 0) -> Dict[str, Any]:
        """Fetch sprints for a board."""
        params = {"startAt": start_at, "maxResults": 50}
        return await self._make_request(
            "GET",
            f"/rest/agile/1.0/board/{board_id}/sprint",
            params=params
        )
    
    async def get_sprint_issues(self, sprint_id: int, start_at: int = 0) -> Dict[str, Any]:
        """Fetch issues in a sprint."""
        params = {
            "startAt": start_at,
            "maxResults": 100,
            "fields": "key,summary,status,issuetype,assignee,priority,created,resolutiondate"
        }
        return await self._make_request(
            "GET",
            f"/rest/agile/1.0/sprint/{sprint_id}/issue",
            params=params
        )
    
    async def search_issues(self, jql: str, start_at: int = 0, max_results: int = 100) -> Dict[str, Any]:
        """Search issues using JQL."""
        params = {
            "jql": jql,
            "startAt": start_at,
            "maxResults": max_results,
            "fields": "key,summary,status,issuetype,assignee,priority,created,resolutiondate,customfield_10016,customfield_10106"
        }
        return await self._make_request("GET", "/rest/api/3/search", params=params)