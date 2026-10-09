S = r"\scriptstyle "


def tail(correct, subject, topic, explanation):
    return [
        ("Correct", [correct]),
        ("Explanation", explanation),
        ("Subject", [subject]),
        ("Topic", [topic]),
        ("Correct Marks", ["2"]),
        ("Incorrect Marks", ["0.66"]),
        ("Hint", ["-"]),
        ("Video Solution", ["-"]),
        ("PYQ", ["GATE ECE 2007"]),
        ("OTS ID", [""]),
    ]


def vec(a, b):
    return r"\begin{bmatrix}" + a + r"\\" + b + r"\end{bmatrix}"


def pair(lam, a, b):
    return r"\left(" + lam + r",\ " + vec(a, b) + r"\right)"


statement_8085 = [
    "Statement for linked questions: an 8085 assembly language program is given below.",
    "Line 1: MVI A,B5H",
    "Line 2: MVI B,0EH",
    "Line 3: XRI 69H",
    "Line 4: ADD B",
    "Line 5: ANI 9BH",
    "Line 6: CPI 9FH",
    "Line 7: STA 3010H",
    "Line 8: HLT",
]

Q79 = dict(
    body=statement_8085 + [
        "After execution of line 7 of the program, the status of the CY and Z flags will be",
    ],
    options=[
        "$" + S + r"\text{CY}=0,\ \text{Z}=0$",
        "$" + S + r"\text{CY}=0,\ \text{Z}=1$",
        "$" + S + r"\text{CY}=1,\ \text{Z}=0$",
        "$" + S + r"\text{CY}=1,\ \text{Z}=1$",
    ],
    tail=tail("3", "Digital Electronics", "Microprocessor (Microprocessor)", [
        "Given: the program above; the flags are asked after line 7.",
        "Line 1-2: $" + S + r"A=\text{B5H}$ and $" + S + r"B=\text{0EH}$.",
        "Line 3 (XRI 69H): $" + S + r"A=\text{B5H}\oplus\text{69H}=1011\,0101\oplus 0110\,1001=1101\,1100=\text{DCH}$. XRI clears the carry, so $" + S + r"\text{CY}=0$.",
        "Line 4 (ADD B): $" + S + r"A=\text{DCH}+\text{0EH}=\text{EAH}$, with no carry out, so $" + S + r"\text{CY}=0$.",
        "Line 5 (ANI 9BH): $" + S + r"A=\text{EAH}\cdot\text{9BH}=1110\,1010\cdot 1001\,1011=1000\,1010=\text{8AH}$, and ANI clears the carry again.",
        "Line 6 (CPI 9FH): the comparison does $" + S + r"\text{8AH}-\text{9FH}$ without changing A. Since $" + S + r"\text{8AH}<\text{9FH}$, a borrow occurs and $" + S + r"\text{CY}=1$; the two values are not equal, so $" + S + r"\text{Z}=0$.",
        "Line 7 (STA 3010H) only stores A in memory and does not change any flag, so after line 7: $" + S + r"\text{CY}=1,\ \text{Z}=0$.",
        "Hence the correct option is (3).",
        "",
        "Tip: Track the flags instruction by instruction and let only the last flag-setting instruction decide, which here is CPI at line 6: it sets CY when the accumulator is smaller than the immediate byte and Z when they are equal, while the STA at line 7 leaves the flags exactly as CPI left them.",
    ]),
)

statement_lin = [
    "Statement for linked questions: consider a linear system whose state space representation is $" + S + r"\dot{\mathbf{x}}(t)=\mathbf{A}\mathbf{x}(t)$. "
    "If the initial state vector of the system is $" + S + r"\mathbf{x}(0)=" + vec("1", "-2") + r"$, then the system response is $" + S + r"\mathbf{x}(t)=" + vec("e^{-2t}", "-2e^{-2t}") + r"$.",
    "If the initial state vector of the system changes to $" + S + r"\mathbf{x}(0)=" + vec("1", "-1") + r"$, then the system response becomes $" + S + r"\mathbf{x}(t)=" + vec("e^{-t}", "-e^{-t}") + r"$.",
]

