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

        window.speechSynthesis.speak(speech);

        if (data.youtube) {
            window.open(data.youtube, "_blank");
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