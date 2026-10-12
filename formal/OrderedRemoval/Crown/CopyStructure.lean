import OrderedRemoval.Crown.Arithmetic

namespace OrderedRemoval.Crown
open Concrete

theorem Copy.row_anchor_initial {h : ℕ} (E : Copy h) (i j : Fin 3)
    (hij : i<j) (hj : IsAnchor (E.rows j)) : IsAnchor (E.rows i) := by
  obtain ⟨a,ha⟩ : ∃ a, E.rows j=.inl a := by
    cases he : E.rows j <;> simp_all [IsAnchor]
  obtain ⟨a,ha⟩ := OrderedHost.row_anchor_initial (E.rowIncreasing hij) ⟨a,ha⟩
  simp [ha,IsAnchor]

theorem Copy.col_anchor_final {h : ℕ} (E : Copy h) (i j : Fin 3)
    (hij : i<j) (hi : IsAnchor (E.cols i)) : IsAnchor (E.cols j) := by
  obtain ⟨a,ha⟩ : ∃ a, E.cols i=.inl a := by
    cases he : E.cols i <;> simp_all [IsAnchor]
  obtain ⟨a,ha⟩ := OrderedHost.column_anchor_final (E.colIncreasing hij) ⟨a,ha⟩
  simp [ha,IsAnchor]

theorem Copy.rows_nonanchor {h : ℕ} (E : Copy h) (i j : Fin 3)
    (hij : i≤j) (hi : ¬ IsAnchor (E.rows i)) : ¬ IsAnchor (E.rows j) := by
  rcases lt_or_eq_of_le hij with hij | rfl
  · exact fun hj => hi (E.row_anchor_initial i j hij hj)
  · exact hi

theorem Copy.cols_nonanchor {h : ℕ} (E : Copy h) (i j : Fin 3)
    (hij : i≤j) (hj : ¬ IsAnchor (E.cols j)) : ¬ IsAnchor (E.cols i) := by
  rcases lt_or_eq_of_le hij with hij | rfl
  · exact fun hi => hj (E.col_anchor_final i j hij hi)
  · exact hj

theorem Copy.no_repeated_dummy_rows {h : ℕ} (E : Copy h) {i j : Fin 3}
    {x y : Fin (2^h)} (hi : E.rows i=.inr (.inr x))
    (hj : E.rows j=.inr (.inr y)) : i=j := by
  apply rows_distinct
  intro k
  rw [←E.entry_eq,←E.entry_eq,hi,hj]
  rcases E.cols k with a | (c | d) <;> rfl

