import os

S = r"\scriptstyle "
BASE = os.path.dirname(os.path.abspath(__file__))


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
        ("PYQ", ["GATE ECE 2001"]),
        ("OTS ID", [""]),
    ]


def m(x):
    return "$" + S + x + "$"


# ---------------------------------------------------------------- 1-mark MCQs
Q122 = dict(
    body=["A transmission line is distortion-less if"],
    options=[m(r"RL=\tfrac{1}{GC}"), m(r"RL=GC"), m(r"LG=RC"), m(r"RG=LC")],
    tail=tail("3", "1", "0.33", "EMFT - ECE", "Transmission Lines (General Transmission Line Equations)", [
        "Concept: a line is distortion-less when the attenuation constant is frequency independent and the phase constant is linear in frequency, which happens when the series and shunt branches have the same time constant.",
        "Condition (Heaviside): $" + S + r"\tfrac{R}{L}=\tfrac{G}{C}$.",
        "Cross-multiplying gives $" + S + r"RC=LG$.",
        "Hence the correct option is (3).",
        "",
        "Tip: Match the time constants of the two branches: the ratio $" + S + r"\tfrac{R}{L}$ (series branch) must equal $" + S + r"\tfrac{G}{C}$ (shunt branch); writing it as $" + S + r"RC=LG$ pairs each resistive element with the opposite reactive element.",
    ]),
)

Q123 = dict(
    body=[
        "If a plane electromagnetic wave satisfies the equation $" + S + r"\tfrac{\partial^2 E_x}{\partial z^2}=\tfrac{1}{c^2}\tfrac{\partial^2 E_x}{\partial t^2}$, the wave propagates in the",
    ],
    options=["x-direction", "z-direction", "y-direction", "xy plane at an angle of $" + S + r"45^{\circ}$ between the x and z directions"],
    tail=tail("2", "1", "0.33", "EMFT - ECE", "Plane Waves (Plane Waves in Loseless Media)", [
        "Concept: the one-dimensional wave equation $" + S + r"\tfrac{\partial^2 E}{\partial s^2}=\tfrac{1}{c^2}\tfrac{\partial^2 E}{\partial t^2}$ describes a wave travelling along the coordinate $" + S + r"s$ that appears in the space derivative, at speed $" + S + r"c$.",
        "Here the space derivative is with respect to $" + S + r"z$ and the field component is $" + S + r"E_x$, so the field varies only along $" + S + r"z$ and is perpendicular to it, as required for a transverse plane wave.",
        "So the wave travels along the z-direction.",
        "Hence the correct option is (2).",
        "",
        "Tip: Read the propagation direction from the variable in the space derivative, and the polarization from the subscript on $" + S + r"E$; for a plane wave these two must be perpendicular, which is exactly the case with $" + S + r"E_x$ travelling along $" + S + r"z$.",
    ]),
)

Q124 = dict(
    body=["The phase velocity of waves propagating in a hollow metal waveguide is"],
    options=[
        "greater than the velocity of light in free space.",
        "less than the velocity of light in free space.",
        "equal to the velocity of light in free space.",
        "equal to the group velocity.",
    ],
    tail=tail("1", "1", "0.33", "EMFT - ECE", "Waveguides (Rectangular Waveguides)", [
        "Concept: for a mode above cut-off in a hollow waveguide, the phase constant is $" + S + r"\beta=\tfrac{\omega}{c}\sqrt{1-\left(\tfrac{f_c}{f}\right)^2}$, which is smaller than the free-space value $" + S + r"\tfrac{\omega}{c}$.",
        "Phase velocity: $" + S + r"v_p=\tfrac{\omega}{\beta}=\tfrac{c}{\sqrt{1-(f_c/f)^2}}$. Since the square root is less than $" + S + r"1$, $" + S + r"v_p>c$.",
        "Hence the correct option is (1).",
        "",
        "Tip: The phase velocity can exceed $" + S + r"c$ because it describes the motion of a constant-phase point, not of energy; the group velocity $" + S + r"v_g=\tfrac{c^2}{v_p}=c\sqrt{1-(f_c/f)^2}$ is the one that stays below $" + S + r"c$, and $" + S + r"v_p\,v_g=c^2$.",
    ]),
)

