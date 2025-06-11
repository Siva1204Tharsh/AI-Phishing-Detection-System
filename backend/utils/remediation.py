def get_remediation_action(is_phishing):
    if is_phishing:
        return {
            "action": "Phishing detected",
            "steps": [
                "Avoid clicking on any links.",
                "Report this message to your IT department.",
                "Block the sender if not recognized."
            ]
        }
    else:
        return {
            "action": "No phishing detected",
            "steps": ["No action needed."]
        }
