import OrderedRemoval.Rectangular.CopyStructure
import OrderedRemoval.Rectangular.OneAnchorArithmetic

namespace OrderedRemoval.Rectangular
open Concrete

/-- Any nonanchor column after a variable column is itself variable. -/
theorem Copy.column_variable_after {h : ℕ} (E : Copy h) (i j : Fin 4)
    (hij : i<j) (v : VariablePosition h) (hi : E.cols i=.inr (.inl v))
    (hj : ¬ IsAnchor (E.cols j)) : ∃ w : VariablePosition h, E.cols j=.inr (.inl w) := by
  rcases he : E.cols j with a | (w | d)
  · simp [he,IsAnchor] at hj
  · exact ⟨w,rfl⟩
  · have ho := E.colIncreasing hij
    change OrderedHost.columnIndex h (E.cols i)<OrderedHost.columnIndex h (E.cols j) at ho
    rw [hi,he] at ho
    exact (not_lt_of_gt (OrderedHost.column_dummy_lt_variable v d) ho).elim

theorem Copy.anchor_mode_strict {h : ℕ} (E : Copy h) (i j : Fin 3)
    (hij : i<j) (A B : Mode h) (g k : Fin 2) (x y : Fin (2^h))
    (hi : E.rows i=.inl (A,g,x)) (hj : E.rows j=.inl (B,k,y)) :
    modeRank A < modeRank B := by
  have ho := E.rowIncreasing hij
  change OrderedHost.rowIndex h (E.rows i)<OrderedHost.rowIndex h (E.rows j) at ho
  rw [hi,hj,row_anchor_order_iff] at ho
  rcases ho with ho | ⟨rfl,ho⟩
  · exact ho
  · exact ((ne_of_lt hij) (E.no_repeated_anchor_rows hi hj)).elim

