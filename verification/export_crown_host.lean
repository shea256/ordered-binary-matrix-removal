/- Executable semantic cross-check input, not an all-depth certificate.
Exports the actual Lean entry rules and both raw axis orders. -/
import OrderedRemoval.Crown.OrderedHost
import Lean.Data.Json

open OrderedRemoval OrderedRemoval.Concrete OrderedRemoval.Crown

def crownPositions (h : ℕ) : List (Position h) :=
  ((List.finRange (6*h)).flatMap fun t => (List.finRange 2).flatMap fun g =>
    (List.finRange (2^h)).map fun x => .inl (t,g,x)) ++
  ((List.finRange (2*h+1)).flatMap fun c => (List.finRange (2^h)).map fun x =>
    .inr (.inl (c,x))) ++
  ((List.finRange (2^h)).map fun x => .inr (.inr x))

def crownRowList (h : ℕ) : List (Position h) :=
  (crownPositions h).mergeSort (fun r s =>
    @decide (@LE.le _ (Crown.OrderedHost.rowOrder h).toLE r s)
      ((Crown.OrderedHost.rowOrder h).toDecidableLE r s))

def crownColumnList (h : ℕ) : List (Position h) :=
  (crownPositions h).mergeSort (fun r s =>
    @decide (@LE.le _ (Crown.OrderedHost.columnOrder h).toLE r s)
      ((Crown.OrderedHost.columnOrder h).toDecidableLE r s))

def crownPositionCode {h : ℕ} : Position h → List ℕ
  | .inl (t,g,x) => [0,t.val,g.val,x.val]
  | .inr (.inl (c,x)) => [1,c.val,x.val]
  | .inr (.inr x) => [2,x.val]

def exportCrown (h : ℕ) : IO Unit := do
  let rs := crownRowList h
  let cs := crownColumnList h
  let obj := Lean.Json.mkObj [
    ("h",Lean.toJson h),
    ("rows",Lean.toJson (rs.map crownPositionCode)),
    ("columns",Lean.toJson (cs.map crownPositionCode)),
    ("entries",Lean.toJson (rs.map fun r => cs.map fun c => if Crown.host r c then 1 else (0:ℕ))) ]
  IO.println obj.compress

#eval ([0,1,2,3] : List ℕ).forM exportCrown
