S = r"\scriptstyle "


def tail(correct, subject, topic, explanation):
    return [
        ("Correct", [correct]),
        ("Explanation", explanation),
        ("Subject", [subject]),
        ("Topic", [topic]),
        ("Correct Marks", ["2"]),
        ("Incorrect Marks", ["0"]),
        ("Hint", ["-"]),
        ("Video Solution", ["-"]),
        ("PYQ", ["GATE ECE 2002"]),
        ("OTS ID", [""]),
    ]


Q18 = dict(
    type="MSQ",
    body=[
        "A continuous time signal with finite energy, band limited from $" + S + r"3\ \text{MHz}$ to $" + S + r"5\ \text{MHz}$ is ideally sampled, encoded by a fixed length PCM coder and then transmitted over a digital channel of capacity $" + S + r"7\ \text{Mbps}$. The probability density function (pdf) at the output of the sampler is uniform over the range $" + S + r"-2\ \text{V}$ to $" + S + r"+2\ \text{V}$.",
        "Which of the following statements are correct?",
    ],
    options=[
        "The minimum sampling rate necessary for perfect reconstruction is $" + S + r"5\ \text{MHz}$",
        "The number of PCM bits per sample that the channel can carry is $" + S + r"1$",
        "The maximum SNR that may be achieved is about $" + S + r"6\ \text{dB}$",
        "The minimum sampling rate necessary for perfect reconstruction is $" + S + r"10\ \text{MHz}$",
    ],
    tail=tail("1,2,3", "Communication Systems",
              "Digital Communication (Baseband Digital Pulse Modulation methods-PCM, DPCM, DM)", [
        "Given: $" + S + r"f_L=3\ \text{MHz}$, $" + S + r"f_H=5\ \text{MHz}$, bandwidth $" + S + r"B=f_H-f_L=2\ \text{MHz}$, channel capacity $" + S + r"7\ \text{Mbps}$, signal pdf uniform over $" + S + r"-2\ \text{V}$ to $" + S + r"+2\ \text{V}$.",
        "Step 1 (minimum sampling rate): this is a band-pass signal, so band-pass sampling applies. $" + S + r"\tfrac{f_H}{B}=\tfrac{5}{2}=2.5$, so the integer part is $" + S + r"k=2$.",
        "$" + S + r"f_{s,min}=\tfrac{2f_H}{k}=\tfrac{2\times 5}{2}=5\ \text{MHz}$. This is allowed because for $" + S + r"k=2$ the valid range is $" + S + r"5\ \text{MHz}\leq f_s\leq 6\ \text{MHz}$.",
        "Step 2 (bits per sample): at the minimum rate the channel can carry $" + S + r"\tfrac{7\ \text{Mbps}}{5\ \text{Msamples/s}}=1.4$ bits per sample. A fixed-length coder needs a whole number of bits, so $" + S + r"n=1$ bit per sample.",
        "Step 3 (maximum SNR): the signal is uniform over $" + S + r"[-2,2]$, so its power is $" + S + r"\tfrac{4^2}{12}=\tfrac{4}{3}\ \text{V}^2$. With $" + S + r"L=2^n$ uniform levels the step is $" + S + r"\Delta=\tfrac{4}{L}$ and the quantization noise power is $" + S + r"\tfrac{\Delta^2}{12}=\tfrac{16}{12L^2}$.",
        "So $" + S + r"\text{SNR}=L^2=2^{2n}$, i.e. $" + S + r"20\log_{10}2^n=6.02\,n\ \text{dB}$. For $" + S + r"n=1$: $" + S + r"\text{SNR}\approx 6\ \text{dB}$.",
        "Hence options (1), (2) and (3) are correct.",
        "",
        "Tip: Sampling at the lowest valid band-pass rate leaves the most channel capacity for bits, and every extra bit per sample is worth about $" + S + r"6\ \text{dB}$; here $" + S + r"7/5=1.4$ only allows $" + S + r"1$ whole bit, so the fractional $" + S + r"0.4$ bit is wasted.",
    ]),
)

