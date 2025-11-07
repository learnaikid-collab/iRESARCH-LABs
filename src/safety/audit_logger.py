"""
Audit Logger for decision tracking and compliance.

Logs all system decisions for transparency and accountability.
"""

import logging
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class AuditLogger:
    """
    Logs system decisions and actions for audit purposes.
    
    Features:
    - Decision logging
    - Event tracking
    - Performance metrics
    - Privacy-preserving logging
    - Structured output
    """
    
    def __init__(
        self,
        log_dir: str = "logs/audit",
        anonymize: bool = True,
        retention_days: int = 90,
    ):
        """
        Initialize Audit Logger.
        
        Args:
            log_dir: Directory for audit logs
            anonymize: Whether to anonymize user data
            retention_days: How long to keep logs
        """
        self.log_dir = Path(log_dir)
        self.anonymize = anonymize
        self.retention_days = retention_days
        
        # Create log directory
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(
            f"Audit Logger initialized (dir={log_dir}, "
            f"anonymize={anonymize})"
        )
    
    def log_event(
        self,
        event_type: str,
        data: Dict[str, Any],
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ):
        """
        Log an audit event.
        
        Args:
            event_type: Type of event (e.g., 'optimization_request', 'safety_violation')
            data: Event data
            user_id: Optional user identifier
            session_id: Optional session identifier
        """
        timestamp = datetime.utcnow()
        
        # Anonymize if enabled
        if self.anonymize and user_id:
            user_id = self._hash_id(user_id)
        
        event = {
            "timestamp": timestamp.isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "session_id": session_id,
            "data": data,
        }
        
        # Write to daily log file
        log_file = self.log_dir / f"audit_{timestamp.strftime('%Y%m%d')}.jsonl"
        
        try:
            with open(log_file, 'a') as f:
                f.write(json.dumps(event) + '\n')
            
            logger.debug(f"Logged audit event: {event_type}")
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")
    
    def log_optimization(
        self,
        request: str,
        strategy: str,
        result: Dict[str, Any],
        user_id: Optional[str] = None,
    ):
        """Log an optimization request."""
        self.log_event(
            "optimization_request",
            {
                "request_summary": request[:100] if self.anonymize else request,
                "strategy": strategy,
                "iterations": result.get("iterations", 0),
                "final_score": result.get("final_score", 0.0),
                "improvement": result.get("improvement", 0.0),
            },
            user_id=user_id,
        )
    
    def log_safety_violation(
        self,
        content: str,
        violations: list,
        action_taken: str,
        user_id: Optional[str] = None,
    ):
        """Log a safety violation."""
        self.log_event(
            "safety_violation",
            {
                "content_summary": content[:100] if self.anonymize else content,
                "violations": violations,
                "action_taken": action_taken,
            },
            user_id=user_id,
        )
    
    def log_policy_enforcement(
        self,
        policy: str,
        content: str,
        enforced: bool,
        user_id: Optional[str] = None,
    ):
        """Log policy enforcement action."""
        self.log_event(
            "policy_enforcement",
            {
                "policy": policy,
                "content_summary": content[:100] if self.anonymize else content,
                "enforced": enforced,
            },
            user_id=user_id,
        )
    
    def log_performance(
        self,
        operation: str,
        metrics: Dict[str, Any],
    ):
        """Log performance metrics."""
        self.log_event(
            "performance_metrics",
            {
                "operation": operation,
                "metrics": metrics,
            },
        )
    
    def _hash_id(self, identifier: str) -> str:
        """Hash an identifier for anonymization."""
        import hashlib
        return hashlib.sha256(identifier.encode()).hexdigest()[:16]
    
    def get_stats(self, days: int = 7) -> Dict[str, Any]:
        """
        Get audit statistics for recent days.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with statistics
        """
        # Placeholder implementation
        return {
            "total_events": 0,
            "events_by_type": {},
            "period_days": days,
        }
