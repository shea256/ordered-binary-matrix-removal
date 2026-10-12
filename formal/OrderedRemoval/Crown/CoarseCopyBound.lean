import OrderedRemoval.Crown.ZeroLocalization
import OrderedRemoval.Crown.HostSampledSelection
import OrderedRemoval.Rectangular.CountingInjection

namespace OrderedRemoval.Crown
noncomputable section
open Concrete

def concreteMatrix (h : ℕ) : BinaryMatrix (OrderedHost.size h) :=
  matrix (OrderedHost.rowIndex h) (OrderedHost.columnIndex h)

def copyOfIndices {h : ℕ} (r : Fin 3 → Fin (OrderedHost.size h))
    (c : Fin 3 → Fin (OrderedHost.size h)) (hr : StrictMono r) (hc : StrictMono c)
    (he : ∀ i j, concreteMatrix h (r i) (c j)=fixedH i j) : Copy h where
  rows := (OrderedHost.rowIndex h).symm ∘ r
  cols := (OrderedHost.columnIndex h).symm ∘ c
  rowIncreasing := by simpa only [Function.comp_def,Equiv.apply_symm_apply] using hr
  colIncreasing := by simpa only [Function.comp_def,Equiv.apply_symm_apply] using hc
  entry_eq := he

def indexedZeroCells (h : ℕ) :
    Finset (Fin (OrderedHost.size h) × Fin (OrderedHost.size h)) :=
  (zeroCells h).image (fun p => (OrderedHost.rowIndex h p.1,OrderedHost.columnIndex h p.2))

theorem card_indexedZeroCells_le (h : ℕ) : (indexedZeroCells h).card ≤ 2*2^h :=
  Finset.card_image_le.trans (card_zeroCells_le h)

/-- Unconditional all-copy bound for the 3×3 crown. -/
theorem copyCount_le (h : ℕ) :
    copyCount (concreteMatrix h) ≤ 2*2^h*(OrderedHost.size h)^4 := by
  classical
  have hc : (orderedCopies (concreteMatrix h)).card ≤
      (indexedZeroCells h).card*(OrderedHost.size h)^4 := by
    apply Rectangular.CopyBound.card_le_card_mul_pow (r:=2) (c:=2) _ 1 1
    intro rc hrc
    have he : ∀ i j, concreteMatrix h (rc.1.val i) (rc.2.val j)=fixedH i j := by
      simpa [orderedCopies] using hrc
    have hz := (copyOfIndices rc.1.val rc.2.val rc.1.property rc.2.property he).zero_localization
    apply Finset.mem_image.mpr
    refine ⟨((OrderedHost.rowIndex h).symm (rc.1.val 1),
      (OrderedHost.columnIndex h).symm (rc.2.val 1)), ?_, ?_⟩
    · simpa [zeroCells,copyOfIndices] using hz
    · simp
  exact hc.trans (Nat.mul_le_mul_right _ (card_indexedZeroCells_le h))

end
end OrderedRemoval.Crown
