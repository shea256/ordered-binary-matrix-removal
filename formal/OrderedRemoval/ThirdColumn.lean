import OrderedRemoval.LocalizationArithmetic

namespace OrderedRemoval.Concrete
set_option maxHeartbeats 2000000

theorem ModeFrame.balanced_alignment {h : ℕ} {E : Copy h} (F : ModeFrame E)
    (ha : IsAnchor (E.cols 1)) :
    F.A=F.B ∧ F.group=0 ∧ ∃ u, E.cols 1=.inl (F.B,1,u) := by
  obtain ⟨C,k,w,hc1⟩ := (isAnchor_iff_exists _).mp ha
  have hAC := anchor_one_mode_groups F.A C F.group k F.x w (by
    rw [←F.row0,←hc1,E.entry_eq]; rfl)
  obtain ⟨hAC,hgk⟩ := hAC
  subst C
  have hcorder := E.colIncreasing (show (0:Fin 4)<1 by decide)
  change OrderedHost.columnIndex h (E.cols 0)<OrderedHost.columnIndex h (E.cols 1) at hcorder
  rw [F.col0,hc1,col_anchor_order_iff] at hcorder
  have hm : modeRank F.B ≤ modeRank F.A := by
    rcases hcorder with hh | ⟨hh,_⟩
    · omega
    · rw [hh]
  have hAB : F.A=F.B := modeRank_injective h (Nat.le_antisymm F.mode_le hm)
  have hrow := E.row_rank_strict 0 1 (by decide) ((E.anchor_rows_iff 1).mpr (by decide))
  rw [F.row0,F.row1] at hrow
  simp only [anchorRank,anchorGroup,hAB] at hrow
  have hg : F.group=0 := by apply Fin.ext; change F.group.val=0; omega
  have hk : k=1 := by fin_cases k <;> simp_all
  exact ⟨hAB,hg,w,by rw [hc1,hAB,hk]⟩

theorem vertical_zero_impossible {h : ℕ} (B : Mode h) (r s d : VariablePosition h)
    (hk : kind B<2)
    (hr : rowRole B 0 (.inr (.inl r))) (hs : rowRole B 1 (.inr (.inl s)))
    (hd : colRole B 1 (.inr (.inl d)))
    (hz : variableEntry r d=false) (hone : variableEntry s d=true)
    (ho : TreePositions.rowKey h r < TreePositions.rowKey h s) : False := by
  have hp := level_pos B
  have hl := level_le B
  have hrv := r.1.isLt
  have hsv := s.1.isLt
  have hdv := d.1.isLt
  have hzero : ¬ variableEntry r d=true := by simp [hz]
  rw [variableEntry_true_iff] at hzero hone
  interval_cases he : kind B
  · simp [rowRole,colRole,he] at hr hs hd
    have hr' : AtLevel ((level B-1)+1) true r := by simpa [Nat.sub_add_cancel hp] using hr
    have hord := (row_plus_lt_iff hr' hs).mp ho
    simp [AtLevel,depth,plus] at hr hs hd
    omega
  · simp [rowRole,colRole,he] at hr hs hd
    have hs' : AtLevel ((level B-1)+1) false s := by simpa [Nat.sub_add_cancel hp] using hs
    have hord := (row_minus_lt_iff hs' hr).mp ho
    simp [AtLevel,depth,plus] at hr hs hd
    omega

/-- A dummy third column would force the balanced vertical case, which the
concrete row order and the two right-column entries rule out. -/
theorem ModeFrame.third_column_variable {h : ℕ} {E : Copy h} (F : ModeFrame E) :
    ∃ c : VariablePosition h, E.cols 2=.inr (.inl c) := by
  have hn := E.col_nonanchor 2 (by decide)
  rcases hec : E.cols 2 with a | (c | u)
  · simp [hec,IsAnchor] at hn
  · exact ⟨c,rfl⟩
  · have ha : IsAnchor (E.cols 1) := by
      by_contra hn1
      obtain ⟨r',c',hr',hc'⟩ := nonanchor_zero_variables (E.rows 2) (E.cols 1)
        (by rw [E.anchor_rows_iff]; decide) hn1 (E.entry_eq 2 1)
      have hord := E.colIncreasing (show (1:Fin 4)<2 by decide)
      change OrderedHost.columnIndex h (E.cols 1)<OrderedHost.columnIndex h (E.cols 2) at hord
      rw [hc',hec] at hord
      exact (not_lt_of_gt (OrderedHost.column_dummy_lt_variable c' u)) hord
    obtain ⟨hAB,hg,w,hc1⟩ := F.balanced_alignment ha
    have hcr := F.c_role
    rw [hAB,hg,hec] at hcr
    have hk : kind F.B<2 := by simpa [colRole] using hcr
    have hnon : ¬ IsAnchor (E.rows 3) := by rw [E.anchor_rows_iff]; decide
    have hsr : rowRole F.B 1 (E.rows 3) :=
      (anchor_col_role _ F.B 1 w hnon).mp (by rw [←hc1,E.entry_eq]; rfl)
    rcases hes : E.rows 3 with a | (s | v)
    · simp [hes,IsAnchor] at hnon
    · rw [hes] at hsr
      have hz : variableEntry F.r F.d=false := by
        rw [←host_variable_variable,←F.row2,←F.col3,E.entry_eq]; rfl
      have hone : variableEntry s F.d=true := by
        rw [←host_variable_variable,←hes,←F.col3,E.entry_eq]; rfl
      have ho := E.rowIncreasing (show (2:Fin 4)<3 by decide)
      change OrderedHost.rowIndex h (E.rows 2)<OrderedHost.rowIndex h (E.rows 3) at ho
      rw [F.row2,hes,OrderedHost.rowIndex_variable_lt_iff] at ho
      exact (vertical_zero_impossible F.B F.r s F.d hk F.r_role hsr F.d_role hz hone ho).elim
    · simp [hes,rowRole] at hsr
      omega

end OrderedRemoval.Concrete
