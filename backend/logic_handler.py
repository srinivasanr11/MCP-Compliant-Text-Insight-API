def summarize(text: str) -> tuple[str, str]:
    """
    Summarizes the given user text and classifies it into a category.

    Args:
        text (str): The user input or feedback text.

    Returns:
        tuple[str, str]: A tuple containing a short summary and its corresponding category.
    """
    text_lower = text.lower()  # Normalize input text to lowercase for keyword checks

    # Rule-based summarization and classification using keyword patterns
    if "login" in text_lower and "crash" in text_lower:
        return "Login functionality is unstable and crashing.", "Bug"

    if "dark mode" in text_lower:
        return "User praises the dark mode for aesthetics and comfort.", "Praise"

    if "profile" in text_lower and "settings" in text_lower:
        return "User is struggling to find the profile settings.", "Usability Issue"

    if "search" in text_lower and ("slow" in text_lower or "broken" in text_lower):
        return "Search feature is either slow or not working.", "Usability Issue"

    if "update" in text_lower and "issue" in text_lower:
        return "Recent update introduced several issues.", "Bug"

    if any(word in text_lower for word in ["feature", "enhancement", "request"]):
        return "User is requesting a new feature or enhancement.", "Feature Request"

    if any(word in text_lower for word in ["payment", "billing", "refund"]):
        return "User reports a problem with billing or payment.", "Payment Issue"

    # Default: Truncate text and label as "Other" if no rule matched
    summary = text[:100] + "..." if len(text) > 100 else text
    return summary, "Other"


def classify(text: str) -> tuple[str, float]:
    """
    Classifies the given user text into a predefined category with a confidence score.

    Args:
        text (str): The user input or feedback text.

    Returns:
        tuple[str, float]: A tuple containing the category and its confidence score.
    """
    text_lower = text.lower()  # Normalize input text to lowercase

    # Bug-related keywords
    if any(
        word in text_lower
        for word in ["crash", "error", "bug", "issue", "fail", "hang", "freeze"]
    ):
        return "Bug", 0.92

    # Feature request or improvement-related keywords
    elif any(
        word in text_lower
        for word in [
            "feature",
            "add",
            "enhancement",
            "improve",
            "suggestion",
            "request",
        ]
    ):
        return "Feature Request", 0.87

    # Praise-related keywords
    elif any(
        word in text_lower
        for word in [
            "love",
            "like",
            "great",
            "brilliant",
            "good",
            "excellent",
            "amazing",
            "thank you",
        ]
    ):
        return "Praise", 0.88

    # Usability problems
    elif any(
        word in text_lower
        for word in ["slow", "confusing", "not working", "difficult", "complex"]
    ):
        return "Usability Issue", 0.82

    # Payment or billing issues
    elif any(
        word in text_lower
        for word in ["payment", "billing", "invoice", "charge", "refund"]
    ):
        return "Payment Issue", 0.84

    # Default fallback
    else:
        return "Other", 0.70
