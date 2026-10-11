import OrderedRemoval.Rectangular.NoAnchorColumns

namespace OrderedRemoval.Rectangular
open Concrete

theorem Copy.second_row_nonanchor {h : ℕ} (E : Copy h) : ¬ IsAnchor (E.rows 1) :=
  E.second_row_nonanchor_of_first_col_anchor E.first_col_anchor

theorem Copy.last_row_nonanchor {h : ℕ} (E : Copy h) : ¬ IsAnchor (E.rows 2) :=
  E.rows_nonanchor 1 2 (by decide) E.second_row_nonanchor

/-- The first anchor column belongs to the top row's own group zero. -/
theorem Copy.first_frame {h : ℕ} (E : Copy h) :
    ∃ t g x y, E.rows 0=.inl (t,g,x) ∧ E.cols 0=.inl (t,0,y) := by
  obtain ⟨t,g,x,hr⟩ := (Concrete.isAnchor_iff_exists _).mp E.first_row_anchor
  obtain ⟨u,k,y,hc⟩ := (Concrete.isAnchor_iff_exists _).mp E.first_col_anchor
  have hh := anchor_one_mode t u g k x y (by rw [←hr,←hc,E.entry_eq]; rfl)
  exact ⟨t,g,x,y,hr,by rw [hc,←hh.1,hh.2]⟩

theorem Copy.last_col_nonanchor {h : ℕ} (E : Copy h) : ¬ IsAnchor (E.cols 3) := by
  intro hc3
  obtain ⟨t,g,x,y,hr,hc⟩ := E.first_frame
  obtain ⟨u,k,z,hc3⟩ := (Concrete.isAnchor_iff_exists _).mp hc3
  have hh := anchor_one_mode t u g k x z (by rw [←hr,←hc3,E.entry_eq]; rfl)
  have he : E.cols 3=.inl (t,0,z) := by rw [hc3,←hh.1,hh.2]
  have hn := E.no_repeated_anchor_cols hc he
  contradiction

theorem Copy.third_col_nonanchor {h : ℕ} (E : Copy h) : ¬ IsAnchor (E.cols 2) := by
  intro hc2
  obtain ⟨t,g,x,hc⟩ := (Concrete.isAnchor_iff_exists _).mp hc2
  have hr : rowRole t g (E.rows 1) :=
    (anchor_col_role _ t g x E.second_row_nonanchor).mp (by rw [←hc,E.entry_eq]; rfl)
  have hs : rowRole t g (E.rows 2) :=
    (anchor_col_role _ t g x E.last_row_nonanchor).mp (by rw [←hc,E.entry_eq]; rfl)
  have hcls := rowRole_same_class hr hs
  obtain ⟨r,d,heR,heD⟩ := nonanchor_zero_variables _ _
    E.second_row_nonanchor E.last_col_nonanchor (E.entry_eq 1 3)
  rcases heS : E.rows 2 with a | (s | u)
  · have hn := E.last_row_nonanchor
    simp [heS,IsAnchor] at hn
  · have hcls' : r.1=s.1 := by
      apply Fin.ext
      simpa [heR,heS,nonanchorClass] using hcls
    have ho := E.rowIncreasing (show (1:Fin 3)<2 by decide)
    change OrderedHost.rowIndex h (E.rows 1)<OrderedHost.rowIndex h (E.rows 2) at ho
    rw [heR,heS,OrderedHost.rowIndex_variable_lt_iff] at ho
    have hone : variableEntry s d=true := by simpa [heS,heD,host,fixedH] using E.entry_eq 2 3
    have hzero : variableEntry r d=false := by simpa [heR,heD,host,fixedH] using E.entry_eq 1 3
    have hb := variableEntry_row_antimono r s d hcls' (row_same_class_node_le r s hcls' ho) hone
    simp [hzero] at hb
  · have hb := r.1.isLt
    simp [heR,heS,nonanchorClass] at hcls
    omega

structure ModeFrame {h : ℕ} (E : Copy h) where
  mode : Mode h
  group : Fin 2
  x : Fin (2^h)
  y : Fin (2^h)
  r : VariablePosition h
  d : VariablePosition h
  row0 : E.rows 0=.inl (mode,group,x)
  col0 : E.cols 0=.inl (mode,0,y)
  row1 : E.rows 1=.inr (.inl r)
  col3 : E.cols 3=.inr (.inl d)
  r_role : rowRole mode 0 (.inr (.inl r))
  d_top : topVariable mode d
  c_not_top : host (.inl (mode,group,x)) (E.cols 2)=false

theorem Copy.mode_frame {h : ℕ} (E : Copy h) : Nonempty (ModeFrame E) := by
  obtain ⟨t,g,x,y,hr,hc⟩ := E.first_frame
  obtain ⟨r,d,hr1,hc3⟩ := nonanchor_zero_variables _ _
    E.second_row_nonanchor E.last_col_nonanchor (E.entry_eq 1 3)
  refine ⟨⟨t,g,x,y,r,d,hr,hc,hr1,hc3,?_,?_,?_⟩⟩
  · apply (anchor_col_role _ t 0 y (by simp [IsAnchor])).mp
    rw [←hr1,←hc,E.entry_eq]; rfl
  · simpa [hr,hc3,host,fixedH] using E.entry_eq 0 3
  · rw [←hr,E.entry_eq]; rfl

end OrderedRemoval.Rectangular
