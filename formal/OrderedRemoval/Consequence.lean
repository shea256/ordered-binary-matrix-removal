/-
Adapted from OpenAI Consequence.lean, commit
fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb (Apache-2.0).
Use host coefficient 14, pattern exponent 8, and the factor two in
the coarse zero-set bound; the analytic and normalization methods are inherited.
-/
import OrderedRemoval.Model
import OrderedRemoval.Asymptotics

namespace OrderedRemoval

/-!
The sequence of matrix counterexamples rules out every polynomial
removal bound.
-/

noncomputable section


/-- Exponential decay of the copy density rules out polynomial removal bounds. -/
theorem no_polynomial_removal_bound_of_sequence
    (hseq : ∀ h : ℕ, 1 ≤ h →
      let d : ℕ := 14 * h + 2
      let n : ℕ := d * 2 ^ h
      ∃ A : BinaryMatrix n,
        fixedDistance A ≥ 1 / ((d : ℝ) ^ 2) ∧
        (copyCount fixedH A : ℝ) / ((n : ℝ) ^ 8) ≤
          2 * (1 / ((d : ℝ) ^ 2)) * (1 / ((2 : ℝ) ^ h))) :
    ∀ c C : ℝ, 0 < c → 0 < C →
      ∃ n : ℕ, 1 ≤ n ∧
        ∃ ε : ℝ, 0 < ε ∧ ε < 1 ∧
          ∃ A : BinaryMatrix n,
            fixedDistance A ≥ ε ∧
            (copyCount fixedH A : ℝ) <
              c * Real.rpow ε C * ((n : ℝ) ^ 8) := by
  intro c C hc _hC
  obtain ⟨h, hh, hdecay⟩ := exists_depth_polynomial_decay c C hc
  let d : ℕ := 14 * h + 2
  let n : ℕ := d * 2 ^ h
  have hd : 1 < d := by dsimp [d]; omega
  have hdR : (1 : ℝ) < d := by exact_mod_cast hd
  have hdpos : (0 : ℝ) < d := by linarith
  have hn : 0 < n := Nat.mul_pos (by omega) (pow_pos (by decide) _)
  have hnR : (0 : ℝ) < n := by exact_mod_cast hn
  obtain ⟨A, hdist, hcopies⟩ := hseq h hh
  refine ⟨n, hn, 1 / ((d : ℝ) ^ 2), by positivity, ?_, A, hdist, ?_⟩
  · apply (div_lt_one (by positivity)).2
    nlinarith
  · have hdecay' : 2 * (1 / ((d : ℝ) ^ 2)) * (1 / ((2 : ℝ) ^ h)) <
        c * Real.rpow (1 / ((d : ℝ) ^ 2)) C := by
      simpa [d] using hdecay
    exact (div_lt_iff₀ (pow_pos hnR 8)).mp (hcopies.trans_lt hdecay')


end

end OrderedRemoval
