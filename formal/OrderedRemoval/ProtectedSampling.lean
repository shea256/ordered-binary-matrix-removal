import OrderedRemoval.Propagation

/-!
# Finite protected-sample counting and its propagation consequence

The counting argument makes no independence assumption between protected
cells. It allows repetitions in the sample list and in the edit list.
The concrete host's incidence bound remains a hypothesis, not a formalized
property of the host. For the alternate three-seed sampler described in
formal/README.md the intended parameters are samples.length = m^3,
frequency = m, edits.length < m^2. The paper instead uses many representatives
chosen independently conditional on the leaf; its outcome count differs.
-/

namespace OrderedRemoval.ProtectedSampling

theorem count_or_le {α : Type} (samples : List α) (p q : α → Bool) :
    samples.countP (fun s => p s || q s) ≤
      samples.countP p + samples.countP q := by
  induction samples with
  | nil => simp
  | cons s samples ih =>
    cases hp : p s <;> cases hq : q s <;>
      simp_all <;> omega

/-- Union bound in integer form, valid even for correlated incidences. -/
theorem union_bound {Sample Cell : Type}
    (samples : List Sample) (edits : List Cell) (touch : Cell → Sample → Bool) :
    samples.countP (fun s => edits.any (fun e => touch e s)) ≤
      (edits.map (fun e => samples.countP (touch e))).sum := by
  induction edits with
  | nil => simp
  | cons e edits ih =>
    have h := count_or_le samples (touch e) (fun s => edits.any (fun f => touch f s))
    simp only [List.any_cons, List.map_cons, List.sum_cons]
    omega

theorem sum_frequency_bound {Sample Cell : Type}
    (samples : List Sample) (edits : List Cell)
    (touch : Cell → Sample → Bool) (frequency : Nat)
    (hfrequency : ∀ e ∈ edits, samples.countP (touch e) ≤ frequency) :
    (edits.map (fun e => samples.countP (touch e))).sum ≤ edits.length * frequency := by
  induction edits with
  | nil => simp
  | cons e edits ih =>
    have he := hfrequency e (by simp)
    have ht := ih (fun f hf => hfrequency f (by simp [hf]))
    simp only [List.map_cons, List.sum_cons, List.length_cons, Nat.add_mul]
    omega

/-- Fewer possible hits than samples leaves at least one untouched sample. -/
theorem exists_untouched {Sample Cell : Type}
    (samples : List Sample) (edits : List Cell)
    (touch : Cell → Sample → Bool) (frequency : Nat)
    (hfrequency : ∀ e ∈ edits, samples.countP (touch e) ≤ frequency)
    (hbudget : edits.length * frequency < samples.length) :
    ∃ s ∈ samples, ∀ e ∈ edits, touch e s = false := by
  have hbound := union_bound samples edits touch
  have hsum := sum_frequency_bound samples edits touch frequency hfrequency
  have hless : samples.countP (fun s => edits.any (fun e => touch e s)) <
      samples.length := by omega
  have hnotall : ¬ ∀ s ∈ samples, edits.any (fun e => touch e s) = true := by
    intro hall
    have heq := List.countP_eq_length.mpr hall
    omega
  classical
  apply Classical.byContradiction
  intro hnone
  apply hnotall
  intro s hs
  cases hvalue : edits.any (fun e => touch e s) with
  | false =>
    exfalso
    apply hnone
    refine ⟨s, hs, ?_⟩
    intro e he
    by_cases hit : touch e s = true
    · have hany : edits.any (fun f => touch f s) = true :=
        List.any_eq_true.mpr ⟨e, he, hit⟩
      simp [hvalue] at hany
    · exact Bool.eq_false_iff.mpr hit
  | true => rfl

/-- Protected incidence bounds plus arbitrary-bit propagation force a body.
The host-specific extension of that body to an ordered H copy is separate. -/
theorem exists_body_of_small_edit_set {Sample Cell : Type}
    (samples : List Sample) (edits : List Cell)
    (touch : Cell → Sample → Bool) (frequency h : Nat)
    (plus minus crossPlus crossMinus : Sample → Nat → Bool)
    (hfrequency : ∀ e ∈ edits, samples.countP (touch e) ≤ frequency)
    (hbudget : edits.length * frequency < samples.length)
    (hroot : ∀ s ∈ samples, (∀ e ∈ edits, touch e s = false) →
      plus s 0 = true ∧ minus s 0 = false)
    (hshared : ∀ s ∈ samples, plus s h = minus s h) :
    ∃ s ∈ samples, (∀ e ∈ edits, touch e s = false) ∧
      ∃ i, i < h ∧ Propagation.EdgeBody
        (plus s) (minus s) (crossPlus s) (crossMinus s) i := by
  obtain ⟨s, hs, hclean⟩ := exists_untouched samples edits touch frequency hfrequency hbudget
  obtain ⟨hp, hm⟩ := hroot s hs hclean
  exact ⟨s, hs, hclean, Propagation.exists_body
    (plus s) (minus s) (crossPlus s) (crossMinus s) h hp hm (hshared s hs)⟩

end OrderedRemoval.ProtectedSampling
