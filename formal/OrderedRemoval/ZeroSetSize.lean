import OrderedRemoval.ZeroLocalization

namespace OrderedRemoval.Concrete

theorem inZeroSet_variables {h : ℕ} {x y : Position h} (hz : InZeroSet x y) :
    ∃ r d : VariablePosition h, x=.inr (.inl r) ∧ y=.inr (.inl d) ∧
      r.1.val=2*h ∧ d.1.val+1=2*h ∧ node d=node r/2 := by
  rcases x with a | (r | u) <;> rcases y with b | (d | v) <;> simp_all [InZeroSet]

theorem zero_coordinate_quotients {h : ℕ} (r d : VariablePosition h)
    (hr : r.1.val=2*h) (hd : d.1.val+1=2*h) (hn : node d=node r/2) :
    d.2.val/2=r.2.val/2 := by
  have hw : h-d.1.val/2=1 := by omega
  simpa [node,depth,hr,hw] using hn

def variableCoordinate {h : ℕ} : Position h → Fin (2^h)
  | .inr (.inl v) => v.2
  | _ => ⟨0,by positivity⟩

/-- A localized zero is determined by its leaf and one parity bit. -/
def zeroCode {h : ℕ} (p : Position h × Position h) : Fin (2^h) × Fin 2 :=
  (variableCoordinate p.1, ⟨(variableCoordinate p.2).val%2,Nat.mod_lt _ (by decide)⟩)

theorem zeroCode_injective_on_zeros {h : ℕ} {x y : Position h × Position h}
    (hx : InZeroSet x.1 x.2) (hy : InZeroSet y.1 y.2) (he : zeroCode x=zeroCode y) : x=y := by
  rcases x with ⟨xr,xc⟩
  rcases y with ⟨yr,yc⟩
  obtain ⟨r,d,rfl,rfl,hr,hd,hn⟩ := inZeroSet_variables hx
  obtain ⟨s,e,rfl,rfl,hs,hec,heN⟩ := inZeroSet_variables hy
  have hrow : r.2=s.2 := congrArg Prod.fst he
  have hbit : d.2.val%2=e.2.val%2 := congrArg (fun z => z.2.val) he
  have hdq := zero_coordinate_quotients r d hr hd hn
  have heq := zero_coordinate_quotients s e hs hec heN
  have hrowv := congrArg Fin.val hrow
  have hrc : r=s := Prod.ext (Fin.ext (hr.trans hs.symm)) hrow
  have hdc : d=e := Prod.ext (Fin.ext (by omega)) (Fin.ext (by omega))
  simp [hrc,hdc]

def zeroCells (h : ℕ) : Finset (Position h × Position h) :=
  Finset.univ.filter (fun p => InZeroSet p.1 p.2)

/-- The quantitative zero-set bound needed for the coarse copy count. -/
theorem card_zeroCells_le (h : ℕ) : (zeroCells h).card ≤ 2*2^h := by
  have hinj : Set.InjOn (@zeroCode h) ↑(zeroCells h) := by
    intro x hx y hy he
    exact zeroCode_injective_on_zeros (by simpa [zeroCells] using hx)
      (by simpa [zeroCells] using hy) he
  calc
    (zeroCells h).card = ((zeroCells h).image zeroCode).card :=
      (Finset.card_image_of_injOn hinj).symm
    _ ≤ Fintype.card (Fin (2^h) × Fin 2) := Finset.card_le_univ _
    _ = 2*2^h := by simp [Nat.mul_comm]

end OrderedRemoval.Concrete
