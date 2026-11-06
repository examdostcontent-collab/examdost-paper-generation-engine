S = r"\scriptstyle "


def m(x):
    return "$" + S + x + "$"


def tail(correct, marks, neg, subject, topic, explanation, with_hint=True):
    rows = [("Correct", [correct]), ("Explanation", explanation), ("Subject", [subject]), ("Topic", [topic]),
            ("Correct Marks", [marks]), ("Incorrect Marks", [neg])]
    if with_hint:
        rows += [("Hint", ["-"]), ("Video Solution", ["-"])]
    rows += [("PYQ", ["GATE ECE 1993"]), ("OTS ID", [""])]
    return rows


Q14 = dict(
    type="MSQ",
    body=["Which of the following is (are) valid FORTRAN 77 statement(s)?"],
    options=["DO 131 = 1", "A = DIM *** 7", "READ = 15.0", "GOTO 3 = 10"],
    tail=tail("1,3,4", "1", "0", "Digital Electronics", "Computer Organisation (Computer Organisation)", [
        "Concept: in FORTRAN 77 blanks are not significant and there are no reserved words, so a statement is classified by its form. A statement with an equals sign and no comma after it is an assignment to a variable, whatever the name looks like.",
        "Statement (1): $" + S + r"\text{DO 131 = 1}$ has no comma after the equals sign, so it is not a DO loop. It is the assignment of $" + S + r"1$ to the variable named $" + S + r"\text{DO131}$, which is valid.",
        "Statement (3): $" + S + r"\text{READ = 15.0}$ assigns $" + S + r"15.0$ to a variable named $" + S + r"\text{READ}$, which is valid because READ is not reserved.",
        "Statement (4): $" + S + r"\text{GOTO 3 = 10}$ becomes $" + S + r"\text{GOTO3 = 10}$ after ignoring blanks, an assignment to a variable named $" + S + r"\text{GOTO3}$, which is valid.",
        "Hence options (1), (3) and (4) are correct.",
        "",
        "Tip: Remove the blanks and look for the shape of the statement; a DO loop needs a comma after the equals sign, as in $" + S + r"\text{DO 131 I = 1, 10}$, and without it the line is just an assignment. The string $" + S + r"\text{***}$ in the second statement is not a valid operator.",
    ]),
)

Q25 = dict(
    type="NAT",
    body=[
        "For $" + S + r"X=4.0$, the value of $" + S + r"I$ in the FORTRAN 77 statement $" + S + r"I=-2**2+5.0*X/X*3+3/4$ is ________",
    ],
    options=[],
    tail=tail("11", "1", "0", "Digital Electronics", "Computer Organisation (Computer Organisation)", [
        "Given: $" + S + r"X=4.0$ (real) and the statement $" + S + r"I=-2**2+5.0*X/X*3+3/4$. The variable $" + S + r"I$ starts with the letter I, so by FORTRAN's implicit typing it is an integer and the result is truncated to an integer on assignment.",
        "Exponentiation has the highest priority, then unary minus: $" + S + r"-2**2=-(2^2)=-4$.",
        "Multiplication and division go left to right: $" + S + r"5.0*X=20.0$; $" + S + r"20.0/X=5.0$; $" + S + r"5.0*3=15.0$.",
        "$" + S + r"3/4$ is an integer division in FORTRAN, so it equals $" + S + r"0$.",
        "Sum: $" + S + r"-4+15.0+0=11.0$, which is stored in the integer $" + S + r"I$ as $" + S + r"11$.",
        "Hence $" + S + r"I=11$.",
        "",
        "Tip: Two FORTRAN rules decide this answer: the exponent binds tighter than the unary minus, so $" + S + r"-2**2$ is $" + S + r"-4$ and not $" + S + r"4$; and an integer division such as $" + S + r"3/4$ gives $" + S + r"0$, not $" + S + r"0.75$.",
    ], with_hint=False),
)

