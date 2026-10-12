import OrderedRemoval.Crown.Complete
set_option pp.fullNames true
#check @OrderedRemoval.Crown.no_polynomial_removal_bound
#check @OrderedRemoval.Crown.concrete_host_bounds
#check @OrderedRemoval.Crown.Copy.zero_localization
#print axioms OrderedRemoval.Crown.no_polynomial_removal_bound
#eval (List.finRange 3).map fun i => (List.finRange 3).map fun j =>
  if OrderedRemoval.Crown.fixedH i j then 1 else (0 : Nat)
