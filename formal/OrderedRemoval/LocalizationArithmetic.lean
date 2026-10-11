import OrderedRemoval.LocalizationFrame
import OrderedRemoval.TreeComparisons

namespace OrderedRemoval.Concrete
set_option maxHeartbeats 2000000

/-- Arithmetic consequences of the concrete column order. -/
structure ColumnBounds {h : ℕ} (c d : VariablePosition h) : Prop where
  same : c.1.val/2=d.1.val/2 → node c ≤ node d
  minus_plus : c.1.val/2=d.1.val/2 → c.1.val%2=1 → d.1.val%2=0 → node c < node d
  child_parent : c.1.val/2=d.1.val/2+1 → node c/2 ≤ node d
  child_plus : c.1.val/2=d.1.val/2+1 → d.1.val%2=0 → node c/2 < node d
  parent_child : d.1.val/2=c.1.val/2+1 → node c ≤ node d/2
  minus_child : d.1.val/2=c.1.val/2+1 → c.1.val%2=1 → node c < node d/2

theorem atLevel_self_even {h : ℕ} (v : VariablePosition h) (hv : v.1.val%2=0) :
    AtLevel (v.1.val/2) true v := by
  simp [AtLevel,depth,plus,hv]

theorem atLevel_self_odd {h : ℕ} (v : VariablePosition h) (hv : v.1.val%2=1) :
    AtLevel (v.1.val/2) false v := by
  simp [AtLevel,depth,plus,hv]

