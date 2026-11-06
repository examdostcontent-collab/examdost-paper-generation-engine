S = r"\scriptstyle "

Q22 = dict(
    body=[
        "If the scattering matrix $" + S + r"[S]$ of a two port network is",
        "$" + S + r"[S]=\begin{bmatrix}0.2\angle 0^{\circ} & 0.9\angle 90^{\circ}\ 0.9\angle 90^{\circ} & 0.1\angle 90^{\circ}\end{bmatrix}$",
        "then the network is",
    ],
    options=[
        "lossless and reciprocal",
        "lossless but not reciprocal",
        "not lossless but reciprocal",
        "neither lossless nor reciprocal",
    ],
    tail=[
        ("Correct", ["3"]),
        ("Explanation", [
            "Given: $" + S + r"S_{11}=0.2\angle 0^{\circ},\ S_{12}=0.9\angle 90^{\circ},\ S_{21}=0.9\angle 90^{\circ},\ S_{22}=0.1\angle 90^{\circ}$.",
            "Reciprocity test: a reciprocal network has a symmetric scattering matrix, $" + S + r"S_{12}=S_{21}$. Here both equal $" + S + r"0.9\angle 90^{\circ}$, so the network is reciprocal.",
            "Lossless test: a lossless network has a unitary scattering matrix, so the squared magnitudes in each column must add to $" + S + r"1$. First column: $" + S + r"|S_{11}|^2+|S_{21}|^2=0.2^2+0.9^2=0.04+0.81=0.85$.",
            "This is not equal to $" + S + r"1$, so the matrix is not unitary and the network is not lossless.",
            "Hence the correct option is (3).",
            "",
            "Tip: Reciprocity only needs the off-diagonal terms to match, while losslessness needs every column to have unit total power $" + S + r"\sum_i |S_{ij}|^2=1$ and different columns to be orthogonal; here the deficit $" + S + r"1-0.85=0.15$ is the fraction of power absorbed inside the network.",
        ]),
        ("Subject", ["Network Analysis"]),
        ("Topic", ["Two Port Network (Two Port Network)"]),
        ("Correct Marks", ["1"]),
        ("Incorrect Marks", ["0.33"]),
        ("Hint", ["-"]),
        ("Video Solution", ["-"]),
        ("PYQ", ["GATE ECE 2010"]),
        ("OTS ID", [""]),
    ],
)
