# Audio Extraction

# - Handle multilingual audio content

# Instructor supports extracting structured data from audio files using the `Audio` class, making it easy to process speech and audio content.
import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
from instructor.multimodal import Audio

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define a model for audio transcription
class AudioTranscription(BaseModel):
    text: str = Field(description="Full transcription of the audio")
    speaker: str = Field(description="Identity of the speaker if known")
    language: str = Field(description="Language spoken in the audio")
    confidence: float = Field(description="Confidence score for the transcription", ge=0.0, le=1.0)

# Extract transcription from audio
def transcribe_audio(audio_path: str) -> AudioTranscription:
    """Extract structured transcription from an audio file."""
    # Load the audio using Instructor's Audio class
    audio = Audio.from_path(audio_path)

    return client.chat.completions.create(
        model="gpt-4o-audio-preview",  # Audio-capable model
        response_model=AudioTranscription,
        messages=[
            {
                "role": "user",
                "content": [
                    "Transcribe this audio file and identify the speaker and language:",
                    audio  # The Audio object is handled automatically
                ]
            }
        ]
    )

# Example usage
# transcript = transcribe_audio("path/to/audio.wav")
# print(f"Transcript: {transcript.text}")
# print(f"Speaker: {transcript.speaker}")
# print(f"Language: {transcript.language}")
# print(f"Confidence: {transcript.confidence:.2f}")

# For more specific information extraction from audio:
from typing import List, Optional
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI
from instructor.multimodal import Audio

# Initialize the client with instructor
client = instructor.from_openai(OpenAI())

# Define a model for person information
class Person(BaseModel):
    name: str = Field(description="Person's full name")
    age: int = Field(description="Person's age in years")
    occupation: Optional[str] = Field(None, description="Person's job or profession if mentioned")

# Define a model for meeting information
class MeetingPoint(BaseModel):
    topic: str = Field(description="Topic discussed")
    decision: Optional[str] = Field(None, description="Decision made on this topic")
    action_items: List[str] = Field(default_factory=list, description="Action items related to this topic")

class Meeting(BaseModel):
    title: str = Field(description="Meeting title or purpose")
    date: Optional[str] = Field(None, description="Meeting date if mentioned")
    participants: List[str] = Field(description="Names of meeting participants")
    key_points: List[MeetingPoint] = Field(description="Key discussion points and decisions")
    summary: str = Field(description="Brief summary of the meeting")

# Extract structured information from audio
def extract_meeting_info(audio_path: str) -> Meeting:
    """Extract structured meeting information from audio recording."""
    audio = Audio.from_path(audio_path)

    return client.chat.completions.create(
        model="gpt-4o-audio-preview",
        response_model=Meeting,
        messages=[
            {
                "role": "system",
                "content": "Extract detailed meeting information from this audio recording."
            },
            {
                "role": "user",
                "content": [
                    "Extract the complete meeting details from this recording:",
                    audio
                ]
            }
        ]
    )

# Extract person information
def extract_person_from_audio(audio_path: str) -> Person:
    """Extract structured person information from audio."""
    audio = Audio.from_path(audio_path)

    return client.chat.completions.create(
        model="gpt-4o-audio-preview",
        response_model=Person,
        messages=[
            {
                "role": "user",
                "content": [
                    "Extract the person's name, age, and occupation from this audio:",
                    audio
                ]
            }
        ]
    )

# Example usage
# person = extract_person_from_audio("path/to/introduction.wav")
# print(f"Name: {person.name}, Age: {person.age}")
# if person.occupation:
#     print(f"Occupation: {person.occupation}")

