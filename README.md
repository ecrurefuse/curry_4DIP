# 4DIP: A Self-Stabilizing Framework for Predicting Physical Systems

4DIP (4-Dimensional Iterative Prediction) is a symbolic, adaptive simulation framework designed to evolve physical systems while removing singularities, avoiding divergence, and converging naturally based on physical quantities—not arbitrary tolerances.

Unlike traditional solvers like RK45 or Euler methods, 4DIP uses dual convergence logic:
- **Dynamic time control** based on a Fourier-like curvature function
- **Symbolic energy damping** derived from the instantaneous rate of energy change

The result is a method that can resolve behavior across scalar, vector, matrix, and tensor systems using only first-principles physics—achieving convergence down to \( \Delta E < 10^{-14} \) (Tier 5 precision).

---

## 🧪 What's Included

- 🧠 Full Paper: `paper/4dip_framework_paper.tex`  
- 📄 PDF: `paper/4dip_framework_paper.pdf`  
- 📂 Code:
  - All Tier 5 test scripts in `code/`
  - Scalar systems (60+ total)
  - Chaos and orbital modules (future releases)
- 📊 Results:
  - Output files from each system test in `results/`

---

## 🧬 Validated Systems (Preview from Paper)

- **Relativity:** Time dilation, Lorentz contraction
- **Gravitational Systems:** Capped inverse-square, uncapped gravity
- **Quantum Systems:** Planck curvature
- **Classical Mechanics:** Spring, oscillators, energy decay
- **Matrix and Tensor:** 2x2 matrix system (decay)
- **Chaos:** Lorenz, Chua, pendulum

---

## ✉️ Author

**Jon Curry**  
Independent Researcher, USA  
📧 Email: [4dip@protonmail.com](mailto:4dip@protonmail.com)  
🔗 GitHub: [ecrurefuse/curry_4DIP](https://github.com/ecrurefuse/curry_4DIP)

---

## 📜 License

This repository is licensed under the [MIT License](LICENSE). You can freely use, modify, and distribute the software for academic and research purposes.
