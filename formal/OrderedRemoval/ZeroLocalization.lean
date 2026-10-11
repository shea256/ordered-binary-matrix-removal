import OrderedRemoval.ThirdColumn

namespace OrderedRemoval.Concrete

/-- The leaf-to-parent-minus zero set, on raw row and column positions.
For h≥1 each leaf has precisely two positions in its parent's minus block. -/
def InZeroSet {h : ℕ} : Position h → Position h → Prop
  | .inr (.inl r), .inr (.inl d) =>
      r.1.val=2*h ∧ d.1.val+1=2*h ∧ node d=node r/2
  | _, _ => False

instance {h : ℕ} (r c : Position h) : Decidable (InZeroSet r c) := by
  unfold InZeroSet
  split <;> infer_instance

theorem zeroSet_entry {h : ℕ} (r c : Position h) (hz : InZeroSet r c) : host r c=false := by
  rcases r with a | (r | u) <;> rcases c with b | (c | v) <;> simp_all [InZeroSet]
  have ht : ¬ variableEntry r c=true := by
    rw [variableEntry_true_iff]
    omega
  cases he : variableEntry r c <;> simp_all

/-- Concrete, all-depth localization of the fixed (third row, fourth column)
zero in every ordered H4 copy. -/
theorem Copy.zero_localization {h : ℕ} (E : Copy h) : InZeroSet (E.rows 2) (E.cols 3) := by
  obtain ⟨F⟩ := E.mode_frame
  obtain ⟨c,hc⟩ := F.third_column_variable
  have hcr := F.c_role
  rw [hc] at hcr
  have hone : variableEntry F.r c=true := by
    rw [←host_variable_variable,←F.row2,←hc,E.entry_eq]; rfl
  have hz : variableEntry F.r F.d=false := by
    rw [←host_variable_variable,←F.row2,←F.col3,E.entry_eq]; rfl
  have ho := E.colIncreasing (show (2:Fin 4)<3 by decide)
  change OrderedHost.columnIndex h (E.cols 2)<OrderedHost.columnIndex h (E.cols 3) at ho
  rw [hc,F.col3,OrderedHost.columnIndex_variable_lt_iff] at ho
  obtain ⟨hr,hd,hn,_⟩ := mode_zero_localization F.A F.B F.group F.r c F.d
    F.mode_le F.r_role F.d_role hcr hone hz ho
  simpa [F.row2,F.col3,InZeroSet] using (show F.r.1.val=2*h ∧ F.d.1.val+1=2*h ∧
    node F.d=node F.r/2 from ⟨hr,hd,hn⟩)

/-- The same localization for ordinary matrix indices, with independent
increasing row and column maps and no structural assumptions. -/
theorem matrix_zero_localization {h : ℕ} (r c : Fin 4 → Fin (OrderedHost.size h))
    (hr : StrictMono r) (hc : StrictMono c)
    (he : ∀ i j, matrix h (r i) (c j)=AnchorClassification.H4 i j) :
    InZeroSet ((OrderedHost.rowIndex h).symm (r 2))
      ((OrderedHost.columnIndex h).symm (c 3)) :=
  (copyOfIndices r c hr hc he).zero_localization

end OrderedRemoval.Concrete
