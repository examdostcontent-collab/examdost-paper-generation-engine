import os

S = r"\scriptstyle "
BASE = os.path.dirname(os.path.abspath(__file__))


def m(x):
    return "$" + S + x + "$"


Q54 = dict(
    body=[
        "Match List-I with List-II.",
        "List-I",
        "(1) Wave tilt",
        "(2) Faraday rotation",
        "List-II",
        "(a) Under-water propagation",
        "(b) Ground wave propagation",
        "(c) Space wave propagation",
        "(d) Ionospheric propagation",
    ],
    options=[
        "(1)-(b), (2)-(d)",
        "(1)-(a), (2)-(c)",
        "(1)-(c), (2)-(a)",
        "(1)-(d), (2)-(b)",
    ],
    tail=[
        ("Correct", ["1"]),
        ("Explanation", [
            "Wave tilt: a ground wave travels along the lossy earth. Because the ground is not a perfect conductor, the wavefront tilts forward and gets a small component of electric field along the direction of travel. This forward tilt of the wavefront is called wave tilt, so (1) goes with (b) ground wave propagation.",
            "Faraday rotation: in the ionosphere the electrons move in the earth's magnetic field, which makes the medium anisotropic (gyrotropic). A linearly polarized wave passing through it has its plane of polarization rotated. This is Faraday rotation, so (2) goes with (d) ionospheric propagation.",
            "So the matching is (1)-(b) and (2)-(d).",
            "Hence the correct option is (1).",
            "",
            "Tip: Link each effect to the medium that causes it: a lossy, finitely conducting earth tilts the wavefront of a ground wave, while the ionized, magnetized plasma of the ionosphere rotates the polarization of a sky wave passing through it.",
        ]),
        ("Subject", ["EMFT - ECE"]),
        ("Topic", ["Plane Waves (Polarization of Plane Waves)"]),
        ("Correct Marks", ["2"]),
        ("Incorrect Marks", ["0.66"]),
        ("Hint", ["-"]),
        ("Video Solution", ["-"]),
        ("PYQ", ["GATE ECE 1997"]),
        ("OTS ID", [""]),
    ],
)

Q10 = dict(
    type="MSQ",
    body=[
        "In the circuit of the figure, $" + S + r"R=100\ \Omega$, $" + S + r"L=20\ \text{nH}$ and $" + S + r"C=32\ \text{pF}$. The circuit is maintained at a temperature of $" + S + r"300\ \text{K}$. Derive and plot the power spectral density of the voltage $" + S + r"V_o$. Mark all the relevant points on the plot with numerical values. (The Boltzmann constant $" + S + r"k=1.28\times 10^{-23}\ \text{J/K}$)",
        "Which of the following statements are correct?",
    ],
    image=os.path.join(BASE, "GATE_ECE_1997_Q10", "q10_diagram.png"),
    image_w=2.6,
    options=[
        "The PSD of $" + S + r"V_o$ is $" + S + r"S_v(f)=\tfrac{4kTR}{1+Q^2\left(\tfrac{f}{f_0}-\tfrac{f_0}{f}\right)^2}$",
        "The resonant frequency is $" + S + r"f_0\approx 199\ \text{MHz}$, the quality factor is $" + S + r"Q=4$ and the $" + S + r"3\ \text{dB}$ bandwidth is about $" + S + r"49.7\ \text{MHz}$",
        "The peak value of the PSD, at $" + S + r"f_0$, is $" + S + r"4kTR\approx 1.54\times 10^{-18}\ \text{V}^2/\text{Hz}$",
        "The total mean-square noise voltage is $" + S + r"\tfrac{kT}{L}$",
    ],
    tail=[
        ("Correct", ["1,2,3"]),
        ("Explanation", [
            "Given: $" + S + r"R=100\ \Omega$, $" + S + r"L=20\ \text{nH}$, $" + S + r"C=32\ \text{pF}$, $" + S + r"T=300\ \text{K}$, $" + S + r"k=1.28\times 10^{-23}\ \text{J/K}$. Only the resistor generates thermal noise; $" + S + r"L$ and $" + S + r"C$ are noiseless.",
            "Model: the resistor's noise is a current source of PSD $" + S + r"\tfrac{4kT}{R}\ \text{A}^2/\text{Hz}$ in parallel with the $" + S + r"R$-$" + S + r"L$-$" + S + r"C$ network. The output voltage is this current times the parallel impedance $" + S + r"Z(f)$, so $" + S + r"S_v(f)=\tfrac{4kT}{R}\,|Z(f)|^2$.",
            "Parallel resonant impedance: $" + S + r"|Z(f)|^2=\tfrac{R^2}{1+Q^2\left(\tfrac{f}{f_0}-\tfrac{f_0}{f}\right)^2}$, with $" + S + r"f_0=\tfrac{1}{2\pi\sqrt{LC}}$ and $" + S + r"Q=R\sqrt{\tfrac{C}{L}}$.",
            "Therefore $" + S + r"S_v(f)=\tfrac{4kTR}{1+Q^2\left(\tfrac{f}{f_0}-\tfrac{f_0}{f}\right)^2}$.",
            "Numbers: $" + S + r"\sqrt{LC}=\sqrt{20\times 10^{-9}\times 32\times 10^{-12}}=0.8\ \text{ns}$, so $" + S + r"\omega_0=1.25\times 10^{9}\ \text{rad/s}$ and $" + S + r"f_0=\tfrac{\omega_0}{2\pi}\approx 199\ \text{MHz}$. $" + S + r"Q=100\sqrt{\tfrac{32\times 10^{-12}}{20\times 10^{-9}}}=100\times 0.04=4$, so the $" + S + r"3\ \text{dB}$ bandwidth is $" + S + r"\tfrac{f_0}{Q}\approx 49.7\ \text{MHz}$.",
            "Peak: $" + S + r"S_v(f_0)=4kTR=4\times 1.28\times 10^{-23}\times 300\times 100\approx 1.54\times 10^{-18}\ \text{V}^2/\text{Hz}$. Half of this value (about $" + S + r"0.77\times 10^{-18}$) occurs at $" + S + r"f\approx 175.6\ \text{MHz}$ and $" + S + r"225.3\ \text{MHz}$, the half-power points.",
            "Check: the total mean-square voltage is $" + S + r"\int_0^\infty S_v\,df=\tfrac{kT}{C}=\tfrac{1.28\times 10^{-23}\times 300}{32\times 10^{-12}}=1.2\times 10^{-10}\ \text{V}^2$ (about $" + S + r"11\ \mu\text{V}$ rms), independent of $" + S + r"R$.",
            "Hence options (1), (2) and (3) are correct.",
            "",
            "Tip: The plot is a single resonance peak of height $" + S + r"4kTR$ at $" + S + r"f_0$ with width $" + S + r"\tfrac{f_0}{Q}$, and the area under it always comes out as $" + S + r"\tfrac{kT}{C}$ whatever the value of $" + S + r"R$, because a larger $" + S + r"R$ gives a taller but narrower peak.",
        ]),
        ("Subject", ["Analog Electronics"]),
        ("Topic", ["Signal Conditioning, Noise and Interference (Noise (Thermal, Shot, Flicker))"]),
        ("Correct Marks", ["2"]),
        ("Incorrect Marks", ["0"]),
        ("Hint", ["-"]),
        ("Video Solution", ["-"]),
        ("PYQ", ["GATE ECE 1997"]),
        ("OTS ID", [""]),
    ],
)
ALL = [Q54, Q10]
