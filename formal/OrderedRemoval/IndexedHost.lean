import OrderedRemoval.AnchorCertificate

/-! The concrete matrix indexed by two independent ordered enumerations.
This interface connects arbitrary increasing index maps to the raw-position
copy model; no structural certificate is an input. -/
namespace OrderedRemoval.Concrete
noncomputable section

def matrix (h : ℕ) (r c : Fin (OrderedHost.size h)) : Bool :=
  host ((OrderedHost.rowIndex h).symm r) ((OrderedHost.columnIndex h).symm c)

def copyOfIndices {h : ℕ} (r c : Fin 4 → Fin (OrderedHost.size h))
    (hr : StrictMono r) (hc : StrictMono c)
    (he : ∀ i j, matrix h (r i) (c j) = AnchorClassification.H4 i j) : Copy h where
  rows := (OrderedHost.rowIndex h).symm ∘ r
  cols := (OrderedHost.columnIndex h).symm ∘ c
  rowIncreasing := by simpa only [Function.comp_def, Equiv.apply_symm_apply] using hr
  colIncreasing := by simpa only [Function.comp_def, Equiv.apply_symm_apply] using hc
  entry_eq := he

/-- Classification for any increasing row and column maps in the actual matrix. -/
theorem matrix_anchor_counts {h : ℕ} (r c : Fin 4 → Fin (OrderedHost.size h))
    (hr : StrictMono r) (hc : StrictMono c)
    (he : ∀ i j, matrix h (r i) (c j) = AnchorClassification.H4 i j) :
    prefixCount ((OrderedHost.rowIndex h).symm ∘ r) = 2 ∧
      (prefixCount ((OrderedHost.columnIndex h).symm ∘ c) = 1 ∨
       prefixCount ((OrderedHost.columnIndex h).symm ∘ c) = 2) :=
  (copyOfIndices r c hr hc he).anchor_counts

/-- The degenerate height-zero matrix has no ordered H4 copy. -/
theorem Copy.positive_height {h : ℕ} (E : Copy h) : 0 < h := by
  have ha : IsAnchor (E.rows 0) := (E.row_anchor_prefix 0).mpr (by
    rw [E.anchor_counts.1]; decide)
  rcases he : E.rows 0 with ⟨t,j,x⟩ | v
  · have ht := t.isLt
    omega
  · simp [he, IsAnchor] at ha

private def witnessRows : Fin 4 → Position 1 :=
  ![.inl (4,0,0), .inl (4,1,0), .inr (.inl (2,0)), .inr (.inr 0)]
private def witnessCols : Fin 4 → Position 1 :=
  ![.inl (4,0,0), .inl (4,1,0), .inr (.inl (2,0)), .inr (.inl (1,0))]

/-- A concrete balanced copy at height one witnesses nonvacuity. -/
theorem exists_copy_height_one : Nonempty (Copy 1) := by
  refine ⟨{
    rows := witnessRows
    cols := witnessCols
    rowIncreasing := ?_
    colIncreasing := ?_
    entry_eq := ?_ }⟩
  · intro i j hij
    change OrderedHost.rowIndex 1 (witnessRows i) < OrderedHost.rowIndex 1 (witnessRows j)
    rw [OrderedHost.rowIndex_lt_iff]
    fin_cases i <;> fin_cases j <;> norm_num at hij <;> decide
  · intro i j hij
    change OrderedHost.columnIndex 1 (witnessCols i) < OrderedHost.columnIndex 1 (witnessCols j)
    rw [OrderedHost.columnIndex_lt_iff]
    fin_cases i <;> fin_cases j <;> norm_num at hij <;> decide
  · decide

end
end OrderedRemoval.Concrete