Q125 = dict(
    body=["The dominant mode in a rectangular waveguide is $" + S + r"\text{TE}_{10}$, because this mode has"],
    options=["no attenuation", "no cut-off", "no magnetic field component", "the highest cut-off wavelength"],
    tail=tail("4", "1", "0.33", "EMFT - ECE", "Waveguides (Rectangular Waveguides)", [
        "Concept: the dominant mode is the mode with the lowest cut-off frequency, which is the same as the highest cut-off wavelength.",
        "For a rectangular guide with $" + S + r"a>b$: $" + S + r"\lambda_c=\tfrac{2}{\sqrt{(m/a)^2+(n/b)^2}}$. For $" + S + r"\text{TE}_{10}$: $" + S + r"\lambda_c=2a$, which is the largest value among all modes.",
        "Hence the correct option is (4).",
        "",
        "Tip: In a hollow guide no mode is free of cut-off or attenuation (below cut-off every mode decays); the special thing about $" + S + r"\text{TE}_{10}$ is only that its cut-off $" + S + r"\lambda_c=2a$ is the longest, so it is the first to propagate as frequency rises.",
    ]),
)

# ---------------------------------------------------------------- 2-mark MCQs
Q222 = dict(
    body=[
        "A material has conductivity of $" + S + r"10^{-2}\ \text{mho/m}$ and a relative permittivity of $" + S + r"4$. The frequency at which the conduction current in the medium is equal to the displacement current is",
    ],
    options=[m(r"45\ \text{MHz}"), m(r"90\ \text{MHz}"), m(r"450\ \text{MHz}"), m(r"900\ \text{MHz}")],
    tail=tail("1", "2", "0.66", "EMFT - ECE", "Plane Waves (Plane Waves in Lossy Media)", [
        "Given: $" + S + r"\sigma=10^{-2}\ \text{mho/m}$, $" + S + r"\varepsilon_r=4$, $" + S + r"\varepsilon_0=8.854\times 10^{-12}\ \text{F/m}$.",
        "Concept: conduction current density is $" + S + r"\sigma E$ and displacement current density has magnitude $" + S + r"\omega\varepsilon E$; they are equal when $" + S + r"\sigma=\omega\varepsilon$ (loss tangent equal to 1).",
        "$" + S + r"f=\tfrac{\sigma}{2\pi\varepsilon_0\varepsilon_r}=\tfrac{10^{-2}}{2\pi\times 8.854\times 10^{-12}\times 4}=\tfrac{10^{-2}}{2.225\times 10^{-10}}\approx 4.5\times 10^{7}\ \text{Hz}$.",
        "So $" + S + r"f\approx 45\ \text{MHz}$.",
        "Hence the correct option is (1).",
        "",
        "Tip: The ratio $" + S + r"\tfrac{\sigma}{\omega\varepsilon}$ is the loss tangent; the frequency where it equals $" + S + r"1$ is the boundary between a medium behaving mainly as a conductor (below it) and mainly as a dielectric (above it).",
    ]),
)

Q223 = dict(
    body=[
        "A uniform plane electromagnetic wave incident normally on a plane surface of a dielectric material is reflected with a VSWR of $" + S + r"3$. What is the percentage of incident power that is reflected?",
    ],
    options=[m(r"10\%"), m(r"25\%"), m(r"50\%"), m(r"75\%")],
    tail=tail("2", "2", "0.66", "EMFT - ECE", "Plane Waves (Normal and Oblique incidence of Plane Waves)", [
        "Given: $" + S + r"\text{VSWR}=3$.",
        "Concept: $" + S + r"\text{VSWR}=\tfrac{1+|\Gamma|}{1-|\Gamma|}$, so $" + S + r"|\Gamma|=\tfrac{\text{VSWR}-1}{\text{VSWR}+1}=\tfrac{3-1}{3+1}=0.5$.",
        "The reflected power fraction is $" + S + r"|\Gamma|^2=0.5^2=0.25$.",
        "So $" + S + r"25\%$ of the incident power is reflected.",
        "Hence the correct option is (2).",
        "",
        "Tip: Power depends on the square of the reflection coefficient, so a VSWR of $" + S + r"3$ (a reflection coefficient of $" + S + r"0.5$ in magnitude) reflects only a quarter of the power, and the remaining $" + S + r"75\%$ is transmitted.",
    ]),
)

