import OrderedRemoval.Crown.Main
import OrderedRemoval.Crown.Blowup

namespace OrderedRemoval.Crown
noncomputable section

/-- The fixed 3×3 pattern admits no polynomial removal bound, with arbitrarily
small epsilon and arbitrarily large hosts for that same epsilon. All binary
repair directions and locations are unrestricted. -/
theorem no_polynomial_removal_bound (c C ε₀ : ℝ)
    (hc : 0<c) (hC : 0<C) (hε₀ : 0<ε₀) :
    ∃ ε : ℝ, 0<ε ∧ ε<ε₀ ∧ ∀ N : ℕ,
      ∃ n : ℕ, max 1 N≤n ∧ ∃ A : BinaryMatrix n,
        (∀ B : BinaryMatrix n, HFree B → ε*(n:ℝ)^2≤(hammingDistance A B:ℝ)) ∧
        (copyCount A:ℝ)<c*Real.rpow ε C*(n:ℝ)^6 := by
  obtain ⟨ε,hε,hεsmall,n,hn,A,hrep,hcount⟩ :=
    no_polynomial_bound_small_epsilon c C ε₀ hc hC hε₀
  refine ⟨ε,hε,hεsmall,?_⟩
  intro N
  let q := N+1
  have hq : 0<q := by dsimp [q]; omega
  have hnq : max 1 N≤n*q := by
    have he : q≤n*q := by nlinarith
    have hm : max 1 N≤q := by dsimp [q]; omega
    exact hm.trans he
  have hqR : (0:ℝ)<q := by exact_mod_cast hq
  refine ⟨n*q,hnq,blowup A q,?_,?_⟩
  · exact blowup_repair_normalized A ε hrep
  · calc
      (copyCount (blowup A q):ℝ)≤(copyCount A:ℝ)*(q:ℝ)^6 := by
        exact_mod_cast blowup_copyCount_le (q:=q) A
      _ < (c*Real.rpow ε C*(n:ℝ)^6)*(q:ℝ)^6 :=
        mul_lt_mul_of_pos_right hcount (pow_pos hqR 6)
      _ = c*Real.rpow ε C*((n*q:ℕ):ℝ)^6 := by push_cast; ring

end
end OrderedRemoval.Crown
