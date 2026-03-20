"""語音輸入處理模組"""
import io
import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment

def convert_to_wav(audio_bytes, format_hint=None):
    """將瀏覽器或上傳的音訊轉換為 SpeechRecognition 支援的 WAV 格式"""
    try:
        audio_io = io.BytesIO(audio_bytes)
        
        if format_hint:
            audio = AudioSegment.from_file(audio_io, format=format_hint)
        else:
            audio = AudioSegment.from_file(audio_io)
            
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        return wav_io
    except Exception as e:
        return f"❌ 音訊格式轉換失敗，詳細錯誤: {e}"

def process_transcription(audio_bytes, format_hint=None):
    """執行音訊轉換與語音辨識"""
    with st.spinner("系統正在轉換格式並辨識語音中..."):
        wav_io = convert_to_wav(audio_bytes, format_hint)
        
        # 轉換失敗回傳錯誤字串
        if isinstance(wav_io, str):
            return wav_io
            
        if not wav_io:
            return "❌ 無法轉換音訊格式"

        r = sr.Recognizer()
        try:
            with sr.AudioFile(wav_io) as source:
                audio_data = r.record(source)
                # 呼叫 Google Web Speech API，指定 zh-TW
                text = r.recognize_google(audio_data, language="zh-TW")
                return text
                
        except sr.UnknownValueError:
            return "⚠️ 無法辨識語音內容（可能沒說話、聲音太小或雜音過大）。"
        except sr.RequestError as e:
            return f"❌ 無法連線至語音辨識服務: {e}"
        except Exception as e:
            return f"❌ 發生未知的錯誤: {e}"
