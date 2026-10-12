import OrderedRemoval.Crown.Model
import OrderedRemoval.GuardedFrame

namespace OrderedRemoval.Crown
noncomputable section
open GuardedPath

/-- One prefix anchor row and one suffix anchor column complete P to the
3×3 crown. The inherited guard set protects a superset of these five cells. -/
structure FrameValid {n : ℕ} (F : AnchorFrame n) (A : BinaryMatrix n)
    (r₀ r₁ c₀ c₁ : Fin n) : Prop where
  row_before : ∀ u, F.rows.val u < r₀
  row_lt : r₀ < r₁
  col_after : ∀ v, c₁ < F.cols.val v
  col_lt : c₀ < c₁
  anchor : A (F.rows.val 1) (F.cols.val 0) = true
  row_zero : A r₀ (F.cols.val 0) = true
  row_one : A r₁ (F.cols.val 0) = false
  col_zero : A (F.rows.val 1) c₀ = false
  col_one : A (F.rows.val 1) c₁ = true

theorem FrameValid.transfer {n : ℕ} {F : AnchorFrame n} {A B : BinaryMatrix n}
    {r₀ r₁ c₀ c₁ : Fin n} (hF : FrameValid F A r₀ r₁ c₀ c₁)
    (hag : ∀ rc, F.Cell r₀ r₁ c₀ c₁ rc → A rc.1 rc.2 = B rc.1 rc.2) :
    FrameValid F B r₀ r₁ c₀ c₁ := by
  refine ⟨hF.row_before,hF.row_lt,hF.col_after,hF.col_lt,?_,?_,?_,?_,?_⟩
  · exact (hag _ (Or.inl ⟨1,0,rfl⟩)).symm.trans hF.anchor
  · exact (hag _ (Or.inr (Or.inl ⟨0,Or.inl rfl⟩))).symm.trans hF.row_zero
  · exact (hag _ (Or.inr (Or.inl ⟨0,Or.inr rfl⟩))).symm.trans hF.row_one
  · exact (hag _ (Or.inr (Or.inr ⟨1,Or.inl rfl⟩))).symm.trans hF.col_zero
  · exact (hag _ (Or.inr (Or.inr ⟨1,Or.inr rfl⟩))).symm.trans hF.col_one

theorem FrameValid.not_HFree {n : ℕ} {F : AnchorFrame n} {B : BinaryMatrix n}
    {r₀ r₁ c₀ c₁ : Fin n} (hF : FrameValid F B r₀ r₁ c₀ c₁)
    (hbody : PathPropagation.Body B r₀ r₁ c₀ c₁) : ¬ HFree B := by
  classical
  let ar : IncreasingMap 1 n := ⟨fun _ => F.rows.val 1, by
    intro i j hij; have hi := i.isLt; have hj := j.isLt
    have hij' : i.val < j.val := hij
    omega⟩
  let ac : IncreasingMap 1 n := ⟨fun _ => c₀, by
    intro i j hij; have hi := i.isLt; have hj := j.isLt
    have hij' : i.val < j.val := hij
    omega⟩
  let rr := appendTwoIncreasing ar r₀ r₁ (fun _ => hF.row_before 1) hF.row_lt
  let cc := appendTwoIncreasing ac c₁ (F.cols.val 0) (fun _ => hF.col_lt) (hF.col_after 0)
  have hmem : (rr,cc) ∈ orderedCopies B := by
    simp only [orderedCopies,Finset.mem_filter,Finset.mem_univ,true_and]
    intro i j
    have ha := hF.anchor
    have hr0 := hF.row_zero
    have hr1 := hF.row_one
    have hc0 := hF.col_zero
    have hc1 := hF.col_one
    rcases hbody with ⟨h00,h01,h10,h11⟩
    fin_cases i <;> fin_cases j <;>
      simp_all [rr,cc,ar,ac,appendTwoIncreasing,appendTwo,fixedH]
  exact Nat.ne_of_gt (Finset.card_pos.mpr ⟨(rr,cc),hmem⟩)

end
end OrderedRemoval.Crown
