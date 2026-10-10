import Std

/-!
# Anchor-count classification from explicit structural hypotheses

The structure below describes the restriction of a host to one ordered H4
copy. Its assumptions express anchor order, off-mode zero entries, crown
exclusion, role-class comparability, and ordered laminar supports.

The theorem proves that these assumptions force exactly (2,2) or (2,1)
selected anchors. It does NOT prove that the concrete host satisfies all
the assumptions. That connection remains an explicit formalization boundary.
-/

namespace OrderedRemoval.AnchorClassification

def H4 (i j : Fin 4) : Bool :=
  match i.val, j.val with
  | 0, 1 | 0, 2 | 1, 0 | 1, 3 | 2, 0 | 2, 2 | 3, 1 | 3, 2 | 3, 3 => true
  | _, _ => false

theorem rows_distinct :
    ∀ i j : Fin 4, (∀ k : Fin 4, H4 i k = H4 j k) → i = j := by decide

theorem columns_distinct :
    ∀ i j : Fin 4, (∀ k : Fin 4, H4 k i = H4 k j) → i = j := by decide

def Cross (r s c d : Fin 4) : Prop :=
  H4 r c = false ∧ H4 r d = true ∧ H4 s c = true ∧ H4 s d = false

def Crown (r s t c d e : Fin 4) : Prop :=
  H4 r c = true ∧ H4 r d = false ∧ H4 r e = true ∧
  H4 s c = true ∧ H4 s d = true ∧ H4 s e = false ∧
  H4 t c = false ∧ H4 t d = true ∧ H4 t e = true

/-- Counts a,b are prefix lengths among four selected positions on each axis.
Ranks distinguish mode/group blocks, not individual twin positions.
Distinct H4 rows/columns exclude repeated twins before this certificate
can be extracted from a concrete copy. -/
structure Certificate (a b : Nat) where
  rows_le : a ≤ 4
  cols_le : b ≤ 4
  rowMode : Fin 4 → Nat
  colMode : Fin 4 → Nat
  rowGroup : Fin 4 → Fin 2
  colGroup : Fin 4 → Fin 2
  row_order : ∀ i j : Fin 4, i < j → j.val < a →
    2 * rowMode i + (rowGroup i).val < 2 * rowMode j + (rowGroup j).val
  col_order : ∀ i j : Fin 4, i < j → j.val < b →
    2 * colMode i + (colGroup i).val < 2 * colMode j + (colGroup j).val
  anchor_one : ∀ i j : Fin 4, i.val < a → j.val < b →
    H4 i j = true → rowMode i = colMode j
  crown_absent : ∀ r s t c d e : Fin 4,
    a ≤ r.val → a ≤ s.val → a ≤ t.val →
    b ≤ c.val → b ≤ d.val → b ≤ e.val → ¬ Crown r s t c d e
  row_support_comparable : ∀ k r s c d : Fin 4,
    k.val < b → a ≤ r.val → a ≤ s.val → b ≤ c.val → b ≤ d.val →
    H4 r k = true → H4 s k = true → ¬ Cross r s c d
  col_support_comparable : ∀ k r s c d : Fin 4,
    k.val < a → a ≤ r.val → a ≤ s.val → b ≤ c.val → b ≤ d.val →
    H4 k c = true → H4 k d = true → ¬ Cross r s c d
  no_backward_row_containment : ∀ r s c d : Fin 4,
    r < s → s.val < a → b ≤ c.val → b ≤ d.val →
    ¬ (H4 r c = true ∧ H4 r d = true ∧ H4 s c = false ∧ H4 s d = true)
  no_backward_col_containment : ∀ c d r s : Fin 4,
    c < d → d.val < b → a ≤ r.val → a ≤ s.val →
    ¬ (H4 r c = true ∧ H4 s c = true ∧ H4 r d = false ∧ H4 s d = true)

theorem balanced_counts {a b : Nat} (cert : Certificate a b)
    (ha : 2 ≤ a) (hb : 2 ≤ b) : a = 2 ∧ b = 2 := by
  have hr := cert.row_order 0 1 (by decide) (by omega)
  have hc := cert.col_order 0 1 (by decide) (by omega)
  have hone01 := cert.anchor_one 0 1 (by omega) (by omega) (by decide)
  have hone10 := cert.anchor_one 1 0 (by omega) (by omega) (by decide)
  have rg0 := (cert.rowGroup 0).isLt
  have rg1 := (cert.rowGroup 1).isLt
  have cg0 := (cert.colGroup 0).isLt
  have cg1 := (cert.colGroup 1).isLt
  have hm : cert.rowMode 0 = cert.rowMode 1 ∧
      cert.rowMode 0 = cert.colMode 0 ∧
      (cert.rowGroup 1).val = 1 ∧ (cert.colGroup 1).val = 1 := by omega
  have hmaxa : a ≤ 2 := by
    apply Nat.le_of_not_gt
    intro hx
    have hr2 := cert.row_order 1 2 (by decide) (by omega)
    have hone20 := cert.anchor_one 2 0 (by omega) (by omega) (by decide)
    have rg2 := (cert.rowGroup 2).isLt
    omega
  have hmaxb : b ≤ 2 := by
    apply Nat.le_of_not_gt
    intro hx
    have hc2 := cert.col_order 1 2 (by decide) (by omega)
    have hone02 := cert.anchor_one 0 2 (by omega) (by omega) (by decide)
    have cg2 := (cert.colGroup 2).isLt
    omega
  omega

/-- All 25 possible prefix-count pairs are covered by the structural argument. -/
theorem anchor_counts {a b : Nat} (cert : Certificate a b) :
    a = 2 ∧ (b = 1 ∨ b = 2) := by
  have ha : 2 ≤ a := by
    apply Nat.le_of_not_gt
    intro hsmall
    by_cases hb0 : b = 0
    · have hno := cert.crown_absent 1 2 3 0 2 3
        (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
      exact hno (by unfold Crown; decide)
    by_cases hb2 : b ≤ 2
    · have hno := cert.row_support_comparable 0 1 2 2 3
        (by omega) (by omega) (by omega) (by omega) (by omega)
        (by decide) (by decide)
      exact hno (by unfold Cross; decide)
    · have hno := cert.no_backward_col_containment 0 2 1 2
        (by decide) (by omega) (by omega) (by omega)
      exact hno (by decide)
  by_cases hb : 2 ≤ b
  · obtain ⟨ha2, hb2⟩ := balanced_counts cert ha hb
    exact ⟨ha2, Or.inr hb2⟩
  have ha2 : a = 2 := by
    by_cases hlarge : 3 ≤ a
    · have hno := cert.no_backward_row_containment 0 2 1 2
        (by decide) (by omega) (by omega) (by omega)
      exact False.elim (hno (by decide))
    · omega
  have hb1 : b = 1 := by
    by_cases hb0 : b = 0
    · have hno := cert.col_support_comparable 1 3 2 0 3
        (by omega) (by omega) (by omega) (by omega) (by omega)
        (by decide) (by decide)
      exact False.elim (hno (by unfold Cross; decide))
    · omega
  exact ⟨ha2, Or.inl hb1⟩

end OrderedRemoval.AnchorClassification
