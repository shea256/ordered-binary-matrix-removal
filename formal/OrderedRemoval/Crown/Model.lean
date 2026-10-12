import OrderedRemoval.Model

namespace OrderedRemoval.Crown
noncomputable section

abbrev Pattern := Fin 3 → Fin 3 → Bool

/-- The fixed ordered 3×3 crown, with both binary labels prescribed. -/
def fixedH : Pattern := ![![false,true,true], ![true,false,true], ![true,true,false]]

def orderedCopies {n : ℕ} (A : BinaryMatrix n) :
    Finset (IncreasingMap 3 n × IncreasingMap 3 n) := by
  classical
  exact Finset.univ.filter (fun rc => ∀ i j, A (rc.1.val i) (rc.2.val j)=fixedH i j)

def copyCount {n : ℕ} (A : BinaryMatrix n) : ℕ := (orderedCopies A).card
def HFree {n : ℕ} (A : BinaryMatrix n) : Prop := copyCount A=0

theorem rows_distinct {i j : Fin 3} (he : ∀ k, fixedH i k=fixedH j k) : i=j := by
  fin_cases i <;> fin_cases j <;> simp_all [fixedH, Fin.forall_fin_succ]

theorem columns_distinct {i j : Fin 3} (he : ∀ k, fixedH k i=fixedH k j) : i=j := by
  fin_cases i <;> fin_cases j <;> simp_all [fixedH, Fin.forall_fin_succ]

end
end OrderedRemoval.Crown