/-- A nonanchor row followed by another copy row is variable, since all
dummy rows are twins and occur last. -/
theorem Copy.row_variable_before {h : ℕ} (E : Copy h) (i j : Fin 3)
    (hij : i<j) (hi : ¬ IsAnchor (E.rows i)) :
    ∃ r : VariablePosition h, E.rows i=.inr (.inl r) := by
  have hj := E.rows_nonanchor i j hij.le hi
  rcases he : E.rows i with a | (r | d)
  · simp [he,IsAnchor] at hi
  · exact ⟨r,rfl⟩
  rcases he' : E.rows j with a | (s | e)
  · simp [he',IsAnchor] at hj
  · have ho := E.rowIncreasing hij
    change OrderedHost.rowIndex h (E.rows i)<OrderedHost.rowIndex h (E.rows j) at ho
    rw [he,he'] at ho
    exact (lt_asymm ho (OrderedHost.row_variable_lt_dummy s d)).elim
  · exact ((ne_of_lt hij) (E.no_repeated_dummy_rows he he')).elim

theorem Copy.first_row_anchor {h : ℕ} (E : Copy h) : IsAnchor (E.rows 0) := by
  by_contra h0
  have h1 := E.rows_nonanchor 0 1 (by decide) h0
  have h2 := E.rows_nonanchor 0 2 (by decide) h0
  by_cases hc2 : IsAnchor (E.cols 2)
  · obtain ⟨T,g,x,hT⟩ := (Concrete.isAnchor_iff_exists _).mp hc2
    obtain ⟨r,hr⟩ := E.row_variable_before 0 2 (by decide) h0
    obtain ⟨s,hs⟩ := E.row_variable_before 1 2 (by decide) h1
    have hTr : rowRole T 0 (.inr (.inl r)) := by
      simpa [hr,hT,host,fixedH] using E.entry_eq 0 2
    have hTs : rowRole T 0 (.inr (.inl s)) := by
      simpa [hs,hT,host,fixedH] using E.entry_eq 1 2
    have hcls : r.1=s.1 := Fin.ext (rowRole_same_class hTr hTs)
    by_cases hc0 : IsAnchor (E.cols 0)
    · have hc1 := E.col_anchor_final 0 1 (by decide) hc0
      obtain ⟨A,j,a,hA⟩ := (Concrete.isAnchor_iff_exists _).mp hc0
      obtain ⟨B,k,b,hB⟩ := (Concrete.isAnchor_iff_exists _).mp hc1
      have har : ¬rowRole A 0 (.inr (.inl r)) := by
        simpa [hr,hA,host,fixedH] using E.entry_eq 0 0
      have has : rowRole A 0 (.inr (.inl s)) := by
        simpa [hs,hA,host,fixedH] using E.entry_eq 1 0
      have hbr : rowRole B 0 (.inr (.inl r)) := by
        simpa [hr,hB,host,fixedH] using E.entry_eq 0 1
      have hbs : ¬rowRole B 0 (.inr (.inl s)) := by
        simpa [hs,hB,host,fixedH] using E.entry_eq 1 1
      rcases ht : E.rows 2 with a | (t | d)
      · simp [ht,IsAnchor] at h2
      · apply opposite_roles_disjoint A B r s (.inr (.inl t)) hcls har has hbr hbs
        · simpa [ht,hA,host,fixedH] using E.entry_eq 2 0
        · simpa [ht,hB,host,fixedH] using E.entry_eq 2 1
      · have hk := opposite_roles_horizontal A r s hcls har has
        have he := E.entry_eq 2 0
        simp [ht,hA,host,fixedH,not_lt_of_ge hk] at he
    · obtain ⟨r',c,hr',hc⟩ := nonanchor_zero_variables _ _ h0 hc0 (E.entry_eq 0 0)
      have hrn : r=r' := by simpa [hr] using hr'
      subst r'
      have hone : variableEntry s c=true := by
        simpa [hs,hc,host,fixedH] using E.entry_eq 1 0
      have hzero : variableEntry r c=false := by
        simpa [hr,hc,host,fixedH] using E.entry_eq 0 0
      have ho := E.rowIncreasing (show (0:Fin 3)<1 by decide)
      change OrderedHost.rowIndex h (E.rows 0)<OrderedHost.rowIndex h (E.rows 1) at ho
      rw [hr,hs,OrderedHost.rowIndex_variable_lt_iff] at ho
      have he := variableEntry_row_antimono r s c hcls
        (Rectangular.row_same_class_node_le r s hcls ho) hone
      simp [hzero] at he
  · have hc0 := E.cols_nonanchor 0 2 (by decide) hc2
    have hc1 := E.cols_nonanchor 1 2 (by decide) hc2
    exact nonanchor_crown_absent _ _ _ _ _ _ h1 h2 h0 hc0 hc1 hc2
      (E.entry_eq 1 0) (E.entry_eq 1 1) (E.entry_eq 1 2)
      (E.entry_eq 2 0) (E.entry_eq 2 1) (E.entry_eq 2 2)
      (E.entry_eq 0 0) (E.entry_eq 0 1) (E.entry_eq 0 2)

theorem anchor_one_mode {h : ℕ} (A B : Mode h) (j k : Fin 2)
    (x y : Fin (2^h)) (he : host (.inl (A,j,x)) (.inl (B,k,y))=true) : A=B :=
  of_decide_eq_true he

theorem Copy.middle_col_nonanchor {h : ℕ} (E : Copy h) : ¬IsAnchor (E.cols 1) := by
  intro hc1
  have hc2 := E.col_anchor_final 1 2 (by decide) hc1
  obtain ⟨A,g,x,hA⟩ := (Concrete.isAnchor_iff_exists _).mp E.first_row_anchor
  obtain ⟨B,j,y,hB⟩ := (Concrete.isAnchor_iff_exists _).mp hc1
  obtain ⟨C,k,z,hC⟩ := (Concrete.isAnchor_iff_exists _).mp hc2
  have hab := anchor_one_mode A B g j x y (by rw [←hA,←hB,E.entry_eq]; rfl)
  have hac := anchor_one_mode A C g k x z (by rw [←hA,←hC,E.entry_eq]; rfl)
  have hbc : B=C := hab.symm.trans hac
  have hC' : E.cols 2=.inl (B,k,z) := by rw [hC,←hbc]
  have he := E.no_repeated_anchor_cols hB hC'
  contradiction

theorem Copy.second_row_nonanchor_of_last_col_anchor {h : ℕ} (E : Copy h)
    (hc : IsAnchor (E.cols 2)) : ¬ IsAnchor (E.rows 1) := by
  intro hr
  obtain ⟨A,j,x,ha⟩ := (Concrete.isAnchor_iff_exists _).mp E.first_row_anchor
  obtain ⟨B,k,y,hb⟩ := (Concrete.isAnchor_iff_exists _).mp hr
  obtain ⟨C,l,z,hc⟩ := (Concrete.isAnchor_iff_exists _).mp hc
  have hac := anchor_one_mode A C j l x z (by rw [←ha,←hc,E.entry_eq]; rfl)
  have hbc := anchor_one_mode B C k l y z (by rw [←hb,←hc,E.entry_eq]; rfl)
  have hab : A=B := hac.trans hbc.symm
  have hb' : E.rows 1=.inl (A,k,y) := by rw [hb,←hab]
  have he := E.no_repeated_anchor_rows ha hb'
  contradiction

end OrderedRemoval.Crown
