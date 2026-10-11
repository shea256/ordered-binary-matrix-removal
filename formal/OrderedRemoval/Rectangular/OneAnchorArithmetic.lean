import OrderedRemoval.Rectangular.RowArithmetic

namespace OrderedRemoval.Rectangular
open Concrete
set_option maxHeartbeats 600000

/-- No copy can have one anchor row and no anchor columns. This is a local
arithmetic statement about the actual variable entry rules and tree orders. -/
theorem one_anchor_no_anchor_columns {h : ℕ} (A : Mode h)
    (r s a b c d : VariablePosition h)
    (hat : topVariable A a) (hbt : ¬ topVariable A b)
    (hct : ¬ topVariable A c) (hdt : topVariable A d)
    (hra : variableEntry r a=true) (hrb : variableEntry r b=false)
    (hrc : variableEntry r c=true) (hrd : variableEntry r d=false)
    (_hsa : variableEntry s a=false) (hsb : variableEntry s b=true)
    (hsc : variableEntry s c=true) (hsd : variableEntry s d=true)
    (hco : TreePositions.columnKey h a < TreePositions.columnKey h d)
    (hro : TreePositions.rowKey h r < TreePositions.rowKey h s) : False := by
  have hrm := r.1.isLt
  have hsm := s.1.isLt
  have ham := a.1.isLt
  have hbm := b.1.isLt
  have hcm := c.1.isLt
  have hdm := d.1.isLt
  have hAp := level_pos A
  have hAl := level_le A
  have hAk := kind_lt A
  have hrs : r.1.val≠s.1.val := by
    intro he
    have he' := ordered_row_antimono r s (.inr (.inl b)) (by simp [IsAnchor])
      (Fin.ext he) hro hsb
    simp [host,hrb] at he'
  have had : a.1.val≠d.1.val := by
    intro he
    have he' := variableEntry_column_mono r a d (Fin.ext he)
      (column_same_class_node_le a d (Fin.ext he) hco) hra
    simp [hrd] at he'
  have hmode : kind A=4 ∧ level A<h ∧
      ((a.1.val=2*(level A-1)+1 ∧ d.1.val=2*level A+1) ∨
       (d.1.val=2*(level A-1)+1 ∧ a.1.val=2*level A+1)) := by
    interval_cases hk : kind A <;> simp_all [topVariable]
    all_goals omega
  obtain ⟨hkind,hlevel,hcases⟩ := hmode
  have hrsac := variableEntry_class_shape hra
  have hrscc := variableEntry_class_shape hrc
  have hsscc := variableEntry_class_shape hsc
  have hssdc := variableEntry_class_shape hsd
  have hcnot : c.1.val≠2*(level A-1)+1 := by
    simp [topVariable,hkind,hlevel] at hct
    exact hct.1
  have hrzero : ¬variableEntry r d=true := by simp [hrd]
  have hbzero : ¬variableEntry r b=true := by simp [hrb]
  have hchild : (r.1.val=2*(level A+1)+1 ∨
      (level A+1=h ∧ r.1.val=2*h)) → s.1.val=2*level A+1 → node r/2<node s := by
    intro hr hs
    apply row_child_before_minus_parent r s (i:=level A) _ _ hro
    · simp [AtLevel,depth,plus]; omega
    · simp [AtLevel,depth,plus,hs]; omega
  rcases hcases with ⟨ha,hd⟩ | ⟨hd,ha⟩
  · have hrclass : r.1.val=2*level A+1 := by omega
    have hbound := (column_node_bounds a d hco).minus_child (by omega) (by omega)
    have hrparent : node r/2<node a := by
      rw [variableEntry_true_iff] at hra
      omega
    apply hrzero
    rw [variableEntry_true_iff]
    exact Or.inl ⟨by omega,Or.inr ⟨by omega,by omega⟩⟩
  · have hrclass : r.1.val=2*(level A+1)+1 ∨
        (level A+1=h ∧ r.1.val=2*h) := by omega
    have hsclass : s.1.val=2*level A+1 := by omega
    have hbound := hchild hrclass hsclass
    simp [topVariable,hkind,hlevel] at hbt
    have hbclass : b.1.val=2*level A+1 := by
      have hsbshape := variableEntry_class_shape hsb
      omega
    have hsbnode : node s<node b := by
      rw [variableEntry_true_iff] at hsb
      omega
    apply hbzero
    rw [variableEntry_true_iff]
    rcases hrclass with hrclass | ⟨hleaf,hrclass⟩
    · exact Or.inr (Or.inl ⟨by omega,Or.inr ⟨by omega,by omega⟩⟩)
    · exact Or.inr (Or.inr ⟨hrclass,by omega,by omega⟩)

end OrderedRemoval.Rectangular
