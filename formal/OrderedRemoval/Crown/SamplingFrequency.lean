import OrderedRemoval.Crown.SampledSelection
import OrderedRemoval.HostRepairDistance

namespace OrderedRemoval.Crown.SampledSelection
noncomputable section
open Concrete HostSampledPath HostSampling TreeSampling Concrete.SampledSelection

/-- The actual constant-offset anchor frame is chosen by its row/column seeds. -/
theorem frame_chosen {h n : ℕ} (er ec : Position h ≃ Fin n)
    (ha : AxisConditions er ec) (s : Seeds (2 ^ h)) (t : Mode h) :
    FrameChosen er ec s (frame er ec ha t s.2.1 s.2.2) := by
  constructor
  · intro u
    simp [frame, SelectedAnchor.frame, sampleDepth]
  · intro v
    simp [frame, SelectedAnchor.frame, sampleDepth]
  · intro u
    exact rowChosen_path_anchor er s t u
  · intro v
    exact colChosen_path_anchor ec s t v

/-- Every actual path point and anchor frame obeys the uniform sampler's
coordinate equations. This is separate from all matrix-entry claims. -/
theorem selection_chosen {h n : ℕ} (hh : 1 ≤ h) (er ec : Position h ≃ Fin n)
    (ha : AxisConditions er ec) (s : Seeds (2 ^ h)) :
    PathChosen er ec s (selection hh er ec ha s.1 s.2.1 s.2.2) := by
  constructor
  · intro i hi
    simpa only [selection, path_of_le hi] using rowChosen_path er i hi true s
  · intro i hi
    simpa only [selection, path_of_le hi] using rowChosen_path er i hi false s
  · intro i hi
    simpa only [selection, path_of_le hi] using colChosen_path ec i hi true s
  · intro i hi
    simpa only [selection, path_of_le hi] using colChosen_path ec i hi false s
  · exact rowChosen_path_dummy er s
  · exact colChosen_path_dummy ec s
  · simp [selection, HostSampledPath.dummy, sampleDepth]
  · simp [selection, HostSampledPath.dummy, sampleDepth]
  · simpa only [selection, Equiv.symm_apply_apply, path_of_le (Nat.zero_le h)] using
      protected_path_roots h true true s.1 s.2.1 s.2.2
  · simpa only [selection, Equiv.symm_apply_apply, path_of_le (Nat.zero_le h)] using
      protected_path_roots h false false s.1 s.2.1 s.2.2
  · intro i hi
    exact frame_chosen er ec ha s _
  · intro i hi
    exact frame_chosen er ec ha s _
  · intro i hi
    exact frame_chosen er ec ha s _
  · intro i hi
    exact frame_chosen er ec ha s _

/-- Each fixed guarded cell occupies at most the prescribed `1/m²` fraction
of the three-seed sample space, for the actual selected paths. -/
theorem selection_guard_frequency {h n : ℕ} (hh : 1 ≤ h)
    (er ec : Position h ≃ Fin n) (ha : AxisConditions er ec)
    (rc : Fin n × Fin n) :
    (Finset.univ.filter fun s : Seeds (2 ^ h) =>
      rc ∈ (selection hh er ec ha s.1 s.2.1 s.2.2).guards h).card * (2 ^ h) ^ 2 ≤
        Fintype.card (Seeds (2 ^ h)) :=
  path_guard_frequency er ec
    (fun s => selection hh er ec ha s.1 s.2.1 s.2.2)
    (fun s => selection_chosen hh er ec ha s) rc


end
end OrderedRemoval.Crown.SampledSelection
