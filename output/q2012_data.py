S = r"\scriptstyle "


def tail(correct, marks, neg, explanation, topic):
    return [
        ("Correct", [correct]),
        ("Explanation", explanation),
        ("Subject", ["Signals and Systems"]),
        ("Topic", [topic]),
        ("Correct Marks", [marks]),
        ("Incorrect Marks", [neg]),
        ("Hint", ["-"]),
        ("Video Solution", ["-"]),
        ("PYQ", ["GATE ECE 2012"]),
        ("OTS ID", [""]),
    ]


Q11 = dict(
    body=[
        "The unilateral Laplace transform of $" + S + r"f(t)$ is $" + S + r"\tfrac{1}{s^2+s+1}$. The unilateral Laplace transform of $" + S + r"t\,f(t)$ is",
    ],
    options=[
        "$" + S + r"-\tfrac{s}{(s^2+s+1)^2}$",
        "$" + S + r"-\tfrac{2s+1}{(s^2+s+1)^2}$",
        "$" + S + r"\tfrac{s}{(s^2+s+1)^2}$",
        "$" + S + r"\tfrac{2s+1}{(s^2+s+1)^2}$",
    ],
    tail=tail("4", "1", "0.33", [
        "Given: $" + S + r"F(s)=\mathcal{L}\{f(t)\}=\tfrac{1}{s^2+s+1}$.",
        "Concept: multiplication by $" + S + r"t$ in the time domain corresponds to differentiation in the $" + S + r"s$-domain, $" + S + r"\mathcal{L}\{t\,f(t)\}=-\tfrac{d}{ds}F(s)$.",
        "Differentiate: $" + S + r"\tfrac{d}{ds}\left(s^2+s+1\right)^{-1}=-\tfrac{2s+1}{(s^2+s+1)^2}$.",
        "Therefore $" + S + r"\mathcal{L}\{t\,f(t)\}=-\left[-\tfrac{2s+1}{(s^2+s+1)^2}\right]=\tfrac{2s+1}{(s^2+s+1)^2}$.",
        "Hence the correct option is (4).",
        "",
        "Tip: The minus sign in $" + S + r"-\tfrac{dF}{ds}$ cancels the minus that comes from differentiating the reciprocal $" + S + r"\left(s^2+s+1\right)^{-1}$, so the final result here is positive and the numerator is just the derivative $" + S + r"2s+1$ of the denominator.",
    ], "Laplace Transform (Laplace Transform Properties)"),
)

Q18 = dict(
    body=[
        "If $" + S + r"x[n]=(1/3)^{|n|}-(1/2)^{n}u[n]$, then the region of convergence (ROC) of its $" + S + "Z$-transform in the $" + S + "Z$-plane will be",
    ],
    options=[
        "$" + S + r"\tfrac{1}{3}<|z|<3$",
        "$" + S + r"\tfrac{1}{3}<|z|<\tfrac{1}{2}$",
        "$" + S + r"\tfrac{1}{2}<|z|<3$",
        "$" + S + r"\tfrac{1}{3}<|z|$",
    ],
    tail=tail("3", "1", "0.33", [
        "Given: $" + S + r"x[n]=x_1[n]-x_2[n]$ with $" + S + r"x_1[n]=(1/3)^{|n|}$ and $" + S + r"x_2[n]=(1/2)^{n}u[n]$.",
        "Step 1: $" + S + r"x_1[n]=(1/3)^{|n|}$ is two-sided, made of a right-sided part $" + S + r"(1/3)^n u[n]$ (ROC $" + S + r"|z|>\tfrac{1}{3}$) and a left-sided part $" + S + r"(1/3)^{-n}u[-n-1]=3^{n}u[-n-1]$ (ROC $" + S + r"|z|<3$). So the ROC of $" + S + r"X_1(z)$ is $" + S + r"\tfrac{1}{3}<|z|<3$.",
        "Step 2: $" + S + r"x_2[n]=(1/2)^{n}u[n]$ is right-sided with its pole at $" + S + r"z=\tfrac{1}{2}$, so its ROC is $" + S + r"|z|>\tfrac{1}{2}$.",
        "Step 3: the ROC of the difference is the common region: $" + S + r"\left(\tfrac{1}{3}<|z|<3\right)\cap\left(|z|>\tfrac{1}{2}\right)=\tfrac{1}{2}<|z|<3$.",
        "Hence the correct option is (3).",
        "",
        "Tip: When a sequence is a sum or difference of terms, intersect the ROCs of the individual terms; the pole at $" + S + r"z=\tfrac{1}{2}$ of the right-sided part is what pushes the inner radius up from $" + S + r"\tfrac{1}{3}$ to $" + S + r"\tfrac{1}{2}$ here.",
    ], "Z Transform (Z-Transform Calculation)"),
)

