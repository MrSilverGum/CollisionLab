import streamlit as st
import time

st.set_page_config(page_title="⚛️ Particle Reaction Simulator", page_icon="⚛️", layout="wide")

# --- Inject CSS to increase number input width and tighten spacing ---
st.markdown("""
<style>
div[data-testid="stNumberInput"] {
    width: 140px !important;
    margin-left: 4px !important;
    margin-top: -2px !important;
}

div[data-testid="stNumberInput"] input {
    width: 60px !important;
    text-align: center;
}

.css-1kyxreq, .stCheckbox {
    margin-bottom: 0.75rem !important;
    margin-right: 2px !important;
}

section.main > div { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# --- Particles and Symbols ---
PAIRS = [
    ("Proton (p)", "p", "Antiproton (p̄)", "anti_p"),
    ("Neutron (n)", "n", "Antineutron (n̄)", "anti_n"),
    ("Electron (e⁻)", "e_minus", "Positron (e⁺)", "e_plus"),
    ("Electron neutrino (νₑ)", "nu_e", "Electron antineutrino (ν̄ₑ)", "anti_nu_e")
]

#SINGLES = [("Photon (γ)", "gamma")]

LATEX = {
    "p": "p", "anti_p": "\\bar{p}",
    "n": "n", "anti_n": "\\bar{n}",
    "e_minus": "e^-", "e_plus": "e^+",
    "nu_e": "\\nu_e", "anti_nu_e": "\\bar{\\nu}_e",
    "gamma": "\\gamma"
}

st.markdown("<h1 style='text-align: center;'>⚛️ Particle Reaction Simulator</h1>", unsafe_allow_html=True)
top = st.container()

# --- Reset Button ---
col_reset, _, _ = st.columns([1, 4, 1])
with col_reset:
    if st.button("Reset All"):
        for _, s1, _, s2 in PAIRS:
            st.session_state[f"check_{s1}"] = False
            st.session_state[f"input_{s1}"] = 1
            st.session_state[f"check_{s2}"] = False
            st.session_state[f"input_{s2}"] = 1
#        for _, s in SINGLES:
#            st.session_state[f"check_{s}"] = False
#            st.session_state[f"input_{s}"] = 1

st.divider()

# --- Particle Row Renderer ---
def render_particle_inline(label, symbol):
    cbox_key = f"check_{symbol}"
    input_key = f"input_{symbol}"

    if cbox_key not in st.session_state:
        st.session_state[cbox_key] = False
    if input_key not in st.session_state:
        st.session_state[input_key] = 1

    row = st.columns([0.3, 0.7])
    with row[0]:
        checked = st.checkbox(label, key=cbox_key)
    with row[1]:
        if checked:
            st.number_input(" ", key=input_key, min_value=1, step=1, format="%d", label_visibility="collapsed")

# --- Render Paired Particles ---
for left, sym_l, right, sym_r in PAIRS:
    cols = st.columns(2)
    with cols[0]:
        render_particle_inline(left, sym_l)
    with cols[1]:
        render_particle_inline(right, sym_r)

# --- Render Singles with alignment ---
#for name, sym in SINGLES:
#    cols = st.columns(2)
#    with cols[0]:
#        render_particle_inline(name, sym)
#    with cols[1]:
#        st.write("")

# --- Collect and Display Reaction ---
particles = {}
for _, sym_l, _, sym_r in PAIRS:
    if st.session_state.get(f"check_{sym_l}"):
        particles[sym_l] = st.session_state.get(f"input_{sym_l}", 0)
    if st.session_state.get(f"check_{sym_r}"):
        particles[sym_r] = st.session_state.get(f"input_{sym_r}", 0)

#for _, sym in SINGLES:
#    if st.session_state.get(f"check_{sym}"):
#        particles[sym] = st.session_state.get(f"input_{sym}", 0)

with top:
    st.divider()
#    st.subheader("📦 Current Reaction Setup")
    start = time.perf_counter()

    if particles:
    # format left-hand side

    # compute sum expressions to bound loops
        p = particles.get('p', 0)
        n = particles.get('n', 0)
        e_minus = particles.get('e_minus', 0)
        nu_e = particles.get('nu_e', 0)
        e_plus = particles.get('e_plus', 0)
        anti_p = particles.get('anti_p', 0)
        anti_n = particles.get('anti_n', 0)
        anti_nu_e = particles.get('anti_nu_e', 0)

        p_n = p + n - anti_p - anti_n
        p_e_plus = p + e_plus - e_minus - anti_p
        p_nu_e = p + nu_e - anti_p - anti_nu_e
        n_e_minus = n + e_minus - e_plus - anti_n
        n_anti_nu_e = n + anti_nu_e - nu_e - anti_n
        e_minus_anti_p = e_minus + anti_p - p - e_plus
        e_minus_nu_e = e_minus + nu_e - e_plus - anti_nu_e
        e_plus_anti_n = e_plus + anti_n - e_minus - n
        e_plus_anti_nu_e = e_plus + anti_nu_e - e_minus - nu_e
        anti_p_anti_n = anti_p + anti_n - p - n
        anti_p_anti_nu_e = anti_p + anti_nu_e - p - nu_e
        anti_n_nu_e = anti_n + nu_e - n - anti_nu_e

        masses = {
            'p': 938.272,      
            'n': 939.565,     
            'e_minus': 0.511, 
            'e_plus': 0.511,  
            'nu_e': 0.0000022,   
            'anti_p': 938.272,
            'anti_n': 939.565,
            'anti_nu_e': 0.0000022,
            'gamma': 0.0
        }

        sums = {
        'p_n': p_n,
        'p_e_plus': p_e_plus,
        'p_nu_e': p_nu_e,
        'n_e_minus': n_e_minus,
        'n_anti_nu_e': n_anti_nu_e,
        'e_minus_anti_p': e_minus_anti_p,
        'e_minus_nu_e': e_minus_nu_e,
        'e_plus_anti_n': e_plus_anti_n,
        'e_plus_anti_nu_e': e_plus_anti_nu_e,
        'anti_p_anti_n': anti_p_anti_n,
        'anti_p_anti_nu_e': anti_p_anti_nu_e,
        'anti_n_nu_e': anti_n_nu_e
        }
    # Debug sums
        #st.write("Debug sums:", sums)

    # determine max counts per species based on sums
        max_counts = {
        'p': max(0, p_n, p_e_plus, p_nu_e),
        'n': max(0, p_n, n_e_minus, n_anti_nu_e),
        'e_minus': max(0, n_e_minus, e_minus_anti_p, e_minus_nu_e),
        'nu_e': max(0, p_nu_e, e_minus_nu_e, anti_n_nu_e),
        'e_plus': max(0, p_e_plus, e_plus_anti_n, e_plus_anti_nu_e),
        'anti_p': max(0, e_minus_anti_p, anti_p_anti_n, anti_p_anti_nu_e),
        'anti_n': max(0, e_plus_anti_n, anti_p_anti_n, anti_n_nu_e),
        'anti_nu_e': max(0, n_anti_nu_e, e_plus_anti_nu_e, anti_p_anti_nu_e)
        }
    # Debug max_counts
        #st.write("Debug max_counts:", max_counts)

    # enumerate possible reactions
        particles_list = ['p', 'n', 'e_minus', 'nu_e', 'e_plus', 'anti_p', 'anti_n', 'anti_nu_e']
        seen_signatures = set()
        reactions = []

        def compute_reaction_from_leading(leading, value):
            vals = {p: 0 for p in particles_list}
            vals[leading] = value

            try:
                if leading == 'p':
                    vals['n'] = sums['p_n'] - vals['p']
                    vals['e_minus'] = sums['n_e_minus'] - vals['n']
                    vals['nu_e'] = sums['p_nu_e'] - vals['p']
                    vals['e_plus'] = sums['p_e_plus'] - vals['p']
                    vals['anti_p'] = sums['e_minus_anti_p'] - vals['e_minus']
                    vals['anti_n'] = sums['anti_n_nu_e'] - vals['nu_e']
                    vals['anti_nu_e'] = sums['n_anti_nu_e'] - vals['n']
                elif leading == 'n':
                    vals['p'] = sums['p_n'] - vals['n']
                    vals['e_minus'] = sums['n_e_minus'] - vals['n']
                    vals['nu_e'] = sums['p_nu_e'] - vals['p']
                    vals['e_plus'] = sums['p_e_plus'] - vals['p']
                    vals['anti_p'] = sums['e_minus_anti_p'] - vals['e_minus']
                    vals['anti_n'] = sums['anti_n_nu_e'] - vals['nu_e']
                    vals['anti_nu_e'] = sums['n_anti_nu_e'] - vals['n']
                elif leading == 'e_minus':
                    vals['n'] = sums['n_e_minus'] - vals['e_minus']
                    vals['p'] = sums['p_n'] - vals['n']
                    vals['nu_e'] = sums['p_nu_e'] - vals['p']
                    vals['e_plus'] = sums['p_e_plus'] - vals['p']
                    vals['anti_p'] = sums['e_minus_anti_p'] - vals['e_minus']
                    vals['anti_n'] = sums['anti_n_nu_e'] - vals['nu_e']
                    vals['anti_nu_e'] = sums['n_anti_nu_e'] - vals['n']
                elif leading == 'nu_e':
                    vals['p'] = sums['p_nu_e'] - vals['nu_e']
                    vals['n'] = sums['p_n'] - vals['p']
                    vals['e_minus'] = sums['n_e_minus'] - vals['n']
                    vals['e_plus'] = sums['p_e_plus'] - vals['p']
                    vals['anti_p'] = sums['e_minus_anti_p'] - vals['e_minus']
                    vals['anti_n'] = sums['anti_n_nu_e'] - vals['nu_e']
                    vals['anti_nu_e'] = sums['n_anti_nu_e'] - vals['n']
                elif leading == 'e_plus':
                    vals['p'] = sums['p_e_plus'] - vals['e_plus']
                    vals['n'] = sums['p_n'] - vals['p']
                    vals['e_minus'] = sums['n_e_minus'] - vals['n']
                    vals['nu_e'] = sums['p_nu_e'] - vals['p']
                    vals['anti_p'] = sums['e_minus_anti_p'] - vals['e_minus']
                    vals['anti_n'] = sums['anti_n_nu_e'] - vals['nu_e']
                    vals['anti_nu_e'] = sums['n_anti_nu_e'] - vals['n']
                elif leading == 'anti_p':
                    vals['e_minus'] = sums['e_minus_anti_p'] - vals['anti_p']
                    vals['n'] = sums['n_e_minus'] - vals['e_minus']
                    vals['p'] = sums['p_n'] - vals['n']
                    vals['e_plus'] = sums['p_e_plus'] - vals['p']
                    vals['nu_e'] = sums['p_nu_e'] - vals['p']
                    vals['anti_n'] = sums['anti_n_nu_e'] - vals['nu_e']
                    vals['anti_nu_e'] = sums['n_anti_nu_e'] - vals['n']
                elif leading == 'anti_n':
                    vals['nu_e'] = sums['anti_n_nu_e'] - vals['anti_n']
                    vals['p'] = sums['p_nu_e'] - vals['nu_e']
                    vals['n'] = sums['p_n'] - vals['p']
                    vals['e_minus'] = sums['n_e_minus'] - vals['n']
                    vals['e_plus'] = sums['p_e_plus'] - vals['p']
                    vals['anti_p'] = sums['e_minus_anti_p'] - vals['e_minus']
                    vals['anti_nu_e'] = sums['n_anti_nu_e'] - vals['n']
                elif leading == 'anti_nu_e':
                    vals['n'] = sums['n_anti_nu_e'] - vals['anti_nu_e']
                    vals['p'] = sums['p_n'] - vals['n']
                    vals['nu_e'] = sums['p_nu_e'] - vals['p']
                    vals['e_minus'] = sums['n_e_minus'] - vals['n']
                    vals['e_plus'] = sums['p_e_plus'] - vals['p']
                    vals['anti_p'] = sums['e_minus_anti_p'] - vals['e_minus']
                    vals['anti_n'] = sums['anti_n_nu_e'] - vals['nu_e']                                                              
            except Exception:
                return None 

            #if any(v < 0 for v in vals.values()):
            #    return None

            return vals

        def compute_mass_energy(state, masses):
            return sum(
                masses.get(k, 0) * v
                for k, v in state.items()
                if v > 0
            )
        
        lhs_energy = compute_mass_energy(particles, masses)

        for particle in particles_list:
            for i in range(max_counts[particle] + 1):
                reaction = compute_reaction_from_leading(particle, i)
                if reaction is None:
                    continue

                signature = tuple(reaction[p] for p in particles_list)
                if signature in seen_signatures:
                    continue

                seen_signatures.add(signature)
                rhs_energy = compute_mass_energy(reaction, masses)
                #st.write(f"Found {reaction} reactions.")
                delta_e = lhs_energy - rhs_energy
                reactions.append((delta_e, reaction))

        #st.write(f"Found {len(reactions)} reactions.")
    # format and display

        reactions.sort(key=lambda x: -x[0])

        lhs = " + ".join(
            f"{cnt}{LATEX[k]}" if cnt > 1 else LATEX[k]
            for k, cnt in particles.items() if cnt > 0
        )

        for delta_e, out in reactions:
            rhs = " + ".join(
                f"{cnt}{LATEX[k]}" if cnt > 1 else LATEX[k]
                for k, cnt in out.items() if cnt > 0
            )
            energy_str = f"{'+ '}{abs(delta_e):.3f}\\,\\text{{MeV}}"
            if delta_e >= 0:
                st.latex(f"{lhs} \\rightarrow {rhs} {energy_str}")
            else:
                st.latex(f"{lhs} {energy_str} \\rightarrow {rhs}")
            #st.success("✅ Simulation updated.")
        st.success(f"✅ {len(reactions)} reactions calculated")
    else:
        st.info("No particles selected.")

    st.caption(f"🕒 Computation time: {time.perf_counter() - start:.5f} seconds")