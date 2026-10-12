import OrderedRemoval.HostSampledSelection

namespace OrderedRemoval.Crown.SampledSelection
noncomputable section
open Concrete HostSampledPath Concrete.SampledSelection

structure AxisConditions {h n : ℕ} (er ec : Position h ≃ Fin n) : Prop where
  anchor_rows : ∀ (t : Mode h) (a : Fin (2 ^ h)),
    StrictMono (fun u : Fin 2 => er (.inl (t, u, a)))
  anchor_cols : ∀ (t : Mode h) (a : Fin (2 ^ h)),
    StrictMono (fun u : Fin 2 => ec (.inl (t, u, a)))
  anchor_before_rows : ∀ (t : Mode h) (u : Fin 2) (a : Fin (2 ^ h))
    (x : VariablePosition h ⊕ Fin (2 ^ h)), er (.inl (t, u, a)) < er (.inr x)
  nonanchor_before_cols : ∀ (t : Mode h) (u : Fin 2) (a : Fin (2 ^ h))
    (x : VariablePosition h ⊕ Fin (2 ^ h)), ec (.inr x) < ec (.inl (t, u, a))
  variable_before_dummy : ∀ (x : VariablePosition h) (a : Fin (2 ^ h)),
    er (.inr (.inl x)) < er (dummy h a)
  dummy_before_variable : ∀ (x : VariablePosition h) (a : Fin (2 ^ h)),
    ec (dummy h a) < ec (.inr (.inl x))
  row_plus : ∀ (i : Fin h) (z u : Fin (2 ^ h)),
    er (position h (i.val + 1) (by omega) true z u) <
      er (position h i.val (by omega) true z u)
  row_minus : ∀ (i : Fin h) (z u : Fin (2 ^ h)),
    er (position h i.val (by omega) false z u) <
      er (position h (i.val + 1) (by omega) false z u)
  col_plus : ∀ (i : Fin h) (z u : Fin (2 ^ h)),
    ec (position h i.val (by omega) true z u) <
      ec (position h (i.val + 1) (by omega) true z u)
  col_minus : ∀ (i : Fin h) (z u : Fin (2 ^ h)),
    ec (position h (i.val + 1) (by omega) false z u) <
      ec (position h i.val (by omega) false z u)

/-- The selected anchor representatives use the same row/column seed in every
anchor group. This correlation does not affect the cellwise sampling proof. -/
def frame {h n : ℕ} (er ec : Position h ≃ Fin n)
    (ha : AxisConditions er ec) (t : Mode h) (u v : Fin (2 ^ h)) :
    GuardedPath.AnchorFrame n :=
  SelectedAnchor.frame er ec t (fun _ => u) (fun _ => v)
    (ha.anchor_rows t u) (ha.anchor_cols t v)

/-- The actual selected path and four anchor frames at each edge. -/
def selection {h n : ℕ} (hh : 1 ≤ h) (er ec : Position h ≃ Fin n)
    (ha : AxisConditions er ec) (z u v : Fin (2 ^ h)) : GuardedPath.Selection n where
  xp i := er (path h i true z u)
  xm i := er (path h i false z u)
  yp i := ec (path h i true z v)
  ym i := ec (path h i false z v)
  xd := er (dummy h u)
  yd := ec (dummy h v)
  vPlus i := frame er ec ha (vertical (edge hh i) true) u v
  vMinus i := frame er ec ha (vertical (edge hh i) false) u v
  wPlus i := frame er ec ha (horizontalMode hh z i true) u v
  wMinus i := frame er ec ha (horizontalMode hh z i false) u v


end
end OrderedRemoval.Crown.SampledSelection
