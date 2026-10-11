import OrderedRemoval.ConcreteCopies

namespace OrderedRemoval.Concrete

def anchorRank {h : ℕ} : Position h → ℕ
  | .inl (t,_,_) => modeRank t
  | .inr _ => 0

def anchorGroup {h : ℕ} : Position h → Fin 2
  | .inl (_,j,_) => j
  | .inr _ => 0

def prefixCount {h : ℕ} (f : Fin 4 → Position h) : ℕ :=
  if IsAnchor (f 0) then
    if IsAnchor (f 1) then
      if IsAnchor (f 2) then
        if IsAnchor (f 3) then 4 else 3
      else 2
    else 1
  else 0

theorem prefixCount_le {h : ℕ} (f : Fin 4 → Position h) : prefixCount f ≤ 4 := by
  unfold prefixCount
  split_ifs <;> decide

theorem prefixCount_spec {h : ℕ} (f : Fin 4 → Position h)
    (hinit : ∀ i j : Fin 4, i < j → IsAnchor (f j) → IsAnchor (f i)) :
    ∀ i : Fin 4, IsAnchor (f i) ↔ i.val < prefixCount f := by
  have h01 := hinit 0 1 (by decide)
  have h02 := hinit 0 2 (by decide)
  have h03 := hinit 0 3 (by decide)
  have h12 := hinit 1 2 (by decide)
  have h13 := hinit 1 3 (by decide)
  have h23 := hinit 2 3 (by decide)
  intro i
  fin_cases i <;> unfold prefixCount <;> split_ifs <;> simp_all

theorem Copy.row_anchor_prefix {h : ℕ} (E : Copy h) (i : Fin 4) :
    IsAnchor (E.rows i) ↔ i.val < prefixCount E.rows := by
  apply prefixCount_spec
  intro a b hab hb
  have hh : ∃ x, E.rows b = .inl x := by
    cases he : E.rows b with
    | inl x => exact ⟨x, rfl⟩
    | inr x => simp [he, IsAnchor] at hb
  obtain ⟨x,hx⟩ := OrderedHost.row_anchor_initial (E.rowIncreasing hab) hh
  simp [hx, IsAnchor]

theorem Copy.col_anchor_prefix {h : ℕ} (E : Copy h) (i : Fin 4) :
    IsAnchor (E.cols i) ↔ i.val < prefixCount E.cols := by
  apply prefixCount_spec
  intro a b hab hb
  have hh : ∃ x, E.cols b = .inl x := by
    cases he : E.cols b with
    | inl x => exact ⟨x, rfl⟩
    | inr x => simp [he, IsAnchor] at hb
  obtain ⟨x,hx⟩ := OrderedHost.column_anchor_initial (E.colIncreasing hab) hh
  simp [hx, IsAnchor]

theorem anchor_col_role {h : ℕ} (x : Position h) (t : Mode h)
    (j : Fin 2) (v : Fin (2^h)) (hx : ¬ IsAnchor x) :
    host x (.inl (t,j,v)) = true ↔ rowRole t j x := by
  rcases x with a | (x | d) <;> simp_all [IsAnchor]
  all_goals fin_cases j <;> simp [host]

theorem anchor_row_role {h : ℕ} (x : Position h) (t : Mode h)
    (j : Fin 2) (v : Fin (2^h)) (hx : ¬ IsAnchor x) :
    host (.inl (t,j,v)) x = true ↔ colRole t j x := by
  rcases x with a | (x | d) <;> simp_all [IsAnchor]
  all_goals fin_cases j <;> simp [host]

theorem Copy.row_rank_strict {h : ℕ} (E : Copy h) (i j : Fin 4)
    (hij : i < j) (hj : IsAnchor (E.rows j)) :
    2*anchorRank (E.rows i) + (anchorGroup (E.rows i)).val <
      2*anchorRank (E.rows j) + (anchorGroup (E.rows j)).val := by
  have hi : IsAnchor (E.rows i) := by
    rw [E.row_anchor_prefix] at hj ⊢
    omega
  cases hei : E.rows i with
  | inr x => simp [hei, IsAnchor] at hi
  | inl a =>
    rcases a with ⟨t,g,x⟩
    cases hej : E.rows j with
    | inr y => simp [hej, IsAnchor] at hj
    | inl b =>
      rcases b with ⟨u,k,y⟩
      have hord := E.rowIncreasing hij
      change OrderedHost.rowIndex h (E.rows i) < OrderedHost.rowIndex h (E.rows j) at hord
      rw [hei, hej, row_anchor_order_iff] at hord
      have hne : ¬ (t = u ∧ g = k) := by
        rintro ⟨rfl,rfl⟩
        exact (ne_of_lt hij) (E.no_repeated_anchor_rows hei hej)
      simp only [anchorRank, anchorGroup]
      have hg := g.isLt
      have hk := k.isLt
      rcases hord with hord | ⟨rfl,hord⟩
      · omega
      · have hneq : g ≠ k := fun he => hne ⟨rfl,he⟩
        have hval : g.val ≠ k.val := fun he => hneq (Fin.ext he)
        rcases hord with hord | ⟨he,_⟩
        · exact Nat.add_lt_add_left hord _
        · exact (hneq he).elim

theorem Copy.col_rank_strict {h : ℕ} (E : Copy h) (i j : Fin 4)
    (hij : i < j) (hj : IsAnchor (E.cols j)) :
    2*anchorRank (E.cols i) + (anchorGroup (E.cols i)).val <
      2*anchorRank (E.cols j) + (anchorGroup (E.cols j)).val := by
  have hi : IsAnchor (E.cols i) := by
    rw [E.col_anchor_prefix] at hj ⊢
    omega
  cases hei : E.cols i with
  | inr x => simp [hei, IsAnchor] at hi
  | inl a =>
    rcases a with ⟨t,g,x⟩
    cases hej : E.cols j with
    | inr y => simp [hej, IsAnchor] at hj
    | inl b =>
      rcases b with ⟨u,k,y⟩
      have hord := E.colIncreasing hij
      change OrderedHost.columnIndex h (E.cols i) < OrderedHost.columnIndex h (E.cols j) at hord
      rw [hei, hej, col_anchor_order_iff] at hord
      have hne : ¬ (t = u ∧ g = k) := by
        rintro ⟨rfl,rfl⟩
        exact (ne_of_lt hij) (E.no_repeated_anchor_cols hei hej)
      simp only [anchorRank, anchorGroup]
      have hg := g.isLt
      have hk := k.isLt
      rcases hord with hord | ⟨rfl,hord⟩
      · omega
      · have hneq : g ≠ k := fun he => hne ⟨rfl,he⟩
        rcases hord with hord | ⟨he,_⟩
        · exact Nat.add_lt_add_left hord _
        · exact (hneq he).elim

theorem anchor_one_rank {h : ℕ} (r c : Position h)
    (hr : IsAnchor r) (hc : IsAnchor c) (hone : host r c = true) :
    anchorRank r = anchorRank c := by
  rcases r with ⟨t,g,x⟩ | r <;> simp_all [IsAnchor]
  rcases c with ⟨u,k,y⟩ | c <;> simp_all
  simp only [host] at hone
  have htu : t = u := by
    by_contra hne
    simp [hne] at hone
  simp [anchorRank, htu]

end OrderedRemoval.Concrete
