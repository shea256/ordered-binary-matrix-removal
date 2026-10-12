import OrderedRemoval.Crown.CoarseCopyBound
import OrderedRemoval.Crown.RepairDistance
import OrderedRemoval.Rectangular.Asymptotics

namespace OrderedRemoval.Crown
noncomputable section

/-- The same concrete square host has both required integer estimates. -/
theorem concrete_host_bounds (h : ℕ) (hh : 1≤h) :
    (∀ B : BinaryMatrix (OrderedHost.size h), HFree B →
      (2^h)^2 ≤ hammingDistance (concreteMatrix h) B) ∧
    copyCount (concreteMatrix h) ≤ 2*2^h*(OrderedHost.size h)^4 :=
  ⟨concrete_repair_lower_bound h hh,copyCount_le h⟩

/-- Density normalization keeps the factor two and uses 3+3=6 positions. -/
theorem concrete_copy_density (h : ℕ) :
    (copyCount (concreteMatrix h) : ℝ) / (OrderedHost.size h : ℝ)^6 ≤
      2 * (1/((14*(h:ℝ)+2)^2)) * (1/((2:ℝ)^h)) := by
  have hd : 0<14*(h:ℝ)+2 := by positivity
  have hm : 0<(2:ℝ)^h := by positivity
  have hn : 0<(OrderedHost.size h : ℝ) := by
    dsimp [OrderedHost.size]; positivity
  have hc : (copyCount (concreteMatrix h) : ℝ) ≤
      2*(2:ℝ)^h*(OrderedHost.size h : ℝ)^4 := by exact_mod_cast copyCount_le h
  apply (div_le_iff₀ (pow_pos hn 6)).2
  calc
    _ ≤ 2*(2:ℝ)^h*(OrderedHost.size h : ℝ)^4 := hc
    _ = _ := by simp only [OrderedHost.size,Nat.cast_mul,Nat.cast_add,Nat.cast_pow,Nat.cast_ofNat]; field_simp

/-- Every repair obeys the normalized distance lower bound. -/
theorem concrete_repair_normalized (h : ℕ) (hh : 1≤h)
    (B : BinaryMatrix (OrderedHost.size h)) (hB : HFree B) :
    (1/((14*(h:ℝ)+2)^2))*(OrderedHost.size h : ℝ)^2 ≤
      (hammingDistance (concreteMatrix h) B : ℝ) := by
  have hd : 0<14*(h:ℝ)+2 := by positivity
  have he : (1/((14*(h:ℝ)+2)^2))*(OrderedHost.size h : ℝ)^2 = ((2:ℝ)^h)^2 := by
    simp only [OrderedHost.size,Nat.cast_mul,Nat.cast_add,Nat.cast_pow,Nat.cast_ofNat]
    field_simp
  rw [he]
  exact_mod_cast concrete_repair_lower_bound h hh B hB

/-- Preliminary capstone with arbitrarily small distance scale. The separate
blowup theorem is needed to keep this same epsilon for arbitrarily large hosts. -/
theorem no_polynomial_bound_small_epsilon (c C ε₀ : ℝ)
    (hc : 0<c) (_hC : 0<C) (hε₀ : 0<ε₀) :
    ∃ ε : ℝ, 0<ε ∧ ε<ε₀ ∧ ∃ n : ℕ, 1≤n ∧ ∃ A : BinaryMatrix n,
      (∀ B : BinaryMatrix n, HFree B → ε*(n:ℝ)^2≤(hammingDistance A B:ℝ)) ∧
      (copyCount A:ℝ)<c*Real.rpow ε C*(n:ℝ)^6 := by
  obtain ⟨N,hN⟩ := exists_nat_gt (1/ε₀)
  obtain ⟨h,hhN,hh,hdecay⟩ := Rectangular.exists_depth_polynomial_decay c C hc N
  let ε : ℝ := 1/((14*(h:ℝ)+2)^2)
  have hε : 0<ε := by dsimp [ε]; positivity
  have hεsmall : ε<ε₀ := by
    have hhR : (N:ℝ)≤h := by exact_mod_cast hhN
    have hh0 : (0:ℝ)≤h := Nat.cast_nonneg h
    have hh1 : (1:ℝ)≤h := by exact_mod_cast hh
    have hd : 0<14*(h:ℝ)+2 := by positivity
    have hb : 1/ε₀<(14*(h:ℝ)+2)^2 := by nlinarith
    have hb' := (div_lt_iff₀ hε₀).mp hb
    exact (div_lt_iff₀ (pow_pos hd 2)).2 (by nlinarith)
  have hn : 0<OrderedHost.size h := by dsimp [OrderedHost.size]; positivity
  have hnR : (0:ℝ)<OrderedHost.size h := by exact_mod_cast hn
  refine ⟨ε,hε,hεsmall,OrderedHost.size h,hn,concreteMatrix h,?_,?_⟩
  · exact concrete_repair_normalized h hh
  · exact (div_lt_iff₀ (pow_pos hnR 6)).mp ((concrete_copy_density h).trans_lt hdecay)

end
end OrderedRemoval.Crown
