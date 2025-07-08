def run_compliance_check(config):
    score = 0
    feedback = []

    if config.get("data_encrypted"):
        score += 1
    else:
        feedback.append("❌ Data should be encrypted to comply with GDPR.")

    if config.get("user_consent"):
        score += 1
    else:
        feedback.append("❌ User consent is required before data collection.")

    if config.get("device_authentication"):
        score += 1
    else:
        feedback.append("❌ Devices should be authenticated securely (NIST).")

    if config.get("audit_logs"):
        score += 1
    else:
        feedback.append("❌ Maintain proper audit logs (NIST requirement).")

    total = 4
    percentage = int((score / total) * 100)
    status = "✅ Compliant" if percentage >= 75 else "⚠️ Partial / Non-Compliant"

    return {
        "score": percentage,
        "status": status,
        "feedback": feedback
    }

