import OrderedRemoval.HostStructure

namespace OrderedRemoval.Concrete

set_option maxHeartbeats 2000000

def nonanchorClass {h : ℕ} : Position h → ℕ
  | .inl _ => 2*h+2
  | .inr (.inl v) => v.1.val
  | .inr (.inr _) => 2*h+1

def positionNode {h : ℕ} : Position h → ℕ
  | .inr (.inl v) => node v
  | _ => 0

def classAt (h i : ℕ) (s : Bool) : ℕ :=
  if i = h ∨ s = true then 2*i else 2*i+1

structure Support where
  cls : ℕ
  parity : Option ℕ

def Support.Holds (S : Support) {h : ℕ} (x : Position h) : Prop :=
  nonanchorClass x = S.cls ∧ (S.parity = none ∨ S.parity = some (positionNode x % 2))

def rowSupport {h : ℕ} (t : Mode h) (j : Fin 2) : Support :=
  if kind t = 0 then
    ⟨classAt h (if j.val = 0 then level t else level t-1) true, none⟩
  else if kind t = 1 then
    ⟨classAt h (if j.val = 0 then level t-1 else level t) false, none⟩
  else if j.val = 1 then ⟨2*h+1, none⟩
  else ⟨classAt h (level t) (decide (kind t < 4)), some (kind t % 2)⟩

def colSupport {h : ℕ} (t : Mode h) (j : Fin 2) : Support :=
  if kind t < 2 then
    if j.val = 0 then ⟨2*h+1, none⟩
    else ⟨classAt h (level t-1) (decide (kind t = 0)), none⟩
  else if kind t < 4 then
    if j.val = 0 then ⟨classAt h (level t-1) true, none⟩
    else ⟨classAt h (level t) true, some (kind t % 2)⟩
  else
    if j.val = 0 then ⟨classAt h (level t) false, some (kind t % 2)⟩
    else ⟨classAt h (level t-1) false, none⟩

theorem atLevel_iff_class {h i : ℕ} (_hi : i ≤ h) (s : Bool)
    (v : VariablePosition h) :
    AtLevel i s v ↔ v.1.val = classAt h i s := by
  have hv := v.1.isLt
  cases s <;> simp [AtLevel, classAt, depth, plus] <;> (try split_ifs) <;> omega

theorem rowRole_support {h : ℕ} (t : Mode h) (j : Fin 2) (x : Position h) :
    rowRole t j x ↔ (rowSupport t j).Holds x := by
  have hl := level_le t
  have hp := level_pos t
  have hk := kind_lt t
  have hj := j.isLt
  rcases x with a | (v | d)
  · simp only [rowRole, Support.Holds, nonanchorClass]
    unfold rowSupport classAt
    split_ifs <;> simp_all <;> omega
  · have hv := v.1.isLt
    simp only [rowRole, Support.Holds, nonanchorClass, positionNode]
    unfold rowSupport classAt
    split_ifs <;> simp_all [AtLevel, depth, plus] <;> omega
  · simp only [rowRole, Support.Holds, nonanchorClass, positionNode]
    unfold rowSupport classAt
    split_ifs <;> simp_all <;> omega

theorem colRole_support {h : ℕ} (t : Mode h) (j : Fin 2) (x : Position h) :
    colRole t j x ↔ (colSupport t j).Holds x := by
  have hl := level_le t
  have hp := level_pos t
  have hk := kind_lt t
  have hj := j.isLt
  rcases x with a | (v | d)
  · simp only [colRole, Support.Holds, nonanchorClass]
    unfold colSupport classAt
    split_ifs <;> simp_all <;> omega
  · have hv := v.1.isLt
    simp only [colRole, Support.Holds, nonanchorClass, positionNode]
    unfold colSupport classAt
    split_ifs <;> simp_all [AtLevel, depth, plus] <;> omega
  · simp only [colRole, Support.Holds, nonanchorClass, positionNode]
    unfold colSupport classAt
    split_ifs <;> simp_all <;> omega

