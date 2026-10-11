import OrderedRemoval.HostTreeOrder
import OrderedRemoval.OrderedHost

/-! Additional comparisons for localization, including both child signs. -/
namespace OrderedRemoval.TreePositions

theorem key_endpoint_le {a b p q t u c d x y : ℕ}
    (h : key a p t c x < key b q u d y) : a ≤ b := by
  simp only [key, Prod.Lex.lt_iff, ofLex_toLex] at h
  omega

theorem key_endpoint_lt_of_phase_gt {a b p q t u c d x y : ℕ}
    (h : key a p t c x < key b q u d y) (hp : q < p) : a < b := by
  simp only [key, Prod.Lex.lt_iff, ofLex_toLex] at h
  omega

theorem key_endpoint_lt_of_tie_gt {a b p t u c d x y : ℕ}
    (h : key a p t c x < key b p u d y) (ht : u < t) : a < b := by
  simp only [key, Prod.Lex.lt_iff, ofLex_toLex] at h
  omega

theorem early_parent_lt_late_child (b i r p a c d x y : ℕ) (hb : 0 < b) :
    earlyKey i (2*b) a c x < lateKey r b p d y ↔ a ≤ p/2 := by
  simp only [earlyKey, lateKey, key, Prod.Lex.lt_iff, ofLex_toLex]
  have h1 : 2*a*(2*b) = (4*a)*b := by ring
  have h2 : 2*(p+1)*b = (2*p+2)*b := by ring
  simp only [h1, h2]
  have hcancel : (4*a)*b < (2*p+2)*b ↔ 4*a < 2*p+2 := mul_lt_mul_iff_left₀ hb
  omega

theorem early_child_lt_late_parent (b i r p a c d x y : ℕ) (hb : 0 < b) :
    earlyKey i b p c x < lateKey r (2*b) a d y ↔ p/2 ≤ a := by
  simp only [earlyKey, lateKey, key, Prod.Lex.lt_iff, ofLex_toLex]
  have he : 2*(a+1)*(2*b) = (4*a+4)*b := by ring
  simp only [he]
  have hcancel : (2*p)*b < (4*a+4)*b ↔ 2*p < 4*a+4 := mul_lt_mul_iff_left₀ hb
  omega

theorem column_plus_parent_lt_minus_child {h i : ℕ} (hi : i < h)
    (x y : Fin (2^h)) :
    columnKey h (plusPos i (Nat.le_of_lt hi) y) <
      columnKey h (minusPos (i+1) (by omega) x) ↔ node i y ≤ node (i+1) x / 2 := by
  by_cases he : i+1=h
  · subst h
    rw [minusPos_leaf, columnKey_leaf, columnKey_plus_internal hi]
    have hs : i+1-i=1 := by omega
    simp only [hs, pow_one]
    simpa [node] using earlyKey_parent_lt_leafKey (i+1) i x.val (node i y) (2*i) y.val
  · have hic : i+1<h := by omega
    rw [columnKey_plus_internal hi, columnKey_minus_internal hic]
    have hr : h-i=h-(i+1)+1 := by omega
    have hb : 2^(h-i)=2*2^(h-(i+1)) := by rw [hr,pow_succ]; omega
    rw [hb]
    exact early_parent_lt_late_child _ _ _ _ _ _ _ _ _ (by positivity)

theorem column_plus_child_lt_minus_parent {h i : ℕ} (hi : i < h)
    (x y : Fin (2^h)) :
    columnKey h (plusPos (i+1) (by omega) x) <
      columnKey h (minusPos i (Nat.le_of_lt hi) y) ↔ node (i+1) x / 2 ≤ node i y := by
  by_cases he : i+1=h
  · subst h
    rw [columnKey_leaf, columnKey_minus_internal hi]
    have hs : i+1-i=1 := by omega
    simp only [hs,pow_one]
    simpa [node] using leafKey_lt_lateKey_parent (i+1) 1 x.val (node i y) (2*i+1) y.val
  · have hic : i+1<h := by omega
    rw [columnKey_plus_internal hic,columnKey_minus_internal hi]
    have hr : h-i=h-(i+1)+1 := by omega
    have hb : 2^(h-i)=2*2^(h-(i+1)) := by rw [hr,pow_succ]; omega
    rw [hb]
    exact early_child_lt_late_parent _ _ _ _ _ _ _ _ _ (by positivity)

end OrderedRemoval.TreePositions

namespace OrderedRemoval.Concrete
open TreePositions in
theorem column_same_class_node_le {h : ℕ} (v w : VariablePosition h)
    (hc : v.1 = w.1) (ho : columnKey h v < columnKey h w) : node v ≤ node w := by
  have hv := congrArg Fin.val hc
  have hb : 0 < 2 ^ (h - v.1.val / 2) := by positivity
  unfold columnKey orderKey at ho
  simp only [← hv] at ho
  split_ifs at ho with hl hs
  · have he := key_endpoint_le ho
    simp [node, depth, ← hv, hl]
    omega
  · have he := key_endpoint_le ho
    change 2 * (v.2.val / 2^(h-v.1.val/2)) * 2^(h-v.1.val/2) ≤
      2 * (w.2.val / 2^(h-v.1.val/2)) * 2^(h-v.1.val/2) at he
    rw [mul_le_mul_iff_left₀ hb] at he
    simp only [node, depth, ← hv]
    omega
  · have he := key_endpoint_le ho
    change 2 * (v.2.val / 2^(h-v.1.val/2)+1) * 2^(h-v.1.val/2) ≤
      2 * (w.2.val / 2^(h-v.1.val/2)+1) * 2^(h-v.1.val/2) at he
    rw [mul_le_mul_iff_left₀ hb] at he
    simp only [node, depth, ← hv]
    omega

