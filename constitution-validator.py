#!/usr/bin/env python3
"""
Constitutional Validator — Toy Prototype
Checks agent actions against a personal AI constitution.

Usage:
  python3 constitution-validator.py check <constitution.yaml> <action.json>
  python3 constitution-validator.py boot <constitution.yaml>
  python3 constitution-validator.py propose <constitution.yaml> <amendment.json>
"""

import sys
import json
import yaml
from datetime import datetime
from pathlib import Path
from enum import Enum

class Weight(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Verdict(Enum):
    ALLOW = "allow"
    WARN = "warn"
    DENY = "deny"

# Map actions to articles they might violate
ACTION_ARTICLE_MAP = {
    "send_message": ["privacy-1", "scope-1", "transparency-1"],
    "read_file": ["privacy-1"],
    "write_file": ["privacy-1", "memory-1"],
    "modify_memory": ["memory-1"],
    "spawn_agent": ["delegation-1"],
    "access_financial": ["scope-1"],
    "access_social": ["scope-1"],
    "delete_data": ["autonomy-1", "memory-1"],
    "external_api": ["privacy-1", "scope-1", "transparency-1"],
    "propose_amendment": ["memory-1"],
}

def load_constitution(path):
    with open(path) as f:
        return yaml.safe_load(f)

def evaluate_action(constitution, action):
    """Check an action against all relevant constitutional articles."""
    articles = {a["id"]: a for a in constitution.get("articles", [])}
    action_type = action.get("type", "unknown")
    relevant_ids = ACTION_ARTICLE_MAP.get(action_type, [])
    
    results = []
    verdict = Verdict.ALLOW
    reasons = []
    
    for aid in relevant_ids:
        if aid not in articles:
            continue
        article = articles[aid]
        weight = Weight(article.get("weight", "medium"))
        
        # Simple rule-based evaluation
        violates = _check_violation(article, action)
        
        if violates:
            if weight == Weight.CRITICAL:
                verdict = Verdict.DENY
                reasons.append(f"CRITICAL: '{article['title']}' violated")
            elif weight == Weight.HIGH:
                if verdict != Verdict.DENY:
                    verdict = Verdict.WARN
                reasons.append(f"HIGH: '{article['title']}' may be violated")
            else:
                reasons.append(f"MEDIUM: '{article['title']}' — logged for transparency")
        
        results.append({
            "article_id": aid,
            "title": article["title"],
            "weight": weight.value,
            "violates": violates,
        })
    
    return {
        "verdict": verdict.value,
        "action": action_type,
        "reasons": reasons,
        "article_results": results,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

def _check_violation(article, action):
    """Naive violation check — in reality this would be much more sophisticated."""
    action_type = action.get("type", "")
    target = action.get("target", "")
    
    # Simple heuristics for the prototype
    if "exfiltration" in article.get("text", "").lower():
        if action_type in ("send_message", "external_api") and "external" in target:
            return True
    if "financial" in article.get("text", "").lower():
        if action_type == "access_financial" and not action.get("unlock_token"):
            return True
    if "social media" in article.get("text", "").lower():
        if action_type == "access_social" and not action.get("unlock_token"):
            return True
    if "memory" in article.get("text", "").lower() and "modify" in article.get("text", "").lower():
        if action_type == "propose_amendment":
            return True
    if "delete" in article.get("text", "").lower():
        if action_type == "delete_data":
            return not action.get("holder_request", False)
    return False

def boot_check(constitution):
    """Validate constitution at agent boot time."""
    issues = []
    articles = constitution.get("articles", [])
    
    # Check required fields
    if not constitution.get("metadata"):
        issues.append("Missing metadata section")
    if not constitution.get("signatures"):
        issues.append("No signatures — unsigned constitution")
    if not articles:
        issues.append("No articles defined")
    
    # Check for at least one critical article
    has_critical = any(a.get("weight") == "critical" for a in articles)
    if not has_critical:
        issues.append("WARNING: No critical articles — no hard boundaries set")
    
    # Validate article structure
    for a in articles:
        if not a.get("id"):
            issues.append(f"Article missing id: {a}")
        if not a.get("title"):
            issues.append(f"Article missing title: {a}")
        if a.get("weight") not in ("critical", "high", "medium", "low"):
            issues.append(f"Article '{a.get('id')}' has invalid weight: {a.get('weight')}")
    
    return {
        "status": "READY" if not any("Missing" in i or "No sig" in i for i in issues) else "DEGRADED",
        "articles_loaded": len(articles),
        "critical_articles": sum(1 for a in articles if a.get("weight") == "critical"),
        "issues": issues,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

def propose_amendment(constitution, amendment):
    """Agent proposes an amendment (cannot modify directly)."""
    proposal = {
        "proposed_by": "agent",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "amendment": amendment,
        "status": "PENDING_HOLDER_APPROVAL",
    }
    # In reality: write to a proposals queue, notify holder
    return {
        "status": "PROPOSED",
        "message": "Amendment proposed. Holder must approve before it takes effect.",
        "proposal": proposal,
    }

def main():
    if len(sys.argv) < 3:
        print("Usage: constitution-validator.py <check|boot|propose> <constitution.yaml> [action.json|amendment.json]")
        sys.exit(1)
    
    command = sys.argv[1]
    const_path = sys.argv[2]
    constitution = load_constitution(const_path)
    
    if command == "boot":
        result = boot_check(constitution)
    elif command == "check":
        if len(sys.argv) < 4:
            print("Error: 'check' requires an action.json")
            sys.exit(1)
        with open(sys.argv[3]) as f:
            action = json.load(f)
        result = evaluate_action(constitution, action)
    elif command == "propose":
        if len(sys.argv) < 4:
            print("Error: 'propose' requires an amendment.json")
            sys.exit(1)
        with open(sys.argv[3]) as f:
            amendment = json.load(f)
        result = propose_amendment(constitution, amendment)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
