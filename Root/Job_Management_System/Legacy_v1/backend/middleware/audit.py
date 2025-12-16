import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import sys

# Configure logger
logger = logging.getLogger("audit_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - [AUDIT] - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        # Log details
        # For authenticated users, we might want to extract user info from token again, 
        # but middleware runs before dependencies often, or we can inspect headers manually if needed.
        # For now, we log the path, method, status, and duration.
        
        user_id = "anonymous"
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            # We won't fully decode here to avoid double-processing cost, 
            # but in a real system we might attach user to request state in a previous middleware.
            user_id = "authenticated_user" 

        log_message = (
            f"User: {user_id} | "
            f"Method: {request.method} | "
            f"Path: {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Duration: {process_time:.4f}s"
        )
        
        logger.info(log_message)
        
        return response