Q224 = dict(
    body=[
        "A medium wave radio transmitter operating at a wavelength of $" + S + r"492\ \text{m}$ has a tower antenna of height $" + S + r"124\ \text{m}$. What is the radiation resistance of the antenna?",
    ],
    options=[m(r"25\ \Omega"), m(r"36.5\ \Omega"), m(r"50\ \Omega"), m(r"73\ \Omega")],
    tail=tail("2", "2", "0.66", "EMFT - ECE", "Antennas (Linear Antennas)", [
        "Given: $" + S + r"\lambda=492\ \text{m}$ and tower height $" + S + r"h=124\ \text{m}$.",
        "Step 1: $" + S + r"\tfrac{h}{\lambda}=\tfrac{124}{492}\approx 0.252\approx\tfrac{1}{4}$, so the tower is a quarter-wave vertical monopole over the ground.",
        "Step 2: a half-wave dipole has $" + S + r"R_{rad}\approx 73\ \Omega$. A monopole over a perfectly conducting ground radiates only into the upper half space, so its radiation resistance is half of that.",
        "$" + S + r"R_{rad}=\tfrac{73}{2}\approx 36.5\ \Omega$.",
        "Hence the correct option is (2).",
        "",
        "Tip: A tower of height about $" + S + r"\tfrac{\lambda}{4}$ above a ground plane behaves like half of a half-wave dipole (its image supplies the other half), so its radiation resistance is half of the dipole's $" + S + r"73\ \Omega$.",
    ]),
)

Q225 = dict(
    body=[
        "In a uniform linear array, four isotropic radiating elements are spaced $" + S + r"\tfrac{\lambda}{4}$ apart. The progressive phase shift between the elements required for forming the main beam at $" + S + r"60^{\circ}$ off the end-fire is:",
    ],
    options=[m(r"-\pi\ \text{radians}"), m(r"-\tfrac{\pi}{2}\ \text{radians}"), m(r"-\tfrac{\pi}{4}\ \text{radians}"), m(r"-\tfrac{\pi}{8}\ \text{radians}")],
    tail=tail("3", "2", "0.66", "EMFT - ECE", "Antennas (Antenna Arrays)", [
        "Given: element spacing $" + S + r"d=\tfrac{\lambda}{4}$, main beam at an angle of $" + S + r"\theta=60^{\circ}$ from the end-fire direction (the array axis).",
        "Concept: for a uniform linear array the total phase between adjacent elements is $" + S + r"\psi=\beta d\cos\theta+\alpha$, and the main beam points where $" + S + r"\psi=0$, so $" + S + r"\alpha=-\beta d\cos\theta$.",
        "$" + S + r"\beta d=\tfrac{2\pi}{\lambda}\times\tfrac{\lambda}{4}=\tfrac{\pi}{2}$ and $" + S + r"\cos 60^{\circ}=\tfrac{1}{2}$.",
        "$" + S + r"\alpha=-\tfrac{\pi}{2}\times\tfrac{1}{2}=-\tfrac{\pi}{4}\ \text{radians}$.",
        "Hence the correct option is (3).",
        "",
        "Tip: The angle is measured from the array axis (end-fire is $" + S + r"0^{\circ}$), so the $" + S + r"\cos\theta$ factor is $" + S + r"\cos 60^{\circ}=\tfrac{1}{2}$, not $" + S + r"\cos 30^{\circ}$ which would be used for an angle measured from broadside.",
    ]),
)

