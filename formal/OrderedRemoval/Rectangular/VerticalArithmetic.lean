import OrderedRemoval.Rectangular.RowArithmetic

namespace OrderedRemoval.Rectangular
open Concrete
set_option maxHeartbeats 2000000

/-- A vertical zero cannot have a later variable row carrying a one in the
same last column. The row is unrestricted; it need not occupy a named role. -/
theorem vertical_zero_later_impossible {h : ℕ} (t : Mode h)
    (r s d : VariablePosition h) (hk : kind t<2)
    (hr : rowRole t 0 (.inr (.inl r))) (hd : topVariable t d)
    (hz : variableEntry r d=false) (hs : variableEntry s d=true)
    (ho : TreePositions.rowKey h r < TreePositions.rowKey h s) : False := by
  have hp := level_pos t
  have hl := level_le t
  have hrm := r.1.isLt
  have hsm := s.1.isLt
  have hdm := d.1.isLt
  by_cases hcls : r.1=s.1
  · have he := variableEntry_row_antimono r s d hcls
      (row_same_class_node_le r s hcls ho) hs
    simp [hz] at he
  have hn : r.1.val≠s.1.val := fun he => hcls (Fin.ext he)
  have hshape := variableEntry_class_shape hs
  have hzero : ¬variableEntry r d=true := by simp [hz]
  have hrS := (rowRole_support t 0 (.inr (.inl r))).mp hr
  have hparent : level t-1≠h := by omega
  interval_cases he : kind t
  · have hr' : AtLevel ((level t-1)+1) true r := by
      simpa [rowRole,he,Nat.sub_add_cancel hp] using hr
    have hs' : AtLevel (level t-1) true s := by
      simp [rowSupport,classAt,he,Support.Holds,nonanchorClass] at hrS
      simp [topVariable,he] at hd
      simp [AtLevel,depth,plus]; omega
    have hbound := (row_plus_lt_iff hr' hs').mp ho
    simp [rowRole,AtLevel,depth,plus,he] at hr
    simp [topVariable,he] at hd
    rw [variableEntry_true_iff] at hs hzero
    simp [AtLevel,depth,plus] at hs'
    omega
  · have hr' : AtLevel (level t-1) false r := by simpa [rowRole,he] using hr
    have hs' : AtLevel ((level t-1)+1) false s := by
      simp [rowSupport,classAt,he,hparent,Support.Holds,nonanchorClass] at hrS
      simp [topVariable,he] at hd
      simp [AtLevel,depth,plus]; omega
    have hbound := (row_minus_lt_iff hs' hr').mp ho
    simp [rowRole,AtLevel,depth,plus,he] at hr
    simp [topVariable,he] at hd
    rw [variableEntry_true_iff] at hs hzero
    simp [AtLevel,depth,plus] at hs'
    omega

end OrderedRemoval.Rectangular
