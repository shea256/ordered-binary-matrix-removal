import OrderedRemoval.ConcreteHost

/-!
Concrete nonanchor entry and support facts. These statements concern the
host function itself, without assumed crown or comparability certificates.
-/

namespace OrderedRemoval.Concrete

theorem variableEntry_true_iff {h : ℕ} (r c : VariablePosition h) :
    variableEntry r c = true ↔
      (r.1.val = c.1.val ∧
        ((r.1.val % 2 = 0 ∧ node r ≤ node c) ∨
         (r.1.val % 2 = 1 ∧ node r < node c))) ∨
      (r.1.val = c.1.val + 2 ∧
        ((c.1.val % 2 = 0 ∧ node r / 2 ≤ node c) ∨
         (c.1.val % 2 = 1 ∧ node r / 2 < node c))) ∨
      (r.1.val = 2 * h ∧ c.1.val + 1 = 2 * h ∧ node r / 2 < node c) := by
  have hr := r.1.isLt
  have hc := c.1.isLt
  unfold variableEntry depth plus
  split_ifs <;> simp_all <;> omega

theorem variableEntry_class_shape {h : ℕ} {r c : VariablePosition h}
    (he : variableEntry r c = true) :
    r.1.val = c.1.val ∨ r.1.val = c.1.val + 2 ∨
      (r.1.val = 2 * h ∧ c.1.val + 1 = 2 * h) := by
  rcases (variableEntry_true_iff r c).mp he with h | h | h
  · exact Or.inl h.1
  · exact Or.inr (Or.inl h.1)
  · exact Or.inr (Or.inr ⟨h.1, h.2.1⟩)

theorem variableEntry_column_mono {h : ℕ} (r c d : VariablePosition h)
    (hclass : c.1 = d.1) (hn : node c ≤ node d)
    (hc : variableEntry r c = true) : variableEntry r d = true := by
  rw [variableEntry_true_iff] at hc ⊢
  have hv := congrArg Fin.val hclass
  omega

theorem variableEntry_row_antimono {h : ℕ} (r s c : VariablePosition h)
    (hclass : r.1 = s.1) (hn : node r ≤ node s)
    (hs : variableEntry s c = true) : variableEntry r c = true := by
  rw [variableEntry_true_iff] at hs ⊢
  have hv := congrArg Fin.val hclass
  omega

/-- Two distinct column classes seen with ones by a row form a chain edge,
or both belong to the three terminal classes. -/
theorem common_one_classes {h : ℕ} (r c d : VariablePosition h)
    (hc : variableEntry r c = true) (hd : variableEntry r d = true)
    (hne : c.1 ≠ d.1) :
    c.1.val + 2 = d.1.val ∨ d.1.val + 2 = c.1.val ∨
      (2 * h ≤ c.1.val + 2 ∧ 2 * h ≤ d.1.val + 2) := by
  have hsc := variableEntry_class_shape hc
  have hsd := variableEntry_class_shape hd
  have hcmax := c.1.isLt
  have hdmax := d.1.isLt
  have hne' : c.1.val ≠ d.1.val := fun he => hne (Fin.ext he)
  omega

/-- The abstract class graph consists of two chains with one terminal triangle. -/
theorem class_triangle_terminal (h a b c : ℕ)
    (ha : a ≤ 2*h) (hb : b ≤ 2*h) (hc : c ≤ 2*h)
    (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c)
    (eab : a+2=b ∨ b+2=a ∨ (2*h≤a+2 ∧ 2*h≤b+2))
    (eac : a+2=c ∨ c+2=a ∨ (2*h≤a+2 ∧ 2*h≤c+2))
    (ebc : b+2=c ∨ c+2=b ∨ (2*h≤b+2 ∧ 2*h≤c+2)) :
    2*h ≤ a+2 ∧ 2*h ≤ b+2 ∧ 2*h ≤ c+2 := by
  omega