theorem row_leaf_node_lt {h : ℕ} (v w : VariablePosition h)
    (hv : v.1.val = 2*h) (hw : w.1.val = 2*h)
    (ho : TreePositions.rowKey h v < TreePositions.rowKey h w) : node v < node w := by
  simp [TreePositions.rowKey, TreePositions.orderKey, TreePositions.leafKey,
    TreePositions.key, Prod.Lex.lt_iff, hv, hw] at ho
  simp [node, depth, hv, hw]
  omega

theorem column_parent_plus_lt_iff {h i : ℕ} {child parent : VariablePosition h}
    (hc : depth child = i+1) (hp : AtLevel i true parent) :
    TreePositions.columnKey h parent < TreePositions.columnKey h child ↔
      node parent ≤ node child / 2 := by
  have hi : i<h := by have := depth_le child; omega
  by_cases hs : plus child = true
  · exact column_plus_lt_iff ⟨hc,Or.inr hs⟩ hp
  · have hs' : plus child = false := by cases he : plus child <;> simp_all
    have hcl : AtLevel (i+1) false child := ⟨hc,Or.inr hs'⟩
    rw [node_eq_level_node hp.1, node_eq_level_node hc,
      eq_minusPos_of_atLevel hcl, eq_plusPos_of_atLevel hp]
    exact TreePositions.column_plus_parent_lt_minus_child hi child.2 parent.2

theorem column_child_lt_parent_minus_iff {h i : ℕ} {child parent : VariablePosition h}
    (hc : depth child = i+1) (hp : AtLevel i false parent) :
    TreePositions.columnKey h child < TreePositions.columnKey h parent ↔
      node child / 2 ≤ node parent := by
  have hi : i<h := by have := depth_le child; omega
  by_cases hs : plus child = false
  · exact column_minus_lt_iff ⟨hc,Or.inr hs⟩ hp
  · have hs' : plus child = true := by cases he : plus child <;> simp_all
    have hcl : AtLevel (i+1) true child := ⟨hc,Or.inr hs'⟩
    rw [node_eq_level_node hp.1, node_eq_level_node hc,
      eq_plusPos_of_atLevel hcl, eq_minusPos_of_atLevel hp]
    exact TreePositions.column_plus_child_lt_minus_parent hi child.2 parent.2

theorem column_child_before_plus {h i : ℕ} {child parent : VariablePosition h}
    (hc : depth child = i+1) (hp : AtLevel i true parent)
    (ho : TreePositions.columnKey h child < TreePositions.columnKey h parent) :
    node child / 2 < node parent := by
  have hn : ¬ node parent ≤ node child / 2 := fun hn =>
    (not_lt_of_gt ho) ((column_parent_plus_lt_iff hc hp).mpr hn)
  omega

theorem column_minus_before_child {h i : ℕ} {child parent : VariablePosition h}
    (hc : depth child = i+1) (hp : AtLevel i false parent)
    (ho : TreePositions.columnKey h parent < TreePositions.columnKey h child) :
    node parent < node child / 2 := by
  have hn : ¬ node child / 2 ≤ node parent := fun hn =>
    (not_lt_of_gt ho) ((column_child_lt_parent_minus_iff hc hp).mpr hn)
  omega

theorem column_plus_before_minus {h i : ℕ} {v w : VariablePosition h}
    (hi : i<h) (hv : AtLevel i true v) (hw : AtLevel i false w)
    (ho : TreePositions.columnKey h v < TreePositions.columnKey h w) : node v ≤ node w := by
  have ho' := ho
  rw [eq_plusPos_of_atLevel hv,eq_minusPos_of_atLevel hw,
    TreePositions.columnKey_plus_internal hi,TreePositions.columnKey_minus_internal hi] at ho'
  have he := TreePositions.key_endpoint_lt_of_phase_gt ho' (by decide)
  have hb : 0<2^(h-i) := by positivity
  rw [mul_lt_mul_iff_left₀ hb] at he
  rw [node_eq_level_node hv.1,node_eq_level_node hw.1]
  omega

theorem column_minus_before_plus {h i : ℕ} {v w : VariablePosition h}
    (hi : i<h) (hv : AtLevel i false v) (hw : AtLevel i true w)
    (ho : TreePositions.columnKey h v < TreePositions.columnKey h w) : node v < node w := by
  have ho' := ho
  rw [eq_minusPos_of_atLevel hv,eq_plusPos_of_atLevel hw,
    TreePositions.columnKey_minus_internal hi,TreePositions.columnKey_plus_internal hi] at ho'
  have he := TreePositions.key_endpoint_le ho'
  have hb : 0<2^(h-i) := by positivity
  rw [mul_le_mul_iff_left₀ hb] at he
  rw [node_eq_level_node hv.1,node_eq_level_node hw.1]
  omega

end OrderedRemoval.Concrete