Q29 = dict(
    body=[
        "The input $" + S + r"x(t)$ and output $" + S + r"y(t)$ of a system are related as $" + S + r"y(t)=\int_{0}^{t}x(\tau)\cos(3\tau)\,d\tau$. The system is",
    ],
    options=[
        "time-invariant and stable",
        "stable and not time-invariant",
        "time-invariant and not stable",
        "not time-invariant and not stable",
    ],
    tail=tail("4", "2", "0.66", [
        "Given: $" + S + r"y(t)=\int_{0}^{t}x(\tau)\cos(3\tau)\,d\tau$.",
        "Time invariance: delay the input to $" + S + r"x(t-t_0)$. The new output is $" + S + r"y_1(t)=\int_{0}^{t}x(\tau-t_0)\cos(3\tau)\,d\tau$. Put $" + S + r"u=\tau-t_0$: $" + S + r"y_1(t)=\int_{-t_0}^{t-t_0}x(u)\cos\left(3u+3t_0\right)du$.",
        "The delayed output is $" + S + r"y(t-t_0)=\int_{0}^{t-t_0}x(u)\cos(3u)\,du$. Since $" + S + r"y_1(t)\neq y(t-t_0)$ (different limits and an extra phase $" + S + r"3t_0$ in the cosine), the system is not time-invariant.",
        "Stability: take the bounded input $" + S + r"x(t)=\cos(3t)$. Then $" + S + r"y(t)=\int_{0}^{t}\cos^2(3\tau)\,d\tau=\tfrac{t}{2}+\tfrac{\sin 6t}{12}$, which grows without bound as $" + S + r"t\to\infty$. A bounded input gives an unbounded output, so the system is not stable.",
        "Hence the correct option is (4).",
        "",
        "Tip: A time-varying factor such as $" + S + r"\cos(3\tau)$ multiplying the input inside the integral already rules out time invariance, and an integrator is only BIBO-stable when the input cannot keep adding up: here the input that matches the cosine frequency adds up with the same sign forever.",
    ], "LTI Systems (LTI System Properties)"),
)

Q31 = dict(
    body=[
        "The Fourier transform of a signal $" + S + r"h(t)$ is $" + S + r"H(j\omega)=(2\cos\omega)(\sin 2\omega)/\omega$. The value of $" + S + r"h(0)$ is",
    ],
    options=[
        "$" + S + r"1/4$",
        "$" + S + r"1/2$",
        "$" + S + r"1$",
        "$" + S + r"2$",
    ],
    tail=tail("3", "2", "0.66", [
        "Given: $" + S + r"H(j\omega)=\tfrac{(2\cos\omega)(\sin 2\omega)}{\omega}$.",
        "Step 1: use $" + S + r"2\cos\omega\,\sin 2\omega=\sin 3\omega+\sin\omega$, so $" + S + r"H(j\omega)=\tfrac{\sin 3\omega}{\omega}+\tfrac{\sin\omega}{\omega}$.",
        "Step 2: a rectangular pulse $" + S + r"\tfrac{1}{2}\,\text{rect}$ of half-width $" + S + r"a$, i.e. $" + S + r"\tfrac{1}{2}$ for $" + S + r"|t|<a$ and $" + S + r"0$ otherwise, has the transform $" + S + r"\tfrac{\sin a\omega}{\omega}$.",
        "So $" + S + r"h(t)=\tfrac{1}{2}$ for $" + S + r"|t|<3$ plus $" + S + r"\tfrac{1}{2}$ for $" + S + r"|t|<1$.",
        "At $" + S + r"t=0$ both pulses are present: $" + S + r"h(0)=\tfrac{1}{2}+\tfrac{1}{2}=1$.",
        "Hence the correct option is (3).",
        "",
        "Tip: The value at $" + S + r"t=0$ can also be read from the area under the transform, $" + S + r"h(0)=\tfrac{1}{2\pi}\int H(j\omega)\,d\omega$; each term $" + S + r"\tfrac{\sin a\omega}{\omega}$ has area $" + S + r"\pi$, so each contributes $" + S + r"\tfrac{1}{2}$ here.",
    ], "Fourier Transform (Continuous Time Fourier Transform Calculation)"),
)

Q42 = dict(
    body=[
        "Let $" + S + r"y[n]$ denote the convolution of $" + S + r"h[n]$ and $" + S + r"g[n]$, where $" + S + r"h[n]=(1/2)^{n}u[n]$ and $" + S + r"g[n]$ is a causal sequence. If $" + S + r"y[0]=1$ and $" + S + r"y[1]=1/2$, then $" + S + r"g[1]$ equals",
    ],
    options=[
        "$" + S + r"0$",
        "$" + S + r"1/2$",
        "$" + S + r"1$",
        "$" + S + r"3/2$",
    ],
    tail=tail("1", "2", "0.66", [
        "Given: $" + S + r"y[n]=h[n]*g[n]=\sum_{k=0}^{n}h[k]\,g[n-k]$ because both $" + S + r"h[n]$ and $" + S + r"g[n]$ are causal, with $" + S + r"h[0]=1$ and $" + S + r"h[1]=\tfrac{1}{2}$.",
        "For $" + S + r"n=0$: $" + S + r"y[0]=h[0]\,g[0]=g[0]=1$.",
        "For $" + S + r"n=1$: $" + S + r"y[1]=h[0]\,g[1]+h[1]\,g[0]=g[1]+\tfrac{1}{2}\times 1$.",
        "Using $" + S + r"y[1]=\tfrac{1}{2}$: $" + S + r"g[1]+\tfrac{1}{2}=\tfrac{1}{2}$, so $" + S + r"g[1]=0$.",
        "Hence the correct option is (1).",
        "",
        "Tip: For causal sequences the convolution sum starts at $" + S + r"k=0$ and stops at $" + S + r"k=n$, so each new output sample brings in exactly one new unknown term of $" + S + r"g[n]$; here the extra term $" + S + r"h[1]g[0]=\tfrac{1}{2}$ already accounts for the whole of $" + S + r"y[1]$.",
    ], "LTI Systems (Discrete Convolution)"),
)
