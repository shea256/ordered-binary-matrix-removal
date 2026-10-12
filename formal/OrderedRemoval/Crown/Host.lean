import OrderedRemoval.Crown.Model
import OrderedRemoval.Rectangular.Host
import OrderedRemoval.ConcreteCopies

namespace OrderedRemoval.Crown
open Concrete

abbrev modeRank := @Rectangular.modeRank
abbrev modeOrder := Rectangular.modeOrder
abbrev topVariable := @Rectangular.topVariable

/-- The formal host uses two consecutive twin subgroups on each anchor axis.
Thus each mode has one anchor block of size 2m, and n=(14h+2)m. This padded
variant proves the qualitative 3×3 theorem; it is not the n=(8h+2)m family
used for the sharper written exact enumeration. -/
def host {h : ℕ} (r c : Position h) : Bool :=
  match r,c with
  | .inl (t,_,_), .inl (u,_,_) => decide (t=u)
  | .inl (t,_,_), .inr (.inl c) => decide (topVariable t c)
  | .inl (t,_,_), .inr (.inr _) => decide (2 ≤ kind t)
  | .inr (.inl r), .inl (t,_,_) => decide (rowRole t 0 (.inr (.inl r)))
  | .inr (.inr _), .inl (t,_,_) => decide (kind t < 2)
  | .inr (.inl r), .inr (.inl c) => variableEntry r c
  | .inr _, .inr _ => true

theorem top_on_role {h : ℕ} (t : Mode h) (j : Fin 2) (c : Position h)
    (hc : colRole t j c) (u : Fin 2) (x : Fin (2^h)) :
    host (.inl (t,u,x)) c = decide (j.val=1) := by
  have he := Rectangular.top_on_role t j c hc u x
  rcases c with a | (c | d)
  · simp [colRole] at hc
  · exact he
  · exact he

theorem rows_same_mode {h : ℕ} (t : Mode h) (u v : Fin 2)
    (x y : Fin (2^h)) (c : Position h) :
    host (.inl (t,u,x)) c=host (.inl (t,v,y)) c := by
  rcases c with a | (c | d) <;> rfl

theorem cols_same_mode {h : ℕ} (t : Mode h) (u v : Fin 2)
    (x y : Fin (2^h)) (r : Position h) :
    host r (.inl (t,u,x))=host r (.inl (t,v,y)) := by
  rcases r with a | (r | d) <;> rfl

theorem bottom_on_role {h : ℕ} (t : Mode h) (j : Fin 2) (r : Position h)
    (hr : rowRole t j r) (g : Fin 2) (x : Fin (2^h)) :
    host r (.inl (t,g,x)) = decide (j.val=0) := by
  rcases r with a | (r | d)
  · simp [rowRole] at hr
  · fin_cases j
    · change rowRole t 0 (.inr (.inl r)) at hr
      simp [host,hr]
    · have hn : ¬rowRole t 0 (.inr (.inl r)) := fun h₀ => rowRole_disjoint t _ ⟨h₀,hr⟩
      simp [host,hn]
  · have hk := kind_lt t
    fin_cases j <;> interval_cases he : kind t <;> simp_all [rowRole,host]

theorem nonanchor_eq {h : ℕ} (r c : Position h)
    (hr : ¬ IsAnchor r) (hc : ¬ IsAnchor c) :
    host r c=Rectangular.host r c := by
  rcases r with a | (r | d) <;> rcases c with b | (c | e) <;>
    simp_all [IsAnchor,host,Rectangular.host]

end OrderedRemoval.Crown
