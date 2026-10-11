import OrderedRemoval.Rectangular.LocalizationArithmetic

namespace OrderedRemoval.Rectangular
open Concrete
open TreePositions in
theorem row_same_class_node_le {h : ℕ} (v w : Concrete.VariablePosition h)
    (hc : v.1 = w.1) (ho : rowKey h v < rowKey h w) : Concrete.node v ≤ Concrete.node w := by
  have hv := congrArg Fin.val hc
  have hb : 0 < 2 ^ (h - v.1.val / 2) := by positivity
  unfold rowKey orderKey at ho
  simp only [Bool.false_eq_true, ↓reduceIte, ← hv] at ho
  split_ifs at ho with hl hs
  · have he := key_endpoint_le ho
    simp [Concrete.node, Concrete.depth, ← hv, hl]
    omega
  · have he := key_endpoint_le ho
    change 2 * (v.2.val / 2^(h-v.1.val/2)) * 2^(h-v.1.val/2) ≤
      2 * (w.2.val / 2^(h-v.1.val/2)) * 2^(h-v.1.val/2) at he
    rw [mul_le_mul_iff_left₀ hb] at he
    simp only [Concrete.node, Concrete.depth, ← hv]
    omega
  · have he := key_endpoint_le ho
    change 2 * (v.2.val / 2^(h-v.1.val/2)+1) * 2^(h-v.1.val/2) ≤
      2 * (w.2.val / 2^(h-v.1.val/2)+1) * 2^(h-v.1.val/2) at he
    rw [mul_le_mul_iff_left₀ hb] at he
    simp only [Concrete.node, Concrete.depth, ← hv]
    omega

theorem row_child_before_minus_parent {h i : ℕ} (r s : VariablePosition h)
    (hr : AtLevel (i+1) false r) (hs : AtLevel i false s)
    (ho : TreePositions.rowKey h r < TreePositions.rowKey h s) :
    node r/2 < node s := by
  have hn : ¬ node s ≤ node r/2 := fun he =>
    (not_lt_of_gt ho) ((row_minus_lt_iff hr hs).mpr he)
  omega

/-- The nonanchor row entries are nonincreasing along each row class. -/
theorem ordered_row_antimono {h : ℕ} (r s : VariablePosition h)
    (c : Position h) (hc : ¬ IsAnchor c) (hcls : r.1=s.1)
    (ho : TreePositions.rowKey h r < TreePositions.rowKey h s)
    (hs : host (.inr (.inl s)) c=true) : host (.inr (.inl r)) c=true := by
  rcases c with a | (c | d)
  · simp [IsAnchor] at hc
  · exact variableEntry_row_antimono r s c hcls (row_same_class_node_le r s hcls ho) hs
  · rfl

end OrderedRemoval.Rectangular
