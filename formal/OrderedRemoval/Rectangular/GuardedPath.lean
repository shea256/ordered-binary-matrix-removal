import OrderedRemoval.Rectangular.GuardedFrame
import OrderedRemoval.GuardedPath

namespace OrderedRemoval.Rectangular
noncomputable section
open GuardedPath GuardedPath.Selection
variable {n : ℕ}

/-- Explicit original-matrix conditions on a selected path. The frame validity
contains all required order comparisons and all 2-anchor signatures. -/
structure PathValid (P : Selection n) (A : BinaryMatrix n) (h : ℕ) : Prop where
  root_plus : A (P.xp 0) (P.yp 0) = true
  root_minus : A (P.xm 0) (P.ym 0) = false
  dummy_col : ∀ i, i ≤ h → A (P.xp i) P.yd = true ∧ A (P.xm i) P.yd = true
  dummy_row : ∀ i, i ≤ h → A P.xd (P.yp i) = true ∧ A P.xd (P.ym i) = true
  leaf_row : P.xp h = P.xm h
  leaf_col : P.yp h = P.ym h
  vertical_plus : ∀ i, i < h →
    FrameValid (P.vPlus i) A (P.xp (i + 1)) (P.xp i) P.yd (P.yp i)
  vertical_minus : ∀ i, i < h →
    FrameValid (P.vMinus i) A (P.xm i) (P.xm (i + 1)) P.yd (P.ym i)
  horizontal_plus : ∀ i, i < h →
    FrameValid (P.wPlus i) A (P.xp (i + 1)) P.xd (P.yp i) (P.yp (i + 1))
  horizontal_minus : ∀ i, i < h →
    FrameValid (P.wMinus i) A (P.xm (i + 1)) P.xd (P.ym (i + 1)) (P.ym i)

/-- If no guard cell was edited, every condition needed for path propagation
and exact anchor completion survives. -/
theorem PathValid.transfer {P : Selection n} {A B : BinaryMatrix n} {h : ℕ}
    (hv : PathValid P A h)
    (hag : ∀ rc ∈ P.guards h, A rc.1 rc.2 = B rc.1 rc.2) :
    PathValid P B h := by
  have hc : ∀ rc, P.CoreCell h rc → A rc.1 rc.2 = B rc.1 rc.2 := by
    intro rc hrc
    exact hag rc ((mem_guards P h rc).mpr (Or.inl hrc))
  have he : ∀ i, i < h → ∀ rc, P.EdgeCell i rc → A rc.1 rc.2 = B rc.1 rc.2 := by
    intro i hi rc hrc
    exact hag rc ((mem_guards P h rc).mpr (Or.inr ⟨i, hi, hrc⟩))
  refine ⟨?_, ?_, ?_, ?_, hv.leaf_row, hv.leaf_col, ?_, ?_, ?_, ?_⟩
  · exact (hc _ (Or.inl rfl)).symm.trans hv.root_plus
  · exact (hc _ (Or.inr (Or.inl rfl))).symm.trans hv.root_minus
  · intro i hi
    constructor
    · exact (hc _ (Or.inr (Or.inr ⟨i, hi, Or.inl rfl⟩))).symm.trans
        (hv.dummy_col i hi).1
    · exact (hc _ (Or.inr (Or.inr ⟨i, hi, Or.inr (Or.inl rfl)⟩))).symm.trans
        (hv.dummy_col i hi).2
  · intro i hi
    constructor
    · exact (hc _ (Or.inr (Or.inr ⟨i, hi, Or.inr (Or.inr (Or.inl rfl))⟩))).symm.trans
        (hv.dummy_row i hi).1
    · exact (hc _ (Or.inr (Or.inr ⟨i, hi, Or.inr (Or.inr (Or.inr rfl))⟩))).symm.trans
        (hv.dummy_row i hi).2
  · intro i hi
    exact (hv.vertical_plus i hi).transfer (fun rc hrc => he i hi rc (Or.inl hrc))
  · intro i hi
    exact (hv.vertical_minus i hi).transfer
      (fun rc hrc => he i hi rc (Or.inr (Or.inl hrc)))
  · intro i hi
    exact (hv.horizontal_plus i hi).transfer
      (fun rc hrc => he i hi rc (Or.inr (Or.inr (Or.inl hrc))))
  · intro i hi
    exact (hv.horizontal_minus i hi).transfer
      (fun rc hrc => he i hi rc (Or.inr (Or.inr (Or.inr hrc))))

/-- Every valid selected path gives a copy of the exact fixed H. -/
theorem PathValid.not_HFree {P : Selection n} {B : BinaryMatrix n} {h : ℕ}
    (hv : PathValid P B h) : ¬ HFree B := by
  obtain ⟨i, hi, hb⟩ := PathPropagation.exists_modeBody hv.root_plus hv.root_minus
    hv.dummy_col hv.dummy_row hv.leaf_row hv.leaf_col
  rcases hb with hb | hb | hb | hb
  · exact (hv.vertical_plus i hi).not_HFree hb
  · exact (hv.vertical_minus i hi).not_HFree hb
  · exact (hv.horizontal_plus i hi).not_HFree hb
  · exact (hv.horizontal_minus i hi).not_HFree hb

/-- Arbitrary edits outside the finite guard set cannot destroy all copies. -/
theorem not_HFree_of_agree {P : Selection n} {A B : BinaryMatrix n} {h : ℕ}
    (hv : PathValid P A h)
    (hag : ∀ rc ∈ P.guards h, A rc.1 rc.2 = B rc.1 rc.2) :
    ¬ HFree B :=
  (hv.transfer hag).not_HFree

/-- Every H-free repair must hit the guard set of each valid selected path.
This is a statement about all repairs, not just destroying original copies. -/
theorem repair_hits_guards {P : Selection n} {A B : BinaryMatrix n} {h : ℕ}
    (hv : PathValid P A h) (hfree : HFree B) :
    ∃ rc ∈ P.guards h, A rc.1 rc.2 ≠ B rc.1 rc.2 := by
  classical
  by_contra hn
  push Not at hn
  exact not_HFree_of_agree hv hn hfree


end
end OrderedRemoval.Rectangular
