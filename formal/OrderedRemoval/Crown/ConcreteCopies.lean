import OrderedRemoval.Crown.OrderedHost
import OrderedRemoval.ConcreteCopies

namespace OrderedRemoval.Crown
open Concrete

structure Copy (h : ℕ) where
  rows : Fin 3 → Position h
  cols : Fin 3 → Position h
  rowIncreasing : StrictMono (OrderedHost.rowIndex h ∘ rows)
  colIncreasing : StrictMono (OrderedHost.columnIndex h ∘ cols)
  entry_eq : ∀ i j, host (rows i) (cols j) = fixedH i j

theorem anchor_row_twins {h : ℕ} (t : Mode h) (j : Fin 2)
    (u v : Fin (2^h)) (c : Position h) :
    host (.inl (t,j,u)) c = host (.inl (t,j,v)) c := by
  rcases c with a | (w | d) <;> rfl

theorem anchor_col_twins {h : ℕ} (t : Mode h) (j : Fin 2)
    (u v : Fin (2^h)) (r : Position h) :
    host r (.inl (t,j,u)) = host r (.inl (t,j,v)) := by
  rcases r with a | (w | d) <;> rfl

theorem Copy.no_repeated_anchor_rows {h : ℕ} (E : Copy h) {i j : Fin 3}
    {t : Mode h} {g k : Fin 2} {x y : Fin (2^h)}
    (hi : E.rows i = .inl (t,g,x)) (hj : E.rows j = .inl (t,k,y)) : i = j := by
  apply rows_distinct
  intro z
  rw [← E.entry_eq, ← E.entry_eq, hi, hj]
  exact rows_same_mode t g k x y (E.cols z)

theorem Copy.no_repeated_anchor_cols {h : ℕ} (E : Copy h) {i j : Fin 3}
    {t : Mode h} {g k : Fin 2} {x y : Fin (2^h)}
    (hi : E.cols i = .inl (t,g,x)) (hj : E.cols j = .inl (t,k,y)) : i = j := by
  apply columns_distinct
  intro z
  rw [← E.entry_eq, ← E.entry_eq, hi, hj]
  exact cols_same_mode t g k x y (E.rows z)

theorem row_anchor_order_iff {h : ℕ} (t u : Mode h) (j k : Fin 2)
    (x y : Fin (2^h)) :
    OrderedHost.rowIndex h (.inl (t,j,x)) < OrderedHost.rowIndex h (.inl (u,k,y)) ↔
      modeRank t < modeRank u ∨ (t = u ∧ (j < k ∨ (j = k ∧ x < y))) := by
  rw [OrderedHost.rowIndex_lt_iff]
  change Sum.Lex _ _ (Sum.inl (toLex (t, toLex (j,x))))
    (Sum.inl (toLex (u, toLex (k,y)))) ↔ _
  rw [Sum.lex_inl_inl]
  simp only [Prod.Lex.lt_iff, ofLex_toLex]
  rfl

theorem nonanchor_zero_variables {h : ℕ} (r c : Position h)
    (hr : ¬ IsAnchor r) (hc : ¬ IsAnchor c) (he : host r c = false) :
    ∃ v w : VariablePosition h, r = .inr (.inl v) ∧ c = .inr (.inl w) := by
  rcases r with a | (v | d) <;> rcases c with b | (w | e) <;>
    simp_all [IsAnchor, host]

theorem nonanchor_crown_absent {h : ℕ} (r s t a b c : Position h)
    (hr : ¬ IsAnchor r) (hs : ¬ IsAnchor s) (ht : ¬ IsAnchor t)
    (ha : ¬ IsAnchor a) (hb : ¬ IsAnchor b) (hc : ¬ IsAnchor c)
    (hra : host r a = true) (hrb : host r b = false) (hrc : host r c = true)
    (hsa : host s a = true) (hsb : host s b = true) (hsc : host s c = false)
    (hta : host t a = false) (htb : host t b = true) (htc : host t c = true) :
    False := by
  obtain ⟨r,b,rfl,rfl⟩ := nonanchor_zero_variables r b hr hb hrb
  obtain ⟨s,c,rfl,rfl⟩ := nonanchor_zero_variables s c hs hc hsc
  obtain ⟨t,a,rfl,rfl⟩ := nonanchor_zero_variables t a ht ha hta
  exact variable_crown_absent r s t a b c hra hrb hrc hsa hsb hsc hta htb htc

theorem nonanchor_row_comparable {h : ℕ} (r s c d : Position h)
    (hr : ¬ IsAnchor r) (hs : ¬ IsAnchor s)
    (hc : ¬ IsAnchor c) (hd : ¬ IsAnchor d)
    (hclass : nonanchorClass r = nonanchorClass s)
    (hrc : host r c = false) (hrd : host r d = true)
    (hsc : host s c = true) (hsd : host s d = false) : False := by
  obtain ⟨r,c,rfl,rfl⟩ := nonanchor_zero_variables r c hr hc hrc
  obtain ⟨s,d,rfl,rfl⟩ := nonanchor_zero_variables s d hs hd hsd
  simp only [host] at hrc hrd hsc hsd
  have hcls : r.1 = s.1 := Fin.ext hclass
  rcases le_total (node r) (node s) with hn | hn
  · have he := variableEntry_row_antimono r s c hcls hn hsc
    simp [hrc] at he
  · have he := variableEntry_row_antimono s r d hcls.symm hn hrd
    simp [hsd] at he

theorem nonanchor_col_comparable {h : ℕ} (r s c d : Position h)
    (hr : ¬ IsAnchor r) (hs : ¬ IsAnchor s)
    (hc : ¬ IsAnchor c) (hd : ¬ IsAnchor d)
    (hclass : nonanchorClass c = nonanchorClass d)
    (hrc : host r c = false) (hrd : host r d = true)
    (hsc : host s c = true) (hsd : host s d = false) : False := by
  obtain ⟨r,c,rfl,rfl⟩ := nonanchor_zero_variables r c hr hc hrc
  obtain ⟨s,d,rfl,rfl⟩ := nonanchor_zero_variables s d hs hd hsd
  simp only [host] at hrc hrd hsc hsd
  have hcls : c.1 = d.1 := Fin.ext hclass
  rcases le_total (node c) (node d) with hn | hn
  · have he := variableEntry_column_mono s c d hcls hn hsc
    simp [hsd] at he
  · have he := variableEntry_column_mono r d c hcls.symm hn hrd
    simp [hrc] at he

end OrderedRemoval.Crown
