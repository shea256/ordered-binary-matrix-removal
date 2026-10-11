import OrderedRemoval.ZeroLocalization

namespace OrderedRemoval.Concrete

theorem ModeFrame.localization_data {h : ℕ} {E : Copy h} (F : ModeFrame E)
    (c : VariablePosition h) (hc : E.cols 2=.inr (.inl c)) :
    F.r.1.val=2*h ∧ F.d.1.val+1=2*h ∧ node F.d=node F.r/2 ∧
      (c.1.val=2*h ∨ c.1.val+2=2*h) := by
  have hcr := F.c_role
  rw [hc] at hcr
  have hone : variableEntry F.r c=true := by
    rw [←host_variable_variable,←F.row2,←hc,E.entry_eq]; rfl
  have hz : variableEntry F.r F.d=false := by
    rw [←host_variable_variable,←F.row2,←F.col3,E.entry_eq]; rfl
  have ho := E.colIncreasing (show (2:Fin 4)<3 by decide)
  change OrderedHost.columnIndex h (E.cols 2)<OrderedHost.columnIndex h (E.cols 3) at ho
  rw [hc,F.col3,OrderedHost.columnIndex_variable_lt_iff] at ho
  exact mode_zero_localization F.A F.B F.group F.r c F.d
    F.mode_le F.r_role F.d_role hcr hone hz ho

theorem ModeFrame.minus_mode {h : ℕ} {E : Copy h} (F : ModeFrame E)
    (hrl : F.r.1.val=2*h) (hdl : F.d.1.val+1=2*h) : 4 ≤ kind F.B := by
  have hr := F.r_role
  have hd := F.d_role
  have hl := level_le F.B
  have hp := level_pos F.B
  have hrv := F.r.1.isLt
  have hdv := F.d.1.isLt
  by_contra hn
  have hk : kind F.B<4 := by omega
  interval_cases he : kind F.B <;> simp [rowRole,colRole,he,AtLevel,depth,plus] at hr hd <;> omega

/-- The last selected row is dummy, including the unbalanced-anchor copies. -/
theorem Copy.last_row_dummy {h : ℕ} (E : Copy h) :
    ∃ u : Fin (2^h), E.rows 3=.inr (.inr u) := by
  obtain ⟨F⟩ := E.mode_frame
  obtain ⟨c,hc⟩ := F.third_column_variable
  obtain ⟨hrl,hdl,hn,hcl⟩ := F.localization_data c hc
  have hB := F.minus_mode hrl hdl
  have hsna : ¬ IsAnchor (E.rows 3) := by rw [E.anchor_rows_iff]; decide
  rcases hes : E.rows 3 with a | (s | u)
  · simp [hes,IsAnchor] at hsna
  · exfalso
    by_cases ha : IsAnchor (E.cols 1)
    · obtain ⟨_,_,w,hc1⟩ := F.balanced_alignment ha
      have hsr : rowRole F.B 1 (.inr (.inl s)) :=
        (anchor_col_role _ F.B 1 w (by simp [IsAnchor])).mp (by
          rw [←hes,←hc1,E.entry_eq]; rfl)
      have hk0 : kind F.B≠0 := by omega
      have hk1 : kind F.B≠1 := by omega
      simp [rowRole,hk0,hk1] at hsr
    · obtain ⟨r',q,_,hc1⟩ := nonanchor_zero_variables (E.rows 2) (E.cols 1)
        (by rw [E.anchor_rows_iff]; decide) ha (E.entry_eq 2 1)
      have hqr : colRole F.A F.group (.inr (.inl q)) :=
        (anchor_row_role _ F.A F.group F.x (by simp [IsAnchor])).mp (by
          rw [←F.row0,←hc1,E.entry_eq]; rfl)
      have hcr := F.c_role
      rw [hc] at hcr
      have hcls : q.1.val=c.1.val := colRole_same_class hqr hcr
      have hsq : variableEntry s q=true := by
        rw [←host_variable_variable,←hes,←hc1,E.entry_eq]; rfl
      have hsd : variableEntry s F.d=true := by
        rw [←host_variable_variable,←hes,←F.col3,E.entry_eq]; rfl
      have hshapeq := variableEntry_class_shape hsq
      have hshaped := variableEntry_class_shape hsd
      have hsmax := s.1.isLt
      have hsl : s.1.val=2*h := by omega
      have hord := E.rowIncreasing (show (2:Fin 4)<3 by decide)
      change OrderedHost.rowIndex h (E.rows 2)<OrderedHost.rowIndex h (E.rows 3) at hord
      rw [F.row2,hes,OrderedHost.rowIndex_variable_lt_iff] at hord
      have hnodes := row_leaf_node_lt F.r s hrl hsl hord
      have hsame : F.r.1=s.1 := Fin.ext (hrl.trans hsl.symm)
      have hone := variableEntry_row_antimono F.r s q hsame (Nat.le_of_lt hnodes) hsq
      have hzero : variableEntry F.r q=false := by
        rw [←host_variable_variable,←F.row2,←hc1,E.entry_eq]; rfl
      simp [hzero] at hone
  · exact ⟨u,rfl⟩

end OrderedRemoval.Concrete
