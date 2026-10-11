/- The tree/body and roles are inherited from OpenAI's construction.
The asymmetric anchor entries and global mode order are the new 3×4 host.
The two row anchor subgroups are consecutive twins, giving one block of size 2m. -/
import OrderedRemoval.ConcreteHost
import OrderedRemoval.RoleSupports
import OrderedRemoval.Rectangular.Model

namespace OrderedRemoval.Rectangular
open Concrete

def modeRank {h : ℕ} (t : Mode h) : ℕ :=
  if 4 ≤ kind t then 2*(level t-1)+(kind t-4)
  else if 2 ≤ kind t then 2*h+2*(level t-1)+(kind t-2)
  else 4*h+2*(level t-1)+kind t

theorem modeRank_injective (h : ℕ) : Function.Injective (@modeRank h) := by
  intro t u he
  have htl := level_le t
  have hul := level_le u
  have htp := level_pos t
  have hup := level_pos u
  have htk := kind_lt t
  have huk := kind_lt u
  have het : t.val = 6*(level t-1)+kind t := by simp [level,kind]; omega
  have heu : u.val = 6*(level u-1)+kind u := by simp [level,kind]; omega
  apply Fin.ext
  unfold modeRank at he
  split_ifs at he <;> omega

abbrev modeOrder (h : ℕ) : LinearOrder (Mode h) :=
  LinearOrder.lift' modeRank (modeRank_injective h)

def topVariable {h : ℕ} (t : Mode h) (c : VariablePosition h) : Prop :=
  if kind t < 2 then c.1.val=2*(level t-1)+(if kind t=0 then 0 else 1)
  else if kind t < 4 then c.1.val=2*level t ∧ node c%2=kind t%2
  else c.1.val=2*(level t-1)+1 ∨
    (kind t=4 ∧ level t<h ∧ c.1.val=2*level t+1 ∧ node c%2=1)

instance {h : ℕ} (t : Mode h) (c : VariablePosition h) : Decidable (topVariable t c) := by
  unfold topVariable; split <;> (try split) <;> infer_instance

def host {h : ℕ} (r c : Position h) : Bool :=
  match r,c with
  | .inl (t,_,_), .inl (u,g,_) => decide (t=u ∧ g.val=0)
  | .inl (t,_,_), .inr (.inl c) => decide (topVariable t c)
  | .inl (t,_,_), .inr (.inr _) => decide (2 ≤ kind t)
  | .inr _, .inl (t,g,_) => decide (rowRole t g r)
  | .inr (.inl r), .inr (.inl c) => variableEntry r c
  | .inr _, .inr _ => true

theorem top_on_role {h : ℕ} (t : Mode h) (j : Fin 2) (c : Position h)
    (hc : colRole t j c) (u : Fin 2) (x : Fin (2^h)) :
    host (.inl (t,u,x)) c = decide (j.val=1) := by
  have hl := level_le t
  have hp := level_pos t
  have hk := kind_lt t
  rcases c with a | (c | d)
  · simp [colRole] at hc
  · have hmax := c.1.isLt
    interval_cases e : kind t <;> fin_cases j <;>
      simp_all [host,topVariable,colRole,AtLevel,depth,plus] <;> omega
  · interval_cases e : kind t <;> fin_cases j <;> simp_all [host,colRole]

theorem rows_same_mode {h : ℕ} (t : Mode h) (u v : Fin 2)
    (x y : Fin (2^h)) (c : Position h) :
    host (.inl (t,u,x)) c=host (.inl (t,v,y)) c := by
  rcases c with a | (c | d) <;> rfl

end OrderedRemoval.Rectangular