theorem Copy.first_col_anchor {h : ℕ} (E : Copy h) : IsAnchor (E.cols 0) := by
  by_contra hc0
  have hc1 := E.cols_nonanchor 0 1 (by decide) hc0
  have hc2 := E.cols_nonanchor 0 2 (by decide) hc0
  have hc3 := E.cols_nonanchor 0 3 (by decide) hc0
  obtain ⟨A,g,x,hA⟩ := (Concrete.isAnchor_iff_exists _).mp E.first_row_anchor
  by_cases hr1 : IsAnchor (E.rows 1)
  · obtain ⟨B,k,y,hB⟩ := (Concrete.isAnchor_iff_exists _).mp hr1
    have ho := E.anchor_mode_strict 0 1 (by decide) A B g k x y hA hB
    by_cases hr2 : IsAnchor (E.rows 2)
    · obtain ⟨C,l,z,hC⟩ := (Concrete.isAnchor_iff_exists _).mp hr2
      rcases ha : E.cols 0 with u | (a | u)
      · simp [ha,IsAnchor] at hc0
      · obtain ⟨b,hb⟩ := E.column_variable_after 0 1 (by decide) a ha hc1
        obtain ⟨c,hc⟩ := E.column_variable_after 0 2 (by decide) a ha hc2
        obtain ⟨d,hd⟩ := E.column_variable_after 0 3 (by decide) a ha hc3
        apply crossing_no_anchor_bottom A B C a c d ho
        all_goals first
          | simpa [hA,hB,hC,ha,hb,hc,hd,host,fixedH] using E.entry_eq 0 0
          | simpa [hA,hB,hC,ha,hb,hc,hd,host,fixedH] using E.entry_eq 1 0
          | simpa [hA,hB,hC,ha,hb,hc,hd,host,fixedH] using E.entry_eq 0 2
          | simpa [hA,hB,hC,ha,hb,hc,hd,host,fixedH] using E.entry_eq 1 2
          | simpa [hA,hB,hC,ha,hb,hc,hd,host,fixedH] using E.entry_eq 0 3
          | simpa [hA,hB,hC,ha,hb,hc,hd,host,fixedH] using E.entry_eq 1 3
          | simpa [hA,hB,hC,ha,hb,hc,hd,host,fixedH] using E.entry_eq 2 2
          | simpa [hA,hB,hC,ha,hb,hc,hd,host,fixedH] using E.entry_eq 2 3
      · have hAk : 2≤kind A := by simpa [hA,ha,host,fixedH] using E.entry_eq 0 0
        have hBk : 2≤kind B := by simpa [hB,ha,host,fixedH] using E.entry_eq 1 0
        have hCk : kind C<2 := by simpa [hC,ha,host,fixedH] using E.entry_eq 2 0
        obtain ⟨b,hb⟩ : ∃ b : VariablePosition h, E.cols 1=.inr (.inl b) := by
          rcases hb : E.cols 1 with v | (b | v)
          · simp [hb,IsAnchor] at hc1
          · exact ⟨b,rfl⟩
          · have he := E.entry_eq 0 1
            simp [hA,hb,host,fixedH,hAk] at he
        obtain ⟨c,hc⟩ := E.column_variable_after 1 2 (by decide) b hb hc2
        obtain ⟨d,hd⟩ := E.column_variable_after 1 3 (by decide) b hb hc3
        apply dummy_crossing_no_anchor_bottom A B C c d b hAk hBk hCk
        all_goals first
          | simpa [hA,hB,hC,hb,hc,hd,host,fixedH] using E.entry_eq 0 2
          | simpa [hA,hB,hC,hb,hc,hd,host,fixedH] using E.entry_eq 1 2
          | simpa [hA,hB,hC,hb,hc,hd,host,fixedH] using E.entry_eq 0 3
          | simpa [hA,hB,hC,hb,hc,hd,host,fixedH] using E.entry_eq 1 3
          | simpa [hA,hB,hC,hb,hc,hd,host,fixedH] using E.entry_eq 0 1
          | simpa [hA,hB,hC,hb,hc,hd,host,fixedH] using E.entry_eq 1 1
          | simpa [hA,hB,hC,hb,hc,hd,host,fixedH] using E.entry_eq 2 2
          | simpa [hA,hB,hC,hb,hc,hd,host,fixedH] using E.entry_eq 2 3
          | simpa [hA,hB,hC,hb,hc,hd,host,fixedH] using E.entry_eq 2 1
    · obtain ⟨r,a,hr,ha⟩ := nonanchor_zero_variables _ _ hr2 hc0 (E.entry_eq 2 0)
      obtain ⟨b,hb⟩ := E.column_variable_after 0 1 (by decide) a ha hc1
      obtain ⟨c,hc⟩ := E.column_variable_after 0 2 (by decide) a ha hc2
      obtain ⟨d,hd⟩ := E.column_variable_after 0 3 (by decide) a ha hc3
      apply crossing_no_variable_bottom A B r a c d b ho
      all_goals first
        | simpa [hA,hB,hr,ha,hb,hc,hd,host,fixedH] using E.entry_eq 0 0
        | simpa [hA,hB,hr,ha,hb,hc,hd,host,fixedH] using E.entry_eq 1 0
        | simpa [hA,hB,hr,ha,hb,hc,hd,host,fixedH] using E.entry_eq 0 2
        | simpa [hA,hB,hr,ha,hb,hc,hd,host,fixedH] using E.entry_eq 1 2
        | simpa [hA,hB,hr,ha,hb,hc,hd,host,fixedH] using E.entry_eq 0 3
        | simpa [hA,hB,hr,ha,hb,hc,hd,host,fixedH] using E.entry_eq 1 3
        | simpa [hA,hB,hr,ha,hb,hc,hd,host,fixedH] using E.entry_eq 0 1
        | simpa [hA,hB,hr,ha,hb,hc,hd,host,fixedH] using E.entry_eq 1 1
        | simpa [hA,hB,hr,ha,hb,hc,hd,host,fixedH] using E.entry_eq 2 2
        | simpa [hA,hB,hr,ha,hb,hc,hd,host,fixedH] using E.entry_eq 2 3
        | simpa [hA,hB,hr,ha,hb,hc,hd,host,fixedH] using E.entry_eq 2 1
  · have hr2 := E.rows_nonanchor 1 2 (by decide) hr1
    obtain ⟨s,a,hs,ha⟩ := nonanchor_zero_variables _ _ hr2 hc0 (E.entry_eq 2 0)
    obtain ⟨r,d,hr,hd⟩ := nonanchor_zero_variables _ _ hr1 hc3 (E.entry_eq 1 3)
    obtain ⟨b,hb⟩ := E.column_variable_after 0 1 (by decide) a ha hc1
    obtain ⟨c,hc⟩ := E.column_variable_after 0 2 (by decide) a ha hc2
    apply one_anchor_no_anchor_columns A r s a b c d
    all_goals first
      | simpa [hA,hr,hs,ha,hb,hc,hd,host,fixedH] using E.entry_eq 0 0
      | simpa [hA,hr,hs,ha,hb,hc,hd,host,fixedH] using E.entry_eq 0 1
      | simpa [hA,hr,hs,ha,hb,hc,hd,host,fixedH] using E.entry_eq 0 2
      | simpa [hA,hr,hs,ha,hb,hc,hd,host,fixedH] using E.entry_eq 0 3
      | simpa [hA,hr,hs,ha,hb,hc,hd,host,fixedH] using E.entry_eq 1 0
      | simpa [hA,hr,hs,ha,hb,hc,hd,host,fixedH] using E.entry_eq 1 1
      | simpa [hA,hr,hs,ha,hb,hc,hd,host,fixedH] using E.entry_eq 1 2
      | simpa [hA,hr,hs,ha,hb,hc,hd,host,fixedH] using E.entry_eq 1 3
      | simpa [hA,hr,hs,ha,hb,hc,hd,host,fixedH] using E.entry_eq 2 0
      | simpa [hA,hr,hs,ha,hb,hc,hd,host,fixedH] using E.entry_eq 2 1
      | simpa [hA,hr,hs,ha,hb,hc,hd,host,fixedH] using E.entry_eq 2 2
      | simpa [hA,hr,hs,ha,hb,hc,hd,host,fixedH] using E.entry_eq 2 3
      | have ho := E.colIncreasing (show (0:Fin 4)<3 by decide)
        change OrderedHost.columnIndex h (E.cols 0)<OrderedHost.columnIndex h (E.cols 3) at ho
        rwa [ha,hd,OrderedHost.columnIndex_variable_lt_iff] at ho
      | have ho := E.rowIncreasing (show (1:Fin 3)<2 by decide)
        change OrderedHost.rowIndex h (E.rows 1)<OrderedHost.rowIndex h (E.rows 2) at ho
        rwa [hr,hs,OrderedHost.rowIndex_variable_lt_iff] at ho

end OrderedRemoval.Rectangular
