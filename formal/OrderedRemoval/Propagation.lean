import Std

/-!
# All-depth Boolean propagation under arbitrary changes

This is the inherited four-body path argument, expressed using only core
Lean/Std. The Boolean sequences are completely arbitrary; no variable entry
is assumed unchanged. Opposite root bits and the common terminal bit force
one of the four P bodies. Dummy ones are explicit constants in the bodies.

This does not establish that every such body extends to an ordered H copy
in a repaired host, or establish the protected-cell sampling bound.
Those host connections remain separate proof obligations.
-/

namespace OrderedRemoval.Propagation

def Body (a b c d : Bool) : Prop :=
  a = true ∧ b = false ∧ c = true ∧ d = true

def EdgeBody (plus minus crossPlus crossMinus : Nat → Bool) (i : Nat) : Prop :=
  Body true (crossPlus i) true (plus i) ∨
  Body true (minus i) true (crossMinus i) ∨
  Body (crossPlus i) (plus (i+1)) true true ∨
  Body (minus (i+1)) (crossMinus i) true true

/-- A single P-free edge preserves the opposite signs. -/
theorem one_step (p m bp bm cp cm : Bool)
    (hp : p = true) (hm : m = false)
    (hvPlus : ¬ Body true bp true p)
    (hvMinus : ¬ Body true m true bm)
    (hwPlus : ¬ Body bp cp true true)
    (hwMinus : ¬ Body cm bm true true) :
    cp = true ∧ cm = false := by
  subst p
  subst m
  cases bp <;> cases bm <;> cases cp <;> cases cm <;>
    simp_all [Body]

/-- Induction over arbitrary path length, without a finite depth cutoff. -/
theorem propagate (plus minus crossPlus crossMinus : Nat → Bool) (h : Nat)
    (hrootPlus : plus 0 = true) (hrootMinus : minus 0 = false)
    (havoid : ∀ i, i < h → ¬ EdgeBody plus minus crossPlus crossMinus i) :
    ∀ i, i ≤ h → plus i = true ∧ minus i = false := by
  intro i
  induction i with
  | zero => exact fun _ => ⟨hrootPlus, hrootMinus⟩
  | succ i ih =>
    intro hi
    have hit : i < h := by omega
    obtain ⟨hp, hm⟩ := ih (by omega)
    exact one_step (plus i) (minus i) (crossPlus i) (crossMinus i)
      (plus (i+1)) (minus (i+1)) hp hm
      (fun hb => havoid i hit (Or.inl hb))
      (fun hb => havoid i hit (Or.inr (Or.inl hb)))
      (fun hb => havoid i hit (Or.inr (Or.inr (Or.inl hb))))
      (fun hb => havoid i hit (Or.inr (Or.inr (Or.inr hb))))

/-- The universal obstruction along the sampled path. -/
theorem exists_body (plus minus crossPlus crossMinus : Nat → Bool) (h : Nat)
    (hrootPlus : plus 0 = true) (hrootMinus : minus 0 = false)
    (hshared : plus h = minus h) :
    ∃ i, i < h ∧ EdgeBody plus minus crossPlus crossMinus i := by
  apply Classical.byContradiction
  intro hnone
  have havoid : ∀ i, i < h → ¬ EdgeBody plus minus crossPlus crossMinus i := by
    intro i hi hb
    exact hnone ⟨i, hi, hb⟩
  obtain ⟨hp, hm⟩ := propagate plus minus crossPlus crossMinus h
    hrootPlus hrootMinus havoid h (Nat.le_refl h)
  rw [hshared, hm] at hp
  cases hp

end OrderedRemoval.Propagation
