import OrderedRemoval.Model

namespace OrderedRemoval
noncomputable section

/-- An actual H4-free repair always exists, including at matrix size zero. -/
theorem zero_HFree (n : ℕ) : HFree fixedH (fun _ _ : Fin n => false) := by
  classical
  unfold HFree copyCount
  rw [Finset.card_eq_zero]
  apply Finset.eq_empty_iff_forall_notMem.mpr
  intro rc hrc
  simp only [orderedCopies,Finset.mem_filter,Finset.mem_univ,true_and] at hrc
  have he := hrc 0 1
  simp [fixedH,anchor2] at he

theorem hammingDistance_le_square {n : ℕ} (A B : BinaryMatrix n) :
    hammingDistance A B ≤ n*n := by
  classical
  unfold hammingDistance
  simpa using (Finset.card_filter_le (s := (Finset.univ : Finset (Fin n × Fin n)))
    (fun rc => A rc.1 rc.2 ≠ B rc.1 rc.2))

theorem fixedMinEdits_le_repair {n : ℕ} (A B : BinaryMatrix n) (hf : HFree fixedH B) :
    fixedMinEdits A ≤ hammingDistance A B := by
  classical
  unfold fixedMinEdits
  apply Finset.min'_le
  exact Finset.mem_image.mpr ⟨B,Finset.mem_univ _,by simp [hf]⟩

theorem fixedMinEdits_le_square {n : ℕ} (A : BinaryMatrix n) : fixedMinEdits A ≤ n*n :=
  (fixedMinEdits_le_repair A _ (zero_HFree n)).trans (hammingDistance_le_square A _)

/-- The sentinel definition equals the edit count of an actual optimal repair. -/
theorem exists_optimal_repair {n : ℕ} (A : BinaryMatrix n) :
    ∃ B : BinaryMatrix n, HFree fixedH B ∧ fixedMinEdits A=hammingDistance A B := by
  classical
  have hmem : fixedMinEdits A ∈ (Finset.univ.image (fun B : BinaryMatrix n =>
      if HFree fixedH B then hammingDistance A B else n*n+1)) := by
    unfold fixedMinEdits
    exact Finset.min'_mem _ _
  obtain ⟨B,_,he⟩ := Finset.mem_image.mp hmem
  by_cases hf : HFree fixedH B
  · exact ⟨B,hf,(by simpa [hf] using he.symm)⟩
  · have hb := fixedMinEdits_le_square A
    simp only [hf,if_false] at he
    omega

theorem fixedDistance_le_repair {n : ℕ} (A B : BinaryMatrix n) (hf : HFree fixedH B) :
    fixedDistance A ≤ (hammingDistance A B : ℝ)/(n : ℝ)^2 := by
  unfold fixedDistance
  exact div_le_div_of_nonneg_right (by exact_mod_cast fixedMinEdits_le_repair A B hf)
    (sq_nonneg _)

end
end OrderedRemoval
