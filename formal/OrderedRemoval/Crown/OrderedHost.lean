import OrderedRemoval.Crown.Host
import OrderedRemoval.Rectangular.OrderedHost

namespace OrderedRemoval.Crown
noncomputable section
namespace OrderedHost
open Concrete

abbrev size := Rectangular.OrderedHost.size
abbrev rowIndex := Rectangular.OrderedHost.rowIndex
abbrev rowOrder := Rectangular.OrderedHost.rowOrder

abbrev ColKey (h : ℕ) :=
  (Fin (2^h) ⊕ₗ VariablePosition h) ⊕ₗ AnchorFrames.AnchorOrder (Mode h) (Fin (2^h))

/-- Column anchors are a suffix; the dummy and tree orders are unchanged. -/
def colKey {h : ℕ} : Position h → ColKey h
  | .inl (t,u,x) => .inrₗ (toLex (t,toLex (u,x)))
  | .inr (.inl v) => .inlₗ (.inrₗ v)
  | .inr (.inr x) => .inlₗ (.inlₗ x)

def colEquiv (h : ℕ) : Position h ≃ ColKey h where
  toFun := colKey
  invFun x := match ofLex x with
    | .inr a => .inl ((ofLex a).1, (ofLex (ofLex a).2).1, (ofLex (ofLex a).2).2)
    | .inl b => match ofLex b with
      | .inl x => .inr (.inr x)
      | .inr v => .inr (.inl v)
  left_inv := by rintro (⟨t,u,x⟩ | (v | x)) <;> rfl
  right_inv := by rintro ((x | v) | ⟨t,u,x⟩) <;> rfl

abbrev columnOrder (h : ℕ) : LinearOrder (Position h) := by
  letI := modeOrder h
  letI := TreePositions.positionOrder true h
  exact LinearOrder.lift' colKey (colEquiv h).injective

def columnIndex (h : ℕ) : Position h ≃ Fin (size h) := by
  letI := columnOrder h
  exact (monoEquivOfFin (Position h) (card_position h)).toEquiv.symm

theorem rowIndex_lt_iff (h : ℕ) (r s : Position h) :
    rowIndex h r < rowIndex h s ↔ @LT.lt _ (rowOrder h).toLT r s :=
  Rectangular.OrderedHost.rowIndex_lt_iff h r s

theorem columnIndex_lt_iff (h : ℕ) (r s : Position h) :
    columnIndex h r < columnIndex h s ↔ @LT.lt _ (columnOrder h).toLT r s := by
  let := columnOrder h
  exact @OrderIso.lt_iff_lt _ _ (columnOrder h).toPreorder inferInstance
    (@OrderIso.symm _ _ inferInstance (columnOrder h).toLE
      (monoEquivOfFin (Position h) (card_position h))) r s

theorem rowIndex_variable_lt_iff {h : ℕ} (v w : VariablePosition h) :
    rowIndex h (.inr (.inl v)) < rowIndex h (.inr (.inl w)) ↔
      TreePositions.rowKey h v < TreePositions.rowKey h w :=
  Rectangular.OrderedHost.rowIndex_variable_lt_iff v w

theorem columnIndex_variable_lt_iff {h : ℕ} (v w : VariablePosition h) :
    columnIndex h (.inr (.inl v)) < columnIndex h (.inr (.inl w)) ↔
      TreePositions.columnKey h v < TreePositions.columnKey h w := by
  rw [columnIndex_lt_iff]
  change Sum.Lex _ _
    (Sum.inl (toLex (Sum.inr v : Fin (2^h) ⊕ VariablePosition h)))
    (Sum.inl (toLex (Sum.inr w : Fin (2^h) ⊕ VariablePosition h))) ↔ _
  rw [Sum.lex_inl_inl]
  change Sum.Lex _ _ (Sum.inr v) (Sum.inr w) ↔ _
  rw [Sum.lex_inr_inr]
  rfl

theorem row_anchor_strictMono {h : ℕ} (t : Mode h) (a : Fin 2 → Fin (2^h)) :
    StrictMono (fun u => rowIndex h (.inl (t,u,a u))) :=
  Rectangular.OrderedHost.row_anchor_strictMono t a

theorem column_anchor_strictMono {h : ℕ} (t : Mode h) (a : Fin 2 → Fin (2^h)) :
    StrictMono (fun u => columnIndex h (.inl (t,u,a u))) := by
  intro u v huv
  rw [columnIndex_lt_iff]
  change Sum.Lex _ _ _ _
  apply Sum.Lex.inr
  apply Prod.Lex.right
  exact Prod.Lex.left _ _ huv

theorem row_anchor_lt_nonanchor {h : ℕ} (t : Mode h) (u : Fin 2)
    (a : Fin (2^h)) (x : VariablePosition h ⊕ Fin (2^h)) :
    rowIndex h (.inl (t,u,a)) < rowIndex h (.inr x) :=
  Rectangular.OrderedHost.row_anchor_lt_nonanchor t u a x

theorem column_nonanchor_lt_anchor {h : ℕ} (t : Mode h) (u : Fin 2)
    (a : Fin (2^h)) (x : VariablePosition h ⊕ Fin (2^h)) :
    columnIndex h (.inr x) < columnIndex h (.inl (t,u,a)) := by
  rw [columnIndex_lt_iff]
  cases x <;> exact Sum.Lex.sep _ _

theorem row_variable_lt_dummy {h : ℕ} (v : VariablePosition h) (x : Fin (2^h)) :
    rowIndex h (.inr (.inl v)) < rowIndex h (.inr (.inr x)) :=
  Rectangular.OrderedHost.row_variable_lt_dummy v x

theorem column_dummy_lt_variable {h : ℕ} (v : VariablePosition h) (x : Fin (2^h)) :
    columnIndex h (.inr (.inr x)) < columnIndex h (.inr (.inl v)) := by
  rw [columnIndex_lt_iff]
  exact Sum.Lex.inl (Sum.Lex.sep _ _)

theorem row_anchor_initial {h : ℕ} {r s : Position h}
    (hrs : rowIndex h r < rowIndex h s) (hs : ∃ a, s=.inl a) :
    ∃ a, r=.inl a := Rectangular.OrderedHost.row_anchor_initial hrs hs

theorem column_anchor_final {h : ℕ} {r s : Position h}
    (hrs : columnIndex h r < columnIndex h s) (hr : ∃ a, r=.inl a) :
    ∃ a, s=.inl a := by
  obtain ⟨⟨t,u,x⟩,rfl⟩ := hr
  rcases s with a | v
  · exact ⟨a,rfl⟩
  · exact (lt_asymm hrs (column_nonanchor_lt_anchor t u x v)).elim

end OrderedHost
end
end OrderedRemoval.Crown
