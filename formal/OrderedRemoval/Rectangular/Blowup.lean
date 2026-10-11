import OrderedRemoval.Rectangular.Model

namespace OrderedRemoval.Rectangular
noncomputable section

/-- Replace each row and column by q consecutive twins. -/
def blowup {n : ℕ} (A : BinaryMatrix n) (q : ℕ) : BinaryMatrix (n*q) :=
  fun r c => A r.divNat c.divNat

def liftIndex {n q : ℕ} (u : Fin q) (r : Fin n) : Fin (n*q) :=
  finProdFinEquiv (r,u)

@[simp] theorem liftIndex_div {n q : ℕ} (u : Fin q) (r : Fin n) :
    (liftIndex u r).divNat=r :=
  congrArg Prod.fst (finProdFinEquiv.symm_apply_apply (r,u))

theorem liftIndex_strictMono {n q : ℕ} (u : Fin q) : StrictMono (@liftIndex n q u) := by
  intro r s hrs
  have hq : 0<q := Nat.zero_lt_of_lt u.isLt
  change u.val+q*r.val<u.val+q*s.val
  exact Nat.add_lt_add_left (Nat.mul_lt_mul_of_pos_left hrs hq) _

def restrict {n q : ℕ} (B : BinaryMatrix (n*q)) (u v : Fin q) : BinaryMatrix n :=
  fun r c => B (liftIndex u r) (liftIndex v c)

theorem restrict_HFree {n q : ℕ} {B : BinaryMatrix (n*q)}
    (hB : HFree B) (u v : Fin q) : HFree (restrict B u v) := by
  classical
  change (orderedCopies (restrict B u v)).card=0
  apply Finset.card_eq_zero.mpr
  apply Finset.eq_empty_of_forall_notMem
  intro rc hrc
  have he : ∀ i j, restrict B u v (rc.1.val i) (rc.2.val j)=fixedH i j := by
    simpa [orderedCopies] using hrc
  let rr : IncreasingMap 3 (n*q) := ⟨liftIndex u ∘ rc.1.val,(liftIndex_strictMono u).comp rc.1.property⟩
  let cc : IncreasingMap 4 (n*q) := ⟨liftIndex v ∘ rc.2.val,(liftIndex_strictMono v).comp rc.2.property⟩
  have hmem : (rr,cc)∈orderedCopies B := by
    simp only [orderedCopies,Finset.mem_filter,Finset.mem_univ,true_and]
    exact he
  have hpos : 0<copyCount B := Finset.card_pos.mpr ⟨(rr,cc),hmem⟩
  exact (Nat.ne_of_gt hpos) hB

theorem hammingDistance_eq_sum {n : ℕ} (A B : BinaryMatrix n) :
    hammingDistance A B=∑ r, ∑ c, if A r c≠B r c then 1 else 0 := by
  classical
  simp only [hammingDistance,Finset.card_eq_sum_ones,Finset.sum_filter,Fintype.sum_prod_type]

/-- Every cell occurs in exactly one of the q² offset slices. -/
theorem blowup_hamming_sum {n q : ℕ} (A : BinaryMatrix n) (B : BinaryMatrix (n*q)) :
    hammingDistance (blowup A q) B=∑ u : Fin q, ∑ v : Fin q,
      hammingDistance A (restrict B u v) := by
  classical
  simp_rw [hammingDistance_eq_sum]
  rw [← (finProdFinEquiv : Fin n×Fin q≃Fin (n*q)).sum_comp]
  simp only [Fintype.sum_prod_type]
  conv_lhs =>
    arg 2
    ext r
    arg 2
    ext u
    rw [← (finProdFinEquiv : Fin n×Fin q≃Fin (n*q)).sum_comp]
  simp only [Fintype.sum_prod_type]
  change (∑ r, ∑ u : Fin q, ∑ c, ∑ v : Fin q,
      if A (liftIndex u r).divNat (liftIndex v c).divNat≠B (liftIndex u r) (liftIndex v c)
      then 1 else 0) = _
  simp only [liftIndex_div,restrict]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro u hu
  calc
    (∑ r, ∑ c, ∑ v : Fin q, if A r c≠B (liftIndex u r) (liftIndex v c) then 1 else 0)
      = ∑ r, ∑ v : Fin q, ∑ c, if A r c≠B (liftIndex u r) (liftIndex v c) then 1 else 0 := by
        apply Finset.sum_congr rfl
        intro r hr
        exact Finset.sum_comm
    _ = _ := Finset.sum_comm

/-- Arbitrary-repair distance grows by at least q² under uniform blowup. -/
theorem blowup_repair_lower_bound {n q M : ℕ} (A : BinaryMatrix n)
    (hA : ∀ B : BinaryMatrix n, HFree B → M≤hammingDistance A B)
    (B : BinaryMatrix (n*q)) (hB : HFree B) :
    q^2*M≤hammingDistance (blowup A q) B := by
  classical
  rw [blowup_hamming_sum]
  have hs := Finset.sum_le_sum (s:=Finset.univ) (fun u _ =>
    Finset.sum_le_sum (s:=Finset.univ) (fun v _ => hA _ (restrict_HFree hB u v)))
  simpa [pow_two,Nat.mul_assoc] using hs

