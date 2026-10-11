import OrderedRemoval.Rectangular.AnchorClassification
import OrderedRemoval.Rectangular.VerticalArithmetic
import OrderedRemoval.ZeroSetSize

namespace OrderedRemoval.Rectangular
open Concrete
set_option maxHeartbeats 2000000

theorem ModeFrame.third_column_variable {h : ℕ} {E : Copy h} (F : ModeFrame E) :
    ∃ c : VariablePosition h, E.cols 2=.inr (.inl c) := by
  have hn := E.third_col_nonanchor
  rcases hec : E.cols 2 with a | (c | u)
  · simp [hec,IsAnchor] at hn
  · exact ⟨c,rfl⟩
  · have hk : kind F.mode<2 := by
      have he := F.c_not_top
      simpa [hec,host] using he
    have ha : IsAnchor (E.cols 1) := by
      by_contra hn1
      obtain ⟨r',c',hr',hc'⟩ := nonanchor_zero_variables _ _
        E.second_row_nonanchor hn1 (E.entry_eq 1 1)
      have ho := E.colIncreasing (show (1:Fin 4)<2 by decide)
      change OrderedHost.columnIndex h (E.cols 1)<OrderedHost.columnIndex h (E.cols 2) at ho
      rw [hc',hec] at ho
      exact not_lt_of_gt (OrderedHost.column_dummy_lt_variable c' u) ho
    obtain ⟨B,j,y,hc1⟩ := (Concrete.isAnchor_iff_exists _).mp ha
    have hnon := E.last_row_nonanchor
    rcases her : E.rows 2 with a | (s | v)
    · simp [her,IsAnchor] at hnon
    · have hz : variableEntry F.r F.d=false := by
        simpa [F.row1,F.col3,host,fixedH] using E.entry_eq 1 3
      have hone : variableEntry s F.d=true := by
        simpa [her,F.col3,host,fixedH] using E.entry_eq 2 3
      have ho := E.rowIncreasing (show (1:Fin 3)<2 by decide)
      change OrderedHost.rowIndex h (E.rows 1)<OrderedHost.rowIndex h (E.rows 2) at ho
      rw [F.row1,her,OrderedHost.rowIndex_variable_lt_iff] at ho
      exact (vertical_zero_later_impossible F.mode F.r s F.d hk F.r_role F.d_top hz hone ho).elim
    · have hs : rowRole B j (.inr (.inr v)) :=
        (anchor_col_role _ B j y (by simp [IsAnchor])).mp (by
          rw [←her,←hc1,E.entry_eq]; rfl)
      have hBk : 2≤kind B := by simp [rowRole] at hs; omega
      have ho := E.colIncreasing (show (0:Fin 4)<1 by decide)
      change OrderedHost.columnIndex h (E.cols 0)<OrderedHost.columnIndex h (E.cols 1) at ho
      rw [F.col0,hc1,col_anchor_order_iff] at ho
      have hle : modeRank F.mode ≤ modeRank B := by
        rcases ho with ho | ⟨he,_⟩
        · omega
        · rw [he]
      have hFl := level_le F.mode
      have hFp := level_pos F.mode
      have hBl := level_le B
      have hBp := level_pos B
      have hBklt := kind_lt B
      unfold modeRank at hle
      split_ifs at hle <;> omega

theorem Copy.zero_localization {h : ℕ} (E : Copy h) :
    InZeroSet (E.rows 1) (E.cols 3) := by
  obtain ⟨F⟩ := E.mode_frame
  obtain ⟨c,hc⟩ := F.third_column_variable
  have hcnot : ¬topVariable F.mode c := by
    simpa [hc,host] using F.c_not_top
  have hone : variableEntry F.r c=true := by
    simpa [F.row1,hc,host,fixedH] using E.entry_eq 1 2
  have hzero : variableEntry F.r F.d=false := by
    simpa [F.row1,F.col3,host,fixedH] using E.entry_eq 1 3
  have ho := E.colIncreasing (show (2:Fin 4)<3 by decide)
  change OrderedHost.columnIndex h (E.cols 2)<OrderedHost.columnIndex h (E.cols 3) at ho
  rw [hc,F.col3,OrderedHost.columnIndex_variable_lt_iff] at ho
  obtain ⟨hr,hd,hn,_⟩ := mode_zero_localization F.mode F.r c F.d
    F.r_role hcnot F.d_top hone hzero ho
  simpa [F.row1,F.col3,InZeroSet] using And.intro hr (And.intro hd hn)

end OrderedRemoval.Rectangular
