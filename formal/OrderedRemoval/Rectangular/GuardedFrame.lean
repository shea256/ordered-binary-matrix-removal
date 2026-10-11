import OrderedRemoval.Rectangular.Model
import OrderedRemoval.GuardedFrame

namespace OrderedRemoval.Rectangular
noncomputable section
open GuardedPath

/-- The selected second anchor row, together with both anchor columns, suffices
for the rectangular pattern. The inherited guard set protects a superset. -/
structure FrameValid {n : ℕ} (F : AnchorFrame n) (A : BinaryMatrix n)
    (r₀ r₁ c₀ c₁ : Fin n) : Prop where
  row_before : ∀ u, F.rows.val u < r₀
  row_lt : r₀ < r₁
  col_before : ∀ v, F.cols.val v < c₀
  col_lt : c₀ < c₁
  anchor : ∀ v, A (F.rows.val 1) (F.cols.val v) = decide (v.val = 0)
  row_zero : ∀ v, A r₀ (F.cols.val v) = decide (v.val = 0)
  row_one : ∀ v, A r₁ (F.cols.val v) = decide (v.val = 1)
  col_zero : A (F.rows.val 1) c₀ = false
  col_one : A (F.rows.val 1) c₁ = true

theorem FrameValid.transfer {n : ℕ} {F : AnchorFrame n} {A B : BinaryMatrix n}
    {r₀ r₁ c₀ c₁ : Fin n} (hF : FrameValid F A r₀ r₁ c₀ c₁)
    (hag : ∀ rc, F.Cell r₀ r₁ c₀ c₁ rc → A rc.1 rc.2 = B rc.1 rc.2) :
    FrameValid F B r₀ r₁ c₀ c₁ := by
  refine ⟨hF.row_before, hF.row_lt, hF.col_before, hF.col_lt, ?_, ?_, ?_, ?_, ?_⟩
  · intro v
    exact (hag _ (Or.inl ⟨1, v, rfl⟩)).symm.trans (hF.anchor v)
  · intro v
    exact (hag _ (Or.inr (Or.inl ⟨v, Or.inl rfl⟩))).symm.trans (hF.row_zero v)
  · intro v
    exact (hag _ (Or.inr (Or.inl ⟨v, Or.inr rfl⟩))).symm.trans (hF.row_one v)
  · exact (hag _ (Or.inr (Or.inr ⟨1, Or.inl rfl⟩))).symm.trans hF.col_zero
  · exact (hag _ (Or.inr (Or.inr ⟨1, Or.inr rfl⟩))).symm.trans hF.col_one

theorem FrameValid.not_HFree {n : ℕ} {F : AnchorFrame n} {B : BinaryMatrix n}
    {r₀ r₁ c₀ c₁ : Fin n} (hF : FrameValid F B r₀ r₁ c₀ c₁)
    (hbody : PathPropagation.Body B r₀ r₁ c₀ c₁) : ¬ HFree B := by
  classical
  let ar : IncreasingMap 1 n := ⟨fun _ => F.rows.val 1, by
    intro i j hij; have hi := i.isLt; have hj := j.isLt
    have hij' : i.val < j.val := hij
    omega⟩
  let rr := appendTwoIncreasing ar r₀ r₁ (fun _ => hF.row_before 1) hF.row_lt
  let cc := appendTwoIncreasing F.cols c₀ c₁ hF.col_before hF.col_lt
  have hmem : (rr, cc) ∈ orderedCopies B := by
    simp only [orderedCopies, Finset.mem_filter, Finset.mem_univ, true_and]
    intro i j
    have ha0 := hF.anchor 0
    have ha1 := hF.anchor 1
    have hr00 := hF.row_zero 0
    have hr01 := hF.row_zero 1
    have hr10 := hF.row_one 0
    have hr11 := hF.row_one 1
    rcases hbody with ⟨h00,h01,h10,h11⟩
    have hc0 := hF.col_zero
    have hc1 := hF.col_one
    fin_cases i <;> fin_cases j <;>
      simp_all [rr,cc,ar,appendTwoIncreasing,appendTwo,fixedH]
  exact Nat.ne_of_gt (Finset.card_pos.mpr ⟨(rr,cc),hmem⟩)

end
end OrderedRemoval.Rectangular
