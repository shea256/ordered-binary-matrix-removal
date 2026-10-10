import OrderedRemoval.ExtractAnchors

namespace OrderedRemoval.Concrete

theorem row_shared_anchor_comparable {h : ℕ} (k r s c d : Position h)
    (hk : IsAnchor k) (hr : ¬ IsAnchor r) (hs : ¬ IsAnchor s)
    (hc : ¬ IsAnchor c) (hd : ¬ IsAnchor d)
    (hrk : host r k = true) (hsk : host s k = true)
    (hrc : host r c = false) (hrd : host r d = true)
    (hsc : host s c = true) (hsd : host s d = false) : False := by
  rcases k with ⟨t,j,u⟩ | k <;> simp_all [IsAnchor]
  have hrr := (anchor_col_role r t j u hr).mp hrk
  have hsr := (anchor_col_role s t j u hs).mp hsk
  exact nonanchor_row_comparable r s c d hr hs hc hd
    (rowRole_same_class hrr hsr) hrc hrd hsc hsd

theorem col_shared_anchor_comparable {h : ℕ} (k r s c d : Position h)
    (hk : IsAnchor k) (hr : ¬ IsAnchor r) (hs : ¬ IsAnchor s)
    (hc : ¬ IsAnchor c) (hd : ¬ IsAnchor d)
    (hkc : host k c = true) (hkd : host k d = true)
    (hrc : host r c = false) (hrd : host r d = true)
    (hsc : host s c = true) (hsd : host s d = false) : False := by
  rcases k with ⟨t,j,u⟩ | k <;> simp_all [IsAnchor]
  have hcr := (anchor_row_role c t j u hc).mp hkc
  have hdr := (anchor_row_role d t j u hd).mp hkd
  exact nonanchor_col_comparable r s c d hr hs hc hd
    (colRole_same_class hcr hdr) hrc hrd hsc hsd

theorem no_backward_anchor_rows {h : ℕ} (r s c d : Position h)
    (hr : IsAnchor r) (hs : IsAnchor s) (hc : ¬ IsAnchor c) (hd : ¬ IsAnchor d)
    (horder : OrderedHost.rowIndex h r < OrderedHost.rowIndex h s)
    (hrc : host r c = true) (hrd : host r d = true)
    (hsc : host s c = false) (hsd : host s d = true) : False := by
  rcases r with ⟨t,j,x⟩ | r <;> simp_all [IsAnchor]
  rcases s with ⟨u,k,y⟩ | s <;> simp_all
  have hm : modeRank t ≤ modeRank u := by
    rcases (row_anchor_order_iff t u j k x y).mp horder with hh | ⟨rfl,_⟩
    · omega
    · exact le_rfl
  have htc := (anchor_row_role c t j x hc).mp hrc
  have htd := (anchor_row_role d t j x hd).mp hrd
  have hud := (anchor_row_role d u k y hd).mp hsd
  have he := (anchor_row_role c u k y hc).mpr (colRole_forward hm htc htd hud)
  simp [hsc] at he

theorem no_backward_anchor_cols {h : ℕ} (c d r s : Position h)
    (hc : IsAnchor c) (hd : IsAnchor d) (hr : ¬ IsAnchor r) (hs : ¬ IsAnchor s)
    (horder : OrderedHost.columnIndex h c < OrderedHost.columnIndex h d)
    (hrc : host r c = true) (hsc : host s c = true)
    (hrd : host r d = false) (hsd : host s d = true) : False := by
  rcases c with ⟨t,j,x⟩ | c <;> simp_all [IsAnchor]
  rcases d with ⟨u,k,y⟩ | d <;> simp_all
  have hm : modeRank t ≤ modeRank u := by
    rcases (col_anchor_order_iff t u j k x y).mp horder with hh | ⟨rfl,_⟩
    · omega
    · exact le_rfl
  have htr := (anchor_col_role r t j x hr).mp hrc
  have hts := (anchor_col_role s t j x hs).mp hsc
  have hus := (anchor_col_role s u k y hs).mp hsd
  have he := (anchor_col_role r u k y hr).mpr (rowRole_forward hm htr hts hus)
  simp [hrd] at he

