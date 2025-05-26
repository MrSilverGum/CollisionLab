# ⚛️ Particle Reaction Simulator

Instant calculation of possible reactions involving particles and antiparticles while preserving physical laws and energy assessment.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://collisionlab.streamlit.app)

## 🔍 Overview

Particle Reaction Simulator is a web application built with Streamlit for exploring interactions between elementary particles and their antiparticles. It allows users to select input particles, and then:

### 💥 Enumerates possible output reactions that: ###

- Conserve baryon number

- Conserve electric charge

- Conserve lepton number

### 🔋 Computes energy balance of each reaction based on rest mass

### 📈 Sorts the reactions by energy output (from most exothermic to most endothermic)

## 📝 Supported Particles


| Name                   | Symbol    |
|------------------------|-----------|
| Proton                 | p         |
| Antiproton             | p̄        |
| Neutron                | n         |
| Antineutron            | n̄        |
| Electron               | e⁻        |
| Positron               | e⁺        |
| Electron Neutrino      | νₑ        |
| Electron Antineutrino  | ν̄ₑ       |

_(Photon γ may be implicitly assumed in energy balance but is not explicitly shown.)_

## 🚀 Features

- Custom UI for particle selection

- Dynamic equation rendering in LaTeX

- Efficient combination search with signature hashing

- Mass-energy calculation in MeV (Mega Electron Volts)

- Reaction filtering based on physics rules

- Ultra-fast performance even with hundreds of particles

### 🖥️ How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