# ---------------------------------------------------------------- Section B, counted as 2 marks (MSQ)
Q19 = dict(
    type="MSQ",
    body=[
        "A periodic signal $" + S + r"g(t)$ is shown in the figure (pulse height $" + S + r"A$, pulse width $" + S + r"\pi$, period $" + S + r"2\pi$). Determine the PSD of $" + S + r"g(t)$.",
        "Which of the following statements are correct?",
    ],
    image=os.path.join(BASE, "GATE_ECE_2001_Q19", "q19_diagram.png"),
    image_w=4.2,
    options=[
        "The PSD consists of impulses at $" + S + r"f=\tfrac{n}{2\pi}\ \text{Hz}$ (multiples of the fundamental frequency)",
        "The impulse at $" + S + r"f=0$ has weight $" + S + r"\tfrac{A^2}{4}$",
        "The impulse at $" + S + r"f=\tfrac{n}{2\pi}$ has weight $" + S + r"\tfrac{A^2}{n^2\pi^2}$ for odd $" + S + r"n$, and the even harmonics $" + S + r"(n\neq 0)$ are absent",
        "The total power of $" + S + r"g(t)$ is $" + S + r"A^2$",
    ],
    tail=tail("1,2,3", "2", "0", "Signals and Systems", "Fourier Series (Continuous Time Fourier Series)", [
        "Given: pulse train of height $" + S + r"A$, pulse width $" + S + r"\tau=\pi$, period $" + S + r"T_0=2\pi$, centred at $" + S + r"t=0$. The fundamental is $" + S + r"\omega_0=\tfrac{2\pi}{T_0}=1\ \text{rad/s}$, i.e. $" + S + r"f_0=\tfrac{1}{2\pi}\ \text{Hz}$.",
        "Fourier coefficients: $" + S + r"c_n=\tfrac{1}{T_0}\int_{-\pi/2}^{\pi/2}A\,e^{-jnt}\,dt=\tfrac{A}{2\pi}\cdot\tfrac{2\sin(n\pi/2)}{n}=\tfrac{A\sin(n\pi/2)}{n\pi}$, and $" + S + r"c_0=\tfrac{A\pi}{2\pi}=\tfrac{A}{2}$.",
        "So $" + S + r"|c_0|^2=\tfrac{A^2}{4}$; for odd $" + S + r"n$, $" + S + r"|c_n|^2=\tfrac{A^2}{n^2\pi^2}$; for even $" + S + r"n\neq 0$, $" + S + r"c_n=0$.",
        "PSD of a periodic signal: $" + S + r"S_g(f)=\sum_{n}|c_n|^2\,\delta\!\left(f-\tfrac{n}{2\pi}\right)=\tfrac{A^2}{4}\delta(f)+\sum_{n\ \text{odd}}\tfrac{A^2}{n^2\pi^2}\delta\!\left(f-\tfrac{n}{2\pi}\right)$.",
        "Total power (check): $" + S + r"P=\tfrac{1}{T_0}\int|g(t)|^2dt=\tfrac{A^2\pi}{2\pi}=\tfrac{A^2}{2}$.",
        "Hence options (1), (2) and (3) are correct.",
        "",
        "Tip: For a periodic signal the PSD is a line spectrum whose weights are $" + S + r"|c_n|^2$; a pulse width of exactly half the period makes every even harmonic vanish because $" + S + r"\sin(n\pi/2)=0$ for even $" + S + r"n$.",
    ]),
)

Q20 = dict(
    type="MSQ",
    body=[
        "A system of three electric charges lying in a straight line is in equilibrium. Two of the charges are positive with magnitudes $" + S + r"Q$ and $" + S + r"2Q$, and are $" + S + r"50\ \text{cm}$ apart. Determine the sign, magnitude and position of the third charge.",
        "Which of the following statements are correct?",
    ],
    options=[
        "The third charge is negative",
        "It lies between the two charges, about $" + S + r"20.7\ \text{cm}$ from the charge $" + S + r"Q$",
        "Its magnitude is about $" + S + r"0.343\,Q$",
        "It lies outside the two charges, beyond the charge $" + S + r"2Q$",
    ],
    tail=tail("1,2,3", "2", "0", "EMFT - ECE", "Electric and Magnetic Fields (Electric Fields)", [
        "Given: charges $" + S + r"Q$ and $" + S + r"2Q$ at distance $" + S + r"d=0.5\ \text{m}$; a third charge $" + S + r"q$ makes all three charges be in equilibrium.",
        "Position: $" + S + r"q$ must itself be in equilibrium, so the forces from $" + S + r"Q$ and $" + S + r"2Q$ on it must cancel. Place it between them, at distance $" + S + r"x$ from $" + S + r"Q$: $" + S + r"\tfrac{Q}{x^2}=\tfrac{2Q}{(0.5-x)^2}$, so $" + S + r"0.5-x=\sqrt{2}\,x$ and $" + S + r"x=\tfrac{0.5}{1+\sqrt{2}}\approx 0.207\ \text{m}=20.7\ \text{cm}$.",
        "Sign and magnitude: the charge $" + S + r"Q$ is pushed away from $" + S + r"2Q$ by repulsion, so $" + S + r"q$ must pull it back, which requires $" + S + r"q$ to be negative. Balancing forces on $" + S + r"Q$: $" + S + r"\tfrac{Q\cdot 2Q}{0.5^2}=\tfrac{Q\,|q|}{x^2}$, so $" + S + r"|q|=8Q\,x^2=8Q\times 0.0429\approx 0.343\,Q$.",
        "So $" + S + r"q\approx -0.343\,Q$, located $" + S + r"20.7\ \text{cm}$ from $" + S + r"Q$ (and $" + S + r"29.3\ \text{cm}$ from $" + S + r"2Q$) on the line joining them.",
        "Check on $" + S + r"2Q$: repulsion from $" + S + r"Q$ is $" + S + r"\tfrac{2Q^2}{0.25}=8Q^2$ (times $" + S + r"k$) and attraction towards $" + S + r"q$ is $" + S + r"\tfrac{2Q\times 0.343Q}{0.293^2}\approx 8Q^2$, so $" + S + r"2Q$ is in equilibrium too.",
        "Hence options (1), (2) and (3) are correct.",
        "",
        "Tip: Use the two conditions in turn, first the position from equilibrium of the unknown charge (a ratio of the two charges), then its magnitude from equilibrium of one of the known charges; the third equilibrium is then automatically satisfied, which serves as a check.",
    ]),
)

