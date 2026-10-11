import OrderedRemoval.CoarseCopyBound
import OrderedRemoval.OrderedRepairDistance
import OrderedRemoval.SequenceAssembly
import OrderedRemoval.Consequence
import OrderedRemoval.DistanceMeaning

namespace OrderedRemoval
noncomputable section

/-- Both integer bounds hold for the same concrete host and independent axis orders. -/
theorem concrete_host_bounds (h : ℕ) (hh : 1 ≤ h) :
    SequenceAssembly.HostBounds (Concrete.matrix h) (2 ^ h) := by
  refine ⟨?_, Concrete.copyCount_le h⟩
  intro B hfree
  exact OrderedHost.hammingDistance_ge hh B hfree

/-- The actual 4×4 construction gives the counterexample sequence at every depth. -/
theorem counterexample_sequence :
    ∀ h : ℕ, 1 ≤ h →
      let d : ℕ := 14 * h + 2
      let n : ℕ := d * 2 ^ h
      ∃ A : BinaryMatrix n,
        fixedDistance A ≥ 1 / ((d : ℝ) ^ 2) ∧
        (copyCount fixedH A : ℝ) / ((n : ℝ) ^ 8) ≤
          2 * (1 / ((d : ℝ) ^ 2)) * (1 / ((2 : ℝ) ^ h)) := by
  apply SequenceAssembly.counterexample_sequence_of_integer_bounds
  intro h hh
  exact ⟨Concrete.matrix h, concrete_host_bounds h hh⟩

/-- The fixed 4×4 ordered binary pattern admits no polynomial removal bound. -/
theorem no_polynomial_removal_bound :
    ∀ c C : ℝ, 0 < c → 0 < C →
      ∃ n : ℕ, 1 ≤ n ∧
        ∃ ε : ℝ, 0 < ε ∧ ε < 1 ∧
          ∃ A : BinaryMatrix n,
            fixedDistance A ≥ ε ∧
            (copyCount fixedH A : ℝ) <
              c * Real.rpow ε C * ((n : ℝ) ^ 8) :=
  no_polynomial_removal_bound_of_sequence counterexample_sequence

/-- The same capstone stated directly in terms of every binary repair, without
using a minimum-distance definition in the statement. -/
theorem no_polynomial_removal_bound_arbitrary_repairs :
    ∀ c C : ℝ, 0 < c → 0 < C →
      ∃ n : ℕ, 1 ≤ n ∧
        ∃ ε : ℝ, 0 < ε ∧ ε < 1 ∧
          ∃ A : BinaryMatrix n,
            (∀ B : BinaryMatrix n, HFree fixedH B →
              ε * (n : ℝ) ^ 2 ≤ (hammingDistance A B : ℝ)) ∧
            (copyCount fixedH A : ℝ) <
              c * Real.rpow ε C * ((n : ℝ) ^ 8) := by
  intro c C hc hC
  obtain ⟨n, hn, ε, hε, hε1, A, hdist, hcount⟩ :=
    no_polynomial_removal_bound c C hc hC
  refine ⟨n, hn, ε, hε, hε1, A, ?_, hcount⟩
  intro B hfree
  have hnR : (0 : ℝ) < n := by exact_mod_cast hn
  exact (le_div_iff₀ (pow_pos hnR 2)).mp
    (hdist.trans (fixedDistance_le_repair A B hfree))

end
end OrderedRemoval
