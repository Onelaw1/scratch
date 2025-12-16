import os
import yaml
from typing import List
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from .database import get_db

# Load permission matrix
PERMISSIONS_PATH = os.path.join(os.path.dirname(__file__), "permissions.yaml")
if not os.path.exists(PERMISSIONS_PATH):
    # Fallback or create empty if missing during init
    PERM_MATRIX = {}
else:
    with open(PERMISSIONS_PATH, "r", encoding="utf-8") as f:
        PERM_MATRIX = yaml.safe_load(f)

# Secret key for JWT decoding (placeholder, should be set securely)
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = "HS256"

def get_current_user(request: Request):
    """Extract and verify JWT token, return user dict with id and roles list."""
    auth: str = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        # Strict RBAC: No token = 401
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authentication token")
    
    token = auth.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        roles: List[str] = payload.get("role", [])
        if not roles and payload.get("roles"): 
            roles = payload.get("roles")
        if not isinstance(roles, list):
             roles = [roles] if roles else []

        if not user_id:
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return {"id": user_id, "roles": roles}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def require_roles(*allowed_roles: str):
    """Dependency that ensures the current user has at least one of the allowed roles."""
    def checker(user = Depends(get_current_user)):
        user_roles = set(user["roles"])
        if "SUPER_ADMIN" in user_roles: return user
        
        if not user_roles.intersection(set(allowed_roles)):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return user
    return checker

def require_permission(resource: str, level: str):
    """Dependency that checks permission matrix for the requested resource/level."""
    def checker(user = Depends(get_current_user)):
        user_roles = user["roles"]
        if "SUPER_ADMIN" in user_roles: return user
        
        for role in user_roles:
            perms = PERM_MATRIX.get(role, {})
            if perms.get("all"): return user
            
            user_level = perms.get(resource)
            if not user_level: continue

            if user_level == "all": return user
            if user_level == level: return user
            
            # Simple hierarchy
            if level == "read" and user_level in ["read", "read_own", "write_own", "write_review", "write_all"]: return user
            
            if level.startswith("write"):
                if user_level == "write_all": return user
                if level == "write_own" and user_level in ["write_all", "write_review", "write_own"]: return user
                
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Insufficient permission for {resource}:{level}")
    return checker
