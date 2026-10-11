import OrderedRemoval.Rectangular.ConcreteCopies
import OrderedRemoval.Rectangular.LocalizationArithmetic

namespace OrderedRemoval.Rectangular
open Concrete
set_option maxHeartbeats 4000000

/-- Whole classes and parity half-classes cannot have the crossing traces
110 and 011. This uses no assumption about mode order. -/
theorem role_laminar {h : ℕ} (A B : Mode h) (j k : Fin 2)
    (r s t : Position h) (har : rowRole A j r) (has : rowRole A j s)
    (hat : ¬ rowRole A j t) (hbr : ¬ rowRole B k r)
    (hbs : rowRole B k s) (hbt : rowRole B k t) : False := by
  simp only [rowRole_support,Support.Holds] at *
  obtain ⟨har,ha⟩ := har
  obtain ⟨has,hsa⟩ := has
  obtain ⟨hbs,hsb⟩ := hbs
  obtain ⟨hbt,hb⟩ := hbt
  rcases ha with ha | ha
  · exact hat ⟨by omega,Or.inl ha⟩
  rcases hb with hb | hb
  · exact hbr ⟨by omega,Or.inl hb⟩
  rcases hsa with hsa | hsa
  · exact hat ⟨by omega,Or.inl hsa⟩
  rcases hsb with hsb | hsb
  · exact hbr ⟨by omega,Or.inl hsb⟩
  have he : positionNode r%2=positionNode s%2 := Option.some.inj (ha.symm.trans hsa)
  exact hbr ⟨by omega,Or.inr (hsb.trans (congrArg some he.symm))⟩

/-- The only crossing pair with a variable common column and a variable
first-only column. All classes here are the literal carrier class numbers. -/
theorem top_crossing {h : ℕ} (A B : Mode h) (c a b : VariablePosition h)
    (ho : modeRank A < modeRank B)
    (hac : topVariable A c) (hbc : topVariable B c)
    (haa : ¬ topVariable A a) (hba : topVariable B a)
    (hab : topVariable A b) (hbb : ¬ topVariable B b) :
    kind A=4 ∧ level A<h ∧ level B=level A+1 ∧
    (4≤kind B ∨ kind B=1) ∧
    c.1.val=2*level A+1 ∧ node c%2=1 ∧
    b.1.val=2*(level A-1)+1 ∧
    ((a.1.val=2*level A+1 ∧ node a%2=0) ∨
     (kind B=4 ∧ level B<h ∧ a.1.val=2*level B+1 ∧ node a%2=1)) := by
  have hAl := level_le A
  have hBl := level_le B
  have hAp := level_pos A
  have hBp := level_pos B
  have hAk := kind_lt A
  have hBk := kind_lt B
  have hcm := c.1.isLt
  have ham := a.1.isLt
  have hbm := b.1.isLt
  interval_cases hA : kind A <;> interval_cases hB : kind B <;>
    simp [modeRank,topVariable,hA,hB] at * <;> omega

/-- A variable bottom row cannot supply 001,011,101 underneath a crossing
pair of anchor supports. Only class incidence is needed in this case. -/
theorem crossing_no_variable_bottom {h : ℕ} (A B : Mode h)
    (r c a b d : VariablePosition h) (ho : modeRank A < modeRank B)
    (hac : topVariable A c) (hbc : topVariable B c)
    (haa : ¬ topVariable A a) (hba : topVariable B a)
    (hab : topVariable A b) (hbb : ¬ topVariable B b)
    (had : ¬ topVariable A d) (hbd : ¬ topVariable B d)
    (hra : variableEntry r a=true) (hrb : variableEntry r b=true)
    (hrd : variableEntry r d=true) : False := by
  obtain ⟨hAk,hAl,hlevel,hBk,hcc,hcn,hbc,ha⟩ :=
    top_crossing A B c a b ho hac hbc haa hba hab hbb
  have hAp := level_pos A
  have hBp := level_pos B
  have hBl := level_le B
  have hBklt := kind_lt B
  have hrm := r.1.isLt
  have hdm := d.1.isLt
  have hra := variableEntry_class_shape hra
  have hrb := variableEntry_class_shape hrb
  have hrd := variableEntry_class_shape hrd
  simp [topVariable,hAk] at had
  interval_cases hk : kind B <;> simp_all [topVariable] <;> omega

/-- No third anchor support can contain both exclusive columns in the
variable-intersection crossing case. -/
theorem crossing_no_anchor_bottom {h : ℕ} (A B C : Mode h)
    (c a b : VariablePosition h) (ho : modeRank A < modeRank B)
    (hac : topVariable A c) (hbc : topVariable B c)
    (haa : ¬ topVariable A a) (hba : topVariable B a)
    (hab : topVariable A b) (hbb : ¬ topVariable B b)
    (hCa : topVariable C a) (hCb : topVariable C b) : False := by
  obtain ⟨hAk,hAl,hlevel,hBk,hcc,hcn,hbc,ha⟩ :=
    top_crossing A B c a b ho hac hbc haa hba hab hbb
  have hAp := level_pos A
  have hBp := level_pos B
  have hCp := level_pos C
  have hCl := level_le C
  have hCk := kind_lt C
  have ham := a.1.isLt
  have hbm := b.1.isLt
  interval_cases hk : kind C <;> simp_all [topVariable]
  all_goals omega

/-- When the common first column is dummy, a final V row cannot produce
001 after the two W rows produce both exclusive traces in its own class. -/
theorem dummy_crossing_no_anchor_bottom {h : ℕ} (A B C : Mode h)
    (a b d : VariablePosition h) (hAk : 2≤kind A) (hBk : 2≤kind B)
    (hCk : kind C<2)
    (haa : ¬ topVariable A a) (hba : topVariable B a)
    (hab : topVariable A b) (hbb : ¬ topVariable B b)
    (had : ¬ topVariable A d) (hbd : ¬ topVariable B d)
    (hCa : topVariable C a) (hCb : topVariable C b)
    (hCd : topVariable C d) : False := by
  have hAp := level_pos A
  have hBp := level_pos B
  have hCp := level_pos C
  have hAkl := kind_lt A
  have hBkl := kind_lt B
  interval_cases hkA : kind A <;> interval_cases hkB : kind B <;>
    interval_cases hkC : kind C <;> simp_all [topVariable]

end OrderedRemoval.Rectangular
