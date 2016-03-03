import cmath

def runPllSim():
    input("Press Enter to continue...");
    phase_offset = 0.0;
    frequency_offset = 0.30;
    bandwidth = 0.01;
    damping_factor = 0.707;
    gain = 1000;
    samples = 400;

    tau_1 = gain / (bandwidth * bandwidth);
    tau_2 = 2 * damping_factor/bandwidth;

    b0 = (4 * gain/tau_1)*(1.0+tau_2/2.0)
    b1 = (8 * gain/tau_1)
    b2 = (4 * gain/tau_1)*(1.0-tau_2/2.0)

    a1 = -2.0
    a2 = 1.0

    print("#  b = [b0:%12.8f, b1:%12.8f, b2:%12.8f]\n" %(b0, b1, b2))
    print("#  a = [a0:%12.8f, a1:%12.8f, a2:%12.8f]\n" % (1, a1, a2))
    input("Done!")

    # Filter Buffers
    v0 = 0.0;
    v1 = 0.0;
    v2 = 0.0;

    # init states
    phi = phase_offset;
    phi_hat = 0.0;

    # table legend
    print("# %6s %12s %12s %12s %12s %12s\n" % ("index", "real(x)", "imag(x)", "real(y)", "imag(y)", "error"));

    # simulation
    i = 0;
    x = complex(0,0);
    y = complex(0,0);
    for i in range(0, samples):
        # input
        x = cmath.rect(1, phi);
        phi = phi + frequency_offset;

        # pll phase estimate
        y = cmath.rect(1,phi_hat);

        # error
        delta_phi = cmath.phase(x * y.conjugate());

        # print results to standard output
        print("  %6u %12.8f %12.8f %12.8f %12.8f %12.8f\n" % (i,x.real, x.imag, y.real, y.imag, delta_phi));

        # push Buffers
        v2 = v1
        v1 = v0


        v0 = delta_phi - v1*a1 - v2 *a2;

        # new output
        phi_hat = v0*b0 + v1+b1 + v2*b2;

    input("Done!");

if __name__ == "__main__":
    runPllSim();
