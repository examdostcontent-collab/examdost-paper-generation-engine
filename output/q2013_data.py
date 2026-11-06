S = r"\scriptstyle "


def row_tail(correct, explanation, topic):
    return [
        ("Correct", [correct]),
        ("Explanation", explanation),
        ("Subject", ["Signals and Systems"]),
        ("Topic", [topic]),
        ("Correct Marks", ["1"]),
        ("Incorrect Marks", ["0.33"]),
        ("Hint", ["-"]),
        ("Video Solution", ["-"]),
        ("PYQ", ["GATE ECE 2013"]),
        ("OTS ID", [""]),
    ]


Q3 = dict(
    body=[
        "Two systems with impulse responses $" + S + r"h_1(t)$ and $" + S + r"h_2(t)$ are connected in cascade. Then the overall impulse response of the cascaded system is given by",
    ],
    options=[
        "product of $" + S + r"h_1(t)$ and $" + S + r"h_2(t)$",
        "sum of $" + S + r"h_1(t)$ and $" + S + r"h_2(t)$",
        "convolution of $" + S + r"h_1(t)$ and $" + S + r"h_2(t)$",
        "subtraction of $" + S + r"h_2(t)$ from $" + S + r"h_1(t)$",
    ],
    tail=row_tail("3", [
        "Given: two LTI systems with impulse responses $" + S + r"h_1(t)$ and $" + S + r"h_2(t)$ connected in cascade, so the output of the first is the input of the second.",
        "For an input $" + S + r"x(t)$, the output of the first system is $" + S + r"y_1(t)=x(t)*h_1(t)$.",
        "This is the input of the second system, so $" + S + r"y(t)=y_1(t)*h_2(t)=\left[x(t)*h_1(t)\right]*h_2(t)$.",
        "Convolution is associative, so $" + S + r"y(t)=x(t)*\left[h_1(t)*h_2(t)\right]$.",
        "Comparing with $" + S + r"y(t)=x(t)*h(t)$ gives the overall impulse response $" + S + r"h(t)=h_1(t)*h_2(t)$.",
        "Hence the correct option is (3).",
        "",
        "Tip: Cascaded LTI systems multiply in the frequency domain, $" + S + r"H(s)=H_1(s)H_2(s)$, which is the same statement as convolution in time; and because convolution is commutative, swapping the order of the two systems leaves the overall $" + S + r"h(t)$ unchanged.",
    ], "LTI Systems (LTI System Properties)"),
)

Q8 = dict(
    body=[
        "The impulse response of a system is $" + S + r"h(t)=t\,u(t)$. For an input $" + S + r"u(t-1)$, the output is",
    ],
    options=[
        "$" + S + r"\tfrac{t^2}{2}u(t)$",
        "$" + S + r"\tfrac{t(t-1)}{2}u(t-1)$",
        "$" + S + r"\tfrac{(t-1)^2}{2}u(t-1)$",
        "$" + S + r"\tfrac{t^2-1}{2}u(t-1)$",
    ],
    tail=row_tail("3", [
        "Given: $" + S + r"h(t)=t\,u(t)$ and input $" + S + r"x(t)=u(t-1)$.",
        "Step 1: response to a unit step $" + S + r"u(t)$. $" + S + r"y_0(t)=\int_{0}^{t}h(\tau)\,d\tau=\int_{0}^{t}\tau\,d\tau=\tfrac{t^2}{2}u(t)$.",
        "Step 2: the system is time-invariant, so a delay of 1 s in the input delays the output by 1 s. $" + S + r"y(t)=y_0(t-1)=\tfrac{(t-1)^2}{2}u(t-1)$.",
        "Check by convolution: $" + S + r"y(t)=\int_{0}^{t-1}\tau\,d\tau=\tfrac{(t-1)^2}{2}$ for $" + S + r"t\geq 1$.",
        "Hence the correct option is (3).",
        "",
        "Tip: For a step input, the output of an LTI system is simply the running integral of $" + S + r"h(t)$; here the ramp $" + S + r"t\,u(t)$ integrates to $" + S + r"\tfrac{t^2}{2}$, and the only change for the delayed step is replacing $" + S + r"t$ by $" + S + r"t-1$ everywhere, including inside the step function.",
    ], "LTI Systems (Continuous Convolution)"),
)

Q16 = dict(
    body=[
        "A band-limited signal with a maximum frequency of $" + S + r"5\ \text{kHz}$ is to be sampled. According to the sampling theorem, the sampling frequency which is not valid is",
    ],
    options=[
        "$" + S + r"5\ \text{kHz}$",
        "$" + S + r"12\ \text{kHz}$",
        "$" + S + r"15\ \text{kHz}$",
        "$" + S + r"20\ \text{kHz}$",
    ],
    tail=row_tail("1", [
        "Given: maximum signal frequency $" + S + r"f_m=5\ \text{kHz}$.",
        "Concept: the sampling theorem requires the sampling frequency to be at least twice the maximum signal frequency, $" + S + r"f_s\geq 2f_m$, so that the spectral copies do not overlap.",
        "Minimum (Nyquist) rate: $" + S + r"f_s\geq 2\times 5\ \text{kHz}=10\ \text{kHz}$.",
        "A sampling frequency of $" + S + r"5\ \text{kHz}$ is below $" + S + r"10\ \text{kHz}$, so it violates the theorem.",
        "Hence the correct option is (1).",
        "",
        "Tip: Always compare the sampling rate with twice the highest frequency present in the signal, here $" + S + r"2	imes 5=10\ 	ext{kHz}$; the theorem gives only a lower limit, so any rate above that minimum is acceptable.",
    ], "Sampling (Sampling)"),
)