/-- On the terminal triangle all rows that meet the leaf column are leaves,
and the leaf traces are nested. This rules out the required opposite traces. -/
theorem variable_crown_absent {h : ℕ}
    (r s t a b c : VariablePosition h)
    (hra : variableEntry r a = true) (hrb : variableEntry r b = false)
    (hrc : variableEntry r c = true)
    (hsa : variableEntry s a = true) (hsb : variableEntry s b = true)
    (hsc : variableEntry s c = false)
    (hta : variableEntry t a = false) (htb : variableEntry t b = true)
    (htc : variableEntry t c = true) : False := by
  have hab : a.1 ≠ b.1 := by
    intro he
    rcases le_total (node a) (node b) with hn | hn
    · have hx := variableEntry_column_mono r a b he hn hra
      simp [hrb] at hx
    · have hx := variableEntry_column_mono t b a he.symm hn htb
      simp [hta] at hx
  have hac : a.1 ≠ c.1 := by
    intro he
    rcases le_total (node a) (node c) with hn | hn
    · have hx := variableEntry_column_mono s a c he hn hsa
      simp [hsc] at hx
    · have hx := variableEntry_column_mono t c a he.symm hn htc
      simp [hta] at hx
  have hbc : b.1 ≠ c.1 := by
    intro he
    rcases le_total (node b) (node c) with hn | hn
    · have hx := variableEntry_column_mono s b c he hn hsb
      simp [hsc] at hx
    · have hx := variableEntry_column_mono r c b he.symm hn hrc
      simp [hrb] at hx
  have tri := class_triangle_terminal h a.1.val b.1.val c.1.val
    (by have := a.1.isLt; omega) (by have := b.1.isLt; omega)
    (by have := c.1.isLt; omega)
    (fun he => hab (Fin.ext he)) (fun he => hac (Fin.ext he))
    (fun he => hbc (Fin.ext he))
    (common_one_classes s a b hsa hsb hab)
    (common_one_classes r a c hra hrc hac)
    (common_one_classes t b c htb htc hbc)
  have hasLeaf : a.1.val = 2*h ∨ b.1.val = 2*h ∨ c.1.val = 2*h := by
    have ha := a.1.isLt
    have hb := b.1.isLt
    have hc := c.1.isLt
    have hab' : a.1.val ≠ b.1.val := fun he => hab (Fin.ext he)
    have hac' : a.1.val ≠ c.1.val := fun he => hac (Fin.ext he)
    have hbc' : b.1.val ≠ c.1.val := fun he => hbc (Fin.ext he)
    omega
  have leaf_of_one (x y : VariablePosition h) (hy : y.1.val = 2*h)
      (hxy : variableEntry x y = true) : x.1.val = 2*h := by
    have hx := x.1.isLt
    have hs := variableEntry_class_shape hxy
    omega
  rcases hasLeaf with ha | hb | hc
  · have hrs : r.1 = s.1 := Fin.ext ((leaf_of_one r a ha hra).trans
      (leaf_of_one s a ha hsa).symm)
    rcases le_total (node r) (node s) with hn | hn
    · have hx := variableEntry_row_antimono r s b hrs hn hsb
      simp [hrb] at hx
    · have hx := variableEntry_row_antimono s r c hrs.symm hn hrc
      simp [hsc] at hx
  · have hst : s.1 = t.1 := Fin.ext ((leaf_of_one s b hb hsb).trans
      (leaf_of_one t b hb htb).symm)
    rcases le_total (node s) (node t) with hn | hn
    · have hx := variableEntry_row_antimono s t c hst hn htc
      simp [hsc] at hx
    · have hx := variableEntry_row_antimono t s a hst.symm hn hsa
      simp [hta] at hx
  · have hrt : r.1 = t.1 := Fin.ext ((leaf_of_one r c hc hrc).trans
      (leaf_of_one t c hc htc).symm)
    rcases le_total (node r) (node t) with hn | hn
    · have hx := variableEntry_row_antimono r t b hrt hn htb
      simp [hrb] at hx
    · have hx := variableEntry_row_antimono t r a hrt.symm hn hra
      simp [hta] at hx

end OrderedRemoval.Concrete
