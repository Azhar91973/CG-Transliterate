from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Character-level mapping (for fallback if needed)
devanagari_mapping = {
    "अ": "अ", "आ": "आ", "इ": "इ", "ई": "ई", "उ": "उ", "ऊ": "ऊ",
    "ऋ": "ऋ", "ए": "ए", "ऐ": "ऐ", "ओ": "ओ", "औ": "औ",
    "क": "क", "ख": "ख", "ग": "ग", "घ": "घ", "ङ": "ङ",
    "च": "च", "छ": "छ", "ज": "ज", "झ": "झ", "ञ": "ञ",
    "ट": "ट", "ठ": "ठ", "ड": "ड", "ढ": "ढ", "ण": "ण",
    "त": "त", "थ": "थ", "द": "द", "ध": "ध", "न": "न",
    "प": "प", "फ": "फ", "ब": "ब", "भ": "भ", "म": "म",
    "य": "य", "र": "र", "ल": "ल", "व": "व", "श": "श",
    "ष": "ष", "स": "स", "ह": "ह",
    "ा": "ा", "ि": "ि", "ी": "ी", "ु": "ु", "ू": "ू",
    "े": "े", "ै": "ै", "ो": "ो", "ौ": "ौ", "ं": "ं", "ः": "ः",
    "्": "्"
}

