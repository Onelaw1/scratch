import hashlib
import json
from datetime import datetime, date
from typing import Dict, Any, List
import random
from ..models import User

class BlockchainService:
    """
    Mock Blockchain Service for issuing Verifiable Experience Certificates.
    """

    def _generate_hash(self, data: Dict[str, Any]) -> str:
        """
        Generates a SHA-256 hash of the certificate data.
        """
        data_string = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(data_string.encode()).hexdigest()

    def issue_certificate(self, user: User) -> Dict[str, Any]:
        """
        Issues a new blockchain-backed certificate for a user.
        """
        # 1. Gather Career Data (Immutable Snapshot)
        issue_date = datetime.utcnow().isoformat()
        
        certificate_data = {
            "issuer": "Global Job Management System (JMS)",
            "issuer_id": "did:jms:kr:public_sector_node_01",
            "recipient_id": user.id,
            "recipient_name": user.name,
            "position": user.position.title if user.position else "Employee",
            "department": user.department.name if user.department else "General",
            "hire_date": user.hire_date.isoformat() if user.hire_date else "2020-01-01",
            "issue_date": issue_date,
            "type": "EXPERIENCE_AND_ACHIEVEMENTS",
            "status": "VALID",
            "nonce": random.randint(100000, 999999) # Random salt
        }

        # 2. Sign (Hash) the Data
        block_hash = self._generate_hash(certificate_data)
        
        # 3. Simulate Blockchain Transaction
        transaction_id = f"0x{block_hash[:16]}...{block_hash[-16:]}"
        block_height = 145023 + random.randint(1, 100)
        
        return {
            "certificate_id": f"CERT-{datetime.now().year}-{random.randint(1000, 9999)}",
            "data": certificate_data,
            "blockchain_proof": {
                "network": "Hyperledger Besu (Private Consortium)",
                "common_name": "ROK-Public-Sector-Chain",
                "block_height": block_height,
                "transaction_hash": transaction_id,
                "signature": block_hash
            },
            "verification_url": f"https://verify.jms.gov.kr/cert/{block_hash[:8]}"
        }
