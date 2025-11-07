"""
Policy Engine for creative compliance.

Enforces safety policies while enabling creative solutions.
"""

import logging
from typing import Dict, Any, List
import yaml
import os

logger = logging.getLogger(__name__)


class PolicyEngine:
    """
    Enforces safety policies with creative compliance.
    
    Features:
    - Policy definition and loading
    - Violation detection
    - Creative reframing of unsafe requests
    - Alternative suggestions
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize Policy Engine.
        
        Args:
            config_path: Path to safety configuration file
        """
        self.config_path = config_path or "config/safety.yaml"
        self.policies = self._load_policies()
        logger.info("Policy Engine initialized")
    
    def _load_policies(self) -> Dict[str, Any]:
        """Load safety policies from config."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Could not load policies: {e}")
        
        # Default policies
        return {
            "policy": {
                "blocked_topics": [
                    "harmful_content",
                    "privacy_violation",
                    "illegal_activities",
                ],
                "enforcement_level": "strict",
            }
        }
    
    def check_policy(self, content: str, task_type: str = None) -> Dict[str, Any]:
        """
        Check if content complies with policies.
        
        Args:
            content: Content to check
            task_type: Type of task being performed
            
        Returns:
            Dictionary with policy check results
        """
        logger.debug("Checking policy compliance")
        
        violations = []
        blocked_topics = self.policies.get("policy", {}).get("blocked_topics", [])
        
        content_lower = content.lower()
        for topic in blocked_topics:
            topic_key = topic.replace("_", " ")
            if topic_key in content_lower:
                violations.append(topic)
        
        compliant = len(violations) == 0
        
        result = {
            "compliant": compliant,
            "violations": violations,
            "enforcement_level": self.policies.get("policy", {}).get("enforcement_level", "strict"),
            "allow_with_warning": False,
        }
        
        if not compliant:
            result["message"] = f"Policy violations detected: {', '.join(violations)}"
            result["alternative"] = self._suggest_alternative(content, violations)
        
        return result
    
    def _suggest_alternative(self, content: str, violations: List[str]) -> str:
        """Suggest creative alternative that complies with policies."""
        return (
            f"This request may involve {', '.join(violations)}. "
            "Consider reframing your request in a way that focuses on "
            "educational, informational, or constructive purposes."
        )
    
    def enforce(self, content: str) -> Dict[str, Any]:
        """
        Enforce policies on content.
        
        Returns content if compliant, or modified/blocked based on policies.
        """
        policy_check = self.check_policy(content)
        
        if policy_check["compliant"]:
            return {
                "allowed": True,
                "content": content,
                "modified": False,
            }
        
        enforcement = self.policies.get("policy", {}).get("enforcement_level", "strict")
        
        if enforcement == "strict":
            return {
                "allowed": False,
                "content": None,
                "modified": False,
                "reason": policy_check.get("message", "Policy violation"),
                "alternative": policy_check.get("alternative"),
            }
        else:
            # Moderate enforcement: allow with warning
            return {
                "allowed": True,
                "content": content,
                "modified": False,
                "warning": policy_check.get("message"),
            }
