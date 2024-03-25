import streamlit as st
import nemo.collections.asr as nemo_asr
import nltk as nltk
import os

nltk.download('punkt')

st.title("NLP Outcome")

transcribed_text = ""
transcribed_text_tokens = []
asr_model = nemo_asr.models.ASRModel.from_pretrained("hishab/hishab_bn_fastconformer")
st.success("ASR model has been initialized.")

audio_file = st.file_uploader("Upload an audio file", type=["wav"], disabled=not asr_model)
if audio_file is not None:
    st.text("Audio file uploaded." + audio_file.name)
    st.audio(audio_file, format='audio/wav')

    with st.spinner("Transcribing..."):
        if audio_file is not None:
            # write the file in the disk
            with open(audio_file.name, "wb") as f:
                f.write(audio_file.getbuffer())

            transcriptions = asr_model.transcribe([audio_file.name])
            
            st.success("Transcription completed.")
            # Display the transcription
            # st.write(transcriptions)
            transcribed_text = transcriptions[0]
            # tokenize the transcribed text
            tokens = nltk.word_tokenize(transcribed_text)

            # delete uploaded the audio file
            os.remove(audio_file.name)

        else:
            st.warning("Please upload an audio file.")

def partially_matched_words(phrase, text):
    # Split the phrase into individual words
    phrase_words = phrase.split()
    
    # Split the text into individual words
    text_words = text.split()
    
    partially_matched = []
    
    for word in phrase_words:
        for text_word in text_words:
            if word.lower() in text_word.lower() and text_word.lower() not in partially_matched:
                partially_matched.append(text_word)
    
    return partially_matched

# show the transcribed text
st.text_area("Transcribed Campaign Script", value=transcribed_text)


# test
# transcribed_text  = "দেখতে পাচ্ছি হলিউ সিগারেট জনপ্রিয় ব্র্যান্ড হলিউড নিয়ে আপনার সাথে একটু কথা বলতে চাই সময় হবে হ্যাঁ বলেনা একটু বসে কথা বলি স্য কথা বলার শুরুতে আপনার কিছু গুরুত্বপূর্ণ দ থেকে সাহায্য নাম্বারটি একটু বলবেনাইম জিরো ওয়ান সেভেন ওয়ান টু ডবল থ্রি এইট সেভেন থ্রি ওয়ানমে গেছে স্যার আপনি কি প্রাইমারি ব্র্যান্ড্ড হিসেবে সবসময় হলিউ ঠিক খান হলিউড খাচ্চ্ছে আর কি অনেকদিন ধরে গেছে ছবি আইডি কার্ড আছে শনাক্ত করতে পারি হ্যাঁ আমার হল ড্রাইভিং লাইসেন্স আছেটু স্যার আপনার পুরো নামটা একটু যদি বলতেন মোহাম্মদ সাময়েল খান বাবার নাম জাহাঙ্গীর আলম ঠিকানাটা কোন এলাকাতে আমি থাকি এখন হল মোহাম্মদপুর স্যার আপনি"
# show transcibed text
# st.text_area("Transcribed text", value=transcribed_text)
        
# extract keywords from the transcribed text
keywords = [
        "দেখতে পাচ্ছি আপনি একজন ধূমপায়ী আপনার প্রিয় সিগারেট ব্রান্ড হলিউড নিয়ে আপনার সাথে কিছু কথা বলতে চাচ্ছি একটু সময় দিবেন", 
        "হলিউড এর সাথে থাকার জন্য শুরুতেই আপনাকে জানাই অসংখ্য ধন্যবাদ। আপনি হয়ত জানেন এক যুগেরও বেশি সময় ধরে আপনার মত স্বপ্ন জয়ীদের সাথে আছে হলিউড",
        "গ্লোরি অফ হলিউড প্যাক",
        "গোল্ডেন সিল অফ কোয়ালিটি",
        "মর্ডান এবং স্টাইলিশ",
        "গ্লোরিয়াস জার্নি",
        "ম্যাচ বক্স"
]

matched_keywords = []

for keyword in keywords:
    matched = partially_matched_words(keyword, transcribed_text)
    if matched:
        matched_keywords.append(" ".join(matched))
    else:
        matched_keywords.append("")
    
# show the result in table
# thre columns: keyword, matched words, matched percentage
data = []
for i, keyword in enumerate(keywords):
    percent_matched = round(len(matched_keywords[i].split()) / len(keyword.split()) * 100)
    if percent_matched > 100:
        percent_matched = 100

    data.append([
        keyword, 
        matched_keywords[i],
        # calculate the percentage of matched words
        str(percent_matched) + "%"
    ])

# table title
st.write("Matched Keywords")
# table
st.table(data)