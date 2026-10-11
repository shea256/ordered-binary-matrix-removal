import OrderedRemoval.Model
import OrderedRemoval.CountingInjection
import OrderedRemoval.ZeroSetSize

namespace OrderedRemoval.Concrete
noncomputable section

/-- Reindex the raw zero set by the independent row and column enumerations. -/
def indexedZeroCells (h : ℕ) :
    Finset (Fin (OrderedHost.size h) × Fin (OrderedHost.size h)) :=
  (zeroCells h).image (fun p => (OrderedHost.rowIndex h p.1, OrderedHost.columnIndex h p.2))

theorem card_indexedZeroCells_le (h : ℕ) : (indexedZeroCells h).card ≤ 2*2^h :=
  (Finset.card_image_le).trans (card_zeroCells_le h)

/-- The universal localization theorem now bounds the actual ordered-copy count. -/
theorem copyCount_le (h : ℕ) :
    copyCount fixedH (matrix h) ≤ 2*2^h*(OrderedHost.size h)^6 := by
  classical
  have hc : (orderedCopies fixedH (matrix h)).card ≤
      (indexedZeroCells h).card * (OrderedHost.size h)^6 := by
    apply CopyBound.card_le_card_mul_pow (k:=3) _ 2 3
    intro rc hrc
    have he : ∀ i j, matrix h (rc.1.val i) (rc.2.val j)=AnchorClassification.H4 i j := by
      simpa [orderedCopies,fixedH_eq_H4] using hrc
    have hz := matrix_zero_localization rc.1.val rc.2.val rc.1.property rc.2.property he
    apply Finset.mem_image.mpr
    refine ⟨((OrderedHost.rowIndex h).symm (rc.1.val 2),
      (OrderedHost.columnIndex h).symm (rc.2.val 3)), ?_, ?_⟩
    · simpa [zeroCells] using hz
    · simp
  exact hc.trans (Nat.mul_le_mul_right _ (card_indexedZeroCells_le h))

end
end OrderedRemoval.Concrete
