import OrderedRemoval.Crown.CopyStructure

namespace OrderedRemoval.Crown
open Concrete

theorem Copy.variable_columns_order {h : ℕ} (E : Copy h) {i j : Fin 3}
    {a b : VariablePosition h} (hij : i<j)
    (hi : E.cols i=.inr (.inl a)) (hj : E.cols j=.inr (.inl b)) :
    TreePositions.columnKey h a < TreePositions.columnKey h b := by
  have ho := E.colIncreasing hij
  change OrderedHost.columnIndex h (E.cols i)<OrderedHost.columnIndex h (E.cols j) at ho
  rwa [hi,hj,OrderedHost.columnIndex_variable_lt_iff] at ho

theorem Copy.variable_rows_order {h : ℕ} (E : Copy h) {i j : Fin 3}
    {a b : VariablePosition h} (hij : i<j)
    (hi : E.rows i=.inr (.inl a)) (hj : E.rows j=.inr (.inl b)) :
    TreePositions.rowKey h a < TreePositions.rowKey h b := by
  have ho := E.rowIncreasing hij
  change OrderedHost.rowIndex h (E.rows i)<OrderedHost.rowIndex h (E.rows j) at ho
  rwa [hi,hj,OrderedHost.rowIndex_variable_lt_iff] at ho

theorem Copy.column_variable_after {h : ℕ} (E : Copy h) (i j : Fin 3)
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

theorem vertical_not_before_horizontal {h : ℕ} (A B : Mode h)
    (hA : kind A<2) (hB : 2≤kind B) : ¬ modeRank A < modeRank B := by
  have hAl := level_le A
  have hBl := level_le B
  have hAp := level_pos A
  have hBp := level_pos B
  have hAk := kind_lt A
  have hBk := kind_lt B
  unfold modeRank Rectangular.modeRank
  split_ifs <;> omega

theorem Copy.last_col_anchor {h : ℕ} (E : Copy h) : IsAnchor (E.cols 2) := by
  by_contra hc2
  have hc0 := E.cols_nonanchor 0 2 (by decide) hc2
  have hc1 := E.cols_nonanchor 1 2 (by decide) hc2
  obtain ⟨A,g,x,hA⟩ := (Concrete.isAnchor_iff_exists _).mp E.first_row_anchor
  by_cases hr1 : IsAnchor (E.rows 1)
  · obtain ⟨B,k,y,hB⟩ := (Concrete.isAnchor_iff_exists _).mp hr1
    have ho := E.anchor_mode_strict 0 1 (by decide) A B g k x y hA hB
    obtain ⟨a,ha⟩ : ∃ a : VariablePosition h, E.cols 0=.inr (.inl a) := by
      rcases ha : E.cols 0 with t | (a | d)
      · simp [ha,IsAnchor] at hc0
      · exact ⟨a,rfl⟩
      · have hkA : kind A<2 := by simpa [hA,ha,host,fixedH] using E.entry_eq 0 0
        have hkB : 2≤kind B := by simpa [hB,ha,host,fixedH] using E.entry_eq 1 0
        exact (vertical_not_before_horizontal A B hkA hkB ho).elim
    obtain ⟨b,hb⟩ := E.column_variable_after 0 1 (by decide) a ha hc1
    obtain ⟨c,hc⟩ := E.column_variable_after 0 2 (by decide) a ha hc2
    have hac : topVariable A c := by simpa [hA,hc,host,fixedH] using E.entry_eq 0 2
    have hbc : topVariable B c := by simpa [hB,hc,host,fixedH] using E.entry_eq 1 2
    have haa : ¬topVariable A a := by simpa [hA,ha,host,fixedH] using E.entry_eq 0 0
    have hba : topVariable B a := by simpa [hB,ha,host,fixedH] using E.entry_eq 1 0
    have hab : topVariable A b := by simpa [hA,hb,host,fixedH] using E.entry_eq 0 1
    have hbb : ¬topVariable B b := by simpa [hB,hb,host,fixedH] using E.entry_eq 1 1
    by_cases hr2 : IsAnchor (E.rows 2)
    · obtain ⟨C,l,z,hC⟩ := (Concrete.isAnchor_iff_exists _).mp hr2
      apply Rectangular.crossing_no_anchor_bottom A B C c a b ho hac hbc haa hba hab hbb
      · simpa [hC,ha,host,fixedH] using E.entry_eq 2 0
      · simpa [hC,hb,host,fixedH] using E.entry_eq 2 1
    · obtain ⟨r,c',hr,hc'⟩ := nonanchor_zero_variables _ _ hr2 hc2 (E.entry_eq 2 2)
      apply crossing_no_variable_bottom A B r a b c ho hac hbc haa hba hab hbb
      · simpa [hr,ha,host,fixedH] using E.entry_eq 2 0
      · simpa [hr,hb,host,fixedH] using E.entry_eq 2 1
      · simpa [hr,hc,host,fixedH] using E.entry_eq 2 2
      · exact E.variable_columns_order (by decide) ha hc
  · have hr2 := E.rows_nonanchor 1 2 (by decide) hr1
    obtain ⟨r,b,hr,hb⟩ := nonanchor_zero_variables _ _ hr1 hc1 (E.entry_eq 1 1)
    obtain ⟨s,c,hs,hc⟩ := nonanchor_zero_variables _ _ hr2 hc2 (E.entry_eq 2 2)
    have hbt : topVariable A b := by simpa [hA,hb,host,fixedH] using E.entry_eq 0 1
    have hct : topVariable A c := by simpa [hA,hc,host,fixedH] using E.entry_eq 0 2
    have hbc := E.variable_columns_order (by decide) hb hc
    have hsb : variableEntry s b=true := by simpa [hs,hb,host,fixedH] using E.entry_eq 2 1
    have hsc : variableEntry s c=false := by simpa [hs,hc,host,fixedH] using E.entry_eq 2 2
    rcases ha : E.cols 0 with t | (a | d)
    · simp [ha,IsAnchor] at hc0
    · apply one_anchor_no_anchor_columns A r s a b c hbt hct
      · simpa [hr,ha,host,fixedH] using E.entry_eq 1 0
      · simpa [hr,hb,host,fixedH] using E.entry_eq 1 1
      · simpa [hr,hc,host,fixedH] using E.entry_eq 1 2
      · simpa [hs,ha,host,fixedH] using E.entry_eq 2 0
      · exact hsb
      · exact hsc
      · exact E.variable_columns_order (by decide) ha hb
      · exact hbc
    · have hkA : kind A<2 := by simpa [hA,ha,host,fixedH] using E.entry_eq 0 0
      have hcls : b.1=c.1 := by
        by_contra hn
        have he := (top_two_classes A b c hbt hct hn).1
        omega
      have he := ordered_column_mono s b c hcls hbc hsb
      simp [hsc] at he

end OrderedRemoval.Crown
