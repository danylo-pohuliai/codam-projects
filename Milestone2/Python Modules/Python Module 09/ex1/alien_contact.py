from enum import Enum
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field, model_validator, ValidationError


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def validate_business_rules(self) -> 'AlienContact':
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if self.contact_type == ContactType.TELEPATHIC and \
           self.witness_count < 3:
            raise ValueError("Telepathic contact requires"
                             " at least 3 witnesses")
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) should"
                             " include received messages")
        return self


valid_report: dict[str, Any] = {
    'contact_id': "AC_2024_001",
    'timestamp': datetime(2019, 6, 1, 12, 22),
    'location': "Area 51, Nevada",
    'contact_type': ContactType.RADIO,
    'signal_strength': 8.5,
    'duration_minutes': 45,
    'witness_count': 5,
    'is_verified': True,
    'message_received': "Greetings from Zeta Reticuli"
}

invalid_report: dict[str, Any] = {
    'contact_id': "AC_2024_001",
    'timestamp': datetime(2019, 6, 1, 12, 22),
    'location': "Area 51, Nevada",
    'contact_type': ContactType.TELEPATHIC,
    'signal_strength': 8.5,
    'duration_minutes': 45,
    'witness_count': 2,
    'is_verified': True,
    'message_received': "Greetings from Zeta Reticuli"
}


if __name__ == "__main__":
    try:
        rep1 = AlienContact(**valid_report)
        print("Alien Contact Log Validation")
        print("======================================")
        print("Valid contact report:")
        print(f"ID: {rep1.contact_id}")
        print(f"Type: {rep1.contact_type.value}")
        print(f"Location: {rep1.location}")
        print(f"Signal: {rep1.signal_strength}/10")
        print(f"Duration: {rep1.duration_minutes} minutes")
        print(f"Witnesses: {rep1.witness_count}")
        print(f"Message: '{rep1.message_received}'")
    except ValidationError as e:
        msg = e.errors()[0]['msg'].replace("Value error, ", "")
        print(f"Expected validation error:\n{msg}")
    print("\n======================================")
    try:
        AlienContact(**invalid_report)
    except ValidationError as e:
        msg = e.errors()[0]['msg'].replace("Value error, ", "")
        print(f"Expected validation error:\n{msg}")
