import OrderedRemoval.Rectangular.OrderedHost
import OrderedRemoval.LocalizationArithmetic

namespace OrderedRemoval.Rectangular
open Concrete
set_option maxHeartbeats 4000000

/-- All variable-column cases of the asymmetric localization argument.
The remaining vertical/dummy case is excluded using the full copy order. -/
theorem mode_zero_localization {h : ℕ} (t : Mode h)
    (r c d : VariablePosition h)
    (hr : rowRole t 0 (.inr (.inl r)))
    (hc : ¬ topVariable t c) (hd : topVariable t d)
    (hone : variableEntry r c=true) (hzero : variableEntry r d=false)
    (ho : TreePositions.columnKey h c < TreePositions.columnKey h d) :
    r.1.val=2*h ∧ d.1.val+1=2*h ∧ node d=node r/2 ∧ 4 ≤ kind t := by
  have hrmax := r.1.isLt
  have hcmax := c.1.isLt
  have hdmax := d.1.isLt
  have hl := level_le t
  have hp := level_pos t
  have hk := kind_lt t
  have hz : ¬ variableEntry r d=true := by simp [hzero]
  rw [variableEntry_true_iff] at hone hz
  obtain ⟨hs,hmp,hcp,hcplus,hpc,hmchild⟩ := column_node_bounds c d ho
  have hrS := (rowRole_support t 0 (.inr (.inl r))).mp hr
  clear hr ho hzero
  have hparent : level t-1 ≠ h := by omega
  have hhparent : h-1 ≠ h := by omega
  by_cases hleaf : level t=h <;> interval_cases he : kind t <;>
    simp [rowSupport,classAt,he,hleaf,hparent,hhparent,
      Support.Holds,nonanchorClass,positionNode] at hrS
  all_goals simp only [topVariable, he] at hc hd
  all_goals norm_num at hc hd
  all_goals rcases hone with hone | hone | hone
  all_goals try rcases hd with hd | hd
  all_goals
    try have hs' := (hs (by clear hz hs hmp hcp hcplus hpc hmchild; omega))
    try have hmp' := (hmp
      (by clear hz hs hmp hcp hcplus hpc hmchild; omega)
      (by clear hz hs hmp hcp hcplus hpc hmchild; omega)
      (by clear hz hs hmp hcp hcplus hpc hmchild; omega))
    try have hcp' := (hcp (by clear hz hs hmp hcp hcplus hpc hmchild; omega))
    try have hcplus' := (hcplus
      (by clear hz hs hmp hcp hcplus hpc hmchild; omega)
      (by clear hz hs hmp hcp hcplus hpc hmchild; omega))
    try have hpc' := (hpc (by clear hz hs hmp hcp hcplus hpc hmchild; omega))
    try have hmchild' := (hmchild
      (by clear hz hs hmp hcp hcplus hpc hmchild; omega)
      (by clear hz hs hmp hcp hcplus hpc hmchild; omega))
    clear hs hmp hcp hcplus hpc hmchild
    omega

end OrderedRemoval.Rectangular
