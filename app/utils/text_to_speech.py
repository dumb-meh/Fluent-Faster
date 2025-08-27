from fastapi import APIRouter, HTTPException, Body, Response
import azure.cognitiveservices.speech as speechsdk
import tempfile

router = APIRouter()

@router.post("/text_to_speech")
async def text_to_speech(request_data: str = Body(..., media_type="text/plain")):
    try:
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
        speech_config.speech_synthesis_output_format = speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3


        auto_detect_source_lang_config = speechsdk.SpeechSynthesisAutoDetectionConfig()

        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            auto_detect_source_language_config=auto_detect_source_lang_config
        )

        result = synthesizer.speak_text_async(request_data).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return Response(content=result.audio_data, media_type="audio/mpeg")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            raise HTTPException(status_code=500, detail=f"TTS canceled: {cancellation_details.reason}")
        else:
            raise HTTPException(status_code=500, detail="Text-to-speech synthesis failed.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
