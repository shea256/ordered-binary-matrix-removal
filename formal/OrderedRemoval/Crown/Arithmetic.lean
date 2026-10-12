import OrderedRemoval.Crown.ConcreteCopies
import OrderedRemoval.Rectangular.SupportArithmetic
import OrderedRemoval.Rectangular.RowArithmetic
import OrderedRemoval.Rectangular.VerticalArithmetic

namespace OrderedRemoval.Crown
open Concrete
set_option maxHeartbeats 4000000

theorem top_two_classes {h : ℕ} (A : Mode h) (b c : VariablePosition h)
    (hb : topVariable A b) (hc : topVariable A c) (hne : b.1≠c.1) :
    kind A=4 ∧ level A<h ∧
      ((b.1.val=2*(level A-1)+1 ∧ c.1.val=2*level A+1) ∨
       (c.1.val=2*(level A-1)+1 ∧ b.1.val=2*level A+1)) := by
  have hk := kind_lt A
  have hn : b.1.val≠c.1.val := fun he => hne (Fin.ext he)
  interval_cases he : kind A <;> simp_all [topVariable,Rectangular.topVariable]
  all_goals omega

theorem ordered_column_mono {h : ℕ} (r a b : VariablePosition h)
    (hcls : a.1=b.1) (ho : TreePositions.columnKey h a < TreePositions.columnKey h b)
    (ha : variableEntry r a=true) : variableEntry r b=true :=
  variableEntry_column_mono r a b hcls (column_same_class_node_le a b hcls ho) ha

/-- With one anchor and no anchor columns, the two positive column classes
force the earlier common positive column into one of those same classes. -/
theorem one_anchor_no_anchor_columns {h : ℕ} (A : Mode h)
    (r s a b c : VariablePosition h)
    (hb : topVariable A b) (hc : topVariable A c)
    (hra : variableEntry r a=true) (hrb : variableEntry r b=false)
    (hrc : variableEntry r c=true) (hsa : variableEntry s a=true)
    (hsb : variableEntry s b=true) (hsc : variableEntry s c=false)
    (hab : TreePositions.columnKey h a < TreePositions.columnKey h b)
    (hbc : TreePositions.columnKey h b < TreePositions.columnKey h c) : False := by
  have hne : b.1≠c.1 := by
    intro he
    have hx := ordered_column_mono s b c he hbc hsb
    simp [hsc] at hx
  obtain ⟨hk,hl,hclasses⟩ := top_two_classes A b c hb hc hne
  have hp := level_pos A
  have hrm := r.1.isLt
  have hsm := s.1.isLt
  have ham := a.1.isLt
  have hra' := variableEntry_class_shape hra
  have hrc' := variableEntry_class_shape hrc
  have hsa' := variableEntry_class_shape hsa
  have hsb' := variableEntry_class_shape hsb
  have haclass : a.1.val=b.1.val ∨ a.1.val=c.1.val := by omega
  rcases haclass with he | he
  · have hx := ordered_column_mono r a b (Fin.ext he) hab hra
    simp [hrb] at hx
  · have hx := ordered_column_mono s a c (Fin.ext he) (hab.trans hbc) hsa
    simp [hsc] at hx

/-- A third variable row cannot finish a crown below two crossing anchors. -/
theorem crossing_no_variable_bottom {h : ℕ} (A B : Mode h)
    (r a b c : VariablePosition h) (ho : modeRank A < modeRank B)
    (hac : topVariable A c) (hbc : topVariable B c)
    (haa : ¬ topVariable A a) (hba : topVariable B a)
    (hab : topVariable A b) (hbb : ¬ topVariable B b)
    (hra : variableEntry r a=true) (hrb : variableEntry r b=true)
    (hrc : variableEntry r c=false)
    (hacOrder : TreePositions.columnKey h a < TreePositions.columnKey h c) : False := by
  obtain ⟨hAk,hAl,hlevel,hBk,hcc,hcn,hbc',ha⟩ :=
    Rectangular.top_crossing A B c a b ho hac hbc haa hba hab hbb
  have hp := level_pos A
  have hbl := level_le B
  have hrm := r.1.isLt
  have hra' := variableEntry_class_shape hra
  have hrb' := variableEntry_class_shape hrb
  have he : a.1=c.1 := Fin.ext (by omega)
  have hx := ordered_column_mono r a c he hacOrder hra
  simp [hrc] at hx

/-- Opposite traces of two whole/parity supports on a fixed row class
force disjoint parity halves. -/
theorem opposite_roles_disjoint {h : ℕ} (A B : Mode h)
    (r s : VariablePosition h) (x : Position h) (hcls : r.1=s.1)
    (har : ¬ rowRole A 0 (.inr (.inl r)))
    (has : rowRole A 0 (.inr (.inl s)))
    (hbr : rowRole B 0 (.inr (.inl r)))
    (hbs : ¬ rowRole B 0 (.inr (.inl s)))
    (hax : rowRole A 0 x) (hbx : rowRole B 0 x) : False := by
  simp only [rowRole_support,Support.Holds,nonanchorClass,positionNode] at *
  have hv := congrArg Fin.val hcls
  rcases has with ⟨has,hasp | hasp⟩
  · exact har ⟨by omega,Or.inl hasp⟩
  rcases hbr with ⟨hbr,hbrp | hbrp⟩
  · exact hbs ⟨by omega,Or.inl hbrp⟩
  rcases hax.2 with ha0 | ha
  · simp_all
  rcases hbx.2 with hb0 | hb
  · simp_all
  have hn := Option.some.inj (hbrp.symm.trans (hb.trans (ha.symm.trans hasp)))
  exact har ⟨by omega,Or.inr (hasp.trans (congrArg some hn.symm))⟩

theorem opposite_roles_horizontal {h : ℕ} (A : Mode h)
    (r s : VariablePosition h) (hcls : r.1=s.1)
    (har : ¬ rowRole A 0 (.inr (.inl r)))
    (has : rowRole A 0 (.inr (.inl s))) : 2≤kind A := by
  have hk := kind_lt A
  have hp := level_pos A
  have hv := congrArg Fin.val hcls
  by_contra hn
  interval_cases he : kind A <;>
    simp_all [rowRole,AtLevel,depth,plus]

end OrderedRemoval.Crown