/-- The normalized repair lower bound is unchanged by uniform blowup. -/
theorem blowup_repair_normalized {n q : ℕ} (A : BinaryMatrix n) (ε : ℝ)
    (hA : ∀ B : BinaryMatrix n, HFree B → ε*(n:ℝ)^2≤(hammingDistance A B:ℝ))
    (B : BinaryMatrix (n*q)) (hB : HFree B) :
    ε*((n*q:ℕ):ℝ)^2≤(hammingDistance (blowup A q) B:ℝ) := by
  classical
  rw [blowup_hamming_sum]
  push_cast
  have hs := Finset.sum_le_sum (s:=Finset.univ) (fun u : Fin q => fun _ =>
    Finset.sum_le_sum (s:=Finset.univ) (fun v : Fin q => fun _ => hA _ (restrict_HFree hB u v)))
  calc
    ε*((n:ℝ)*q)^2=(q:ℝ)*((q:ℝ)*(ε*(n:ℝ)^2)) := by ring
    _ ≤ _ := by simpa using hs

/-- Distinct pattern rows force the projected row map to remain injective. -/
theorem projected_rows_strict {n q : ℕ} (A : BinaryMatrix n)
    (r : IncreasingMap 3 (n*q)) (c : IncreasingMap 4 (n*q))
    (he : ∀ i j, blowup A q (r.val i) (c.val j)=fixedH i j) :
    StrictMono (fun i => (r.val i).divNat) := by
  have hm : Monotone (fun i => (r.val i).divNat) := by
    intro i j hij
    exact Nat.div_le_div_right (r.property.monotone hij)
  apply hm.strictMono_of_injective
  intro i j hij
  apply rows_distinct
  intro k
  rw [←he i k,←he j k]
  exact congrArg (fun x => A x (c.val k).divNat) hij

theorem projected_cols_strict {n q : ℕ} (A : BinaryMatrix n)
    (r : IncreasingMap 3 (n*q)) (c : IncreasingMap 4 (n*q))
    (he : ∀ i j, blowup A q (r.val i) (c.val j)=fixedH i j) :
    StrictMono (fun j => (c.val j).divNat) := by
  have hm : Monotone (fun j => (c.val j).divNat) := by
    intro i j hij
    exact Nat.div_le_div_right (c.property.monotone hij)
  apply hm.strictMono_of_injective
  intro i j hij
  apply columns_distinct
  intro k
  rw [←he k i,←he k j]
  exact congrArg (A (r.val k).divNat) hij

/-- Project a copy, retaining its seven within-twin offsets. -/
theorem blowup_copyCount_le {n q : ℕ} (A : BinaryMatrix n) :
    copyCount (blowup A q)≤copyCount A*q^7 := by
  classical
  let project : orderedCopies (blowup A q) → orderedCopies A := fun rc => by
    have he : ∀ i j, blowup A q (rc.val.1.val i) (rc.val.2.val j)=fixedH i j := by
      simpa [orderedCopies] using rc.property
    let rr : IncreasingMap 3 n := ⟨fun i => (rc.val.1.val i).divNat,
      projected_rows_strict A _ _ he⟩
    let cc : IncreasingMap 4 n := ⟨fun j => (rc.val.2.val j).divNat,
      projected_cols_strict A _ _ he⟩
    exact ⟨(rr,cc),by simpa [orderedCopies,rr,cc,blowup] using he⟩
  let encode : orderedCopies (blowup A q) →
      orderedCopies A × ((Fin 3→Fin q) × (Fin 4→Fin q)) := fun rc =>
    (project rc,(fun i => (rc.val.1.val i).modNat,fun j => (rc.val.2.val j).modNat))
  have hinj : Function.Injective encode := by
    intro x y he
    apply Subtype.ext
    apply Prod.ext
    · apply Subtype.ext
      funext i
      apply (finProdFinEquiv : Fin n×Fin q≃Fin (n*q)).symm.injective
      apply Prod.ext
      · exact congrArg (fun z => z.1.val.1.val i) he
      · exact congrArg (fun z => z.2.1 i) he
    · apply Subtype.ext
      funext j
      apply (finProdFinEquiv : Fin n×Fin q≃Fin (n*q)).symm.injective
      apply Prod.ext
      · exact congrArg (fun z => z.1.val.2.val j) he
      · exact congrArg (fun z => z.2.2 j) he
  have hc := Fintype.card_le_of_injective encode hinj
  simpa only [copyCount,Fintype.card_coe,Fintype.card_prod,Fintype.card_fun,
    Fintype.card_fin,←pow_add] using hc

end
end OrderedRemoval.Rectangular
