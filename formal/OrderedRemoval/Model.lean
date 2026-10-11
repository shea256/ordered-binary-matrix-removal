/-
Adapted from OpenAI Model.lean, commit
fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb (Apache-2.0).
The ordered-copy and edit-distance definitions are unchanged; the fixed
pattern is the 4×4 candidate, with a two-group off-diagonal anchor.
-/
import Mathlib
import OrderedRemoval.AnchorClassification

namespace OrderedRemoval
noncomputable section

abbrev BinaryMatrix (n : ℕ) := Fin n → Fin n → Bool
abbrev IncreasingMap (k n : ℕ) := {f : Fin k → Fin n // StrictMono f}

def orderedCopies {k n : ℕ} (H : BinaryMatrix k) (A : BinaryMatrix n) :
    Finset (IncreasingMap k n × IncreasingMap k n) := by
  classical
  exact Finset.univ.filter (fun rc => ∀ i j, A (rc.1.val i) (rc.2.val j)=H i j)

def copyCount {k n : ℕ} (H : BinaryMatrix k) (A : BinaryMatrix n) : ℕ :=
  (orderedCopies H A).card

def HFree {k n : ℕ} (H : BinaryMatrix k) (A : BinaryMatrix n) : Prop :=
  copyCount H A=0

def hammingDistance {n : ℕ} (A B : BinaryMatrix n) : ℕ := by
  classical
  exact (Finset.univ.filter (fun rc : Fin n × Fin n => A rc.1 rc.2 ≠ B rc.1 rc.2)).card

def anchor2 (u v : Fin 2) : Bool := decide (u ≠ v)

def fixedH : BinaryMatrix 4 := fun u v =>
  if hu : u.val < 2 then
    if hv : v.val < 2 then anchor2 ⟨u.val,hu⟩ ⟨v.val,hv⟩
    else decide ((v.val=2 ∧ u.val=0) ∨ (v.val=3 ∧ u.val=1))
  else if v.val < 2 then
    decide ((u.val=2 ∧ v.val=0) ∨ (u.val=3 ∧ v.val=1))
  else decide (u.val=3 ∨ v.val=2)

/-- The pattern in the removal model is exactly the already-localized H4. -/
theorem fixedH_eq_H4 : fixedH = AnchorClassification.H4 := by decide

def fixedMinEdits {n : ℕ} (A : BinaryMatrix n) : ℕ := by
  classical
  exact (Finset.univ.image (fun B : BinaryMatrix n =>
    if HFree fixedH B then hammingDistance A B else n*n+1)).min' (by simp)

def fixedDistance {n : ℕ} (A : BinaryMatrix n) : ℝ :=
  (fixedMinEdits A : ℝ) / ((n : ℝ)^2)

end
end OrderedRemoval
