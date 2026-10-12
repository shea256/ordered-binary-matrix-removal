import OrderedRemoval.Crown.NoAnchorColumns
import OrderedRemoval.ZeroSetSize

namespace OrderedRemoval.Crown
open Concrete

/-- Every ordered crown localizes its middle zero to a leaf and its own
minus parent. This quantifies over all copies, without a designated-role
assumption. -/
theorem Copy.zero_localization {h : ℕ} (E : Copy h) :
    InZeroSet (E.rows 1) (E.cols 1) := by
  have hr1 := E.second_row_nonanchor_of_last_col_anchor E.last_col_anchor
  have hr2 := E.rows_nonanchor 1 2 (by decide) hr1
  have hc1 := E.middle_col_nonanchor
  have hc0 := E.cols_nonanchor 0 1 (by decide) hc1
  obtain ⟨A,g,x,hA⟩ := (Concrete.isAnchor_iff_exists _).mp E.first_row_anchor
  obtain ⟨B,j,y,hB⟩ := (Concrete.isAnchor_iff_exists _).mp E.last_col_anchor
  have hab := anchor_one_mode A B g j x y (by rw [←hA,←hB,E.entry_eq]; rfl)
  have hB' : E.cols 2=.inl (A,j,y) := by rw [hB,←hab]
  obtain ⟨r,d,hr,hd⟩ := nonanchor_zero_variables _ _ hr1 hc1 (E.entry_eq 1 1)
  have hrrole : rowRole A 0 (.inr (.inl r)) := by
    simpa [hr,hB',host,fixedH] using E.entry_eq 1 2
  have hdtop : topVariable A d := by
    simpa [hA,hd,host,fixedH] using E.entry_eq 0 1
  have hzero : variableEntry r d=false := by
    simpa [hr,hd,host,fixedH] using E.entry_eq 1 1
  obtain ⟨c,hc⟩ : ∃ c : VariablePosition h, E.cols 0=.inr (.inl c) := by
    rcases hc : E.cols 0 with a | (c | u)
    · simp [hc,IsAnchor] at hc0
    · exact ⟨c,rfl⟩
    · have hk : kind A<2 := by simpa [hA,hc,host,fixedH] using E.entry_eq 0 0
      rcases hs : E.rows 2 with a | (s | v)
      · simp [hs,IsAnchor] at hr2
      · have hone : variableEntry s d=true := by
          simpa [hs,hd,host,fixedH] using E.entry_eq 2 1
        exact (Rectangular.vertical_zero_later_impossible A r s d hk hrrole hdtop
          hzero hone (E.variable_rows_order (by decide) hr hs)).elim
      · have he := E.entry_eq 2 2
        simp [hs,hB',host,fixedH,hk] at he
  have hcnot : ¬topVariable A c := by
    simpa [hA,hc,host,fixedH] using E.entry_eq 0 0
  have hone : variableEntry r c=true := by
    simpa [hr,hc,host,fixedH] using E.entry_eq 1 0
  obtain ⟨hrleaf,hdparent,hn,_⟩ := Rectangular.mode_zero_localization A r c d
    hrrole hcnot hdtop hone hzero (E.variable_columns_order (by decide) hc hd)
  simpa [hr,hd,InZeroSet] using And.intro hrleaf (And.intro hdparent hn)

end OrderedRemoval.Crown