theorem rowRole_same_class {h : ℕ} {t : Mode h} {j : Fin 2} {x y : Position h}
    (hx : rowRole t j x) (hy : rowRole t j y) :
    nonanchorClass x = nonanchorClass y :=
  ((rowRole_support t j x).mp hx).1.trans ((rowRole_support t j y).mp hy).1.symm

theorem colRole_same_class {h : ℕ} {t : Mode h} {j : Fin 2} {x y : Position h}
    (hx : colRole t j x) (hy : colRole t j y) :
    nonanchorClass x = nonanchorClass y :=
  ((colRole_support t j x).mp hx).1.trans ((colRole_support t j y).mp hy).1.symm

/-- A whole support cannot precede a parity half of the same variable class. -/
theorem row_whole_not_before_half {h : ℕ} (t u : Mode h) (j k : Fin 2)
    (horder : modeRank t ≤ modeRank u)
    (hclass : (rowSupport t j).cls = (rowSupport u k).cls)
    (ht : (rowSupport t j).parity = none) :
    (rowSupport u k).parity = none := by
  have htlevel := level_le t
  have hulevel := level_le u
  have htpos := level_pos t
  have hupos := level_pos u
  have htKind := kind_lt t
  have huKind := kind_lt u
  have hj := j.isLt
  have hk := k.isLt
  rw [modeRank_eq, modeRank_eq] at horder
  interval_cases htk : kind t <;> interval_cases huk : kind u <;>
    fin_cases j <;> fin_cases k <;> simp_all [rowSupport, classAt]
  all_goals (try split_ifs at *) <;> (try simp_all) <;> omega

theorem col_whole_not_before_half {h : ℕ} (t u : Mode h) (j k : Fin 2)
    (horder : modeRank t ≤ modeRank u)
    (hclass : (colSupport t j).cls = (colSupport u k).cls)
    (ht : (colSupport t j).parity = none) :
    (colSupport u k).parity = none := by
  have htlevel := level_le t
  have hulevel := level_le u
  have htpos := level_pos t
  have hupos := level_pos u
  have htKind := kind_lt t
  have huKind := kind_lt u
  have hj := j.isLt
  have hk := k.isLt
  rw [modeRank_eq, modeRank_eq] at horder
  interval_cases htk : kind t <;> interval_cases huk : kind u <;>
    fin_cases j <;> fin_cases k <;> simp_all [colSupport, classAt]
  all_goals (try split_ifs at *) <;> (try simp_all) <;> omega

theorem support_forward {h : ℕ} (S T : Support) (x y : Position h)
    (hsx : S.Holds x) (hsy : S.Holds y) (hty : T.Holds y)
    (hwhole : S.parity = none → T.parity = none) : T.Holds x := by
  refine ⟨hsx.1.trans (hsy.1.symm.trans hty.1), ?_⟩
  rcases hsx.2 with hs0 | hs
  · exact Or.inl (hwhole hs0)
  rcases hsy.2 with hs0 | hs'
  · exact Or.inl (hwhole hs0)
  rcases hty.2 with ht0 | ht
  · exact Or.inl ht0
  · exact Or.inr (ht.trans (hs'.symm.trans hs))

theorem rowRole_forward {h : ℕ} {t u : Mode h} {j k : Fin 2} {x y : Position h}
    (horder : modeRank t ≤ modeRank u)
    (htx : rowRole t j x) (hty : rowRole t j y) (huy : rowRole u k y) :
    rowRole u k x := by
  rw [rowRole_support] at htx hty huy ⊢
  exact support_forward _ _ x y htx hty huy
    (row_whole_not_before_half t u j k horder (hty.1.symm.trans huy.1))

theorem colRole_forward {h : ℕ} {t u : Mode h} {j k : Fin 2} {x y : Position h}
    (horder : modeRank t ≤ modeRank u)
    (htx : colRole t j x) (hty : colRole t j y) (huy : colRole u k y) :
    colRole u k x := by
  rw [colRole_support] at htx hty huy ⊢
  exact support_forward _ _ x y htx hty huy
    (col_whole_not_before_half t u j k horder (hty.1.symm.trans huy.1))

end OrderedRemoval.Concrete