theorem column_node_bounds {h : ℕ} (c d : VariablePosition h)
    (ho : TreePositions.columnKey h c < TreePositions.columnKey h d) : ColumnBounds c d := by
  have hc := c.1.isLt
  have hd := d.1.isLt
  have hcm : c.1.val%2=0 ∨ c.1.val%2=1 := by omega
  have hdm : d.1.val%2=0 ∨ d.1.val%2=1 := by omega
  constructor
  · intro he
    by_cases hcls : c.1=d.1
    · exact column_same_class_node_le c d hcls ho
    · have hne : c.1.val≠d.1.val := fun hh => hcls (Fin.ext hh)
      have hi : c.1.val/2<h := by omega
      rcases hcm with hm | hm
      · have hm' : d.1.val%2=1 := by omega
        exact column_plus_before_minus hi (atLevel_self_even c hm)
          (he ▸ atLevel_self_odd d hm') ho
      · have hm' : d.1.val%2=0 := by omega
        exact le_of_lt (column_minus_before_plus hi (atLevel_self_odd c hm)
          (he ▸ atLevel_self_even d hm') ho)
  · intro he hm hn
    have hi : c.1.val/2<h := by omega
    exact column_minus_before_plus hi (atLevel_self_odd c hm)
      (he ▸ atLevel_self_even d hn) ho
  · intro he
    rcases hdm with hm | hm
    · exact le_of_lt (column_child_before_plus he (atLevel_self_even d hm) ho)
    · exact (column_child_lt_parent_minus_iff he (atLevel_self_odd d hm)).mp ho
  · intro he hm
    exact column_child_before_plus he (atLevel_self_even d hm) ho
  · intro he
    rcases hcm with hm | hm
    · exact (column_parent_plus_lt_iff he (atLevel_self_even c hm)).mp ho
    · exact le_of_lt (column_minus_before_child he (atLevel_self_odd c hm) ho)
  · intro he hm
    exact column_minus_before_child he (atLevel_self_odd c hm) ho

/-- Before a nonleaf minus mode, an own-class column support must be a
minus parity half whose parity is no later in the revised mode order. -/
theorem earlier_minus_child_parity {h : ℕ} (A B : Mode h) (g : Fin 2)
    (c : VariablePosition h) (hB : 4 ≤ kind B) (hint : level B < h)
    (hc : colRole A g (.inr (.inl c))) (hclass : c.1.val=2*level B+1)
    (horder : modeRank A ≤ modeRank B) : node c%2 ≤ kind B%2 := by
  have hAl := level_le A
  have hBl := level_le B
  have hAp := level_pos A
  have hBp := level_pos B
  have hAk := kind_lt A
  have hBk := kind_lt B
  have hv := c.1.isLt
  rw [modeRank_eq,modeRank_eq] at horder
  interval_cases hkA : kind A <;> interval_cases hkB : kind B <;>
    fin_cases g <;> simp_all [colRole,AtLevel,depth,plus] <;> omega

/-- The mode/entry/order data of a non-dummy third column forces the fixed
zero to the leaf-to-parent-minus set. This covers both anchor-count cases. -/
theorem mode_zero_localization {h : ℕ} (A B : Mode h) (g : Fin 2)
    (r c d : VariablePosition h)
    (horder : modeRank A ≤ modeRank B)
    (hr : rowRole B 0 (.inr (.inl r))) (hd : colRole B 1 (.inr (.inl d)))
    (hc : colRole A g (.inr (.inl c)))
    (hone : variableEntry r c=true) (hzero : variableEntry r d=false)
    (ho : TreePositions.columnKey h c < TreePositions.columnKey h d) :
    r.1.val=2*h ∧ d.1.val+1=2*h ∧ node d=node r/2 ∧
      (c.1.val=2*h ∨ c.1.val+2=2*h) := by
  have hrmax := r.1.isLt
  have hcmax := c.1.isLt
  have hdmax := d.1.isLt
  have hBl := level_le B
  have hBp := level_pos B
  have hBk := kind_lt B
  have hz : ¬ variableEntry r d=true := by simp [hzero]
  rw [variableEntry_true_iff] at hone hz
  obtain ⟨hs,hmp,hcp,hcplus,hpc,hmchild⟩ := column_node_bounds c d ho
  have hpar : (4 ≤ kind B ∧ level B<h ∧ c.1.val=2*level B+1) →
      node c%2 ≤ kind B%2 := fun hh =>
    earlier_minus_child_parity A B g c hh.1 hh.2.1 hc hh.2.2 horder
  clear hc horder ho hzero A g
  have hrS := (rowRole_support B 0 (.inr (.inl r))).mp hr
  have hdS := (colRole_support B 1 (.inr (.inl d))).mp hd
  clear hr hd
  have hparent : level B-1 ≠ h := by omega
  have hhparent : h-1 ≠ h := by omega
  by_cases hleaf : level B=h <;> interval_cases hk : kind B <;>
    simp [rowSupport,colSupport,classAt,hk,hleaf,hparent,hhparent,
      Support.Holds,nonanchorClass,positionNode] at hrS hdS
  all_goals rcases hone with hone | hone | hone
  -- Instantiate only the order inequalities whose class premises hold.
  -- This avoids a large disjunction search over unused conditional bounds.
  all_goals
    try have hs' := (hs
      (by clear hz hs hmp hcp hcplus hpc hmchild hpar; omega))
    try have hmp' := (hmp
      (by clear hz hs hmp hcp hcplus hpc hmchild hpar; omega)
      (by clear hz hs hmp hcp hcplus hpc hmchild hpar; omega)
      (by clear hz hs hmp hcp hcplus hpc hmchild hpar; omega))
    try have hcp' := (hcp
      (by clear hz hs hmp hcp hcplus hpc hmchild hpar; omega))
    try have hcplus' := (hcplus
      (by clear hz hs hmp hcp hcplus hpc hmchild hpar; omega)
      (by clear hz hs hmp hcp hcplus hpc hmchild hpar; omega))
    try have hpc' := (hpc
      (by clear hz hs hmp hcp hcplus hpc hmchild hpar; omega))
    try have hmchild' := (hmchild
      (by clear hz hs hmp hcp hcplus hpc hmchild hpar; omega)
      (by clear hz hs hmp hcp hcplus hpc hmchild hpar; omega))
    try have hpar' := (hpar
      (by clear hz hs hmp hcp hcplus hpc hmchild hpar; omega))
    clear hs hmp hcp hcplus hpc hmchild hpar
    omega

end OrderedRemoval.Concrete
