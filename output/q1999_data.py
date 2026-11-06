import os

S = r"\scriptstyle "
BASE = os.path.dirname(os.path.abspath(__file__))

Q9 = dict(
    type="MSQ",
    body=[
        "A transistor LC oscillator circuit is shown in the figure. Assume that the transistor has very high $" + S + r"\beta$ (so that you may neglect $" + S + r"r_d$). Derive an equation governing the circuit operation, and find the frequency of oscillation. Also, state the gain condition required for oscillation to start.",
        "Which of the following statements are correct?",
    ],
    image=os.path.join(BASE, "GATE_ECE_1999_Q9", "q9_diagram.png"),
    image_w=3.4,
    options=[
        "The governing equation is $" + S + r"s^3LC_1C_2+s^2\tfrac{LC_1}{R_L}+s(C_1+C_2)+\left(g_m+\tfrac{1}{R_L}\right)=0$",
        "The frequency of oscillation is $" + S + r"\omega_0=\sqrt{\tfrac{C_1+C_2}{LC_1C_2}}$",
        "The gain condition for oscillation is $" + S + r"g_mR_L>\tfrac{C_1}{C_2}$",
        "The frequency of oscillation is $" + S + r"\omega_0=\tfrac{1}{\sqrt{L(C_1+C_2)}}$",
    ],
    tail=[
        ("Correct", ["1,2,3"]),
        ("Explanation", [
            "Given: a common-base Colpitts-type circuit. The base is at ac ground, the collector is connected to the supply through $" + S + r"L$ (ac ground), $" + S + r"C_1$ is between collector and emitter, and $" + S + r"C_2$ between emitter and ground. $" + S + r"C_3=\infty$ is an ac short, so $" + S + r"R_L$ sits across $" + S + r"C_2$; the bias current source is open for ac.",
            "Small-signal model: very high $" + S + r"\beta$ means $" + S + r"i_e\approx i_c=g_mv_{be}=-g_mv_e$ (base grounded, so $" + S + r"v_{be}=-v_e$).",
            "KCL at the collector node: $" + S + r"v_c\left(\tfrac{1}{sL}+sC_1\right)=v_e\left(sC_1+g_m\right)$.",
            "KCL at the emitter node: $" + S + r"v_c\,sC_1=v_e\left(sC_1+sC_2+g_m+\tfrac{1}{R_L}\right)$.",
            "Eliminating $" + S + r"v_c/v_e$ between the two equations gives the governing equation $" + S + r"s^3LC_1C_2+s^2\tfrac{LC_1}{R_L}+s(C_1+C_2)+\left(g_m+\tfrac{1}{R_L}\right)=0$.",
            "Put $" + S + r"s=j\omega$. Imaginary part: $" + S + r"-\omega^3LC_1C_2+\omega(C_1+C_2)=0$, so $" + S + r"\omega_0^2=\tfrac{C_1+C_2}{LC_1C_2}$, i.e. $" + S + r"\omega_0=\tfrac{1}{\sqrt{L\,C_{eq}}}$ with $" + S + r"C_{eq}=\tfrac{C_1C_2}{C_1+C_2}$.",
            "Real part: $" + S + r"-\omega_0^2\tfrac{LC_1}{R_L}+g_m+\tfrac{1}{R_L}=0$. Using $" + S + r"\omega_0^2L=\tfrac{C_1+C_2}{C_1C_2}$ this becomes $" + S + r"g_m=\tfrac{1}{R_L}\tfrac{C_1}{C_2}$, so sustained oscillation needs $" + S + r"g_mR_L=\tfrac{C_1}{C_2}$ and oscillation starts when $" + S + r"g_mR_L>\tfrac{C_1}{C_2}$.",
            "Hence options (1), (2) and (3) are correct.",
            "",
            "Tip: In a Colpitts oscillator the two capacitors act in series across the inductor, so the frequency uses $" + S + r"C_{eq}=\tfrac{C_1C_2}{C_1+C_2}$ and is independent of $" + S + r"g_m$ and $" + S + r"R_L$; those two only set the start-up condition through the capacitor ratio $" + S + r"\tfrac{C_1}{C_2}$.",
        ]),
        ("Subject", ["Analog Electronics"]),
        ("Topic", ["Oscillators (Sinusoidal Oscillator Circuits and 555 timers)"]),
        ("Correct Marks", ["2"]),
        ("Incorrect Marks", ["0"]),
        ("Hint", ["-"]),
        ("Video Solution", ["-"]),
        ("PYQ", ["GATE ECE 1999"]),
        ("OTS ID", [""]),
    ],
)
