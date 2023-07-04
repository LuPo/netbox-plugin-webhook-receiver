from utilities.choices import ChoiceSet


class WebhookAuthMethodChoices(ChoiceSet):
    TOKEN = "token"
    SIGNATURE_VERIFICATION = "signature_verification"

    CHOICES = [
        (TOKEN, "Token"),
        (SIGNATURE_VERIFICATION, "Signature Verification"),
    ]


class HashingAlgorithmChoices(ChoiceSet):
    SHA_256 = "sha256"
    SHA_512 = "sha512"

    CHOICES = (
        (SHA_256, "SHA-256"),
        (SHA_512, "SHA-512"),
    )
