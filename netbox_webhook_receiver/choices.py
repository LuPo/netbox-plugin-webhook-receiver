from utilities.choices import ChoiceSet


class WebhookAuthMethodChoices(ChoiceSet):
    TOKEN = "site"
    SIGNATURE_VERIFICATION = "signature_verification"

    CHOICES = [
        (TOKEN, "Token"),
        (SIGNATURE_VERIFICATION, "Signature Verification"),
    ]
