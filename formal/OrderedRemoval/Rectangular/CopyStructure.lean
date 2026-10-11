import OrderedRemoval.Rectangular.SupportArithmetic

namespace OrderedRemoval.Rectangular
open Concrete

/-- The anchors form initial segments independently on the two axes. -/
theorem Copy.row_anchor_initial {h : ℕ} (E : Copy h) (i j : Fin 3)
    (hij : i<j) (hj : IsAnchor (E.rows j)) : IsAnchor (E.rows i) := by
  obtain ⟨a,ha⟩ : ∃ a, E.rows j=.inl a := by
    cases he : E.rows j <;> simp_all [IsAnchor]
  obtain ⟨a,ha⟩ := OrderedHost.row_anchor_initial (E.rowIncreasing hij) ⟨a,ha⟩
  simp [ha,IsAnchor]

theorem Copy.col_anchor_initial {h : ℕ} (E : Copy h) (i j : Fin 4)
    (hij : i<j) (hj : IsAnchor (E.cols j)) : IsAnchor (E.cols i) := by
  obtain ⟨a,ha⟩ : ∃ a, E.cols j=.inl a := by
    cases he : E.cols j <;> simp_all [IsAnchor]
  obtain ⟨a,ha⟩ := OrderedHost.column_anchor_initial (E.colIncreasing hij) ⟨a,ha⟩
  simp [ha,IsAnchor]

theorem Copy.rows_nonanchor {h : ℕ} (E : Copy h) (i j : Fin 3)
    (hij : i≤j) (hi : ¬ IsAnchor (E.rows i)) : ¬ IsAnchor (E.rows j) := by
  rcases lt_or_eq_of_le hij with hij | rfl
  · exact fun hj => hi (E.row_anchor_initial i j hij hj)
  · exact hi

theorem Copy.cols_nonanchor {h : ℕ} (E : Copy h) (i j : Fin 4)
    (hij : i≤j) (hi : ¬ IsAnchor (E.cols i)) : ¬ IsAnchor (E.cols j) := by
  rcases lt_or_eq_of_le hij with hij | rfl
  · exact fun hj => hi (E.col_anchor_initial i j hij hj)
  · exact hi

theorem anchor_col_role {h : ℕ} (x : Position h) (t : Mode h)
    (j : Fin 2) (v : Fin (2^h)) (hx : ¬ IsAnchor x) :
    host x (.inl (t,j,v)) = true ↔ rowRole t j x := by
  rcases x with a | (x | d) <;> simp_all [IsAnchor,host]

theorem anchor_one_mode {h : ℕ} (A B : Mode h) (j k : Fin 2)
    (x y : Fin (2^h)) (he : host (.inl (A,j,x)) (.inl (B,k,y))=true) :
    A=B ∧ k=0 := by
  have hh : A=B ∧ k.val=0 := of_decide_eq_true he
  exact ⟨hh.1,Fin.ext hh.2⟩

theorem Copy.first_row_anchor {h : ℕ} (E : Copy h) : IsAnchor (E.rows 0) := by
  by_contra h0
  have h1 := E.rows_nonanchor 0 1 (by decide) h0
  have h2 := E.rows_nonanchor 0 2 (by decide) h0
  by_cases hc2 : IsAnchor (E.cols 2)
  · obtain ⟨A,j,x,hc0⟩ := (Concrete.isAnchor_iff_exists _).mp
      (E.col_anchor_initial 0 2 (by decide) hc2)
    obtain ⟨B,k,y,hc2⟩ := (Concrete.isAnchor_iff_exists _).mp hc2
    have har : rowRole A j (E.rows 0) := (anchor_col_role _ A j x h0).mp
      (by rw [←hc0,E.entry_eq]; rfl)
    have has : rowRole A j (E.rows 1) := (anchor_col_role _ A j x h1).mp
      (by rw [←hc0,E.entry_eq]; rfl)
    have hat : ¬ rowRole A j (E.rows 2) := by
      intro ht
      have he := (anchor_col_role _ A j x h2).mpr ht
      rw [←hc0,E.entry_eq] at he
      contradiction
    have hbr : ¬ rowRole B k (E.rows 0) := by
      intro ht
      have he := (anchor_col_role _ B k y h0).mpr ht
      rw [←hc2,E.entry_eq] at he
      contradiction
    have hbs : rowRole B k (E.rows 1) := (anchor_col_role _ B k y h1).mp
      (by rw [←hc2,E.entry_eq]; rfl)
    have hbt : rowRole B k (E.rows 2) := (anchor_col_role _ B k y h2).mp
      (by rw [←hc2,E.entry_eq]; rfl)
    exact role_laminar A B j k _ _ _ har has hat hbr hbs hbt
  have hc3 := E.cols_nonanchor 2 3 (by decide) hc2
  by_cases hc0 : IsAnchor (E.cols 0)
  · obtain ⟨A,j,x,hc0⟩ := (Concrete.isAnchor_iff_exists _).mp hc0
    have har : rowRole A j (E.rows 0) := (anchor_col_role _ A j x h0).mp
      (by rw [←hc0,E.entry_eq]; rfl)
    have has : rowRole A j (E.rows 1) := (anchor_col_role _ A j x h1).mp
      (by rw [←hc0,E.entry_eq]; rfl)
    exact nonanchor_row_comparable _ _ _ _ h0 h1 hc2 hc3
      (rowRole_same_class har has) (E.entry_eq 0 2) (E.entry_eq 0 3)
      (E.entry_eq 1 2) (E.entry_eq 1 3)
  exact nonanchor_crown_absent _ _ _ _ _ _ h0 h1 h2 hc0 hc2 hc3
    (E.entry_eq 0 0) (E.entry_eq 0 2) (E.entry_eq 0 3)
    (E.entry_eq 1 0) (E.entry_eq 1 2) (E.entry_eq 1 3)
    (E.entry_eq 2 0) (E.entry_eq 2 2) (E.entry_eq 2 3)

theorem Copy.second_row_nonanchor_of_first_col_anchor {h : ℕ} (E : Copy h)
    (hc : IsAnchor (E.cols 0)) : ¬ IsAnchor (E.rows 1) := by
  intro hr
  obtain ⟨A,j,x,ha⟩ := (Concrete.isAnchor_iff_exists _).mp E.first_row_anchor
  obtain ⟨B,k,y,hb⟩ := (Concrete.isAnchor_iff_exists _).mp hr
  obtain ⟨C,l,z,hc⟩ := (Concrete.isAnchor_iff_exists _).mp hc
  have hac := anchor_one_mode A C j l x z (by rw [←ha,←hc,E.entry_eq]; rfl)
  have hbc := anchor_one_mode B C k l y z (by rw [←hb,←hc,E.entry_eq]; rfl)
  have hab : A=B := hac.1.trans hbc.1.symm
  subst B
  have he := E.no_repeated_anchor_rows ha hb
  contradiction

end OrderedRemoval.Rectangular