/-- Every actual ordered H copy supplies all structural assumptions of the
previously conditional anchor classification theorem. -/
def Copy.anchorCertificate {h : ℕ} (E : Copy h) :
    AnchorClassification.Certificate (prefixCount E.rows) (prefixCount E.cols) where
  rows_le := prefixCount_le E.rows
  cols_le := prefixCount_le E.cols
  rowMode := anchorRank ∘ E.rows
  colMode := anchorRank ∘ E.cols
  rowGroup := anchorGroup ∘ E.rows
  colGroup := anchorGroup ∘ E.cols
  row_order := fun i j hij hj => E.row_rank_strict i j hij ((E.row_anchor_prefix j).mpr hj)
  col_order := fun i j hij hj => E.col_rank_strict i j hij ((E.col_anchor_prefix j).mpr hj)
  anchor_one := by
    intro i j hi hj hone
    exact anchor_one_rank (E.rows i) (E.cols j)
      ((E.row_anchor_prefix i).mpr hi) ((E.col_anchor_prefix j).mpr hj)
      ((E.entry_eq i j).trans hone)
  crown_absent := by
    intro r s t c d e hr hs ht hc hd he hQ
    unfold AnchorClassification.Crown at hQ
    rcases hQ with ⟨h1,h2,h3,h4,h5,h6,h7,h8,h9⟩
    apply nonanchor_crown_absent (E.rows r) (E.rows s) (E.rows t)
      (E.cols c) (E.cols d) (E.cols e)
      (by rw [E.row_anchor_prefix]; omega)
      (by rw [E.row_anchor_prefix]; omega)
      (by rw [E.row_anchor_prefix]; omega)
      (by rw [E.col_anchor_prefix]; omega)
      (by rw [E.col_anchor_prefix]; omega)
      (by rw [E.col_anchor_prefix]; omega)
    all_goals simp_all [E.entry_eq]
  row_support_comparable := by
    intro k r s c d hk hr hs hc hd hrk hsk hcross
    rcases hcross with ⟨h1,h2,h3,h4⟩
    apply row_shared_anchor_comparable (E.cols k) (E.rows r) (E.rows s) (E.cols c) (E.cols d)
      ((E.col_anchor_prefix k).mpr hk)
      (by rw [E.row_anchor_prefix]; omega)
      (by rw [E.row_anchor_prefix]; omega)
      (by rw [E.col_anchor_prefix]; omega)
      (by rw [E.col_anchor_prefix]; omega)
    all_goals simp_all [E.entry_eq]
  col_support_comparable := by
    intro k r s c d hk hr hs hc hd hkc hkd hcross
    rcases hcross with ⟨h1,h2,h3,h4⟩
    apply col_shared_anchor_comparable (E.rows k) (E.rows r) (E.rows s) (E.cols c) (E.cols d)
      ((E.row_anchor_prefix k).mpr hk)
      (by rw [E.row_anchor_prefix]; omega)
      (by rw [E.row_anchor_prefix]; omega)
      (by rw [E.col_anchor_prefix]; omega)
      (by rw [E.col_anchor_prefix]; omega)
    all_goals simp_all [E.entry_eq]
  no_backward_row_containment := by
    intro r s c d hrs hs hc hd htrace
    rcases htrace with ⟨h1,h2,h3,h4⟩
    apply no_backward_anchor_rows (E.rows r) (E.rows s) (E.cols c) (E.cols d)
      (by rw [E.row_anchor_prefix]; omega)
      ((E.row_anchor_prefix s).mpr hs)
      (by rw [E.col_anchor_prefix]; omega)
      (by rw [E.col_anchor_prefix]; omega)
      (E.rowIncreasing hrs)
    all_goals simp_all [E.entry_eq]
  no_backward_col_containment := by
    intro c d r s hcd hd hr hs htrace
    rcases htrace with ⟨h1,h2,h3,h4⟩
    apply no_backward_anchor_cols (E.cols c) (E.cols d) (E.rows r) (E.rows s)
      (by rw [E.col_anchor_prefix]; omega)
      ((E.col_anchor_prefix d).mpr hd)
      (by rw [E.row_anchor_prefix]; omega)
      (by rw [E.row_anchor_prefix]; omega)
      (E.colIncreasing hcd)
    all_goals simp_all [E.entry_eq]

/-- Unconditional, all-depth anchor-count theorem for the concrete host. -/
theorem Copy.anchor_counts {h : ℕ} (E : Copy h) :
    prefixCount E.rows = 2 ∧ (prefixCount E.cols = 1 ∨ prefixCount E.cols = 2) :=
  AnchorClassification.anchor_counts E.anchorCertificate

end OrderedRemoval.Concrete
