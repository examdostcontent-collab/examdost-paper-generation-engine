S = r"\scriptstyle "

Q310 = dict(
    type="NAT",
    body=[
        "The Laplace transform of the output of an ideal full-wave rectifier fed with $" + S + r"A\sin t$ is $" + S + r"V_0(s)=\tfrac{A}{s^2+1}\coth(\alpha s)$, where $" + S + r"\alpha$ is a constant. Determine the value of $" + S + r"\alpha$.",
    ],
    options=[],
    tail=[
        ("Correct", ["1.56 to 1.58"]),
        ("Explanation", [
            "Given: the output of a full-wave rectifier fed with $" + S + r"A\sin t$ is the periodic signal $" + S + r"v_0(t)=A|\sin t|$, whose period is $" + S + r"T=\pi$ and whose first period is $" + S + r"A\sin t$ for $" + S + r"0\leq t\leq\pi$.",
            "Concept: the Laplace transform of a periodic signal is $" + S + r"V_0(s)=\tfrac{F_1(s)}{1-e^{-sT}}$, where $" + S + r"F_1(s)$ is the transform of one period.",
            "One period: $" + S + r"F_1(s)=\int_{0}^{\pi}A\sin t\,e^{-st}\,dt=\tfrac{A\left(1+e^{-\pi s}\right)}{s^2+1}$.",
            "So $" + S + r"V_0(s)=\tfrac{A}{s^2+1}\cdot\tfrac{1+e^{-\pi s}}{1-e^{-\pi s}}$.",
            "Using $" + S + r"\tfrac{1+e^{-\pi s}}{1-e^{-\pi s}}=\tfrac{e^{\pi s/2}+e^{-\pi s/2}}{e^{\pi s/2}-e^{-\pi s/2}}=\coth\left(\tfrac{\pi s}{2}\right)$, we get $" + S + r"V_0(s)=\tfrac{A}{s^2+1}\coth\left(\tfrac{\pi s}{2}\right)$.",
            "Comparing with $" + S + r"\coth(\alpha s)$ gives $" + S + r"\alpha=\tfrac{\pi}{2}\approx 1.57$.",
            "Hence $" + S + r"\alpha$ is about $" + S + r"1.57$.",
            "",
            "Tip: The argument of coth is half the period of the rectified wave, $" + S + r"\alpha=\tfrac{T}{2}$; the full-wave rectified sine repeats every $" + S + r"\pi$ (twice as often as the input), which is why $" + S + r"\alpha=\tfrac{\pi}{2}$ and not $" + S + r"\pi$.",
        ]),
        ("Subject", ["Signals and Systems"]),
        ("Topic", ["Laplace Transform (Laplace Transform Calculation)"]),
        ("Correct Marks", ["1"]),
        ("Incorrect Marks", ["0"]),
        ("PYQ", ["GATE ECE 1995"]),
        ("OTS ID", [""]),
    ],
)
ALL = [Q310]