Q80 = dict(
    body=statement_lin + [
        "The eigenvalue and eigenvector pairs $" + S + r"(\lambda_i,\ v_i)$ for the system are",
    ],
    options=[
        "$" + S + pair("-1", "1", "-1") + r"\ \text{and}\ " + pair("-2", "1", "-2") + "$",
        "$" + S + pair("-2", "1", "-1") + r"\ \text{and}\ " + pair("-1", "1", "-2") + "$",
        "$" + S + pair("-1", "1", "-1") + r"\ \text{and}\ " + pair("2", "1", "-2") + "$",
        "$" + S + pair("-2", "1", "-1") + r"\ \text{and}\ " + pair("1", "1", "-2") + "$",
    ],
    tail=tail("1", "Control Systems", "State Variable Analysis (State Model Analysis)", [
        "Given: $" + S + r"\dot{\mathbf{x}}=\mathbf{A}\mathbf{x}$ with two initial states and their responses.",
        "Concept: if the initial state is an eigenvector $" + S + r"v$ of $" + S + r"\mathbf{A}$ with eigenvalue $" + S + r"\lambda$, the response stays along $" + S + r"v$ and is $" + S + r"\mathbf{x}(t)=e^{\lambda t}v$.",
        "Case 1: $" + S + r"\mathbf{x}(0)=" + vec("1", "-2") + r"$ gives $" + S + r"\mathbf{x}(t)=e^{-2t}" + vec("1", "-2") + r"$, so $" + S + r"\lambda_1=-2$ with $" + S + r"v_1=" + vec("1", "-2") + r"$.",
        "Case 2: $" + S + r"\mathbf{x}(0)=" + vec("1", "-1") + r"$ gives $" + S + r"\mathbf{x}(t)=e^{-t}" + vec("1", "-1") + r"$, so $" + S + r"\lambda_2=-1$ with $" + S + r"v_2=" + vec("1", "-1") + r"$.",
        "So the pairs are $" + S + pair("-1", "1", "-1") + r"$ and $" + S + pair("-2", "1", "-2") + r"$.",
        "Hence the correct option is (1).",
        "",
        "Tip: Whenever a response keeps the direction of its initial state and only shrinks by one exponential, read the eigenvalue straight from the exponent and the eigenvector from the initial state; no characteristic equation is needed.",
    ]),
)

Q81 = dict(
    body=statement_lin + [
        "The system matrix $" + S + r"\mathbf{A}$ is",
    ],
    options=[
        "$" + S + r"\begin{bmatrix}0 & 1\\-1 & 1\end{bmatrix}$",
        "$" + S + r"\begin{bmatrix}1 & 1\\-1 & -2\end{bmatrix}$",
        "$" + S + r"\begin{bmatrix}2 & 1\\-1 & -1\end{bmatrix}$",
        "$" + S + r"\begin{bmatrix}0 & 1\\-2 & -3\end{bmatrix}$",
    ],
    tail=tail("4", "Control Systems", "State Variable Analysis (State Model Analysis)", [
        "Given: from the linked data, $" + S + r"\lambda_1=-1,\ v_1=" + vec("1", "-1") + r"$ and $" + S + r"\lambda_2=-2,\ v_2=" + vec("1", "-2") + r"$.",
        "Let $" + S + r"\mathbf{A}=\begin{bmatrix}a & b\\c & d\end{bmatrix}$ and use $" + S + r"\mathbf{A}v_i=\lambda_i v_i$.",
        "From $" + S + r"\mathbf{A}v_1=-v_1$: $" + S + r"a-b=-1$ and $" + S + r"c-d=1$.",
        "From $" + S + r"\mathbf{A}v_2=-2v_2$: $" + S + r"a-2b=-2$ and $" + S + r"c-2d=4$.",
        "Subtracting the first pair of equations from the second: $" + S + r"b=1$, so $" + S + r"a=0$; and $" + S + r"d=-3$, so $" + S + r"c=-2$.",
        "So $" + S + r"\mathbf{A}=\begin{bmatrix}0 & 1\\-2 & -3\end{bmatrix}$, whose characteristic equation $" + S + r"\lambda^2+3\lambda+2=0$ indeed gives $" + S + r"\lambda=-1,-2$.",
        "Hence the correct option is (4).",
        "",
        "Tip: Writing one equation per eigenpair, $" + S + r"\mathbf{A}v_i=\lambda_i v_i$, gives four linear equations for the four unknown entries, and the trace $" + S + r"-3$ and determinant $" + S + r"2$ of the result must equal the sum $" + S + r"-3$ and product $" + S + r"2$ of the eigenvalues.",
    ]),
)
