/-
Adapted from OpenAI CopyBound.lean, commit
fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb (Apache-2.0).
The finite encoding lemma is unchanged.
-/
import Mathlib
namespace OrderedRemoval.CopyBound
/-- If one specified row-column pair in every member of a finite family belongs
 to `L`, the family is encoded by that cell and all remaining coordinates. -/
theorem card_le_card_mul_pow {k n : ℕ}
    (S : Finset
      ({f : Fin (k + 1) → Fin n // StrictMono f} ×
       {f : Fin (k + 1) → Fin n // StrictMono f}))
    (i j : Fin (k + 1)) (L : Finset (Fin n × Fin n))
    (hL : ∀ rc ∈ S, (rc.1.val i, rc.2.val j) ∈ L) :
    S.card ≤ L.card * n ^ (2 * k) := by
  classical
  let encode : S → L × ((Fin k → Fin n) × (Fin k → Fin n)) :=
    fun rc =>
      (⟨(rc.val.1.val i, rc.val.2.val j), hL rc.val rc.property⟩,
       (fun a => rc.val.1.val (i.succAbove a),
        fun b => rc.val.2.val (j.succAbove b)))
  have hinj : Function.Injective encode := by
    intro x y hxy
    apply Subtype.ext
    apply Prod.ext
    · apply Subtype.ext
      funext a
      rcases Fin.eq_self_or_eq_succAbove i a with ha | ⟨b, hb⟩
      · subst a
        exact congrArg (fun z => z.1.val.1) hxy
      · subst a
        exact congrArg (fun z => z.2.1 b) hxy
    · apply Subtype.ext
      funext a
      rcases Fin.eq_self_or_eq_succAbove j a with ha | ⟨b, hb⟩
      · subst a
        exact congrArg (fun z => z.1.val.2) hxy
      · subst a
        exact congrArg (fun z => z.2.2 b) hxy
  have hc := Fintype.card_le_of_injective encode hinj
  simpa only [Fintype.card_coe, Fintype.card_prod, Fintype.card_fun,
    Fintype.card_fin, two_mul, pow_add, mul_assoc] using hc


end OrderedRemoval.CopyBound