Q27 = dict(
    body=[
        "If $" + S + r"A=\begin{bmatrix}1 & 0 & 0 & 1\\0 & -1 & 0 & -1\\0 & 0 & i & i\\0 & 0 & 0 & -i\end{bmatrix}$, the matrix $" + S + r"A^4$, calculated by the use of Cayley-Hamilton theorem or otherwise, is",
    ],
    options=[
        "the $" + S + r"4\times 4$ identity matrix",
        "the $" + S + r"4\times 4$ null matrix",
        "the matrix $" + S + r"A$ itself",
        "the matrix $" + S + r"-I_4$",
    ],
    tail=tail("1", "1", "0.33", "Engineering Mathematics", "Linear Algebra (Eigen Values and Eigen Vectors)", [
        "Given: $" + S + r"A$ is upper triangular, so its eigenvalues are its diagonal entries $" + S + r"1,\ -1,\ i,\ -i$.",
        "Characteristic equation: $" + S + r"(\lambda-1)(\lambda+1)(\lambda-i)(\lambda+i)=(\lambda^2-1)(\lambda^2+1)=\lambda^4-1=0$.",
        "By the Cayley-Hamilton theorem every matrix satisfies its own characteristic equation, so $" + S + r"A^4-I=0$, that is $" + S + r"A^4=I$.",
        "So $" + S + r"A^4$ is the $" + S + r"4\times 4$ identity matrix.",
        "Hence the correct option is (1).",
        "",
        "Tip: The four diagonal entries are the four fourth roots of unity, so $" + S + r"\lambda^4=1$ for each eigenvalue; because they are distinct the matrix satisfies $" + S + r"\lambda^4-1=0$ exactly, without needing to multiply out $" + S + r"A^4$.",
    ]),
)

Q44 = dict(
    body=["While starting a dc shunt motor:"],
    options=[
        "reduced armature voltage $" + S + r"V_a$ and reduced field voltage $" + S + r"V_f$ should be applied and full regulator resistance $" + S + r"R_r$ should be included in the field circuit.",
        "reduced $" + S + r"V_a$ but full $" + S + r"V_f$ should be applied and $" + S + r"R_r$ should be zero.",
        "rated $" + S + r"V_a$ and rated $" + S + r"V_f$ should be applied and $" + S + r"R_r$ should be zero.",
        "rated $" + S + r"V_a$ and rated $" + S + r"V_f$ should be applied and $" + S + r"R_r$ should be maximum.",
    ],
    tail=tail("2", "1", "0.33", "Electrical Machines", "DC Machines (Starting, Braking and Testing of DC Motor)", [
        "Concept: at start the back emf is zero, so the armature current would be $" + S + r"\tfrac{V_a}{R_a}$, many times the rated value. The armature voltage must therefore be reduced (by a starter resistance) to limit the current.",
        "The torque is $" + S + r"T\propto\phi\,I_a$. To get the largest starting torque for the permitted current the flux must be maximum, so the full field voltage $" + S + r"V_f$ is applied and the field regulator resistance $" + S + r"R_r$ is kept at zero.",
        "So the correct procedure is a reduced $" + S + r"V_a$ with full $" + S + r"V_f$ and $" + S + r"R_r=0$.",
        "Hence the correct option is (2).",
        "",
        "Tip: Remember the two opposite rules for a shunt motor: armature side weak (to limit the current) and field side strong (to get the torque); the field regulator is set to zero resistance at start and is increased later only to raise the speed.",
    ]),
)

Q45 = dict(
    body=[
        "A $" + S + r"6$ pole $" + S + r"3$ phase wound-rotor induction machine is driven by another machine at $" + S + r"1800\ \text{rpm}$. The rotor of the induction machine is connected to a $" + S + r"50\ \text{Hz}$ system. If the mechanical rotation of the rotor is in the same direction as the rotor winding flux rotation, then the frequency of the stator voltage will be",
    ],
    options=[m(r"50\ \text{Hz}"), m(r"140\ \text{Hz}"), m(r"150\ \text{Hz}"), m(r"200\ \text{Hz}")],
    tail=tail("2", "1", "0.33", "Electrical Machines", "Induction Machines (Construction and Rotating Magnetic Field)", [
        "Given: $" + S + r"P=6$ poles, rotor driven at $" + S + r"N_r=1800\ \text{rpm}$, rotor winding supplied at $" + S + r"f_r=50\ \text{Hz}$, mechanical rotation in the same direction as the rotor flux rotation.",
        "Speed of the rotor flux relative to the rotor: $" + S + r"N_f=\tfrac{120f_r}{P}=\tfrac{120\times 50}{6}=1000\ \text{rpm}$.",
        "Speed of the rotor flux in space (relative to the stator) is the sum of the two speeds, because they are in the same direction: $" + S + r"N=1000+1800=2800\ \text{rpm}$.",
        "The stator voltage frequency is $" + S + r"f_s=\tfrac{P\,N}{120}=\tfrac{6\times 2800}{120}=140\ \text{Hz}$.",
        "Hence the correct option is (2).",
        "",
        "Tip: Add the electrical frequency of the rotor supply to the frequency produced by the mechanical rotation: $" + S + r"f_s=f_r+\tfrac{P\,N_r}{120}=50+90=140\ \text{Hz}$; if the rotation were opposite to the rotor flux rotation, the two would subtract instead.",
    ]),
)

ALL = [Q14, Q25, Q27, Q44, Q45]