Q20 = dict(
    type="MSQ",
    body=[
        "Transmission line transformation of a load $" + S + r"Z_L$ and $" + S + r"Z$ is given by",
        "$" + S + r"Z=Z_0\,\tfrac{Z_L+jZ_0\tan\beta l}{Z_0+jZ_L\tan\beta l}$",
        "Which of the following statements about this transformation are correct?",
    ],
    options=[
        "For real $" + S + r"Z_0$, the same line transforms $" + S + r"Z^{*}$ into $" + S + r"Z_L^{*}$",
        "Conjugate matching at one end of a lossless line implies conjugate matching at the other end, as seen through the line",
        "The result holds only when $" + S + r"Z_0$ is complex",
        "The line transforms $" + S + r"Z_L$ into $" + S + r"Z_L^{*}$ for every length $" + S + r"l$",
    ],
    tail=tail("1,2", "EMFT - ECE", "Transmission Lines (Wave Characteristics on Finite Transmission Lines)", [
        "Given: $" + S + r"Z=Z_0\tfrac{Z_L+jZ_0 t}{Z_0+jZ_L t}$ with $" + S + r"t=\tan\beta l$, and $" + S + r"Z_0$ real, so $" + S + r"t$ and $" + S + r"Z_0$ are both real.",
        "Step 1: solve for $" + S + r"Z_L$. From $" + S + r"Z(Z_0+jZ_Lt)=Z_0(Z_L+jZ_0t)$ we get $" + S + r"Z_L=Z_0\tfrac{Z-jZ_0t}{Z_0-jZt}$.",
        "Step 2: take the complex conjugate. Because $" + S + r"Z_0$ and $" + S + r"t$ are real, $" + S + r"Z_L^{*}=Z_0\tfrac{Z^{*}+jZ_0t}{Z_0+jZ^{*}t}$.",
        "Step 3: compare with the original transformation, which turns a load $" + S + r"Z_L$ into $" + S + r"Z_0\tfrac{Z_L+jZ_0t}{Z_0+jZ_Lt}$. Putting the load as $" + S + r"Z^{*}$ in it gives exactly the expression for $" + S + r"Z_L^{*}$, so the same line transforms $" + S + r"Z^{*}$ into $" + S + r"Z_L^{*}$. Statement (1) is correct.",
        "Importance: let the source impedance be $" + S + r"Z_g=Z^{*}$, the conjugate-matched value at the input of the line. Looking back from the load through the same line, the source appears as the transformed $" + S + r"Z^{*}$, which is $" + S + r"Z_L^{*}$. So the load is also conjugate-matched to what it sees. Conjugate matching (maximum power transfer) is therefore preserved along a lossless line. Statement (2) is correct.",
        "Statement (3) is false: the step $" + S + r"Z_0^{*}=Z_0$ used in the conjugation needs a real $" + S + r"Z_0$, and for a complex $" + S + r"Z_0$ the conjugate of the transformation has $" + S + r"Z_0^{*}$ in it and the result no longer follows.",
        "Statement (4) is false: the result maps $" + S + r"Z^{*}$ (not $" + S + r"Z_L$) into $" + S + r"Z_L^{*}$; the load $" + S + r"Z_L$ itself is transformed into the input impedance $" + S + r"Z$, which changes with $" + S + r"l$ and equals $" + S + r"Z_L^{*}$ only in special cases.",
        "Hence options (1) and (2) are correct.",
        "",
        "Tip: The trick is to conjugate the inverse relation $" + S + r"Z_L=Z_0\tfrac{Z-jZ_0t}{Z_0-jZt}$; since $" + S + r"jt$ changes sign on conjugation, the inverse (length $" + S + r"-l$) form turns into the forward (length $" + S + r"+l$) form acting on the conjugates.",
    ]),
)
