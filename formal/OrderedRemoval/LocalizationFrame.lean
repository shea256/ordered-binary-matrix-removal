import OrderedRemoval.IndexedHost

namespace OrderedRemoval.Concrete

theorem isAnchor_iff_exists {h : ℕ} (x : Position h) :
    IsAnchor x ↔ ∃ t j u, x = .inl (t,j,u) := by
  rcases x with ⟨t,j,u⟩ | x <;> simp [IsAnchor]

theorem Copy.anchor_rows_iff {h : ℕ} (E : Copy h) (i : Fin 4) :
    IsAnchor (E.rows i) ↔ i.val < 2 := by
  rw [E.row_anchor_prefix, E.anchor_counts.1]

theorem Copy.first_col_anchor {h : ℕ} (E : Copy h) : IsAnchor (E.cols 0) := by
  rw [E.col_anchor_prefix]
  have hb := E.anchor_counts.2
  omega

theorem Copy.col_nonanchor {h : ℕ} (E : Copy h) (i : Fin 4) (hi : 2 ≤ i.val) :
    ¬ IsAnchor (E.cols i) := by
  rw [E.col_anchor_prefix]
  have hb := E.anchor_counts.2
  omega

theorem anchor_one_mode_groups {h : ℕ} (t u : Mode h) (j k : Fin 2)
    (x y : Fin (2^h)) (he : host (.inl (t,j,x)) (.inl (u,k,y)) = true) :
    t = u ∧ j ≠ k := by
  by_cases ht : t=u
  · simpa [host,ht] using he
  · simp [host,ht] at he

theorem variable_wrong_roles {h : ℕ} (t : Mode h) (r d : VariablePosition h)
    (hr : rowRole t 1 (.inr (.inl r))) (hd : colRole t 0 (.inr (.inl d))) : False := by
  have hk := kind_lt t
  interval_cases he : kind t <;> simp_all [rowRole,colRole]

theorem variable_role_orientation {h : ℕ} (t : Mode h) (j k : Fin 2)
    (r d : VariablePosition h) (hne : j ≠ k)
    (hr : rowRole t k (.inr (.inl r))) (hd : colRole t j (.inr (.inl d))) :
    j=1 ∧ k=0 := by
  fin_cases j <;> fin_cases k <;> simp_all
  exact (variable_wrong_roles t r d hr hd).elim

/-- The three anchor positions and the fixed zero determine a common mode B.
The first anchor row may belong to an earlier mode A. No localization is
assumed by this frame. -/
structure ModeFrame {h : ℕ} (E : Copy h) where
  A : Mode h
  B : Mode h
  group : Fin 2
  x : Fin (2^h)
  y : Fin (2^h)
  z : Fin (2^h)
  r : VariablePosition h
  d : VariablePosition h
  row0 : E.rows 0 = .inl (A,group,x)
  row1 : E.rows 1 = .inl (B,1,y)
  col0 : E.cols 0 = .inl (B,0,z)
  row2 : E.rows 2 = .inr (.inl r)
  col3 : E.cols 3 = .inr (.inl d)
  mode_le : modeRank A ≤ modeRank B
  r_role : rowRole B 0 (.inr (.inl r))
  d_role : colRole B 1 (.inr (.inl d))
  c_role : colRole A group (E.cols 2)

theorem Copy.mode_frame {h : ℕ} (E : Copy h) : Nonempty (ModeFrame E) := by
  obtain ⟨A,g,x,hr0⟩ := (isAnchor_iff_exists _).mp ((E.anchor_rows_iff 0).mpr (by decide))
  obtain ⟨B,j,y,hr1⟩ := (isAnchor_iff_exists _).mp ((E.anchor_rows_iff 1).mpr (by decide))
  obtain ⟨D,k,z,hc0⟩ := (isAnchor_iff_exists _).mp E.first_col_anchor
  obtain ⟨r,d,hr2,hc3⟩ := nonanchor_zero_variables (E.rows 2) (E.cols 3)
    (by rw [E.anchor_rows_iff]; decide) (E.col_nonanchor 3 (by decide))
    (E.entry_eq 2 3)
  have hBD := anchor_one_mode_groups B D j k y z (by
    rw [←hr1,←hc0,E.entry_eq]; rfl)
  obtain ⟨rfl,hjk⟩ := hBD
  have hrr : rowRole B k (.inr (.inl r)) := (anchor_col_role _ B k z (by simp [IsAnchor])).mp (by
    rw [←hr2,←hc0,E.entry_eq]; rfl)
  have hdr : colRole B j (.inr (.inl d)) := (anchor_row_role _ B j y (by simp [IsAnchor])).mp (by
    rw [←hr1,←hc3,E.entry_eq]; rfl)
  obtain ⟨rfl,rfl⟩ := variable_role_orientation B j k r d hjk hrr hdr
  have horder := E.rowIncreasing (show (0:Fin 4)<1 by decide)
  change OrderedHost.rowIndex h (E.rows 0) < OrderedHost.rowIndex h (E.rows 1) at horder
  rw [hr0,hr1,row_anchor_order_iff] at horder
  have hm : modeRank A ≤ modeRank B := by
    rcases horder with hh | ⟨rfl,_⟩
    · omega
    · exact le_rfl
  have hcr : colRole A g (E.cols 2) :=
    (anchor_row_role _ A g x (E.col_nonanchor 2 (by decide))).mp (by
      rw [←hr0,E.entry_eq]; rfl)
  exact ⟨⟨A,B,g,x,y,z,r,d,hr0,hr1,hc0,hr2,hc3,hm,hrr,hdr,hcr⟩⟩

end OrderedRemoval.Concrete
