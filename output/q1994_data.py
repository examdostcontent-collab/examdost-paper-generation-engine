S = r"\scriptstyle "

Q116 = dict(
    body=["Medium wave radio signals may be received at far off distances at night because"],
    options=[
        "radio waves travel faster at night",
        "ground wave attenuation is low at night",
        "the sky wave is stronger at night",
        "there is no fading at night",
    ],
    tail=[
        ("Correct", ["3"]),
        ("Explanation", [
            "Concept: medium wave signals reach far-off places mainly by the sky wave, which is reflected by the ionosphere back to the ground.",
            "During the day the lower ionospheric layer (the D layer) is strongly ionized and absorbs medium wave signals, so the sky wave is heavily attenuated and only the ground wave (short range) is useful.",
            "At night the D layer disappears, so the sky wave is absorbed much less and reaches the receiver at far-off distances with a larger strength.",
            "Hence the correct option is (3).",
            "",
            "Tip: Medium wave reception at long distances after sunset comes from reduced daytime absorption in the D layer, not from any change in wave speed; the speed of a radio wave in the medium does not depend on the time of day.",
        ]),
        ("Subject", ["EMFT - ECE"]),
        ("Topic", ["Plane Waves (Plane Waves in Lossy Media)"]),
        ("Correct Marks", ["1"]),
        ("Incorrect Marks", ["0.33"]),
        ("Hint", ["-"]),
        ("Video Solution", ["-"]),
        ("PYQ", ["GATE ECE 1994"]),
        ("OTS ID", [""]),
    ],
)

Q212 = dict(
    type="NAT",
    body=[
        "For the 2N338 transistor, the manufacturer specifies $" + S + r"P_{max}=100\ \text{mW}$ at $" + S + r"25^{\circ}\text{C}$ free-air temperature and maximum junction temperature $" + S + r"T_{j,max}=125^{\circ}\text{C}$. Its thermal resistance (in $" + S + r"^{\circ}\text{C/W}$) is ________",
    ],
    options=[],
    tail=[
        ("Correct", ["1000"]),
        ("Explanation", [
            "Given: $" + S + r"P_{max}=100\ \text{mW}=0.1\ \text{W}$ at ambient (free-air) temperature $" + S + r"T_A=25^{\circ}\text{C}$, and $" + S + r"T_{j,max}=125^{\circ}\text{C}$.",
            "Concept: the junction temperature rises above the ambient temperature by the power dissipated times the thermal resistance, $" + S + r"T_j-T_A=\theta\,P$.",
            "At the rated power, $" + S + r"T_j=T_{j,max}$, so $" + S + r"\theta=\tfrac{T_{j,max}-T_A}{P_{max}}$.",
            "$" + S + r"\theta=\tfrac{125-25}{0.1}=\tfrac{100}{0.1}=1000\ ^{\circ}\text{C/W}$ (which is the same as $" + S + r"1\ ^{\circ}\text{C/mW}$).",
            "Hence the thermal resistance is $" + S + r"1000\ ^{\circ}\text{C/W}$.",
            "",
            "Tip: The same number gives the derating slope: above $" + S + r"25^{\circ}\text{C}$ the allowed power falls by $" + S + r"\tfrac{1}{\theta}=1\ \text{mW}$ per degree, reaching zero when the ambient reaches $" + S + r"125^{\circ}\text{C}$.",
        ]),
        ("Subject", ["Analog Electronics"]),
        ("Topic", ["Amplifiers (Power Amplifiers)"]),
        ("Correct Marks", ["1"]),
        ("Incorrect Marks", ["0"]),
        ("PYQ", ["GATE ECE 1994"]),
        ("OTS ID", [""]),
    ],
)
ALL = [Q116, Q212]
