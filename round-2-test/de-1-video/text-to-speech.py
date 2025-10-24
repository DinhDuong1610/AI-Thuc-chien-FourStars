from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()
synthesis_input = texttospeech.SynthesisInput(text="Xin chào...")
voice = texttospeech.VoiceSelectionParams(
    language_code="vi-VN", name="vi-VN-Standard-A"
)
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
audio = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
with open("voice.mp3", "wb") as f:
    f.write(audio.audio_content)
