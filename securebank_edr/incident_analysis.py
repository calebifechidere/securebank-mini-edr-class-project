from datetime import datetime


def sort_events(events):
    """Arrange supporting events from oldest to newest."""

    def get_time(event):
        timestamp = event.get("timestamp_utc", "")

        try:
            return datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )
        except (ValueError, TypeError):
            return datetime.min

    return sorted(events, key=get_time)


def analyze_incident(incident, events):
    """
    Analyse an incident and its supporting evidence.

    Returns an investigation summary for the analyst.
    """

    if not isinstance(incident, dict):
        raise ValueError("Incident must be a dictionary.")

    if not isinstance(events, list):
        raise ValueError("Events must be provided as a list.")

    # Arrange events chronologically
    timeline = sort_events(events)

    # Identify affected files
    affected_files = set()

    for event in timeline:
        filename = event.get("file")

        if filename:
            affected_files.add(filename)

    # Collect event types
    event_types = sorted({
        event.get("event_type", "UNKNOWN")
        for event in timeline
    })

    # Get incident information
    title = incident.get("title", "Untitled incident")
    severity = incident.get("severity", "UNKNOWN")
    rule_reason = incident.get(
        "rule_reason",
        "No detection explanation was provided."
    )

    # Prepare observations
    observations = [
        f"{len(timeline)} supporting events were examined.",
        f"{len(affected_files)} distinct files were affected."
    ]

    if event_types:
        observations.append(
            "Recorded event types: " + ", ".join(event_types)
        )

    # Assess the evidence without assuming malicious intent
    assessment = (
        "The recorded activity matches the detection information "
        "provided by the EDR. This alone does not prove that the "
        "activity was malicious."
    )

    # Recommend next steps
    recommendations = [
        "Verify whether the file changes were authorised.",
        "Review the event timestamps and supporting evidence.",
        "Preserve relevant logs for further investigation."
    ]

    if not timeline:
        recommendations.insert(
            0,
            "Collect and verify supporting evidence before drawing conclusions."
        )

    # Build the investigation report
    investigation = {
        "incident_title": title,
        "severity": severity,
        "detection_reason": rule_reason,
        "affected_files": sorted(affected_files),
        "event_count": len(timeline),
        "timeline": timeline,
        "observations": observations,
        "assessment": assessment,
        "uncertainty": (
            "The available file-change evidence cannot establish "
            "who caused the changes or whether they were malicious."
        ),
        "recommendations": recommendations
    }

    return investigation
