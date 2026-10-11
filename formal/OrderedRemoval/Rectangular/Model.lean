import OrderedRemoval.Model

namespace OrderedRemoval.Rectangular
noncomputable section

abbrev Pattern := Fin 3 → Fin 4 → Bool

def fixedH : Pattern := ![![true,false,false,true], ![true,false,true,false], ![false,true,true,true]]

def orderedCopies {n : ℕ} (A : BinaryMatrix n) :
    Finset (IncreasingMap 3 n × IncreasingMap 4 n) := by
  classical
  exact Finset.univ.filter (fun rc => ∀ i j, A (rc.1.val i) (rc.2.val j)=fixedH i j)

def copyCount {n : ℕ} (A : BinaryMatrix n) : ℕ := (orderedCopies A).card

def HFree {n : ℕ} (A : BinaryMatrix n) : Prop := copyCount A=0

theorem rows_distinct {i j : Fin 3} (he : ∀ k, fixedH i k=fixedH j k) : i=j := by
  fin_cases i <;> fin_cases j <;> simp_all [fixedH, Fin.forall_fin_succ]

theorem columns_distinct {i j : Fin 4} (he : ∀ k, fixedH k i=fixedH k j) : i=j := by
  fin_cases i <;> fin_cases j <;> simp_all [fixedH, Fin.forall_fin_succ]

end
end OrderedRemoval.Rectangular
