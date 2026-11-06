S = r"\scriptstyle "


def tail(correct, subject, topic, explanation):
    return [
        ("Correct", [correct]),
        ("Explanation", explanation),
        ("Subject", [subject]),
        ("Topic", [topic]),
        ("Correct Marks", ["1"]),
        ("Incorrect Marks", ["0.33"]),
        ("Hint", ["-"]),
        ("Video Solution", ["-"]),
        ("PYQ", ["GATE ECE 1998"]),
        ("OTS ID", [""]),
    ]


def m(x):
    return "$" + S + x + "$"


Q123 = dict(
    body=[
        "The transfer function of a phase lead controller is $" + S + r"\tfrac{1+3Ts}{1+Ts}$. The maximum value of phase provided by this controller is",
    ],
    options=[m(r"90^{\circ}"), m(r"60^{\circ}"), m(r"45^{\circ}"), m(r"30^{\circ}")],
    tail=tail("4", "Control Systems", "Control System Design (Compensators)", [
        "Given: $" + S + r"G_c(s)=\tfrac{1+3Ts}{1+Ts}$, a lead network with zero at $" + S + r"\tfrac{1}{3T}$ and pole at $" + S + r"\tfrac{1}{T}$.",
        "Phase: $" + S + r"\phi(\omega)=\tan^{-1}(3\omega T)-\tan^{-1}(\omega T)$.",
        "The maximum phase occurs at the geometric mean of the zero and pole frequencies, $" + S + r"\omega_m=\tfrac{1}{\sqrt{3}\,T}$.",
        "At this frequency: $" + S + r"\phi_m=\tan^{-1}(\sqrt{3})-\tan^{-1}\left(\tfrac{1}{\sqrt{3}}\right)=60^{\circ}-30^{\circ}=30^{\circ}$.",
        "Check with the standard formula, with $" + S + r"\alpha=3$: $" + S + r"\sin\phi_m=\tfrac{\alpha-1}{\alpha+1}=\tfrac{2}{4}=\tfrac{1}{2}$, so $" + S + r"\phi_m=30^{\circ}$.",
        "Hence the correct option is (4).",
        "",
        "Tip: For a lead network $" + S + r"\tfrac{1+\alpha Ts}{1+Ts}$ the maximum phase depends only on the ratio $" + S + r"\alpha$ of pole to zero frequency, through $" + S + r"\sin\phi_m=\tfrac{\alpha-1}{\alpha+1}$; a ratio of $" + S + r"3$ gives only $" + S + r"30^{\circ}$, and $" + S + r"90^{\circ}$ would need an infinite ratio.",
    ]),
)

Q135 = dict(
    body=[
        "A high Q-quartz crystal exhibits series resonance at the frequency $" + S + r"\omega_s$ and parallel resonance at the frequency $" + S + r"\omega_p$. Then",
    ],
    options=[
        m(r"\omega_s") + " is very close to, but less than " + m(r"\omega_p"),
        m(r"\omega_s\ll\omega_p"),
        m(r"\omega_s") + " is very close to, but greater than " + m(r"\omega_p"),
        m(r"\omega_s\gg\omega_p"),
    ],
    tail=tail("1", "Analog Electronics", "Oscillators (Sinusoidal Oscillator Circuits and 555 timers)", [
        "Concept: the crystal's equivalent circuit is a series branch $" + S + r"L$, $" + S + r"C$ (and a small loss resistance) in parallel with the holder capacitance $" + S + r"C_0$.",
        "Series resonance (only the series branch): $" + S + r"\omega_s=\tfrac{1}{\sqrt{LC}}$.",
        "Parallel resonance (the series branch resonates with $" + S + r"C$ in series with $" + S + r"C_0$): $" + S + r"\omega_p=\tfrac{1}{\sqrt{L\,\tfrac{CC_0}{C+C_0}}}=\omega_s\sqrt{1+\tfrac{C}{C_0}}$.",
        "For a quartz crystal $" + S + r"C\ll C_0$ (for example femtofarads against picofarads), so $" + S + r"\sqrt{1+\tfrac{C}{C_0}}$ is only slightly greater than $" + S + r"1$.",
        "Therefore $" + S + r"\omega_s$ is very close to, but slightly less than, $" + S + r"\omega_p$.",
        "Hence the correct option is (1).",
        "",
        "Tip: The factor $" + S + r"\sqrt{1+\tfrac{C}{C_0}}$ is always greater than $" + S + r"1$, so parallel resonance is above series resonance; in a crystal the gap is tiny because $" + S + r"C\ll C_0$, which is why the usable inductive window between $" + S + r"\omega_s$ and $" + S + r"\omega_p$ is so narrow and stable.",
    ]),
)
ALL = [Q123, Q135]
