const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();

recognition.lang = "en-US";
recognition.continuous = false;
recognition.interimResults = false;

const mic = document.getElementById("mic");
const status = document.getElementById("status");
const response = document.getElementById("response");

mic.addEventListener("click", () => {

    mic.classList.add("active");
    status.innerHTML = "🎤 Listening...";

    recognition.start();

});

recognition.onresult = (event) => {

    const text = event.results[0][0].transcript;

    status.innerHTML = "You: " + text;

    fetch("/assistant", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            text: text
        })

    })

    .then(res => res.json())

    .then(data => {

    response.innerHTML = data.reply;

    const speech = new SpeechSynthesisUtterance(data.reply);

    speech.lang = "en-US";
    speech.rate = 1;
    speech.pitch = 1;

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(speech);

    // Open YouTube
    if (data.youtube) {
        window.open(data.youtube, "_blank");
    }

    // Open Google Search
    if (data.google) {
        window.open(data.google, "_blank");
    }

    // Open Google Maps
    if (data.maps) {
        window.open(data.maps, "_blank");
    }

    // Open Any Website
    if (data.website) {
        window.open(data.website, "_blank");
    }

    // Gmail Compose
    if (data.mail) {
        window.open(data.mail, "_blank");
    }

    // Telephone
    if (data.phone) {
        window.location.href = data.phone;
    }

    // SMS
    if (data.sms) {
        window.location.href = data.sms;
    }

});

};

recognition.onerror = () => {

    mic.classList.remove("active");

    status.innerHTML = "❌ Microphone Error";

};

recognition.onend = () => {

    mic.classList.remove("active");

    status.innerHTML = "🎙 Click microphone to speak";

};