import os

S = r"\scriptstyle "
BASE = os.path.dirname(os.path.abspath(__file__))

Q10 = dict(
    type="MSQ",
    body=[
        "(a) A signal $" + S + r"A\sin\omega_m t$ is input to a square-law device $" + S + r"(e_o=e_{in}^2)$. The output of the device is given to an FM modulator as the modulating signal. The frequency deviation characteristic of the FM modulator is $" + S + r"f=f_c+K\,e(t)$, where $" + S + r"e(t)$ is the modulating signal and $" + S + r"K$ is a constant. Determine the FM signal and the frequency components in its spectrum.",
        "(b) In the figure, $" + S + r"x(t)$ is the modulating signal and $" + S + r"\omega_c t$ is the carrier. Determine the value of gain $" + S + r"K$ so that the output is a suppressed carrier DSB signal.",
        "Which of the following statements are correct?",
    ],
    image=os.path.join(BASE, "GATE_ECE_1991_Q10", "q10_diagram.png"),
    image_w=4.8,
    image_after=1,
    options=[
        "After the square-law device $" + S + r"e(t)=\tfrac{A^2}{2}\left(1-\cos 2\omega_m t\right)$, and the FM signal is $" + S + r"\cos\left[2\pi\left(f_c+\tfrac{KA^2}{2}\right)t-\tfrac{\pi KA^2}{2\omega_m}\sin 2\omega_m t\right]$ (unit carrier amplitude)",
        "The spectrum has components at $" + S + r"f_c+\tfrac{KA^2}{2}\pm n\,\tfrac{\omega_m}{\pi}$ for $" + S + r"n=0,1,2,\dots$ with amplitudes proportional to $" + S + r"J_n(\beta)$, where $" + S + r"\beta=\tfrac{\pi KA^2}{2\omega_m}$",
        "The output is a suppressed carrier DSB signal when $" + S + r"K=\sqrt{\tfrac{b}{a}}$, where $" + S + r"a$ and $" + S + r"b$ are the coefficients of the two square-law blocks",
        "The output is a suppressed carrier DSB signal when $" + S + r"K=\tfrac{b}{a}$",
    ],
    tail=[
        ("Correct", ["1,2,3"]),
        ("Explanation", [
            "Part (a), modulating signal: $" + S + r"e(t)=\left(A\sin\omega_m t\right)^2=\tfrac{A^2}{2}\left(1-\cos 2\omega_m t\right)$, which has a DC part and a part at $" + S + r"2\omega_m$.",
            "Instantaneous frequency: $" + S + r"f_i=f_c+K\,e(t)=\left(f_c+\tfrac{KA^2}{2}\right)-\tfrac{KA^2}{2}\cos 2\omega_m t$. The new centre frequency is $" + S + r"f_c'=f_c+\tfrac{KA^2}{2}$, the frequency deviation is $" + S + r"\Delta f=\tfrac{KA^2}{2}$, and the modulating frequency is $" + S + r"2f_m=\tfrac{\omega_m}{\pi}$.",
            "Phase: $" + S + r"\theta(t)=2\pi\int f_i\,dt=2\pi f_c' t-\tfrac{2\pi\Delta f}{2\omega_m}\sin 2\omega_m t$. With $" + S + r"\beta=\tfrac{\Delta f}{2f_m}=\tfrac{KA^2/2}{\omega_m/\pi}=\tfrac{\pi KA^2}{2\omega_m}$, the FM signal is $" + S + r"\cos\left[2\pi f_c' t-\beta\sin 2\omega_m t\right]$, which is the expression in option (1).",
            "Spectrum: a single-tone FM wave has components $" + S + r"J_n(\beta)\cos\left[2\pi\left(f_c'+n\cdot 2f_m\right)t\right]$ at $" + S + r"f_c'\pm n\cdot 2f_m=f_c+\tfrac{KA^2}{2}\pm n\tfrac{\omega_m}{\pi}$, with amplitude $" + S + r"|J_n(\beta)|$, as in option (2).",
            "Part (b): let the carrier be $" + S + r"c(t)=\cos\omega_ct$. The upper block input is $" + S + r"K\left(x+c\right)$, the lower block input is $" + S + r"\left(x-c\right)$. Write the upper coefficient (printed as Q in the scan) as $" + S + r"a$.",
            "$" + S + r"e_{out}=aK^2(x+c)^2-b(x-c)^2=\left(aK^2-b\right)\left(x^2+c^2\right)+2\left(aK^2+b\right)xc$.",
            "For a suppressed carrier DSB output the $" + S + r"x^2$ and $" + S + r"c^2$ terms must vanish, so $" + S + r"aK^2=b$, i.e. $" + S + r"K=\sqrt{\tfrac{b}{a}}$. Then $" + S + r"e_{out}=4b\,x(t)\cos\omega_c t$, a DSB-SC signal.",
            "Hence options (1), (2) and (3) are correct.",
            "",
            "Tip: Squaring a sinusoid doubles its frequency and adds a DC term, so the FM modulator sees a tone at $" + S + r"2\omega_m$ on top of a constant that only shifts the centre frequency; for the balanced modulator, choose $" + S + r"K$ so that the squared terms of the two branches cancel and only the cross term $" + S + r"xc$ is left.",
        ]),
        ("Subject", ["Communication Systems"]),
        ("Topic", ["Analog Communication (Frequency Modulation and Demodulation)"]),
        ("Correct Marks", ["2"]),
        ("Incorrect Marks", ["0"]),
        ("Hint", ["-"]),
        ("Video Solution", ["-"]),
        ("PYQ", ["GATE ECE 1991"]),
        ("OTS ID", [""]),
    ],
)
ALL = [Q10]