Q21 = dict(
    type="MSQ",
    body=[
        "A medium has breakdown strength of $" + S + r"16\ \text{kV/m}$ r.m.s. Its relative permeability is $" + S + r"1.0$ and relative permittivity is $" + S + r"4.0$. A plane electromagnetic wave is transmitted through the medium. Calculate the maximum possible power flow density and the associated magnetic field.",
        "Which of the following statements are correct?",
    ],
    options=[
        "The intrinsic impedance of the medium is about $" + S + r"188.5\ \Omega$",
        "The maximum power flow density is about $" + S + r"1.36\ \text{MW/m}^2$",
        "The associated magnetic field is about $" + S + r"84.9\ \text{A/m}$ (r.m.s.)",
        "The maximum power flow density is about $" + S + r"0.68\ \text{MW/m}^2$",
    ],
    tail=tail("1,2,3", "2", "0", "EMFT - ECE", "Plane Waves (Flow of Electromagnetic Power and Poynting vector)", [
        "Given: $" + S + r"E_{rms}=16\ \text{kV/m}$ (the largest field the medium can withstand), $" + S + r"\mu_r=1$, $" + S + r"\varepsilon_r=4$.",
        "Intrinsic impedance: $" + S + r"\eta=\eta_0\sqrt{\tfrac{\mu_r}{\varepsilon_r}}=377\times\tfrac{1}{2}\approx 188.5\ \Omega$.",
        "Maximum power flow density: $" + S + r"S=\tfrac{E_{rms}^2}{\eta}=\tfrac{(16\times 10^3)^2}{188.5}=\tfrac{2.56\times 10^8}{188.5}\approx 1.36\times 10^{6}\ \text{W/m}^2$.",
        "Associated magnetic field: $" + S + r"H_{rms}=\tfrac{E_{rms}}{\eta}=\tfrac{16\times 10^3}{188.5}\approx 84.9\ \text{A/m}$.",
        "Hence options (1), (2) and (3) are correct.",
        "",
        "Tip: The breakdown strength limits the electric field, and the power density is then fixed by the medium's impedance, $" + S + r"S=\tfrac{E^2}{\eta}$ in r.m.s. values; a denser dielectric has a smaller $" + S + r"\eta$ and so carries more power for the same field.",
    ]),
)

