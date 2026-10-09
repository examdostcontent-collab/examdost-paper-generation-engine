S = r"\scriptstyle "


def m(x):
    return "$" + S + x + "$"


def tail(correct, marks, neg, subject, topic, explanation):
    return [
        ("Correct", [correct]),
        ("Explanation", explanation),
        ("Subject", [subject]),
        ("Topic", [topic]),
        ("Correct Marks", [marks]),
        ("Incorrect Marks", [neg]),
        ("Hint", ["-"]),
        ("Video Solution", ["-"]),
        ("PYQ", ["GATE ECE 1996"]),
        ("OTS ID", [""]),
    ]


Q14 = dict(
    body=[
        "A lossless transmission line having $" + S + r"50\ \Omega$ characteristic impedance and length $" + S + r"\tfrac{\lambda}{4}$ is short circuited at one end and connected to an ideal voltage source of $" + S + r"1\ \text{V}$ at the other end. The current drawn from the voltage source is",
    ],
    options=[m("0"), m(r"0.02\ \text{A}"), m(r"\infty"), "none of these"],
    tail=tail("1", "1", "0.33", "EMFT - ECE", "Transmission Lines (Wave Characteristics on Finite Transmission Lines)", [
        "Given: $" + S + r"Z_0=50\ \Omega$, length $" + S + r"l=\tfrac{\lambda}{4}$, load $" + S + r"Z_L=0$ (short circuit), source $" + S + r"1\ \text{V}$.",
        "A quarter-wave lossless line inverts the load impedance: $" + S + r"Z_{in}=\tfrac{Z_0^2}{Z_L}$.",
        "With $" + S + r"Z_L=0$: $" + S + r"Z_{in}=\tfrac{50^2}{0}\to\infty$, so the shorted quarter-wave line looks like an open circuit at the input.",
        "The current drawn from the source is $" + S + r"I=\tfrac{V}{Z_{in}}=\tfrac{1}{\infty}=0$.",
        "Hence the correct option is (1).",
        "",
        "Tip: A quarter-wave line turns a short into an open circuit (and an open into a short), which is why a shorted $" + S + r"\tfrac{\lambda}{4}$ stub is used as an insulator in a transmission-line support; the source sees no current even though the far end is shorted.",
    ]),
)

Q214 = dict(
    body=[
        "The following sequence of instructions are executed by an 8085 microprocessor:",
        "1000 LXI SP,27FF",
        "1003 CALL 1006",
        "1006 POP H",
        "The contents of the stack pointer (SP) and the HL register pair on completion of execution of these instructions are",
    ],
    options=[
        m(r"\text{SP}=\text{27FF},\ \text{HL}=\text{1003}"),
        m(r"\text{SP}=\text{27FD},\ \text{HL}=\text{1003}"),
        m(r"\text{SP}=\text{27FF},\ \text{HL}=\text{1006}"),
        m(r"\text{SP}=\text{27FD},\ \text{HL}=\text{1006}"),
    ],
    tail=tail("3", "2", "0.66", "Digital Electronics", "Microprocessor (Microprocessor)", [
        "Given: the three-instruction sequence above.",
        "LXI SP,27FF: loads the stack pointer, so $" + S + r"\text{SP}=\text{27FF}$. This instruction occupies 3 bytes (1000 to 1002), so the next instruction starts at 1003.",
        "CALL 1006 (3 bytes, at 1003 to 1005): the return address is the address of the next instruction, $" + S + r"\text{1006}$. CALL pushes it on the stack: the high byte $" + S + r"\text{10}$ goes to address 27FE and the low byte $" + S + r"\text{06}$ to address 27FD, so $" + S + r"\text{SP}=\text{27FD}$, and the program counter is loaded with 1006.",
        "POP H (at 1006): pops the top two bytes into the register pair: $" + S + r"L=\text{06}$ (from 27FD) and $" + S + r"H=\text{10}$ (from 27FE), so $" + S + r"\text{HL}=\text{1006}$, and SP increases by 2 back to $" + S + r"\text{27FF}$.",
        "So $" + S + r"\text{SP}=\text{27FF}$ and $" + S + r"\text{HL}=\text{1006}$.",
        "Hence the correct option is (3).",
        "",
        "Tip: CALL pushes the address of the instruction that follows it (not the call target), and here the call target and that next instruction are both 1006, so POP H reads back exactly 1006 and SP returns to its starting value.",
    ]),
)
ALL = [Q14, Q214]
