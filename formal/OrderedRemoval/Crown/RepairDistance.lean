import OrderedRemoval.Crown.OrderedSampledSelection
import OrderedRemoval.Crown.SamplingFrequency

namespace OrderedRemoval.Crown
noncomputable section
open Concrete TreeSampling

/-- Every H-free repair of the 3×3 host changes at least m² cells. The inherited
three-seed guard set includes both m-sized subgroups on each anchor axis; completion uses one. Its marginal is 1/m (not 1/(2m)), still giving the needed cell bound. -/
theorem hammingDistance_ge {h n : ℕ} (hh : 1 ≤ h)
    (er ec : Position h ≃ Fin n) (ha : SampledSelection.AxisConditions er ec)
    (B : BinaryMatrix n) (hfree : HFree B) :
    (2 ^ h) ^ 2 ≤ hammingDistance (matrix er ec) B := by
  classical
  by_contra hn
  have hsmall : (Finset.univ.filter (fun e : Fin n × Fin n =>
      matrix er ec e.1 e.2 ≠ B e.1 e.2)).card < (2 ^ h) ^ 2 := by
    simpa only [hammingDistance] using Nat.lt_of_not_ge hn
  have hΩ : 0 < Fintype.card (Seeds (2 ^ h)) := by rw [card_seeds]; positivity
  obtain ⟨s,hs⟩ := Sampling.exists_agreement_of_changed_card_lt
    (fun e : Fin n × Fin n => matrix er ec e.1 e.2)
    (fun e : Fin n × Fin n => B e.1 e.2)
    (fun s : Seeds (2 ^ h) => fun e => e ∈
      (SampledSelection.selection hh er ec ha s.1 s.2.1 s.2.2).guards h)
    (fun _ => True) (2 ^ h) hΩ
    (fun e _ => SampledSelection.selection_guard_frequency hh er ec ha e) hsmall
  exact not_HFree_of_agree
    (SampledSelection.selection_valid hh er ec ha s.1 s.2.1 s.2.2)
    (fun e he => hs e True.intro he) hfree

/-- Unconditional repair theorem for the independently ordered square host. -/
theorem concrete_repair_lower_bound (h : ℕ) (hh : 1 ≤ h)
    (B : BinaryMatrix (OrderedHost.size h)) (hfree : HFree B) :
    (2 ^ h) ^ 2 ≤ hammingDistance
      (matrix (OrderedHost.rowIndex h) (OrderedHost.columnIndex h)) B :=
  hammingDistance_ge hh _ _ (OrderedHost.sampledAxisConditions h) B hfree

end
end OrderedRemoval.Crown