Q22 = dict(
    type="MSQ",
    body=[
        "A rectangular hollow metal waveguide has dimensions $" + S + r"a=2.29\ \text{cm}$ and $" + S + r"b=1.02\ \text{cm}$. Microwave power at $" + S + r"10\ \text{GHz}$ is transmitted through the waveguide in the $" + S + r"\text{TE}_{10}$ mode. (a) Calculate the cut-off wavelength and the guide wavelength for this mode. (b) What are the other (TE or TM) modes that can propagate through the waveguide? (c) If $" + S + r"a=b=2.29\ \text{cm}$, what are the modes which can propagate through the waveguide?",
        "Which of the following statements are correct?",
    ],
    options=[
        "The cut-off wavelength of the $" + S + r"\text{TE}_{10}$ mode is $" + S + r"4.58\ \text{cm}$",
        "The guide wavelength of the $" + S + r"\text{TE}_{10}$ mode at $" + S + r"10\ \text{GHz}$ is about $" + S + r"3.97\ \text{cm}$",
        "No other mode propagates in the $" + S + r"2.29\ \text{cm}\times 1.02\ \text{cm}$ guide at $" + S + r"10\ \text{GHz}$, and for $" + S + r"a=b=2.29\ \text{cm}$ the propagating modes are $" + S + r"\text{TE}_{10},\ \text{TE}_{01},\ \text{TE}_{11}$ and $" + S + r"\text{TM}_{11}$",
        "For $" + S + r"a=b=2.29\ \text{cm}$ only $" + S + r"\text{TE}_{10}$ and $" + S + r"\text{TE}_{01}$ propagate",
    ],
    tail=tail("1,2,3", "2", "0", "EMFT - ECE", "Waveguides (Rectangular Waveguides)", [
        "Given: $" + S + r"a=2.29\ \text{cm}$, $" + S + r"b=1.02\ \text{cm}$, $" + S + r"f=10\ \text{GHz}$, so the free-space wavelength is $" + S + r"\lambda_0=\tfrac{c}{f}=\tfrac{3\times 10^{10}}{10^{10}}=3\ \text{cm}$.",
        "(a) For $" + S + r"\text{TE}_{10}$: $" + S + r"\lambda_c=2a=4.58\ \text{cm}$ (so $" + S + r"f_c=\tfrac{c}{2a}=6.55\ \text{GHz}$). Guide wavelength: $" + S + r"\lambda_g=\tfrac{\lambda_0}{\sqrt{1-(\lambda_0/\lambda_c)^2}}=\tfrac{3}{\sqrt{1-(3/4.58)^2}}=\tfrac{3}{0.7556}\approx 3.97\ \text{cm}$.",
        "(b) Cut-off frequencies $" + S + r"f_c=\tfrac{c}{2}\sqrt{(m/a)^2+(n/b)^2}$ for the next modes: $" + S + r"\text{TE}_{20}$: $" + S + r"\tfrac{c}{a}=13.1\ \text{GHz}$; $" + S + r"\text{TE}_{01}$: $" + S + r"\tfrac{c}{2b}=14.7\ \text{GHz}$. Both are above $" + S + r"10\ \text{GHz}$, and every other mode is higher still, so only $" + S + r"\text{TE}_{10}$ propagates.",
        "(c) For $" + S + r"a=b=2.29\ \text{cm}$: $" + S + r"\text{TE}_{10}$ and $" + S + r"\text{TE}_{01}$ both have $" + S + r"f_c=6.55\ \text{GHz}$, and $" + S + r"\text{TE}_{11}$ and $" + S + r"\text{TM}_{11}$ have $" + S + r"f_c=\tfrac{c}{\sqrt{2}\,a}=9.26\ \text{GHz}$, all below $" + S + r"10\ \text{GHz}$. The next modes ($" + S + r"\text{TE}_{20},\ \text{TE}_{02}$ at $" + S + r"13.1\ \text{GHz}$) are cut off. So the propagating modes are $" + S + r"\text{TE}_{10},\ \text{TE}_{01},\ \text{TE}_{11},\ \text{TM}_{11}$.",
        "Hence options (1), (2) and (3) are correct.",
        "",
        "Tip: To list the propagating modes, compare the cut-off frequency of each $" + S + r"(m,n)$ pair with the operating frequency and stop once $" + S + r"f_c>f$; in the square guide the modes $" + S + r"\text{TE}_{10}$ and $" + S + r"\text{TE}_{01}$ are degenerate, and $" + S + r"\text{TE}_{11}$ and $" + S + r"\text{TM}_{11}$ always share a cut-off, which is why all four appear together.",
    ]),
)

ALL = [Q122, Q123, Q124, Q125, Q222, Q223, Q224, Q225, Q19, Q20, Q21, Q22]
