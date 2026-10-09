S = r"\scriptstyle "

Q86 = dict(
    body=[
        "In a microwave test bench, why is the microwave signal amplitude modulated at $" + S + r"1\ \text{kHz}$?",
    ],
    options=[
        "To increase the sensitivity of measurement",
        "To transmit the signal to a far-off place",
        "To study amplitude modulations",
        "Because crystal detector fails at microwave frequencies",
    ],
    tail=[
        ("Correct", ["4"]),
        ("Explanation", [
            "Concept: a crystal detector in a microwave test bench is a square-law diode detector. For an unmodulated (continuous wave) microwave signal it can only give a steady DC output, which cannot be amplified or measured reliably because of drift and noise.",
            "The microwave carrier is therefore amplitude modulated by a $" + S + r"1\ \text{kHz}$ signal, so the crystal detector recovers a $" + S + r"1\ \text{kHz}$ envelope at its output. This audio-frequency signal is then amplified and read on a tuned meter, because the detector itself cannot handle the microwave frequency directly.",
            "Hence the correct option is (4).",
            "",
            "Tip: Think of the $" + S + r"1\ \text{kHz}$ modulation as a way of bringing the measurement down to audio frequency; the microwave frequency is far above anything the detector output circuit can follow, while a $" + S + r"1\ \text{kHz}$ envelope is easy to amplify.",
        ]),
        ("Subject", ["EMFT - ECE"]),
        ("Topic", ["Waveguides (Rectangular Waveguides)"]),
        ("Correct Marks", ["2"]),
        ("Incorrect Marks", ["0.66"]),
        ("Hint", ["-"]),
        ("Video Solution", ["-"]),
        ("PYQ", ["GATE ECE 2004"]),
        ("OTS ID", [""]),
    ],
)
