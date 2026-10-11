import OrderedRemoval.Rectangular.Host
import OrderedRemoval.Rectangular.GuardedPath
import OrderedRemoval.HostSampledSelection

namespace OrderedRemoval.Rectangular
noncomputable section
open Concrete HostSampledPath

def matrix {h n : ℕ} (er ec : Position h ≃ Fin n) : BinaryMatrix n :=
  fun r c => host (er.symm r) (ec.symm c)

@[simp] theorem matrix_apply {h n : ℕ} (er ec : Position h ≃ Fin n)
    (r c : Position h) : matrix er ec (er r) (ec c) = host r c := by
  simp [matrix]

namespace SampledSelection
open Concrete.SampledSelection

theorem frame_valid {h n : ℕ} (er ec : Position h ≃ Fin n)
    (ha : AxisConditions er ec) (t : Mode h) (u v : Fin (2 ^ h))
    (r₀ r₁ c₀ c₁ : Position h)
    (hr₀ : rowRole t 0 r₀) (hr₁ : rowRole t 1 r₁)
    (hc₀ : colRole t 0 c₀) (hc₁ : colRole t 1 c₁)
    (hrs : er r₀ < er r₁) (hcs : ec c₀ < ec c₁) :
    FrameValid (frame er ec ha t u v) (matrix er ec)
      (er r₀) (er r₁) (ec c₀) (ec c₁) := by
  refine ⟨?_, hrs, ?_, hcs, ?_, ?_, ?_, ?_, ?_⟩
  · intro j
    cases r₀ with
    | inl a => simp [rowRole] at hr₀
    | inr x => exact ha.anchor_before_rows t j u x
  · intro j
    cases c₀ with
    | inl a => simp [colRole] at hc₀
    | inr x => exact ha.anchor_before_cols t j v x
  · intro j
    simp [frame, SelectedAnchor.frame, matrix, host]
  · intro j
    have hn : ¬ rowRole t 1 r₀ := fun h₁ => rowRole_disjoint t r₀ ⟨hr₀,h₁⟩
    cases r₀ with
    | inl a => simp [rowRole] at hr₀
    | inr r => fin_cases j <;>
        simp_all [frame, SelectedAnchor.frame, matrix, host]
  · intro j
    have hn : ¬ rowRole t 0 r₁ := fun h₀ => rowRole_disjoint t r₁ ⟨h₀,hr₁⟩
    cases r₁ with
    | inl a => simp [rowRole] at hr₁
    | inr r => fin_cases j <;>
        simp_all [frame, SelectedAnchor.frame, matrix, host]
  · simpa [frame,SelectedAnchor.frame] using
      (matrix_apply er ec (.inl (t,1,u)) c₀).trans (top_on_role t 0 c₀ hc₀ 1 u)
  · simpa [frame,SelectedAnchor.frame] using
      (matrix_apply er ec (.inl (t,1,u)) c₁).trans (top_on_role t 1 c₁ hc₁ 1 u)

theorem vertical_plus_valid {h n : ℕ} (er ec : Position h ≃ Fin n)
    (ha : AxisConditions er ec) (i : Fin h) (z u v : Fin (2 ^ h)) :
    FrameValid (frame er ec ha (vertical i true) u v) (matrix er ec)
      (er (position h (i.val + 1) (by omega) true z u))
      (er (position h i.val (by omega) true z u))
      (ec (dummy h v)) (ec (position h i.val (by omega) true z v)) := by
  apply frame_valid er ec ha
  · exact vertical_plus_row_first i z u
  · exact vertical_plus_row_second i z u
  · exact vertical_col_first i true v
  · exact vertical_col_second i true z v
  · exact ha.row_plus i z u
  · exact ha.dummy_before_variable _ v

theorem vertical_minus_valid {h n : ℕ} (er ec : Position h ≃ Fin n)
    (ha : AxisConditions er ec) (i : Fin h) (z u v : Fin (2 ^ h)) :
    FrameValid (frame er ec ha (vertical i false) u v) (matrix er ec)
      (er (position h i.val (by omega) false z u))
      (er (position h (i.val + 1) (by omega) false z u))
      (ec (dummy h v)) (ec (position h i.val (by omega) false z v)) := by
  apply frame_valid er ec ha
  · exact vertical_minus_row_first i z u
  · exact vertical_minus_row_second i z u
  · exact vertical_col_first i false v
  · exact vertical_col_second i false z v
  · exact ha.row_minus i z u
  · exact ha.dummy_before_variable _ v

