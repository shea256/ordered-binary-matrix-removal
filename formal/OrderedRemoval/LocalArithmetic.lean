import Std

/-!
# Universal arithmetic certificates for the four-by-four proof audit

These are unbounded natural-number theorems, not bounded computations.
Their assumptions are the entry inequalities, order comparisons, and parity
constraints extracted in Sections 3 and 5 of proofs/four-by-four.md.

The extraction of those assumptions from every actual host copy is NOT
formalized by this file. In particular this is not the matrix removal theorem.
-/

namespace OrderedRemoval.LocalArithmetic

/-- Quotient and remainder order suffice to compare the original node labels. -/
theorem parity_order (p q : Nat)
    (hdiv : p / 2 ≤ q / 2) (hmod : p % 2 ≤ q % 2) : p ≤ q := by
  omega

/-- The two terminal crown traces would require crossing monotone thresholds. -/
theorem terminal_crown_impossible (p q plus minus : Nat)
    (hpPlus : p / 2 ≤ plus) (hpMinus : ¬ p / 2 < minus)
    (hqPlus : ¬ q / 2 ≤ plus) (hqMinus : q / 2 < minus) : False := by
  omega

/-- Balanced V-plus: the row order and bottom-right one contradict the zero. -/
theorem balanced_v_plus (p a b : Nat)
    (horder : p / 2 ≤ a) (hone : a ≤ b) (hzero : ¬ p / 2 ≤ b) : False := by
  omega

/-- Balanced V-minus: the bottom-right one contradicts the other constraints. -/
theorem balanced_v_minus (p a b : Nat)
    (horder : a ≤ p / 2) (hzero : ¬ a < b) (hone : p / 2 < b) : False := by
  omega

theorem balanced_w_plus (p q b : Nat)
    (horder : b ≤ q / 2) (hone : p / 2 ≤ b)
    (hparity : p % 2 = q % 2) (hzero : ¬ p ≤ q) : False := by
  omega

theorem balanced_w_minus_internal (p q b : Nat)
    (horder : q / 2 ≤ b) (hzero : ¬ p / 2 < b)
    (hparity : p % 2 = q % 2) (hone : p < q) : False := by
  omega

/-- At the common leaf the weak diagonal inequality allows exactly equality. -/
theorem balanced_w_minus_leaf (p q b : Nat)
    (horder : q / 2 ≤ b) (hzero : ¬ p / 2 < b)
    (hparity : p % 2 = q % 2) (hone : p ≤ q) :
    p = q ∧ b = p / 2 := by
  omega

theorem unbalanced_v_plus_parent (p a b : Nat)
    (hzero : ¬ p / 2 ≤ b) (hone : p / 2 ≤ a) (horder : a ≤ b) : False := by
  omega

theorem unbalanced_v_plus_own (p q b : Nat)
    (hzero : ¬ p / 2 ≤ b) (hone : p ≤ q) (horder : q / 2 < b) : False := by
  omega

theorem unbalanced_v_plus_leaf_minus (p a b : Nat)
    (hzero : ¬ p / 2 ≤ b) (hone : p / 2 < a) (horder : a < b) : False := by
  omega

theorem unbalanced_v_minus_own (p a b : Nat)
    (hzero : ¬ p < b) (hone : p < a) (horder : a ≤ b) : False := by
  omega

theorem unbalanced_v_minus_parent (p a b : Nat)
    (hzero : ¬ p < b) (hone : p / 2 < a) (horder : a < b / 2) : False := by
  omega

theorem unbalanced_w_plus_own (p q q' : Nat)
    (hzero : ¬ p ≤ q) (hone : p ≤ q') (horder : q' ≤ q) : False := by
  omega

theorem unbalanced_w_plus_parent (p q a : Nat)
    (hzero : ¬ p ≤ q) (hone : p / 2 ≤ a) (horder : a ≤ q / 2)
    (hparity : p % 2 = q % 2) : False := by
  omega

theorem unbalanced_w_plus_leaf_minus (p q a : Nat)
    (hzero : ¬ p ≤ q) (hone : p / 2 < a) (horder : a < q / 2) : False := by
  omega

theorem unbalanced_w_minus_parent_minus (p a b : Nat)
    (hzero : ¬ p / 2 < b) (hone : p / 2 < a) (horder : a ≤ b) : False := by
  omega

/-- The key nonleaf exclusion needs the ordered parity inequality, not equality. -/
theorem unbalanced_w_minus_internal (p q b : Nat)
    (hzero : ¬ p / 2 < b) (hone : p < q) (horder : q / 2 ≤ b)
    (hparityOrder : q % 2 ≤ p % 2) : False := by
  omega

/-- Shared leaves permit both parities but force the parent node. -/
theorem unbalanced_w_minus_leaf (p q b : Nat)
    (hzero : ¬ p / 2 < b) (hone : p ≤ q) (horder : q / 2 ≤ b) :
    b = p / 2 ∧ q / 2 = p / 2 := by
  omega

theorem unbalanced_w_minus_leaf_plus (p a b : Nat)
    (hzero : ¬ p / 2 < b) (hone : p / 2 ≤ a) (horder : a ≤ b) :
    b = p / 2 ∧ a = b := by
  omega

/-- A later nondummy leaf cannot be one at an earlier leaf column. -/
theorem last_row_leaf_case (p q r : Nat)
    (hzero : ¬ p ≤ q) (horder : p < r) (hone : r ≤ q) : False := by
  omega

/-- Nor can it be one at a plus-parent column strictly before p's parent. -/
theorem last_row_parent_case (p a r : Nat)
    (hzero : ¬ p / 2 ≤ a) (horder : p < r) (hone : r / 2 ≤ a) : False := by
  omega

/-- The parity-order hypothesis really is needed: p=2 and q=3 violate the
desired conclusion if it is dropped, at fixed parent node b=1. -/
theorem reversed_parity_arithmetic_witness :
    ¬ (2 / 2 < (1 : Nat)) ∧ 2 < (3 : Nat) ∧ 3 / 2 ≤ (1 : Nat) ∧
      ¬ (3 % 2 ≤ (2 : Nat) % 2) := by
  decide

end OrderedRemoval.LocalArithmetic