word_mapping = {
    "बोलत": "बोलता",
    "खावत": "खाता",
    "जावत": "जाता",
    "अऊ": "और",
    "हवय": "है",
    "तोर": "तेरा",
    "मोर": "मेरा",
    "का": "क्या",
    "एखर": "इसका",
    "काबर": "क्यों",
    "छांट": "चुन",
    "लहुट": "लौट",
    "घलो": "भी",
    "जादा": "ज़्यादा",
    "सरलग": "सीधा",
    "बदना": "बताना",
    "धीर": "धीरे",
    "साल": "साल",
    "रात": "रात",
    "दिन": "दिन",
    "चाहे": "चाहिए",
    "मन": "मन",
    "दोर": "दो",
    "अइसे": "ऐसा",
    "करे": "करता",
    "पानी": "पानी",
    "कहाँ": "कहाँ",
    "क्या": "क्या",
    "हवई": "हवाई",
    "हम": "हम",
    "तैं": "तुम",
    "नहिं": "नहीं",
    "आजा": "आ जाओ",
    "दिया": "दी",
    "लेव": "लेव",
    "चल": "चल",
    "सिख": "सिख",
    "लाओ": "लाओ",
    "करत": "कर",
    "रोज": "रोज",
    "कहा": "कहा",
    "जो": "जो",
    "समझ": "समझ",
    "कह": "कह",
    "मिल": "मिल",
    "देख": "देख",
    "आय": "आया",
    "खत्म": "खत्म",
    "बात": "बात",
    "सब": "सब",
    "मिला": "मिला",
    "नीचे": "नीचे",
    "ऊपर": "ऊपर",
    "आगे": "आगे",
    "पीछे": "पीछे",
    "साथ": "साथ",
    "कम": "कम",
    "ज्यादा": "ज़्यादा",
    "चंगा": "अच्छा",
    "खुश": "खुश",
    "नया": "नया",
    "पुराना": "पुराना",
    "सादा": "साधा",
    "वह": "वह",
    "यह": "यह",
    "तुम": "तुम",
    "उस": "उस",
    "मुझे": "मुझे",
    "तेरे": "तेरे",
    "मेरा": "मेरा",
    "तुम्हारा": "तुम्हारा",
    "उनका": "उनका",
    "हमारा": "हमारा",
    "कहाँ": "कहाँ",
    "कब": "कब",
    "कैसा": "कैसा",
    "कौन": "कौन",
    "शहर": "शहर",
    "गांव": "गांव",
    "स्कूल": "स्कूल",
    "रोज़": "रोज़",
    "समय": "समय",
    "खेल": "खेल",
    "घर": "घर",
    "बाजार": "बाजार",
    "बड़ा": "बड़ा",
    "छोटा": "छोटा",
    "सपना": "सपना",
    "सपने": "सपने",
    "काम": "काम",
    "सोच": "सोच",
    "सांस": "सांस",
    "दिल": "दिल",
    "आलम": "आलम",
    "स्वागत": "स्वागत",
    "अच्छा": "अच्छा",
    "जाना": "जाना",
    "मुझे": "मुझे",
    "सिखाना": "सिखाना",
    "सुन": "सुन",
    "बच्चा": "बच्चा",
    "माँ": "माँ",
    "पापा": "पापा",
    "आलसी": "आलसी",
    "कभी": "कभी",
    "बिलकुल": "बिल्कुल",
    "जोड़": "जोड़",
    "गाड़ी": "गाड़ी",
    "रखना": "रखना",
    "रख": "रख",
    "जान": "जान",
    "ध्यान": "ध्यान",
    "परख": "परख",
    "वो": "वो",
    "इन": "इन",
    "सबक": "सबक",
    "मौत": "मौत",
    "बच": "बच",
    "नसीब": "नसीब",
    "झूठ": "झूठ",
    "सच्चा": "सच्चा",
    "परिश्रम": "परिश्रम",
    "आशा": "आशा",
    "नकली": "नकली",
    "समझा": "समझा",
    "अहम": "अहम",
    "गुनाह": "गुनाह",
    "पाप": "पाप",
    "राज़": "राज़",
    "हंसी": "हंसी",
    "रोना": "रोना",
    "चुप": "चुप",
    "शांत": "शांत",
    "खुशहाल": "खुशहाल",
    "संबंध": "संबंध",
    "नफरत": "नफरत",
    "प्यार": "प्यार",
    "नाव": "नाम",
    "इज्जत": "इज्जत",
    "तबियत": "तबियत",
    "कसूर": "कसूर",
    "लाइफ": "जीवन",
    "उत्सव": "उत्सव",
    "मौका": "मौका",
    "रविवार": "रविवार",
    "सोमवार": "सोमवार",
    "मंगलवार": "मंगलवार",
    "बुधवार": "बुधवार",
    "गुरुवार": "गुरुवार",
    "शुक्रवार": "शुक्रवार",
    "शनिवार": "शनिवार",
    "बचपन": "बचपन",
    "युवावस्था": "युवावस्था",
    "वृद्धावस्था": "वृद्धावस्था",
    "कुशल": "कुशल",
    "अकला": "अकेला",
    "अत्यधिक": "अत्यधिक",
    "समाधान": "समाधान",
    "सुलझा": "सुलझा",
    "चिंता": "चिंता",
    "दिमाग": "दिमाग",
    "रात": "रात",
    "दिन": "दिन",
    "आज़माइश": "आज़माइश",
    "चयन": "चयन",
    "विकास": "विकास",
    "मदद": "मदद",
    "सहारा": "सहारा",
    "समान": "समान",
    "विभिन्न": "विभिन्न",
    "सुरक्षित": "सुरक्षित",
    "बेहतर": "बेहतर",
    "आश्वासन": "आश्वासन",
    "अनुभव": "अनुभव",
    "बिगाड़": "बिगाड़",
    "समाप्त": "समाप्त",
    "अंतिम": "अंतिम",
    "खत्म": "खत्म",
    "खोजना": "खोजना",
    "साफ": "साफ",
    "ध्यान": "ध्यान",
    "शुरू": "शुरू",
    "संग": "संग",
    "निकल": "निकल",
    "फिर": "फिर",
    "मांग": "मांग",
    "समझ": "समझ",
    "समझा": "समझा",
    "खुश": "खुश",
    "बुरा": "बुरा",
    "शांति": "शांति",
    "साझा": "साझा",
    "त्योहार": "त्योहार",
    "त्योहारों": "त्योहारों",
     "कुंदरु": "कुंदरू",
    "चैला": "छैला",
    "अलबेला": "अलबेला",
    "तोर": "तेरा",
    "मोर": "मेरा",
    "आज": "आज",
    "राजा": "राजा",
    "खवाहूं": "ख्वाहिश",
    "पड़की": "कबूतर",
    "कोईली": "कोयल",
    "मैना": "मैना",
    "कोहरा": "कुहासा",
    "लोवा": "धुंआ",
    "नारे": "आवाज",
    "सरगे": "स्वर्ग",
    "बीना": "बिना",
    "हिरदे": "हृदय",
    "लहुट": "लौट",
    "घलो": "भी",
    "जादा": "ज़्यादा",
    "सरलग": "सीधा",
    "बदना": "बतलाना",
    "धीर": "धीरे",
    "चांट": "चुन",
    "लवां": "लवां",
    "मयारुं": "प्रिय",
    "झुलय": "झूलना",
    "समये": "समय",
    "कांदा": "कांदा",
    "राधे": "राधा",
    "कचालू": "शकरकंदी",
    "भाजी": "सब्जी",
    "दूध": "दूध",
    "लाज": "लाज",
    "पार": "पार",
    "तीर": "तरफ़",
    "नचावय": "नचाना",
    "मोहार": "मोहब्बत",
    "विरा": "वीर",
    "कुँआर": "क्वार",
    "मुखिया": "मुखिया",
    "फूल": "फूल",
    "घुंघरु": "घुंघरू",
    "धिना": "धिन",
    "मांदर": "मांदल",
    "सूतरी": "सूत",
    "अहम": "अहम",
    "उलट": "उलट",
    "ढेर": "ढेर",
    "हर": "हर",
    "पानी": "पानी"
}


# Transliteration function
def transliterate_chhattisgarhi_to_hindi(chhattisgarhi_text):
    words = chhattisgarhi_text.split()  # Split input text into words
    hindi_translation = []

    for word in words:
        # Check word-level mapping first
        if word in word_mapping:
            hindi_translation.append(word_mapping[word])
        else:
            # Fall back to character-level transliteration
            hindi_word = "".join([devanagari_mapping.get(char, char) for char in word])
            hindi_translation.append(hindi_word)

    return " ".join(hindi_translation)

@app.route("/")
def index():
    return render_template("index.html")  # Frontend interface

@app.route("/transliterate", methods=["POST"])
def transliterate():
    data = request.get_json()  # Get JSON data from the request
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400  # Handle missing text key
    
    chhattisgarhi_text = data.get("text", "").strip()
    if not chhattisgarhi_text:
        return jsonify({"error": "Empty input"}), 400  # Handle empty input
    
    hindi_text = transliterate_chhattisgarhi_to_hindi(chhattisgarhi_text)
    return jsonify({"hindi_text": hindi_text})  # Return the transliterated text in JSON format

if __name__ == "__main__":  
    app.run(debug=True)