theorem horizontal_plus_valid {h n : ℕ} (er ec : Position h ≃ Fin n)
    (ha : AxisConditions er ec) (i : Fin h) (z u v : Fin (2 ^ h)) :
    FrameValid (frame er ec ha
      (horizontal i true (parity (z.val / SampledPath.blockSize h (i.val + 1)))) u v)
      (matrix er ec)
      (er (position h (i.val + 1) (by omega) true z u)) (er (dummy h u))
      (ec (position h i.val (by omega) true z v))
      (ec (position h (i.val + 1) (by omega) true z v)) := by
  apply frame_valid er ec ha
  · exact horizontal_row_first i true z u
  · exact horizontal_row_second i true _ u
  · exact horizontal_plus_col_first i _ z v
  · exact horizontal_plus_col_second i z v
  · exact ha.variable_before_dummy _ u
  · exact ha.col_plus i z v

theorem horizontal_minus_valid {h n : ℕ} (er ec : Position h ≃ Fin n)
    (ha : AxisConditions er ec) (i : Fin h) (z u v : Fin (2 ^ h)) :
    FrameValid (frame er ec ha
      (horizontal i false (parity (z.val / SampledPath.blockSize h (i.val + 1)))) u v)
      (matrix er ec)
      (er (position h (i.val + 1) (by omega) false z u)) (er (dummy h u))
      (ec (position h (i.val + 1) (by omega) false z v))
      (ec (position h i.val (by omega) false z v)) := by
  apply frame_valid er ec ha
  · exact horizontal_row_first i false z u
  · exact horizontal_row_second i false _ u
  · exact horizontal_minus_col_first i z v
  · exact horizontal_minus_col_second i _ z v
  · exact ha.variable_before_dummy _ u
  · exact ha.col_minus i z v

/-- Every concrete three-seed selection satisfies all guarded-path hypotheses.
Only the axis order laws were assumed; the entire original-matrix certificate
is derived from the exact host entries and the sampled common-leaf path. -/
theorem selection_valid {h n : ℕ} (hh : 1 ≤ h) (er ec : Position h ≃ Fin n)
    (ha : AxisConditions er ec) (z u v : Fin (2 ^ h)) :
    PathValid (selection hh er ec ha z u v) (matrix er ec) h := by
  constructor
  · simp only [selection, matrix_apply,
      path_of_le (Nat.zero_le h)]
    exact variableEntry_root_plus_of_atLevel hh _ _
      (sample_atLevel h 0 (Nat.zero_le h) true z u)
      (sample_atLevel h 0 (Nat.zero_le h) true z v)
  · simp only [selection, matrix_apply,
      path_of_le (Nat.zero_le h)]
    exact variableEntry_root_minus_of_atLevel hh _ _
      (sample_atLevel h 0 (Nat.zero_le h) false z u)
      (sample_atLevel h 0 (Nat.zero_le h) false z v)
  · intro i hi
    simp [selection, matrix_apply, path, position, dummy, host]
  · intro i hi
    simp [selection, matrix_apply, path, position, dummy, host]
  · simp only [selection, path_of_le (Nat.le_refl h)]
    exact congrArg er (position_shared_leaf h true false z u u)
  · simp only [selection, path_of_le (Nat.le_refl h)]
    exact congrArg ec (position_shared_leaf h true false z v v)
  · intro i hi
    simpa only [selection, edge_of_lt hh hi, path_of_le hi.le,
      path_of_le (show i + 1 ≤ h by omega)] using
      vertical_plus_valid er ec ha ⟨i, hi⟩ z u v
  · intro i hi
    simpa only [selection, edge_of_lt hh hi, path_of_le hi.le,
      path_of_le (show i + 1 ≤ h by omega)] using
      vertical_minus_valid er ec ha ⟨i, hi⟩ z u v
  · intro i hi
    simpa only [selection, horizontalMode, edge_of_lt hh hi, path_of_le hi.le,
      path_of_le (show i + 1 ≤ h by omega)] using
      horizontal_plus_valid er ec ha ⟨i, hi⟩ z u v
  · intro i hi
    simpa only [selection, horizontalMode, edge_of_lt hh hi, path_of_le hi.le,
      path_of_le (show i + 1 ≤ h by omega)] using
      horizontal_minus_valid er ec ha ⟨i, hi⟩ z u v


end SampledSelection
end
end OrderedRemoval.Rectangular
